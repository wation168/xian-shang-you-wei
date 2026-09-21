# -*- coding: utf-8 -*-
from seo_scanner.models import Page
from seo_scanner.url_evidence import check_missing_local_targets
from seo_scanner.disposition import apply_disposition_rules
from seo_scanner.understanding import build_site_understanding


def _p(slug, links):
    return Page(path=f"{slug}.html", slug=slug, lang="en", body_text="x "*50, internal_links=links, abs_path=f"/tmp/{slug}.html")


def test_missing_slug_is_insufficient_evidence():
    pages = [
        _p("home", ["home", "ghost-page"]),
        _p("about", ["home"]),
    ]
    issues = check_missing_local_targets(pages)
    assert len(issues) == 1
    ev = issues[0].evidence
    assert ev["disposition"] == "insufficient_evidence"
    assert issues[0].priority == "P3"
    assert "ghost-page" in ev["missing_targets_sample"]


def test_disposition_preserves_url_evidence():
    pages = [_p("home", ["ghost"])]
    issues = check_missing_local_targets(pages)
    su = build_site_understanding(pages)
    apply_disposition_rules(issues, site_understanding=su)
    assert issues[0].evidence["disposition"] == "insufficient_evidence"
