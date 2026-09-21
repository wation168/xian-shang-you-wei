# -*- coding: utf-8 -*-
"""彙整各檢查模組的 Issue，排序並產出摘要。"""

from __future__ import annotations

from collections import Counter
from typing import Any, Optional

from .models import Page, Issue, PRIORITY_ORDER
from .similarity import compute_similarity_pairs, SimPair
from .sim_clusters import build_sim_clusters, clusters_to_issues, cluster_summary
from .link_opportunities import (
    build_link_opportunities,
    opportunities_to_issues,
    opportunity_summary,
)
from .checks_meta import check_meta
from .checks_links import check_links
from .checks_i18n import check_i18n
from .understanding import build_site_understanding, estimate_shell_and_unique_for_slugs
from .disposition import apply_disposition_rules, disposition_counts
from .url_evidence import build_url_evidence_issues


def _enrich_similarity_shell_metrics(
    issues: list[Issue],
    pages: list[Page],
    site_understanding: dict[str, Any],
) -> None:
    """Attach generic template-shell sketch onto similarity cluster issues."""
    shell = site_understanding.get("template_shell_sketch") or {}
    for issue in issues:
        if issue.category != "similarity":
            continue
        ev = issue.evidence if issue.evidence is not None else {}
        issue.evidence = ev
        slugs = list(ev.get("slugs") or issue.pages or [])
        cluster_shell = estimate_shell_and_unique_for_slugs(pages, slugs) if slugs else {}
        metrics = {
            "site_mean_unique_ratio": shell.get("mean_unique_ratio"),
            "site_shell_token_types": shell.get("shell_token_types"),
            "site_mean_body_tokens": shell.get("mean_body_tokens"),
            "cluster_mean_unique_ratio": cluster_shell.get("mean_unique_ratio"),
            "cluster_shell_token_types": cluster_shell.get("shell_token_types"),
            "cluster_mean_body_tokens": cluster_shell.get("mean_body_tokens"),
            "cluster_pair_count": ev.get("pair_count"),
            "cluster_page_count": ev.get("page_count") or len(issue.pages or []),
            "note": (
                "Shell/unique ratios are structural estimates for review; "
                "they are not Google spam classifications. Prefer cluster_* over site_* for template clusters."
            ),
        }
        ev["template_shell_metrics"] = metrics


