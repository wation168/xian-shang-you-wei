#!/usr/bin/env python3
"""
SoftGlow Knowledge Engine — Pattern Page Generator
===================================================
Reads: pattern-catalog.json + locale-config.json + content/{slug}_{lang}.json + pattern-template.html
Outputs: static HTML pages in output/patterns/

Usage:
    python generate_patterns.py                          # all patterns × all languages
    python generate_patterns.py --slug bullish-engulfing # one pattern × all languages
    python generate_patterns.py --slug bullish-engulfing --langs zh-TW,en  # one pattern × specific langs

URL structure:
    zh-TW: /patterns/{slug}.html  (root level)
    Others: /patterns/{lang}/{slug}.html
"""

import json
import os
import sys
import argparse
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CATALOG_PATH = os.path.join(BASE_DIR, "pattern-catalog.json")
LOCALE_PATH = os.path.join(BASE_DIR, "locale-config.json")
TEMPLATE_PATH = os.path.join(BASE_DIR, "pattern-template.html")
CONTENT_DIR = os.path.join(BASE_DIR, "content")
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "patterns")

SITE_URL = "https://softglow-ai.com"
ALL_LANGS = ["zh-TW", "en", "ja", "ko", "de", "fr", "es", "pt", "id", "zh-CN"]
GENERATOR_VERSION = "1.0"

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_template():
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()

# ---------------------------------------------------------------------------
# SVG Renderer — uses candle_data from catalog + locale colors
# ---------------------------------------------------------------------------
def render_svg(candle_data, locale_cfg):
    """Generate SVG candlestick chart from standardized candle_data."""
    colors = locale_cfg["candle_colors"]
    
    svg_parts = []
    svg_parts.append('<svg viewBox="0 0 180 140" xmlns="http://www.w3.org/2000/svg">')
    svg_parts.append('<rect width="180" height="140" fill="#F7FAFC" rx="8"/>')
    
    n = len(candle_data)
    candle_width = 36
    gap = 20
    total_w = n * candle_width + (n - 1) * gap
    start_x = (180 - total_w) / 2
    
    # Normalize values to SVG coordinates (y-axis inverted)
    all_vals = []
    for c in candle_data:
        all_vals.extend([c["high"], c["low"]])
    v_min = min(all_vals)
    v_max = max(all_vals)
    v_range = v_max - v_min if v_max != v_min else 1
    
    def y(val):
        return 15 + (1 - (val - v_min) / v_range) * 100
    
    for i, c in enumerate(candle_data):
        cx = start_x + i * (candle_width + gap) + candle_width / 2
        fill = colors["bullish"] if c["type"] == "bullish" else colors["bearish"]
        
        o = c["open"]
        cl = c["close"]
        hi = c["high"]
        lo = c["low"]
        
        body_top = y(max(o, cl))
        body_bot = y(min(o, cl))
        body_h = body_bot - body_top
        if body_h < 3:
            body_h = 3
        
        # Wick (high to low)
        svg_parts.append(f'<line x1="{cx}" y1="{y(hi)}" x2="{cx}" y2="{y(lo)}" stroke="{fill}" stroke-width="2"/>')
        # Body
        svg_parts.append(f'<rect x="{cx - candle_width/2}" y="{body_top}" width="{candle_width}" height="{body_h}" fill="{fill}" rx="2"/>')
        # Label
        if c.get("label"):
            svg_parts.append(f'<text x="{cx}" y="{y(lo) + 16}" text-anchor="middle" font-size="11" fill="#718096" font-weight="500">{c["label"]}</text>')
    
    svg_parts.append('</svg>')
    return "\n".join(svg_parts)

# ---------------------------------------------------------------------------
# Build hreflang tags
# ---------------------------------------------------------------------------
def build_hreflang(slug, available_langs):
    tags = []
    for lang in available_langs:
        url = pattern_url(slug, lang)
        tags.append(f'<link rel="alternate" hreflang="{lang}" href="{url}"/>')
    # x-default = en
    tags.append(f'<link rel="alternate" hreflang="x-default" href="{pattern_url(slug, "en")}"/>')
    return "\n".join(tags)

