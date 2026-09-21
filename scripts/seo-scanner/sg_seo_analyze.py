#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sg_seo_analyze.py — SoftGlow 站內 SEO 掃描：第二步（分析＋產生儀表板）

用法：
    python sg_seo_analyze.py --pages pages_lottery.json --site-name "樂透站" --out dashboard_lottery.html
    python sg_seo_analyze.py --pages pages_tools.json --site-name "323工具平台" --out dashboard_tools.html

    如果有從GSC匯出的CSV（欄位需含 Page/網頁 和 Impressions/曝光 兩欄），可以加：
    python sg_seo_analyze.py --pages pages_tools.json --gsc-csv gsc_export.csv --out dashboard_tools.html

這支腳本讀第一步 sg_seo_parse.py 輸出的 pages.json，做兩件獨立的分析：
  模組A：內部連結地圖——同語言頁面之間，主題相似但目前沒有互連的，列成建議清單
  模組B：規模化內容濫用（Scaled Content Abuse）自查——重複內容／重複title-meta／
         hreflang-canonical正確性／（若有提供GSC資料）長期零曝光頁面

輸出一個「單一、自包含」的HTML儀表板——資料直接內嵌在檔案裡，雙擊就能開，
不需要另外開本機伺服器（如果用fetch()讀外部json檔，用瀏覽器雙擊打開html時
會被瀏覽器的file://安全限制擋下來，所以改成資料內嵌）。
"""

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError:
    print("缺少 scikit-learn 套件，請先執行：pip install scikit-learn")
    sys.exit(1)
import numpy as np

# 全站已知語言代碼（用來檢查hreflang有沒有缺漏）
# 注意：<html lang="..">用的是簡碼（zh-TW／zh-CN），但實際hreflang標籤用的是更精確的
# BCP47格式（zh-Hant-TW／zh-Hans-CN，這其實是Google建議的正確寫法，不是站方寫錯）。
# 這個對照表就是用來把「頁面自己的語言」轉換成「hreflang標籤裡該用的代碼」，
# 兩者要對得起來，才不會把「已定案的正確用法」誤判成「缺漏」。
LANG_TO_HREFLANG = {
    "zh-TW": "zh-Hant-TW", "zh-CN": "zh-Hans-CN",
    "en": "en", "de": "de", "fr": "fr", "es": "es",
    "pt": "pt", "ko": "ko", "id": "id", "ja": "ja",
}

LINK_SIM_THRESHOLD = 0.12      # 主題相似度超過這個值才建議互連（char n-gram cosine，經驗值，非絕對）
DUPLICATE_SIM_THRESHOLD = 0.90  # 超過這個值視為「內容高度重複」候選，要人工複查
TOP_N_SUGGESTIONS = 5           # 每頁最多建議幾個連結對象


def load_pages(paths):
    pages = []
    for p in paths:
        data = json.loads(Path(p).read_text(encoding="utf-8"))
        pages.extend(data["pages"])
    return pages


def build_similarity(pages_subset):
    """對同一批頁面（通常是同語言）算char n-gram TF-IDF cosine相似度矩陣。
    用字元n-gram而不是用空白分詞，是因為中文/日文/韓文沒有空白斷詞，
    字元n-gram對所有語言都適用，不用另外裝jieba/mecab這類語言專用斷詞工具。"""
    texts = [p["body_text"] or p["title"] for p in pages_subset]
    if len(texts) < 2:
        return None
    vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=1)
    matrix = vec.fit_transform(texts)
    return cosine_similarity(matrix)


def analyze_link_map(pages):
    """模組A：內部連結地圖。回傳 {lang: [ {from, to, similarity, anchor_suggestion, already_linked}, ... ]}"""
    by_lang = defaultdict(list)
    for p in pages:
        by_lang[p["lang"]].append(p)

    result = {}
    for lang, subset in by_lang.items():
        sim = build_similarity(subset)
        if sim is None:
            result[lang] = {"page_count": len(subset), "suggestions": []}
            continue

        suggestions = []
        for i, page in enumerate(subset):
            existing_hrefs = {l["href"] for l in page["existing_links"]}
            # 找出跟這頁最相似的其他頁面，排序後取前N名
            sims = [(j, sim[i][j]) for j in range(len(subset)) if j != i]
            sims.sort(key=lambda x: x[1], reverse=True)
            for j, score in sims[:TOP_N_SUGGESTIONS]:
                if score < LINK_SIM_THRESHOLD:
                    continue
                if score >= DUPLICATE_SIM_THRESHOLD:
                    # 相似度高到這個地步，兩頁根本是同一個模板套不同遊戲名稱／年份，
                    # 這種狀況該做的是「把內容改得更有差異化」，不是「幫它們互連」——
                    # 互連兩篇幾乎一樣的頁面對SEO沒有幫助，這種情況已經在Module B
                    # 的「重複內容」清單報過了，這裡不重複建議，避免灌水又誤導。
                    continue
                target = subset[j]
                # 判斷這個連結是否已經存在（用檔名/slug去比對href尾端）
                already = any(target["slug"] in href for href in existing_hrefs)
                suggestions.append({
                    "from_slug": page["slug"],
                    "from_title": page["title"],
                    "to_slug": target["slug"],
                    "to_title": target["title"],
                    "similarity": round(float(score), 3),
                    "already_linked": already,
                    "anchor_suggestion": target["h1"] or target["title"],
                })
        # 只保留「還沒連」的建議，已經連好的不用再提示
        missing = [s for s in suggestions if not s["already_linked"]]
        missing.sort(key=lambda x: x["similarity"], reverse=True)
        result[lang] = {"page_count": len(subset), "suggestions": missing}
    return result


def analyze_spam_audit(pages):
    """模組B：Scaled Content Abuse 自查。"""
    findings = {
        "duplicate_content": [],
        "duplicate_title": [],
        "duplicate_meta": [],
        "canonical_issues": [],
        "hreflang_missing": [],
        "hreflang_reciprocity_issues": [],
        "summary": {},
    }

    by_lang = defaultdict(list)
    url_map = {}
    for p in pages:
        by_lang[p["lang"]].append(p)
        if p["url"]:
            url_map[p["url"]] = p

    # 1. 同語言內：重複內容偵測
    for lang, subset in by_lang.items():
        sim = build_similarity(subset)
        if sim is None:
            continue
        seen_pairs = set()
        for i in range(len(subset)):
            for j in range(i + 1, len(subset)):
                score = sim[i][j]
                if score >= DUPLICATE_SIM_THRESHOLD:
                    pair = tuple(sorted([subset[i]["slug"], subset[j]["slug"]]))
                    if pair in seen_pairs:
                        continue
                    seen_pairs.add(pair)
                    findings["duplicate_content"].append({
                        "lang": lang,
                        "page_a": subset[i]["slug"],
                        "page_b": subset[j]["slug"],
                        "similarity": round(float(score), 3),
                    })

    # 2/3. 同語言內：title / meta description 完全重複
    for lang, subset in by_lang.items():
        title_groups = defaultdict(list)
        meta_groups = defaultdict(list)
        for p in subset:
            if p["title"]:
                title_groups[p["title"]].append(p["slug"])
            if p["meta_description"]:
                meta_groups[p["meta_description"]].append(p["slug"])
        for title, slugs in title_groups.items():
            if len(slugs) > 1:
                findings["duplicate_title"].append({"lang": lang, "title": title, "pages": slugs})
        for meta, slugs in meta_groups.items():
            if len(slugs) > 1:
                findings["duplicate_meta"].append({"lang": lang, "meta_description": meta, "pages": slugs})

    # 4. canonical 是否自我指向（一個頁面的canonical應該等於自己的URL）
    for p in pages:
        if p["canonical"] and p["url"] and p["canonical"] != p["url"]:
            findings["canonical_issues"].append({
                "slug": p["slug"], "lang": p["lang"],
                "url": p["url"], "canonical": p["canonical"],
            })
        elif not p["canonical"]:
            findings["canonical_issues"].append({
                "slug": p["slug"], "lang": p["lang"],
                "url": p["url"], "canonical": "(缺少canonical標籤)",
            })

    # 5. hreflang 是否缺漏語言 + 互相對應（reciprocity）
    # 判斷「缺漏」的基準不是「每一頁都該有全部10種語言」（很多樂透遊戲本來就只在特定
    # 國家上架，例如Powerball只有英文版，這不是缺漏，是設計如此），而是「這個slug實際
    # 存在的語言版本，是否每個都被這頁的hreflang涵蓋到」——同一slug在幾種語言下都有
    # 檔案，就該有幾個hreflang對應。
    slug_to_langs = defaultdict(set)
    for p in pages:
        slug_to_langs[p["slug"]].add(p["lang"])

    for p in pages:
        existing_langs = slug_to_langs[p["slug"]]
        expected_codes = {LANG_TO_HREFLANG.get(l, l) for l in existing_langs}
        expected_codes.add("x-default")
        have = set(p["hreflang"].keys())
        missing = expected_codes - have
        if missing:
            findings["hreflang_missing"].append({
                "slug": p["slug"], "lang": p["lang"], "url": p["url"],
                "missing": sorted(missing),
            })
        for hl, href in p["hreflang"].items():
            if hl == "x-default":
                continue  # x-default本身不用檢查對方是否回指
            target = url_map.get(href)
            if target is None:
                continue  # 目標頁面不在這次掃描範圍內，無法驗證，跳過
            expected_back_code = LANG_TO_HREFLANG.get(p["lang"], p["lang"])
            back = target["hreflang"].get(expected_back_code)
            if back != p["url"]:
                findings["hreflang_reciprocity_issues"].append({
                    "from_slug": p["slug"], "from_lang": p["lang"], "from_url": p["url"],
                    "to_slug": target["slug"], "to_lang": target["lang"], "to_url": href,
                })

    findings["summary"] = {
        "total_pages": len(pages),
        "duplicate_content_pairs": len(findings["duplicate_content"]),
        "duplicate_title_groups": len(findings["duplicate_title"]),
        "duplicate_meta_groups": len(findings["duplicate_meta"]),
        "canonical_issues": len(findings["canonical_issues"]),
        "hreflang_missing_pages": len(findings["hreflang_missing"]),
        "hreflang_reciprocity_issues": len(findings["hreflang_reciprocity_issues"]),
    }
    return findings


def analyze_gsc(pages, gsc_csv_path):
    """（選用）合併GSC匯出的CSV，找出長期零曝光的頁面。"""
    if not gsc_csv_path:
        return None
    rows = []
    with open(gsc_csv_path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if not rows:
        return {"error": "GSC CSV是空的"}

    # GSC匯出的欄位名稱依語言介面可能是「網頁」「Page」「Top pages」等，這裡盡量抓常見欄位名
    page_col = None
    impr_col = None
    for col in rows[0].keys():
        lc = col.strip().lower()
        if page_col is None and lc in ("page", "top pages", "網頁", "網址"):
            page_col = col
        if impr_col is None and lc in ("impressions", "曝光", "曝光次數"):
            impr_col = col
    if not page_col or not impr_col:
        return {"error": f"認不出GSC CSV的欄位名稱，目前欄位是：{list(rows[0].keys())}，"
                          f"請確認匯出時有包含網頁/曝光兩欄"}

    gsc_by_url = {}
    for row in rows:
        url = row[page_col].strip()
        try:
            impr = int(float(row[impr_col]))
        except (ValueError, KeyError):
            impr = 0
        gsc_by_url[url] = impr

    zero_impression = []
    matched = 0
    for p in pages:
        if p["url"] in gsc_by_url:
            matched += 1
            if gsc_by_url[p["url"]] == 0:
                zero_impression.append({"slug": p["slug"], "lang": p["lang"], "url": p["url"]})

    return {
        "gsc_rows": len(rows),
        "matched_pages": matched,
        "zero_impression_pages": zero_impression,
        "zero_impression_count": len(zero_impression),
    }


DASHBOARD_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<title>{site_name} — SEO掃描儀表板</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  :root {{
    --bg: #0f1117; --panel: #171a24; --border: #2a2f3d; --text: #e8eaf0;
    --muted: #8b90a3; --accent: #6ea8fe; --danger: #ff6b6b; --warn: #ffb454; --ok: #4ade80;
  }}
  * {{ box-sizing: border-box; }}
  body {{ margin:0; font-family: -apple-system, "Noto Sans TC", "Segoe UI", sans-serif;
         background: var(--bg); color: var(--text); }}
  header {{ padding: 20px 28px; border-bottom: 1px solid var(--border); }}
  header h1 {{ margin: 0 0 4px; font-size: 20px; }}
  header .meta {{ color: var(--muted); font-size: 13px; }}
  .tabs {{ display: flex; gap: 4px; padding: 0 28px; border-bottom: 1px solid var(--border); }}
  .tab {{ padding: 12px 18px; cursor: pointer; color: var(--muted); border-bottom: 2px solid transparent;
         font-size: 14px; user-select: none; }}
  .tab.active {{ color: var(--text); border-bottom-color: var(--accent); }}
  .view {{ display: none; padding: 24px 28px; }}
  .view.active {{ display: block; }}
  .stat-row {{ display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 20px; }}
  .stat {{ background: var(--panel); border: 1px solid var(--border); border-radius: 10px;
          padding: 14px 18px; min-width: 140px; }}
  .stat .num {{ font-size: 24px; font-weight: 700; }}
  .stat .label {{ color: var(--muted); font-size: 12px; margin-top: 2px; }}
  .stat.danger .num {{ color: var(--danger); }}
  .stat.warn .num {{ color: var(--warn); }}
  .stat.ok .num {{ color: var(--ok); }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; margin-bottom: 24px; }}
  th, td {{ text-align: left; padding: 8px 10px; border-bottom: 1px solid var(--border); }}
  th {{ color: var(--muted); font-weight: 500; font-size: 12px; }}
  .badge {{ display: inline-block; padding: 2px 8px; border-radius: 999px; font-size: 11px; }}
  .badge.high {{ background: rgba(255,107,107,.15); color: var(--danger); }}
  .badge.mid {{ background: rgba(255,180,84,.15); color: var(--warn); }}
  section h2 {{ font-size: 16px; margin: 28px 0 10px; }}
  .empty {{ color: var(--muted); font-size: 13px; padding: 8px 0; }}
  select {{ background: var(--panel); color: var(--text); border: 1px solid var(--border);
           border-radius: 6px; padding: 6px 10px; font-size: 13px; }}
  code {{ background: rgba(255,255,255,.06); padding: 1px 5px; border-radius: 4px; }}
</style>
</head>
<body>
<header>
  <h1>{site_name} — SEO掃描儀表板</h1>
  <div class="meta">掃描頁數：{total_pages} ｜ 產生時間：{generated_at}（資料為本機檔案掃描結果，非即時線上資料）</div>
</header>
<div class="tabs">
  <div class="tab active" data-view="linkmap">內部連結地圖</div>
  <div class="tab" data-view="spam">規模化內容濫用自查</div>
</div>

<div id="view-linkmap" class="view active">
  <div class="stat-row" id="linkmap-stats"></div>
  <label>語言：<select id="lang-select"></select></label>
  <table id="linkmap-table">
    <thead><tr><th>來源頁</th><th>建議連到</th><th>相似度</th><th>建議錨點文字</th></tr></thead>
    <tbody></tbody>
  </table>
</div>

<div id="view-spam" class="view">
  <div class="stat-row" id="spam-stats"></div>
  <section>
    <h2>重複內容（同語言頁面內容高度相似，需人工複查是不是換湯不換藥）</h2>
    <div id="spam-duplicate-content"></div>
  </section>
  <section>
    <h2>Title 重複</h2>
    <div id="spam-duplicate-title"></div>
  </section>
  <section>
    <h2>Meta Description 重複</h2>
    <div id="spam-duplicate-meta"></div>
  </section>
  <section>
    <h2>Canonical 標籤問題</h2>
    <div id="spam-canonical"></div>
  </section>
  <section>
    <h2>Hreflang 缺漏</h2>
    <div id="spam-hreflang-missing"></div>
  </section>
  <section>
    <h2>Hreflang 互相對應問題</h2>
    <div id="spam-hreflang-recip"></div>
  </section>
  <section id="gsc-section" style="display:none">
    <h2>GSC 長期零曝光頁面</h2>
    <div id="spam-gsc"></div>
  </section>
</div>

<script>
const REPORT = {report_json};

document.querySelectorAll(".tab").forEach(function(tab) {{
  tab.addEventListener("click", function() {{
    document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
    document.querySelectorAll(".view").forEach(v => v.classList.remove("active"));
    tab.classList.add("active");
    document.getElementById("view-" + tab.dataset.view).classList.add("active");
  }});
}});

function esc(s) {{
  return String(s == null ? "" : s).replace(/[&<>"]/g, c => ({{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}}[c]));
}}

// ---- 內部連結地圖 ----
const langSelect = document.getElementById("lang-select");
const langs = Object.keys(REPORT.link_map);
langs.forEach(l => {{
  const opt = document.createElement("option");
  opt.value = l; opt.textContent = l + "（" + REPORT.link_map[l].page_count + "頁）";
  langSelect.appendChild(opt);
}});

function renderLinkMap(lang) {{
  const data = REPORT.link_map[lang];
  const tbody = document.querySelector("#linkmap-table tbody");
  tbody.innerHTML = "";
  document.getElementById("linkmap-stats").innerHTML =
    '<div class="stat"><div class="num">' + data.page_count + '</div><div class="label">頁面數</div></div>' +
    '<div class="stat warn"><div class="num">' + data.suggestions.length + '</div><div class="label">建議新增連結</div></div>';
  if (data.suggestions.length === 0) {{
    tbody.innerHTML = '<tr><td colspan="4" class="empty">沒有找到建議（可能頁面太少，或都已經互連）</td></tr>';
    return;
  }}
  data.suggestions.forEach(function(s) {{
    const tr = document.createElement("tr");
    tr.innerHTML = '<td>' + esc(s.from_title) + '<br><code>' + esc(s.from_slug) + '</code></td>' +
      '<td>' + esc(s.to_title) + '<br><code>' + esc(s.to_slug) + '</code></td>' +
      '<td>' + s.similarity + '</td>' +
      '<td>' + esc(s.anchor_suggestion) + '</td>';
    tbody.appendChild(tr);
  }});
}}
if (langs.length) {{ langSelect.value = langs[0]; renderLinkMap(langs[0]); }}
langSelect.addEventListener("change", () => renderLinkMap(langSelect.value));

// ---- Scaled Content Abuse 自查 ----
const spam = REPORT.spam_audit;
const s = spam.summary;
document.getElementById("spam-stats").innerHTML = [
  ["duplicate_content_pairs", "重複內容配對", "danger"],
  ["duplicate_title_groups", "Title重複組數", "warn"],
  ["duplicate_meta_groups", "Meta重複組數", "warn"],
  ["canonical_issues", "Canonical問題", "danger"],
  ["hreflang_missing_pages", "Hreflang缺漏頁數", "warn"],
  ["hreflang_reciprocity_issues", "Hreflang互指問題", "warn"],
].map(([key, label, cls]) =>
  '<div class="stat ' + (s[key] > 0 ? cls : "ok") + '"><div class="num">' + s[key] + '</div><div class="label">' + label + '</div></div>'
).join("");

function renderList(elId, items, rowFn) {{
  const el = document.getElementById(elId);
  if (!items || items.length === 0) {{ el.innerHTML = '<div class="empty">沒有發現問題</div>'; return; }}
  el.innerHTML = '<table><tbody>' + items.map(rowFn).join("") + '</tbody></table>';
}}

renderList("spam-duplicate-content", spam.duplicate_content, i =>
  '<tr><td><span class="badge high">' + i.similarity + '</span></td><td>' + esc(i.lang) + '</td>' +
  '<td><code>' + esc(i.page_a) + '</code> ⟷ <code>' + esc(i.page_b) + '</code></td></tr>');

renderList("spam-duplicate-title", spam.duplicate_title, i =>
  '<tr><td>' + esc(i.lang) + '</td><td>' + esc(i.title) + '</td><td>' + i.pages.map(esc).join(", ") + '</td></tr>');

renderList("spam-duplicate-meta", spam.duplicate_meta, i =>
  '<tr><td>' + esc(i.lang) + '</td><td>' + esc(i.meta_description).slice(0,80) + '</td><td>' + i.pages.map(esc).join(", ") + '</td></tr>');

renderList("spam-canonical", spam.canonical_issues, i =>
  '<tr><td>' + esc(i.lang) + '</td><td><code>' + esc(i.slug) + '</code></td><td>' + esc(i.canonical) + '</td></tr>');

renderList("spam-hreflang-missing", spam.hreflang_missing, i =>
  '<tr><td>' + esc(i.lang) + '</td><td><code>' + esc(i.slug) + '</code></td><td>缺少：' + i.missing.map(esc).join(", ") + '</td></tr>');

renderList("spam-hreflang-recip", spam.hreflang_reciprocity_issues, i =>
  '<tr><td><code>' + esc(i.from_slug) + '</code>（' + esc(i.from_lang) + '）</td><td>→</td>' +
  '<td><code>' + esc(i.to_slug) + '</code>（' + esc(i.to_lang) + '）沒有指回來</td></tr>');

if (REPORT.gsc_audit) {{
  document.getElementById("gsc-section").style.display = "block";
  const g = REPORT.gsc_audit;
  if (g.error) {{
    document.getElementById("spam-gsc").innerHTML = '<div class="empty">' + esc(g.error) + '</div>';
  }} else {{
    renderList("spam-gsc", g.zero_impression_pages, i =>
      '<tr><td>' + esc(i.lang) + '</td><td><code>' + esc(i.slug) + '</code></td><td>' + esc(i.url) + '</td></tr>');
  }}
}}
</script>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser(description="分析pages.json並產生SEO掃描儀表板")
    ap.add_argument("--pages", nargs="+", required=True, help="一個或多個 sg_seo_parse.py 產生的json檔")
    ap.add_argument("--site-name", default="SoftGlow", help="顯示在儀表板標題的站名")
    ap.add_argument("--gsc-csv", default=None, help="（選用）GSC匯出的CSV檔路徑")
    ap.add_argument("--out", required=True, help="輸出的html儀表板檔名")
    args = ap.parse_args()

    pages = load_pages(args.pages)
    if not pages:
        print("❌ 沒有讀到任何頁面資料")
        sys.exit(1)

    print(f"讀取 {len(pages)} 頁，開始分析...")
    link_map = analyze_link_map(pages)
    spam_audit = analyze_spam_audit(pages)
    gsc_audit = analyze_gsc(pages, args.gsc_csv)

    report = {
        "site_name": args.site_name,
        "total_pages": len(pages),
        "link_map": link_map,
        "spam_audit": spam_audit,
        "gsc_audit": gsc_audit,
    }

    import datetime
    # 保險：頁面內容裡萬一真的出現「</script」這幾個字，要避免它提前把<script>標籤關掉
    report_json = json.dumps(report, ensure_ascii=False).replace("</script", "<\\/script")
    html = DASHBOARD_TEMPLATE.format(
        site_name=args.site_name,
        total_pages=len(pages),
        generated_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        report_json=report_json,
    )
    Path(args.out).write_text(html, encoding="utf-8")

    print(f"✅ 分析完成，儀表板已產生：{Path(args.out).resolve()}")
    print(f"   內部連結建議：{sum(len(v['suggestions']) for v in link_map.values())} 條")
    print(f"   自查發現項目：{json.dumps(spam_audit['summary'], ensure_ascii=False)}")
    print("雙擊這個html檔案就能用瀏覽器打開看結果，不用開伺服器。")


if __name__ == "__main__":
    main()
