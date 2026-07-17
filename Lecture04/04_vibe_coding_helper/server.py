"""CILLM Vibe Coding Helper 的本機靜態伺服器與同源 API Proxy。

使用方式：
    python server.py

Server 只監聽 127.0.0.1，不會把頁面或 API Key 暴露到區域網路。
API Key 由瀏覽器每次 request 傳入，只用來轉送 CILLM，程式不寫入磁碟或 log。
"""

from __future__ import annotations

import argparse
import json
import threading
import webbrowser
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import requests


HOST = "127.0.0.1"
DEFAULT_PORT = 8088
MAX_REQUEST_BYTES = 2 * 1024 * 1024
STATIC_DIR = Path(__file__).resolve().parent


class VibeCodingHandler(SimpleHTTPRequestHandler):
    server_version = "CILLMVibeCoding/1.0"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def do_POST(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        if self.path != "/api/chat":
            self._send_json(HTTPStatus.NOT_FOUND, {"detail": "Not Found"})
            return

        if self.headers.get_content_type() != "application/json":
            self._send_json(
                HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
                {"detail": "Content-Type must be application/json."},
            )
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._send_json(HTTPStatus.BAD_REQUEST, {"detail": "Invalid Content-Length."})
            return

        if content_length <= 0 or content_length > MAX_REQUEST_BYTES:
            self._send_json(
                HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
                {"detail": "Request body must be between 1 byte and 2 MB."},
            )
            return

        try:
            payload = json.loads(self.rfile.read(content_length))
            request_data = self._validate_payload(payload)
        except (json.JSONDecodeError, UnicodeDecodeError):
            self._send_json(HTTPStatus.BAD_REQUEST, {"detail": "Request body is not valid JSON."})
            return
        except ValueError as exc:
            self._send_json(HTTPStatus.BAD_REQUEST, {"detail": str(exc)})
            return

        api_key = request_data.pop("api_key")
        base_url = request_data.pop("base_url")
        chat_url = f"{base_url}/chat/completions"

        try:
            upstream = requests.post(
                chat_url,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "X-User-ID": "workshop-vibe-coder",
                    "X-Platform": "cillm-workshop",
                    "X-Agent": "lecture04-vibe-coding-helper",
                },
                json=request_data,
                timeout=(10, 610),
            )
        except requests.Timeout:
            self._send_json(
                HTTPStatus.GATEWAY_TIMEOUT,
                {"detail": "CILLM Gateway did not respond within 610 seconds."},
            )
            return
        except requests.RequestException as exc:
            self._send_json(
                HTTPStatus.BAD_GATEWAY,
                {"detail": f"Could not connect to CILLM Gateway: {exc}"},
            )
            return

        content_type = upstream.headers.get("Content-Type", "application/json")
        response_body = upstream.content
        self.send_response(upstream.status_code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(response_body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(response_body)

    def end_headers(self) -> None:
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        super().end_headers()

    def log_message(self, format: str, *args: Any) -> None:
        # BaseHTTPRequestHandler 只會記錄 method/path/status，不會記錄 request body 或 API Key。
        super().log_message(format, *args)

    @staticmethod
    def _validate_payload(payload: Any) -> dict[str, Any]:
        if not isinstance(payload, dict):
            raise ValueError("Request body must be a JSON object.")

        api_key = payload.get("api_key")
        base_url = payload.get("base_url")
        model = payload.get("model")
        messages = payload.get("messages")

        if not isinstance(api_key, str) or not api_key.strip():
            raise ValueError("api_key is required.")
        if not isinstance(base_url, str) or not base_url.strip():
            raise ValueError("base_url is required.")
        normalized_base_url = base_url.strip().rstrip("/")
        parsed_url = urlparse(normalized_base_url)
        if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
            raise ValueError("base_url must be a valid http or https URL.")
        if parsed_url.username or parsed_url.password:
            raise ValueError("base_url must not contain credentials.")
        if parsed_url.query or parsed_url.fragment:
            raise ValueError("base_url must not contain a query string or fragment.")
        if not isinstance(model, str) or not model.strip():
            raise ValueError("model is required.")
        if not isinstance(messages, list) or not messages:
            raise ValueError("messages must be a non-empty array.")
        if len(messages) > 20:
            raise ValueError("messages exceeds the 20-message limit.")

        clean_messages: list[dict[str, str]] = []
        for index, message in enumerate(messages):
            if not isinstance(message, dict):
                raise ValueError(f"messages[{index}] must be an object.")
            role = message.get("role")
            content = message.get("content")
            if role not in {"system", "user", "assistant"}:
                raise ValueError(f"messages[{index}].role is invalid.")
            if not isinstance(content, str) or not content.strip():
                raise ValueError(f"messages[{index}].content must be a non-empty string.")
            clean_messages.append({"role": role, "content": content})

        max_tokens = payload.get("max_tokens", 5000)
        if not isinstance(max_tokens, int) or isinstance(max_tokens, bool):
            raise ValueError("max_tokens must be an integer.")
        max_tokens = min(max(max_tokens, 1), 8000)

        temperature = payload.get("temperature", 0.2)
        if not isinstance(temperature, (int, float)) or isinstance(temperature, bool):
            raise ValueError("temperature must be a number.")
        temperature = min(max(float(temperature), 0.0), 2.0)

        return {
            "api_key": api_key.strip(),
            "base_url": normalized_base_url,
            "model": model.strip(),
            "messages": clean_messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": False,
        }

    def _send_json(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status.value)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the local CILLM Vibe Coding Helper.")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Local port (default: 8088).")
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Do not open the browser automatically.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not 1 <= args.port <= 65535:
        raise SystemExit("Port must be between 1 and 65535.")

    server = ThreadingHTTPServer((HOST, args.port), VibeCodingHandler)
    url = f"http://{HOST}:{args.port}/"
    print("CILLM Vibe Coding Helper is running.")
    print(f"Open: {url}")
    print("Press Ctrl+C to stop. API Keys are not written to disk or logs.")

    if not args.no_browser:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