# ---------------------------------------------------------------------------
# URL helpers
# ---------------------------------------------------------------------------
def pattern_url(slug, lang):
    if lang == "zh-TW":
        return f"{SITE_URL}/patterns/{slug}.html"
    return f"{SITE_URL}/patterns/{lang}/{slug}.html"

def pattern_path(slug, lang):
    """File system path for output."""
    if lang == "zh-TW":
        return os.path.join(OUTPUT_DIR, f"{slug}.html")
    return os.path.join(OUTPUT_DIR, lang, f"{slug}.html")

def tools_url(lang):
    if lang == "zh-TW":
        return "/tools/"
    return f"/tools/{lang}/"

def patterns_index_url(lang):
    if lang == "zh-TW":
        return "/patterns/index.html"
    return f"/patterns/{lang}.html"

def tool_link(tool_slug, lang):
    if lang == "zh-TW":
        return f"/tools/{tool_slug}.html"
    return f"/tools/{lang}/{tool_slug}.html"

def blog_link(blog_slug, lang):
    if lang == "zh-TW":
        return f"/blog/{blog_slug}.html"
    return f"/blog/{lang}/{blog_slug}.html"

def pattern_link(pattern_slug, lang):
    if lang == "zh-TW":
        return f"/patterns/{pattern_slug}.html"
    return f"/patterns/{lang}/{pattern_slug}.html"

# ---------------------------------------------------------------------------
# Schema JSON-LD builders
# ---------------------------------------------------------------------------
def build_article_schema(slug, lang, content, catalog_entry):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": content["seo"]["h1"],
        "description": content["seo"]["description"],
        "author": {"@type": "Organization", "name": "SoftGlow"},
        "publisher": {
            "@type": "Organization",
            "name": "SoftGlow",
            "url": SITE_URL
        },
        "datePublished": "2026-07-11",
        "dateModified": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "mainEntityOfPage": pattern_url(slug, lang),
        "image": f"{SITE_URL}/images/patterns/{slug}.svg"
    }, ensure_ascii=False)

def build_breadcrumb_schema(slug, lang, locale_cfg, content):
    ui = locale_cfg["ui"]
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": ui["breadcrumb_home"], "item": SITE_URL},
            {"@type": "ListItem", "position": 2, "name": ui["breadcrumb_patterns"], "item": f"{SITE_URL}{patterns_index_url(lang)}"},
            {"@type": "ListItem", "position": 3, "name": content["seo"]["h1"]}
        ]
    }, ensure_ascii=False)

def build_faq_schema(faq_items):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item["q"],
                "acceptedAnswer": {"@type": "Answer", "text": item["a"]}
            }
            for item in faq_items
        ]
    }, ensure_ascii=False)

# ---------------------------------------------------------------------------
# Build related HTML (shared between sidebar and mobile)
# ---------------------------------------------------------------------------
def build_related_html(catalog_entry, lang, locale_cfg, all_catalog):
    ui = locale_cfg["ui"]
    parts = []
    
    # Related patterns
    rp = catalog_entry.get("related_patterns", [])
    if rp:
        parts.append(f'<div class="related-card"><h3>{ui["related_patterns"]}</h3>')
        for p_slug in rp:
            # Try to get localized name from content JSON, fallback to slug
            label = _get_pattern_name(p_slug, lang)
            parts.append(f'<a class="related-link" href="{pattern_link(p_slug, lang)}">{label}</a>')
        parts.append('</div>')
    
    # Related tools
    rt = catalog_entry.get("related_tools", [])
    if rt:
        parts.append(f'<div class="related-card"><h3>{ui["related_tools"]}</h3>')
        for t_slug in rt:
            label = t_slug.replace("-", " ").title()
            parts.append(f'<a class="related-link" href="{tool_link(t_slug, lang)}">{label}</a>')
        parts.append('</div>')
    
    # Related blog
    rb = catalog_entry.get("related_blog", [])
    if rb:
        parts.append(f'<div class="related-card"><h3>{ui["related_blog"]}</h3>')
        for b_slug in rb:
            label = b_slug.replace("-", " ").title()
            parts.append(f'<a class="related-link" href="{blog_link(b_slug, lang)}">{label}</a>')
        parts.append('</div>')
    
    return "\n".join(parts)

