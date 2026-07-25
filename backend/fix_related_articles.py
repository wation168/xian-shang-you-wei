"""
fix_related_articles.py
修正全站工具頁的 Related Articles 連結
問題：generate_tools_v2.py 把所有工具頁都連到 KD/MACD/停損 三篇股票文章
修法：根據工具分類，連到同分類的其他工具

用法（在 backend 目錄下執行）：
  python fix_related_articles.py --dry-run     # 先看會改哪些
  python fix_related_articles.py               # 執行修改
"""

import os
import re
import sys

TOOLS_DIR = os.path.join(os.path.dirname(__file__), "frontend", "tools")

# 工具分類對照表（slug → category）
TOOL_CATEGORIES = {
    # 金融投資
    "compound-interest": "finance", "roi-calculator": "finance", "risk-reward": "finance",
    "position-size": "finance", "stop-loss": "finance", "dividend-yield": "finance",
    "pe-ratio": "finance", "dca-calculator": "finance", "retirement-calculator": "finance",
    "mortgage-calculator": "finance", "inflation-calculator": "finance", "currency-converter": "finance",
    "margin-calculator": "finance", "cagr": "finance", "stock-gain-loss": "finance",
    "trading-fee": "finance", "stock-split": "finance", "average-down": "finance",
    "break-even": "finance", "rule-of-72": "finance", "asset-allocation": "finance",
    "dcf-calculator": "finance", "intrinsic-value": "finance", "options-profit": "finance",
    "sharpe-ratio": "finance", "kelly-criterion": "finance", "salary-raise": "finance",
    "savings-goal": "finance", "loan-calculator": "finance", "credit-card-payoff": "finance",
    "net-worth": "finance", "tip-calculator": "finance", "discount-calculator": "finance",
    "tax-bracket": "finance", "payroll-tax": "finance", "freelance-tax": "finance",
    "sales-commission": "finance", "depreciation": "finance", "business-valuation": "finance",
    "startup-cost": "finance", "profit-margin": "finance",

    # 健康體適能
    "bmi-calculator": "health", "calorie-calculator": "health", "body-fat": "health",
    "bmr-calculator": "health", "macro-calculator": "health", "water-intake": "health",
    "steps-to-calories": "health", "heart-rate-zone": "health", "ideal-weight": "health",
    "waist-hip-ratio": "health", "pregnancy-due-date": "health", "ovulation-calculator": "health",
    "caffeine-calculator": "health", "sleep-calculator": "health", "blood-alcohol": "health",
    "pace-calculator": "health", "one-rep-max": "health",

    # 電力能源
    "electricity-cost": "energy", "solar-panel": "energy", "battery-calculator": "energy",
    "ev-range": "energy", "carbon-footprint": "energy", "appliance-energy": "energy",
    "air-conditioner-size": "energy", "water-usage": "energy", "kwh-calculator": "energy",
    "power-consumption": "energy", "generator-size": "energy", "gas-mileage": "energy",
    "fuel-cost": "energy",

    # 電商物流
    "shipping-cost": "ecommerce", "cbm-calculator": "ecommerce", "customs-duty": "ecommerce",
    "fba-calculator": "ecommerce", "ebay-fee": "ecommerce", "etsy-fee": "ecommerce",
    "dropshipping-profit": "ecommerce", "amazon-roi": "ecommerce",

    # 建築裝修
    "paint-calculator": "construction", "tile-calculator": "construction",
    "concrete-calculator": "construction", "flooring-calculator": "construction",
    "wallpaper-calculator": "construction", "lumber-calculator": "construction",
    "roof-calculator": "construction", "fence-calculator": "construction",

    # 日期時間
    "work-days": "datetime", "date-difference": "datetime", "age-calculator": "datetime",
    "time-zone-converter": "datetime", "countdown-timer": "datetime",

    # 數學統計
    "percentage-calculator": "math", "gpa-calculator": "math", "grade-calculator": "math",
    "scientific-calculator": "math", "fraction-calculator": "math", "standard-deviation": "math",

    # 單位換算
    "length-converter": "conversion", "weight-converter": "conversion",
    "temperature-converter": "conversion", "volume-converter": "conversion",
    "cooking-conversion": "conversion", "paper-weight": "conversion",

    # 法律合規
    "court-fee": "legal", "alimony-calculator": "legal", "child-support": "legal",
    "overtime-calculator": "legal", "severance-calculator": "legal",

    # 保險
    "health-insurance-estimate": "insurance", "life-insurance": "insurance",
    "car-insurance": "insurance", "travel-insurance": "insurance",

    # 房地產
    "rent-vs-buy": "realestate", "property-tax": "realestate", 
    "down-payment": "realestate", "closing-cost": "realestate",

    # 汽車交通
    "car-loan": "auto", "car-depreciation": "auto", "lease-vs-buy": "auto",
    "road-trip-cost": "auto", "tire-size": "auto",

    # 教育
    "student-loan": "education", "scholarship-calculator": "education",
    "tuition-calculator": "education", "study-abroad-cost": "education",

    # 技術分析（股票相關工具才連到 blog）
    "fibonacci-retracement": "technical", "pivot-point": "technical",
    "rsi-calculator": "technical", "macd-calculator": "technical",
    "bollinger-bands": "technical", "atr-calculator": "technical",
    "ma-crossover": "technical", "candlestick-identifier": "technical",
    "support-resistance": "technical", "pip-value": "technical",
}

