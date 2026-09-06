# -*- coding: utf-8 -*-
r"""
generate_comparisons_index.py
2026/07/30 產出：為 frontend/comparisons/ 底下每個語言資料夾（含根目錄=zh-TW）
產生缺少的 index.html 清單頁，解決 /comparisons/{locale} 404 的SEO缺口。

【使用方式】
1. 把這支腳本放在 D:\xian-shang-you-wei\scripts\ 底下（不放backend，避免誤部署，
   照帥哥鴻訂的規則：所有本機腳本一律放scripts資料夾）
2. 先 dry-run 看會產生哪些檔案，不會真的寫入任何東西：
   cd D:\xian-shang-you-wei\scripts
   python generate_comparisons_index.py
3. 確認清單沒問題後，加 --apply 才會真的寫入檔案：
   python generate_comparisons_index.py --apply

【安全設計】
- 預設 dry-run，不加 --apply 不會寫入任何檔案
- 只在 index.html 不存在時才建立，絕不覆蓋已存在的 index.html（避免誤刪已有內容）
- 每篇文章的標題/描述直接從該篇文章的 <title>/<meta description> 抓取，不是憑空編造
- 找不到任何文章的語言資料夾會跳過並印出警告，不會產生空白頁
"""
import os
import re
import sys
import argparse

BASE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "backend", "frontend", "comparisons"
)
BASE_DIR = os.path.normpath(BASE_DIR)

# locale: (資料夾名, 網址路徑, hreflang代碼, 頁面顯示語言名稱, hero標題, hero說明, nav文字, footer連結文字)
LOCALES = [
    ("",     "/comparisons/",       "zh-tw", "繁體中文", "投資理財工具完整比較指南",
     "比較各種投資理財工具、技術指標與策略的優缺點，幫助你做出更明智的決定。", "工具", "首頁"),
    ("en",   "/comparisons/en/",    "en",    "English", "Complete Financial Tools Comparison Guide",
     "Compare investment tools, technical indicators, and strategies side by side to make smarter decisions.", "Tools", "Home"),
    ("ja",   "/comparisons/ja/",    "ja",    "日本語", "投資ツール完全比較ガイド",
     "投資ツール、テクニカル指標、戦略を徹底比較し、より賢い判断をサポートします。", "ツール", "ホーム"),
    ("ko",   "/comparisons/ko/",    "ko",    "한국어", "투자 도구 완벽 비교 가이드",
     "투자 도구, 기술 지표, 전략을 나란히 비교하여 더 스마트한 결정을 내리세요.", "도구", "홈"),
    ("es",   "/comparisons/es/",    "es",    "Español", "Guía Completa de Comparación de Herramientas Financieras",
     "Compara herramientas de inversión, indicadores técnicos y estrategias para tomar mejores decisiones.", "Herramientas", "Inicio"),
    ("pt",   "/comparisons/pt/",    "pt",    "Português", "Guia Completo de Comparação de Ferramentas Financeiras",
     "Compare ferramentas de investimento, indicadores técnicos e estratégias para decisões mais inteligentes.", "Ferramentas", "Início"),
    ("id",   "/comparisons/id/",    "id",    "Indonesia", "Panduan Lengkap Perbandingan Alat Keuangan",
     "Bandingkan alat investasi, indikator teknikal, dan strategi untuk keputusan yang lebih cerdas.", "Alat", "Beranda"),
    ("de",   "/comparisons/de/",    "de",    "Deutsch", "Vollständiger Vergleichsleitfaden für Finanztools",
     "Vergleichen Sie Investment-Tools, technische Indikatoren und Strategien für klügere Entscheidungen.", "Tools", "Startseite"),
    ("fr",   "/comparisons/fr/",    "fr",    "Français", "Guide Complet de Comparaison des Outils Financiers",
     "Comparez les outils d'investissement, les indicateurs techniques et les stratégies pour de meilleures décisions.", "Outils", "Accueil"),
    ("zh-CN","/comparisons/zh-CN/", "zh-cn", "简体中文", "投资理财工具完整比较指南",
     "比较各种投资理财工具、技术指标与策略的优缺点，帮助你做出更明智的决定。", "工具", "首页"),
]

