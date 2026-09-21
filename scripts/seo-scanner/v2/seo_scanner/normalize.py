# -*- coding: utf-8 -*-
"""正文變數正規化：把數字、百分比、日期、遊戲名等「移除」（替成空白），
讓「僅變數不同的套殼」norm 升到極高，而「有獨有段落」的頁面 norm 落在較安全區間。
"""

from __future__ import annotations

import re
from typing import Iterable, Set

from .models import Page

GAME_PAGE_SUFFIXES = (
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
    "-payout",
    "-drawing",
    "-draw",
    "-checker",
    "-predictor",
)

_STOP_TOKENS = {
    "the", "and", "for", "with", "from", "how", "to", "play", "guide",
    "tool", "tools", "lottery", "lotto", "number", "numbers", "generator",
    "history", "results", "statistics", "overview", "odds", "prizes",
    "faq", "tips", "best", "free", "online", "page", "html",
    "zh", "tw", "cn", "en", "de", "fr", "es", "pt", "ko", "id", "ja",
}


def game_family_base(slug: str) -> str | None:
    s = slug.lower().rsplit("/", 1)[-1]
    for suf in sorted(GAME_PAGE_SUFFIXES, key=len, reverse=True):
        if s.endswith(suf) and len(s) > len(suf):
            return s[: -len(suf)]
    return None


def same_game_family(slug_a: str, slug_b: str) -> bool:
    if slug_a == slug_b:
        return False
    ba, bb = game_family_base(slug_a), game_family_base(slug_b)
    if ba and bb and ba == bb:
        return True
    a = slug_a.lower().rsplit("/", 1)[-1]
    b = slug_b.lower().rsplit("/", 1)[-1]
    for base, other in ((a, b), (b, a)):
        for suf in GAME_PAGE_SUFFIXES:
            if other == base + suf:
                return True
    return False


def _tokens_from_text(text: str) -> Set[str]:
    toks = set()
    for m in re.finditer(r"[A-Za-z][A-Za-z0-9'&-]{2,}", text or ""):
        t = m.group(0).lower().strip("-'")
        if t in _STOP_TOKENS or len(t) < 3:
            continue
        toks.add(t)
    for m in re.finditer(r"[\u4e00-\u9fff]{2,12}", text or ""):
        toks.add(m.group(0))
    return toks


def collect_game_tokens(page: Page) -> Set[str]:
    toks: Set[str] = set()
    toks |= _tokens_from_text(page.title)
    toks |= _tokens_from_text(page.h1)
    leaf = page.slug.rsplit("/", 1)[-1]
    for part in re.split(r"[-_/]", leaf):
        part = part.lower().strip()
        if part and part not in _STOP_TOKENS and len(part) >= 3:
            if part.isdigit():
                continue
            if f"-{part}" in GAME_PAGE_SUFFIXES or part in {
                "generator", "statistics", "history", "results",
                "overview", "howto", "odds", "prizes", "number",
            }:
                continue
            toks.add(part)
    base = game_family_base(page.slug)
    if base:
        for part in base.split("-"):
            if part and part not in _STOP_TOKENS and len(part) >= 3:
                toks.add(part)
    return toks


def normalize_body(text: str, extra_tokens: Iterable[str] | None = None) -> str:
    """移除變數後回傳正規化正文（空白合併）。"""
    if not text:
        return ""

    s = text

    s = re.sub(r"\b\d{4}[-/.\u5e74]\d{1,2}[-/.\u6708]\d{1,2}\u65e5?\b", " ", s)
    s = re.sub(r"\b\d{1,2}[-/.]\d{1,2}[-/.]\d{4}\b", " ", s)
    s = re.sub(
        r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2},?\s+\d{4}\b",
        " ",
        s,
        flags=re.I,
    )
    s = re.sub(r"\b(?:19|20)\d{2}\b", " ", s)
    s = re.sub(r"\b\d+(?:[.,]\d+)?\s*%", " ", s)
    s = re.sub(
        r"(?:US\$|USD|EUR|GBP|NT\$|HK\$|￥|\$|€|£|¥)\s*[\d,]+(?:\.\d+)?",
        " ",
        s,
        flags=re.I,
    )
    s = re.sub(
        r"[\d,]+(?:\.\d+)?\s*(?:USD|EUR|GBP|million|billion|萬|億)",
        " ",
        s,
        flags=re.I,
    )
    s = re.sub(r"\b\d{1,2}(?:\s*[-–,]\s*\d{1,2}){2,}\b", " ", s)
    s = re.sub(r"\b\d{1,3}(?:,\d{3})+(?:\.\d+)?\b", " ", s)
    s = re.sub(r"\b\d{4,}(?:\.\d+)?\b", " ", s)
    s = re.sub(r"\b\d+(?:\.\d+)?\b", " ", s)

    tokens = sorted(set(extra_tokens or []), key=len, reverse=True)
    for tok in tokens:
        if len(tok) < 3:
            continue
        if re.search(r"[\u4e00-\u9fff]", tok):
            s = s.replace(tok, " ")
        else:
            s = re.sub(rf"\b{re.escape(tok)}\b", " ", s, flags=re.I)

    # 過長專有英文詞
    s = re.sub(r"\b[A-Z][a-zA-Z]{11,}\b", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def normalize_page_body(page: Page) -> str:
    return normalize_body(page.body_text, collect_game_tokens(page))
