from pathlib import Path
import ast, base64, getpass, hashlib, json, os, re
from typing import List
import pandas as pd
import requests
from dotenv import load_dotenv
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")
GPT_OSS_MODEL = os.getenv("GPT_OSS_MODEL_NAME", "openai/gpt-oss-120b")
GEMMA_MODEL = os.getenv("GEMMA_MODEL_NAME", "google/gemma-4-31b-it")
OPENAI_MODEL = os.getenv("OPENAI_MODEL_NAME", "gpt-4o")
DEFAULT_CILLM_BASE_URL = "https://cillmtest.china-airlines.com/v1"
OPENAI_BASE_URL = "https://api.openai.com/v1"
CILLM_HEADERS = {
    "X-User-ID": os.getenv("CILLM_USER_ID", "admin"),
    "X-Platform": os.getenv("CILLM_PLATFORM", "edu-demo"),
    "X-Agent": os.getenv("CILLM_AGENT", "cal-edu-notebook"),
}

def prompt_for_cillm_api_key():
    """若 .env 未提供 Key，於 Notebook 中以隱藏輸入要求使用者輸入。"""
    key = os.getenv("CILLM_API_KEY", "").strip()
    if not key:
        key = getpass.getpass("請輸入 CILLM_API_KEY（輸入內容不會顯示）：").strip()
        if not key:
            raise RuntimeError("未輸入 CILLM_API_KEY，無法繼續執行教材。")
        os.environ["CILLM_API_KEY"] = key
    return key

def get_llm_config(prompt_if_missing=True):
    """CILLM 優先；未設定 CILLM 時才使用 OpenAI。"""
    if os.getenv("CILLM_API_KEY", "").strip():
        return {
            "provider": "cillm",
            "api_key": os.environ["CILLM_API_KEY"].strip(),
            "base_url": os.getenv("CILLM_BASE_URL") or DEFAULT_CILLM_BASE_URL,
            "model": GPT_OSS_MODEL,
        }
    if os.getenv("OPENAI_API_KEY", "").strip():
        return {
            "provider": "openai",
            "api_key": os.environ["OPENAI_API_KEY"].strip(),
            "base_url": OPENAI_BASE_URL,
            "model": OPENAI_MODEL,
        }
    if prompt_if_missing:
        prompt_for_cillm_api_key()
        return get_llm_config(prompt_if_missing=False)
    raise RuntimeError("未設定 CILLM_API_KEY 或 OPENAI_API_KEY。")

def prompt_for_aes_key():
    """若 .env 未提供 AES_KEY，於 Notebook 中以隱藏輸入要求使用者輸入。"""
    key = os.getenv("AES_KEY", "").strip()
    if not key:
        key = getpass.getpass("請貼上 AES_KEY（URL-safe Base64，通常為 44 字元；輸入不會顯示）：").strip()
        if not key:
            raise RuntimeError("未輸入 AES_KEY，無法繼續執行 AES 教材。")
        os.environ["AES_KEY"] = key
    try:
        decoded = base64.urlsafe_b64decode(key)
    except Exception as e:
        raise RuntimeError("AES_KEY 格式錯誤。請先執行 Notebook 的『產生 AES-256 測試 Key』Cell，再完整貼上產生的字串。") from e
    if len(decoded) != 32:
        raise RuntimeError(f"AES_KEY 解碼後是 {len(decoded)} bytes，必須是 32 bytes（AES-256）。請重新產生測試 Key。")
    return key

def require_cillm_config():
    if not os.getenv("CILLM_API_KEY"):
        raise RuntimeError("缺少 CILLM_API_KEY。請複製 .env.example 為 .env，填入 Key 後重新啟動 Kernel。")
    if GPT_OSS_MODEL != "openai/gpt-oss-120b":
        print(f"提醒：目前 GPT_OSS_MODEL_NAME={GPT_OSS_MODEL}，本教材指定模型為 openai/gpt-oss-120b。")
    return {"base_url": os.getenv("CILLM_BASE_URL") or DEFAULT_CILLM_BASE_URL, "model": GPT_OSS_MODEL}

