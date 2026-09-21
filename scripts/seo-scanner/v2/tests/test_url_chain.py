# -*- coding: utf-8 -*-
"""URL Evidence Chain unit cases (fixture HTTP — no live network)."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from seo_scanner.url_chain import build_chain_from_probe, classify_redirect
from seo_scanner.http_probe import load_probe_fixture, lookup_probe
from seo_scanner.url_evidence import build_url_evidence_issues
from seo_scanner.models import Page


FIXTURE = ROOT / "fixtures" / "url_probe_cases.json"
# When installed under v2/tests, fixtures may live at v2/fixtures
if not FIXTURE.exists():
    FIXTURE = ROOT.parent / "fixtures" / "url_probe_cases.json"
if not FIXTURE.exists():
    FIXTURE = Path(__file__).resolve().parent.parent / "fixtures" / "url_probe_cases.json"


class TestUrlChain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fx = load_probe_fixture(FIXTURE)

    def test_normal_200(self):
        c = build_chain_from_probe(
            "https://example.com/ok",
            probe=self.fx["https://example.com/ok"],
            local_slug_known=True,
            sitemap_checked=True,
            sitemap_urls={"https://example.com/ok"},
        )
        self.assertEqual(c.status_map()["http_response"], "confirmed")
        self.assertEqual(c.status_map()["redirect"], "not_applicable")
        self.assertEqual(c.status_map()["sitemap"], "confirmed")
        self.assertNotEqual(c.judgment, "true_issue")

    def test_404_is_true_issue(self):
        c = build_chain_from_probe(
            "https://example.com/gone",
            probe=self.fx["https://example.com/gone"],
            local_slug_known=False,
        )
        self.assertEqual(c.judgment, "true_issue")
        self.assertEqual(c.confidence, "high")

    def test_single_redirect_not_problem(self):
        c = build_chain_from_probe(
            "https://example.com/old",
            probe=self.fx["https://example.com/old"],
            local_slug_known=False,
        )
        self.assertEqual(c.get("redirect").data.get("kind"), "normal")
        self.assertNotEqual(c.judgment, "true_issue")

    def test_redirect_chain_needs_review(self):
        c = build_chain_from_probe(
            "https://example.com/chain",
            probe=self.fx["https://example.com/chain"],
        )
        self.assertEqual(c.get("redirect").data.get("kind"), "chain")
        self.assertEqual(c.judgment, "needs_review")

    def test_redirect_loop_true_issue(self):
        c = build_chain_from_probe(
            "https://example.com/loop",
            probe=self.fx["https://example.com/loop"],
        )
        self.assertEqual(c.get("redirect").data.get("kind"), "loop")
        self.assertEqual(c.judgment, "true_issue")

    def test_canonical_mismatch_not_auto_true(self):
        c = build_chain_from_probe(
            "https://example.com/page-with-canon",
            probe=self.fx["page-with-canon"],
            page_canonical="https://example.com/other-canon",
            page_type="article",
            page_lang="en",
            local_slug_known=True,
        )
        self.assertEqual(c.judgment, "needs_review")
        self.assertIn("Canonical", c.evidence_gap or c.notes or "Canonical")

    def test_missing_slug_without_http_insufficient(self):
        c = build_chain_from_probe(
            "powerball-number-generator",
            probe=None,
            local_slug_known=False,
        )
        self.assertEqual(c.status_map()["http_response"], "unavailable")
        self.assertEqual(c.judgment, "insufficient_evidence")
        self.assertIn("404", c.evidence_gap.lower() or "")

    def test_sitemap_absent_not_broken(self):
        c = build_chain_from_probe(
            "https://example.com/ok",
            probe=None,
            sitemap_checked=True,
            sitemap_urls=set(),
            local_slug_known=True,
        )
        self.assertEqual(c.status_map()["sitemap"], "confirmed")
        self.assertIs(c.get("sitemap").data.get("in_sitemap"), False)
        self.assertEqual(c.judgment, "insufficient_evidence")

    def test_lifecycle_evidence_gap(self):
        c = build_chain_from_probe(
            "legacy-old-page",
            probe=None,
            local_slug_known=False,
            lifecycle_hints=["name_suggests_legacy_slug"],
        )
        self.assertEqual(c.judgment, "insufficient_evidence")
        self.assertTrue(c.evidence_gap)

    def test_build_issues_number_generator_not_404(self):
        pages = [
            Page(
                path="en/a.html",
                slug="a",
                lang="en",
                internal_links=["powerball-number-generator", "mega-millions-number-generator"],
            )
        ]
        issues, summary = build_url_evidence_issues(pages, probe_fixture_path=None)
        self.assertTrue(any(i.id == "url-missing-local-01" for i in issues))
        miss = next(i for i in issues if i.id == "url-missing-local-01")
        self.assertEqual(miss.evidence.get("disposition"), "insufficient_evidence")
        self.assertFalse(any("404" in (i.problem or "") for i in issues))
        # no true_issue http rows without fixture
        self.assertFalse(any(i.id.startswith("url-http-") for i in issues))

    def test_build_issues_http_404_promotes(self):
        pages = [
            Page(
                path="en/a.html",
                slug="a",
                lang="en",
                internal_links=["https://example.com/gone"],
            )
        ]
        issues, summary = build_url_evidence_issues(pages, probe_fixture_path=FIXTURE)
        http_issues = [i for i in issues if i.id.startswith("url-http-")]
        self.assertTrue(http_issues)
        self.assertEqual(http_issues[0].evidence.get("disposition"), "true_issue")


if __name__ == "__main__":
    unittest.main()
