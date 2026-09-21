# -*- coding: utf-8 -*-
"""相似內容 Cluster 聚合。

在既有 pairwise（SimPair）之上做聚合，不改動 raw/norm 門檻與分類規則。

聚合規則：
1. 同一 {slug_a, slug_b} 跨語言 → 一個 slug-pair 視圖
2. shell / near_duplicate 邊做連通分量 → 模板影響頁集合
3. 連通分量若成員共享同一頁型後綴（如 -history）→ 頁型模板 cluster
4. shared_template_ok / same_game_family / 鏡像對 → folded（預設摺疊）
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, asdict, field
from typing import Optional

from .models import Issue
from .normalize import GAME_PAGE_SUFFIXES
from .similarity import SimPair, fix_suggestion

# 頁型後綴（用於「History 模板」這類標籤；取最長匹配）
PAGE_TYPE_SUFFIXES = tuple(
    sorted(
        (
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
        ),
        key=len,
        reverse=True,
    )
)

PAGE_TYPE_LABELS = {
    "-history": "History 模板",
    "-statistics": "Statistics 模板",
    "-results": "Results 模板",
    "-overview": "Overview 模板",
    "-number-generator": "選號工具模板",
    "-generator": "Generator 模板",
    "-odds": "Odds 模板",
    "-prizes": "Prizes 模板",
    "-howto": "Howto 模板",
    "-how-to-play": "How-to-play 模板",
}

MIRROR_MARKERS = (
    ("bullish", "bearish"),
    ("bearish", "bullish"),
    ("rising", "falling"),
    ("falling", "rising"),
    ("bull", "bear"),
    ("bear", "bull"),
    ("up", "down"),
    ("down", "up"),
)


def _page_type_suffix(slug: str) -> str:
    s = slug.lower().rsplit("/", 1)[-1]
    for suf in PAGE_TYPE_SUFFIXES:
        if s.endswith(suf) and len(s) > len(suf):
            return suf
    return ""


def _is_mirror_pair(slug_a: str, slug_b: str) -> bool:
    """多空／升降等鏡像命名（不保證內容，僅作呈現分桶輔助）。"""
    a = slug_a.lower().rsplit("/", 1)[-1]
    b = slug_b.lower().rsplit("/", 1)[-1]
    for x, y in MIRROR_MARKERS:
        if x in a and y in b:
            # 去掉標記後主幹近似
            aa = a.replace(x, "").replace("--", "-").strip("-")
            bb = b.replace(y, "").replace("--", "-").strip("-")
            if aa == bb or aa.replace("-", "") == bb.replace("-", ""):
                return True
            # abandoned-baby-bullish / abandoned-baby-bearish
            if a.replace(x, "X") == b.replace(y, "X"):
                return True
        if y in a and x in b:
            aa = a.replace(y, "").replace("--", "-").strip("-")
            bb = b.replace(x, "").replace("--", "-").strip("-")
            if aa == bb or a.replace(y, "X") == b.replace(x, "X"):
                return True
    return False


@dataclass
class SimCluster:
    """一個可呈現的相似內容集群。"""

    id: str
    title: str
    bucket: str  # actionable_template | ok_shared | mirror_pair | same_family
    folded: bool
    priority: str
    kind: str  # page_type_template | content_template | slug_pair_ok | slug_pair_family | slug_pair_mirror
    slugs: list = field(default_factory=list)
    langs: list = field(default_factory=list)
    pair_count: int = 0
    page_count: int = 0
    lang_count: int = 0
    classifications: dict = field(default_factory=dict)
    raw_min: float = 0.0
    raw_max: float = 0.0
    norm_min: float = 0.0
    norm_max: float = 0.0
    page_type_suffix: str = ""
    why: str = ""
    fix: str = ""
    pair_refs: list = field(default_factory=list)  # [{slug_a,slug_b,lang,raw,norm,class,pri}]

    def to_dict(self) -> dict:
        return asdict(self)


def _uf_find(parent: dict, x: str) -> str:
    parent.setdefault(x, x)
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def _uf_union(parent: dict, a: str, b: str) -> None:
    ra, rb = _uf_find(parent, a), _uf_find(parent, b)
    if ra != rb:
        parent[rb] = ra


def _pair_ref(p: SimPair) -> dict:
    return {
        "slug_a": p.slug_a,
        "slug_b": p.slug_b,
        "lang": p.lang,
        "raw_sim": p.raw_sim,
        "norm_sim": p.norm_sim,
        "drop": p.drop,
        "classification": p.classification,
        "priority": p.priority,
        "same_game_family": p.is_same_game_family,
    }


def _pairwise_stats(plist: list[SimPair]) -> dict:
    raws = [p.raw_sim for p in plist]
    norms = [p.norm_sim for p in plist]
    return {
        "pair_count": len(plist),
        "langs": sorted({p.lang for p in plist}),
        "classifications": dict(Counter(p.classification for p in plist)),
        "raw_min": round(min(raws), 4) if raws else 0.0,
        "raw_max": round(max(raws), 4) if raws else 0.0,
        "norm_min": round(min(norms), 4) if norms else 0.0,
        "norm_max": round(max(norms), 4) if norms else 0.0,
        "pair_refs": [_pair_ref(p) for p in sorted(plist, key=lambda x: (-x.norm_sim, x.lang))],
    }


def _cluster_priority(plist: list[SimPair], page_count: int, lang_count: int) -> str:
    """以集群嚴重度判斷，不以配對數量。"""
    if any(p.priority == "P0" or p.norm_sim >= 0.99 for p in plist):
        return "P0"
    if any(p.classification == "template_shell" for p in plist):
        # 影響面大升 P0，否則 P1
        if page_count >= 8 or lang_count >= 5:
            return "P0"
        return "P1"
    if any(p.classification == "near_duplicate" for p in plist):
        return "P1"
    return "P3"


def _lang_label(langs: list[str]) -> str:
    n = len(langs)
    if n <= 0:
        return "語系不明"
    if n == 1:
        return langs[0]
    if n >= 5:
        return "多語（%d）" % n
    return "多語（%s）" % "/".join(langs)


def build_sim_clusters(pairs: list[SimPair]) -> list[SimCluster]:
    """從 pairwise 產出 cluster 列表（actionable + folded）。"""
    if not pairs:
        return []

    clusters: list[SimCluster] = []
    cid = 0

    def next_id(prefix: str) -> str:
        nonlocal cid
        cid += 1
        return "%s-%03d" % (prefix, cid)

    # --- 1) 跨語 slug-pair 索引 ---
    by_slug_pair: dict[frozenset, list[SimPair]] = defaultdict(list)
    for p in pairs:
        by_slug_pair[frozenset([p.slug_a, p.slug_b])].append(p)

    # --- 2) shell/near 連通分量（排除 same_game_family 分類，避免家族誤併）---
    parent: dict[str, str] = {}
    actionable_edges: list[SimPair] = []
    for p in pairs:
        if p.classification not in ("template_shell", "near_duplicate"):
            continue
        if p.classification == "same_game_family" or p.is_same_game_family:
            continue
        actionable_edges.append(p)
        _uf_union(parent, p.slug_a, p.slug_b)

    comps: dict[str, set[str]] = defaultdict(set)
    for p in actionable_edges:
        comps[_uf_find(parent, p.slug_a)].add(p.slug_a)
        comps[_uf_find(parent, p.slug_a)].add(p.slug_b)

    consumed_slug_pairs: set[frozenset] = set()

    # --- 3) 每個連通分量 → actionable template cluster ---
    for members in sorted(comps.values(), key=lambda s: (-len(s), sorted(s)[0])):
        member_list = sorted(members)
        # 收集分量內所有 shell/near edges
        edge_pairs = [
            p
            for p in actionable_edges
            if p.slug_a in members and p.slug_b in members
        ]
        if not edge_pairs:
            continue

        for p in edge_pairs:
            consumed_slug_pairs.add(frozenset([p.slug_a, p.slug_b]))

        stats = _pairwise_stats(edge_pairs)
        suffixes = [_page_type_suffix(s) for s in member_list]
        nonempty = [s for s in suffixes if s]
        common_suf = ""
        kind = "content_template"
        if nonempty and len(set(nonempty)) == 1 and len(nonempty) >= max(2, int(len(member_list) * 0.8)):
            # 絕大多數成員同後綴 → 頁型模板（避免硬併不相關）
            common_suf = nonempty[0]
            kind = "page_type_template"

        pri = _cluster_priority(edge_pairs, len(member_list), len(stats["langs"]))
        lang_lab = _lang_label(stats["langs"])

        if kind == "page_type_template":
            label = PAGE_TYPE_LABELS.get(common_suf, "頁型模板%s" % common_suf)
            # 「15 個遊戲」：後綴去掉後的 base 數
            bases = []
            for s in member_list:
                leaf = s.rsplit("/", 1)[-1]
                if common_suf and leaf.endswith(common_suf):
                    bases.append(leaf[: -len(common_suf)])
                else:
                    bases.append(leaf)
            entity_n = len(set(bases))
            title = "%s｜%d 個實體｜%s｜%s" % (
                label,
                entity_n,
                lang_lab,
                "高優先" if pri in ("P0", "P1") else "中優先",
            )
            why = (
                "多個不同實體的「%s」子頁在扣掉名稱／數字後仍高度相似（norm 最高 %.3f），"
                "屬同一頁型母版套殼。涉及 %d 個 pairwise（含多語回聲），應以母版視角一次處理，"
                "不要拆成 %d 筆獨立工單。"
                % (common_suf or "子頁", stats["norm_max"], stats["pair_count"], stats["pair_count"])
            )
            fix = (
                "改「%s」頁型母版／生成邏輯：為各實體補不可替換的獨有段落（規則差異、數據解讀、常見問題）。"
                "【勿直接上線未審核數字】"
                % (common_suf or "該")
            )
        else:
            title = "內容模板／百科套殼｜%d 個頁面｜%s｜%s" % (
                len(member_list),
                lang_lab,
                "高優先" if pri in ("P0", "P1") else "中優先",
            )
            # SoftGlow patterns 常見
            if len(member_list) >= 8:
                title = "型態／內容百科模板｜%d 個頁面｜%s｜%s" % (
                    len(member_list),
                    lang_lab,
                    "高優先" if pri in ("P0", "P1") else "中優先",
                )
            why = (
                "以下頁面經 shell／near 邊連成同一團（norm 最高 %.3f），共用高度相似骨架；"
                "多語言會放大 pairwise 數（本集群 %d 對），實際是一個模板問題。"
                % (stats["norm_max"], stats["pair_count"])
            )
            fix = (
                "改共用內容母版：保留可替換欄位，但每頁需有不可替換的獨有解說／情境／差異點。"
                "【勿編造未審核數字】"
            )

        clusters.append(
            SimCluster(
                id=next_id("simc"),
                title=title,
                bucket="actionable_template",
                folded=False,
                priority=pri,
                kind=kind,
                slugs=member_list,
                langs=stats["langs"],
                pair_count=stats["pair_count"],
                page_count=len(member_list),
                lang_count=len(stats["langs"]),
                classifications=stats["classifications"],
                raw_min=stats["raw_min"],
                raw_max=stats["raw_max"],
                norm_min=stats["norm_min"],
                norm_max=stats["norm_max"],
                page_type_suffix=common_suf,
                why=why,
                fix=fix,
                pair_refs=stats["pair_refs"],
            )
        )

    # --- 4) 其餘 slug-pair：ok / family / mirror → folded ---
    for key, plist in sorted(by_slug_pair.items(), key=lambda kv: -len(kv[1])):
        if key in consumed_slug_pairs:
            continue
        slugs = sorted(key)
        stats = _pairwise_stats(plist)
        dominant = Counter(p.classification for p in plist).most_common(1)[0][0]
        is_fam = any(p.is_same_game_family or p.classification == "same_game_family" for p in plist)
        is_mirror = _is_mirror_pair(slugs[0], slugs[1])
        is_ok = dominant == "shared_template_ok" or all(
            p.classification == "shared_template_ok" for p in plist
        )

        # 若還有未消耗的 shell/near 單邊（落單、未進大分量）— 仍 actionable 小 cluster
        if dominant in ("template_shell", "near_duplicate") and not is_fam:
            pri = _cluster_priority(plist, 2, len(stats["langs"]))
            title = "高度相似頁對｜%s ↔ %s｜%s" % (slugs[0], slugs[1], _lang_label(stats["langs"]))
            clusters.append(
                SimCluster(
                    id=next_id("simc"),
                    title=title,
                    bucket="actionable_template",
                    folded=False,
                    priority=pri,
                    kind="slug_pair_shell",
                    slugs=slugs,
                    langs=stats["langs"],
                    pair_count=stats["pair_count"],
                    page_count=2,
                    lang_count=len(stats["langs"]),
                    classifications=stats["classifications"],
                    raw_min=stats["raw_min"],
                    raw_max=stats["raw_max"],
                    norm_min=stats["norm_min"],
                    norm_max=stats["norm_max"],
                    page_type_suffix=_page_type_suffix(slugs[0]),
                    why="此 slug 對在正規化後仍高度相似（norm 最高 %.3f），且未併入更大模板團。"
                    % stats["norm_max"],
                    fix=fix_suggestion(dominant, slugs[0], slugs[1]),
                    pair_refs=stats["pair_refs"],
                )
            )
            continue

        if is_fam:
            bucket, kind, folded = "same_family", "slug_pair_family", True
            title = "同遊戲家族｜%s ↔ %s｜%s" % (slugs[0], slugs[1], _lang_label(stats["langs"]))
            why = "同遊戲不同子頁，相似度偏高通常可接受。"
            fix = fix_suggestion("same_game_family", slugs[0], slugs[1])
        elif is_mirror and (is_ok or dominant in ("shared_template_ok", "near_duplicate", "template_shell")):
            # 鏡像對：若已是 ok 則 folded；若仍 shell 但明顯鏡像命名，仍標 mirror 並 folded 為資訊
            # 若是真正 shell 且非 ok，上面已處理；此處僅 ok 或以 mirror 摺疊的 shared
            if dominant in ("template_shell", "near_duplicate") and not is_ok:
                # 真套殼鏡像仍應 actionable？分析時 harami 是 ok。若 shell 鏡像，給 actionable 小對
                pri = _cluster_priority(plist, 2, len(stats["langs"]))
                clusters.append(
                    SimCluster(
                        id=next_id("simc"),
                        title="鏡像頁高度相似｜%s ↔ %s｜%s"
                        % (slugs[0], slugs[1], _lang_label(stats["langs"])),
                        bucket="actionable_template",
                        folded=False,
                        priority=pri,
                        kind="slug_pair_shell",
                        slugs=slugs,
                        langs=stats["langs"],
                        pair_count=stats["pair_count"],
                        page_count=2,
                        lang_count=len(stats["langs"]),
                        classifications=stats["classifications"],
                        raw_min=stats["raw_min"],
                        raw_max=stats["raw_max"],
                        norm_min=stats["norm_min"],
                        norm_max=stats["norm_max"],
                        why="命名呈鏡像但正規化後仍過像，需確認是否只換多空詞。",
                        fix=fix_suggestion(dominant, slugs[0], slugs[1]),
                        pair_refs=stats["pair_refs"],
                    )
                )
                continue
            bucket, kind, folded = "mirror_pair", "slug_pair_mirror", True
            title = "鏡像頁（可摺疊）｜%s ↔ %s｜%s" % (
                slugs[0],
                slugs[1],
                _lang_label(stats["langs"]),
            )
            why = "多空／升降鏡像對，扣變數後相似度下降或屬合理對照頁。"
            fix = "通常無需大改；若要差異化，可強調多空各自的失效條件與案例。"
        else:
            bucket, kind, folded = "ok_shared", "slug_pair_ok", True
            title = "合理共用模板｜%s ↔ %s｜%s" % (
                slugs[0],
                slugs[1],
                _lang_label(stats["langs"]),
            )
            why = (
                "raw 達標但 norm 落到較安全區間（norm 最高 %.3f），屬變數填充有效的共用模板。"
                % stats["norm_max"]
            )
            fix = fix_suggestion("shared_template_ok", slugs[0], slugs[1])

        clusters.append(
            SimCluster(
                id=next_id("simc"),
                title=title,
                bucket=bucket,
                folded=folded,
                priority="P3",
                kind=kind,
                slugs=slugs,
                langs=stats["langs"],
                pair_count=stats["pair_count"],
                page_count=2,
                lang_count=len(stats["langs"]),
                classifications=stats["classifications"],
                raw_min=stats["raw_min"],
                raw_max=stats["raw_max"],
                norm_min=stats["norm_min"],
                norm_max=stats["norm_max"],
                page_type_suffix=_page_type_suffix(slugs[0]),
                why=why,
                fix=fix,
                pair_refs=stats["pair_refs"],
            )
        )

    # 排序：actionable 先，再 folded
    def sort_key(c: SimCluster):
        fold = 1 if c.folded else 0
        pri = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}.get(c.priority, 9)
        return (fold, pri, -c.page_count, -c.pair_count, c.title)

    clusters.sort(key=sort_key)
    return clusters


def clusters_to_issues(clusters: list[SimCluster]) -> list[Issue]:
    """Cluster → Issue（診斷清單用）。folded 仍產出但標 folded，Dashboard 可摺疊。"""
    issues: list[Issue] = []
    for c in clusters:
        issues.append(
            Issue(
                id=c.id,
                category="similarity",
                problem=c.title,
                cause=c.why,
                fix=c.fix,
                priority=c.priority,
                evidence={
                    "cluster": True,
                    "folded": c.folded,
                    "bucket": c.bucket,
                    "kind": c.kind,
                    "slugs": c.slugs,
                    "langs": c.langs,
                    "pair_count": c.pair_count,
                    "page_count": c.page_count,
                    "lang_count": c.lang_count,
                    "classifications": c.classifications,
                    "raw_min": c.raw_min,
                    "raw_max": c.raw_max,
                    "norm_min": c.norm_min,
                    "norm_max": c.norm_max,
                    "page_type_suffix": c.page_type_suffix,
                    "pair_refs": c.pair_refs,
                },
                pages=list(c.slugs),
            )
        )
    return issues


def cluster_summary(clusters: list[SimCluster]) -> dict:
    actionable = [c for c in clusters if not c.folded]
    folded = [c for c in clusters if c.folded]
    return {
        "cluster_count": len(clusters),
        "actionable_cluster_count": len(actionable),
        "folded_cluster_count": len(folded),
        "bucket_counts": dict(Counter(c.bucket for c in clusters)),
        "actionable_titles": [c.title for c in actionable],
    }
