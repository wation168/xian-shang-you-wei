# -*- coding: utf-8 -*-
"""page_type structural heuristics (no brand hardcoding)."""

from __future__ import annotations

import sys
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from seo_scanner.link_opportunities import page_type


def test_weblog_dated_slugs_not_tool_types():
    """Chronological blog/news slugs must be index/article, never converter/results."""
    weblog = [
        "2026",
        "2026_aug",
        "2026_aug_28_django-developers-survey-2026-results",
        "2026_sep_15_djangocon-europe-2027-is-heading-to-innsbruck",
        "2026_sep_18_proposed-change-to-dsf-voting-membership",
        "2026_sep_16_executive-director-search-extended",
        "2026_sep_02_bugfix-releases",
    ]
    hist = Counter(page_type(s) for s in weblog)
    assert hist.get("-converter", 0) == 0, hist
    assert hist.get("-results", 0) == 0, hist
    assert hist["index"] >= 2, hist
    assert hist["article"] >= 4, hist
    assert page_type("2026_aug_28_django-developers-survey-2026-results") == "article"
    assert page_type("2026_sep_15_djangocon-europe-2027-is-heading-to-innsbruck") == "article"


def test_tool_suffixes_still_classified():
    """Lottery/tool intentional suffixes and short unit X-to-Y remain tool types."""
    assert page_type("mega-millions-number-generator") == "-number-generator"
    assert page_type("powerball-results") == "-results"
    assert page_type("eurojackpot-statistics") == "-statistics"
    assert page_type("lotto-history") == "-history"
    assert page_type("currency-converter") == "-converter"
    assert page_type("usd-to-eur-converter") == "-converter"
    assert page_type("usd-to-eur") == "-converter"
    assert page_type("mortgage-calculator") == "-calculator"
    assert page_type("loan-to-value-calculator") == "-calculator"


def test_prose_to_and_howto_not_converter():
    assert page_type("heading-to-innsbruck") == "other"
    assert page_type("change-to-dsf-voting-membership") == "other"
    assert page_type("how-to-install-python") == "article"
    assert page_type("abandoned-baby-bearish") == "other"
    assert page_type("python-for-loops") == "other"


if __name__ == "__main__":
    test_weblog_dated_slugs_not_tool_types()
    test_tool_suffixes_still_classified()
    test_prose_to_and_howto_not_converter()
    print("ALL page_type TESTS PASSED")