def _get_pattern_name(slug, lang):
    """Try to load pattern name from content JSON, fallback to formatted slug."""
    content_path = os.path.join(CONTENT_DIR, f"{slug}_{lang}.json")
    if os.path.exists(content_path):
        try:
            data = load_json(content_path)
            return data["seo"]["h1"]
        except Exception:
            pass
    return slug.replace("-", " ").title()

# ---------------------------------------------------------------------------
# Build lang buttons
# ---------------------------------------------------------------------------
def build_lang_buttons(slug, current_lang, available_langs, locale_configs):
    buttons = []
    for lang in available_langs:
        cfg = locale_configs.get(lang, {})
        name = cfg.get("lang_name", lang)
        url = pattern_url(slug, lang)
        cls = "lang-btn active" if lang == current_lang else "lang-btn"
        buttons.append(f'<a class="{cls}" href="{url}">{name}</a>')
    return "\n".join(buttons)

# ---------------------------------------------------------------------------
# Build mistakes HTML
# ---------------------------------------------------------------------------
def build_mistakes_html(mistakes):
    parts = []
    for m in mistakes.get("items", []):
        parts.append(f'<div class="mistake-item"><h3>{m["title"]}</h3><p>{m["text"]}</p></div>')
    return "\n".join(parts)

# ---------------------------------------------------------------------------
# Build checklist HTML
# ---------------------------------------------------------------------------
def build_checklist_html(checklist):
    parts = []
    for item in checklist.get("items", []):
        parts.append(f"<li>{item}</li>")
    return "\n".join(parts)

# ---------------------------------------------------------------------------
# Build FAQ HTML
# ---------------------------------------------------------------------------
def build_faq_html(faq_items):
    parts = []
    for item in faq_items:
        parts.append(f'<div class="faq-item"><div class="faq-q">{item["q"]}</div><div class="faq-a">{item["a"]}</div></div>')
    return "\n".join(parts)

# ---------------------------------------------------------------------------
# Resolve locale-aware values
# ---------------------------------------------------------------------------
def resolve_signal_value(signal, locale_cfg):
    ui = locale_cfg["ui"]
    mapping = {"bullish": ui["signal_bullish"], "bearish": ui["signal_bearish"], "neutral": ui["signal_neutral"]}
    return mapping.get(signal, signal)

def resolve_reliability_value(reliability, locale_cfg):
    ui = locale_cfg["ui"]
    mapping = {"high": ui["reliability_high"], "medium": ui["reliability_medium"], "low": ui["reliability_low"]}
    return mapping.get(reliability, reliability)

def resolve_difficulty_value(difficulty, locale_cfg):
    ui = locale_cfg["ui"]
    mapping = {
        "beginner": ui["difficulty_beginner"],
        "intermediate": ui["difficulty_intermediate"],
        "advanced": ui["difficulty_advanced"]
    }
    return mapping.get(difficulty, difficulty)

def resolve_market_values(markets, locale_cfg):
    ui = locale_cfg["ui"]
    mapping = {
        "downtrend": ui["market_downtrend"],
        "uptrend": ui["market_uptrend"],
        "ranging": ui["market_ranging"],
        "breakout": ui["market_breakout"],
        "pullback": ui["market_pullback"]
    }
    return ", ".join(mapping.get(m, m) for m in markets)

