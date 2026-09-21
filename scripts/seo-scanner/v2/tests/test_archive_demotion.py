# -*- coding: utf-8 -*-
"""Archive/date URL demotion for link opportunities (structural only)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from seo_scanner.models import Issue
from seo_scanner.link_opportunities import (
    page_type,
    _is_archive_index,
    _is_archive_shell_pair,
    _overlap_is_calendar_only,
    build_link_opportunities,
    opportunity_summary,
)


def test_archive_index_path_forms():
    assert _is_archive_index("2026")
    assert _is_archive_index("2026_sep")
    assert _is_archive_index("2026-09")
    assert _is_archive_index("2024-01")
    assert _is_archive_index("2026/09")
    assert _is_archive_index("blog/2026/sep")
    assert _is_archive_index("page-2")
    assert page_type("2026/09") == "index"
    assert page_type("2026_sep") == "index"
    # archive/<year> path form (leaf year) — already covered structurally
    assert _is_archive_index("archive/2026")
    assert _is_archive_index("archives/2026")
    assert _is_archive_index("blog/archive/2026")
    assert page_type("archive/2026") == "index"
    # year + pagination under path: 2026/page/2
    assert _is_archive_index("2026/page/2")
    assert _is_archive_index("2026/page/3")
    assert _is_archive_index("archive/2026/page/2")
    assert _is_archive_index("2026/09/page/2")
    assert page_type("2026/page/2") == "index"
    # dated article is NOT archive index
    assert not _is_archive_index("2026_sep_15_djangocon-europe-2027-is-heading-to-innsbruck")
    assert page_type("2026_sep_15_djangocon-europe-2027-is-heading-to-innsbruck") == "article"


def test_archive_shell_pair_positive():
    assert _is_archive_shell_pair("2026", "2026_sep")
    assert _is_archive_shell_pair("2026_aug", "2026_jun")
    assert _is_archive_shell_pair("2026/09", "2026/08")
    assert _is_archive_shell_pair("archive/2026", "2026/page/2")
    assert _is_archive_shell_pair("2026/page/2", "2026/page/3")
    assert _overlap_is_calendar_only("2026", "2026_sep")


def test_archive_shell_pair_negative_topical_articles():
    """Two topical articles must stay eligible (not demoted as archive shells)."""
    a = "mortgage-refinance-calculator"
    b = "home-loan-amortization-calculator"
    assert not _is_archive_shell_pair(a, b)
    assert not _overlap_is_calendar_only(a, b)
    # dated articles with unique bodies are not archive shells
    a2 = "2026_sep_15_djangocon-europe-2027-is-heading-to-innsbruck"
    b2 = "2026_aug_28_django-developers-survey-2026-results"
    assert not _is_archive_shell_pair(a2, b2)


def _pair_issue(slug_a: str, slug_b: str, sim: float, lang: str = "en") -> Issue:
    return Issue(
        id="lp-%s-%s" % (slug_a[:12], slug_b[:12]),
        category="links",
        problem="pair",
        cause="",
        fix="",
        priority="P2" if sim >= 0.28 else "P3",
        evidence={
            "lang": lang,
            "link_sim": sim,
            "body_lens": [800, 800],
            "paths": [slug_a, slug_b],
        },
        pages=[slug_a, slug_b],
    )


def test_build_demotes_archive_index_mesh():
    """Year↔year-month pairs should not stay high_value template/strong_pair."""
    pairs = [
        ("2026", "2026_sep", 0.92),
        ("2026", "2026_aug", 0.72),
        ("2026_aug", "2026_jun", 0.56),
        ("2026_aug", "2026_sep", 0.56),
        ("2026", "2026_jun", 0.55),
        ("2026_may", "2026_jul", 0.50),
    ]
    issues = [_pair_issue(a, b, s) for a, b, s in pairs]
    opps = build_link_opportunities(issues)
    summary = opportunity_summary(opps)
    assert summary["bucket_counts"]["strong_pair"] == 0, summary
    # archive mesh demoted to folded
    demoted = [o for o in opps if o.kind == "archive_date_demoted" or (o.evidence or {}).get("archive_date_demoted")]
    assert demoted, [o.kind for o in opps]
    assert all(not o.high_value for o in demoted)
    assert all(o.folded for o in demoted)
    assert summary["high_value_count"] == 0, summary
    assert summary.get("archive_date_demoted_count", 0) >= 1


def test_build_keeps_topical_strong_or_template():
    """Tool/topic pairs with real overlap stay eligible for high_value buckets."""
    pairs = [
        ("mortgage-refinance-calculator", "home-loan-calculator", 0.80),
        ("mortgage-refinance-calculator", "heloc-calculator", 0.70),
        ("personal-loan-calculator", "car-loan-calculator", 0.65),
        ("student-loan-refi-calculator", "mortgage-refinance-calculator", 0.60),
        ("business-loan-calculator", "personal-loan-calculator", 0.58),
        ("loan-amortization-calculator", "mortgage-calculator", 0.57),
    ]
    issues = [_pair_issue(a, b, s) for a, b, s in pairs]
    opps = build_link_opportunities(issues)
    summary = opportunity_summary(opps)
    # Should not classify as archive demotion
    demoted = [o for o in opps if o.kind == "archive_date_demoted"]
    assert not demoted, demoted
    # Expect some high_value (template mesh of -calculator or topic/strong)
    assert summary["high_value_count"] >= 1, summary
    assert summary["bucket_counts"]["strong_pair"] + summary["bucket_counts"]["template"] + summary["bucket_counts"]["topic"] >= 1


if __name__ == "__main__":
    test_archive_index_path_forms()
    test_archive_shell_pair_positive()
    test_archive_shell_pair_negative_topical_articles()
    test_build_demotes_archive_index_mesh()
    test_build_keeps_topical_strong_or_template()
    print("ALL archive_demotion TESTS PASSED")