ALL_LOCALE_CODES = [(loc[0] or "zh-tw" if loc[0] == "" else loc[0]) for loc in LOCALES]

TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S)
DESC_RE = re.compile(r'<meta\s+name="description"\s+content="([^"]*)"', re.S)


def extract_meta(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return None, None
    tm = TITLE_RE.search(content)
    dm = DESC_RE.search(content)
    title = tm.group(1).strip() if tm else None
    desc = dm.group(1).strip() if dm else ""
    return title, desc


def build_index_html(locale_folder, url_prefix, hreflang_self, lang_label,
                      hero_title, hero_desc, nav_tools_text, nav_home_text, articles):
    """articles: list of (filename, title, desc)"""
    cards = "\n".join(
        f'    <a href="{url_prefix}{fn}" class="tool-card">{title}</a>'
        for fn, title, desc in articles
    )

    # hreflang alternate 連結：跟其他10個語言版本互相聲明
    alt_links = []
    for loc, prefix, hl, *_ in LOCALES:
        alt_links.append(f'<link rel="alternate" hreflang="{hl}" href="https://softglow-ai.com{prefix}">')
    alt_links.append(f'<link rel="alternate" hreflang="x-default" href="https://softglow-ai.com/comparisons/en/">')
    alt_block = "\n".join(alt_links)

    lang_bar_links = "\n".join(
        f'    <a href="{prefix}" class="lang-btn{" active" if prefix == url_prefix else ""}">{label}</a>'
        for _, prefix, _, label, *_ in LOCALES
    )

    html = f"""<!DOCTYPE html>
<html lang="{hreflang_self}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{hero_title} — SoftGlow</title>
<meta name="description" content="{hero_desc}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://softglow-ai.com{url_prefix}">
{alt_block}
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "CollectionPage", "name": "{hero_title}", "description": "{hero_desc}", "url": "https://softglow-ai.com{url_prefix}"}}</script>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;color:#2D3748;background:#fff;line-height:1.6}}
a{{color:#2563EB;text-decoration:none}}
a:hover{{text-decoration:underline}}
.nav{{position:sticky;top:0;z-index:100;background:rgba(255,255,255,0.95);backdrop-filter:blur(8px);border-bottom:1px solid #E2E8F0}}
.nav-inner{{max-width:1080px;margin:0 auto;padding:0 20px;display:flex;align-items:center;justify-content:space-between;height:52px}}
.nav-logo{{font-size:17px;font-weight:700;color:#2D3748;letter-spacing:-0.5px}}
.nav-logo span{{color:#2563EB}}
.nav-links{{display:flex;gap:16px;align-items:center}}
.nav-links a{{font-size:13px;color:#4A5568;font-weight:500}}
.nav-links a:hover{{color:#2563EB;text-decoration:none}}
.hero{{max-width:1080px;margin:0 auto;padding:40px 20px 20px;text-align:center}}
.hero h1{{font-size:26px;font-weight:700;color:#1A202C;margin-bottom:8px}}
.hero p{{font-size:15px;color:#718096;max-width:700px;margin:0 auto 20px}}
.lang-bar{{display:flex;gap:6px;flex-wrap:wrap;justify-content:center;margin:20px auto;max-width:800px}}
.lang-btn{{font-size:12px;padding:4px 12px;border-radius:20px;background:#F7FAFC;border:1px solid #E2E8F0;color:#718096}}
.lang-btn:hover{{background:#EBF5FF;border-color:#BEE3F8;text-decoration:none}}
.lang-btn.active{{background:#2563EB;color:#fff;border-color:#2563EB}}
.container{{max-width:1080px;margin:0 auto;padding:0 20px 40px}}
.tool-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:10px}}
.tool-card{{display:block;padding:12px 16px;background:#F7FAFC;border:1px solid #E2E8F0;border-radius:8px;font-size:14px;color:#2D3748;font-weight:500;transition:all 0.15s}}
.tool-card:hover{{background:#EBF5FF;border-color:#BEE3F8;text-decoration:none;transform:translateY(-1px)}}
.footer{{border-top:1px solid #E2E8F0;padding:24px 0;margin-top:40px}}
.footer-inner{{max-width:1080px;margin:0 auto;padding:0 20px;display:flex;flex-wrap:wrap;gap:16px;font-size:12px;color:#A0AEC0}}
.footer-inner a{{color:#718096}}
@media(max-width:768px){{ .hero h1{{font-size:20px}} .tool-grid{{grid-template-columns:1fr}} }}
</style>
<link rel="stylesheet" href="/js/cookie-consent.css">
</head>
<body>

<nav class="nav">
<div class="nav-inner">
  <a href="/" class="nav-logo">Soft<span>Glow</span></a>
  <div class="nav-links">
    <a href="/tools{url_prefix.replace('/comparisons', '')}">{nav_tools_text}</a>
    <a href="/">{nav_home_text}</a>
  </div>
</div>
</nav>

<div class="hero">
  <h1>{hero_title}</h1>
  <p>{hero_desc}</p>
  <div class="lang-bar">
{lang_bar_links}
  </div>
</div>

<div class="container">
<div class="tool-grid">
{cards}
</div>
</div>

<footer class="footer">
<div class="footer-inner">
  <a href="/about.html">About</a>
  <a href="/contact.html">Contact</a>
  <a href="/privacy.html">Privacy</a>
  <a href="/terms.html">Terms</a>
  <span style="margin-left:auto">© 2026 SoftGlow</span>
</div>
</footer>

<script src="/js/softglow-cookies.js" defer></script>
</body>
</html>
"""
    return html


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="真的寫入檔案，不加此參數只會dry-run")
    args = parser.parse_args()

    if not os.path.isdir(BASE_DIR):
        print(f"❌ 找不到資料夾：{BASE_DIR}")
        print("   請確認這支腳本放在 backend/ 底下（跟 frontend 資料夾同一層）")
        sys.exit(1)

    will_create = []
    will_skip = []

    for locale_folder, url_prefix, hreflang_self, lang_label, hero_title, hero_desc, nav_tools_text, nav_home_text in LOCALES:
        folder_path = os.path.join(BASE_DIR, locale_folder) if locale_folder else BASE_DIR
        index_path = os.path.join(folder_path, "index.html")

        if not os.path.isdir(folder_path):
            print(f"⚠️  跳過：資料夾不存在 {folder_path}")
            continue

        if os.path.isfile(index_path):
            will_skip.append((locale_folder or "zh-TW(根目錄)", "index.html 已存在，不覆蓋"))
            continue

        html_files = sorted(
            f for f in os.listdir(folder_path)
            if f.endswith(".html") and f != "index.html"
        )
        if not html_files:
            print(f"⚠️  跳過：{folder_path} 底下沒有任何文章檔案")
            continue

        articles = []
        for fn in html_files:
            title, desc = extract_meta(os.path.join(folder_path, fn))
            if not title:
                print(f"⚠️  {fn} 抓不到 <title>，先跳過這篇，其餘正常產生")
                continue
            # 去掉標題常見的" — SoftGlow"或": xxx Compared"這類尾綴，只取比較主題本身
            clean_title = re.split(r"\s*[—:]\s*", title)[0].strip()
            articles.append((fn, clean_title, desc))

        will_create.append((locale_folder or "zh-TW(根目錄)", index_path, len(articles)))

        if args.apply:
            html = build_index_html(locale_folder, url_prefix, hreflang_self, lang_label,
                                     hero_title, hero_desc, nav_tools_text, nav_home_text, articles)
            with open(index_path, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"✅ 已產生：{index_path}（{len(articles)}篇文章）")

    print("\n" + "=" * 50)
    if not args.apply:
        print("【DRY-RUN 模式，尚未真正寫入任何檔案】\n")
        print(f"會產生 {len(will_create)} 個 index.html：")
        for loc, path, n in will_create:
            print(f"  - {loc}：{path}（{n}篇文章）")
        if will_skip:
            print(f"\n會跳過 {len(will_skip)} 個（已存在，不覆蓋）：")
            for loc, reason in will_skip:
                print(f"  - {loc}：{reason}")
        print("\n確認上面清單沒問題後，加 --apply 參數才會真正寫入：")
        print("  python generate_comparisons_index.py --apply")
    else:
        print(f"【完成】共產生 {len(will_create)} 個 index.html")
        if will_skip:
            print(f"跳過 {len(will_skip)} 個（已存在，未覆蓋）")


if __name__ == "__main__":
    main()
