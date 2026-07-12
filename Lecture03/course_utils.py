from pathlib import Path
import ast, base64, json, os, re
import pandas as pd
import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")
GPT_OSS_MODEL = os.getenv("GPT_OSS_MODEL_NAME", "openai/gpt-oss-120b")
GEMMA_MODEL = os.getenv("GEMMA_MODEL_NAME", "google/gemma-4-31b-it")

def require_cillm_config():
    missing = [name for name in ("CILLM_API_KEY", "CILLM_BASE_URL") if not os.getenv(name)]
    if missing:
        raise RuntimeError("缺少 CILLM 必要設定：" + ", ".join(missing) + "。請複製 .env.example 為 .env，填入設定後重新啟動 Kernel。")
    if GPT_OSS_MODEL != "openai/gpt-oss-120b":
        print(f"提醒：目前 GPT_OSS_MODEL_NAME={GPT_OSS_MODEL}，本教材指定模型為 openai/gpt-oss-120b。")
    return {"base_url": os.getenv("CILLM_BASE_URL"), "model": GPT_OSS_MODEL}

def show(data): print(json.dumps(data, ensure_ascii=False, indent=2, default=str))
def normalize(kind, source, content, **extra): return {"type": kind, "source": Path(source).name, "content": content, **extra}
def parse_text(path): return normalize("text", path, Path(path).read_text(encoding="utf-8"))
def parse_excel(path):
    book = pd.ExcelFile(path); sheets = {}
    for name in book.sheet_names:
        df = pd.read_excel(path, sheet_name=name)
        sheets[name] = {"columns": list(df.columns), "rows": df.where(pd.notna(df), None).to_dict("records")}
    return normalize("excel", path, sheets)
def transcribe_audio(path):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("尚未安裝 faster-whisper；請先安裝後再執行語音轉錄。")
        return normalize("audio", path, "", error="missing_faster_whisper")
    try:
        model = WhisperModel("tiny", device="cpu", compute_type="int8")
        segments, _ = model.transcribe(str(path), language="zh")
        return normalize("audio", path, "".join(s.text for s in segments))
    except Exception as e:
        print(f"語音轉錄失敗：{e}"); return normalize("audio", path, "", error=str(e))

def call_chat(model, messages, max_tokens=800, timeout=60):
    require_cillm_config()
    key, base = os.getenv("CILLM_API_KEY"), os.getenv("CILLM_BASE_URL")
    try:
        r = requests.post(base.rstrip("/") + "/chat/completions", headers={"Authorization": f"Bearer {key}"}, json={"model": model, "messages": messages, "max_tokens": max_tokens}, timeout=timeout)
        r.raise_for_status(); return r.json()["choices"][0]["message"]["content"]
    except requests.RequestException as e:
        raise RuntimeError(f"CILLM API 呼叫失敗：{e}") from e
def ask_gpt_oss(question, context="", instruction="請使用繁體中文簡潔回答。", max_tokens=800):
    messages = [{"role":"system", "content":instruction}]
    content = question + ("\n\n可用內容：\n" + context if context else "")
    messages.append({"role":"user", "content":content})
    return call_chat("openai/gpt-oss-120b", messages, max_tokens=max_tokens)
def analyze_image(path, question="請用繁體中文描述圖片"):
    require_cillm_config()
    model = GEMMA_MODEL
    mime = "image/png" if str(path).lower().endswith("png") else "image/jpeg"
    uri = f"data:{mime};base64," + base64.b64encode(Path(path).read_bytes()).decode()
    content = call_chat(model, [{"role":"user","content":[{"type":"text","text":question},{"type":"image_url","image_url":{"url":uri}}]}])
    return normalize("image", path, content)

def math_tool(a, op, b):
    ops = {"+": lambda: a+b, "-": lambda: a-b, "*": lambda: a*b, "/": lambda: a/b}
    if op not in ops: raise ValueError("只允許 + - * /")
    return ops[op]()

