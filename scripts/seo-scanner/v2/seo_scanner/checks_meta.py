# -*- coding: utf-8 -*-
"""title / meta description / H1 / canonical / 薄內容檢查。

Meta／title 品質規則（2026-09 調整）：
- 高優先：缺漏、同語言完全重複
- 品質提醒：title 與 meta 幾乎相同；無意義／極短無實質內容
- 長度僅輔助：不再用 <50 字元對所有語言打 P2；>160 保留低優先「可能截斷」
- CJK 不因字元數較短進入主問題清單
- 薄內容／canonical 邏輯本檔保留原樣（本輪不改其行為）
"""

from __future__ import annotations

import re
from collections import defaultdict
from urllib.parse import urlparse

from .models import Page, Issue

# title 長度：過短僅在「拉丁語系且極短」當輔助；過長保留低優先
TITLE_MIN_LATIN, TITLE_MAX = 15, 65
# meta：不再用統一 META_MIN=50 打 P2；僅保留過長截斷提醒
META_MAX = 160
# 無意義／極短：低於此視為「可能無實質資訊」（各語言通用，遠低於舊的 50）
META_EMPTYISH_MAX = 12
TITLE_EMPTYISH_MAX = 8
THIN_BODY_LEN = 200

# 視為 CJK 語系（不因「短字元數」進主問題）
CJK_LANG_PREFIXES = ("zh", "ja", "ko")

# 無意義佔位（比對時忽略大小寫與空白）
MEANINGLESS_EXACT = {
    "untitled", "no title", "title", "page", "home", "homepage",
    "index", "website", "site", "test", "demo",
    "首頁", "未命名", "無標題", "標題", "页面", "頁面", "网站", "網站",
    "ホーム", "タイトルなし", "제목 없음", "홈",
}

_WS_RE = re.compile(r"\s+")
_ALNUM_RE = re.compile(r"[A-Za-z0-9\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]+")


def _is_cjk_lang(lang: str) -> bool:
    l = (lang or "").lower().replace("_", "-")
    return any(l == p or l.startswith(p + "-") for p in CJK_LANG_PREFIXES)


def _norm_text(s: str) -> str:
    return _WS_RE.sub("", (s or "").strip().lower())


def _is_meaningless(text: str) -> bool:
    """無意義佔位或幾乎無實質 token。"""
    raw = (text or "").strip()
    if not raw:
        return True
    n = _norm_text(raw)
    if n in MEANINGLESS_EXACT:
        return True
    # 去掉標點後若落在黑名單
    compact = re.sub(r"[^\w\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]+", "", n, flags=re.UNICODE)
    if compact in MEANINGLESS_EXACT:
        return True
    tokens = _ALNUM_RE.findall(raw)
    if not tokens:
        return True
    # 單一極短 token（如 "SEO"、"a"）且整體很短
    if len(raw) <= META_EMPTYISH_MAX and len(tokens) <= 1 and len(tokens[0]) <= 4:
        return True
    return False


def _title_meta_nearly_same(title: str, meta: str) -> bool:
    """title 與 meta 幾乎完全相同（品質提醒）。"""
    t, m = (title or "").strip(), (meta or "").strip()
    if not t or not m:
        return False
    nt, nm = _norm_text(t), _norm_text(m)
    if not nt or not nm:
        return False
    if nt == nm:
        return True
    # 一方完全包含另一方，且較短邊至少佔較長邊 85%
    shorter, longer = (nt, nm) if len(nt) <= len(nm) else (nm, nt)
    if shorter in longer and len(shorter) >= 12:
        if len(shorter) / max(len(longer), 1) >= 0.85:
            return True
    return False


def _canonical_points_to_self(page: Page) -> bool:
    """粗判 canonical 是否自我指向（比對 path 尾段或 slug）。"""
    if not page.canonical:
        return False
    href = page.canonical.strip()
    parsed = urlparse(href)
    path = parsed.path or href
    path = path.rstrip("/")
    leaf = path.split("/")[-1]
    if leaf.endswith(".html"):
        leaf = leaf[:-5]
    file_stem = page.filename[:-5] if page.filename.lower().endswith(".html") else page.filename
    slug_leaf = page.slug.rsplit("/", 1)[-1]
    if leaf == file_stem or leaf == slug_leaf or leaf == page.slug.replace("/", "-"):
        return True
    if page.slug and page.slug in path.replace("\\", "/"):
        return True
    return False