def show(data): print(json.dumps(data, ensure_ascii=False, indent=2, default=str))
def normalize(kind, source, content, **extra): return {"type": kind, "source": Path(source).name, "content": content, **extra}
def parse_text(path): return normalize("text", path, Path(path).read_text(encoding="utf-8"))

def preview_text(path):
    content = Path(path).read_text(encoding="utf-8")
    print(content)
    return content

def preview_image(path):
    from IPython.display import Image, display
    display(Image(filename=str(path)))

def preview_audio(path):
    from IPython.display import Audio, display
    display(Audio(filename=str(path)))

def preview_excel(path):
    from IPython.display import display
    book = pd.ExcelFile(path)
    for sheet in book.sheet_names:
        print(f"Sheet：{sheet}")
        display(pd.read_excel(path, sheet_name=sheet))

def _display_value(value):
    if pd.isna(value): return "空值"
    if isinstance(value, float) and value.is_integer(): return str(int(value))
    return str(value)

def parse_excel(path):
    book = pd.ExcelFile(path); rows_as_text = []
    for name in book.sheet_names:
        df = pd.read_excel(path, sheet_name=name)
        for _, row in df.iterrows():
            fields = [f"{column} 是 {_display_value(row[column])}" for column in df.columns]
            rows_as_text.append("、".join(fields))
    return normalize("text", path, "\n".join(rows_as_text))
def transcribe_audio(path):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("尚未安裝 faster-whisper；請先安裝後再執行語音轉錄。")
        return normalize("audio", path, "", error="missing_faster_whisper")
    try:
        model = WhisperModel("tiny", device="cpu", compute_type="int8")
        segments, _ = model.transcribe(str(path), language="zh")
        content = "".join(s.text for s in segments).strip()
        if not content:
            return normalize("audio", path, "", error="未辨識到語音內容；請確認音檔不是靜音且確實含有人聲。")
        return normalize("audio", path, content)
    except Exception as e:
        print(f"語音轉錄失敗：{e}"); return normalize("audio", path, "", error=str(e))

def call_chat(model, messages, max_tokens=800, timeout=60, response_format=None):
    config = get_llm_config()
    key, base = config["api_key"], config["base_url"]
    selected_model = model if config["provider"] == "cillm" else config["model"]
    try:
        headers = {"Authorization": f"Bearer {key}"}
        if config["provider"] == "cillm": headers.update(CILLM_HEADERS)
        payload = {"model": selected_model, "messages": messages, "max_tokens": max_tokens}
        if response_format is not None: payload["response_format"] = response_format
        r = requests.post(base.rstrip("/") + "/chat/completions", headers=headers, json=payload, timeout=timeout)
        r.raise_for_status(); return r.json()["choices"][0]["message"]["content"]
    except requests.RequestException as e:
        raise RuntimeError(f"CILLM API 呼叫失敗：{e}") from e

def get_current_key_scopes(timeout=30):
    """查詢目前 CILLM Key 實際具備的 RBAC scopes。"""
    if get_llm_config()["provider"] == "openai":
        return None
    config = require_cillm_config()
    headers = {"Authorization": f"Bearer {os.environ['CILLM_API_KEY']}", **CILLM_HEADERS}
    try:
        r = requests.get(
            config["base_url"].rstrip("/") + "/rbac/keys/current",
            headers=headers,
            timeout=timeout,
        )
        r.raise_for_status()
        info = r.json()
    except requests.RequestException as e:
        raise RuntimeError(f"無法查詢 CILLM Key scopes：{e}") from e
    scopes = info.get("scopes", [])
    if not isinstance(scopes, list):
        raise RuntimeError("CILLM 回傳的 scopes 格式不正確。")
    return scopes

def verify_cillm_key(timeout=30):
    """依優先順序驗證 CILLM 或 OpenAI Key、端點與模型。"""
    config = get_llm_config()
    try:
        reply = call_chat(
            config["model"],
            [{"role": "user", "content": "請只回答：API 連線成功"}],
            max_tokens=32,
            timeout=timeout,
        )
    except RuntimeError as e:
        raise RuntimeError(f"{config['provider']} Key 驗證失敗，請確認 .env 與連線環境。") from e
    return {k: v for k, v in config.items() if k != "api_key"} | {"reply": reply}