# ---------------------------------------------------------------------------
# Main generation
# ---------------------------------------------------------------------------
def generate_page(slug, lang, catalog, locale_configs, template):
    catalog_entry = catalog[slug]
    locale_cfg = locale_configs[lang]
    ui = locale_cfg["ui"]
    
    # Load content JSON
    content_path = os.path.join(CONTENT_DIR, f"{slug}_{lang}.json")
    if not os.path.exists(content_path):
        print(f"  ⚠ SKIP {slug}_{lang} — content JSON not found")
        return False
    
    content = load_json(content_path)
    
    # Determine which languages have content for this slug
    available_langs = []
    for l in ALL_LANGS:
        if os.path.exists(os.path.join(CONTENT_DIR, f"{slug}_{l}.json")):
            available_langs.append(l)
    
    now = datetime.now(timezone.utc)
    build_date = now.strftime("%Y-%m-%d")
    build_time = now.isoformat()
    
    # Build all replacements
    replacements = {
        "{{LANG_CODE}}": locale_cfg["lang_code"],
        "{{SEO_TITLE}}": content["seo"]["title"],
        "{{SEO_DESC}}": content["seo"]["description"],
        "{{CANONICAL_URL}}": pattern_url(slug, lang),
        "{{HREFLANG_TAGS}}": build_hreflang(slug, available_langs),
        "{{SCHEMA_ARTICLE}}": build_article_schema(slug, lang, content, catalog_entry),
        "{{SCHEMA_BREADCRUMB}}": build_breadcrumb_schema(slug, lang, locale_cfg, content),
        "{{SCHEMA_FAQ}}": build_faq_schema(content["faq"]),
        
        # Nav
        "{{TOOLS_URL}}": tools_url(lang),
        "{{NAV_TOOLS}}": ui["nav_tools"],
        "{{PATTERNS_INDEX_URL}}": patterns_index_url(lang),
        "{{NAV_PATTERNS}}": ui["nav_patterns"],
        "{{NAV_BLOG}}": ui["nav_blog"],
        "{{NAV_HOME}}": ui["nav_home"],
        
        # Breadcrumb
        "{{BREADCRUMB_HOME}}": ui["breadcrumb_home"],
        "{{BREADCRUMB_PATTERNS}}": ui["breadcrumb_patterns"],
        "{{H1}}": content["seo"]["h1"],
        
        # Hero
        "{{HERO_ONE_LINER}}": content["hero"]["one_liner"],
        "{{SIGNAL}}": catalog_entry["signal"],
        "{{SIGNAL_LABEL}}": ui["signal_label"],
        "{{SIGNAL_VALUE}}": resolve_signal_value(catalog_entry["signal"], locale_cfg),
        "{{RELIABILITY}}": catalog_entry["reliability"],
        "{{RELIABILITY_LABEL}}": ui["reliability_label"],
        "{{RELIABILITY_VALUE}}": resolve_reliability_value(catalog_entry["reliability"], locale_cfg),
        "{{DIFFICULTY_LABEL}}": ui["difficulty_label"],
        "{{DIFFICULTY_VALUE}}": resolve_difficulty_value(catalog_entry["difficulty"], locale_cfg),
        "{{CANDLES_LABEL}}": ui["candles_label"],
        "{{CANDLES}}": str(catalog_entry["candles"]),
        "{{BEST_MARKET_LABEL}}": ui["best_market_label"],
        "{{BEST_MARKET_VALUES}}": resolve_market_values(catalog_entry["best_market"], locale_cfg),
        "{{SVG_CANDLES}}": render_svg(catalog_entry["candle_data"], locale_cfg),
        
        # Sections
        "{{SECTION_SUMMARY}}": ui["section_summary"],
        "{{SUMMARY_TEXT}}": content["summary"]["text"],
        "{{SECTION_STRUCTURE}}": ui["section_structure"],
        "{{STRUCTURE_HTML}}": content["structure"]["html"],
        "{{SECTION_PSYCHOLOGY}}": ui["section_psychology"],
        "{{PSYCHOLOGY_HTML}}": content["psychology"]["html"],
        "{{SECTION_TRADING}}": ui["section_trading"],
        "{{ENTRY_LABEL}}": ui["entry_label"],
        "{{STOP_LOSS_LABEL}}": ui["stop_loss_label"],
        "{{TAKE_PROFIT_LABEL}}": ui["take_profit_label"],
        "{{INVALIDATION_LABEL}}": ui["invalidation_label"],
        "{{RULE_ENTRY}}": content["trading_rules"]["entry"],
        "{{RULE_STOP_LOSS}}": content["trading_rules"]["stop_loss"],
        "{{RULE_TAKE_PROFIT}}": content["trading_rules"]["take_profit"],
        "{{RULE_INVALIDATION}}": content["trading_rules"]["invalidation"],
        "{{SECTION_CONFIRMATION}}": ui["section_confirmation"],
        "{{CONFIRMATION_HTML}}": content["confirmation"]["html"],
        "{{SECTION_MISTAKES}}": ui["section_mistakes"],
        "{{MISTAKES_HTML}}": build_mistakes_html(content["mistakes"]),
        "{{SECTION_CHECKLIST}}": ui["section_checklist"],
        "{{CHECKLIST_HTML}}": build_checklist_html(content["checklist"]),
        "{{SECTION_FAQ}}": ui["section_faq"],
        "{{FAQ_HTML}}": build_faq_html(content["faq"]),
        
        # Related
        "{{RELATED_HTML}}": build_related_html(catalog_entry, lang, locale_cfg, catalog),
        
        # Disclaimer
        "{{DISCLAIMER}}": ui["disclaimer"],
        "{{LAST_UPDATED}}": ui["last_updated"],
        "{{BUILD_DATE}}": build_date,
        
        # Lang buttons
        "{{LANG_BUTTONS}}": build_lang_buttons(slug, lang, available_langs, locale_configs),
        
        # Search & Bookmark UI strings
        "{{SEARCH_PLACEHOLDER}}": _search_placeholder(lang),
        "{{BM_TITLE}}": _bm_title(lang),
        "{{BM_CLEAR}}": _bm_clear(lang),
        
        # Metadata
        "{{GENERATOR_VERSION}}": GENERATOR_VERSION,
        "{{BUILD_TIME}}": build_time,
        "{{MODEL}}": content.get("_meta", {}).get("model", "unknown"),
        "{{SLUG}}": slug,
        "{{LANG}}": lang,
    }
    
    html = template
    for key, value in replacements.items():
        html = html.replace(key, str(value))
    
    # Write output
    out_path = pattern_path(slug, lang)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    return True

