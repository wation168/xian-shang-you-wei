# -*- coding: utf-8 -*-
"""Optional HTTP probe for URL Evidence Chain.

Default offline: no network. Tests inject a fixture map or a transport callable.
Live probing is opt-in and never implied by a missing local slug.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

Transport = Callable[[str], dict[str, Any]]


def load_probe_fixture(path: str | Path) -> dict[str, dict[str, Any]]:
    """Load {url_or_slug: probe_dict} JSON fixture."""
    p = Path(path)
    data = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("probe fixture must be an object keyed by URL/slug")
    return data


def lookup_probe(
    target: str,
    fixture: Optional[dict[str, dict[str, Any]]] = None,
) -> Optional[dict[str, Any]]:
    if not fixture:
        return None
    if target in fixture:
        return fixture[target]
    # try leaf
    leaf = target.rsplit("/", 1)[-1]
    if leaf in fixture:
        return fixture[leaf]
    # try without scheme host
    for k, v in fixture.items():
        if k.endswith(target) or target.endswith(k):
            return v
    return None


def probe_url_live(
    url: str,
    *,
    timeout: float = 8.0,
    max_hops: int = 8,
    user_agent: str = "SoftGlow-SEO-Scanner-URL-Evidence/1.0",
) -> dict[str, Any]:
    """Follow redirects manually; return hops + final status. Never raises."""
    hops: list[dict[str, Any]] = []
    current = url
    try:
        for _ in range(max_hops):
            req = Request(current, method="HEAD", headers={"User-Agent": user_agent})
            try:
                with urlopen(req, timeout=timeout) as resp:
                    status = getattr(resp, "status", None) or resp.getcode()
                    hops.append({"url": current, "status": int(status)})
                    # urllib may already follow; prefer geturl
                    final = resp.geturl()
                    if final and final != current and int(status) < 300:
                        # already resolved
                        return {
                            "ok": True,
                            "error": None,
                            "hops": hops,
                            "final_url": final,
                            "final_status": int(status),
                        }
                    if int(status) in (301, 302, 303, 307, 308):
                        loc = resp.headers.get("Location")
                        if not loc:
                            break
                        from urllib.parse import urljoin

                        current = urljoin(current, loc)
                        continue
                    return {
                        "ok": True,
                        "error": None,
                        "hops": hops,
                        "final_url": final or current,
                        "final_status": int(status),
                    }
            except HTTPError as e:
                status = int(e.code)
                hops.append({"url": current, "status": status})
                if status in (301, 302, 303, 307, 308):
                    loc = e.headers.get("Location") if e.headers else None
                    if loc:
                        from urllib.parse import urljoin

                        current = urljoin(current, loc)
                        continue
                return {
                    "ok": status < 400,
                    "error": None,
                    "hops": hops,
                    "final_url": current,
                    "final_status": status,
                }
        return {
            "ok": False,
            "error": "max_hops_exceeded",
            "hops": hops,
            "final_url": current,
            "final_status": hops[-1]["status"] if hops else None,
        }
    except (URLError, OSError, ValueError) as e:
        return {
            "ok": False,
            "error": str(e),
            "hops": hops,
            "final_url": "",
            "final_status": None,
        }


def resolve_probe(
    target: str,
    *,
    fixture: Optional[dict[str, dict[str, Any]]] = None,
    live: bool = False,
    transport: Optional[Transport] = None,
) -> Optional[dict[str, Any]]:
    if transport is not None:
        return transport(target)
    hit = lookup_probe(target, fixture)
    if hit is not None:
        return hit
    if live and (target.startswith("http://") or target.startswith("https://")):
        return probe_url_live(target)
    return None