def ask_gpt_oss(question, context="", instruction="請使用繁體中文簡潔回答。", max_tokens=800):
    messages = [{"role":"system", "content":instruction}]
    content = question + ("\n\n可用內容：\n" + context if context else "")
    messages.append({"role":"user", "content":content})
    return call_chat("openai/gpt-oss-120b", messages, max_tokens=max_tokens)
def analyze_image(path, question="請用繁體中文描述圖片"):
    config = get_llm_config()
    model = GEMMA_MODEL if config["provider"] == "cillm" else config["model"]
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
 "math_tool": {
     "description":"需要精確執行兩個數值的加、減、乘、除時使用；arguments 必須包含 a、op、b。",
     "arguments_example":{"a":312,"op":"*","b":0.87}, "function":math_tool},
 "image_tool": {
     "description":"問題必須查看圖片像素、辨識圖片文字或理解視覺內容時使用；arguments 必須包含 question。",
     "arguments_example":{"question":"圖片中的航班與登機門是什麼？"}, "function":analyze_image},
 "excel_python_tool": {
     "description":"需要對 Excel 表格做精確篩選、排序、統計、分組或聚合時使用；arguments 必須包含 question。",
     "arguments_example":{"question":"依部門計算平均延誤"}, "function":safe_excel_python}}

class ToolRouteResult(BaseModel):
    tool_name: str = Field(description="選擇 TOOL_REGISTRY 中的一個工具名稱；不需要工具時填 none")
    reason: str = Field(default="模型未提供選擇理由", description="根據工具 description 說明選擇理由")
    arguments: dict = Field(default_factory=dict, description="傳給工具的參數")

class MathToolArguments(BaseModel):
    a: float
    op: str
    b: float

class ImageToolArguments(BaseModel):
    question: str

class ExcelToolArguments(BaseModel):
    question: str

class GeneratedExcelCode(BaseModel):
    code: str = Field(description="可直接執行且最後設定 result 的 pandas 程式碼")
    reason: str = Field(default="模型未提供程式說明", description="程式如何回答問題")

def describe_available_context():
    """自動盤點教材中的資料檔、Excel 欄位與可用 Resources。"""
    parts = []
    data_root = ROOT / "data"
    for kind in ("text", "images", "audio"):
        folder = data_root / kind
        files = sorted(path.name for path in folder.glob("*") if path.is_file())
        if files: parts.append(f"可用 {kind} 檔案：{', '.join(files)}")
    excel_folder = data_root / "excel"
    for path in sorted(excel_folder.glob("*.xlsx")):
        try:
            book = pd.ExcelFile(path)
            sheet_details = []
            for sheet in book.sheet_names:
                columns = list(pd.read_excel(path, sheet_name=sheet, nrows=0).columns)
                sheet_details.append(f"{sheet} 欄位={columns}")
            parts.append(f"可用 Excel：{path.name}（{'；'.join(sheet_details)}）")
        except Exception as error:
            parts.append(f"可用 Excel：{path.name}（欄位讀取失敗：{error}）")
    resources = [f"{name}: {description}" for name, description in RESOURCE_DESCRIPTIONS.items()]
    parts.append("可用 Resources：" + "；".join(resources))
    return "\n".join(parts)

def _merge_available_context(extra_context=""):
    discovered = describe_available_context()
    return discovered + (f"\n任務額外上下文：{extra_context}" if extra_context else "")

def call_structured(model_class, prompt, max_tokens=800):
    """使用 LangChain with_structured_output，直接取得經 Pydantic 驗證的物件。"""
    try:
        from langchain_openai import ChatOpenAI
    except ImportError as e:
        raise RuntimeError("尚未安裝 langchain-openai；請執行 pip install -r requirements.txt 後重啟 Kernel。") from e
    config = get_llm_config()
    kwargs = {
        "model": config["model"],
        "api_key": config["api_key"],
        "base_url": config["base_url"],
        "temperature": 0,
        "max_tokens": max_tokens,
    }
    if config["provider"] == "cillm": kwargs["default_headers"] = CILLM_HEADERS
    llm = ChatOpenAI(**kwargs)
    # Router 的 arguments 會依 Tool 改變，不能使用 OpenAI native json_schema
    # 對 arbitrary dict 的 additionalProperties:false 限制；改由 json_mode + Pydantic 驗證。
    structured_llm = llm.with_structured_output(model_class, method="json_mode", include_raw=True)
    result = structured_llm.invoke(prompt)
    if result.get("parsing_error") is not None:
        raw = getattr(result.get("raw"), "content", result.get("raw"))
        raise RuntimeError(f"LangChain structured output 解析失敗：{result['parsing_error']}；raw={raw}")
    if result.get("parsed") is None:
        raise RuntimeError("LangChain structured output 未回傳 parsed 結果。")
    return result["parsed"]

