#!/usr/bin/env python3
# fix_patterns_and_ads.py
# 1. Patterns inner pages: v8.10 dark -> V3 white (content unchanged, template only)
# 2. Tool pages AdSense: fix availableWidth=0 error
#
# Usage:
#   cd knowledge-engine
#   python fix_patterns_and_ads.py
#
# After:
#   git add -A && git commit -m "fix: patterns V3 white + AdSense" && git push

import os
import re
import sys

# ═══════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Try to find the frontend directory
REPO_ROOT = os.path.dirname(SCRIPT_DIR)  # knowledge-engine's parent
FRONTEND = os.path.join(REPO_ROOT, "backend", "frontend")
if not os.path.isdir(FRONTEND):
    FRONTEND = os.path.join(REPO_ROOT, "frontend")
if not os.path.isdir(FRONTEND):
    print(f"[ERROR] Cannot find frontend directory. Tried:")
    print(f"  {os.path.join(REPO_ROOT, 'backend', 'frontend')}")
    print(f"  {os.path.join(REPO_ROOT, 'frontend')}")
    sys.exit(1)

PATTERNS_DIR = os.path.join(FRONTEND, "patterns")
TOOLS_DIR = os.path.join(FRONTEND, "tools")

LANGS = ['en', 'ja', 'ko', 'de', 'fr', 'es', 'pt', 'id', 'zh-CN']
# zh-TW patterns are in root, other langs in subdirectories

# Indicators of OLD dark theme (v8.10)
DARK_INDICATORS = [
    'background:#1a1a2e',
    'background:#0f0f1a',
    'background:#16213e',
    'background:#1a1a3e',
    'background:#0d1117',
    'background:#0f172a',
    'background: #1a1a2e',
    'background: #0f0f1a',
    'background: #16213e',
    'color:#e2e8f0',
    'color:#E2E8F0;background:#1',
    'background:#111827',
    'background:#1e1e2f',
    'background:#121212',
    '#1a1a2e',  # fallback catch-all dark bg
]

