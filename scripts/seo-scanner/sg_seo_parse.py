#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sg_seo_parse.py — SoftGlow 站內 SEO 掃描：第一步（掃描本機靜態HTML檔案）

用法（在command prompt裡，cd到scripts資料夾後）：
    python sg_seo_parse.py --root "D:/xian-shang-you-wei/backend/frontend/lottery" --out pages_lottery.json
    python sg_seo_parse.py --root "D:/xian-shang-you-wei/backend/frontend/tools" --out pages_tools.json
    （Windows路徑用正斜線 / 或雙反斜線都可以，Python都看得懂）

這支腳本不會發任何網路請求——直接掃描本機資料夾裡的html檔案，逐一讀取解析。
因為這些html檔案本來就是要部署上線的靜態檔案（跟Google實際抓到的內容一模一樣），
所以不需要寫爬蟲對線上網站發HTTP請求，掃描本機資料夾即可，速度是「秒級」而不是「分鐘級」。

輸出：一份 JSON 檔，每個頁面一筆資料，供下一步 sg_seo_analyze.py 使用。
"""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("缺少 beautifulsoup4 套件，請先執行：pip install beautifulsoup4")
    sys.exit(1)

# 排除非「工具/樂透頁面」的雜項html（首頁索引、隱私權等），這些不是要分析的內容頁
EXCLUDE_FILENAMES = {
    "index.html", "privacy.html", "terms.html", "disclaimer.html",
    "refund.html", "contact.html", "about.html", "reset-password.html",
    "sitemap.xml",
}


def clean_text(el):
    """把一個 BeautifulSoup 節點裡的文字抽出來，合併多餘空白。"""
    if el is None:
        return ""
    text = el.get_text(separator=" ", strip=True)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def parse_one_file(path: Path, root: Path):
    """解析單一html檔案，回傳一筆頁面資料 dict；解析失敗回傳 None（並附上原因）。"""
    try:
        raw = path.read_text(encoding="utf-8", errors="strict")
    except UnicodeDecodeError:
        # 極少數檔案編碼有問題，退回用 errors='replace' 讀取，並記錄警告
        raw = path.read_text(encoding="utf-8", errors="replace")

    soup = BeautifulSoup(raw, "html.parser")

    html_tag = soup.find("html")
    lang = html_tag.get("lang", "").strip() if html_tag else ""

    title_tag = soup.find("title")
    title = clean_text(title_tag)

    meta_desc_tag = soup.find("meta", attrs={"name": "description"})
    meta_description = (meta_desc_tag.get("content", "").strip()
                         if meta_desc_tag else "")

    h1_tag = soup.find("h1")
    h1 = clean_text(h1_tag)

    canonical_tag = soup.find("link", attrs={"rel": "canonical"})
    canonical = canonical_tag.get("href", "").strip() if canonical_tag else ""

    hreflang = {}
    for link in soup.find_all("link", attrs={"rel": "alternate"}):
        hl = link.get("hreflang")
        href = link.get("href")
        if hl and href:
            hreflang[hl] = href

    # 正文：不同站（工具站／樂透站）版型不一樣，用「試過就跳下一種」的方式抓，
    # 抓不到正文比誤判成「有內容」更危險（正文是空的，後面相似度分析會整批失真），
    # 所以每一種版型都實際驗證過抓得到東西才留在這裡。
    # 版型一：工具站(tools/)，正文包在 <article>，FAQ 是 <section class="faq">
    article_parts = []
    for art in soup.find_all("article"):
        article_parts.append(clean_text(art))
    faq_section = soup.find("section", class_="faq")
    if faq_section:
        article_parts.append(clean_text(faq_section))
    body_text = " ".join(p for p in article_parts if p)

    # 版型二：樂透站(lottery/)沒有<article>，正文是 .main 底下一串 <div class="card">
    # （包含FAQ，FAQ本來就是某張card裡的.faq-item，一起抓到了）。
    # 側欄 .sidebar 底下也有 class="card" 的區塊，但那些是「全站導覽／交叉推廣」樣板
    # （例如「所有樂透遊戲」清單、「試試選號工具」推廣卡），不是這頁自己的正文，
    # 每頁都一樣，混進來會讓相似度分析全部失真，所以明確排除掉。
    if not body_text:
        card_parts = []
        for card in soup.find_all(class_="card"):
            if card.find_parent(class_="sidebar"):
                continue
            card_copy = BeautifulSoup(str(card), "html.parser")
            for ad in card_copy.find_all(class_="ad-slot"):
                ad.decompose()
            card_parts.append(clean_text(card_copy))
        body_text = " ".join(p for p in card_parts if p)

    # 既有的站內連結，用來判斷「這頁本來就有連到誰」，同樣分版型嘗試：
    # 版型一：工具站的「更多工具」／「相關工具」區塊
    existing_links = []
    for container_class in ("more-tools", "related-card"):
        container = soup.find(class_=container_class)
        if not container:
            continue
        for a in container.find_all("a", href=True):
            href = a["href"]
            anchor = clean_text(a)
            existing_links.append({"href": href, "anchor": anchor})

    # 版型二：樂透站的側欄 .sidebar 裡有一張「所有樂透遊戲」導覽卡，是全站共用的
    # 導覽連結（不是這頁專屬的相關內容連結），但一樣代表「這個目標已經被連到了」，
    # 拿來判斷already_linked仍然有效——只是要注意：因為每頁都有這份清單，
    # 遊戲總覽頁(xxx.html)彼此之間幾乎都已經互連，Module A的建議因此會集中在
    # 「總覽頁該連到自己的history/results/statistics頁」「選號工具之間互連」
    # 這類側欄清單沒涵蓋到的地方，這是正常、預期中的結果。
    if not existing_links:
        sidebar = soup.find(class_="sidebar")
        if sidebar:
            for a in sidebar.find_all("a", href=True):
                if a.find_parent(class_="ad-slot"):
                    continue
                href = a["href"]
                anchor = clean_text(a)
                existing_links.append({"href": href, "anchor": anchor})

    # 樂透站每個「遊戲」自己還有一排分頁籤 .subnav（總覽／Results／History／
    # Statistics／Number Generator），這是「同一個遊戲」內部幾個子頁面互連的地方，
    # 跟.sidebar的「全站所有遊戲」清單是兩回事，兩個都要算進「已經連過了」，
    # 不然history/statistics這些子頁面明明已經彼此連好，卻會被誤判成「還沒連」。
    subnav = soup.find(class_="subnav")
    if subnav:
        for a in subnav.find_all("a", href=True):
            href = a["href"]
            anchor = clean_text(a)
            existing_links.append({"href": href, "anchor": anchor})

    # slug：檔名（不含副檔名），用來比對「同一個工具/頁面的不同語言版本」
    slug = path.stem

    rel_path = str(path.relative_to(root)).replace("\\", "/")

    return {
        "file": rel_path,
        "slug": slug,
        "lang": lang,
        "url": canonical,
        "title": title,
        "meta_description": meta_description,
        "h1": h1,
        "canonical": canonical,
        "hreflang": hreflang,
        "body_text": body_text,
        "text_length": len(body_text),
        "existing_links": existing_links,
    }


def main():
    ap = argparse.ArgumentParser(description="掃描本機HTML資料夾，輸出頁面資料JSON")
    ap.add_argument("--root", required=True, help="要掃描的資料夾路徑，例如 tools 或 lottery 目錄")
    ap.add_argument("--out", required=True, help="輸出的JSON檔名")
    args = ap.parse_args()

    root = Path(args.root)
    if not root.is_dir():
        print(f"❌ 找不到資料夾：{root}")
        sys.exit(1)

    html_files = sorted(root.rglob("*.html"))
    pages = []
    skipped = []
    errors = []

    for f in html_files:
        if f.name in EXCLUDE_FILENAMES:
            skipped.append(str(f.relative_to(root)))
            continue
        try:
            page = parse_one_file(f, root)
            pages.append(page)
        except Exception as e:
            errors.append({"file": str(f.relative_to(root)), "error": str(e)})

    result = {
        "root": str(root),
        "total_html_files": len(html_files),
        "parsed": len(pages),
        "skipped": skipped,
        "errors": errors,
        "pages": pages,
    }

    out_path = Path(args.out)
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✅ 掃描完成：共 {len(html_files)} 個html檔案，成功解析 {len(pages)} 頁，"
          f"跳過 {len(skipped)} 個非內容頁，{len(errors)} 個解析錯誤")
    if errors:
        print("⚠️ 解析錯誤的檔案：")
        for e in errors:
            print(f"   - {e['file']}: {e['error']}")
    print(f"輸出檔案：{out_path.resolve()}")


if __name__ == "__main__":
    main()