BLOCKED = ("import ", "__", "open(", "exec(", "eval(", "compile(", "os.", "sys.", "subprocess", "socket", "requests", "http", "unlink", "remove", "rmdir", "shell")
def safe_excel_python(path, code):
    low = code.lower()
    if any(x in low for x in BLOCKED): raise ValueError("程式碼含禁止的 import、檔案、網路或系統操作")
    tree = ast.parse(code, mode="exec")
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)): raise ValueError("此教學沙箱禁止 import")
    env = {"pd": pd, "np": __import__("numpy"), "excel_path": str(path), "print": print, "len": len, "sum": sum, "min": min, "max": max, "round": round, "sorted": sorted, "list": list, "dict": dict}
    exec(compile(tree, "<excel-tool>", "exec"), {"__builtins__": {}}, env)
    return env.get("result", "程式已執行，但未設定 result")

TOOL_REGISTRY = {
 "math_tool": {"description":"基本加減乘除", "function":math_tool},
 "image_tool": {"description":"使用 Gemma 分析圖片", "function":analyze_image},
 "excel_python_tool": {"description":"以受限 pandas 程式分析 Excel", "function":safe_excel_python}}

RESOURCE_CATALOG = {
 "company_information": ("public/company_information.txt", ["公司","客服","樞紐"]),
 "passenger_service_rules": ("public/passenger_service_rules.txt", ["旅客","登機","行李","延誤","補償","餐點"]),
 "flight_operations_guide": ("operations/flight_operations_guide.txt", ["航班","航務","起飛","雷雨","飛航"]),
 "maintenance_guidelines": ("maintenance/maintenance_guidelines.txt", ["維修","機務","零件","工單","航材"]),
 "it_security_policy": ("it/it_security_policy.txt", ["資安","API key","密碼","帳號","資料"]),
 "employee_policy": ("employee/employee_policy.txt", ["員工","請假","訓練","設備","加班"])}
def choose_resource(question):
    scores = {k: sum(word.lower() in question.lower() for word in words) for k, (_, words) in RESOURCE_CATALOG.items()}
    return max(scores, key=scores.get) if max(scores.values()) else "company_information"
def load_resource(name):
    rel = RESOURCE_CATALOG[name][0]
    return (ROOT / "resources" / rel).read_text(encoding="utf-8")
def search_resource(name, query):
    lines = load_resource(name).splitlines(); terms = [x for x in re.findall(r"[\w\u4e00-\u9fff]+", query) if len(x)>1]
    hits = [line for line in lines if any(t in line for t in terms)]
    return "\n".join(hits or lines[:4])

ROLE_PERMISSIONS = {
 "guest":{"tools":["math_tool"],"resources":["company_information","passenger_service_rules"]},
 "employee":{"tools":["math_tool"],"resources":["company_information","passenger_service_rules","employee_policy"]},
 "operations":{"tools":["math_tool","image_tool","excel_python_tool"],"resources":["company_information","passenger_service_rules","flight_operations_guide"]},
 "maintenance":{"tools":["math_tool","image_tool"],"resources":["company_information","maintenance_guidelines"]},
 "developer":{"tools":["math_tool","image_tool","excel_python_tool"],"resources":["company_information","it_security_policy","employee_policy"]},
 "admin":{"tools":list(TOOL_REGISTRY),"resources":list(RESOURCE_CATALOG)}}
def authorize(role, kind, name): return name in ROLE_PERMISSIONS.get(role, {}).get(kind, [])
def print_execution_trace(**items):
    print("="*30 + "\nAI Agent 執行追蹤\n" + "="*30)
    labels={"question":"使用者問題","normalized":"已取得的標準化資料","tool":"是否需要工具","resource":"是否需要資源","role":"目前角色","tool_auth":"工具權限檢查","resource_auth":"資源權限檢查","aes":"AES 解密","tool_result":"工具執行結果","answer":"最終回答"}
    for k,v in items.items(): print(f"{labels.get(k,k)}：\n{v}\n")
    print("="*30)

def encrypt_resource(source, target, key_b64):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    import os
    key=base64.urlsafe_b64decode(key_b64); nonce=os.urandom(12)
    if len(key)!=32: raise ValueError("AES_KEY 解碼後必須是 32 bytes")
    Path(target).write_bytes(nonce + AESGCM(key).encrypt(nonce, Path(source).read_bytes(), None))
def decrypt_resource(path, key_b64):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    raw=Path(path).read_bytes(); key=base64.urlsafe_b64decode(key_b64)
    return AESGCM(key).decrypt(raw[:12], raw[12:], None).decode("utf-8")