# V3 white theme CSS (matching tool-template.html style)
V3_CSS = """*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;color:#2D3748;background:#fff;line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:#2563EB;text-decoration:none}
a:hover{text-decoration:underline}
.nav{position:sticky;top:0;z-index:100;background:rgba(255,255,255,0.95);backdrop-filter:blur(8px);border-bottom:1px solid #E2E8F0}
.nav-inner{max-width:1080px;margin:0 auto;padding:0 20px;display:flex;align-items:center;justify-content:space-between;height:52px}
.nav-logo{font-size:17px;font-weight:700;color:#2D3748;letter-spacing:-0.5px}
.nav-logo span{color:#2563EB}
.nav-links{display:flex;gap:16px;align-items:center}
.nav-links a{font-size:13px;color:#4A5568;font-weight:500}
.nav-links a:hover{color:#2563EB;text-decoration:none}
.nav-actions{display:flex;gap:8px;align-items:center}
.act-btn{background:none;border:none;cursor:pointer;padding:6px;border-radius:6px;display:flex;align-items:center;justify-content:center}
.act-btn svg{width:18px;height:18px;stroke:#4A5568;stroke-width:2;fill:none;stroke-linecap:round;stroke-linejoin:round}
.act-btn:hover svg{stroke:#2563EB}
.lang-dropdown{position:relative}
.lang-dropdown-btn{font-size:12px;padding:4px 10px;border-radius:6px;background:#F7FAFC;border:1px solid #E2E8F0;color:#4A5568;cursor:pointer;display:flex;align-items:center;gap:4px}
.lang-dropdown-btn:hover{background:#EBF5FF;border-color:#BEE3F8}
.lang-dropdown-menu{display:none;position:absolute;right:0;top:100%;margin-top:4px;background:#fff;border:1px solid #E2E8F0;border-radius:8px;box-shadow:0 4px 12px rgba(0,0,0,0.1);min-width:120px;z-index:200;padding:4px}
.lang-dropdown.open .lang-dropdown-menu{display:block}
.lang-dropdown-menu a{display:block;padding:6px 12px;font-size:12px;color:#4A5568;border-radius:4px}
.lang-dropdown-menu a:hover{background:#EBF5FF;color:#2563EB;text-decoration:none}
.lang-dropdown-menu a.active{background:#2563EB;color:#fff}
.breadcrumb{max-width:1080px;margin:0 auto;padding:12px 20px;font-size:13px;color:#A0AEC0}
.breadcrumb a{color:#718096}
.container{max-width:1080px;margin:0 auto;padding:0 20px}
.layout{display:grid;grid-template-columns:1fr 320px;gap:32px;align-items:start}
.pattern-card{background:#F7FAFC;border:1px solid #E2E8F0;border-radius:16px;padding:32px;margin-bottom:24px}
.pattern-card h1{font-size:24px;font-weight:700;color:#1A202C;margin-bottom:6px}
.pattern-subtitle{font-size:14px;color:#718096;margin-bottom:24px}
.kbar-chart{text-align:center;margin:24px 0;padding:20px;background:#fff;border:1px solid #E2E8F0;border-radius:12px}
.kbar-chart svg{max-width:100%}
.info-card{background:#F7FAFC;border:1px solid #E2E8F0;border-radius:12px;padding:20px;margin-bottom:16px}
.info-card h2{font-size:18px;font-weight:700;color:#1A202C;margin-bottom:12px}
.info-card h3{font-size:16px;font-weight:600;color:#2D3748;margin:16px 0 8px}
.info-card p,.info-card li{font-size:14px;color:#4A5568;line-height:1.7;margin-bottom:8px}
.info-card ul,.info-card ol{margin:8px 0 12px 20px}
.reliability{display:inline-block;padding:4px 12px;border-radius:20px;font-size:13px;font-weight:600;margin-bottom:16px}
.reliability.high{background:#C6F6D5;color:#22543D}
.reliability.medium{background:#FEFCBF;color:#744210}
.reliability.low{background:#FED7D7;color:#822727}
.sidebar{position:sticky;top:68px}
.ad-slot{min-height:250px;min-width:160px;margin-bottom:20px}
.ad-slot ins{min-width:160px}
.related-card{background:#F7FAFC;border:1px solid #E2E8F0;border-radius:12px;padding:20px}
.related-card h3{font-size:15px;font-weight:600;margin-bottom:12px;color:#1A202C}
.related-link{display:block;padding:8px 0;border-bottom:1px solid #EDF2F7;font-size:13px;color:#2563EB}
.related-link:last-child{border-bottom:none}
.related-link:hover{text-decoration:none;color:#1D4ED8}
.article{margin:40px 0;line-height:1.8}
.article h2{font-size:20px;font-weight:700;color:#1A202C;margin:32px 0 12px}
.article h3{font-size:17px;font-weight:600;color:#2D3748;margin:24px 0 10px}
.article p{margin-bottom:16px;color:#4A5568}
.article ul,.article ol{margin:12px 0 16px 24px;color:#4A5568}
.article li{margin-bottom:6px}
.article table{width:100%;border-collapse:collapse;margin:16px 0}
.article th{text-align:left;padding:10px 12px;background:#F7FAFC;border:1px solid #E2E8F0;font-size:13px;font-weight:600;color:#4A5568}
.article td{padding:10px 12px;border:1px solid #E2E8F0;font-size:14px}
.faq{margin:40px 0}
.faq h2{font-size:20px;font-weight:700;color:#1A202C;margin-bottom:16px}
.faq-item{border-bottom:1px solid #E2E8F0;padding:16px 0}
.faq-q{font-size:15px;font-weight:600;color:#2D3748;cursor:pointer;display:flex;justify-content:space-between;align-items:center}
.faq-q::after{content:"+";font-size:18px;color:#A0AEC0;transition:transform 0.2s}
.faq-item.open .faq-q::after{content:"-"}
.faq-a{font-size:14px;color:#718096;line-height:1.7;max-height:0;overflow:hidden;transition:max-height 0.3s,padding 0.3s}
.faq-item.open .faq-a{max-height:500px;padding-top:10px}
.lang-bar{display:flex;gap:6px;flex-wrap:wrap;margin:24px 0}
.lang-btn{font-size:12px;padding:4px 12px;border-radius:20px;background:#F7FAFC;border:1px solid #E2E8F0;color:#718096;text-decoration:none}
.lang-btn:hover{background:#EBF5FF;border-color:#BEE3F8;text-decoration:none}
.lang-btn.active{background:#2563EB;color:#fff;border-color:#2563EB}
.footer{border-top:1px solid #E2E8F0;padding:24px 0;margin-top:40px}
.footer-inner{max-width:1080px;margin:0 auto;padding:0 20px;display:flex;flex-wrap:wrap;gap:16px;font-size:12px;color:#A0AEC0}
.footer-inner a{color:#718096}
@media(max-width:768px){
  .layout{grid-template-columns:1fr}
  .sidebar{position:static}
  .pattern-card{padding:20px}
  .pattern-card h1{font-size:20px}
}"""

