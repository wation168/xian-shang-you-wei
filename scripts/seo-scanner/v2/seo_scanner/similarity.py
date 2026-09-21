# -*- coding: utf-8 -*-
"""相似度計算與分類。

門檻（最終值，README 同步）：
- RAW_CANDIDATE   = 0.90  raw cosine 進候選
- NORM_SHELL      = 0.97  template_shell
- NORM_NEAR_DUP   = 0.93  near_duplicate
- DROP_OK         = 0.05  raw - norm >= 此值 → shared_template_ok（且非 shell）
- same_game_family 一律標註，優先序降至 P3

分類優先序：same_game_family > template_shell > near_duplicate > shared_template_ok
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, asdict
from typing import Optional

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .models import Page, Issue
from .normalize import normalize_page_body, same_game_family

# --- 門檻最終值 ---
RAW_CANDIDATE = 0.90
NORM_SHELL = 0.97
NORM_NEAR_DUP = 0.93
DROP_OK = 0.05


@dataclass
class SimPair:
    """一組同語言高相似配對的診斷結果。"""

    page_a: str
    page_b: str
    slug_a: str
    slug_b: str
    lang: str
    raw_sim: float
    norm_sim: float
    drop: float
    classification: str
    is_same_game_family: bool
    priority: str

    def to_dict(self) -> dict:
        return asdict(self)


def classify_pair(
    raw_sim: float,
    norm_sim: float,
    is_same_family: bool,
) -> tuple[str, str]:
    """回傳 (classification, priority)。

    前置條件：呼叫端已保證 raw_sim >= RAW_CANDIDATE。
    分類只看家族／norm；drop 僅影響文案（見 problem_cause）。
    """
    if is_same_family:
        return "same_game_family", "P3"

    if norm_sim >= NORM_SHELL:
        return "template_shell", "P0" if norm_sim >= 0.99 else "P1"

    if norm_sim >= NORM_NEAR_DUP:
        return "near_duplicate", "P1"

    # raw 已達標且 norm 落到較安全區間 → 合理變數填充／共用版型
    return "shared_template_ok", "P3"


def fix_suggestion(classification: str, slug_a: str, slug_b: str) -> str:
    """依分類給具體（需人工審核）的修復方向。"""
    if classification == "template_shell":
        return (
            "補「%s」與「%s」各自獨有的玩法／規則／使用情境段落；"
            "改寫共用 FAQ，勿整段複製；檢查導言是否只替換遊戲名。"
            "【需人工審核：勿直接上線獎金／賠率數字】"
        ) % (slug_a, slug_b)

    if classification == "near_duplicate":
        return (
            "為「%s」與「%s」各寫至少一段獨有內容"
            "（開獎機制差異、選號策略、常見錯誤）；共用模板區塊可保留。"
            "【需人工審核數字與對外聲明】"
        ) % (slug_a, slug_b)

    if classification == "same_game_family":
        hints = []
        for leaf in (slug_a.rsplit("/", 1)[-1], slug_b.rsplit("/", 1)[-1]):
            if "history" in leaf:
                hints.append("history 頁應著重開獎紀錄解讀而非複製總覽")
            elif "statistics" in leaf:
                hints.append("statistics 頁應著重頻率／分布分析")
            elif "generator" in leaf:
                hints.append("generator 頁應著重工具用法與限制聲明")
            elif "results" in leaf:
                hints.append("results 頁應著重近期結果與查詢方式")
            elif "overview" in leaf:
                hints.append("overview 可保留總覽，但勿與子頁大段重複")
        extra = "；".join(dict.fromkeys(hints)) if hints else "各子頁聚焦自身意圖"
        return (
            "同遊戲家族子頁，相似度偏高通常可接受。建議：%s。優先序低，可摺疊處理。"
            % extra
        )

    return (
        "raw 高但 norm 明顯下降，屬合理變數填充（遊戲名／數字不同）。"
        "通常無需大改；若想再拉開差異，可補一句該遊戲獨有賣點。【資訊性，非緊急】"
    )


def problem_cause(classification: str, raw_sim: float, norm_sim: float) -> tuple[str, str]:
    labels = {
        "template_shell": (
            "兩頁正規化後仍高度相似，疑似真套殼",
            "正文幾乎只替換遊戲名／數字，結構與句子高度重疊（norm_sim=%.3f）" % norm_sim,
        ),
        "near_duplicate": (
            "兩頁內容缺乏足夠獨特性",
            "正規化後相似度仍高（norm_sim=%.3f），獨有段落不足" % norm_sim,
        ),
        "shared_template_ok": (
            "高 raw 相似但屬合理模板變數填充",
            (
                "raw=%.3f，扣除變數後 norm=%.3f（降幅 %.3f）——較像合理變數填充"
                % (raw_sim, norm_sim, raw_sim - norm_sim)
                if (raw_sim - norm_sim) >= DROP_OK
                else "raw=%.3f 達標，norm=%.3f 已低於套殼／近重複門檻；高 raw  alone 不代表 SEO 風險"
                % (raw_sim, norm_sim)
            ),
        ),
        "same_game_family": (
            "同遊戲家族子頁內容相近",
            "slug 後綴顯示為同一遊戲的 overview/history/results 等子頁；raw=%.3f"
            % raw_sim,
        ),
    }
    return labels.get(
        classification,
        ("內容相似", "raw=%.3f norm=%.3f" % (raw_sim, norm_sim)),
    )


def _tfidf_matrix(texts: list[str]):
    """char_wb 3-5 TF-IDF；空字串用佔位避免崩潰。"""
    safe = [t if t and t.strip() else " " for t in texts]
    vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=1)
    return vec.fit_transform(safe)


def compute_similarity_pairs(pages: list[Page]) -> list[SimPair]:
    """對同語言頁面兩兩計算 raw／norm 相似度，回傳達門檻的配對。"""
    by_lang: dict[str, list[Page]] = defaultdict(list)
    for p in pages:
        if p.body_len < 20:
            continue
        by_lang[p.lang or "unknown"].append(p)

    pairs: list[SimPair] = []

    for lang, group in by_lang.items():
        if len(group) < 2:
            continue

        raw_texts = [p.body_text for p in group]
        norm_texts = [normalize_page_body(p) for p in group]

        raw_mat = _tfidf_matrix(raw_texts)
        norm_mat = _tfidf_matrix(norm_texts)

        raw_sim = cosine_similarity(raw_mat)
        norm_sim = cosine_similarity(norm_mat)

        n = len(group)
        for i in range(n):
            for j in range(i + 1, n):
                r = float(raw_sim[i, j])
                if r < RAW_CANDIDATE:
                    continue
                nv = float(norm_sim[i, j])
                fam = same_game_family(group[i].slug, group[j].slug)
                cls, pri = classify_pair(r, nv, fam)
                pairs.append(
                    SimPair(
                        page_a=group[i].path,
                        page_b=group[j].path,
                        slug_a=group[i].slug,
                        slug_b=group[j].slug,
                        lang=lang,
                        raw_sim=round(r, 4),
                        norm_sim=round(nv, 4),
                        drop=round(r - nv, 4),
                        classification=cls,
                        is_same_game_family=fam,
                        priority=pri,
                    )
                )

    pairs.sort(key=lambda x: (-{"P0": 3, "P1": 2, "P2": 1, "P3": 0}[x.priority], -x.norm_sim))
    return pairs


def pairs_to_issues(pairs: list[SimPair]) -> list[Issue]:
    """把 SimPair 轉成 Issue 列表。"""
    issues: list[Issue] = []
    for idx, pair in enumerate(pairs):
        problem, cause = problem_cause(pair.classification, pair.raw_sim, pair.norm_sim)
        fix = fix_suggestion(pair.classification, pair.slug_a, pair.slug_b)
        category = "similarity"
        # same_game_family / shared_template_ok 仍屬 similarity，但可在 evidence 標 flags
        issues.append(
            Issue(
                id="sim-%04d" % (idx + 1),
                category=category,
                problem=problem,
                cause=cause,
                fix=fix,
                priority=pair.priority,
                evidence={
                    "raw_sim": pair.raw_sim,
                    "norm_sim": pair.norm_sim,
                    "drop": pair.drop,
                    "classification": pair.classification,
                    "lang": pair.lang,
                    "flags": {
                        "same_game_family": pair.is_same_game_family,
                        "template_shell": pair.classification == "template_shell",
                        "shared_template_ok": pair.classification == "shared_template_ok",
                    },
                    "paths": [pair.page_a, pair.page_b],
                },
                pages=[pair.slug_a, pair.slug_b],
            )
        )
    return issues


def shell_or_near_slugs(pairs: list[SimPair]) -> set[tuple[str, str]]:
    """回傳應跳過內部連結建議的 (slug_a, slug_b) 無序對（用 frozenset 存）。"""
    skip: set[tuple[str, str]] = set()
    for p in pairs:
        if p.classification in ("template_shell", "near_duplicate"):
            a, b = sorted([p.slug_a, p.slug_b])
            skip.add((a, b))
    return skip
