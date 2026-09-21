# -*- coding: utf-8 -*-
"""Phase 2: site understanding, monolingual detection, disposition heuristics."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from seo_scanner.models import Page, Issue
from seo_scanner.understanding import (
    detect_lang_profile,
    estimate_shell_and_unique,
    build_site_understanding,
)
from seo_scanner.disposition import apply_disposition_rules, disposition_counts


def _page(slug: str, lang: str, body: str, links: list | None = None) -> Page:
    return Page(
        path=f"{lang}/{slug}.html",
        slug=slug,
        lang=lang,
        title=slug,
        body_text=body,
        body_len=len(body),
        internal_links=links or [],
        filename=f"{slug}.html",
    )


def test_monolingual_detection():
    pages = [_page(f"p{i}", "en", f"unique content about topic {i} " * 40) for i in range(5)]
    prof = detect_lang_profile(pages)
    assert prof["monolingual"] is True
    assert prof["distinct_langs"] == 1
    assert prof["primary_lang"] == "en"

    pages_multi = pages + [_page("pX", "zh-TW", "這是繁中內容 " * 40)]
    prof2 = detect_lang_profile(pages_multi)
    assert prof2["monolingual"] is False
    assert prof2["distinct_langs"] >= 2


def test_unique_ratio_high_vs_shell():
    # High unique: each page has distinct payload
    high = [
        _page(
            f"u{i}",
            "en",
            ("shared nav footer " * 3)
            + (" ".join(f"exclusive{i}word{j}" for j in range(120))),
        )
        for i in range(8)
    ]
    hi = estimate_shell_and_unique(high)
    assert hi["mean_unique_ratio"] is not None
    assert hi["mean_unique_ratio"] >= 0.35, hi

    # Low unique: nearly identical body
    shell_body = "template shell boilerplate " * 100
    low = [_page(f"s{i}", "en", shell_body + f" {i}") for i in range(8)]
    lo = estimate_shell_and_unique(low)
    assert lo["mean_unique_ratio"] is not None
    assert lo["mean_unique_ratio"] < 0.25, lo
    assert hi["mean_unique_ratio"] > lo["mean_unique_ratio"]


def test_disposition_monolingual_i18n_softens():
    pages = [
        _page(
            f"p{i}",
            "en",
            ("nav home about " * 2)
            + (" ".join(f"chapter{i}concept{j}" for j in range(100))),
        )
        for i in range(6)
    ]
    und = build_site_understanding(pages, cluster_summary={"cluster_count": 0}, sim_pair_count=0)
    assert und["languages"]["monolingual"] is True
    assert (und["template_shell_sketch"]["mean_unique_ratio"] or 0) >= 0.35, und["template_shell_sketch"]

    issues = [
        Issue(
            id="i18n-1",
            category="i18n",
            problem="hreflang 缺漏：en, x-default",
            cause="expected alternates",
            fix="add tags",
            priority="P2",
            evidence={},
            pages=["p0"],
        ),
        Issue(
            id="link-1",
            category="links",
            problem="百科／詞條 related 網格｜57 對｜1 語｜16 頁",
            cause="same type mesh",
            fix="add links",
            priority="P1",
            evidence={"link_opportunity": True, "high_value": True},
            pages=["p0", "p1"],
        ),
        Issue(
            id="sim-1",
            category="similarity",
            problem="template shell cluster",
            cause="near-identical",
            fix="add unique",
            priority="P0",
            evidence={"bucket": "actionable_template", "kind": "content_template", "cluster": True},
            pages=["p0", "p1"],
        ),
    ]
    apply_disposition_rules(issues, site_understanding=und)
    by_id = {i.id: i for i in issues}

    assert by_id["i18n-1"].evidence["disposition"] == "likely_exception"
    assert by_id["i18n-1"].priority == "P3"
    assert by_id["i18n-1"].evidence.get("priority_before_disposition") == "P2"

    assert by_id["link-1"].evidence["disposition"] == "likely_exception"
    assert by_id["link-1"].priority in ("P2", "P3")
    assert by_id["link-1"].evidence.get("high_value") is False

    assert by_id["sim-1"].evidence["disposition"] == "true_issue"
    assert by_id["sim-1"].priority == "P0"

    counts = disposition_counts(issues)
    assert counts.get("likely_exception", 0) >= 2
    assert counts.get("true_issue", 0) >= 1


def test_multilingual_i18n_not_auto_exception():
    pages = [
        _page("a", "en", "hello world content " * 30),
        _page("a", "zh-TW", "繁中內容正文 " * 30),
        _page("b", "en", "other page content " * 30),
        _page("b", "zh-TW", "另一頁繁中 " * 30),
    ]
    und = build_site_understanding(pages)
    assert und["languages"]["monolingual"] is False
    issue = Issue(
        id="i18n-2",
        category="i18n",
        problem="hreflang 缺漏：x-default",
        cause="missing",
        fix="add",
        priority="P2",
        evidence={},
        pages=["a"],
    )
    apply_disposition_rules([issue], site_understanding=und)
    # Multilingual: monolingual soft-rule must not fire
    assert issue.priority == "P2"
    assert issue.evidence.get("disposition") != "likely_exception"
    assert "priority_before_disposition" not in (issue.evidence or {})


if __name__ == "__main__":
    test_monolingual_detection()
    test_unique_ratio_high_vs_shell()
    test_disposition_monolingual_i18n_softens()
    test_multilingual_i18n_not_auto_exception()
    print("ALL PHASE2 TESTS PASSED")