# 每個分類的推薦連結（slug → display name，每語言）
# 如果同分類工具不足 3 個，用通用工具補
CATEGORY_LINKS = {}  # Will be auto-generated from files on disk

# 語言對應的標題和標籤
LANG_CONFIG = {
    "zh-TW": {"title": "🔧 相關工具", "span": "→ 工具"},
    "en": {"title": "🔧 Related Tools", "span": "→ Tool"},
    "ja": {"title": "🔧 関連ツール", "span": "→ ツール"},
    "ko": {"title": "🔧 관련 도구", "span": "→ 도구"},
    "de": {"title": "🔧 Verwandte Tools", "span": "→ Tool"},
    "fr": {"title": "🔧 Outils associés", "span": "→ Outil"},
    "es": {"title": "🔧 Herramientas relacionadas", "span": "→ Herramienta"},
    "pt": {"title": "🔧 Ferramentas relacionadas", "span": "→ Ferramenta"},
    "id": {"title": "🔧 Alat Terkait", "span": "→ Alat"},
    "zh-CN": {"title": "🔧 相关工具", "span": "→ 工具"},
}


def get_lang_from_path(filepath):
    """Determine language from file path"""
    rel = os.path.relpath(filepath, TOOLS_DIR).replace("\\", "/")
    parts = rel.split("/")
    if len(parts) == 1:
        return "zh-TW"  # root = zh-TW
    return parts[0]


def get_slug_from_path(filepath):
    """Extract slug from filename"""
    return os.path.splitext(os.path.basename(filepath))[0]


def find_related_tools(slug, lang, all_tools_by_lang):
    """Find 3 related tools from same category"""
    category = TOOL_CATEGORIES.get(slug, "other")
    lang_tools = all_tools_by_lang.get(lang, {})
    
    # Same category, excluding self
    same_cat = [s for s, c in TOOL_CATEGORIES.items() 
                if c == category and s != slug and s in lang_tools]
    
    if len(same_cat) >= 3:
        return same_cat[:3]
    
    # Pad with popular tools from other categories
    popular = ["bmi-calculator", "compound-interest", "percentage-calculator",
               "currency-converter", "mortgage-calculator", "calorie-calculator"]
    for p in popular:
        if p != slug and p not in same_cat and p in lang_tools:
            same_cat.append(p)
        if len(same_cat) >= 3:
            break
    
    return same_cat[:3]


