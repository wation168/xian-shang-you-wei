# -*- coding: utf-8 -*-
"""掃描本機靜態 HTML，自動偵測版型並擷取 SEO 欄位。

版型策略（依序嘗試，有內容才採用）：
1. 有 <article> → article + section.faq（tools / patterns / 部分 glossary）
2. 否則非 sidebar 的 .card（lottery）
3. 否則 main / .content / .glossary-body / .main（後備）

hreflang：lottery 多用 zh-Hant-TW / zh-Hans-CN；
tools/patterns/glossary 多用 zh-TW / zh-CN。
本模組只記錄頁面「實際出現」的鍵；互指對照在 checks_i18n 處理。
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, Optional

from bs4 import BeautifulSoup

from .models import Page

# 排除非內容頁
EXCLUDE_FILENAMES = {
    "index.html", "privacy.html", "terms.html", "disclaimer.html",
    "refund.html", "contact.html", "about.html", "reset-password.html",
    "sitemap.xml", "404.html", "robots.txt",
}

# 資料夾名 → html[lang] 備援對照（路徑推語言時用）
FOLDER_LANG_HINTS = {
    "zh-tw": "zh-TW",
    "zh-cn": "zh-CN",
    "zh-hant": "zh-TW",
    "zh-hans": "zh-CN",
    "en": "en",
    "de": "de",
    "fr": "fr",
    "es": "es",
    "pt": "pt",
    "ko": "ko",
    "id": "id",
    "ja": "ja",
    "th": "th",
    "vi": "vi",
}

# 雙套 hreflang 對照（供 i18n 模組匯入）
# key = 資料夾／html lang 正規化後；value = 頁面可能使用的 hreflang 鍵集合
LANG_TO_HREFLANG_CANDIDATES = {
    "zh-TW": ["zh-Hant-TW", "zh-TW", "zh-Hant"],
    "zh-CN": ["zh-Hans-CN", "zh-CN", "zh-Hans"],
    "en": ["en"],
    "de": ["de"],
    "fr": ["fr"],
    "es": ["es"],
    "pt": ["pt", "pt-BR", "pt-PT"],
    "ko": ["ko"],
    "id": ["id"],
    "ja": ["ja"],
    "th": ["th"],
    "vi": ["vi"],
}

# 反向：hreflang 鍵 → 正規化語言（用於互指與同 slug 分組）
HREFLANG_TO_LANG = {}
for _lang, _cands in LANG_TO_HREFLANG_CANDIDATES.items():
    for _c in _cands:
        HREFLANG_TO_LANG[_c.lower()] = _lang
HREFLANG_TO_LANG["x-default"] = "x-default"


def clean_text(el) -> str:
    """抽出節點文字並合併多餘空白。"""
    if el is None:
        return ""
    text = el.get_text(separator=" ", strip=True)
    return re.sub(r"\s+", " ", text).strip()


def _posix_rel(path: Path, root: Path) -> str:
    """相對路徑一律用 /，Windows 友善。"""
    try:
        rel = path.resolve().relative_to(root.resolve())
    except ValueError:
        rel = path
    return rel.as_posix()


def infer_lang_from_path(rel_posix: str, html_lang: str) -> str:
    """優先用 html[lang]；否則從路徑第一段資料夾推。"""
    if html_lang:
        return html_lang.strip()
    parts = rel_posix.split("/")
    if parts:
        hint = FOLDER_LANG_HINTS.get(parts[0].lower())
        if hint:
            return hint
    return ""


def extract_slug(rel_posix: str, lang: str) -> str:
    """去掉語言前綴與 .html，得到跨語言可比對的 slug。"""
    parts = rel_posix.split("/")
    # 去掉副檔名
    if parts and parts[-1].lower().endswith(".html"):
        parts[-1] = parts[-1][:-5]
    # 若第一段是語言資料夾，去掉
    if parts:
        first_lower = parts[0].lower()
        if first_lower in FOLDER_LANG_HINTS:
            parts = parts[1:]
        # 也處理 html lang 對應資料夾名
        elif lang and first_lower.replace("_", "-") == lang.lower().replace("_", "-"):
            parts = parts[1:]
    return "/".join(parts) if parts else rel_posix


def extract_body(soup: BeautifulSoup) -> str:
    """自動偵測版型擷取正文。"""
    # 1) article + faq
    article_parts = []
    for art in soup.find_all("article"):
        t = clean_text(art)
        if t:
            article_parts.append(t)
    faq = soup.find("section", class_="faq")
    if faq:
        t = clean_text(faq)
        if t:
            article_parts.append(t)
    if article_parts:
        body = " ".join(article_parts)
        if len(body) >= 40:
            return body

    # 2) 非 sidebar 的 .card（lottery）
    card_parts = []
    for card in soup.find_all(class_="card"):
        if card.find_parent(class_="sidebar"):
            continue
        if card.find_parent(class_="subnav"):
            continue
        t = clean_text(card)
        if t:
            card_parts.append(t)
    if card_parts:
        body = " ".join(card_parts)
        if len(body) >= 40:
            return body

    # 3) 後備：main / .main / .content / .glossary-body
    for selector in [
        ("main", None),
        (None, "main"),
        (None, "content"),
        (None, "glossary-body"),
        ("div", "article"),
    ]:
        tag, cls = selector
        if cls:
            el = soup.find(tag, class_=cls) if tag else soup.find(class_=cls)
        else:
            el = soup.find(tag)
        if el:
            # 去掉 nav/sidebar
            clone_text = clean_text(el)
            if len(clone_text) >= 40:
                return clone_text

    # 最後：整頁 body，仍排除 nav/sidebar/script/style
    body_el = soup.find("body")
    if body_el:
        for junk in body_el.find_all(["script", "style", "nav", "footer", "header"]):
            junk.decompose()
        for junk in body_el.find_all(class_=["sidebar", "subnav", "more-tools"]):
            junk.decompose()
        return clean_text(body_el)
    return ""


def normalize_link_target(href: str) -> str:
    """把 href／path／slug 收成與 Page.slug 同一套身分 id。

    規則（順序固定）：
    1. 去掉 query／fragment、.html、前後空白
    2. 絕對 URL 只留 path
    3. 反覆去掉開頭的語言資料夾（en、zh-TW…）與站區段前綴（tools、lottery…）
    4. 回傳剩餘 path（通常是單一 leaf slug，與 extract_slug 對齊）

    例：
      /tools/apr-calculator.html          → apr-calculator
      https://x.com/lottery/en/foo.html   → foo
      ../zh-CN/bar.html                   → bar
      tools/en/baz                        → baz
      apr-calculator                      → apr-calculator
    """
    if not href:
        return ""
    s = href.strip()
    if not s or s.startswith(("#", "mailto:", "tel:", "javascript:")):
        return ""
    s = s.split("?")[0].split("#")[0].strip()
    if s.startswith("http://") or s.startswith("https://"):
        # softglow-ai.com/tools/en/foo.html → /tools/en/foo.html
        host_and_path = s.split("//", 1)[-1]
        slash = host_and_path.find("/")
        s = host_and_path[slash:] if slash >= 0 else ""
    s = s.lstrip("./").replace("\\", "/")
    # 去掉開頭多餘 /
    while s.startswith("/"):
        s = s[1:]
    if s.lower().endswith(".html"):
        s = s[:-5]
    parts = [p for p in s.split("/") if p and p != "."]
    # SoftGlow 站區段（掃描 root 是區段內時，slug 不含此前綴；連結卻常帶）
    site_sections = {
        "tools", "lottery", "patterns", "glossary", "blog",
        "comparisons", "home", "common", "quiz", "games",
    }
    changed = True
    while changed and parts:
        changed = False
        head = parts[0].lower().replace("_", "-")
        if head in FOLDER_LANG_HINTS:
            parts = parts[1:]
            changed = True
            continue
        if head in site_sections:
            parts = parts[1:]
            changed = True
            continue
    return "/".join(parts)


def link_ids_equivalent(a: str, b: str) -> bool:
    """兩個連結身分是否指向同一頁（含 leaf 對齊）。"""
    na, nb = normalize_link_target(a), normalize_link_target(b)
    if not na or not nb:
        return False
    if na == nb:
        return True
    return na.rsplit("/", 1)[-1] == nb.rsplit("/", 1)[-1]


def extract_internal_links(soup: BeautifulSoup, page_lang: str) -> list[str]:
    """從導覽／相關區塊抽出站內連結目標（已正規化成與 Page.slug 同一套 id）。"""
    containers = []
    for cls in ("more-tools", "related-card", "sidebar", "subnav"):
        containers.extend(soup.find_all(class_=cls))
    containers.extend(soup.find_all("nav"))

    seen = set()
    results = []
    for container in containers:
        for a in container.find_all("a", href=True):
            key = normalize_link_target(a["href"])
            if key and key not in seen:
                seen.add(key)
                results.append(key)
    return results



def parse_one_file(path: Path, root: Path) -> Optional[Page]:
    """解析單一 HTML；失敗回傳 None。"""
    if path.name.lower() in EXCLUDE_FILENAMES:
        return None
    if path.suffix.lower() != ".html":
        return None

    try:
        raw = path.read_text(encoding="utf-8", errors="strict")
    except UnicodeDecodeError:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None

    soup = BeautifulSoup(raw, "html.parser")
    rel = _posix_rel(path, root)

    html_tag = soup.find("html")
    html_lang = (html_tag.get("lang", "") or "").strip() if html_tag else ""
    lang = infer_lang_from_path(rel, html_lang)

    title = clean_text(soup.find("title"))
    meta_tag = soup.find("meta", attrs={"name": re.compile(r"^description$", re.I)})
    meta_description = (meta_tag.get("content", "") or "").strip() if meta_tag else ""

    h1_tags = soup.find_all("h1")
    h1 = clean_text(h1_tags[0]) if h1_tags else ""
    h1_count = len(h1_tags)

    canonical_tag = soup.find("link", attrs={"rel": re.compile(r"\bcanonical\b", re.I)})
    canonical = (canonical_tag.get("href", "") or "").strip() if canonical_tag else ""

    hreflang = {}
    for link in soup.find_all("link", attrs={"rel": re.compile(r"\balternate\b", re.I)}):
        hl = (link.get("hreflang") or "").strip()
        href = (link.get("href") or "").strip()
        if hl and href:
            hreflang[hl] = href

    body_text = extract_body(soup)
    slug = extract_slug(rel, lang)
    internal_links = extract_internal_links(soup, lang)

    return Page(
        path=rel,
        slug=slug,
        lang=lang,
        title=title,
        meta_description=meta_description,
        h1=h1,
        h1_count=h1_count,
        canonical=canonical,
        hreflang=hreflang,
        body_text=body_text,
        body_len=len(body_text),
        internal_links=internal_links,
        filename=path.name,
        abs_path=str(path.resolve()),
    )


def scan_root(root: Path, lang_filter: Optional[str] = None) -> list[Page]:
    """遞迴掃描 root 下所有 HTML。

    lang_filter: 若指定，只掃該語言子資料夾（加速），比對資料夾名不分大小寫。
    """
    root = Path(root)
    if not root.is_dir():
        raise FileNotFoundError(f"根目錄不存在：{root}")

    pages: list[Page] = []
    html_files: Iterable[Path] = root.rglob("*.html")

    filter_lower = lang_filter.lower().replace("_", "-") if lang_filter else None
    # 也接受 zh-Hant-TW 這類 → 對應資料夾可能是 zh-TW
    filter_aliases = set()
    if filter_lower:
        filter_aliases.add(filter_lower)
        # 正規化到資料夾常見名
        for folder, lang in FOLDER_LANG_HINTS.items():
            if lang.lower() == filter_lower or folder == filter_lower:
                filter_aliases.add(folder)
                filter_aliases.add(lang.lower())
        # hreflang 候選反查
        for lang, cands in LANG_TO_HREFLANG_CANDIDATES.items():
            if lang.lower() == filter_lower or any(c.lower() == filter_lower for c in cands):
                filter_aliases.add(lang.lower())
                for folder, flang in FOLDER_LANG_HINTS.items():
                    if flang == lang:
                        filter_aliases.add(folder)

    for path in html_files:
        if not path.is_file():
            continue
        if filter_aliases:
            rel = _posix_rel(path, root)
            first = rel.split("/")[0].lower() if rel else ""
            # 允許檔案直接在 root，或第一段命中別名
            parts = Path(rel).parts
            hit = False
            for part in parts[:-1]:  # 不含檔名
                if part.lower().replace("_", "-") in filter_aliases:
                    hit = True
                    break
            if not hit and first not in filter_aliases:
                # 若整個站沒有語言子資料夾（扁平），仍靠 html lang 過濾——先 parse 再濾
                page = parse_one_file(path, root)
                if page is None:
                    continue
                pl = (page.lang or "").lower().replace("_", "-")
                if pl not in filter_aliases and not any(
                    pl == a or pl.startswith(a + "-") for a in filter_aliases
                ):
                    continue
                pages.append(page)
                continue

        page = parse_one_file(path, root)
        if page is not None:
            pages.append(page)

    pages.sort(key=lambda p: (p.lang, p.slug, p.path))
    return pages
