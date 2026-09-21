# -*- coding: utf-8 -*-
"""Website Understanding — site-level summary before/alongside issue lists.

Generic heuristics only (no site-specific path hardcoding).
"""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any, Iterable

from .models import Page
from .link_opportunities import page_type


def _tokens(text: str) -> list[str]:
    import re
    return re.findall(r"[a-z0-9\u4e00-\u9fff]+", (text or "").lower())


def estimate_shell_and_unique(pages: list[Page], sample_cap: int = 80) -> dict[str, Any]:
    """Estimate shared shell token ratio vs per-page unique contribution.

    Shell tokens ≈ tokens appearing on >= 80% of sampled pages.
    unique_ratio ≈ 1 - (shell token occurrences / all tokens) averaged.
    """
    sample = pages[:sample_cap] if len(pages) > sample_cap else pages
    if not sample:
        return {
            "sampled_pages": 0,
            "shell_token_types": 0,
            "mean_unique_ratio": None,
            "mean_body_tokens": None,
        }

    docs: list[list[str]] = []
    for p in sample:
        docs.append(_tokens(p.body_text or ""))

    n = len(docs)
    df: Counter[str] = Counter()
    for toks in docs:
        df.update(set(toks))
    thresh = max(1, int(0.8 * n))
    shell = {w for w, c in df.items() if c >= thresh}

    ratios: list[float] = []
    lengths: list[int] = []
    for toks in docs:
        if not toks:
            continue
        lengths.append(len(toks))
        shell_hits = sum(1 for t in toks if t in shell)
        ratios.append(1.0 - shell_hits / len(toks))

    return {
        "sampled_pages": n,
        "shell_token_types": len(shell),
        "mean_unique_ratio": round(sum(ratios) / len(ratios), 4) if ratios else None,
        "mean_body_tokens": round(sum(lengths) / len(lengths), 1) if lengths else None,
        "shell_prevalence_threshold": 0.8,
    }


def detect_lang_profile(pages: list[Page]) -> dict[str, Any]:
    langs = Counter((p.lang or "und").strip() or "und" for p in pages)
    # drop und for diversity if others exist
    meaningful = {k: v for k, v in langs.items() if k not in ("und", "", "unknown")}
    if not meaningful:
        meaningful = dict(langs)
    distinct = len(meaningful)
    return {
        "lang_counts": dict(langs.most_common()),
        "distinct_langs": distinct,
        "monolingual": distinct <= 1,
        "primary_lang": meaningful and max(meaningful, key=meaningful.get) or None,
    }


def hub_degrees(pages: list[Page], top_n: int = 8) -> list[dict[str, Any]]:
    """Inbound internal-link degree by slug (approx)."""
    by_slug = {p.slug: p for p in pages if p.slug}
    inbound: Counter[str] = Counter()
    for p in pages:
        for link in p.internal_links or []:
            # links may be slug-like or paths
            leaf = str(link).rstrip("/").split("/")[-1]
            if leaf.endswith(".html"):
                leaf = leaf[:-5]
            if leaf in by_slug:
                inbound[leaf] += 1
    out = []
    for slug, deg in inbound.most_common(top_n):
        out.append({"slug": slug, "inbound_degree": deg, "page_type": page_type(slug)})
    return out


def build_site_understanding(
    pages: list[Page],
    *,
    cluster_summary: dict[str, Any] | None = None,
    sim_pair_count: int = 0,
) -> dict[str, Any]:
    """Site-level understanding object for dashboard overview."""
    type_hist = Counter(page_type(p.slug) for p in pages)
    lang = detect_lang_profile(pages)
    shell = estimate_shell_and_unique(pages)
    hubs = hub_degrees(pages)

    understanding = {
        "page_count": len(pages),
        "page_type_histogram": dict(type_hist.most_common()),
        "languages": lang,
        "template_shell_sketch": shell,
        "similarity_pair_count": sim_pair_count,
        "similarity_clusters": (cluster_summary or {}),
        "top_hubs_by_inbound": hubs,
        "notes": [],
    }
    if lang.get("monolingual"):
        understanding["notes"].append(
            "Site appears monolingual; missing hreflang alternate sets are often expected."
        )
    ur = shell.get("mean_unique_ratio")
    if ur is not None and ur >= 0.35:
        understanding["notes"].append(
            "Mean unique-content ratio is relatively high; thin template-shell risk is lower."
        )
    elif ur is not None and ur < 0.15 and len(pages) >= 10:
        understanding["notes"].append(
            "Mean unique-content ratio is low across many pages; template-shell review is warranted."
        )
    return understanding


def estimate_shell_and_unique_for_slugs(pages: list[Page], slugs: Iterable[str]) -> dict[str, Any]:
    """Shell/unique sketch restricted to a slug set (e.g. one similarity cluster)."""
    wanted = set(slugs or [])
    subset = [p for p in pages if p.slug in wanted]
    if not subset:
        # try leaf match
        leaves = {s.rsplit("/", 1)[-1] for s in wanted}
        subset = [p for p in pages if p.slug.rsplit("/", 1)[-1] in leaves or p.slug in wanted]
    return estimate_shell_and_unique(subset, sample_cap=max(80, len(subset) or 80))