def get_tool_name_from_html(filepath):
    """Extract h1 tool name from HTML file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read(5000)  # Only read first 5KB
        match = re.search(r'<h1>(.*?)</h1>', content)
        return match.group(1) if match else os.path.splitext(os.path.basename(filepath))[0]
    except:
        return os.path.splitext(os.path.basename(filepath))[0]


def build_tool_url(slug, lang):
    """Build URL path for a tool"""
    if lang == "zh-TW":
        return f"/tools/{slug}.html"
    return f"/tools/{lang}/{slug}.html"


def main():
    dry_run = "--dry-run" in sys.argv
    
    if not os.path.isdir(TOOLS_DIR):
        print(f"❌ Tools directory not found: {TOOLS_DIR}")
        sys.exit(1)
    
    # Scan all tool HTML files
    all_tools_by_lang = {}  # {lang: {slug: filepath}}
    all_files = []
    
    for root, dirs, files in os.walk(TOOLS_DIR):
        for fname in files:
            if not fname.endswith('.html') or fname.startswith('index'):
                continue
            filepath = os.path.join(root, fname)
            lang = get_lang_from_path(filepath)
            slug = get_slug_from_path(filepath)
            
            if lang not in all_tools_by_lang:
                all_tools_by_lang[lang] = {}
            all_tools_by_lang[lang][slug] = filepath
            all_files.append(filepath)
    
    print(f"Found {len(all_files)} tool pages across {len(all_tools_by_lang)} languages")
    
    # Cache tool names
    tool_names = {}
    for filepath in all_files:
        slug = get_slug_from_path(filepath)
        lang = get_lang_from_path(filepath)
        key = f"{lang}/{slug}"
        if key not in tool_names:
            tool_names[key] = get_tool_name_from_html(filepath)
    
    fixed = 0
    skipped = 0
    errors = 0
    
    for filepath in all_files:
        slug = get_slug_from_path(filepath)
        lang = get_lang_from_path(filepath)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            errors += 1
            continue
        
        # Check if blog-section exists and has mismatched links
        blog_section = re.search(r'<div class="blog-section">.*?</div>\s*</div>', content, re.DOTALL)
        if not blog_section:
            skipped += 1
            continue
        
        # Check if it links to stock trading articles (the mismatch)
        section_text = blog_section.group(0)
        is_stock_tool = TOOL_CATEGORIES.get(slug) == "technical"
        has_stock_links = any(x in section_text for x in ["kd-indicator", "macd-indicator", "stop-loss-guide", "candlestick-patterns"])
        
        if is_stock_tool and has_stock_links:
            skipped += 1  # Stock tools linking to stock articles = correct
            continue
        
        if not has_stock_links:
            skipped += 1  # Already fixed or custom links
            continue
        
        # This page has mismatched stock links — fix it
        related_slugs = find_related_tools(slug, lang, all_tools_by_lang)
        
        if not related_slugs:
            skipped += 1
            continue
        
        lang_cfg = LANG_CONFIG.get(lang, LANG_CONFIG["en"])
        cards = []
        for rs in related_slugs:
            url = build_tool_url(rs, lang)
            name = tool_names.get(f"{lang}/{rs}", rs)
            cards.append(f'<a class="blog-card" href="{url}">{name}<span>{lang_cfg["span"]}</span></a>')
        
        new_section = f'<div class="blog-section"><h3>{lang_cfg["title"]}</h3><div class="blog-grid">{"".join(cards)}</div></div>'
        
        if dry_run:
            print(f"  WOULD FIX: {os.path.relpath(filepath, TOOLS_DIR)}")
            fixed += 1
        else:
            content = content[:blog_section.start()] + new_section + content[blog_section.end():]
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            fixed += 1
    
    prefix = "[DRY RUN] " if dry_run else ""
    print(f"\n{prefix}Results: {fixed} fixed, {skipped} skipped (OK), {errors} errors")


if __name__ == "__main__":
    main()
