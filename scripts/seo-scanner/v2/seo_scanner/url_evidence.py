# -*- coding: utf-8 -*-
"""URL evidence chain (prototype).

Offline scans lack HTTP/redirect history. If an internal link slug does not
match any scanned page, emit insufficient_evidence — not Critical true_issue.
"""

from __future__ import annotations

from collections import defaultdict

from .models import Issue, Page


def check_missing_local_targets(
    pages: list[Page],
    *,
    max_targets: int = 40,
) -> list[Issue]:
    """Flag internal link slugs that do not exist in the scanned page set."""
    if not pages:
        return []

    known = {p.slug for p in pages}
    # also accept leaf equality (lang/foo vs foo)
    known_leaves = {s.rsplit("/", 1)[-1] for s in known}

    missing: dict[str, list[str]] = defaultdict(list)
    for page in pages:
        for raw in page.internal_links or []:
            link = str(raw).strip()
            if not link or link.startswith("#"):
                continue
            leaf = link.rsplit("/", 1)[-1]
            if link in known or leaf in known_leaves:
                continue
            # skip very generic tokens that are not page-like
            if leaf in {"index", "home", "css", "js"}:
                continue
            missing[link].append(page.slug)
            if len(missing) >= max_targets:
                break
        if len(missing) >= max_targets:
            break

    if not missing:
        return []

    targets = sorted(missing.keys())[:max_targets]
    sample_map = {t: missing[t][:5] for t in targets}
    return [
        Issue(
            id="url-missing-local-01",
            category="links",
            problem=f"掃描集內找不到連結目標｜{len(targets)} 個 slug（證據不足）",
            cause=(
                "內部連結的目標 slug 不在本次掃描頁面集合中。"
                "離線掃描無法確認線上路由、301、sitemap 或歷史 URL。"
            ),
            fix=(
                "補 URL 證據鏈（HTTP／redirect／sitemap／替代頁）後再決定；"
                "確認前不要當成搬站錯誤直接改站。"
            ),
            priority="P3",
            evidence={
                "url_evidence": True,
                "file_exists": False,
                "http_checked": False,
                "missing_target_count": len(targets),
                "missing_targets_sample": targets[:20],
                "sources_sample": sample_map,
                "disposition": "insufficient_evidence",
                "confidence": "low",
                "do_not_fix_if": (
                    "Do not treat as a migration/SEO error without HTTP, redirect, or sitemap evidence."
                ),
            },
            pages=sorted({s for srcs in sample_map.values() for s in srcs})[:40],
        )
    ]
