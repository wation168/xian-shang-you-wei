# -*- coding: utf-8 -*-
"""Build product-UI JSON payload from scanner pages/issues/summary."""

from __future__ import annotations

from typing import Any, Iterable, Optional
from urllib.parse import urlparse

_BODY_TEXT_MAX = 4000


def _site_key_from_url(sample_url: str, site_label: str = "") -> str:
    host = urlparse(sample_url or "").netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    if host:
        key = host.replace(":", "_").replace(".", "_")
        return key[:64] or "site"
    label = (site_label or "site").strip().lower()
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in label)
    return (safe or "site")[:64]


def _page_to_export_dict(page: Any) -> dict:
    if hasattr(page, "to_dict"):
        d = dict(page.to_dict())
    elif isinstance(page, dict):
        d = dict(page)
    else:
        raise TypeError(f"page must have to_dict() or be dict, got {type(page)}")
    body = d.get("body_text")
    if isinstance(body, str) and len(body) > _BODY_TEXT_MAX:
        d["body_text"] = body[:_BODY_TEXT_MAX] + "…"
    return d


def _issue_to_export_dict(issue: Any) -> dict:
    if hasattr(issue, "to_dict"):
        return dict(issue.to_dict())
    if isinstance(issue, dict):
        return dict(issue)
    raise TypeError(f"issue must have to_dict() or be dict, got {type(issue)}")


def build_product_payload(
    *,
    pages: Iterable[Any],
    issues: Iterable[Any],
    summary: Optional[dict] = None,
    sample_url: str = "",
    site_label: str = "",
    generated_from: str = "live_crawl",
    site_key: Optional[str] = None,
) -> dict:
    """Return product-shaped JSON for SoftGlow product UI."""
    page_list = [_page_to_export_dict(p) for p in (pages or [])]
    issue_list = [_issue_to_export_dict(i) for i in (issues or [])]
    label = site_label or sample_url or "網站"
    key = site_key or _site_key_from_url(sample_url, label)
    return {
        "generated_from": generated_from,
        "site_key": key,
        "site_label": label,
        "sample_url": sample_url,
        "pages": page_list,
        "issues": issue_list,
        "summary": summary if summary is not None else {},
    }