def route_tool(question, available_context="", max_tokens=500):
    available_context = _merge_available_context(available_context)
    tools = [{"name":name, "description":meta["description"], "arguments_example":meta["arguments_example"]} for name, meta in TOOL_REGISTRY.items()]
    prompt = (
        "你是 Tool Router。只能根據各工具的 description 判斷。一次先選一個最適合的工具；"
        "若問題不需要工具則 tool_name 填 none。請輸出符合 schema 的 JSON。\n\n"
        f"輸出 JSON Schema：{json.dumps(ToolRouteResult.model_json_schema(), ensure_ascii=False)}\n\n"
        f"工具：{json.dumps(tools, ensure_ascii=False)}\n\n可用輸入與環境：{available_context or '未提供'}\n\n使用者問題：{question}"
    )
    route = call_structured(ToolRouteResult, prompt, max_tokens=max_tokens)
    if route.tool_name != "none" and route.tool_name not in TOOL_REGISTRY:
        raise ValueError(f"模型選到不存在的工具：{route.tool_name}")
    return route

def validate_tool_arguments(route):
    models = {"math_tool":MathToolArguments, "image_tool":ImageToolArguments, "excel_python_tool":ExcelToolArguments}
    if route.tool_name == "none": return None
    return models[route.tool_name].model_validate(route.arguments)

def generate_excel_code(question, path, max_tokens=800):
    df = pd.read_excel(path)
    sample = df.head(3).where(pd.notna(df.head(3)), None).to_dict("records")
    prompt = f"""你是 pandas 程式碼產生器。請針對問題產生受限程式碼。
可用變數只有 pd 與 excel_path；必須用 pd.read_excel(excel_path) 讀檔，最後把答案存入 result。
禁止 import、檔案寫入、網路、系統操作、eval、exec。只輸出符合 schema 的 JSON。
輸出 JSON Schema：{json.dumps(GeneratedExcelCode.model_json_schema(), ensure_ascii=False)}
欄位：{list(df.columns)}
資料範例：{json.dumps(sample, ensure_ascii=False)}
問題：{question}"""
    return call_structured(GeneratedExcelCode, prompt, max_tokens=max_tokens)

RESOURCE_CATALOG = {
 "company_information": ("public/company_information.txt", ["公司","客服","樞紐"]),
 "passenger_service_rules": ("public/passenger_service_rules.txt", ["旅客","登機","行李","延誤","補償","餐點"]),
 "flight_operations_guide": ("operations/flight_operations_guide.txt", ["航班","航務","起飛","雷雨","飛航"]),
 "maintenance_guidelines": ("maintenance/maintenance_guidelines.txt", ["維修","機務","零件","工單","航材"]),
 "it_security_policy": ("it/it_security_policy.txt", ["資安","API key","密碼","帳號","資料"]),
 "employee_policy": ("employee/employee_policy.txt", ["員工","請假","訓練","設備","加班"])}

RESOURCE_DESCRIPTIONS = {
 "company_information":"一般公司資訊、客服時間、樞紐、服務語言與基本公司原則。",
 "passenger_service_rules":"旅客登機、行李、延誤、餐飲券、補償與特殊服務規定。",
 "flight_operations_guide":"航班、航務、起飛、飛航計畫、雷雨與異常通報作業。",
 "maintenance_guidelines":"機務維修、工單、零件、航材、工具與維修安全規定。",
 "it_security_policy":"API key、密碼、帳號、資料保護與資訊安全規定。",
 "employee_policy":"員工請假、訓練、設備借用、差旅與加班規定。",
}

