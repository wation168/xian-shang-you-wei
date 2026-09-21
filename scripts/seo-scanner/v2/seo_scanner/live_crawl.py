# -*- coding: utf-8 -*-
"""Minimal same-host HTML crawler for SoftGlow live URL scan."""

from __future__ import annotations

import re
import time
from collections import deque
from pathlib import Path
from typing import Optional
from urllib.error import HTTPError, URLError
from urllib.parse import urldefrag, urljoin, urlparse, urlunparse
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

SKIP_SCHEMES = ("mailto:", "javascript:", "tel:", "data:")
BINARY_EXTS = {
    ".pdf", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico",
    ".css", ".js", ".mjs", ".map", ".zip", ".gz", ".tar", ".rar", ".7z",
    ".mp3", ".mp4", ".avi", ".mov", ".woff", ".woff2", ".ttf", ".eot", ".otf",
    ".xml", ".json", ".rss", ".atom", ".csv", ".xls", ".xlsx",
    ".doc", ".docx", ".ppt", ".pptx", ".bin", ".exe", ".dmg", ".apk", ".wasm",
}

# SoftGlow parse.scan_root skips these basenames — rename so live pages are diagnosed.
SCANNER_SKIP_BASENAMES = {
    "index.html", "privacy.html", "terms.html", "disclaimer.html",
    "refund.html", "contact.html", "about.html", "reset-password.html", "404.html",
}


def _normalize_host(netloc: str) -> str:
    host = (netloc or "").lower()
    if "@" in host:
        host = host.rsplit("@", 1)[-1]
    if host.startswith("[") and "]" in host:
        return host
    if ":" in host:
        host = host.rsplit(":", 1)[0]
    if host.startswith("www."):
        host = host[4:]
    return host


def _same_host(a: str, b: str) -> bool:
    return _normalize_host(a) == _normalize_host(b)


def _normalize_url(url: str) -> Optional[str]:
    raw = (url or "").strip()
    if not raw:
        return None
    low = raw.lower()
    if low.startswith(SKIP_SCHEMES) or raw.startswith("#"):
        return None
    raw, _frag = urldefrag(raw)
    parsed = urlparse(raw)
    if parsed.scheme not in ("http", "https"):
        return None
    if not parsed.netloc:
        return None
    path = parsed.path or "/"
    return urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), path, "", "", ""))


def _looks_like_html_path(url: str) -> bool:
    path = urlparse(url).path or "/"
    if path.endswith("/"):
        return True
    name = path.rsplit("/", 1)[-1]
    if not name or "." not in name:
        return True
    ext = "." + name.rsplit(".", 1)[-1].lower()
    if ext in BINARY_EXTS:
        return False
    if ext in (".html", ".htm", ".php", ".asp", ".aspx", ".jsp"):
        return True
    return ext not in BINARY_EXTS


def _url_to_relpath(url: str) -> str:
    """Map URL path → safe relative .html path.

    "/" → index.html ; "/foo/" → foo/index.html ; "/a/b" → a/b.html
    (basename may later be renamed to *_page.html for scanner compatibility)
    """
    path = urlparse(url).path or "/"
    parts = []
    for seg in path.split("/"):
        if not seg or seg in (".", ".."):
            continue
        safe = re.sub(r"[^\w.\-~\u4e00-\u9fff]+", "_", seg, flags=re.UNICODE)
        if not safe or safe in (".", ".."):
            continue
        parts.append(safe)

    if path.endswith("/") or not parts:
        if not parts:
            return "index.html"
        return "/".join(parts + ["index.html"])

    last = parts[-1]
    lower = last.lower()
    if lower.endswith(".html") or lower.endswith(".htm"):
        return "/".join(parts)
    return "/".join(parts) + ".html"


def _avoid_scanner_skip(rel: str) -> str:
    base_lower = Path(rel).name.lower()
    if base_lower in SCANNER_SKIP_BASENAMES:
        return str(Path(rel).with_name(f"{Path(rel).stem}_page.html"))
    return rel


def _is_html_content_type(ctype: Optional[str]) -> bool:
    if not ctype:
        return False
    main = ctype.split(";", 1)[0].strip().lower()
    return main in ("text/html", "application/xhtml+xml") or "html" in main


