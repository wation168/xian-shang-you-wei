#!/usr/bin/env python3
"""
SoftGlow Knowledge Engine — Comparison Page Generator v1.0
Reads comparison JSON content and generates static HTML pages.
No API calls — pure local generation.

Usage:
    python generate_comparison_pages.py
    python generate_comparison_pages.py --slug dca-vs-lump-sum --langs en
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(BASE_DIR, "content", "comparisons")
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "comparisons")
LOCALE_PATH = os.path.join(BASE_DIR, "locale-config.json")
GENERATOR_VERSION = "1.0"

LANGS = ["zh-TW", "zh-CN", "en", "ja", "ko", "fr", "de", "es", "pt", "id"]
FRONTEND_URL = "https://softglow-ai.com"

LANG_NAMES = {
    "zh-TW": "繁體中文", "zh-CN": "简体中文", "en": "English",
    "ja": "日本語", "ko": "한국어", "de": "Deutsch",
    "fr": "Français", "es": "Español", "pt": "Português", "id": "Bahasa Indonesia",
}

# ── Comparison UI strings ──
COMP_UI = {
    "zh-TW": {
        "breadcrumb_comparisons": "比較分析",
        "section_intro": "概述", "section_table": "完整比較",
        "section_when_a": "何時選擇", "section_when_b": "何時選擇",
        "section_combined": "搭配使用策略", "section_faq": "常見問題",
        "section_verdict": "結論與建議", "vs_label": "vs",
        "try_tool": "立即試算", "related_comparisons": "相關比較",
        "related_tools": "相關工具", "related_blog": "教學文章",
        "disclaimer": "本頁面僅供教育參考，不構成任何投資建議。交易有風險，請根據自身情況做出判斷。",
        "last_updated": "最後更新",
        "search_placeholder": "搜尋工具、型態、文章…",
        "bm_title": "我的收藏", "bm_clear": "清除全部",
    },
    "zh-CN": {
        "breadcrumb_comparisons": "比较分析",
        "section_intro": "概述", "section_table": "完整比较",
        "section_when_a": "何时选择", "section_when_b": "何时选择",
        "section_combined": "搭配使用策略", "section_faq": "常见问题",
        "section_verdict": "结论与建议", "vs_label": "vs",
        "try_tool": "立即试算", "related_comparisons": "相关比较",
        "related_tools": "相关工具", "related_blog": "教学文章",
        "disclaimer": "本页面仅供教育参考，不构成任何投资建议。交易有风险，请根据自身情况做出判断。",
        "last_updated": "最后更新",
        "search_placeholder": "搜索工具、形态、文章…",
        "bm_title": "我的收藏", "bm_clear": "清除全部",
    },
    "en": {
        "breadcrumb_comparisons": "Comparisons",
        "section_intro": "Overview", "section_table": "Full Comparison",
        "section_when_a": "When to Choose", "section_when_b": "When to Choose",
        "section_combined": "How to Use Both Together", "section_faq": "Frequently Asked Questions",
        "section_verdict": "Verdict & Recommendation", "vs_label": "vs",
        "try_tool": "Try Calculator", "related_comparisons": "Related Comparisons",
        "related_tools": "Related Tools", "related_blog": "Blog Articles",
        "disclaimer": "This page is for educational purposes only and does not constitute investment advice. Trading involves risk; please make decisions based on your own judgment.",
        "last_updated": "Last Updated",
        "search_placeholder": "Search tools, patterns, articles…",
        "bm_title": "My Bookmarks", "bm_clear": "Clear All",
    },
    "ja": {
        "breadcrumb_comparisons": "比較分析",
        "section_intro": "概要", "section_table": "完全比較",
        "section_when_a": "選ぶべきタイミング", "section_when_b": "選ぶべきタイミング",
        "section_combined": "併用戦略", "section_faq": "よくある質問",
        "section_verdict": "結論と推奨", "vs_label": "vs",
        "try_tool": "計算ツールを試す", "related_comparisons": "関連比較",
        "related_tools": "関連ツール", "related_blog": "ブログ記事",
        "disclaimer": "このページは教育目的のみであり、投資アドバイスを構成するものではありません。取引にはリスクが伴います。ご自身の判断で決定してください。",
        "last_updated": "最終更新",
        "search_placeholder": "ツール、パターン、記事を検索…",
        "bm_title": "ブックマーク", "bm_clear": "すべて削除",
    },
    "ko": {
        "breadcrumb_comparisons": "비교 분석",
        "section_intro": "개요", "section_table": "전체 비교",
        "section_when_a": "선택 시기", "section_when_b": "선택 시기",
        "section_combined": "병행 전략", "section_faq": "자주 묻는 질문",
        "section_verdict": "결론 및 추천", "vs_label": "vs",
        "try_tool": "계산기 사용해보기", "related_comparisons": "관련 비교",
        "related_tools": "관련 도구", "related_blog": "블로그 글",
        "disclaimer": "이 페이지는 교육 목적으로만 제공되며 투자 조언을 구성하지 않습니다. 거래에는 위험이 따릅니다.",
        "last_updated": "최종 업데이트",
        "search_placeholder": "도구, 패턴, 기사 검색…",
        "bm_title": "북마크", "bm_clear": "모두 삭제",
    },
    "de": {
        "breadcrumb_comparisons": "Vergleiche",
        "section_intro": "Überblick", "section_table": "Vollständiger Vergleich",
        "section_when_a": "Wann wählen", "section_when_b": "Wann wählen",
        "section_combined": "Kombinierte Strategie", "section_faq": "Häufig gestellte Fragen",
        "section_verdict": "Fazit & Empfehlung", "vs_label": "vs",
        "try_tool": "Rechner ausprobieren", "related_comparisons": "Verwandte Vergleiche",
        "related_tools": "Verwandte Tools", "related_blog": "Blog-Artikel",
        "disclaimer": "Diese Seite dient ausschließlich Bildungszwecken und stellt keine Anlageberatung dar.",
        "last_updated": "Zuletzt aktualisiert",
        "search_placeholder": "Tools, Muster, Artikel suchen…",
        "bm_title": "Lesezeichen", "bm_clear": "Alle löschen",
    },
    "fr": {
        "breadcrumb_comparisons": "Comparaisons",
        "section_intro": "Aperçu", "section_table": "Comparaison complète",
        "section_when_a": "Quand choisir", "section_when_b": "Quand choisir",
        "section_combined": "Stratégie combinée", "section_faq": "Questions fréquentes",
        "section_verdict": "Verdict & Recommandation", "vs_label": "vs",
        "try_tool": "Essayer le calculateur", "related_comparisons": "Comparaisons associées",
        "related_tools": "Outils associés", "related_blog": "Articles du blog",
        "disclaimer": "Cette page est fournie à des fins éducatives uniquement et ne constitue pas un conseil en investissement.",
        "last_updated": "Dernière mise à jour",
        "search_placeholder": "Rechercher outils, patterns, articles…",
        "bm_title": "Favoris", "bm_clear": "Tout supprimer",
    },
    "es": {
        "breadcrumb_comparisons": "Comparaciones",
        "section_intro": "Resumen", "section_table": "Comparación completa",
        "section_when_a": "Cuándo elegir", "section_when_b": "Cuándo elegir",
        "section_combined": "Estrategia combinada", "section_faq": "Preguntas frecuentes",
        "section_verdict": "Veredicto y Recomendación", "vs_label": "vs",
        "try_tool": "Probar calculadora", "related_comparisons": "Comparaciones relacionadas",
        "related_tools": "Herramientas relacionadas", "related_blog": "Artículos del blog",
        "disclaimer": "Esta página tiene fines educativos únicamente y no constituye asesoramiento de inversión.",
        "last_updated": "Última actualización",
        "search_placeholder": "Buscar herramientas, patrones, artículos…",
        "bm_title": "Marcadores", "bm_clear": "Borrar todo",
    },
    "pt": {
        "breadcrumb_comparisons": "Comparações",
        "section_intro": "Visão geral", "section_table": "Comparação completa",
        "section_when_a": "Quando escolher", "section_when_b": "Quando escolher",
        "section_combined": "Estratégia combinada", "section_faq": "Perguntas frequentes",
        "section_verdict": "Veredito e Recomendação", "vs_label": "vs",
        "try_tool": "Experimentar calculadora", "related_comparisons": "Comparações relacionadas",
        "related_tools": "Ferramentas relacionadas", "related_blog": "Artigos do blog",
        "disclaimer": "Esta página é apenas para fins educacionais e não constitui aconselhamento de investimento.",
        "last_updated": "Última atualização",
        "search_placeholder": "Pesquisar ferramentas, padrões, artigos…",
        "bm_title": "Favoritos", "bm_clear": "Limpar tudo",
    },
    "id": {
        "breadcrumb_comparisons": "Perbandingan",
        "section_intro": "Ringkasan", "section_table": "Perbandingan Lengkap",
        "section_when_a": "Kapan Memilih", "section_when_b": "Kapan Memilih",
        "section_combined": "Strategi Gabungan", "section_faq": "Pertanyaan Umum",
        "section_verdict": "Kesimpulan & Rekomendasi", "vs_label": "vs",
        "try_tool": "Coba Kalkulator", "related_comparisons": "Perbandingan Terkait",
        "related_tools": "Alat Terkait", "related_blog": "Artikel Blog",
        "disclaimer": "Halaman ini hanya untuk tujuan edukasi dan bukan merupakan saran investasi.",
        "last_updated": "Terakhir diperbarui",
        "search_placeholder": "Cari alat, pola, artikel…",
        "bm_title": "Bookmark", "bm_clear": "Hapus Semua",
    },
}


def get_url(slug, lang):
    if lang == "zh-TW":
        return f"{FRONTEND_URL}/comparisons/{slug}.html"
    return f"{FRONTEND_URL}/comparisons/{lang}/{slug}.html"


def tools_url(lang):
    if lang == "zh-TW":
        return "/tools/"
    return f"/tools/{lang}/"


def patterns_index_url(lang):
    if lang == "zh-TW":
        return "/patterns/index.html"
    return f"/patterns/{lang}/index.html"


def build_hreflang(slug):
    tags = []
    for l in LANGS:
        url = get_url(slug, l)
        tags.append(f'<link rel="alternate" hreflang="{l.lower()}" href="{url}">')
    tags.append(f'<link rel="alternate" hreflang="x-default" href="{get_url(slug, "en")}">')
    return "\n".join(tags)


def build_faq_schema(faq_list):
    items = [{"@type": "Question", "name": f["q"],
              "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in faq_list]
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": items}, ensure_ascii=False)


def build_breadcrumb_schema(home_label, comp_label, title, slug, lang):
    comp_url = f"{FRONTEND_URL}/comparisons/" if lang == "zh-TW" else f"{FRONTEND_URL}/comparisons/{lang}/"
    return json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": home_label, "item": FRONTEND_URL + "/"},
        {"@type": "ListItem", "position": 2, "name": comp_label, "item": comp_url},
        {"@type": "ListItem", "position": 3, "name": title, "item": get_url(slug, lang)},
    ]}, ensure_ascii=False)


def build_article_schema(data, slug, lang):
    return json.dumps({"@context": "https://schema.org", "@type": "Article",
        "headline": data["seo"]["h1"], "description": data["seo"]["description"],
        "url": get_url(slug, lang),
        "publisher": {"@type": "Organization", "name": "SoftGlow", "url": FRONTEND_URL},
        "dateModified": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    }, ensure_ascii=False)


def build_comparison_table(table_data):
    headers = table_data.get("headers", ["", "", ""])
    rows = table_data.get("rows", [])
    html = '<div class="table-wrap"><table class="comp-table">\n<thead><tr>'
    for h in headers:
        html += f"<th>{h}</th>"
    html += "</tr></thead>\n<tbody>\n"
    for row in rows:
        html += "<tr>"
        for i, cell in enumerate(row):
            tag = "th" if i == 0 else "td"
            html += f"<{tag}>{cell}</{tag}>"
        html += "</tr>\n"
    html += "</tbody></table></div>"
    return html


def build_faq_html(faq_list):
    return "".join(f'<div class="faq-item">\n<div class="faq-q">{f["q"]}</div>\n<div class="faq-a">{f["a"]}</div>\n</div>\n' for f in faq_list)


def build_lang_buttons(slug, current_lang):
    return "\n".join(
        f'<a href="{get_url(slug, l)}" class="lang-btn{"  active" if l == current_lang else ""}">{LANG_NAMES[l]}</a>'
        for l in LANGS
    )


def build_lang_dropdown(slug, current_lang):
    options = []
    for l in LANGS:
        sel = " selected" if l == current_lang else ""
        options.append(f'<option value="{get_url(slug, l)}"{sel}>{LANG_NAMES[l]}</option>')
    return "\n".join(options)


def find_related(slug, all_slugs):
    return [s for s in all_slugs if s != slug][:5]


def build_related_html(slug, all_slugs, lang, ui):
    related = find_related(slug, all_slugs)
    cards = f'<div class="related-card"><h3>{ui["related_comparisons"]}</h3>\n'
    for rs in related:
        url = get_url(rs, lang)
        label = rs.replace("-", " ").title().replace(" Vs ", " vs ")
        cards += f'<a href="{url}" class="related-link">{label}</a>\n'
    cards += '</div>\n'

    meta = {}  # Will be passed in
    return cards


def generate_html(data, slug, lang, locale_ui, all_slugs):
    meta = data.get("_meta", {})
    seo = data["seo"]
    ui = COMP_UI.get(lang, COMP_UI["en"])
    name_a = meta.get("a", "A")
    name_b = meta.get("b", "B")
    tool_a = meta.get("tool_a", "")
    tool_b = meta.get("tool_b", "")

    nav_home = locale_ui.get("nav_home", "Home")
    nav_patterns = locale_ui.get("nav_patterns", "Patterns")
    nav_tools = locale_ui.get("nav_tools", "Tools")
    nav_blog = locale_ui.get("nav_blog", "Blog")
    breadcrumb_home = locale_ui.get("breadcrumb_home", "Home")

    canonical = get_url(slug, lang)
    hreflang = build_hreflang(slug)
    faq_schema = build_faq_schema(data.get("faq", []))
    bc_schema = build_breadcrumb_schema(breadcrumb_home, ui["breadcrumb_comparisons"], seo["h1"], slug, lang)
    art_schema = build_article_schema(data, slug, lang)
    table_html = build_comparison_table(data.get("comparison_table", {}))
    faq_html = build_faq_html(data.get("faq", []))
    lang_buttons = build_lang_buttons(slug, lang)
    lang_dropdown = build_lang_dropdown(slug, lang)
    build_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    build_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Related sidebar
    related = find_related(slug, all_slugs)
    related_links = ""
    for rs in related:
        url = get_url(rs, lang)
        label = rs.replace("-", " ").title().replace(" Vs ", " vs ")
        related_links += f'<a href="{url}" class="related-link">{label}</a>\n'

    # Tool links
    tool_links_html = ""
    if tool_a:
        tool_links_html += f'<a href="/tools/{tool_a}.html" class="tool-cta">{name_a} → {ui["try_tool"]}</a>\n'
    if tool_b:
        tool_links_html += f'<a href="/tools/{tool_b}.html" class="tool-cta">{name_b} → {ui["try_tool"]}</a>\n'

    # Sidebar tool links
    sidebar_tool_links = ""
    if tool_a:
        sidebar_tool_links += f'<a href="/tools/{tool_a}.html" class="related-link">{name_a}</a>\n'
    if tool_b:
        sidebar_tool_links += f'<a href="/tools/{tool_b}.html" class="related-link">{name_b}</a>\n'

    intro_html = data.get("intro", {}).get("html", "")
    when_a_text = data.get("when_to_use", {}).get("a", "")
    when_b_text = data.get("when_to_use", {}).get("b", "")
    combined_html = data.get("combined_strategy", {}).get("html", "")
    verdict_html = data.get("verdict", {}).get("html", "")

    html = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<link rel="preconnect" href="https://securepubads.g.doubleclick.net">
<link rel="preconnect" href="https://pagead2.googlesyndication.com">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{seo["title"]}</title>
<meta name="description" content="{seo["description"]}">
<meta name="robots" content="index, follow">
<meta name="sg-slug" content="{slug}">
<meta name="sg-type" content="comparison">
<meta name="sg-lang" content="{lang}">
<link rel="canonical" href="{canonical}">
{hreflang}
<link rel="stylesheet" href="/common/softglow-common.css">
<script type="application/ld+json">{art_schema}</script>
<script type="application/ld+json">{bc_schema}</script>
<script type="application/ld+json">{faq_schema}</script>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;color:#2D3748;background:#fff;line-height:1.7;-webkit-font-smoothing:antialiased}}
a{{color:#2563EB;text-decoration:none}}
a:hover{{text-decoration:underline}}

.nav{{position:sticky;top:0;z-index:100;background:rgba(255,255,255,0.95);backdrop-filter:blur(8px);border-bottom:1px solid #E2E8F0}}
.nav-inner{{max-width:1080px;margin:0 auto;padding:0 20px;display:flex;align-items:center;justify-content:space-between;height:52px}}
.nav-logo{{font-size:17px;font-weight:700;color:#2D3748;letter-spacing:-0.5px}}
.nav-logo span{{color:#2563EB}}
.nav-links{{display:flex;gap:16px;align-items:center}}
.nav-links a{{font-size:13px;color:#4A5568;font-weight:500}}
.nav-links a:hover{{color:#2563EB;text-decoration:none}}
.nav-actions{{display:flex;gap:4px;align-items:center}}
.act-btn{{background:none;border:none;cursor:pointer;padding:6px;border-radius:6px;display:flex;align-items:center}}
.act-btn svg{{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}}
.act-btn.primary{{color:#2563EB}}.act-btn.primary:hover{{background:#EBF5FF}}
.act-btn.secondary{{color:#A0AEC0}}.act-btn.secondary:hover{{background:#F7FAFC;color:#4A5568}}
.lang-select{{font-size:12px;padding:4px 8px;border:1px solid #E2E8F0;border-radius:6px;background:#fff;color:#4A5568;cursor:pointer;margin-left:4px}}
.breadcrumb{{max-width:1080px;margin:0 auto;padding:12px 20px;font-size:13px;color:#A0AEC0}}
.breadcrumb a{{color:#718096}}

.container{{max-width:1080px;margin:0 auto;padding:0 20px}}
.layout{{display:grid;grid-template-columns:1fr 300px;gap:32px;align-items:start}}

.hero{{background:linear-gradient(135deg,#EBF5FF 0%,#F7FAFC 100%);border:1px solid #BEE3F8;border-radius:16px;padding:28px 32px;margin-bottom:24px}}
.hero h1{{font-size:26px;font-weight:800;color:#1A202C;margin-bottom:8px;line-height:1.3}}
.hero-subtitle{{font-size:15px;color:#4A5568;margin-bottom:16px}}
.hero-badges{{display:flex;gap:8px;flex-wrap:wrap}}
.badge{{font-size:12px;padding:4px 12px;border-radius:20px;background:#fff;border:1px solid #E2E8F0;color:#4A5568;font-weight:500}}
.badge-a{{background:#DBEAFE;border-color:#93C5FD;color:#1E40AF}}
.badge-b{{background:#FEF3C7;border-color:#FCD34D;color:#92400E}}

.section{{margin-bottom:32px}}
.section h2{{font-size:20px;font-weight:700;color:#1A202C;margin-bottom:14px;padding-bottom:8px;border-bottom:2px solid #E2E8F0}}
.content p{{margin-bottom:14px;color:#4A5568;line-height:1.8;font-size:15px}}
.content strong{{color:#2D3748}}

.table-wrap{{overflow-x:auto;margin:16px 0;border-radius:12px;border:1px solid #E2E8F0}}
.comp-table{{width:100%;border-collapse:collapse;font-size:14px}}
.comp-table th{{text-align:left;padding:12px 16px;background:#F7FAFC;font-weight:600;color:#2D3748;border-bottom:1px solid #E2E8F0}}
.comp-table td{{padding:12px 16px;border-bottom:1px solid #EDF2F7;color:#4A5568;vertical-align:top}}
.comp-table thead th{{background:#2563EB;color:#fff;font-size:13px;text-transform:uppercase;letter-spacing:0.5px}}
.comp-table thead th:first-child{{border-radius:12px 0 0 0}}
.comp-table thead th:last-child{{border-radius:0 12px 0 0}}
.comp-table tbody tr:hover{{background:#F7FAFC}}
.comp-table tbody th{{background:#F7FAFC;font-weight:600;color:#2D3748;min-width:120px}}

.when-cards{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:16px 0}}
.when-card{{padding:20px;border-radius:12px;border:1px solid #E2E8F0;font-size:14px;color:#4A5568;line-height:1.7}}
.when-card-a{{background:#EFF6FF;border-color:#BFDBFE}}
.when-card-b{{background:#FFFBEB;border-color:#FDE68A}}
.when-card h3{{font-size:16px;font-weight:600;margin:0 0 8px;color:#1A202C}}

.tool-cta{{display:inline-block;padding:10px 24px;margin:4px 8px 4px 0;background:#2563EB;color:#fff!important;border-radius:8px;font-size:14px;font-weight:600;text-decoration:none!important}}
.tool-cta:hover{{background:#1D4ED8}}

.ad-slot{{background:#F7FAFC;border:1px dashed #CBD5E0;border-radius:8px;min-height:250px;display:flex;align-items:center;justify-content:center;color:#A0AEC0;font-size:12px;margin-bottom:20px}}

.sidebar{{position:sticky;top:68px}}
.related-card{{background:#F7FAFC;border:1px solid #E2E8F0;border-radius:12px;padding:20px;margin-bottom:16px}}
.related-card h3{{font-size:15px;font-weight:600;margin-bottom:12px;color:#1A202C}}
.related-link{{display:block;padding:7px 0;border-bottom:1px solid #EDF2F7;font-size:13px;color:#2563EB}}
.related-link:last-child{{border-bottom:none}}
.related-link:hover{{text-decoration:none;color:#1D4ED8}}

.faq-item{{border-bottom:1px solid #E2E8F0;padding:14px 0}}
.faq-q{{font-size:15px;font-weight:600;color:#2D3748;cursor:pointer;display:flex;justify-content:space-between;align-items:center}}
.faq-q::after{{content:"＋";font-size:18px;color:#A0AEC0;transition:transform 0.2s}}
.faq-item.open .faq-q::after{{content:"－"}}
.faq-a{{font-size:14px;color:#718096;line-height:1.7;max-height:0;overflow:hidden;transition:max-height 0.3s,padding 0.3s}}
.faq-item.open .faq-a{{max-height:500px;padding-top:10px}}

.disclaimer{{background:#FFFBEB;border:1px solid #FDE68A;border-radius:8px;padding:12px 16px;font-size:12px;color:#92400E;line-height:1.6;margin:24px 0}}
.lang-bar{{display:flex;gap:6px;flex-wrap:wrap;margin:20px 0}}
.lang-btn{{font-size:12px;padding:4px 12px;border-radius:20px;background:#F7FAFC;border:1px solid #E2E8F0;color:#718096}}
.lang-btn:hover{{background:#EBF5FF;border-color:#BEE3F8;text-decoration:none}}
.lang-btn.active{{background:#2563EB;color:#fff;border-color:#2563EB}}
.mobile-related{{display:none}}

.footer{{border-top:1px solid #E2E8F0;padding:24px 0;margin-top:40px}}
.footer-inner{{max-width:1080px;margin:0 auto;padding:0 20px;display:flex;flex-wrap:wrap;gap:16px;font-size:12px;color:#A0AEC0}}
.footer-inner a{{color:#718096}}

@media(max-width:768px){{
  .layout{{grid-template-columns:1fr}}
  .sidebar{{position:static;display:none}}
  .mobile-related{{display:block}}
  .hero{{padding:20px}}
  .hero h1{{font-size:20px}}
  .when-cards{{grid-template-columns:1fr}}
  .comp-table{{font-size:13px}}
  .comp-table th,.comp-table td{{padding:10px 12px}}
  .nav-links{{gap:10px}}
  .lang-select{{display:none}}
}}
</style>
</head>
<body>

<nav class="nav">
<div class="nav-inner">
  <a href="/" class="nav-logo">Soft<span>Glow</span></a>
  <div class="nav-links">
    <a href="{tools_url(lang)}">{nav_tools}</a>
    <a href="{patterns_index_url(lang)}">{nav_patterns}</a>
    <a href="/blog/">{nav_blog}</a>
    <a href="/">{nav_home}</a>
  </div>
  <div class="nav-actions">
    <select class="lang-select" onchange="if(this.value)window.location.href=this.value">
      {lang_dropdown}
    </select>
    <button class="act-btn primary" onclick="sgOpenSearch()" title="Search"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></button>
    <button class="act-btn primary" id="sgBmBtn" onclick="sgToggleBookmark()" ondblclick="sgToggleBmPanel()" title="Bookmark"><svg viewBox="0 0 24 24"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg></button>
    <button class="act-btn secondary" onclick="sgShare()" title="Share"><svg viewBox="0 0 24 24"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg></button>
    <button class="act-btn secondary" onclick="sgPrint()" title="Print"><svg viewBox="0 0 24 24"><path d="M6 9V2h12v7"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg></button>
  </div>
</div>
</nav>

<div class="breadcrumb">
  <a href="/">{breadcrumb_home}</a> › <a href="/comparisons/">{ui["breadcrumb_comparisons"]}</a> › {seo["h1"]}
</div>

<div class="container">
<div class="layout">

<div class="main">

  <div class="hero">
    <h1>{seo["h1"]}</h1>
    <p class="hero-subtitle">{seo["description"]}</p>
    <div class="hero-badges">
      <span class="badge badge-a">{name_a}</span>
      <span class="badge">{ui["vs_label"]}</span>
      <span class="badge badge-b">{name_b}</span>
    </div>
  </div>

  <div class="section">
    <h2>{ui["section_intro"]}</h2>
    <div class="content">{{intro_html}}</div>
  </div>

  <div class="ad-slot" id="ad-1" aria-hidden="true"></div>

  <div class="section">
    <h2>{ui["section_table"]}</h2>
    {table_html}
  </div>

  <div class="section">
    <div class="when-cards">
      <div class="when-card when-card-a">
        <h3>{ui["section_when_a"]} {name_a}</h3>
        <p>{{when_a_text}}</p>
      </div>
      <div class="when-card when-card-b">
        <h3>{ui["section_when_b"]} {name_b}</h3>
        <p>{{when_b_text}}</p>
      </div>
    </div>
  </div>

  <div class="ad-slot" id="ad-2" aria-hidden="true"></div>

  <div class="section">
    <h2>{ui["section_combined"]}</h2>
    <div class="content">{{combined_html}}</div>
  </div>

  <div class="section" style="text-align:center;margin:24px 0">
    {tool_links_html}
  </div>

  <div class="ad-slot" id="ad-3" aria-hidden="true"></div>

  <div class="section">
    <h2>{ui["section_faq"]}</h2>
    {faq_html}
  </div>

  <div class="ad-slot" id="ad-4" aria-hidden="true"></div>

  <div class="section">
    <h2>{ui["section_verdict"]}</h2>
    <div class="content">{{verdict_html}}</div>
  </div>

  <div class="mobile-related">
    <div class="related-card">
      <h3>{ui["related_tools"]}</h3>
      {sidebar_tool_links}
    </div>
    <div class="related-card">
      <h3>{ui["related_comparisons"]}</h3>
      {related_links}
    </div>
  </div>

  <div class="disclaimer">
    {ui["disclaimer"]} — {ui["last_updated"]}: {build_date}
  </div>

  <div class="lang-bar">
    {lang_buttons}
  </div>

</div>

<aside class="sidebar">
  <div class="ad-slot" id="ad-side" aria-hidden="true"></div>
  <div class="related-card">
    <h3>{ui["related_tools"]}</h3>
    {sidebar_tool_links}
  </div>
  <div class="related-card">
    <h3>{ui["related_comparisons"]}</h3>
    {related_links}
  </div>
</aside>

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

<!-- Search Overlay -->
<div class="search-overlay" id="sgSearchOverlay">
  <div class="search-box">
    <div class="search-input-wrap">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
      <input class="search-input" id="sgSearchInput" type="text" placeholder="{ui["search_placeholder"]}" autocomplete="off">
    </div>
    <div class="search-results" id="sgSearchResults"></div>
  </div>
</div>

<!-- Bookmark Panel -->
<div class="bm-panel" id="sgBmPanel">
  <div class="bm-header">
    <h3>{ui["bm_title"]}</h3>
    <button class="bm-clear" onclick="window._sgClearBm()">{ui["bm_clear"]}</button>
  </div>
  <div class="bm-list" id="sgBmList"></div>
</div>

<script src="/common/softglow-common.js"></script>
<script>
document.querySelectorAll('.faq-q').forEach(function(q){{
  q.addEventListener('click',function(){{this.parentElement.classList.toggle('open');}});
}});
</script>

<!-- AdSense delayed load: 2s after page load -->
<script>
setTimeout(function(){{
  var s=document.createElement('script');
  s.src='https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1768270548115739';
  s.async=true;s.crossOrigin='anonymous';
  document.head.appendChild(s);
}},2000);
</script>

<!-- Generator Metadata
version: {GENERATOR_VERSION}
build_time: {build_time}
model: {meta.get("model", "unknown")}
slug: {slug}
lang: {lang}
-->
</body>
</html>'''
    return html


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", help="Generate specific slug only")
    parser.add_argument("--langs", help="Comma-separated languages", default=",".join(LANGS))
    args = parser.parse_args()

    langs = [l.strip() for l in args.langs.split(",")]

    with open(LOCALE_PATH, "r", encoding="utf-8") as f:
        locale_config = json.load(f)

    all_slugs = sorted(set(
        fn.rsplit("_", 1)[0]
        for fn in os.listdir(CONTENT_DIR)
        if fn.endswith(".json") and "_" in fn
    ))

    slugs = [args.slug] if args.slug else all_slugs

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for l in langs:
        if l != "zh-TW":
            os.makedirs(os.path.join(OUTPUT_DIR, l), exist_ok=True)

    print(f"SoftGlow Knowledge Engine — Comparison Page Generator v{GENERATOR_VERSION}")
    print(f"{'='*60}")
    print(f"Comparisons: {len(slugs)} | Languages: {len(langs)}")
    print(f"Max pages: {len(slugs) * len(langs)}")
    print(f"Output: {OUTPUT_DIR}")

    generated = 0
    skipped = 0
    errors = 0

    for slug in slugs:
        for lang in langs:
            content_path = os.path.join(CONTENT_DIR, f"{slug}_{lang}.json")
            if not os.path.exists(content_path):
                skipped += 1
                continue

            try:
                with open(content_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                locale_ui = locale_config.get(lang, locale_config.get("en", {})).get("ui", {})
                html = generate_html(data, slug, lang, locale_ui, all_slugs)

                if lang == "zh-TW":
                    out_path = os.path.join(OUTPUT_DIR, f"{slug}.html")
                else:
                    out_path = os.path.join(OUTPUT_DIR, lang, f"{slug}.html")

                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(html)

                print(f"  ✅ {slug}_{lang}")
                generated += 1
            except Exception as e:
                print(f"  ❌ {slug}_{lang}: {e}")
                errors += 1

    print(f"{'='*60}")
    print(f"Generated: {generated} | Skipped: {skipped} | Errors: {errors}")
    print(f"Output directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