# ═══════════════════════════════════════════════════════════════
# PART 1: Fix Patterns inner pages
# ═══════════════════════════════════════════════════════════════

NAV_LABELS = {
    'zh-TW': {'tools': '工具', 'blog': '教學', 'patterns': 'K棒型態', 'home': '首頁', 'lang_label': '繁中'},
    'zh-CN': {'tools': '工具', 'blog': '教学', 'patterns': 'K线形态', 'home': '首页', 'lang_label': '简中'},
    'en': {'tools': 'Tools', 'blog': 'Blog', 'patterns': 'Patterns', 'home': 'Home', 'lang_label': 'EN'},
    'ja': {'tools': 'ツール', 'blog': 'ブログ', 'patterns': 'ローソク足', 'home': 'ホーム', 'lang_label': 'JA'},
    'ko': {'tools': '도구', 'blog': '블로그', 'patterns': '캔들패턴', 'home': '홈', 'lang_label': 'KO'},
    'de': {'tools': 'Tools', 'blog': 'Blog', 'patterns': 'Muster', 'home': 'Startseite', 'lang_label': 'DE'},
    'fr': {'tools': 'Outils', 'blog': 'Blog', 'patterns': 'Modèles', 'home': 'Accueil', 'lang_label': 'FR'},
    'es': {'tools': 'Herramientas', 'blog': 'Blog', 'patterns': 'Patrones', 'home': 'Inicio', 'lang_label': 'ES'},
    'pt': {'tools': 'Ferramentas', 'blog': 'Blog', 'patterns': 'Padrões', 'home': 'Início', 'lang_label': 'PT'},
    'id': {'tools': 'Alat', 'blog': 'Blog', 'patterns': 'Pola', 'home': 'Beranda', 'lang_label': 'ID'},
}

LANG_NAMES = {
    'zh-TW': '繁體中文', 'zh-CN': '简体中文', 'en': 'English',
    'ja': '日本語', 'ko': '한국어', 'de': 'Deutsch',
    'fr': 'Français', 'es': 'Español', 'pt': 'Português', 'id': 'Bahasa Indonesia'
}

ALL_LANGS = ['zh-TW', 'en', 'zh-CN', 'ja', 'ko', 'de', 'fr', 'es', 'pt', 'id']


def is_dark_theme(html):
    """Check if a page uses the old dark theme."""
    style_match = re.search(r'<style[^>]*>(.*?)</style>', html, re.DOTALL | re.IGNORECASE)
    if not style_match:
        return False
    style = style_match.group(1).lower()
    for indicator in DARK_INDICATORS:
        if indicator.lower() in style:
            return True
    # Also check body background
    if 'background:#fff' in style or 'background: #fff' in style or 'background:white' in style:
        return False
    # Check if body has a dark color
    body_bg = re.search(r'body\s*\{[^}]*background\s*:\s*(#[0-9a-f]{3,6})', style)
    if body_bg:
        color = body_bg.group(1).lower()
        # Dark colors have low values
        if color.startswith('#') and len(color) == 7:
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            if r < 80 and g < 80 and b < 80:
                return True
    return False


