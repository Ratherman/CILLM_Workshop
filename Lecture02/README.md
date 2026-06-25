# CAL edu
- 簡報連結：https://drive.google.com/file/d/1x9goDDxb06yWhYMdb5HprpIP2V4K2ev2/view?usp=sharing
- API 網頁：https://cillmtest.china-airlines.com/docs
- CILLM_API_KEY 和第一次一樣


目前提供兩個 Skills：

- `hr-leave`：公司休假、加班補休與准假權責規則。
- `hr-free-ticket`：員工免費票、優待票規則與查表 scripts。

系統會在終端顯示各 LLM 節點的執行時間、模型、token、結構化判斷結果，以及每輪與累積 token。

## 注意事項

- 目前寫的都沒有防呆或錯誤保護機制，幾乎沒有容錯空間，尤其沒有 retry 機制，任一節點失敗就會報錯跳脫。

- 系統會最大限度解答 user 的問題，例如:

    user query: 我可以獲得幾天特休

    user 並沒有提出年資，llm 並未追問，而是直接回答完整特休年資及給假的表格，這是可接受的回答，但不確定是否要在這種情況追問還是可以接受提供資訊供 user 參考。

- package reload 為測試過程使用，教材正式使用時可刪除

```python
import importlib
import llm_client
import trace_utils
import agent_prompts
import load_skills
import skill_tools
import skill_models

importlib.reload(llm_client)
importlib.reload(trace_utils)
importlib.reload(agent_prompts)
importlib.reload(load_skills)
importlib.reload(skill_tools)
importlib.reload(skill_models)
```

## Quick Start

- 使用環境 `Python 3.11.15`

```powershell
conda create -n CAL_edu python=3.11.15
conda activate CAL_edu
cd CAL_edu
pip install -r requirements.txt
```

- 在 `config.yaml` 選擇 LLM 的 `provider`。目前預留 cillm_portal, cillm_llm, groq, openai，預設 openai

```yaml
provider: openai 
```

- 依 `.env.example` 所示在同目錄建立 `.env`，填入所選 `provider` 的 API key
- 教學主程式：使用 VS Code 或 Jupyter 依序執行 `edu.ipynb`
- CLI: `python main.py` 可直接執行 LLM 呼叫

```powershell
python main.py
```

## Notebook Cells

1. 載入模組、設定 provider 與共用參數。
2. 僅呼叫 LLM，不使用 Skill。
3. 單一 Skill、單輪對話。
4. 多 Skill、單輪對話。
5. 多 Skill、多輪對話，包含 Context Route 與 memory。
6. Practice: 多 Skill、多輪 workflow。
7. 執行 Practice，提供獨立 memory 與輸入迴圈。

## File Structure

```text
CAL_edu/
├─ edu.ipynb             # 教材檔 (單/多輪對話、agent skill 架構入口)
├─ main.py               # 基本 LLM CLI
├─ config.yaml           # Provider、模型與 LLM generation parameter
├─ .env.example          # API key 欄位範例
├─ requirements.txt
├─ llm_client.py         # API client 與 LLM 呼叫
├─ agent_prompts.py      # 各 Agent 節點的 system prompts
├─ skill_models.py       # Pydantic 結構化輸出模型
├─ load_skills.py        # Skill metadata、全文與 reference 載入
├─ skill_tools.py        # 受控執行 Skill scripts
├─ trace_utils.py        # 大系統 Trace、Evaluate 與 token 統計
└─ skills/               # 目前包含兩個 skills
   ├─ hr-leave/
   │  ├─ SKILL.md
   │  └─ references/
   └─ hr-free-ticket/
      ├─ SKILL.md
      ├─ references/
      └─ scripts/
```

## Standard Workflow

多 skill 多輪對話架構說明

```text
User Query
│
▼
是否存在 memory 與 previous_skill_id？
│
├─ 是 → Context Route
│       判斷本次 Query 是否延續上一輪未完成的問題。
│       ├─ continuation=True
│       │  → 沿用 previous_skill_id 對應的 Skill
│       │  → 不再呼叫 Hint 直接進入 Resource Router
│       └─ continuation=False
│          → 清空舊 memory 與 previous_skill_id
│          → 進入 Hint
│
└─ 否 → Hint
        讀取所有 Skills 的 name、description，判斷服務範圍並選出單一 Skill。
        ├─ scope=False
        │  → Python 固定回覆「此問題非本系統服務範圍，請重新提問」
        │  → 不再呼叫 Resource Router、Context Builder、Responder
        └─ scope=True
           → 使用 skill_id 載入選中的 SKILL.md、resource index 與 scripts metadata
│
▼
Resource Router
合併理解 memory 與本次 Query，判斷需要哪些 references 與 scripts。
 ├─ References → Python 安全讀取指定政策檔
 ├─ Scripts    → Python 驗證 script_id、arguments 並執行指定 script
 └─ 無需資源   → 使用空的 reference_contexts／script_results
│
▼
 Context Builder
 根據 memory、User Query、SKILL.md、政策內容與 script 結果：
 1. 判斷回答資訊是否完整
 2. 萃取 Responder 所需的 selected_context
 │
 ├─ information_complete=False
 │   → 產生 missing_information
 │   → Responder 要求 User 補充
 │   → 保存本輪 User Query 與 Responder 回覆至 memory
 │   → 保存 selected_skill.skill_id 至 previous_skill_id
 │
 └─ information_complete=True
     → 產生 selected_context
     → Responder 僅依 selected_context 組織最終答案
     → 回答完成後清空 memory 與 previous_skill_id
│
▼
 顯示回答、各節點 Trace、batch_token 與 total_token
```

## Notes

- Hint 僅讀 Skills 的 `name`、`description`，選出單一 `skill_id`。
- Resource Router 負責選擇 references、scripts 與 arguments，Python script 負責實際讀檔及執行 allowlist scripts。
- Context Builder 擷取精簡 `selected_context`，Responder 不須讀取完整 Skill。
- 多輪 memory 只保存在目前 notebook 執行期間，未使用 database 管理。最終回答完成後會清空。
- `llm_token` 以 provider API 回傳的 `usage.total_tokens` 為準。
