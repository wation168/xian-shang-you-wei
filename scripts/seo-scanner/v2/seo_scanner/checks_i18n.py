# -*- coding: utf-8 -*-
"""hreflang 缺漏與互指檢查。

重要：lottery 多用 zh-Hant-TW / zh-Hans-CN；
tools / patterns / glossary 多用 zh-TW / zh-CN。
預期集合以「同 slug 實際存在的語言」為準，並用雙對照相容兩套鍵名。
"""

from __future__ import annotations

from collections import defaultdict
from urllib.parse import urlparse

from .models import Page, Issue
from .parse import LANG_TO_HREFLANG_CANDIDATES, HREFLANG_TO_LANG, FOLDER_LANG_HINTS


def normalize_lang(lang: str) -> str:
    """把 html[lang] / 資料夾名 正規化成 LANG_TO_HREFLANG_CANDIDATES 的 key。"""
    if not lang:
        return ""
    raw = lang.strip()
    lower = raw.lower().replace("_", "-")
    # 直接命中
    for key in LANG_TO_HREFLANG_CANDIDATES:
        if key.lower() == lower:
            return key
    # hreflang 風格
    mapped = HREFLANG_TO_LANG.get(lower)
    if mapped and mapped != "x-default":
        return mapped
    # 資料夾 hint
    hint = FOLDER_LANG_HINTS.get(lower)
    if hint:
        return hint
    # zh-hant-tw → zh-TW
    if lower.startswith("zh-hant"):
        return "zh-TW"
    if lower.startswith("zh-hans"):
        return "zh-CN"
    if lower in ("zh-tw", "zh-hant-tw"):
        return "zh-TW"
    if lower in ("zh-cn", "zh-hans-cn"):
        return "zh-CN"
    return raw


def expected_hreflang_keys(langs_present: set[str], preferred_style: str) -> list[str]:
    """依同 slug 存在的語言，產生預期 hreflang 鍵。

    preferred_style: 從該 slug 任一頁「實際用過的鍵」推得的風格
      - 'bcp47-script' → zh-Hant-TW（lottery）
      - 'short' → zh-TW（tools/patterns/glossary）
    """
    keys = []
    for lang in sorted(langs_present):
        cands = LANG_TO_HREFLANG_CANDIDATES.get(lang, [lang])
        if preferred_style == "short":
            # 偏好短鍵：zh-TW / zh-CN / en
            pick = cands[-1] if lang.startswith("zh") and len(cands) > 1 else cands[0]
            # 對 zh：short 是 zh-TW（index 0 是 Hant，1 是 TW）— 依我們定義
            # LANG: zh-TW -> [zh-Hant-TW, zh-TW, zh-Hant]
            if lang == "zh-TW":
                pick = "zh-TW"
            elif lang == "zh-CN":
                pick = "zh-CN"
            else:
                pick = cands[0]
        else:
            # bcp47-script：偏好 zh-Hant-TW
            if lang == "zh-TW":
                pick = "zh-Hant-TW"
            elif lang == "zh-CN":
                pick = "zh-Hans-CN"
            else:
                pick = cands[0]
        keys.append(pick)
    keys.append("x-default")
    return keys


def detect_style(pages_for_slug: list[Page]) -> str:
    """從頁面實際 hreflang 鍵偵測風格。"""
    for p in pages_for_slug:
        for k in p.hreflang.keys():
            kl = k.lower()
            if kl in ("zh-hant-tw", "zh-hans-cn", "zh-hant", "zh-hans"):
                return "bcp47-script"
            if kl in ("zh-tw", "zh-cn"):
                return "short"
    return "short"  # tools 預設較常見


def _href_matches_page(href: str, page: Page) -> bool:
    """粗判 hreflang href 是否指向該頁。"""
    if not href:
        return False
    path = urlparse(href).path or href
    path = path.replace("\\", "/").rstrip("/")
    leaf = path.split("/")[-1]
    if leaf.endswith(".html"):
        leaf = leaf[:-5]
    file_stem = page.filename[:-5] if page.filename.lower().endswith(".html") else page.filename
    slug_leaf = page.slug.rsplit("/", 1)[-1]
    if leaf in (file_stem, slug_leaf):
        return True
    if page.slug and page.slug in path:
        return True
    return False


