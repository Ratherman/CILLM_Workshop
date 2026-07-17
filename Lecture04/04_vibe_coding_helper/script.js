"use strict";

const SYSTEM_PROMPT = `
你是 CILLM Vibe Coding Helper，專門協助初學者快速製作 HTML 網頁。

規則：
1. 使用繁體中文簡短說明設計決策。
2. 使用者要求建立或修改網頁時，必須提供一份完整、可直接儲存為 index.html 的程式碼。
3. 完整 HTML 必須放在 \`\`\`html 程式碼區塊中，包含 <!doctype html>、<html>、<head> 與 <body>。
4. 優先產生單一 HTML 檔；CSS 與 JavaScript 可寫在 <style>、<script> 中，方便直接複製執行。
5. 除非使用者明確要求，避免外部 CDN、套件、圖片與網路資源，讓頁面可離線開啟。
6. 注意響應式排版、鍵盤操作、可見 focus、文字對比與按鈕標籤。
7. 根據目前對話記憶修改上一版，不要遺漏使用者已確認的需求。
8. 不要輸出真實 API Key、個資或機密內容。
`.trim();

const MAX_HISTORY_MESSAGES = 12;
const REQUEST_TIMEOUT_MS = 600_000;

const elements = {
  apiKey: document.querySelector("#apiKeyInput"),
  baseUrl: document.querySelector("#baseUrlInput"),
  model: document.querySelector("#modelInput"),
  toggleKey: document.querySelector("#toggleKeyButton"),
  clear: document.querySelector("#clearButton"),
  copyLatest: document.querySelector("#copyLatestButton"),
  messages: document.querySelector("#messages"),
  status: document.querySelector("#statusMessage"),
  badge: document.querySelector("#connectionBadge"),
  form: document.querySelector("#composer"),
  prompt: document.querySelector("#promptInput"),
  send: document.querySelector("#sendButton"),
  messageTemplate: document.querySelector("#messageTemplate"),
  codeTemplate: document.querySelector("#codeTemplate"),
};

let history = [];
let latestHtml = "";
let isSending = false;

elements.form.addEventListener("submit", handleSubmit);
elements.clear.addEventListener("click", clearConversation);
elements.copyLatest.addEventListener("click", () => copyText(latestHtml, elements.copyLatest));
elements.toggleKey.addEventListener("click", toggleApiKeyVisibility);
elements.prompt.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    elements.form.requestSubmit();
  }
});

async function handleSubmit(event) {
  event.preventDefault();
  if (isSending) return;

  const apiKey = elements.apiKey.value.trim();
  const baseUrl = normalizeBaseUrl(elements.baseUrl.value);
  const model = elements.model.value.trim();
  const prompt = elements.prompt.value.trim();

  if (!apiKey) {
    showStatus("請先填入 CILLM API Key。", true);
    elements.apiKey.focus();
    return;
  }
  if (!baseUrl) {
    showStatus("請填入有效的 CILLM Base URL。", true);
    elements.baseUrl.focus();
    return;
  }
  if (!model) {
    showStatus("請填入 Model 名稱。", true);
    elements.model.focus();
    return;
  }
  if (!prompt) {
    showStatus("請先描述你想要的網頁。", true);
    elements.prompt.focus();
    return;
  }

  appendMessage("user", prompt);
  elements.prompt.value = "";
  setSending(true);
  showStatus("gpt-oss-120b 正在整理需求並產生程式碼……");

  const requestMessages = [
    { role: "system", content: SYSTEM_PROMPT },
    ...history,
    { role: "user", content: prompt },
  ];

  try {
    const answer = await requestChatCompletion({ apiKey, baseUrl, model, messages: requestMessages });
    history.push({ role: "user", content: prompt }, { role: "assistant", content: answer });
    history = history.slice(-MAX_HISTORY_MESSAGES);
    appendMessage("assistant", answer);
    updateLatestHtml(answer);
    setConnectionState("connected", "連線成功");
    showStatus("完成。你可以繼續要求修改，或複製最新 HTML。");
  } catch (error) {
    const message = friendlyError(error);
    appendMessage("assistant", `這次請求沒有成功。\n\n${message}`, { isError: true });
    setConnectionState("error", "連線失敗");
    showStatus(message, true);
  } finally {
    setSending(false);
    elements.prompt.focus();
  }
}

async function requestChatCompletion({ apiKey, baseUrl, model, messages }) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

  try {
    const response = await fetch(`${baseUrl}/chat/completions`, {
      method: "POST",
      mode: "cors",
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json",
        "X-User-ID": "workshop-vibe-coder",
        "X-Platform": "cillm-workshop",
        "X-Agent": "lecture04-vibe-coding-helper",
      },
      body: JSON.stringify({
        model,
        messages,
        max_tokens: 5000,
        temperature: 0.2,
        stream: false,
      }),
      signal: controller.signal,
    });

    const rawText = await response.text();
    let payload;
    try {
      payload = rawText ? JSON.parse(rawText) : {};
    } catch {
      throw new ApiError(response.status, `伺服器未回傳 JSON：${rawText.slice(0, 300)}`);
    }

    if (!response.ok) {
      const detail = typeof payload.detail === "string" ? payload.detail : JSON.stringify(payload);
      throw new ApiError(response.status, detail);
    }

    const choice = payload?.choices?.[0];
    const content = choice?.message?.content;
    if (typeof content !== "string" || !content.trim()) {
      const reasoningLength = choice?.message?.reasoning?.length ?? 0;
      throw new Error(
        `模型沒有回傳 content。finish_reason=${choice?.finish_reason ?? "unknown"}，` +
          `reasoning_length=${reasoningLength}。`,
      );
    }
    return content.trim();
  } finally {
    clearTimeout(timeoutId);
  }
}