class ResourceRouteResult(BaseModel):
    resource_name: str = Field(description="選擇 RESOURCE_CATALOG 中的一個資源名稱；不需要資源時填 none")
    reason: str = Field(default="模型未提供選擇理由", description="根據 Resource description 說明選擇理由")

class AgentRoutePlan(BaseModel):
    tools: List[str] = Field(default_factory=list, description="需要的 Tool 名稱，可為空或多個")
    resources: List[str] = Field(default_factory=list, description="需要的 Resource 名稱，可為空或多個")
    reason: str = Field(default="模型未提供規劃理由", description="說明為何需要這些 Tool 與 Resource")

def route_resource(question, available_context="", max_tokens=500):
    available_context = _merge_available_context(available_context)
    resources = [{"name":name, "description":description} for name, description in RESOURCE_DESCRIPTIONS.items()]
    prompt = ("你是 Resource Router。只能根據 Resource description 選擇一個最適合的資源；不需要資源時填 none。"
              "請輸出符合 schema 的 JSON。\n\n"
              f"輸出 JSON Schema：{json.dumps(ResourceRouteResult.model_json_schema(), ensure_ascii=False)}\n\n"
              f"資源：{json.dumps(resources, ensure_ascii=False)}\n\n可用輸入與環境：{available_context or '未提供'}\n\n使用者問題：{question}")
    route = call_structured(ResourceRouteResult, prompt, max_tokens=max_tokens)
    if route.resource_name != "none" and route.resource_name not in RESOURCE_CATALOG:
        raise ValueError(f"模型選到不存在的資源：{route.resource_name}")
    return route

def route_agent(question, available_context="", max_tokens=700):
    available_context = _merge_available_context(available_context)
    tools = [{"name":name, "description":meta["description"]} for name, meta in TOOL_REGISTRY.items()]
    resources = [{"name":name, "description":description} for name, description in RESOURCE_DESCRIPTIONS.items()]
    prompt = ("你是 Agent Router。根據 descriptions 規劃回答問題需要的 Tools 與 Resources；兩者都可為空或多個。"
              "精確計算、圖片理解或 Excel 分析選 Tool；公司規定與內部知識選 Resource。請輸出符合 schema 的 JSON。\n\n"
              f"輸出 JSON Schema：{json.dumps(AgentRoutePlan.model_json_schema(), ensure_ascii=False)}\n\n"
              f"Tools：{json.dumps(tools, ensure_ascii=False)}\nResources：{json.dumps(resources, ensure_ascii=False)}\n\n可用輸入與環境：{available_context or '未提供'}\n\n使用者問題：{question}")
    plan = call_structured(AgentRoutePlan, prompt, max_tokens=max_tokens)
    invalid_tools = [name for name in plan.tools if name not in TOOL_REGISTRY]
    invalid_resources = [name for name in plan.resources if name not in RESOURCE_CATALOG]
    if invalid_tools or invalid_resources:
        raise ValueError(f"模型回傳不存在的能力：tools={invalid_tools}, resources={invalid_resources}")
    return plan

def find_named_data_file(kind, question, suffixes):
    folder = ROOT / "data" / kind
    candidates = [path for path in folder.glob("*") if path.is_file() and path.suffix.lower() in suffixes]
    mentioned = [path for path in candidates if path.name.lower() in question.lower()]
    if mentioned: return mentioned[0]
    if len(candidates) == 1: return candidates[0]
    raise RuntimeError(f"問題未指定要使用哪個 {kind} 檔案；可用檔案：{[path.name for path in candidates]}")