# ---------------------------------------------------------------------------
# Quality check
# ---------------------------------------------------------------------------
def quality_check(slug, lang):
    """Basic quality checks on generated HTML."""
    out_path = pattern_path(slug, lang)
    if not os.path.exists(out_path):
        return ["File not generated"]
    
    with open(out_path, "r", encoding="utf-8") as f:
        html = f.read()
    
    issues = []
    
    # Check for remaining placeholders
    import re
    remaining = re.findall(r'\{\{[A-Z_]+\}\}', html)
    if remaining:
        issues.append(f"Unreplaced placeholders: {remaining}")
    
    # Check file size (should be > 10KB for a proper page)
    size_kb = len(html.encode("utf-8")) / 1024
    if size_kb < 5:
        issues.append(f"File too small: {size_kb:.1f}KB")
    
    # Check required elements
    required = ["FAQPage", "BreadcrumbList", "Article", "canonical", "hreflang"]
    for req in required:
        if req not in html:
            issues.append(f"Missing: {req}")
    
    return issues

# ---------------------------------------------------------------------------
# Search & Bookmark i18n strings
# ---------------------------------------------------------------------------
def _search_placeholder(lang):
    m = {
        "zh-TW": "搜尋工具、型態、文章…",
        "zh-CN": "搜索工具、形态、文章…",
        "en": "Search tools, patterns, articles…",
        "ja": "ツール、パターン、記事を検索…",
        "ko": "도구, 패턴, 기사 검색…",
        "de": "Tools, Muster, Artikel suchen…",
        "fr": "Rechercher outils, patterns, articles…",
        "es": "Buscar herramientas, patrones, artículos…",
        "pt": "Pesquisar ferramentas, padrões, artigos…",
        "id": "Cari alat, pola, artikel…",
    }
    return m.get(lang, m["en"])

