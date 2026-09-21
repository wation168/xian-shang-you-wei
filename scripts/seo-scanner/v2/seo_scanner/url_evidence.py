# -*- coding: utf-8 -*-
"""URL evidence integration for diagnose.

Offline default: missing internal link slugs → insufficient_evidence (NOT 404).
Optional HTTP fixture/live probe can promote confirmed 404/loop to true_issue.
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any, Optional

from .http_probe import load_probe_fixture, resolve_probe
from .link_opportunities import page_type
from .models import Issue, Page
from .url_chain import UrlEvidenceChain, build_chain_from_probe, summarize_chains


def _known_slugs(pages: list[Page]) -> tuple[set[str], set[str]]:
    known = {p.slug for p in pages}
    known_leaves = {s.rsplit("/", 1)[-1] for s in known}
    return known, known_leaves


def _target_known(link: str, known: set[str], known_leaves: set[str]) -> bool:
    leaf = link.rsplit("/", 1)[-1]
    return link in known or leaf in known_leaves


def collect_missing_targets(
    pages: list[Page],
    *,
    max_targets: int = 40,
) -> dict[str, list[str]]:
    known, known_leaves = _known_slugs(pages)
    missing: dict[str, list[str]] = defaultdict(list)
    for page in pages:
        for raw in page.internal_links or []:
            link = str(raw).strip()
            if not link or link.startswith("#"):
                continue
            leaf = link.rsplit("/", 1)[-1]
            if leaf in {"index", "home", "css", "js"}:
                continue
            if _target_known(link, known, known_leaves):
                continue
            missing[link].append(page.slug)
            if len(missing) >= max_targets:
                return missing
    return missing


def load_local_sitemap_urls(site_root: Optional[str | Path]) -> tuple[bool, set[str]]:
    """Best-effort local sitemap*.xml parse. Returns (checked, urls)."""
    if not site_root:
        return False, set()
    root = Path(site_root)
    if not root.is_dir():
        return False, set()
    files = list(root.glob("sitemap*.xml")) + list(root.glob("**/sitemap*.xml"))
    if not files:
        return False, set()
    urls: set[str] = set()
    for f in files[:5]:
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        # minimal <loc> scrape
        parts = text.split("<loc>")
        for part in parts[1:]:
            loc = part.split("</loc>", 1)[0].strip()
            if loc:
                urls.add(loc)
    return True, urls


def build_url_evidence_issues(
    pages: list[Page],
    *,
    site_root: Optional[str | Path] = None,
    probe_fixture_path: Optional[str | Path] = None,
    http_live: bool = False,
    max_targets: int = 40,
    max_chain_issues: int = 12,
) -> tuple[list[Issue], dict[str, Any]]:
    """Emit URL-evidence issues + summary for diagnose.

    - Without HTTP: one folded insufficient_evidence for missing local slugs.
    - With fixture/live confirming 404/loop: separate true_issue rows (capped).
    """
    fixture = load_probe_fixture(probe_fixture_path) if probe_fixture_path else None
    sitemap_checked, sitemap_urls = load_local_sitemap_urls(site_root)
    missing = collect_missing_targets(pages, max_targets=max_targets)

    by_slug = {p.slug: p for p in pages}
    chains: list[UrlEvidenceChain] = []
    issues: list[Issue] = []

    # Chains for missing targets (lifecycle / 404 decisions)
    true_issue_count = 0
    for target, sources in sorted(missing.items()):
        probe = resolve_probe(target, fixture=fixture, live=http_live)
        # lifecycle soft hint from naming only — never invent cause
        hints: list[str] = []
        low = target.lower()
        if any(x in low for x in ("old-", "legacy", "/old/", "deprecated")):
            hints.append("name_suggests_legacy_slug")

        chain = build_chain_from_probe(
            target,
            probe=probe,
            sitemap_urls=sitemap_urls,
            sitemap_checked=sitemap_checked,
            local_slug_known=False,
            link_sources=sources[:8],
            lifecycle_hints=hints,
        )
        chains.append(chain)

        if chain.judgment == "true_issue" and true_issue_count < max_chain_issues:
            true_issue_count += 1
            http = chain.get("http_response")
            final_status = (http.data or {}).get("final_status") if http else None
            issues.append(
                Issue(
                    id=f"url-http-{true_issue_count:02d}",
                    category="links",
                    problem=f"URL HTTP 證據確認異常｜{target}｜status={final_status}",
                    cause="URL Evidence Chain：已確認 HTTP／redirect 結果指向錯誤或迴圈。",
                    fix="依 final URL／redirect 鏈修正連結或伺服器回應；勿在無 HTTP 時當 404。",
                    priority="P1",
                    evidence={
                        "url_evidence": True,
                        "url_evidence_chain": chain.to_dict(),
                        "http_checked": True,
                        "disposition": "true_issue",
                        "confidence": chain.confidence,
                        "do_not_fix_if": "Only if HTTP probe was wrong environment (staging vs prod).",
                    },
                    pages=sources[:20],
                )
            )

    # Always keep offline missing-slug rollup as insufficient_evidence (never 404)
    if missing:
        targets = sorted(missing.keys())[:max_targets]
        sample_map = {t: missing[t][:5] for t in targets}
        # Attach a representative chain (first missing) for Dashboard transparency
        sample_chain = chains[0].to_dict() if chains else None
        issues.append(
            Issue(
                id="url-missing-local-01",
                category="links",
                problem=f"掃描集內找不到連結目標｜{len(targets)} 個 slug（證據不足）",
                cause=(
                    "內部連結指向的 slug 不在本次掃描頁面集合中；"
                    "離線掃描無法確認線上路由／301／sitemap／歷史 URL。"
                ),
                fix=(
                    "走 URL 證據鏈（HTTP／redirect／sitemap／替代）後再決定；"
                    "確認前不要當搬站錯誤直接改站。"
                ),
                priority="P3",
                evidence={
                    "url_evidence": True,
                    "file_exists": False,
                    "http_checked": bool(fixture) or http_live,
                    "missing_target_count": len(targets),
                    "missing_targets_sample": targets[:20],
                    "sources_sample": sample_map,
                    "url_evidence_chain_sample": sample_chain,
                    "disposition": "insufficient_evidence",
                    "confidence": "low",
                    "do_not_fix_if": (
                        "Do not treat as a migration/SEO 404 without HTTP, redirect, or sitemap evidence."
                    ),
                },
                pages=sorted({s for srcs in sample_map.values() for s in srcs})[:40],
            )
        )

    # Optional: page-level canonical/hreflang chains for scanned pages with fixture keys
    # (documentation / needs_review) — only when fixture provides page URL probes
    if fixture:
        extra = 0
        for page in pages:
            if extra >= 5:
                break
            probe = resolve_probe(page.slug, fixture=fixture, live=False)
            if probe is None and page.path:
                probe = resolve_probe(page.path, fixture=fixture, live=False)
            if probe is None:
                continue
            chain = build_chain_from_probe(
                page.slug or page.path,
                probe=probe,
                page_canonical=page.canonical or "",
                page_hreflang=dict(page.hreflang or {}),
                page_type=page_type(page.slug),
                page_lang=page.lang or "",
                sitemap_urls=sitemap_urls,
                sitemap_checked=sitemap_checked,
                local_slug_known=True,
            )
            chains.append(chain)
            if chain.judgment in ("needs_review", "true_issue") and chain.get("canonical"):
                can = chain.get("canonical")
                if can and can.data.get("matches_final_or_target") is False:
                    extra += 1
                    issues.append(
                        Issue(
                            id=f"url-canonical-{extra:02d}",
                            category="meta",
                            problem=f"Canonical 與 final/target 不一致（需審）｜{page.slug}",
                            cause="URL Evidence Chain：canonical 已確認存在但與 HTTP final／頁面 URL 關係不明。",
                            fix="結合語言、page type、內容關係後再改；不要只因不同就改。",
                            priority="P2",
                            evidence={
                                "url_evidence": True,
                                "url_evidence_chain": chain.to_dict(),
                                "disposition": chain.judgment,
                                "confidence": chain.confidence,
                                "do_not_fix_if": chain.evidence_gap
                                or "Canonical pointing at a language/hub variant may be intentional.",
                            },
                            pages=[page.slug],
                        )
                    )

    summary = {
        "url_evidence_chain": summarize_chains(chains),
        "missing_local_targets": len(missing),
        "sitemap_checked": sitemap_checked,
        "sitemap_url_count": len(sitemap_urls),
        "http_fixture_loaded": bool(fixture),
        "http_live": http_live,
    }
    return issues, summary


# Back-compat wrapper used by older diagnose imports
def check_missing_local_targets(
    pages: list[Page],
    *,
    max_targets: int = 40,
) -> list[Issue]:
    issues, _ = build_url_evidence_issues(pages, max_targets=max_targets)
    return issues
