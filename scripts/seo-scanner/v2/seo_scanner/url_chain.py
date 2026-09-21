# -*- coding: utf-8 -*-
"""URL Evidence Chain — SaaS-general evidence statuses (not more scan rules).

Each stage is one of:
  confirmed | unconfirmed | not_applicable | unavailable

Never treat "no evidence" as "there is a problem".
HTTP probing is optional; offline scans mark HTTP stages unavailable.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Optional
from urllib.parse import urlparse

STATUSES = ("confirmed", "unconfirmed", "not_applicable", "unavailable")

STAGES = (
    "url",
    "http_response",
    "redirect",
    "final_url",
    "canonical",
    "hreflang",
    "sitemap",
    "internal_links",
    "alternate_url",
    "history_source",
)


@dataclass
class StageEvidence:
    stage: str
    status: str  # confirmed|unconfirmed|not_applicable|unavailable
    detail: str = ""
    data: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class UrlEvidenceChain:
    target: str
    stages: list[StageEvidence] = field(default_factory=list)
    judgment: str = "insufficient_evidence"  # disposition hint
    confidence: str = "low"
    evidence_gap: str = ""
    notes: list[str] = field(default_factory=list)

    def status_map(self) -> dict[str, str]:
        return {s.stage: s.status for s in self.stages}

    def get(self, stage: str) -> Optional[StageEvidence]:
        for s in self.stages:
            if s.stage == stage:
                return s
        return None

    def to_dict(self) -> dict:
        return {
            "target": self.target,
            "stages": [s.to_dict() for s in self.stages],
            "status_map": self.status_map(),
            "judgment": self.judgment,
            "confidence": self.confidence,
            "evidence_gap": self.evidence_gap,
            "notes": list(self.notes),
        }


def _stage(name: str, status: str, detail: str = "", **data) -> StageEvidence:
    if status not in STATUSES:
        raise ValueError(f"bad status {status}")
    return StageEvidence(stage=name, status=status, detail=detail, data=dict(data))


def norm_path(url: str) -> str:
    u = (url or "").strip()
    if not u:
        return ""
    if "://" in u:
        p = urlparse(u)
        path = p.path or "/"
    else:
        path = u
    path = path.split("#", 1)[0].split("?", 1)[0]
    return path.rstrip("/") or "/"


def classify_redirect(hops: list[dict[str, Any]]) -> tuple[str, str, dict]:
    """Return (kind, detail, data). kind: none|normal|chain|loop|abnormal|unavailable."""
    if not hops:
        return "unavailable", "No redirect hop data", {}
    codes = [int(h.get("status") or 0) for h in hops]
    urls = [str(h.get("url") or "") for h in hops]
    seen: set[str] = set()
    for u in urls:
        nu = norm_path(u)
        if nu in seen:
            return "loop", "Redirect loop detected", {"hops": hops, "codes": codes}
        seen.add(nu)
    redir_hops = [h for h in hops if int(h.get("status") or 0) in (301, 302, 303, 307, 308)]
    if not redir_hops:
        return "none", "No redirect", {"hops": hops}
    if len(redir_hops) >= 3:
        return "chain", f"Redirect chain length {len(redir_hops)}", {"hops": hops, "length": len(redir_hops)}
    final = hops[-1] if hops else {}
    final_status = int(final.get("status") or 0)
    if final_status >= 400:
        return "abnormal", f"Redirect ends at HTTP {final_status}", {"hops": hops}
    return "normal", "Single/normal redirect", {"hops": hops, "length": len(redir_hops)}


def build_chain_from_probe(
    target: str,
    *,
    probe: Optional[dict[str, Any]] = None,
    page_canonical: str = "",
    page_hreflang: Optional[dict] = None,
    page_type: str = "other",
    page_lang: str = "",
    sitemap_urls: Optional[set[str]] = None,
    sitemap_checked: bool = False,
    local_slug_known: Optional[bool] = None,
    link_sources: Optional[list[str]] = None,
    lifecycle_hints: Optional[list[str]] = None,
) -> UrlEvidenceChain:
    """Build a full evidence chain for one target URL/slug.

    ``probe`` optional shape:
      {ok, error, hops:[{url,status}], final_url, final_status}
    """
    chain = UrlEvidenceChain(target=target)
    page_hreflang = page_hreflang or {}
    lifecycle_hints = list(lifecycle_hints or [])

    if target and str(target).strip():
        chain.stages.append(_stage("url", "confirmed", "Target URL/slug identified", raw=target))
    else:
        chain.stages.append(_stage("url", "unconfirmed", "Empty target"))
        chain.judgment = "insufficient_evidence"
        chain.evidence_gap = "No target URL to evaluate."
        return chain

    redir_kind = "unavailable"
    final_status: Optional[int] = None
    final_url = ""

    if probe is None:
        chain.stages.append(_stage("http_response", "unavailable", "HTTP not probed (offline or disabled)"))
        chain.stages.append(_stage("redirect", "unavailable", "No HTTP hop data"))
        chain.stages.append(_stage("final_url", "unavailable", "No final URL from HTTP"))
    else:
        err = probe.get("error")
        hops = list(probe.get("hops") or [])
        final_status = probe.get("final_status")
        if final_status is not None:
            final_status = int(final_status)
        final_url = str(probe.get("final_url") or "")
        if err and not hops:
            chain.stages.append(_stage("http_response", "unavailable", f"Probe failed: {err}", error=err))
            chain.stages.append(_stage("redirect", "unavailable", "No hops after probe failure"))
            chain.stages.append(_stage("final_url", "unavailable", "No final URL"))
        else:
            chain.stages.append(
                _stage(
                    "http_response",
                    "confirmed",
                    f"HTTP final status {final_status}",
                    final_status=final_status,
                    hops=len(hops),
                )
            )
            redir_kind, redir_detail, redir_data = classify_redirect(hops)
            if redir_kind == "none":
                chain.stages.append(_stage("redirect", "not_applicable", redir_detail, **redir_data))
            elif redir_kind == "unavailable":
                chain.stages.append(_stage("redirect", "unavailable", redir_detail, **redir_data))
            else:
                chain.stages.append(
                    _stage("redirect", "confirmed", f"{redir_kind}: {redir_detail}", kind=redir_kind, **redir_data)
                )
            if final_url:
                chain.stages.append(
                    _stage("final_url", "confirmed", final_url, final_url=final_url, final_status=final_status)
                )
            else:
                chain.stages.append(_stage("final_url", "unconfirmed", "Missing final URL in probe"))

    if page_canonical:
        same = norm_path(page_canonical) == norm_path(final_url or target)
        chain.stages.append(
            _stage(
                "canonical",
                "confirmed",
                "Canonical present on page",
                canonical=page_canonical,
                matches_final_or_target=same,
                page_type=page_type,
                page_lang=page_lang,
            )
        )
    else:
        chain.stages.append(_stage("canonical", "unconfirmed", "No canonical observed on this page/context"))

    if page_hreflang:
        chain.stages.append(
            _stage("hreflang", "confirmed", f"{len(page_hreflang)} alternate(s) on page", map=dict(page_hreflang))
        )
    else:
        chain.stages.append(_stage("hreflang", "unconfirmed", "No hreflang map on this page/context"))

    in_sitemap: Optional[bool] = None
    if not sitemap_checked:
        chain.stages.append(_stage("sitemap", "unavailable", "Sitemap not checked"))
    else:
        sm = sitemap_urls or set()
        tnorm = norm_path(target)
        in_sitemap = any(
            norm_path(u) == tnorm or tnorm.endswith(norm_path(u)) or norm_path(u).endswith(tnorm) for u in sm
        )
        if in_sitemap:
            chain.stages.append(_stage("sitemap", "confirmed", "URL found in sitemap", in_sitemap=True))
        else:
            chain.stages.append(
                _stage("sitemap", "confirmed", "URL not listed in checked sitemap(s)", in_sitemap=False)
            )

    if local_slug_known is True:
        chain.stages.append(
            _stage(
                "internal_links",
                "confirmed",
                "Target exists in scanned page set",
                sources=(link_sources or [])[:8],
            )
        )
    elif local_slug_known is False:
        chain.stages.append(
            _stage(
                "internal_links",
                "confirmed",
                "Target slug not in scanned page set (file/slug miss) — not the same as HTTP 404",
                sources=(link_sources or [])[:8],
                file_exists=False,
            )
        )
    else:
        chain.stages.append(_stage("internal_links", "unavailable", "Internal-link membership not evaluated"))

    if page_hreflang:
        alts = list(page_hreflang.values())
        chain.stages.append(_stage("alternate_url", "confirmed", f"{len(alts)} alternate href(s)", hrefs=alts[:20]))
    else:
        chain.stages.append(_stage("alternate_url", "not_applicable", "No alternate map to evaluate"))

    if lifecycle_hints:
        chain.stages.append(
            _stage(
                "history_source",
                "unconfirmed",
                "Lifecycle hints present but cause not proven",
                hints=lifecycle_hints,
            )
        )
        chain.evidence_gap = (
            "Suspected historical/migration/old-slug/redirect URL — need HTTP history, "
            "sitemap across time, or server logs before assigning root cause."
        )
    else:
        chain.stages.append(_stage("history_source", "unavailable", "No history/source evidence attached"))

    judgment, confidence, gap = _judge(
        chain, redir_kind, final_status, in_sitemap, local_slug_known, lifecycle_hints
    )
    chain.judgment = judgment
    chain.confidence = confidence
    if gap and not chain.evidence_gap:
        chain.evidence_gap = gap
    return chain


def _judge(
    chain: UrlEvidenceChain,
    redir_kind: str,
    final_status: Optional[int],
    in_sitemap: Optional[bool],
    local_slug_known: Optional[bool],
    lifecycle_hints: list[str],
) -> tuple[str, str, str]:
    http = chain.get("http_response")
    if http and http.status == "confirmed" and final_status in (404, 410):
        return "true_issue", "high", ""
    if redir_kind == "loop":
        return "true_issue", "high", ""
    if redir_kind == "abnormal" and final_status and final_status >= 400:
        return "true_issue", "high", ""
    if redir_kind == "chain":
        return "needs_review", "medium", "Redirect chain observed; confirm intentional."

    can = chain.get("canonical")
    if can and can.status == "confirmed" and can.data.get("matches_final_or_target") is False:
        return (
            "needs_review",
            "medium",
            "Canonical differs from final/target; confirm language/page-type/content relation before fixing.",
        )

    if local_slug_known is False and (http is None or http.status != "confirmed"):
        return (
            "insufficient_evidence",
            "low",
            "Slug missing from scan set but HTTP/redirect/sitemap not confirmed — do not call this a 404.",
        )

    if in_sitemap is False and (http is None or http.status != "confirmed"):
        return (
            "insufficient_evidence",
            "low",
            "Not in sitemap is a fact, not proof of a broken URL.",
        )

    if lifecycle_hints:
        return (
            "insufficient_evidence",
            "low",
            "Lifecycle suspicion without proven cause — Evidence Gap.",
        )

    if http and http.status == "confirmed" and final_status and 200 <= int(final_status) < 400:
        if redir_kind in ("none", "normal", "unavailable"):
            return "likely_exception", "high", ""

    return "needs_review", "low", "Insufficient hard evidence for Critical."


def summarize_chains(chains: list[UrlEvidenceChain]) -> dict[str, Any]:
    from collections import Counter

    judgments = Counter(c.judgment for c in chains)
    http_404 = 0
    for c in chains:
        http = c.get("http_response")
        if http and http.status == "confirmed" and (http.data or {}).get("final_status") in (404, 410):
            http_404 += 1
    return {
        "chain_count": len(chains),
        "judgment_counts": dict(judgments),
        "confirmed_http_404_or_410": http_404,
        "with_evidence_gap": sum(1 for c in chains if c.evidence_gap),
    }