def extract_content(html):
    """Extract key content from a pattern page regardless of theme."""
    result = {}

    # Extract title from <title> or <h1>
    title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
    result['title'] = title_match.group(1).strip() if title_match else 'Pattern'

    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL | re.IGNORECASE)
    result['h1'] = h1_match.group(1).strip() if h1_match else result['title']

    # Extract meta description
    desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', html, re.IGNORECASE)
    result['description'] = desc_match.group(1) if desc_match else ''

    # Extract lang from <html lang="...">
    lang_match = re.search(r'<html[^>]*lang="([^"]*)"', html, re.IGNORECASE)
    result['lang_code'] = lang_match.group(1) if lang_match else 'zh-TW'

    # Extract canonical
    canonical_match = re.search(r'<link\s+rel="canonical"\s+href="([^"]*)"', html, re.IGNORECASE)
    result['canonical'] = canonical_match.group(1) if canonical_match else ''

    # Extract hreflang tags
    hreflang_matches = re.findall(r'<link\s+rel="alternate"\s+hreflang="[^"]*"\s+href="[^"]*"\s*/?\s*>', html, re.IGNORECASE)
    result['hreflangs'] = '\n'.join(hreflang_matches)

    # Extract all SVGs
    svgs = re.findall(r'<svg[^>]*>.*?</svg>', html, re.DOTALL | re.IGNORECASE)
    result['svgs'] = svgs

    # Extract JSON-LD schemas
    schemas = re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.DOTALL | re.IGNORECASE)
    result['schemas'] = schemas

    # Extract article/content sections - look for various content containers
    # Try to find content between known markers
    content_sections = []

    # Method 1: Look for divs/sections with content-like classes
    for pattern in [
        r'<(?:div|section)\s+class="[^"]*(?:info-card|content|article|pattern-section|section)[^"]*"[^>]*>(.*?)</(?:div|section)>',
    ]:
        matches = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)
        content_sections.extend(matches)

    # Method 2: Extract all h2/h3 sections with their content
    if not content_sections:
        # Get everything between <body> and </body>, strip nav and footer
        body_match = re.search(r'<body[^>]*>(.*)</body>', html, re.DOTALL | re.IGNORECASE)
        if body_match:
            body = body_match.group(1)
            # Remove nav
            body = re.sub(r'<nav[^>]*>.*?</nav>', '', body, flags=re.DOTALL | re.IGNORECASE)
            # Remove footer
            body = re.sub(r'<footer[^>]*>.*?</footer>', '', body, flags=re.DOTALL | re.IGNORECASE)
            # Remove script tags
            body = re.sub(r'<script[^>]*>.*?</script>', '', body, flags=re.DOTALL | re.IGNORECASE)
            # Remove style tags
            body = re.sub(r'<style[^>]*>.*?</style>', '', body, flags=re.DOTALL | re.IGNORECASE)
            # Remove breadcrumb
            body = re.sub(r'<div\s+class="breadcrumb[^"]*"[^>]*>.*?</div>', '', body, flags=re.DOTALL | re.IGNORECASE)
            # Remove lang-bar
            body = re.sub(r'<div\s+class="lang-bar[^"]*"[^>]*>.*?</div>', '', body, flags=re.DOTALL | re.IGNORECASE)
            # Remove ad slots
            body = re.sub(r'<div[^>]*class="[^"]*ad-slot[^"]*"[^>]*>.*?</div>', '', body, flags=re.DOTALL | re.IGNORECASE)
            body = re.sub(r'<ins[^>]*adsbygoogle[^>]*>.*?</ins>', '', body, flags=re.DOTALL | re.IGNORECASE)
            # Remove sidebar
            body = re.sub(r'<aside[^>]*>.*?</aside>', '', body, flags=re.DOTALL | re.IGNORECASE)
            # Remove related cards
            body = re.sub(r'<div\s+class="related-card[^"]*"[^>]*>.*?</div>\s*</div>', '', body, flags=re.DOTALL | re.IGNORECASE)

            result['body_content'] = body.strip()

    # Extract FAQ items
    faq_items = []
    faq_q_matches = list(re.finditer(r'<(?:div|dt)\s+class="[^"]*faq-q[^"]*"[^>]*>(.*?)</(?:div|dt)>', html, re.DOTALL | re.IGNORECASE))
    faq_a_matches = list(re.finditer(r'<(?:div|dd)\s+class="[^"]*faq-a[^"]*"[^>]*>(.*?)</(?:div|dd)>', html, re.DOTALL | re.IGNORECASE))

    for i, q_match in enumerate(faq_q_matches):
        q_text = q_match.group(1).strip()
        # Remove the ::after content marker
        q_text = re.sub(r'<span[^>]*>.*?</span>$', '', q_text).strip()
        a_text = faq_a_matches[i].group(1).strip() if i < len(faq_a_matches) else ''
        if q_text:
            faq_items.append((q_text, a_text))

    result['faq_items'] = faq_items

    # Extract related links
    related_links = re.findall(r'<a[^>]*class="[^"]*related-link[^"]*"[^>]*href="([^"]*)"[^>]*>(.*?)</a>', html, re.DOTALL | re.IGNORECASE)
    result['related_links'] = related_links

    return result


