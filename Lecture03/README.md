# LLM 多模態實戰

* 教材連結：https://drive.google.com/file/d/1U5jDH6h1Z_ZCcWq9_7g2erxeDFJGSKlq/view?usp=drive_link
* 六章依序疊加：資料標準化 → GPT-OSS → Tool → Resource → AI Agent → RBAC 與 AES-256-GCM。

## 快速開始（Windows / Anaconda）

```powershell
cd llm_multimodal_course
conda create -n llm-multimodal python=3.11 -y
conda activate llm-multimodal
pip install -r requirements.txt
Copy-Item .env.example .env
jupyter notebook
```

六本 Notebook 都必須連線 CILLM，並使用 `CILLM_API_KEY` 呼叫 `openai/gpt-oss-120b`。請填寫 `.env` 的 URL、模型名稱與 API key；缺少設定時 Notebook 會立即停止，不會產生 mock 回覆。請勿提交 `.env`。

文字與 Excel Parser、Tool 的 Python 運算、Resource、RBAC、AES，以及 `faster-whisper` CPU 轉錄本身可在本機執行；但為了維持課程一致性，每章仍會把結果交給 GPT-OSS 理解、規劃或整合。

音訊真實轉錄另需 FFmpeg。Notebook 可從專案根目錄或 `notebooks/` 開啟。

## 教材資料

- `data/`：虛構文字、圖片、靜音示範 WAV、航班延誤 Excel。
- `resources/`：六類虛構規範，不可作為真實營運依據。
- `course_utils.py`：各章逐步使用的共用教學函式。
- `generated/`：執行時產生的加密檔等輸出。

更多可替換的文字、圖片、語音素材與建議提問，請看 `data/SAMPLE_CATALOG.md`。

## 安全提醒

第三章的動態 Python 限制只為展示概念，不是 production sandbox。正式環境應使用隔離容器、資源限制、唯讀檔案系統與完整稽核。