def check_meta(pages: list[Page]) -> list[Issue]:
    issues: list[Issue] = []
    counter = 0

    def next_id(prefix: str) -> str:
        nonlocal counter
        counter += 1
        return "%s-%04d" % (prefix, counter)

    for p in pages:
        lang = p.lang or ""
        cjk = _is_cjk_lang(lang)

        # --- title ---
        if not p.title or not p.title.strip():
            issues.append(Issue(
                id=next_id("meta"),
                category="meta",
                problem="缺少 title",
                cause="頁面無 <title> 或內容為空",
                fix="補上具描述性的 title（含主關鍵字與品牌）。",
                priority="P0",
                evidence={"lang": lang, "path": p.path, "kind": "missing_title"},
                pages=[p.slug],
            ))
        elif _is_meaningless(p.title):
            issues.append(Issue(
                id=next_id("meta"),
                category="meta",
                problem="title 無實質資訊",
                cause="title 為佔位字（如 untitled／首頁）或極短且無實質詞",
                fix="改寫成能區分本頁主題的 title。目前：%s" % p.title[:80],
                priority="P1",
                evidence={"lang": lang, "title": p.title, "kind": "meaningless_title"},
                pages=[p.slug],
            ))
        else:
            # 長度僅輔助：不過再用統一短門檻打 CJK；拉丁語系極短才提醒
            if (not cjk) and len(p.title.strip()) < TITLE_MIN_LATIN:
                issues.append(Issue(
                    id=next_id("meta"),
                    category="meta",
                    problem="title 過短（%d 字元）" % len(p.title),
                    cause="拉丁語系 title 過短，SERP 主題信號弱（輔助提醒）",
                    fix="適度擴寫 title；勿堆砌關鍵字。",
                    priority="P3",
                    evidence={"lang": lang, "title": p.title, "len": len(p.title), "kind": "title_short_latin"},
                    pages=[p.slug],
                ))
            elif len(p.title) > TITLE_MAX:
                issues.append(Issue(
                    id=next_id("meta"),
                    category="meta",
                    problem="title 過長（%d 字元）" % len(p.title),
                    cause="SERP 可能被截斷（低優先提醒）",
                    fix="精簡 title 至約 %d 字元內，重要詞靠前。" % TITLE_MAX,
                    priority="P3",
                    evidence={"lang": lang, "title": p.title, "len": len(p.title), "kind": "title_long"},
                    pages=[p.slug],
                ))

        # --- meta description ---
        meta = (p.meta_description or "").strip()
        if not meta:
            issues.append(Issue(
                id=next_id("meta"),
                category="meta",
                problem="缺少 meta description",
                cause="無 name=description 的 meta 標籤",
                fix="補上能區分本頁的描述與行動呼籲。【勿編造未審核數字】",
                priority="P1",
                evidence={"lang": lang, "path": p.path, "kind": "missing_meta"},
                pages=[p.slug],
            ))
        elif _is_meaningless(meta) or len(meta) <= META_EMPTYISH_MAX:
            # 極短且無實質／佔位才當問題；正常的 CJK 30–49 字描述不進這裡
            if _is_meaningless(meta) or (len(meta) <= META_EMPTYISH_MAX and len(_ALNUM_RE.findall(meta)) <= 2):
                issues.append(Issue(
                    id=next_id("meta"),
                    category="meta",
                    problem="meta description 無實質資訊",
                    cause="描述為佔位字或極短且缺少實質內容（非「CJK 字元偏短」）",
                    fix="改寫成說明本頁用途與差異的描述。目前長度=%d" % len(meta),
                    priority="P1",
                    evidence={"lang": lang, "len": len(meta), "sample": meta[:80], "kind": "meaningless_meta"},
                    pages=[p.slug],
                ))
        elif len(meta) > META_MAX:
            issues.append(Issue(
                id=next_id("meta"),
                category="meta",
                problem="meta description 過長（%d 字元）" % len(meta),
                cause="SERP 可能截斷（低優先提醒）",
                fix="精簡至約 %d 字元內，重要句靠前。" % META_MAX,
                priority="P3",
                evidence={"lang": lang, "len": len(meta), "kind": "meta_long"},
                pages=[p.slug],
            ))

        # title ≈ meta（品質提醒，不與缺漏同級）
        if p.title and meta and _title_meta_nearly_same(p.title, meta):
            issues.append(Issue(
                id=next_id("meta"),
                category="meta",
                problem="title 與 meta description 幾乎相同",
                cause="描述未提供比 title 更多的 SERP 資訊",
                fix="讓 meta 補充使用情境、對象或差異點，避免與 title 重複。【勿編造數字】",
                priority="P3",
                evidence={"lang": lang, "kind": "title_meta_same"},
                pages=[p.slug],
            ))

        # H1（保留原行為）
        if p.h1_count == 0:
            issues.append(Issue(
                id=next_id("meta"),
                category="meta",
                problem="缺少 H1",
                cause="頁面沒有 <h1>",
                fix="加一個與主題一致的唯一 H1。",
                priority="P1",
                evidence={"lang": lang, "path": p.path, "kind": "missing_h1"},
                pages=[p.slug],
            ))
        elif p.h1_count > 1:
            issues.append(Issue(
                id=next_id("meta"),
                category="meta",
                problem="多個 H1（%d 個）" % p.h1_count,
                cause="多個 H1 可能稀釋主題信號",
                fix="保留一個主 H1，其餘改為 H2。",
                priority="P2",
                evidence={"lang": lang, "h1_count": p.h1_count, "h1": p.h1, "kind": "multi_h1"},
                pages=[p.slug],
            ))

        # canonical（本輪不改行為）
        if not p.canonical:
            issues.append(Issue(
                id=next_id("meta"),
                category="meta",
                problem="缺少 canonical",
                cause="無 rel=canonical",
                fix="加上指向本頁絕對 URL 的 canonical。",
                priority="P1",
                evidence={"lang": lang, "path": p.path, "kind": "missing_canonical"},
                pages=[p.slug],
            ))
        elif not _canonical_points_to_self(p):
            issues.append(Issue(
                id=next_id("meta"),
                category="meta",
                problem="canonical 可能非自我指向",
                cause="canonical href 與本頁 slug/檔名不一致（需人工確認是否刻意合併）",
                fix="若非刻意 consolidated，改為指向本頁自身 URL。目前 canonical=%s"
                    % p.canonical,
                priority="P2",
                evidence={"lang": lang, "canonical": p.canonical, "slug": p.slug, "kind": "canonical_mismatch"},
                pages=[p.slug],
            ))

        # 薄內容（本輪不改行為）
        if p.body_len < THIN_BODY_LEN:
            issues.append(Issue(
                id=next_id("thin"),
                category="thin",
                problem="正文過短（%d 字元）" % p.body_len,
                cause="擷取正文少於 %d 字元，可能是薄內容或版型未命中" % THIN_BODY_LEN,
                fix="補充實質說明（玩法／用法／注意事項）；若版型特殊請回報以改進擷取。"
                    "【勿貼上未審核的獎金／賠率全文】",
                priority="P1" if p.body_len < 80 else "P2",
                evidence={"lang": lang, "body_len": p.body_len, "path": p.path},
                pages=[p.slug],
            ))

    # --- 同語言完全重複 title / meta（高優先，保留）---
    by_lang_title: dict[str, dict[str, list[Page]]] = defaultdict(lambda: defaultdict(list))
    by_lang_meta: dict[str, dict[str, list[Page]]] = defaultdict(lambda: defaultdict(list))
    for p in pages:
        if p.title and p.title.strip():
            by_lang_title[p.lang][p.title].append(p)
        if p.meta_description and p.meta_description.strip():
            by_lang_meta[p.lang][p.meta_description].append(p)

    for lang, groups in by_lang_title.items():
        for title, group in groups.items():
            if len(group) < 2:
                continue
            slugs = [g.slug for g in group]
            issues.append(Issue(
                id=next_id("meta"),
                category="meta",
                problem="同語言 title 完全重複（%d 頁）" % len(group),
                cause="多頁共用相同 title，SERP 難以區分",
                fix="為各頁改寫差異化 title（含工具／主題名）。涉及頁：%s"
                    % ", ".join(slugs[:8]),
                priority="P1",
                evidence={"lang": lang, "title": title, "count": len(group), "kind": "dup_title"},
                pages=slugs,
            ))

    for lang, groups in by_lang_meta.items():
        for desc, group in groups.items():
            if len(group) < 2:
                continue
            slugs = [g.slug for g in group]
            issues.append(Issue(
                id=next_id("meta"),
                category="meta",
                problem="同語言 meta description 完全重複（%d 頁）" % len(group),
                cause="多頁共用相同描述",
                fix="為各頁改寫差異化 description。【勿編造未審核數字】",
                priority="P1",
                evidence={"lang": lang, "count": len(group), "sample": desc[:80], "kind": "dup_meta"},
                pages=slugs,
            ))

    return issues