def _fetch(url: str, *, timeout: float, user_agent: str) -> tuple[Optional[bytes], Optional[str], Optional[str]]:
    req = Request(
        url,
        headers={
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
        },
        method="GET",
    )
    try:
        with urlopen(req, timeout=timeout) as resp:
            final = resp.geturl() or url
            ctype = resp.headers.get("Content-Type")
            if ctype and not _is_html_content_type(ctype):
                return None, final, f"非 HTML（Content-Type: {ctype}）"
            raw = resp.read()
            if len(raw) > 2_000_000:
                raw = raw[:2_000_000]
            return raw, final, None
    except HTTPError as e:
        return None, url, f"HTTP {e.code}"
    except URLError as e:
        return None, url, f"連線失敗：{e.reason}"
    except Exception as e:  # noqa: BLE001
        return None, url, f"{type(e).__name__}: {e}"


def _extract_links(html: bytes, base_url: str) -> list[str]:
    try:
        soup = BeautifulSoup(html, "html.parser")
    except Exception:  # noqa: BLE001
        return []
    out: list[str] = []
    for a in soup.find_all("a", href=True):
        href = (a.get("href") or "").strip()
        if not href or href.startswith("#"):
            continue
        low = href.lower()
        if low.startswith(SKIP_SCHEMES):
            continue
        joined = urljoin(base_url, href)
        norm = _normalize_url(joined)
        if not norm:
            continue
        if not _looks_like_html_path(norm):
            continue
        out.append(norm)
    return out


def crawl_site(
    start_url: str,
    dest_dir: Path,
    *,
    max_pages: int = 40,
    timeout: float = 12.0,
    user_agent: str = "SoftGlow-Website-Intelligence/0.1",
) -> dict:
    """BFS same-host HTML crawl; save pages under dest_dir.

    Returns meta: fetched, skipped, errors, start_url, final_start_url, pages_saved.
    Never raises for individual page failures. max_pages clamped to 1..60.
    """
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)

    max_pages = max(1, min(int(max_pages or 40), 60))
    timeout = float(timeout) if timeout else 12.0

    start_norm = _normalize_url(start_url)
    meta = {
        "fetched": 0,
        "skipped": 0,
        "errors": [],
        "start_url": start_url,
        "final_start_url": start_norm or start_url,
        "pages_saved": 0,
    }
    if not start_norm:
        meta["errors"].append({"url": start_url, "error": "僅支援 http:// 或 https:// 網址"})
        return meta

    start_host = urlparse(start_norm).netloc
    queue: deque[str] = deque([start_norm])
    seen: set[str] = set()
    saved_paths: set[str] = set()
    final_start = start_norm

    while queue and meta["pages_saved"] < max_pages:
        url = queue.popleft()
        if url in seen:
            continue
        seen.add(url)

        if not _same_host(urlparse(url).netloc, start_host):
            meta["skipped"] += 1
            continue
        if not _looks_like_html_path(url):
            meta["skipped"] += 1
            continue

        body, final_url, err = _fetch(url, timeout=timeout, user_agent=user_agent)
        meta["fetched"] += 1

        if err or body is None:
            meta["errors"].append({"url": url, "error": err or "空白回應"})
            continue

        final_norm = _normalize_url(final_url) or final_url
        if not _same_host(urlparse(final_norm).netloc, start_host):
            meta["skipped"] += 1
            meta["errors"].append({"url": url, "error": f"重新導向到外站 → {final_norm}"})
            continue

        if url == start_norm or meta["pages_saved"] == 0:
            final_start = final_norm
            meta["final_start_url"] = final_start

        rel = _avoid_scanner_skip(_url_to_relpath(final_norm))
        if rel in saved_paths:
            stem = rel[:-5] if rel.endswith(".html") else rel
            n = 2
            while f"{stem}__{n}.html" in saved_paths:
                n += 1
            rel = f"{stem}__{n}.html"
        saved_paths.add(rel)

        out_path = dest_dir / rel
        try:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            try:
                text = body.decode("utf-8")
            except UnicodeDecodeError:
                text = body.decode("utf-8", errors="replace")
            out_path.write_text(text, encoding="utf-8")
            meta["pages_saved"] += 1
        except OSError as e:
            meta["errors"].append({"url": url, "error": f"寫入失敗：{e}"})
            continue

        for link in _extract_links(body, final_norm):
            if link in seen:
                continue
            if not _same_host(urlparse(link).netloc, start_host):
                continue
            queue.append(link)

        time.sleep(0.05)

    return meta