def run_all_checks(
    pages: list[Page],
    gsc_impressions: Optional[dict[str, int]] = None,
    *,
    site_root: Optional[str] = None,
    probe_fixture_path: Optional[str] = None,
    http_live: bool = False,
) -> tuple[list[Issue], list[SimPair], dict[str, Any]]:
    """執行全部檢查，回傳 (issues, sim_pairs, summary)。

    相似度／內連皆以 Cluster／Opportunity 為診斷單位；
    pairwise 完整保留在 summary（sim clusters.pair_refs／link_pairs）。
    """
    sim_pairs = compute_similarity_pairs(pages)
    clusters = build_sim_clusters(sim_pairs)

    # 底層內連候選不變；聚合層只改呈現單位
    link_pair_issues = check_links(pages, sim_pairs)
    link_opps = build_link_opportunities(link_pair_issues)

    issues: list[Issue] = []
    _url_evidence_summary: dict[str, Any] = {}
    issues.extend(clusters_to_issues(clusters))
    issues.extend(check_meta(pages))
    issues.extend(opportunities_to_issues(link_opps))
    issues.extend(check_i18n(pages))
    _url_evidence_issues, _url_evidence_summary = build_url_evidence_issues(
        pages,
        site_root=site_root,
        probe_fixture_path=probe_fixture_path,
        http_live=http_live,
    )
    issues.extend(_url_evidence_issues)

    if gsc_impressions:
        zero_slugs = {k for k, v in gsc_impressions.items() if v == 0}
        for issue in issues:
            if issue.priority in ("P2", "P3") and any(
                s in zero_slugs or any(s in z or z in s for z in zero_slugs)
                for s in issue.pages
            ):
                if issue.category == "similarity":
                    if issue.evidence.get("folded"):
                        continue
                    if issue.evidence.get("bucket") != "actionable_template":
                        continue
                elif issue.category == "links":
                    if issue.evidence.get("folded"):
                        continue
                    if not issue.evidence.get("high_value"):
                        continue
                elif issue.category not in ("thin", "meta"):
                    continue
                bump = {"P3": "P2", "P2": "P1"}
                if issue.priority in bump:
                    issue.priority = bump[issue.priority]
                    issue.evidence["gsc_zero_impression"] = True

    csum = cluster_summary(clusters)
    lsum = opportunity_summary(link_opps)

    site_understanding = build_site_understanding(
        pages,
        cluster_summary=csum,
        sim_pair_count=len(sim_pairs),
    )
    _enrich_similarity_shell_metrics(issues, pages, site_understanding)
    apply_disposition_rules(issues, site_understanding=site_understanding)

    # Keep opportunity cards consistent with disposition softens (additive sync)
    issue_by_id = {i.id: i for i in issues}
    for opp in link_opps:
        it = issue_by_id.get(opp.id)
        if not it:
            continue
        ev = it.evidence or {}
        if ev.get("disposition") == "likely_exception":
            opp.high_value = False
            if it.priority:
                opp.priority = it.priority

    # Re-sort / re-count after disposition may soften priorities
    lsum = opportunity_summary(link_opps)

    issues.sort(
        key=lambda x: (
            PRIORITY_ORDER.get(x.priority, 9),
            1 if x.evidence.get("folded") else 0,
            x.category,
            x.id,
        )
    )

    pri_counts = Counter(i.priority for i in issues)
    cat_counts = Counter(i.category for i in issues)
    pair_cls = Counter(p.classification for p in sim_pairs)

    # 原始 pairwise 完整保留（供 Dashboard 展開／追溯）
    link_pairs = []
    for it in link_pair_issues:
        ev = it.evidence or {}
        pages_ = it.pages or []
        if len(pages_) < 2:
            continue
        link_pairs.append(
            {
                "id": it.id,
                "slug_a": pages_[0],
                "slug_b": pages_[1],
                "lang": ev.get("lang"),
                "link_sim": ev.get("link_sim"),
                "priority": it.priority,
                "body_lens": ev.get("body_lens"),
                "paths": ev.get("paths"),
            }
        )

    disp = disposition_counts(issues)
    summary = {
        "page_count": len(pages),
        "issue_count": len(issues),
        "priority_counts": {
            "P0": pri_counts.get("P0", 0),
            "P1": pri_counts.get("P1", 0),
            "P2": pri_counts.get("P2", 0),
            "P3": pri_counts.get("P3", 0),
        },
        "category_counts": dict(cat_counts),
        "similarity_classifications": dict(pair_cls),
        "similarity_pair_count": len(sim_pairs),
        "clusters": [c.to_dict() for c in clusters],
        "cluster_summary": csum,
        "link_pair_count": len(link_pairs),
        "link_pairs": link_pairs,
        "link_opportunities": [o.to_dict() for o in link_opps],
        "link_opportunity_summary": lsum,
        "lang_counts": dict(Counter(p.lang for p in pages)),
        "site_understanding": site_understanding,
        "disposition_counts": disp,
        # Product-facing Critical vs Needs Review (conceptual buckets)
        "url_evidence_summary": _url_evidence_summary,
        "review_buckets": {
            "critical_true_issue": sum(
                1
                for i in issues
                if (i.evidence or {}).get("disposition") == "true_issue"
                and i.priority in ("P0", "P1")
            ),
            "needs_review": disp.get("needs_review", 0),
            "likely_exception": disp.get("likely_exception", 0),
            "insufficient_evidence": disp.get("insufficient_evidence", 0),
        },
    }
    return issues, sim_pairs, summary
