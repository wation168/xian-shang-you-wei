# -*- coding: utf-8 -*-
"""Phase-2 SaaS foundations: understanding + disposition."""
from __future__ import annotations

from seo_scanner.models import Page, Issue
from seo_scanner.understanding import detect_lang_profile, estimate_shell_and_unique, build_site_understanding
from seo_scanner.disposition import apply_disposition_rules


def _page(slug: str, lang: str, body: str, links=None) -> Page:
    return Page(
        path=f"{lang}/{slug}.html" if lang != "en" else f"{slug}.html",
        slug=slug,
        lang=lang,
        title=slug,
        body_text=body,
        body_len=len(body),
        internal_links=links or [],
        filename=f"{slug}.html",
    )


def test_monolingual_detection():
    pages = [_page("a", "en", "hello world " * 50), _page("b", "en", "another article " * 40)]
    prof = detect_lang_profile(pages)
    assert prof["monolingual"] is True
    assert prof["distinct_langs"] == 1


def test_multilingual_detection():
    pages = [_page("a", "en", "hello " * 40), _page("b", "zh-TW", "你好 " * 40)]
    prof = detect_lang_profile(pages)
    assert prof["monolingual"] is False
    assert prof["distinct_langs"] >= 2


def test_unique_ratio_higher_for_distinct_bodies():
    shared = ("nav footer menu home about " * 30)
    pages_thin = [
        _page("t1", "en", shared + " alpha"),
        _page("t2", "en", shared + " beta"),
        _page("t3", "en", shared + " gamma"),
        _page("t4", "en", shared + " delta"),
        _page("t5", "en", shared + " epsilon"),
    ]
    pages_rich = [
        _page("r1", "en", "completely unique essay about oceans and tides " * 40),
        _page("r2", "en", "different topic covering mountains and geology " * 40),
        _page("r3", "en", "third article on deserts climate and sand " * 40),
        _page("r4", "en", "fourth piece regarding forests canopy and birds " * 40),
        _page("r5", "en", "fifth narrative on cities architecture history " * 40),
    ]
    thin = estimate_shell_and_unique(pages_thin)
    rich = estimate_shell_and_unique(pages_rich)
    assert thin["mean_unique_ratio"] is not None and rich["mean_unique_ratio"] is not None
    assert rich["mean_unique_ratio"] > thin["mean_unique_ratio"]


def test_i18n_monolingual_hreflang_becomes_likely_exception():
    pages = [_page(f"p{i}", "en", ("unique body %d " % i) * 80) for i in range(12)]
    su = build_site_understanding(pages, sim_pair_count=0)
    assert su["languages"]["monolingual"] is True
    issue = Issue(
        id="i18n-1",
        category="i18n",
        problem="hreflang 缺漏：en, x-default",
        cause="missing",
        fix="add",
        priority="P2",
        evidence={},
        pages=["p0"],
    )
    apply_disposition_rules([issue], site_understanding=su)
    assert issue.evidence["disposition"] == "likely_exception"
    assert issue.priority == "P3"


def test_encyclopedia_mesh_softened_on_small_unique_mono_site():
    pages = [_page(f"doc{i}", "en", (f"chapter {i} covers topic-{i} with exclusive examples and narrative-{i} " * 50)) for i in range(16)]
    su = build_site_understanding(pages, sim_pair_count=0)
    issue = Issue(
        id="lopp-1",
        category="links",
        problem="百科／詞條 related 網格｜57 對｜1 語｜16 頁",
        cause="mesh",
        fix="add related",
        priority="P1",
        evidence={"link_opportunity": True, "high_value": True},
        pages=["doc0", "doc1"],
    )
    apply_disposition_rules([issue], site_understanding=su)
    assert issue.evidence["disposition"] == "likely_exception"
    assert issue.priority in ("P2", "P3")
    assert issue.evidence.get("high_value") is False


def test_template_cluster_stays_true_issue():
    pages = [_page("x", "en", "body")]
    su = build_site_understanding(pages)
    issue = Issue(
        id="simc-1",
        category="similarity",
        problem="模板殼",
        cause="shell",
        fix="differentiate",
        priority="P0",
        evidence={"cluster": True, "bucket": "actionable_template", "kind": "content_template"},
        pages=["a", "b"],
    )
    apply_disposition_rules([issue], site_understanding=su)
    assert issue.evidence["disposition"] == "true_issue"
    assert issue.priority == "P0"
