# -*- coding: utf-8 -*-
"""內連 Link Opportunity Cluster 聚合。

在既有 check_links pairwise Issue 之上做聚合，不改動 LINK_SIM_THRESHOLD / TOP_N / 候選計算。

桶（bucket）：
- template   頁型／百科網格（history↔history、pattern↔pattern…）
- topic      主題群（loan / mortgage / valuation…）
- strong_pair 高相似且非純同頁型網格的強關聯（跨語合併）
- hub        高 degree 吸附頁 → 單一 Hub 機會
- folded     一般／低價值（P3、低相似、弱相關）預設摺疊

每個原始 pairwise 恰好進入一個 opportunity 的 pair_refs（完整可追溯）。
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, asdict, field
from typing import Any, Optional

from .models import Issue

# --- 僅供聚合分桶（不是 check_links 門檻）---
STRONG_SIM = 0.55
HUB_MIN_DEGREE = 40
TEMPLATE_MIN_PAIRS = 5
CATALOG_MESH_MIN_PAIRS = 30
CATALOG_MESH_RATIO = 0.80

PAGE_TYPE_SUFFIXES = (
    "-number-generator",
    "-generator",
    "-statistics",
    "-history",
    "-results",
    "-overview",
    "-howto",
    "-how-to-play",
    "-odds",
    "-prizes",
    "-calculator",
    "-calc",
    "-converter",
    "-checker",
    "-predictor",
)

PAGE_TYPE_LABELS = {
    "-history": "History 頁型 related 網格",
    "-statistics": "Statistics 頁型 related 網格",
    "-results": "Results 頁型 related 網格",
    "-generator": "Generator 頁型 related 網格",
    "-number-generator": "選號工具頁型 related 網格",
    "-calculator": "Calculator 頁型 related 網格",
    "-calc": "Calc 頁型 related 網格",
    "-converter": "Converter 頁型 related 網格",
    "-overview": "Overview 頁型 related 網格",
    "article": "文章／日誌 related 網格",
    "index": "列表／Archive related 網格",
    "catalog_mesh": "百科／詞條 related 網格",
}

# 主題詞彙：slug token 命中即歸入主題
TOPIC_LEXICON: dict[str, tuple[str, ...]] = {
    "loan_mortgage": (
        "loan", "mortgage", "refinance", "refi", "amortization", "apr",
        "student-loan", "car-loan", "personal-loan", "business-loan",
        "heloc", "payday",
    ),
    "lease_vs_buy": ("lease", "rent-vs-buy", "loan-vs-lease", "car-lease"),
    "valuation": (
        "valuation", "ebitda", "exit-value", "dcf", "npv", "irr",
        "business-exit", "enterprise-value",
    ),
    "profit_margin": (
        "margin", "profit", "gross-profit", "net-profit", "markup", "cogs",
    ),
    "tax_payroll": (
        "tax", "payroll", "take-home", "withholding", "vat", "sales-tax",
    ),
    "retirement_fire": (
        "retirement", "fire", "coast-fire", "pension", "401k", "annuity",
    ),
    "insurance": ("insurance", "premium", "coverage", "deductible"),
    "invest_market": (
        "stock", "portfolio", "asset-allocation", "dividend", "bond",
        "volatility", "sharpe", "drawdown", "fibonacci", "pivot",
        "support-resistance",
    ),
    "pricing_cost": (
        "pricing", "cost", "renovation", "freelance-rate", "break-even",
    ),
}

TOPIC_LABELS = {
    "loan_mortgage": "貸款／房貸／Refinance 主題群",
    "lease_vs_buy": "租買／Lease 主題群",
    "valuation": "估值／Exit／EBITDA 主題群",
    "profit_margin": "利潤率／Margin 主題群",
    "tax_payroll": "稅務／薪資 主題群",
    "retirement_fire": "退休／FIRE 主題群",
    "insurance": "保險 主題群",
    "invest_market": "投資／市場工具 主題群",
    "pricing_cost": "定價／成本 主題群",
}


def _leaf(slug: str) -> str:
    return (slug or "").lower().rsplit("/", 1)[-1]


_MONTH_TOKENS = (
    "jan", "january", "feb", "february", "mar", "march", "apr", "april",
    "may", "jun", "june", "jul", "july", "aug", "august", "sep", "sept",
    "september", "oct", "october", "nov", "november", "dec", "december",
)

# Calendar scaffolding tokens only (structural; no site/brand names).
_CALENDAR_NOISE = set(_MONTH_TOKENS) | {
    "page", "p", "archive", "archives", "date", "year", "month", "day",
}


def _path_segments(slug: str) -> list[str]:
    """POSIX-ish path segments from a slug (supports 2026/09 style)."""
    s = (slug or "").lower().replace("\\", "/").strip("/")
    return [p for p in s.split("/") if p]


def _norm_slug_tokens(slug: str) -> list[str]:
    """Split leaf on hyphens/underscores for structural checks."""
    import re as _re
    s = _leaf(slug).replace("_", "-")
    return [t for t in _re.split(r"[-\s]+", s) if t]


def _all_slug_tokens(slug: str) -> list[str]:
    """Tokens across path segments (leaf + parents like 2026/09)."""
    import re as _re
    out: list[str] = []
    for seg in _path_segments(slug):
        s = seg.replace("_", "-")
        out.extend(t for t in _re.split(r"[-\s]+", s) if t)
    return out


def _is_year_token(tok: str) -> bool:
    return tok.isdigit() and len(tok) == 4 and 1900 <= int(tok) <= 2100


def _is_month_token(tok: str) -> bool:
    if tok in _MONTH_TOKENS:
        return True
    if tok.isdigit() and 1 <= int(tok) <= 12:
        return True
    return False


def _is_day_token(tok: str) -> bool:
    return tok.isdigit() and 1 <= int(tok) <= 31


def _is_calendar_noise_token(tok: str) -> bool:
    if tok in _CALENDAR_NOISE:
        return True
    if _is_year_token(tok) or _is_month_token(tok) or _is_day_token(tok):
        return True
    return False


def _non_calendar_tokens(slug: str) -> set[str]:
    return {t for t in _all_slug_tokens(slug) if not _is_calendar_noise_token(t)}


def _token_list_is_archive_index(toks: list[str]) -> bool:
    """Year / year-month / pagination shell from a token list."""
    if len(toks) == 1 and _is_year_token(toks[0]):
        return True
    if len(toks) == 2 and _is_year_token(toks[0]) and _is_month_token(toks[1]):
        return True
    if len(toks) == 2 and toks[0] in ("page", "p") and toks[1].isdigit():
        return True
    return False


def _is_archive_index(slug: str) -> bool:
    """Year or year-month archive hubs (e.g. 2026, 2026_sep, 2026/09, 2024-01)."""
    if _token_list_is_archive_index(_norm_slug_tokens(slug)):
        return True
    segs = _path_segments(slug)
    if len(segs) >= 2:
        parent_toks = _norm_slug_tokens(segs[-2])
        leaf_toks = _norm_slug_tokens(segs[-1])
        if (
            len(parent_toks) == 1
            and _is_year_token(parent_toks[0])
            and len(leaf_toks) == 1
            and _is_month_token(leaf_toks[0])
        ):
            return True
    if _token_list_is_archive_index(_all_slug_tokens(slug)):
        return True
    return False


def _is_dated_article(slug: str) -> bool:
    """Chronological post: YYYY mon DD rest or YYYY-MM-DD rest."""
    toks = _norm_slug_tokens(slug)
    if len(toks) < 3:
        return False
    if not _is_year_token(toks[0]):
        return False
    if not _is_month_token(toks[1]):
        return False
    if _is_day_token(toks[2]):
        return True
    return False


def _is_archive_shell_pair(slug_a: str, slug_b: str) -> bool:
    """True when both sides are date/archive index shells (not topical articles).

    Structural only: year / year-month / pagination hubs.
    Dated articles with non-calendar slug body are NOT shells.
    """
    return _is_archive_index(slug_a) and _is_archive_index(slug_b)


def _overlap_is_calendar_only(slug_a: str, slug_b: str) -> bool:
    """Shared tokens are only year/month/day/pagination noise."""
    overlap = _tokens(slug_a) & _tokens(slug_b)
    if not overlap:
        return False
    return all(_is_calendar_noise_token(t) for t in overlap)


def _group_is_archive_shell_mesh(refs: list) -> bool:
    """True if every pair is archive-index ↔ archive-index (calendar shells)."""
    if not refs:
        return False
    return all(_is_archive_shell_pair(r.slug_a, r.slug_b) for r in refs)


def _is_guide_article(slug: str) -> bool:
    """Structural how-to / guide shells (not tool/form pages)."""
    toks = _norm_slug_tokens(slug)
    if not toks:
        return False
    if toks[0] == "how" and len(toks) >= 2 and toks[1] == "to":
        return True
    if toks[0] in ("guide", "tutorial", "blog", "news", "post", "article"):
        return True
    return False


def page_type(slug: str) -> str:
    """Heuristic page-type from structural slug signals only.

    Order:
    1) date/archive / guide shells -> index|article (never tool suffixes)
    2) intentional tool/form suffixes (endswith clear markers)
    3) calculator token / -calc ending
    4) unit-style X-to-Y only when both sides are short tokens
    5) other

    Not ground truth. No site/brand hardcoding.
    """
    s = _leaf(slug)
    # Prefer full-slug archive check so path forms like 2026/09 classify as index.
    if _is_archive_index(slug) or _is_archive_index(s):
        return "index"
    if _is_dated_article(s) or _is_guide_article(s):
        return "article"

    for suf in sorted(PAGE_TYPE_SUFFIXES, key=len, reverse=True):
        if s.endswith(suf) and len(s) > len(suf):
            return suf

    toks = set(_norm_slug_tokens(s))
    if "calculator" in toks:
        return "-calculator"
    if s.endswith("-calc") or (s.endswith("calc") and len(s) > 4):
        return "-calc"

    import re as _re
    m = _re.search(
        r"(?:^|-)([a-z0-9]{1,6})-to-([a-z0-9]{1,6})(?:-converter)?$",
        s.replace("_", "-"),
    )
    if m:
        return "-converter"

    return "other"


def _tokens(slug: str) -> set[str]:
    s = _leaf(slug).replace("_", "-")
    parts = [p for p in s.split("-") if p and len(p) > 1]
    return set(parts)


def _topics_for_slug(slug: str) -> set[str]:
    leaf = _leaf(slug)
    toks = _tokens(slug)
    hit = set()
    for tid, keys in TOPIC_LEXICON.items():
        for k in keys:
            if "-" in k:
                if k in leaf:
                    hit.add(tid)
                    break
            elif k in toks or k in leaf:
                hit.add(tid)
                break
    return hit


def _shared_topics(a: str, b: str) -> set[str]:
    return _topics_for_slug(a) & _topics_for_slug(b)


@dataclass
class LinkPairRef:
    """一筆原始內連 pairwise（可追溯）。"""

    id: str
    slug_a: str
    slug_b: str
    lang: str
    link_sim: float
    priority: str
    body_lens: list = field(default_factory=list)
    paths: list = field(default_factory=list)
    page_types: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class LinkOpportunity:
    id: str
    title: str
    bucket: str  # template|topic|strong_pair|hub|folded
    folded: bool
    priority: str
    kind: str
    why: str
    fix: str
    slugs: list = field(default_factory=list)
    langs: list = field(default_factory=list)
    pair_count: int = 0
    page_count: int = 0
    lang_count: int = 0
    sim_min: float = 0.0
    sim_max: float = 0.0
    high_value: bool = False
    pair_refs: list = field(default_factory=list)
    evidence: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


def _issue_to_ref(issue: Issue) -> Optional[LinkPairRef]:
    pages = issue.pages or []
    if len(pages) < 2:
        return None
    ev = issue.evidence or {}
    sa, sb = pages[0], pages[1]
    return LinkPairRef(
        id=issue.id,
        slug_a=sa,
        slug_b=sb,
        lang=str(ev.get("lang") or ""),
        link_sim=float(ev.get("link_sim") or 0),
        priority=issue.priority or "P3",
        body_lens=list(ev.get("body_lens") or []),
        paths=list(ev.get("paths") or []),
        page_types=[page_type(sa), page_type(sb)],
    )


def _stats(refs: list[LinkPairRef]) -> dict:
    sims = [r.link_sim for r in refs]
    langs = sorted({r.lang for r in refs if r.lang})
    slugs = sorted({s for r in refs for s in (r.slug_a, r.slug_b)})
    return {
        "pair_count": len(refs),
        "langs": langs,
        "lang_count": len(langs),
        "slugs": slugs,
        "page_count": len(slugs),
        "sim_min": round(min(sims), 4) if sims else 0.0,
        "sim_max": round(max(sims), 4) if sims else 0.0,
        "pair_refs": [r.to_dict() for r in sorted(refs, key=lambda x: (-x.link_sim, x.lang, x.slug_a))],
    }


def _opp_priority(refs: list[LinkPairRef], bucket: str) -> str:
    if not refs:
        return "P3"
    if bucket == "folded":
        return "P3"
    if bucket == "hub":
        return "P2"
    if any(r.priority == "P2" for r in refs) or any(r.link_sim >= 0.28 for r in refs):
        if bucket in ("template", "topic", "strong_pair") and (
            len(refs) >= 20 or any(r.link_sim >= STRONG_SIM for r in refs)
        ):
            return "P1" if bucket != "strong_pair" else "P1"
        return "P2"
    return "P3"


def build_link_opportunities(link_issues: list[Issue]) -> list[LinkOpportunity]:
    """從 check_links 產出的 pairwise Issue 聚合為 Link Opportunity。"""
    refs: list[LinkPairRef] = []
    for it in link_issues:
        if it.category != "links":
            continue
        r = _issue_to_ref(it)
        if r:
            refs.append(r)

    if not refs:
        return []

    assigned: set[str] = set()  # LinkPairRef.id
    opps: list[LinkOpportunity] = []
    oid = 0

    def next_id(prefix: str) -> str:
        nonlocal oid
        oid += 1
        return "%s-%03d" % (prefix, oid)

    by_id = {r.id: r for r in refs}

    def claim(ref_list: list[LinkPairRef]) -> list[LinkPairRef]:
        claimed = []
        for r in ref_list:
            if r.id in assigned:
                continue
            assigned.add(r.id)
            claimed.append(r)
        return claimed

    remaining = lambda: [r for r in refs if r.id not in assigned]

    # ---------- 1) Strong pairs (multilang collapse) ----------
    # key = frozenset({slug_a, slug_b})
    strong_groups: dict[frozenset, list[LinkPairRef]] = defaultdict(list)
    for r in refs:
        ta, tb = r.page_types[0], r.page_types[1]
        same_type = ta == tb and ta != "other"
        if same_type:
            continue
        if r.link_sim < STRONG_SIM:
            continue
        # Archive/date URL shells (year ↔ year-month etc.) are not high-value pairs.
        if _is_archive_shell_pair(r.slug_a, r.slug_b):
            continue
        # semantic: token overlap OR shared topic OR mirror-ish shared stem
        overlap = _tokens(r.slug_a) & _tokens(r.slug_b)
        topics = _shared_topics(r.slug_a, r.slug_b)
        # Calendar-only overlap without topical lexicon → not strong_pair
        if not topics and overlap and _overlap_is_calendar_only(r.slug_a, r.slug_b):
            continue
        # other↔other（百科網格）必須有 token／主題線索才當強關聯，
        # 否則留给 catalog mesh，避免 patterns／glossary 炸成數百張強關聯卡。
        if not overlap and not topics:
            if ta == "other" and tb == "other":
                continue
            # 跨頁型：極高相似仍可當強關聯（如 valuation 對）
            if r.link_sim < 0.70:
                continue
        key = frozenset([r.slug_a, r.slug_b])
        strong_groups[key].append(r)

    for key, group in sorted(strong_groups.items(), key=lambda kv: -max(x.link_sim for x in kv[1])):
        claimed = claim(group)
        if not claimed:
            continue
        slugs = sorted(key)
        st = _stats(claimed)
        topics = sorted(_shared_topics(slugs[0], slugs[1]))
        overlap = sorted(_tokens(slugs[0]) & _tokens(slugs[1]))
        title = "強關聯內連｜%s ↔ %s｜%s" % (
            slugs[0],
            slugs[1],
            "多語（%d）" % st["lang_count"] if st["lang_count"] > 1 else (st["langs"][0] if st["langs"] else "?"),
        )
        opps.append(
            LinkOpportunity(
                id=next_id("linko"),
                title=title,
                bucket="strong_pair",
                folded=False,
                priority=_opp_priority(claimed, "strong_pair"),
                kind="strong_pair",
                why=(
                    "內容高相似（sim 最高 %.3f）且非同頁型網格；"
                    "語意線索：overlap=%s topics=%s。跨 %d 語，應視為單一互連機會。"
                    % (st["sim_max"], ",".join(overlap) or "—", ",".join(topics) or "—", st["lang_count"])
                ),
                fix="在雙方相關區塊／文末加入彼此自然錨點連結；多語言版本一次套用同一互連策略。",
                slugs=st["slugs"],
                langs=st["langs"],
                pair_count=st["pair_count"],
                page_count=st["page_count"],
                lang_count=st["lang_count"],
                sim_min=st["sim_min"],
                sim_max=st["sim_max"],
                high_value=True,
                pair_refs=st["pair_refs"],
                evidence={"overlap": overlap, "topics": topics},
            )
        )

    # ---------- 2) Page-type template meshes (same suffix) ----------
    by_type: dict[str, list[LinkPairRef]] = defaultdict(list)
    for r in remaining():
        ta, tb = r.page_types[0], r.page_types[1]
        if ta == tb and ta != "other":
            by_type[ta].append(r)

    for ptype, group in sorted(by_type.items(), key=lambda kv: -len(kv[1])):
        if len(group) < TEMPLATE_MIN_PAIRS:
            continue
        claimed = claim(group)
        if not claimed:
            continue
        # Archive/date index shells → folded low-value (not high_value template mesh)
        if ptype == "index" or _group_is_archive_shell_mesh(claimed):
            st = _stats(claimed)
            title = "日期／Archive 索引內連（已降級摺疊）｜%d 對｜%d 語｜%d 頁" % (
                st["pair_count"],
                st["lang_count"],
                st["page_count"],
            )
            opps.append(
                LinkOpportunity(
                    id=next_id("linko"),
                    title=title,
                    bucket="folded",
                    folded=True,
                    priority="P3",
                    kind="archive_date_demoted",
                    why=(
                        "雙方皆為年份／年月／分頁等 Archive 索引殼層（結構啟發式），"
                        "不是主題文章互推機會；已自 high_value／strong_pair／頁型網格降級。"
                        "共 %d 對。" % st["pair_count"]
                    ),
                    fix="通常不必為年月 Archive 互加 related；優先處理主題文章或常青樞紐頁。",
                    slugs=st["slugs"],
                    langs=st["langs"],
                    pair_count=st["pair_count"],
                    page_count=st["page_count"],
                    lang_count=st["lang_count"],
                    sim_min=st["sim_min"],
                    sim_max=st["sim_max"],
                    high_value=False,
                    pair_refs=st["pair_refs"],
                    evidence={
                        "page_type": ptype,
                        "archive_date_demoted": True,
                        "demotion_reason": "archive_index_shell_pair",
                    },
                )
            )
            continue
        st = _stats(claimed)
        label = PAGE_TYPE_LABELS.get(ptype, "頁型 %s related 網格" % ptype)
        title = "%s｜%d 對｜%d 語｜%d 頁" % (label, st["pair_count"], st["lang_count"], st["page_count"])
        opps.append(
            LinkOpportunity(
                id=next_id("linko"),
                title=title,
                bucket="template",
                folded=False,
                priority=_opp_priority(claimed, "template"),
                kind="page_type_mesh",
                why=(
                    "大量「同頁型 ↔ 同頁型」尚未互連建議（%d 對）。"
                    "這是頁型 related 模組問題，不應拆成 %d 張獨立工單。"
                    % (st["pair_count"], st["pair_count"])
                ),
                fix=(
                    "在「%s」頁型母版加入 related／同類型頁推薦（可依遊戲／主題過濾），"
                    "一次覆蓋多語與多實體。" % ptype
                ),
                slugs=st["slugs"],
                langs=st["langs"],
                pair_count=st["pair_count"],
                page_count=st["page_count"],
                lang_count=st["lang_count"],
                sim_min=st["sim_min"],
                sim_max=st["sim_max"],
                high_value=True,
                pair_refs=st["pair_refs"],
                evidence={"page_type": ptype},
            )
        )

    # ---------- 3) Catalog mesh (pattern/glossary other↔other bulk) ----------
    # 僅當「全站」原始配對高度是 other↔other（百科／詞條站）才啟用，避免 tools 被誤收。
    other_other_all = [
        r for r in refs
        if r.page_types[0] == "other" and r.page_types[1] == "other"
    ]
    catalog_site = (
        len(refs) > 0
        and len(other_other_all) >= CATALOG_MESH_MIN_PAIRS
        and (len(other_other_all) / len(refs)) >= CATALOG_MESH_RATIO
    )
    if catalog_site:
        other_other = [
            r for r in remaining()
            if r.page_types[0] == "other" and r.page_types[1] == "other"
        ]
        if len(other_other) >= CATALOG_MESH_MIN_PAIRS:
            claimed = claim(other_other)
            if len(claimed) >= CATALOG_MESH_MIN_PAIRS:
                st = _stats(claimed)
                title = "%s｜%d 對｜%d 語｜%d 頁" % (
                    PAGE_TYPE_LABELS["catalog_mesh"],
                    st["pair_count"],
                    st["lang_count"],
                    st["page_count"],
                )
                opps.append(
                    LinkOpportunity(
                        id=next_id("linko"),
                        title=title,
                        bucket="template",
                        folded=False,
                        priority=_opp_priority(claimed, "template"),
                        kind="catalog_mesh",
                        why=(
                            "站內百科／詞條兩兩相似且尚未互連的建議高度網格化（%d 對）。"
                            "屬「Related 模組」模板機會，而非數百張獨立互連工單。"
                            % st["pair_count"]
                        ),
                        fix="在百科／詞條母版加入 Related patterns／Related terms（含多空對照、同主題），一次覆蓋多語。",
                        slugs=st["slugs"],
                        langs=st["langs"],
                        pair_count=st["pair_count"],
                        page_count=st["page_count"],
                        lang_count=st["lang_count"],
                        sim_min=st["sim_min"],
                        sim_max=st["sim_max"],
                        high_value=True,
                        pair_refs=st["pair_refs"],
                        evidence={"page_type": "catalog_mesh"},
                    )
                )

    # ---------- 4) Topic groups ----------
    topic_buckets: dict[str, list[LinkPairRef]] = defaultdict(list)
    for r in remaining():
        shared = _shared_topics(r.slug_a, r.slug_b)
        if not shared:
            # single-side topic + other in same topic family via either slug
            ta = _topics_for_slug(r.slug_a)
            tb = _topics_for_slug(r.slug_b)
            shared = ta & tb
            if not shared and (ta or tb):
                # if both have topics but different, skip; if one has topic and sim decent, skip for hub/fold
                continue
        if not shared:
            continue
        # pick primary topic
        tid = sorted(shared)[0]
        topic_buckets[tid].append(r)

    for tid, group in sorted(topic_buckets.items(), key=lambda kv: -len(kv[1])):
        if len(group) < 3:
            continue
        claimed = claim(group)
        if len(claimed) < 3:
            # unclaim? already claimed — if <3 leave them claimed in small topic anyway if >=2
            if len(claimed) < 2:
                continue
        st = _stats(claimed)
        label = TOPIC_LABELS.get(tid, "主題群 %s" % tid)
        title = "%s｜%d 對｜%d 語｜%d 頁" % (label, st["pair_count"], st["lang_count"], st["page_count"])
        opps.append(
            LinkOpportunity(
                id=next_id("linko"),
                title=title,
                bucket="topic",
                folded=False,
                priority=_opp_priority(claimed, "topic"),
                kind="topic_group",
                why=(
                    "多個頁面共享主題線索「%s」，形成尚未互連的主題團（%d 對）。"
                    "建議以主題群 complementary links 一次處理。"
                    % (tid, st["pair_count"])
                ),
                fix="為此主題群設計互連規則（核心頁 ↔ 衛星頁），母版／CMS 一次套用至各語言。",
                slugs=st["slugs"],
                langs=st["langs"],
                pair_count=st["pair_count"],
                page_count=st["page_count"],
                lang_count=st["lang_count"],
                sim_min=st["sim_min"],
                sim_max=st["sim_max"],
                high_value=True,
                pair_refs=st["pair_refs"],
                evidence={"topic_id": tid},
            )
        )

    # ---------- 5) Hubs among remaining ----------
    degree: Counter = Counter()
    rem = remaining()
    for r in rem:
        degree[r.slug_a] += 1
        degree[r.slug_b] += 1

    global_degree: Counter = Counter()
    for r in refs:
        global_degree[r.slug_a] += 1
        global_degree[r.slug_b] += 1
    # Hub：以全局 degree 為準，但只取仍有剩餘配對可吸收者；最多 20 個，避免工單爆炸
    hub_candidates = [s for s, d in global_degree.most_common() if d >= HUB_MIN_DEGREE]
    hub_slugs = []
    for s in hub_candidates:
        if any((r.slug_a == s or r.slug_b == s) for r in remaining()):
            hub_slugs.append(s)
        if len(hub_slugs) >= 20:
            break

    for hub in hub_slugs:
        group = [r for r in remaining() if r.slug_a == hub or r.slug_b == hub]
        if len(group) < 5:
            continue
        claimed = claim(group)
        if not claimed:
            continue
        st = _stats(claimed)
        neighbors = [s for s in st["slugs"] if s != hub]
        title = "Hub 內連吸附｜%s｜degree≈%d｜本卡 %d 對" % (
            hub,
            global_degree[hub],
            st["pair_count"],
        )
        opps.append(
            LinkOpportunity(
                id=next_id("linko"),
                title=title,
                bucket="hub",
                folded=False,
                priority=_opp_priority(claimed, "hub"),
                kind="hub",
                why=(
                    "「%s」在內連建議中出現極高次數（全局 degree %d）。"
                    "不應拆成大量獨立互連工單；應檢視該頁 related 演算法／推薦寬度。"
                    % (hub, global_degree[hub])
                ),
                fix=(
                    "為 Hub 頁設計受控的 related 列表（上限、主題過濾），"
                    "避免無差別連到所有略相似頁；衛星頁可單向連回 Hub。"
                ),
                slugs=st["slugs"],
                langs=st["langs"],
                pair_count=st["pair_count"],
                page_count=st["page_count"],
                lang_count=st["lang_count"],
                sim_min=st["sim_min"],
                sim_max=st["sim_max"],
                high_value=True,
                pair_refs=st["pair_refs"],
                evidence={
                    "hub": hub,
                    "global_degree": global_degree[hub],
                    "neighbor_count": len(neighbors),
                    "neighbors_sample": neighbors[:30],
                },
            )
        )

    # ---------- 6) Fold remaining ----------
    left = remaining()
    if left:
        # optionally split P2 leftover as one "general" folded mesh vs all folded
        claimed = claim(left)
        st = _stats(claimed)
        title = "一般／低價值內連建議（已摺疊）｜%d 對｜%d 語" % (st["pair_count"], st["lang_count"])
        opps.append(
            LinkOpportunity(
                id=next_id("linko"),
                title=title,
                bucket="folded",
                folded=True,
                priority="P3",
                kind="low_value",
                why=(
                    "剩餘建議多為較低相似、弱相關或未進入主題／模板／Hub 的配對（%d 對）。"
                    "預設摺疊；原始 pairwise 仍完整可查。"
                    % st["pair_count"]
                ),
                fix="通常無需逐條處理；若要優化，優先看強關聯與主題群／頁型模板卡。",
                slugs=st["slugs"],
                langs=st["langs"],
                pair_count=st["pair_count"],
                page_count=st["page_count"],
                lang_count=st["lang_count"],
                sim_min=st["sim_min"],
                sim_max=st["sim_max"],
                high_value=False,
                pair_refs=st["pair_refs"],
                evidence={},
            )
        )

    # sort: high_value first, then bucket order, then priority
    bucket_order = {"strong_pair": 0, "topic": 1, "template": 2, "hub": 3, "folded": 4}
    pri_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}

    def sk(o: LinkOpportunity):
        return (
            0 if o.high_value and not o.folded else 1,
            bucket_order.get(o.bucket, 9),
            pri_order.get(o.priority, 9),
            -o.pair_count,
            o.title,
        )

    opps.sort(key=sk)

    # safety: every ref assigned
    if len(assigned) != len(refs):
        missing = [r for r in refs if r.id not in assigned]
        if missing:
            claimed = claim(missing)
            st = _stats(claimed)
            opps.append(
                LinkOpportunity(
                    id=next_id("linko"),
                    title="（補遺）未分類內連 pairwise｜%d 對" % st["pair_count"],
                    bucket="folded",
                    folded=True,
                    priority="P3",
                    kind="orphan_catch",
                    why="聚合收尾補進，確保 pairwise 可追溯。",
                    fix="可忽略；若常見請回報聚合邏輯缺口。",
                    slugs=st["slugs"],
                    langs=st["langs"],
                    pair_count=st["pair_count"],
                    page_count=st["page_count"],
                    lang_count=st["lang_count"],
                    sim_min=st["sim_min"],
                    sim_max=st["sim_max"],
                    high_value=False,
                    pair_refs=st["pair_refs"],
                    evidence={"orphan": True},
                )
            )
            opps.sort(key=sk)

    return opps


def opportunities_to_issues(opps: list[LinkOpportunity]) -> list[Issue]:
    issues: list[Issue] = []
    for o in opps:
        issues.append(
            Issue(
                id=o.id,
                category="links",
                problem=o.title,
                cause=o.why,
                fix=o.fix,
                priority=o.priority,
                evidence={
                    "link_opportunity": True,
                    "folded": o.folded,
                    "bucket": o.bucket,
                    "kind": o.kind,
                    "high_value": o.high_value,
                    "slugs": o.slugs,
                    "langs": o.langs,
                    "pair_count": o.pair_count,
                    "page_count": o.page_count,
                    "lang_count": o.lang_count,
                    "sim_min": o.sim_min,
                    "sim_max": o.sim_max,
                    "pair_refs": o.pair_refs,
                    **(o.evidence or {}),
                },
                pages=list(o.slugs),
            )
        )
    return issues


def opportunity_summary(opps: list[LinkOpportunity]) -> dict[str, Any]:
    bucket_counts = Counter(o.bucket for o in opps)
    high = [o for o in opps if o.high_value and not o.folded]
    folded = [o for o in opps if o.folded]
    archive_demoted = [
        o for o in opps
        if o.kind == "archive_date_demoted"
        or (o.evidence or {}).get("archive_date_demoted")
    ]
    pair_total = sum(o.pair_count for o in opps)
    return {
        "opportunity_count": len(opps),
        "high_value_count": len(high),
        "folded_count": len(folded),
        "archive_date_demoted_count": len(archive_demoted),
        "archive_date_demoted_pairs": sum(o.pair_count for o in archive_demoted),
        "bucket_counts": {
            "template": bucket_counts.get("template", 0),
            "topic": bucket_counts.get("topic", 0),
            "strong_pair": bucket_counts.get("strong_pair", 0),
            "hub": bucket_counts.get("hub", 0),
            "folded": bucket_counts.get("folded", 0),
        },
        "pairwise_in_opportunities": pair_total,
        "high_value_titles": [o.title for o in high],
        "top_titles": [o.title for o in opps[:12]],
    }