def execute_agent(question):
    """完成 Plan、Resource retrieval、Tool execution 與 final answer 的教學 Agent。"""
    plan = route_agent(question)
    resource_results = {}
    for resource_name in plan.resources:
        resource_results[resource_name] = search_resource(resource_name, question)
    resource_context = "\n\n".join(f"[{name}]\n{content}" for name, content in resource_results.items())

    tool_results = {}
    generated_codes = {}
    for tool_name in plan.tools:
        if tool_name == "image_tool":
            path = find_named_data_file("images", question, {".png", ".jpg", ".jpeg"})
            args = ImageToolArguments(question=question)
            tool_results[tool_name] = analyze_image(path, args.question)
        elif tool_name == "excel_python_tool":
            path = find_named_data_file("excel", question, {".xlsx", ".xlsm", ".xls"})
            args = ExcelToolArguments(question=question)
            code_request = args.question + (f"\n\n必須套用的 Resource 條文：\n{resource_context}" if resource_context else "")
            generated = generate_excel_code(code_request, path)
            generated_codes[tool_name] = generated.model_dump()
            tool_results[tool_name] = safe_excel_python(path, generated.code)
        elif tool_name == "math_tool":
            detail_route = route_tool(question)
            args = validate_tool_arguments(detail_route)
            tool_results[tool_name] = math_tool(args.a, args.op, args.b)

    evidence = "Resources：\n" + json.dumps(resource_results, ensure_ascii=False, default=str)
    evidence += "\n\nTool Results：\n" + json.dumps(tool_results, ensure_ascii=False, default=str)
    answer = ask_gpt_oss(question, evidence, "只能根據 Resource 與 Tool Results 回答，不可補造資料。請用繁體中文直接回覆使用者。")
    return {"question":question, "plan":plan.model_dump(), "resources":resource_results, "generated_codes":generated_codes, "tool_results":tool_results, "answer":answer}
def choose_resource(question):
    scores = {k: sum(word.lower() in question.lower() for word in words) for k, (_, words) in RESOURCE_CATALOG.items()}
    return max(scores, key=scores.get) if max(scores.values()) else "company_information"
def load_resource(name):
    rel = RESOURCE_CATALOG[name][0]
    return (ROOT / "resources" / rel).read_text(encoding="utf-8")

SEARCH_SYNONYMS = {
    "餐飲券": ["餐飲券", "餐點", "餐飲", "券"],
    "餐券": ["餐飲券", "餐點", "券"],
    "延遲": ["延誤", "延遲"],
    "行李不見": ["遺失行李", "行李"],
    "密碼": ["密碼", "帳號", "多因子"],
    "請假": ["請假", "病假", "年假"],
}

def search_resource(name, query):
    lines = load_resource(name).splitlines()
    catalog_keywords = RESOURCE_CATALOG[name][1]
    terms = {keyword for keyword in catalog_keywords if keyword.lower() in query.lower()}
    for phrase, synonyms in SEARCH_SYNONYMS.items():
        if phrase in query: terms.update(synonyms)
    ascii_terms = re.findall(r"[A-Za-z][A-Za-z0-9_-]+", query)
    terms.update(ascii_terms)
    scored = []
    for index, line in enumerate(lines):
        score = sum(term.lower() in line.lower() for term in terms)
        if score: scored.append((score, index, line))
    hits = [line for _, _, line in sorted(scored, key=lambda item: (-item[0], item[1]))]
    if hits: return "\n".join(hits)
    return "\n".join(lines[:6]) + "\n[未命中明確關鍵詞，以上為文件摘要；請調整問題或檢索詞。]"

ROLE_PERMISSIONS = {
 "guest":{"tools":["math_tool"],"resources":["company_information","passenger_service_rules"]},
 "employee":{"tools":["math_tool"],"resources":["company_information","passenger_service_rules","employee_policy"]},
 "operations":{"tools":["math_tool","image_tool","excel_python_tool"],"resources":["company_information","passenger_service_rules","flight_operations_guide"]},
 "maintenance":{"tools":["math_tool","image_tool"],"resources":["company_information","maintenance_guidelines"]},
 "developer":{"tools":["math_tool","image_tool","excel_python_tool"],"resources":["company_information","it_security_policy","employee_policy"]},
 "admin":{"tools":list(TOOL_REGISTRY),"resources":list(RESOURCE_CATALOG)}}
def authorize(role, kind, name): return name in ROLE_PERMISSIONS.get(role, {}).get(kind, [])