function appendMessage(role, content, options = {}) {
  const fragment = elements.messageTemplate.content.cloneNode(true);
  const article = fragment.querySelector(".message");
  const meta = fragment.querySelector(".message-meta");
  const body = fragment.querySelector(".message-body");

  article.classList.add(role === "user" ? "message-user" : "message-assistant");
  if (options.isError) article.classList.add("message-error");
  meta.textContent = role === "user" ? "你" : "CILLM 助手";

  if (role === "assistant" && !options.isError) {
    renderAssistantContent(body, content);
  } else {
    const paragraph = document.createElement("p");
    paragraph.textContent = content;
    body.append(paragraph);
  }

  elements.messages.append(fragment);
  elements.messages.scrollTop = elements.messages.scrollHeight;
}

function renderAssistantContent(container, content) {
  const fencePattern = /```([\w+-]*)\s*\n?([\s\S]*?)```/g;
  let cursor = 0;
  let match;

  while ((match = fencePattern.exec(content)) !== null) {
    appendText(container, content.slice(cursor, match.index));
    appendCodeBlock(container, match[1] || "code", match[2].trim());
    cursor = match.index + match[0].length;
  }
  appendText(container, content.slice(cursor));
}

function appendText(container, text) {
  const cleaned = text.trim();
  if (!cleaned) return;
  const paragraph = document.createElement("p");
  paragraph.textContent = cleaned;
  container.append(paragraph);
}

function appendCodeBlock(container, language, code) {
  const fragment = elements.codeTemplate.content.cloneNode(true);
  const label = fragment.querySelector(".code-language");
  const codeElement = fragment.querySelector("code");
  const copyButton = fragment.querySelector(".copy-code-button");

  label.textContent = language.toUpperCase();
  codeElement.textContent = code;
  copyButton.addEventListener("click", () => copyText(code, copyButton));
  container.append(fragment);
}

function updateLatestHtml(answer) {
  const htmlFence = answer.match(/```html\s*\n?([\s\S]*?)```/i);
  if (htmlFence) {
    latestHtml = htmlFence[1].trim();
  } else if (/<!doctype html>/i.test(answer)) {
    latestHtml = answer.slice(answer.search(/<!doctype html>/i)).trim();
  } else {
    latestHtml = "";
  }
  elements.copyLatest.disabled = !latestHtml;
}

async function copyText(text, button) {
  if (!text) return;
  const originalLabel = button.textContent;
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
    } else {
      fallbackCopy(text);
    }
    button.textContent = "已複製";
    setTimeout(() => {
      button.textContent = originalLabel;
    }, 1600);
  } catch {
    showStatus("無法自動複製，請手動選取程式碼。", true);
  }
}

function fallbackCopy(text) {
  const textarea = document.createElement("textarea");
  textarea.value = text;
  textarea.setAttribute("readonly", "");
  textarea.style.position = "fixed";
  textarea.style.opacity = "0";
  document.body.append(textarea);
  textarea.select();
  const successful = document.execCommand("copy");
  textarea.remove();
  if (!successful) throw new Error("copy failed");
}

function clearConversation() {
  history = [];
  latestHtml = "";
  elements.copyLatest.disabled = true;
  elements.messages.replaceChildren();
  appendMessage(
    "assistant",
    "對話已清除。告訴我下一個想製作的網頁，我會從全新的需求開始。",
  );
  showStatus("已清除對話記憶。API Key 仍保留在目前分頁中。");
  elements.prompt.focus();
}

function toggleApiKeyVisibility() {
  const showing = elements.apiKey.type === "text";
  elements.apiKey.type = showing ? "password" : "text";
  elements.toggleKey.textContent = showing ? "顯示" : "隱藏";
  elements.toggleKey.setAttribute("aria-label", showing ? "顯示 API Key" : "隱藏 API Key");
}

function normalizeBaseUrl(value) {
  return value.trim().replace(/\/+$/, "");
}

function setSending(sending) {
  isSending = sending;
  elements.send.disabled = sending;
  elements.send.textContent = sending ? "產生中……" : "送出願望";
  elements.prompt.disabled = sending;
}

function showStatus(message, isError = false) {
  elements.status.textContent = message;
  elements.status.classList.toggle("is-error", isError);
}

function setConnectionState(state, label) {
  elements.badge.textContent = label;
  elements.badge.classList.toggle("is-connected", state === "connected");
  elements.badge.classList.toggle("is-error", state === "error");
}

function friendlyError(error) {
  if (error?.name === "AbortError") {
    return "請求超過 10 分鐘，已停止等待。請縮短需求後再試一次。";
  }
  if (error instanceof ApiError) {
    if (error.status === 401 || error.status === 403) {
      return `HTTP ${error.status}：API Key 無效、過期，或缺少 Chat Completion 權限。`;
    }
    if (error.status === 404) {
      return "HTTP 404：請確認 Base URL 包含 /v1，且 Model 名稱為 openai/gpt-oss-120b。";
    }
    if (error.status === 429) {
      return "HTTP 429：已達 TPM 或同時連線上限，請稍後再試。";
    }
    return `HTTP ${error.status}：${error.message}`;
  }
  if (error instanceof TypeError && /fetch/i.test(error.message)) {
    return (
      "瀏覽器無法連線 CILLM Gateway。請確認網路與網址；若主控台顯示 CORS，" +
      "代表 Portal 尚未允許從 file:// 頁面呼叫。"
    );
  }
  return error?.message || "發生未預期錯誤，請稍後再試。";
}

class ApiError extends Error {
  constructor(status, message) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}