def get_lang_from_path(filepath, patterns_dir):
    """Determine language from file path."""
    rel = os.path.relpath(filepath, patterns_dir)
    parts = rel.replace('\\', '/').split('/')
    if len(parts) == 1:
        # Root level = zh-TW
        return 'zh-TW'
    else:
        lang_dir = parts[0]
        if lang_dir in LANGS:
            return lang_dir
        return 'zh-TW'


def get_slug_from_path(filepath):
    """Get slug from filename."""
    return os.path.splitext(os.path.basename(filepath))[0]


def build_v3_pattern_page(content, lang, slug):
    """Build a V3 white-theme pattern page from extracted content."""
    labels = NAV_LABELS.get(lang, NAV_LABELS['en'])

    # URL paths
    if lang == 'zh-TW':
        tools_url = '/tools/'
        blog_url = '/blog/'
        patterns_url = '/patterns/'
        patterns_index = '/patterns/index.html'
        this_url = f'/patterns/{slug}.html'
    else:
        tools_url = f'/tools/{lang}/'
        blog_url = f'/blog/{lang}/'
        patterns_url = f'/patterns/{lang}/'
        patterns_index = f'/patterns/{lang}.html'
        this_url = f'/patterns/{lang}/{slug}.html'

    # Language dropdown
    dropdown_items = []
    for l in ALL_LANGS:
        if l == 'zh-TW':
            href = f'/patterns/{slug}.html'
        else:
            href = f'/patterns/{l}/{slug}.html'
        active = ' class="active"' if l == lang else ''
        dropdown_items.append(f'<a href="{href}"{active}>{LANG_NAMES[l]}</a>')

    dropdown = f'''<div class="lang-dropdown" onclick="this.classList.toggle('open')">
      <button class="lang-dropdown-btn">{labels["lang_label"]} ▾</button>
      <div class="lang-dropdown-menu">
        {''.join(dropdown_items)}
      </div>
    </div>'''

    # Schemas
    schemas_html = ''
    for s in content.get('schemas', []):
        schemas_html += f'<script type="application/ld+json">{s}</script>\n'

    # SVG chart
    svg_html = ''
    for svg in content.get('svgs', []):
        # Skip tiny nav SVGs (search/bookmark icons)
        if 'viewBox="0 0 24 24"' in svg and len(svg) < 300:
            continue
        svg_html += f'<div class="kbar-chart">{svg}</div>\n'

    # Body content
    body_content = content.get('body_content', '')

    # Clean up old dark-theme inline styles from content
    body_content = re.sub(r'style="[^"]*color\s*:\s*#[ef][0-9a-f]{5}[^"]*"', '', body_content, flags=re.IGNORECASE)
    body_content = re.sub(r'style="[^"]*background\s*:\s*#[012][0-9a-f]{5}[^"]*"', '', body_content, flags=re.IGNORECASE)
    body_content = re.sub(r'color:\s*#(?:e2e8f0|cbd5e0|a0aec0|edf2f7|f7fafc|fff)', 'color:#4A5568', body_content, flags=re.IGNORECASE)
    body_content = re.sub(r'background:\s*#(?:1a1a2e|0f0f1a|16213e|1e1e2f|0d1117|111827|0f172a|2d2d44|252540)', 'background:#F7FAFC', body_content, flags=re.IGNORECASE)
    body_content = re.sub(r'border[^:]*:\s*1px\s+solid\s+#(?:2d2d44|333|3a3a5c|4a4a6a)', 'border:1px solid #E2E8F0', body_content, flags=re.IGNORECASE)

    # FAQ section
    faq_html = ''
    if content.get('faq_items'):
        faq_title = {'zh-TW': '常見問題', 'zh-CN': '常见问题', 'ja': 'よくある質問', 'ko': '자주 묻는 질문',
                      'de': 'Häufig gestellte Fragen', 'fr': 'Questions fréquentes',
                      'es': 'Preguntas frecuentes', 'pt': 'Perguntas frequentes',
                      'id': 'Pertanyaan Umum'}.get(lang, 'FAQ')
        items_html = ''
        for q, a in content['faq_items']:
            items_html += f'''<div class="faq-item">
  <div class="faq-q">{q}</div>
  <div class="faq-a">{a}</div>
</div>\n'''
        faq_html = f'''<section class="faq">
<h2>{faq_title}</h2>
{items_html}
</section>'''

    # Related links
    related_html = ''
    if content.get('related_links'):
        related_title = {'zh-TW': '相關型態', 'zh-CN': '相关形态', 'ja': '関連パターン', 'ko': '관련 패턴',
                         'de': 'Verwandte Muster', 'fr': 'Modèles connexes',
                         'es': 'Patrones relacionados', 'pt': 'Padrões relacionados',
                         'id': 'Pola Terkait'}.get(lang, 'Related Patterns')
        links = ''
        for href, text in content['related_links']:
            links += f'<a class="related-link" href="{href}">{text}</a>\n'
        related_html = f'''<div class="related-card">
    <h3>{related_title}</h3>
    {links}
  </div>'''

    # Language bar at bottom
    lang_buttons = ''
    for l in ALL_LANGS:
        if l == 'zh-TW':
            href = f'/patterns/{slug}.html'
        else:
            href = f'/patterns/{l}/{slug}.html'
        active = ' active' if l == lang else ''
        lang_buttons += f'<a class="lang-btn{active}" href="{href}">{LANG_NAMES[l]}</a>\n'

    # Breadcrumb
    back_label = {'zh-TW': 'K棒型態總覽', 'zh-CN': 'K线形态总览', 'ja': 'ローソク足パターン一覧',
                  'ko': '캔들 패턴 목록', 'de': 'Muster-Übersicht', 'fr': 'Vue d\'ensemble',
                  'es': 'Descripción general', 'pt': 'Visão geral', 'id': 'Daftar Pola'}.get(lang, 'Pattern Overview')

    # AdSense
    ad_slot_html = '''<div class="ad-slot">
  <ins class="adsbygoogle" style="display:block;min-width:160px;min-height:250px" data-ad-client="ca-pub-1768270548115739" data-ad-slot="auto" data-ad-format="auto" data-full-width-responsive="true"></ins>
</div>'''

    html = f'''<!DOCTYPE html>
<html lang="{content['lang_code']}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{content['title']}</title>
<meta name="description" content="{content['description']}">
<meta name="robots" content="index, follow">
{f'<link rel="canonical" href="{content["canonical"]}">' if content.get('canonical') else ''}
{content.get('hreflangs', '')}
<meta name="sg-slug" content="{slug}">
<meta name="sg-type" content="pattern">
<meta name="sg-lang" content="{lang}">
<link rel="stylesheet" href="/common/softglow-common.css">
{schemas_html}
<style>
{V3_CSS}
</style>
</head>
<body>

<nav class="nav">
<div class="nav-inner">
  <a href="/" class="nav-logo">Soft<span>Glow</span></a>
  <div class="nav-links">
    <a href="{tools_url}">{labels['tools']}</a>
    <a href="{blog_url}">{labels['blog']}</a>
    <a href="{patterns_url}">{labels['patterns']}</a>
    <a href="/">{labels['home']}</a>
  </div>
  <div class="nav-actions">
    {dropdown}
    <button class="act-btn" onclick="sgOpenSearch()" title="Search"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></button>
    <button class="act-btn" id="sgBmBtn" onclick="sgToggleBookmark()" title="Bookmark"><svg viewBox="0 0 24 24"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg></button>
  </div>
</div>
</nav>

<div class="breadcrumb">
  <a href="/">Home</a> › <a href="{patterns_index}">{back_label}</a> › {content['h1']}
</div>

<div class="container">
<div class="layout">

<div class="main">
  {svg_html}
  {body_content}
  {faq_html}
  <div class="lang-bar">
    {lang_buttons}
  </div>
</div>

<aside class="sidebar">
  {ad_slot_html}
  {related_html}
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

<div id="sgSearchOverlay" class="search-overlay" style="display:none"></div>
<div id="sgBmPanel" class="bookmark-panel" style="display:none"></div>

<script>
document.querySelectorAll('.faq-q').forEach(function(q){{
  q.addEventListener('click',function(){{this.parentElement.classList.toggle('open')}});
}});
document.addEventListener('click',function(e){{
  document.querySelectorAll('.lang-dropdown.open').forEach(function(d){{
    if(!d.contains(e.target))d.classList.remove('open');
  }});
}});
</script>
<script src="/common/softglow-common.js"></script>
<script>
setTimeout(function(){{
  var s=document.createElement('script');
  s.async=true;
  s.src='https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1768270548115739';
  s.crossOrigin='anonymous';
  document.head.appendChild(s);
  s.onload=function(){{
    document.querySelectorAll('ins.adsbygoogle').forEach(function(ad){{
      if(ad.offsetWidth>0){{try{{(adsbygoogle=window.adsbygoogle||[]).push({{}})}}catch(e){{}}}}
    }});
  }};
}},2000);
</script>

</body>
</html>'''

    return html