def get_role_access_summary(role):
    if role not in ROLE_PERMISSIONS:
        raise ValueError(f"未知角色：{role}")
    allowed_tools = ROLE_PERMISSIONS[role]["tools"]
    allowed_resources = ROLE_PERMISSIONS[role]["resources"]
    return {
        "role": role,
        "tools": {
            "allowed": allowed_tools,
            "denied": [name for name in TOOL_REGISTRY if name not in allowed_tools],
        },
        "resources": {
            "allowed": allowed_resources,
            "denied": [name for name in RESOURCE_CATALOG if name not in allowed_resources],
        },
    }
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
    magic = b"CILLM_AES256_GCM_V1\n"
    Path(target).parent.mkdir(parents=True, exist_ok=True)
    Path(target).write_bytes(magic + nonce + AESGCM(key).encrypt(nonce, Path(source).read_bytes(), magic))
def decrypt_resource(path, key_b64):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    raw=Path(path).read_bytes(); key=base64.urlsafe_b64decode(key_b64)
    magic = b"CILLM_AES256_GCM_V1\n"
    if not raw.startswith(magic): raise ValueError("不是 CILLM AES-256-GCM v1 加密檔")
    payload = raw[len(magic):]; nonce, ciphertext = payload[:12], payload[12:]
    return AESGCM(key).decrypt(nonce, ciphertext, magic).decode("utf-8")

def inspect_encrypted_resource(path):
    raw = Path(path).read_bytes()
    magic = b"CILLM_AES256_GCM_V1\n"
    payload = raw[len(magic):] if raw.startswith(magic) else raw
    try:
        payload.decode("utf-8")
        readable_as_utf8 = True
    except UnicodeDecodeError:
        readable_as_utf8 = False
    return {
        "file": str(path),
        "format": "CILLM AES-256-GCM v1" if raw.startswith(magic) else "unknown",
        "total_bytes": len(raw),
        "nonce_bytes": 12,
        "authentication_tag_bytes": 16,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "ciphertext_hex_preview": payload[12:60].hex(),
        "ciphertext_readable_as_utf8": readable_as_utf8,
    }

def _derive_key_from_password(password, salt):
    from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
    return Scrypt(salt=salt, length=32, n=2**14, r=8, p=1).derive(password.encode("utf-8"))

def prompt_new_vault_password():
    password = getpass.getpass("請設定保險庫密碼（至少 12 個字元；輸入不會顯示）：")
    if len(password) < 12: raise RuntimeError("保險庫密碼至少需要 12 個字元。")
    confirmation = getpass.getpass("請再次輸入相同密碼確認：")
    if password != confirmation: raise RuntimeError("兩次輸入的密碼不一致。")
    return password

def prompt_vault_password():
    password = getpass.getpass("請輸入保險庫密碼以解密（輸入不會顯示）：")
    if not password: raise RuntimeError("未輸入保險庫密碼。")
    return password

def encrypt_resource_with_password(source, target, password):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    salt, nonce = os.urandom(16), os.urandom(12)
    magic = b"CILLM_PW_AES256_GCM_V2\n"
    key = _derive_key_from_password(password, salt)
    ciphertext = AESGCM(key).encrypt(nonce, Path(source).read_bytes(), magic)
    Path(target).parent.mkdir(parents=True, exist_ok=True)
    Path(target).write_bytes(magic + salt + nonce + ciphertext)

def decrypt_resource_with_password(path, password):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    raw = Path(path).read_bytes(); magic = b"CILLM_PW_AES256_GCM_V2\n"
    if not raw.startswith(magic): raise ValueError("不是 CILLM 密碼式 AES-256-GCM v2 加密檔")
    payload = raw[len(magic):]; salt, nonce, ciphertext = payload[:16], payload[16:28], payload[28:]
    key = _derive_key_from_password(password, salt)
    return AESGCM(key).decrypt(nonce, ciphertext, magic).decode("utf-8")

def inspect_password_vault(path):
    raw = Path(path).read_bytes(); magic = b"CILLM_PW_AES256_GCM_V2\n"
    payload = raw[len(magic):] if raw.startswith(magic) else raw
    return {
        "file": str(path), "format": "CILLM password + scrypt + AES-256-GCM v2" if raw.startswith(magic) else "unknown",
        "total_bytes": len(raw), "salt_bytes": 16, "nonce_bytes": 12, "authentication_tag_bytes": 16,
        "sha256": hashlib.sha256(raw).hexdigest(), "ciphertext_hex_preview": payload[28:76].hex(),
        "password_stored_in_file": False, "derived_aes_key_stored_in_file": False,
    }
