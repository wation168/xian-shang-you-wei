# -*- coding: utf-8 -*-
"""Issue disposition / confidence enrichment (SaaS judgment layer).

Detection remains in check modules; this layer classifies *how to treat* an issue
for product UX: Critical vs Needs Review vs Expected exception.
"""

from __future__ import annotations

from typing import Any

from .models import Issue


DISPOSITIONS = (
    "true_issue",
    "needs_review",
    "likely_exception",
    "insufficient_evidence",
)


def _ev(issue: Issue) -> dict[str, Any]:
    if issue.evidence is None:
        issue.evidence = {}
    return issue.evidence


def apply_disposition_rules(
    issues: list[Issue],
    *,
    site_understanding: dict[str, Any],
) -> list[Issue]:
    """Mutate issues in place: set evidence confidence/disposition/do_not_fix_if.

    Existing priority is preserved unless we explicitly soften noisy classes on
    monolingual / high-unique sites (priority demote P1/P2 → keep id but mark disposition).
    """
    mono = bool((site_understanding.get("languages") or {}).get("monolingual"))
    ur = (site_understanding.get("template_shell_sketch") or {}).get("mean_unique_ratio")
    page_count = int(site_understanding.get("page_count") or 0)

    for issue in issues:
        ev = _ev(issue)
        # URL Evidence Chain: honor chain judgment (do not force everything to insufficient)
        if ev.get("url_evidence"):
            d0 = ev.get("disposition") or "insufficient_evidence"
            if d0 not in ("true_issue", "needs_review", "likely_exception", "insufficient_evidence"):
                d0 = "insufficient_evidence"
            ev["disposition"] = d0
            ev.setdefault("confidence", "high" if d0 == "true_issue" else "low")
            continue
        if ev.get("disposition") == "insufficient_evidence":
            ev.setdefault("confidence", "low")
            continue
        # defaults
        if "disposition" not in ev:
            ev["disposition"] = "needs_review"
            ev["confidence"] = "medium"

        cat = issue.category or ""
        problem = issue.problem or ""

        # Similarity template clusters with actionable_template bucket → true_issue candidate
        if cat == "similarity" or ev.get("cluster"):
            if ev.get("bucket") == "actionable_template" or ev.get("kind") == "content_template":
                ev["disposition"] = "true_issue"
                ev["confidence"] = "high" if issue.priority in ("P0", "P1") else "medium"
                ev["do_not_fix_if"] = (
                    "Do not treat as spam solely because pages share a layout; "
                    "confirm unique payload is too thin for the page purpose."
                )
            elif ev.get("folded"):
                ev["disposition"] = "likely_exception"
                ev["confidence"] = "medium"

        # i18n: monolingual missing en/x-default → likely expected
        if cat == "i18n":
            if mono and ("hreflang" in problem.lower() or "hreflang" in problem or "缺漏" in problem):
                ev["disposition"] = "likely_exception"
                ev["confidence"] = "high"
                ev["do_not_fix_if"] = (
                    "Site looks monolingual; adding full hreflang alternate maps may be unnecessary."
                )
                # Soften priority for product Critical queue without deleting detection
                if issue.priority in ("P1", "P2"):
                    ev["priority_before_disposition"] = issue.priority
                    issue.priority = "P3"
            elif "重複" in problem or "duplicate" in problem.lower():
                ev["disposition"] = "true_issue"
                ev["confidence"] = "high"

        # Link opportunities: encyclopedia/page-type mesh on small high-unique mono sites
        if cat == "links" and ev.get("link_opportunity"):
            # Structural archive/date demotion from opportunity builder
            if ev.get("archive_date_demoted") or ev.get("kind") == "archive_date_demoted":
                ev["disposition"] = "likely_exception"
                ev["confidence"] = "high"
                ev["high_value"] = False
                ev["do_not_fix_if"] = (
                    "Year/year-month archive index shells rarely need mutual related links; "
                    "prefer topical articles or evergreen hubs."
                )
                if issue.priority in ("P0", "P1", "P2"):
                    ev.setdefault("priority_before_disposition", issue.priority)
                    issue.priority = "P3"
                continue
            meshy = any(
                k in problem
                for k in ("related 網格", "頁型", "百科", "詞條", "mesh", "網格")
            )
            mean_tok = (site_understanding.get("template_shell_sketch") or {}).get("mean_body_tokens")
            rich_enough = (ur is not None and ur >= 0.25) or (mean_tok is not None and mean_tok >= 800)
            if meshy and mono and rich_enough and page_count <= 80:
                ev["disposition"] = "likely_exception"
                ev["confidence"] = "medium"
                ev["do_not_fix_if"] = (
                    "Dense unique pages with existing navigation often do not need "
                    "a generated same-type related mesh."
                )
                if issue.priority in ("P0", "P1"):
                    ev["priority_before_disposition"] = issue.priority
                    issue.priority = "P2"
                ev["high_value"] = False
            elif ev.get("high_value") and not ev.get("folded"):
                ev["disposition"] = "needs_review"
                ev["confidence"] = "medium"
                ev.setdefault(
                    "do_not_fix_if",
                    "Skip if the suggested pair has no user-task relationship beyond shared tokens.",
                )

        # Meta title length etc. stay needs_review / low
        if cat == "meta":
            if "重複" in problem or "duplicate" in problem.lower() or "相同" in problem:
                ev["disposition"] = "needs_review"
                ev["confidence"] = "medium"
                ev["do_not_fix_if"] = (
                    "Identical titles are not automatically wrong; confirm page purpose differs."
                )
            else:
                ev["disposition"] = "needs_review"
                ev["confidence"] = "low"

        # Promote evidence fields to top-level mirrors for report convenience
        ev.setdefault("confidence", "medium")
        ev.setdefault("disposition", "needs_review")

    return issues


def disposition_counts(issues: list[Issue]) -> dict[str, int]:
    from collections import Counter
    c: Counter[str] = Counter()
    for it in issues:
        c[(it.evidence or {}).get("disposition") or "unset"] += 1
    return dict(c)
