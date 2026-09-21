# -*- coding: utf-8 -*-
"""內部連結建議：主題相似但尚未互連；跳過 template_shell / near_duplicate 配對。"""

from __future__ import annotations

from collections import defaultdict

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .models import Page, Issue
from .parse import normalize_link_target, link_ids_equivalent
from .similarity import SimPair, shell_or_near_slugs

LINK_SIM_THRESHOLD = 0.18
TOP_N_PER_PAGE = 5
MIN_BODY_FOR_LINK = 150


def check_links(
    pages: list[Page],
    sim_pairs: list[SimPair] | None = None,
) -> list[Issue]:
    """建議內部互連；排除高相似套殼配對。"""
    skip = shell_or_near_slugs(sim_pairs or [])
    issues: list[Issue] = []
    counter = 0

    by_lang: dict[str, list[Page]] = defaultdict(list)
    for p in pages:
        if p.body_len < MIN_BODY_FOR_LINK:
            continue
        by_lang[p.lang or "unknown"].append(p)

    for lang, group in by_lang.items():
        if len(group) < 2:
            continue

        texts = [p.body_text for p in group]
        vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=1)
        mat = vec.fit_transform(texts)
        sim = cosine_similarity(mat)

        # 每頁已有的出站目標（正規化成與 slug 同一套 id）
        def _outbound_ids(p: Page) -> set[str]:
            ids: set[str] = set()
            for raw in p.internal_links:
                n = normalize_link_target(raw)
                if not n:
                    continue
                ids.add(n)
                ids.add(n.rsplit("/", 1)[-1])
            return ids

        existing = {p.slug: _outbound_ids(p) for p in group}

        def _already_linked(from_slug: str, to_slug: str) -> bool:
            """from 頁是否已連到 to（身分對齊後比對）。"""
            targets = existing.get(from_slug) or set()
            to_n = normalize_link_target(to_slug)
            if not to_n:
                return False
            if to_n in targets or to_n.rsplit("/", 1)[-1] in targets:
                return True
            # 容錯：集合內任一連結與 to 等價
            for t in targets:
                if link_ids_equivalent(t, to_n):
                    return True
            return False

        # 收集候選 (i,j,score)
        candidates: list[tuple[float, int, int]] = []
        n = len(group)
        for i in range(n):
            for j in range(i + 1, n):
                score = float(sim[i, j])
                if score < LINK_SIM_THRESHOLD:
                    continue
                sa, sb = group[i].slug, group[j].slug
                key = tuple(sorted([sa, sb]))
                if key in skip:
                    continue
                # 任一方已連到另一方則略過（修正：先前 leaf 比對寫在錯誤的 if 裡）
                if _already_linked(sa, sb) or _already_linked(sb, sa):
                    continue
                candidates.append((score, i, j))

        candidates.sort(reverse=True)

        # 每頁最多 TOP_N 建議
        per_page_count: dict[str, int] = defaultdict(int)
        seen_pair: set[tuple[str, str]] = set()

        for score, i, j in candidates:
            sa, sb = group[i].slug, group[j].slug
            key = tuple(sorted([sa, sb]))
            if key in seen_pair:
                continue
            if per_page_count[sa] >= TOP_N_PER_PAGE and per_page_count[sb] >= TOP_N_PER_PAGE:
                continue
            if per_page_count[sa] >= TOP_N_PER_PAGE or per_page_count[sb] >= TOP_N_PER_PAGE:
                # 允許另一方還沒滿時仍報一次
                if per_page_count[sa] >= TOP_N_PER_PAGE and per_page_count[sb] >= TOP_N_PER_PAGE:
                    continue

            seen_pair.add(key)
            per_page_count[sa] += 1
            per_page_count[sb] += 1
            counter += 1

            # 優先序：兩邊都有一定內容 + 中高相似 → P2；否則 P3
            pri = "P2" if score >= 0.28 and group[i].body_len >= 300 and group[j].body_len >= 300 else "P3"

            issues.append(Issue(
                id="link-%04d" % counter,
                category="links",
                problem="主題相關但尚未互連",
                cause="同語言內容相似（link_sim=%.3f），且導覽／相關區塊未發現雙向連結"
                    % score,
                fix="在「%s」與「%s」的相關連結／側欄加入彼此連結（錨點用自然描述，勿關鍵字堆砌）。"
                    % (sa, sb),
                priority=pri,
                evidence={
                    "lang": lang,
                    "link_sim": round(score, 4),
                    "body_lens": [group[i].body_len, group[j].body_len],
                    "paths": [group[i].path, group[j].path],
                },
                pages=[sa, sb],
            ))

    return issues