def fix_patterns():
    """Fix all pattern inner pages from dark to V3 white."""
    print("=" * 60)
    print("PART 1: Fix Patterns Inner Pages → V3 White")
    print("=" * 60)

    if not os.path.isdir(PATTERNS_DIR):
        print(f"  [SKIP] Patterns directory not found: {PATTERNS_DIR}")
        return 0

    fixed = 0
    skipped = 0
    already_v3 = 0
    errors = 0

    # Collect all pattern HTML files (excluding index pages)
    pattern_files = []

    # Root level (zh-TW) — skip index files
    index_names = {'index.html', 'en.html', 'ja.html', 'ko.html', 'de.html',
                   'fr.html', 'es.html', 'pt.html', 'id.html', 'zh-CN.html'}
    for f in os.listdir(PATTERNS_DIR):
        if f.endswith('.html') and f not in index_names:
            pattern_files.append(os.path.join(PATTERNS_DIR, f))

    # Language subdirectories
    for lang_dir in LANGS:
        lang_path = os.path.join(PATTERNS_DIR, lang_dir)
        if os.path.isdir(lang_path):
            for f in os.listdir(lang_path):
                if f.endswith('.html') and f != 'index.html':
                    pattern_files.append(os.path.join(lang_path, f))

    print(f"  Found {len(pattern_files)} pattern inner pages")

    for filepath in sorted(pattern_files):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                html = f.read()

            if not is_dark_theme(html):
                # Check if it already has V3 indicators
                if 'softglow-common.css' in html and 'background:#fff' in html:
                    already_v3 += 1
                    continue
                # Has white bg but missing softglow-common — still needs fix
                if 'softglow-common.css' in html:
                    already_v3 += 1
                    continue

            lang = get_lang_from_path(filepath, PATTERNS_DIR)
            slug = get_slug_from_path(filepath)

            content = extract_content(html)
            new_html = build_v3_pattern_page(content, lang, slug)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_html)

            fixed += 1

        except Exception as e:
            print(f"  [ERROR] {os.path.relpath(filepath, PATTERNS_DIR)}: {e}")
            errors += 1

    print(f"\n  Results:")
    print(f"    Fixed (dark→V3):  {fixed}")
    print(f"    Already V3:       {already_v3}")
    print(f"    Errors:           {errors}")
    print(f"    Total scanned:    {len(pattern_files)}")

    return fixed


