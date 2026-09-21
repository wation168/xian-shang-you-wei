# -*- coding: utf-8 -*-
"""Page / Issue 資料結構。"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class Page:
    """單一靜態 HTML 頁面的擷取結果。"""

    path: str                    # 相對 root 的路徑（POSIX 風格）
    slug: str                    # 去掉語言前綴與 .html 的 slug
    lang: str                    # html[lang] 或從路徑推得
    title: str = ""
    meta_description: str = ""
    h1: str = ""
    h1_count: int = 0
    canonical: str = ""
    hreflang: dict = field(default_factory=dict)  # hreflang_code -> href
    body_text: str = ""
    body_len: int = 0
    internal_links: list = field(default_factory=list)  # 站內相對/絕對連結的 slug 或路徑
    filename: str = ""
    abs_path: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Issue:
    """一筆 SEO 診斷發現。"""

    id: str
    category: str                # similarity|links|meta|i18n|thin
    problem: str
    cause: str
    fix: str
    priority: str                # P0|P1|P2|P3
    evidence: dict = field(default_factory=dict)
    pages: list = field(default_factory=list)  # 相關 slug 列表

    def to_dict(self) -> dict:
        return asdict(self)


# 相似度分類標籤（繁中顯示用）
SIM_CATEGORY_LABELS = {
    "template_shell": "真套殼（模板幾乎未填變數）",
    "near_duplicate": "近重複／缺乏獨特性",
    "shared_template_ok": "合理共用模板（變數填充有效）",
    "same_game_family": "同遊戲家族子頁",
}

PRIORITY_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