def _bm_title(lang):
    m = {
        "zh-TW": "我的收藏", "zh-CN": "我的收藏", "en": "Bookmarks",
        "ja": "ブックマーク", "ko": "북마크", "de": "Lesezeichen",
        "fr": "Favoris", "es": "Marcadores", "pt": "Favoritos", "id": "Bookmark",
    }
    return m.get(lang, m["en"])

def _bm_clear(lang):
    m = {
        "zh-TW": "全部清除", "zh-CN": "全部清除", "en": "Clear all",
        "ja": "すべて削除", "ko": "모두 삭제", "de": "Alle löschen",
        "fr": "Tout effacer", "es": "Borrar todo", "pt": "Limpar tudo", "id": "Hapus semua",
    }
    return m.get(lang, m["en"])

# ---------------------------------------------------------------------------
# Search Index Generator
# ---------------------------------------------------------------------------
def generate_search_index(catalog_entries, locale_configs):
    """Generate search-index.json from all catalog entries + content files."""
    index = []
    
    # Patterns
    for slug, entry in catalog_entries.items():
        titles = {}
        for lang in ALL_LANGS:
            content_path = os.path.join(CONTENT_DIR, f"{slug}_{lang}.json")
            if os.path.exists(content_path):
                try:
                    data = load_json(content_path)
                    titles[lang] = data["seo"]["h1"]
                except Exception:
                    titles[lang] = slug.replace("-", " ").title()
        
        if titles:
            index.append({
                "slug": slug,
                "type": "pattern",
                "category": entry.get("category", ""),
                "titles": titles
            })
    
    # TODO: Add tools and blog entries from their respective catalogs
    # tool-catalog.json → type: "tool"
    # blog-catalog.json → type: "blog"
    
    out_path = os.path.join(OUTPUT_DIR, "..", "search-index.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=None)
    
    print(f"  📇 search-index.json: {len(index)} entries")

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="SoftGlow Pattern Page Generator")
    parser.add_argument("--slug", help="Generate only this pattern (default: all)")
    parser.add_argument("--langs", help="Comma-separated languages (default: all with content)")
    args = parser.parse_args()
    
    print(f"SoftGlow Knowledge Engine — Pattern Generator v{GENERATOR_VERSION}")
    print(f"{'='*60}")
    
    # Load
    catalog = load_json(CATALOG_PATH)
    # Remove _meta key
    catalog_entries = {k: v for k, v in catalog.items() if not k.startswith("_")}
    locale_configs = load_json(LOCALE_PATH)
    template = load_template()
    
    # Filter
    if args.slug:
        if args.slug not in catalog_entries:
            print(f"ERROR: '{args.slug}' not found in pattern-catalog.json")
            sys.exit(1)
        slugs = [args.slug]
    else:
        slugs = list(catalog_entries.keys())
    
    if args.langs:
        langs = [l.strip() for l in args.langs.split(",")]
    else:
        langs = ALL_LANGS
    
    print(f"Patterns: {len(slugs)} | Languages: {len(langs)}")
    print(f"Max pages: {len(slugs) * len(langs)}")
    print(f"Output: {OUTPUT_DIR}")
    print()
    
    generated = 0
    skipped = 0
    errors = 0
    
    for slug in slugs:
        for lang in langs:
            try:
                ok = generate_page(slug, lang, catalog_entries, locale_configs, template)
                if ok:
                    # Quality check
                    issues = quality_check(slug, lang)
                    if issues:
                        print(f"  ⚠ {slug}_{lang}: {issues}")
                        errors += 1
                    else:
                        print(f"  ✅ {slug}_{lang}")
                        generated += 1
                else:
                    skipped += 1
            except Exception as e:
                print(f"  ❌ {slug}_{lang}: {e}")
                errors += 1
    
    # Generate search index
    print()
    generate_search_index(catalog_entries, locale_configs)
    
    print()
    print(f"{'='*60}")
    print(f"Generated: {generated} | Skipped: {skipped} | Errors: {errors}")
    print(f"Output directory: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