def check_i18n(pages: list[Page]) -> list[Issue]:
    issues: list[Issue] = []
    counter = 0

    # slug → 各語言頁面
    by_slug: dict[str, list[Page]] = defaultdict(list)
    for p in pages:
        if not p.slug:
            continue
        by_slug[p.slug].append(p)

    for slug, group in by_slug.items():
        langs = {normalize_lang(p.lang) for p in group if p.lang}
        langs.discard("")
        if len(langs) < 2 and len(group) < 2:
            # 單語頁：仍檢查是否宣告了不存在的語言（若有 hreflang）
            pass

        style = detect_style(group)
        expected = expected_hreflang_keys(langs, style) if langs else []

        # 建立：正規化語言 → Page
        lang_to_page = {}
        for p in group:
            nl = normalize_lang(p.lang)
            if nl:
                lang_to_page[nl] = p

        for p in group:
            counter += 1
            actual_keys = set(p.hreflang.keys())

            if not actual_keys and len(langs) >= 2:
                issues.append(Issue(
                    id="i18n-%04d" % counter,
                    category="i18n",
                    problem="多語言 slug 缺少 hreflang",
                    cause="同 slug 存在語言 %s，但本頁無 rel=alternate hreflang"
                        % ", ".join(sorted(langs)),
                    fix="補上指向各語言版本的 hreflang（含 x-default）。本站此區塊風格偏向 %s。"
                        % ("zh-Hant-TW" if style == "bcp47-script" else "zh-TW"),
                    priority="P1",
                    evidence={
                        "lang": p.lang,
                        "slug": slug,
                        "expected_langs": sorted(langs),
                        "style": style,
                        "path": p.path,
                    },
                    pages=[slug],
                ))
                continue

            if not expected:
                continue

            # 缺漏：預期鍵不在實際鍵中（相容雙對照：任一候選命中即可）
            missing = []
            for exp in expected:
                if exp == "x-default":
                    if "x-default" not in actual_keys and "x-default" not in {k.lower() for k in actual_keys}:
                        missing.append("x-default")
                    continue
                # 找此鍵對應的語言，看實際是否有任一候選
                exp_lang = HREFLANG_TO_LANG.get(exp.lower(), normalize_lang(exp))
                cands = LANG_TO_HREFLANG_CANDIDATES.get(exp_lang, [exp])
                if not any(c in actual_keys for c in cands) and exp not in actual_keys:
                    missing.append(exp)

            if missing:
                issues.append(Issue(
                    id="i18n-%04d" % counter,
                    category="i18n",
                    problem="hreflang 缺漏：%s" % ", ".join(missing),
                    cause="同 slug 實際存在的語言集合與本頁 hreflang 不完全對應",
                    fix="補上缺漏的 hreflang 標籤（鍵名與同資料夾其他頁保持一致："
                        "%s）。" % ("zh-Hant-TW 風格" if style == "bcp47-script" else "zh-TW 風格"),
                    priority="P2",
                    evidence={
                        "lang": p.lang,
                        "missing": missing,
                        "actual": sorted(actual_keys),
                        "expected": expected,
                        "style": style,
                    },
                    pages=[slug],
                ))

            # 互指：本頁宣告的每個 hreflang，目標頁應回指
            for hl_key, href in p.hreflang.items():
                if hl_key.lower() == "x-default":
                    continue
                target_lang = HREFLANG_TO_LANG.get(hl_key.lower()) or normalize_lang(hl_key)
                target = lang_to_page.get(target_lang)
                if target is None:
                    # 宣告了不存在的語言版本
                    issues.append(Issue(
                        id="i18n-orphan-%04d" % counter,
                        category="i18n",
                        problem="hreflang 指向不存在的語言版本（%s）" % hl_key,
                        cause="本頁宣告 %s，但同 slug 找不到對應語言檔" % hl_key,
                        fix="移除無效 hreflang，或補上該語言頁面。",
                        priority="P2",
                        evidence={"lang": p.lang, "hreflang": hl_key, "href": href, "slug": slug},
                        pages=[slug],
                    ))
                    continue

                # 目標頁是否有回指到本頁語言
                back_ok = False
                self_lang = normalize_lang(p.lang)
                self_cands = LANG_TO_HREFLANG_CANDIDATES.get(self_lang, [p.lang])
                for bk, bhref in target.hreflang.items():
                    if bk.lower() == "x-default":
                        continue
                    bk_lang = HREFLANG_TO_LANG.get(bk.lower()) or normalize_lang(bk)
                    if bk_lang == self_lang or bk in self_cands:
                        back_ok = True
                        break
                if target.hreflang and not back_ok:
                    counter += 1
                    issues.append(Issue(
                        id="i18n-recip-%04d" % counter,
                        category="i18n",
                        problem="hreflang 未互指",
                        cause="「%s」指向 %s，但目標頁未回指本頁語言 %s"
                            % (p.path, hl_key, self_lang),
                        fix="在目標頁（%s）補上指向本頁的 hreflang。" % target.path,
                        priority="P2",
                        evidence={
                            "from": p.path,
                            "to": target.path,
                            "hreflang": hl_key,
                            "slug": slug,
                        },
                        pages=[slug],
                    ))

    return issues
