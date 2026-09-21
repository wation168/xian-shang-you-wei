# -*- coding: utf-8 -*-
"""SoftGlow product UI + live scan API (stdlib HTTP server).

Deploy layout:
  v2/
    seo_scanner/live_crawl.py
    seo_scanner/product_payload.py
    product/server.py   ← this file
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import threading
import traceback
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlparse

_PRODUCT_DIR = Path(__file__).resolve().parent
_V2_ROOT = _PRODUCT_DIR.parent
if str(_V2_ROOT) not in sys.path:
    sys.path.insert(0, str(_V2_ROOT))

_SCAN_LOCK = threading.Lock()

DEFAULT_MAX_PAGES = 40
HARD_MAX_PAGES = 60


class ScanHTTPError(Exception):
    def __init__(self, status: int, body: dict):
        super().__init__(body.get("error", "error"))
        self.status = status
        self.body = body


def _json_bytes(obj: Any, status: int = 200) -> tuple[int, bytes, str]:
    raw = json.dumps(obj, ensure_ascii=False).encode("utf-8")
    return status, raw, "application/json; charset=utf-8"


def _validate_url(url: str) -> Optional[str]:
    u = (url or "").strip()
    if not u:
        return "請提供網址（url 欄位不可空白）。"
    parsed = urlparse(u)
    if parsed.scheme not in ("http", "https"):
        return "網址必須以 http:// 或 https:// 開頭。"
    if not parsed.netloc:
        return "網址格式不正確（缺少主機名稱）。"
    return None


def _run_live_scan(url: str, max_pages: int) -> dict:
    from seo_scanner.live_crawl import crawl_site
    from seo_scanner.parse import scan_root
    from seo_scanner.diagnose import run_all_checks
    from seo_scanner.product_payload import build_product_payload

    with tempfile.TemporaryDirectory(prefix="softglow-crawl-") as tmp:
        dest = Path(tmp)
        meta = crawl_site(url, dest, max_pages=max_pages)
        pages_saved = int(meta.get("pages_saved") or 0)
        if pages_saved <= 0:
            detail = ""
            errs = meta.get("errors") or []
            if errs:
                first = errs[0].get("error") if isinstance(errs[0], dict) else str(errs[0])
                detail = f"（細節：{first}）"
            raise ScanHTTPError(
                422,
                {
                    "ok": False,
                    "error": (
                        "無法抓取任何 HTML 頁面。請確認網址可公開存取、"
                        "不是需登入／驗證碼的網站，且首頁有可讀的 HTML 內容。"
                        + detail
                    ),
                    "crawl": meta,
                },
            )

        pages = scan_root(dest)
        if not pages:
            raise ScanHTTPError(
                422,
                {
                    "ok": False,
                    "error": (
                        "已下載檔案，但解析後沒有可用頁面。"
                        "請換一個網址，或確認目標不是純 JavaScript 渲染的單頁應用。"
                    ),
                    "crawl": meta,
                },
            )

        try:
            issues, _pairs, summary = run_all_checks(pages, http_live=False)
        except TypeError:
            issues, _pairs, summary = run_all_checks(pages)

        host = urlparse(meta.get("final_start_url") or url).netloc or url
        payload = build_product_payload(
            pages=pages,
            issues=issues,
            summary=summary,
            sample_url=url,
            site_label=host,
            generated_from="live_crawl",
        )
        payload["crawl_meta"] = {
            "fetched": meta.get("fetched"),
            "skipped": meta.get("skipped"),
            "pages_saved": meta.get("pages_saved"),
            "final_start_url": meta.get("final_start_url"),
            "error_count": len(meta.get("errors") or []),
        }
        return payload


class ProductHandler(SimpleHTTPRequestHandler):
    """Serve product static files + /api/*."""

    def end_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(204)
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        if self.path.split("?", 1)[0] == "/api/health":
            self._send_json(*_json_bytes({"ok": True, "mode": "live"}))
            return
        return super().do_GET()

    def do_POST(self) -> None:  # noqa: N802
        path = self.path.split("?", 1)[0]
        if path != "/api/scan":
            self.send_error(404, "Not Found")
            return

        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length > 0 else b"{}"
        try:
            body = json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            self._send_json(
                *_json_bytes({"ok": False, "error": "請求內容不是有效的 JSON。"}, 400)
            )
            return

        url = str(body.get("url") or "").strip()
        err = _validate_url(url)
        if err:
            self._send_json(*_json_bytes({"ok": False, "error": err}, 400))
            return

        try:
            max_pages = int(body.get("max_pages") if body.get("max_pages") is not None else DEFAULT_MAX_PAGES)
        except (TypeError, ValueError):
            max_pages = DEFAULT_MAX_PAGES
        max_pages = max(1, min(max_pages, HARD_MAX_PAGES))

        if not _SCAN_LOCK.acquire(blocking=False):
            self._send_json(
                *_json_bytes(
                    {
                        "ok": False,
                        "error": "目前已有另一筆掃描進行中，請稍候再試（同時只允許一筆）。",
                    },
                    429,
                )
            )
            return

        try:
            payload = _run_live_scan(url, max_pages)
            self._send_json(*_json_bytes(payload, 200))
        except ScanHTTPError as e:
            self._send_json(*_json_bytes(e.body, e.status))
        except Exception as e:  # noqa: BLE001
            traceback.print_exc()
            self._send_json(
                *_json_bytes(
                    {
                        "ok": False,
                        "error": f"掃描過程發生錯誤：{type(e).__name__}: {e}",
                    },
                    500,
                )
            )
        finally:
            _SCAN_LOCK.release()

    def _send_json(self, status: int, raw: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def log_message(self, fmt: str, *args: Any) -> None:
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="SoftGlow product live-scan server")
    parser.add_argument("--bind", default="127.0.0.1", help="bind address (default 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8765, help="port (default 8765)")
    parser.add_argument(
        "--root",
        default=str(_PRODUCT_DIR),
        help="product directory to serve (default: this file's directory)",
    )
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"錯誤：目錄不存在：{root}", file=sys.stderr)
        return 1

    os.chdir(root)
    httpd = ThreadingHTTPServer((args.bind, args.port), ProductHandler)
    print("=" * 60)
    print("SoftGlow Website Intelligence — 即時掃描伺服器已啟動")
    print(f"請在瀏覽器開啟： http://{args.bind}:{args.port}/")
    print("貼上真實網址即可同網域爬取掃描（預設最多約 40 頁，上限 60）。")
    print("示範按鈕仍載入本地 JSON，不會打即時掃描。")
    print("按 Ctrl+C 結束。")
    print("=" * 60)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n已關閉伺服器。")
    finally:
        httpd.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