# ═══════════════════════════════════════════════════════════════
# PART 2: Fix AdSense availableWidth=0
# ═══════════════════════════════════════════════════════════════

def fix_adsense_in_file(filepath):
    """Fix AdSense issues in a single HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    original = html
    changes = 0

    # Fix 1: Add min-width and min-height to all <ins> adsbygoogle tags
    # Pattern: <ins class="adsbygoogle" style="display:block" ...>
    def fix_ins_style(match):
        nonlocal changes
        tag = match.group(0)
        # Check if already has min-width
        if 'min-width' in tag:
            return tag
        # Add min-width and min-height to the style attribute
        if 'style="' in tag:
            tag = tag.replace('style="', 'style="min-width:160px;min-height:250px;')
            changes += 1
        elif "style='" in tag:
            tag = tag.replace("style='", "style='min-width:160px;min-height:250px;")
            changes += 1
        return tag

    html = re.sub(r'<ins\s+class="adsbygoogle"[^>]*>', fix_ins_style, html)

    # Fix 2: Replace direct adsbygoogle.push with width-checking version
    # Find patterns like: try{(adsbygoogle=window.adsbygoogle||[]).push({})}catch(e){}
    # that are NOT inside a width check

    # Replace the onload function that does direct pushes
    old_onload_pattern = r"s\.onload\s*=\s*function\s*\(\)\s*\{((?:try\s*\{\s*\(adsbygoogle\s*=\s*window\.adsbygoogle\s*\|\|\s*\[\]\)\s*\.push\s*\(\s*\{\}\s*\)\s*\}\s*catch\s*\(\s*\w+\s*\)\s*\{\s*\}\s*)+)\}"

    def replace_onload(match):
        nonlocal changes
        # Count how many push calls
        push_count = match.group(1).count('.push(')
        new_fn = "s.onload=function(){document.querySelectorAll('ins.adsbygoogle').forEach(function(ad){if(ad.offsetWidth>0){try{(adsbygoogle=window.adsbygoogle||[]).push({})}catch(e){}}})}"
        changes += 1
        return new_fn

    html = re.sub(old_onload_pattern, replace_onload, html)

    # Fix 3: Ensure ad container divs have min-width
    def fix_ad_div(match):
        nonlocal changes
        tag = match.group(0)
        if 'min-width' in tag or 'min-height' in tag:
            return tag
        # Add style with min dimensions
        if 'style="' in tag:
            tag = tag.replace('style="', 'style="min-width:160px;min-height:250px;')
        elif "style='" in tag:
            tag = tag.replace("style='", "style='min-width:160px;min-height:250px;")
        else:
            tag = tag.replace('>', ' style="min-width:160px;min-height:250px">', 1)
        changes += 1
        return tag

    html = re.sub(r'<div[^>]*class="[^"]*ad-slot[^"]*"[^>]*>', fix_ad_div, html)

    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)

    return changes


def fix_adsense():
    """Fix AdSense availableWidth=0 across all tool pages."""
    print("\n" + "=" * 60)
    print("PART 2: Fix AdSense availableWidth=0")
    print("=" * 60)

    if not os.path.isdir(TOOLS_DIR):
        print(f"  [SKIP] Tools directory not found: {TOOLS_DIR}")
        return 0

    total_changes = 0
    files_fixed = 0

    # Collect all HTML files in tools directory
    tool_files = []
    for root, dirs, files in os.walk(TOOLS_DIR):
        for f in files:
            if f.endswith('.html'):
                tool_files.append(os.path.join(root, f))

    print(f"  Found {len(tool_files)} tool pages")

    for filepath in sorted(tool_files):
        try:
            changes = fix_adsense_in_file(filepath)
            if changes > 0:
                files_fixed += 1
                total_changes += changes
        except Exception as e:
            print(f"  [ERROR] {os.path.relpath(filepath, TOOLS_DIR)}: {e}")

    # Also fix pattern pages
    pattern_count = 0
    if os.path.isdir(PATTERNS_DIR):
        for root, dirs, files in os.walk(PATTERNS_DIR):
            for f in files:
                if f.endswith('.html'):
                    filepath = os.path.join(root, f)
                    try:
                        changes = fix_adsense_in_file(filepath)
                        if changes > 0:
                            pattern_count += 1
                            total_changes += changes
                    except Exception as e:
                        pass

    print(f"\n  Results:")
    print(f"    Tool pages fixed:     {files_fixed}")
    print(f"    Pattern pages fixed:  {pattern_count}")
    print(f"    Total changes:        {total_changes}")

    return files_fixed + pattern_count


# ═══════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print(f"Frontend directory: {FRONTEND}")
    print(f"Patterns directory: {PATTERNS_DIR}")
    print(f"Tools directory:    {TOOLS_DIR}")
    print()

    p_fixed = fix_patterns()
    a_fixed = fix_adsense()

    print("\n" + "=" * 60)
    print("ALL DONE!")
    print("=" * 60)
    print(f"  Patterns fixed:  {p_fixed}")
    print(f"  AdSense fixed:   {a_fixed}")
    print()
    print("Next steps:")
    print("  cd D:\\xian-shang-you-wei")
    print('  git add -A')
    print('  git commit -m "fix: patterns V3 white + AdSense availableWidth"')
    print('  git push')
