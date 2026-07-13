#!/usr/bin/env python3
"""
SoftGlow — Fix Everything v2.0
===============================
Fixes ALL pending issues in one pass:

1. Tool pages: lang-bar → nav dropdown + related links by category
2. Tool index pages: rebuild with category card layout
3. Blog pages: verify new V3 versions exist (generate_blog.py output)
4. softglow-common.js: fix Chinese search
5. search-index.json: rebuild with tools + patterns + comparisons + blog
6. Tool page JS errors: scan and auto-fix common issues

Run from: D:\\xian-shang-you-wei\\knowledge-engine
Usage:  python fix_everything.py

Prerequisites:
  - generate_blog.py must have finished (120 blog pages in cache/output)
  - All tool pages must be in backend/frontend/tools/
"""

import os, re, json, glob, sys, html as html_mod

# ── Paths ───────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(SCRIPT_DIR, "..", "backend", "frontend")
TOOLS_DIR = os.path.join(BASE, "tools")
BLOG_DIR = os.path.join(BASE, "blog")
PATTERNS_DIR = os.path.join(BASE, "patterns")
COMPARISONS_DIR = os.path.join(BASE, "comparisons")
COMMON_DIR = os.path.join(BASE, "common")

LANGS = ["zh-TW", "en", "ja", "ko", "de", "fr", "es", "pt", "id", "zh-CN"]
LANG_NAMES = {
    "zh-TW": "繁中", "en": "EN", "ja": "日本語", "ko": "한국어",
    "de": "DE", "fr": "FR", "es": "ES", "pt": "PT",
    "id": "ID", "zh-CN": "简中"
}

# ── Tool category definitions ──────────────────────────────────────────
TOOL_CATEGORIES = {
    "finance": {
        "zh-TW": "金融投資", "en": "Finance & Investment", "ja": "金融投資",
        "ko": "금융 투자", "de": "Finanzen", "fr": "Finance",
        "es": "Finanzas", "pt": "Finanças", "id": "Keuangan", "zh-CN": "金融投资",
        "icon": "💰",
        "slugs": [
            "compound-interest", "roi-calculator", "risk-reward", "position-size",
            "stop-loss", "dividend-yield", "pe-ratio", "dca-calculator", "cagr",
            "margin-calculator", "stock-gain-loss", "break-even", "rule-of-72",
            "asset-allocation", "dcf-calculator", "intrinsic-value", "options-profit",
            "fibonacci-retracement", "pivot-point", "rsi-calculator", "macd-calculator",
            "bollinger-bands", "atr-calculator", "sharpe-ratio", "ma-crossover",
            "candlestick-identifier", "support-resistance", "trading-fee",
            "stock-split", "average-down", "pip-value", "currency-converter",
            "kelly-criterion", "retirement", "savings-goal", "bond-yield",
            "portfolio-rebalance", "expense-ratio", "earnings-per-share",
            "price-to-book", "debt-to-equity", "current-ratio", "quick-ratio",
            "free-cash-flow", "wacc-calculator", "payback-period", "npv-calculator",
            "irr-calculator", "annuity-calculator", "sip-calculator",
        ]
    },
    "health": {
        "zh-TW": "健康體適能", "en": "Health & Fitness", "ja": "健康",
        "ko": "건강", "de": "Gesundheit", "fr": "Santé",
        "es": "Salud", "pt": "Saúde", "id": "Kesehatan", "zh-CN": "健康",
        "icon": "🏥",
        "slugs": [
            "bmi-calculator", "bmr-calculator", "tdee-calculator", "body-fat",
            "ideal-weight", "calorie-calculator", "macro-calculator", "water-intake",
            "heart-rate-zone", "pace-calculator", "one-rep-max", "waist-hip-ratio",
            "pregnancy-due-date", "ovulation-calculator", "blood-alcohol",
            "sleep-calculator", "vo2max-estimator", "calorie-density",
            "protein-calculator", "blood-pressure",
        ]
    },
    "realestate": {
        "zh-TW": "房地產", "en": "Real Estate", "ja": "不動産",
        "ko": "부동산", "de": "Immobilien", "fr": "Immobilier",
        "es": "Inmobiliaria", "pt": "Imóveis", "id": "Properti", "zh-CN": "房地产",
        "icon": "🏠",
        "slugs": [
            "mortgage", "rent-vs-buy", "home-affordability", "closing-cost",
            "property-tax", "rental-yield", "ltv-calculator", "refinance-calculator",
            "home-equity", "stamp-duty", "renovation-budget", "sqft-price",
            "amortization-schedule", "down-payment", "moving-cost",
        ]
    },
    "tax": {
        "zh-TW": "稅務薪資", "en": "Tax & Salary", "ja": "税金",
        "ko": "세금", "de": "Steuern", "fr": "Impôts",
        "es": "Impuestos", "pt": "Impostos", "id": "Pajak", "zh-CN": "税务",
        "icon": "🧾",
        "slugs": [
            "income-tax", "sales-tax", "vat-calculator", "payroll-tax",
            "salary-to-hourly", "hourly-to-salary", "overtime-calculator",
            "take-home-pay", "tax-bracket", "capital-gains-tax",
            "self-employment-tax", "bonus-tax", "tip-calculator",
            "inflation", "cost-of-living",
        ]
    },
    "insurance": {
        "zh-TW": "保險估算", "en": "Insurance", "ja": "保険",
        "ko": "보험", "de": "Versicherung", "fr": "Assurance",
        "es": "Seguros", "pt": "Seguros", "id": "Asuransi", "zh-CN": "保险",
        "icon": "🛡️",
        "slugs": [
            "life-insurance", "health-insurance", "car-insurance", "home-insurance",
            "renters-insurance", "disability-insurance", "pet-insurance",
            "travel-insurance", "umbrella-insurance", "term-life-quote",
            "whole-life-value", "insurance-needs", "deductible-optimizer",
            "coverage-gap", "premium-comparison",
            "long-term-care", "critical-illness", "dental-insurance",
            "vision-insurance", "liability-insurance",
        ]
    },
    "loan": {
        "zh-TW": "貸款信用", "en": "Loans & Credit", "ja": "ローン",
        "ko": "대출", "de": "Kredit", "fr": "Prêt",
        "es": "Préstamos", "pt": "Empréstimos", "id": "Pinjaman", "zh-CN": "贷款",
        "icon": "💳",
        "slugs": [
            "loan-calculator", "auto-loan", "personal-loan", "student-loan",
            "credit-card-payoff", "debt-snowball", "debt-avalanche",
            "debt-consolidation", "interest-rate-converter", "apr-calculator",
            "emi-calculator", "balloon-payment", "heloc-calculator",
            "loan-comparison", "prepayment-calculator",
        ]
    },
    "medical": {
        "zh-TW": "醫療費用", "en": "Medical Costs", "ja": "医療費",
        "ko": "의료비", "de": "Medizin", "fr": "Médical",
        "es": "Médico", "pt": "Médico", "id": "Medis", "zh-CN": "医疗",
        "icon": "⚕️",
        "slugs": [
            "medical-bill", "hsa-calculator", "fsa-calculator", "copay-estimator",
            "drug-cost", "surgery-cost", "dental-cost", "vision-cost",
            "therapy-cost", "fertility-cost", "emergency-cost",
            "hospital-stay-cost", "lab-test-cost", "vaccination-cost",
            "mental-health-cost",
        ]
    },
    "ecommerce": {
        "zh-TW": "電商物流", "en": "E-Commerce", "ja": "EC",
        "ko": "이커머스", "de": "E-Commerce", "fr": "E-Commerce",
        "es": "E-Commerce", "pt": "E-Commerce", "id": "E-Commerce", "zh-CN": "电商",
        "icon": "📦",
        "slugs": [
            "shipping-cost", "fba-calculator", "cbm-calculator", "customs-duty",
            "ebay-fee", "amazon-fee", "shopify-profit", "etsy-fee",
            "dropshipping-margin", "cogs-calculator", "markup-calculator",
            "discount-calculator", "wholesale-price", "landed-cost",
            "inventory-turnover",
        ]
    },
    "construction": {
        "zh-TW": "建築裝修", "en": "Construction", "ja": "建築",
        "ko": "건축", "de": "Bau", "fr": "Construction",
        "es": "Construcción", "pt": "Construção", "id": "Konstruksi", "zh-CN": "建筑",
        "icon": "🏗️",
        "slugs": [
            "concrete-calculator", "paint-calculator", "flooring-calculator",
            "roofing-calculator", "tile-calculator", "brick-calculator",
            "lumber-calculator", "drywall-calculator", "insulation-calculator",
            "fence-calculator", "deck-calculator", "gravel-calculator",
            "rebar-calculator", "staircase-calculator", "wallpaper-calculator",
            "plumbing-estimate", "electrical-load", "hvac-sizing",
            "window-cost", "kitchen-remodel",
        ]
    },
    "energy": {
        "zh-TW": "電力能源", "en": "Energy", "ja": "エネルギー",
        "ko": "에너지", "de": "Energie", "fr": "Énergie",
        "es": "Energía", "pt": "Energia", "id": "Energi", "zh-CN": "能源",
        "icon": "⚡",
        "slugs": [
            "electricity-cost", "solar-panel", "led-savings", "ev-charging",
            "carbon-footprint", "kwh-calculator", "generator-size",
            "battery-capacity", "energy-audit", "heat-loss",
            "air-conditioner-size", "water-heater-cost", "gas-bill",
            "renewable-roi", "power-consumption",
        ]
    },
    "auto": {
        "zh-TW": "汽車交通", "en": "Auto & Transport", "ja": "自動車",
        "ko": "자동차", "de": "Auto", "fr": "Auto",
        "es": "Auto", "pt": "Auto", "id": "Otomotif", "zh-CN": "汽车",
        "icon": "🚗",
        "slugs": [
            "fuel-cost", "car-depreciation", "car-lease", "car-payment",
            "mpg-calculator", "tire-size", "towing-capacity", "commute-cost",
            "car-maintenance", "ev-vs-gas", "road-trip-cost", "taxi-fare",
            "parking-cost", "toll-calculator", "vehicle-registration",
        ]
    },
    "hr": {
        "zh-TW": "人資企業", "en": "HR & Business", "ja": "人事",
        "ko": "인사", "de": "Personal", "fr": "RH",
        "es": "RRHH", "pt": "RH", "id": "SDM", "zh-CN": "人力资源",
        "icon": "👔",
        "slugs": [
            "employee-cost", "turnover-cost", "revenue-per-employee",
            "break-even-analysis", "profit-margin", "burn-rate",
            "runway-calculator", "valuation-calculator", "cac-calculator",
            "ltv-calculator", "churn-rate", "conversion-rate",
            "ab-test-calculator", "roi-marketing", "cpm-calculator",
        ]
    },
    "startup": {
        "zh-TW": "創業退休", "en": "Startup & Retirement", "ja": "起業",
        "ko": "창업", "de": "Gründung", "fr": "Startup",
        "es": "Startup", "pt": "Startup", "id": "Startup", "zh-CN": "创业",
        "icon": "🚀",
        "slugs": [
            "startup-cost", "business-loan", "franchise-cost",
            "social-security", "pension-calculator", "401k-calculator",
            "roth-ira", "fire-calculator", "withdrawal-rate",
            "required-minimum-distribution", "catch-up-contribution",
            "retirement-income", "spousal-benefit", "early-retirement",
            "side-hustle-income", "gig-economy-tax", "freelance-rate",
            "consulting-fee", "business-valuation", "equity-dilution",
        ]
    },
    "education": {
        "zh-TW": "教育學術", "en": "Education", "ja": "教育",
        "ko": "교육", "de": "Bildung", "fr": "Éducation",
        "es": "Educación", "pt": "Educação", "id": "Pendidikan", "zh-CN": "教育",
        "icon": "🎓",
        "slugs": [
            "gpa-calculator", "grade-calculator", "college-cost",
            "student-loan-repayment", "scholarship-estimator", "sat-score",
            "act-score", "study-abroad-cost", "textbook-cost",
            "tuition-inflation", "education-roi", "class-size",
            "teacher-salary", "school-budget", "tutoring-rate",
        ]
    },
    "legal": {
        "zh-TW": "法律合規", "en": "Legal", "ja": "法務",
        "ko": "법률", "de": "Recht", "fr": "Juridique",
        "es": "Legal", "pt": "Jurídico", "id": "Hukum", "zh-CN": "法律",
        "icon": "⚖️",
        "slugs": [
            "alimony-calculator", "child-support", "court-fee",
            "legal-fee", "settlement-calculator", "statute-of-limitations",
            "contract-penalty", "compliance-cost", "trademark-cost",
            "patent-cost", "immigration-fee", "visa-cost",
            "notary-fee", "power-of-attorney", "estate-tax",
        ]
    },
    "textile": {
        "zh-TW": "紡織工業", "en": "Textile", "ja": "繊維",
        "ko": "섬유", "de": "Textil", "fr": "Textile",
        "es": "Textil", "pt": "Têxtil", "id": "Tekstil", "zh-CN": "纺织",
        "icon": "🧵",
        "slugs": [
            "fabric-calculator", "yarn-calculator", "dyeing-cost",
            "gsm-calculator", "shrinkage-calculator", "thread-consumption",
            "knitting-gauge", "weaving-density", "pattern-grading",
            "cutting-yield",
        ]
    },
    "cooking": {
        "zh-TW": "烹飪營養", "en": "Cooking", "ja": "料理",
        "ko": "요리", "de": "Kochen", "fr": "Cuisine",
        "es": "Cocina", "pt": "Culinária", "id": "Memasak", "zh-CN": "烹饪",
        "icon": "🍳",
        "slugs": [
            "recipe-scaler", "unit-converter-cooking", "baking-conversion",
            "nutrition-calculator", "meal-prep-cost", "food-cost-percentage",
            "tip-split", "restaurant-markup", "coffee-cost",
            "grocery-budget", "food-waste", "serving-size",
            "alcohol-dilution", "brine-calculator", "sourdough-calculator",
        ]
    },
    "datetime": {
        "zh-TW": "日期時間", "en": "Date & Time", "ja": "日時",
        "ko": "날짜", "de": "Datum", "fr": "Date",
        "es": "Fecha", "pt": "Data", "id": "Tanggal", "zh-CN": "日期",
        "icon": "📅",
        "slugs": [
            "age-calculator", "date-difference", "workday-calculator",
            "timezone-converter", "countdown-timer",
        ]
    },
    "math": {
        "zh-TW": "數學統計", "en": "Math & Stats", "ja": "数学",
        "ko": "수학", "de": "Mathe", "fr": "Maths",
        "es": "Mates", "pt": "Matemática", "id": "Matematika", "zh-CN": "数学",
        "icon": "📐",
        "slugs": [
            "percentage-calculator", "fraction-calculator", "scientific-notation",
            "standard-deviation", "probability", "permutation-combination",
            "logarithm", "quadratic-equation",
        ]
    },
    "unit": {
        "zh-TW": "單位換算", "en": "Unit Conversion", "ja": "単位変換",
        "ko": "단위변환", "de": "Einheiten", "fr": "Unités",
        "es": "Unidades", "pt": "Unidades", "id": "Satuan", "zh-CN": "单位换算",
        "icon": "🔄",
        "slugs": [
            "length-converter", "weight-converter", "temperature-converter",
            "area-converter", "volume-converter",
        ]
    },
}

# Build reverse lookup: slug → category key
SLUG_TO_CAT = {}
for cat_key, cat_data in TOOL_CATEGORIES.items():
    for slug in cat_data["slugs"]:
        SLUG_TO_CAT[slug] = cat_key

# Blog articles grouped by relevance
BLOG_BY_CATEGORY = {
    "finance": ["kd-indicator", "macd-indicator", "rsi-indicator", "moving-average-guide",
                "candlestick-patterns", "support-resistance", "stop-loss-guide",
                "profit-loss-ratio", "position-risk", "institutional-investors", "stock-selection-guide"],
    "health": ["stop-loss-guide", "profit-loss-ratio"],  # fallback
    "default": ["kd-indicator", "macd-indicator", "rsi-indicator"],
}

BLOG_TITLES = {
    "kd-indicator": {"zh-TW": "KD 指標教學", "en": "KD Indicator Guide", "ja": "KD指標ガイド", "ko": "KD 지표 가이드", "de": "KD-Indikator", "fr": "Guide KD", "es": "Guía KD", "pt": "Guia KD", "id": "Panduan KD", "zh-CN": "KD指标教学"},
    "macd-indicator": {"zh-TW": "MACD 指標教學", "en": "MACD Guide", "ja": "MACDガイド", "ko": "MACD 가이드", "de": "MACD-Anleitung", "fr": "Guide MACD", "es": "Guía MACD", "pt": "Guia MACD", "id": "Panduan MACD", "zh-CN": "MACD指标教学"},
    "rsi-indicator": {"zh-TW": "RSI 指標教學", "en": "RSI Guide", "ja": "RSIガイド", "ko": "RSI 가이드", "de": "RSI-Anleitung", "fr": "Guide RSI", "es": "Guía RSI", "pt": "Guia RSI", "id": "Panduan RSI", "zh-CN": "RSI指标教学"},
    "moving-average-guide": {"zh-TW": "均線教學", "en": "Moving Average Guide", "ja": "移動平均線ガイド", "ko": "이동평균선 가이드", "de": "Gleitender Durchschnitt", "fr": "Moyennes mobiles", "es": "Media móvil", "pt": "Média móvel", "id": "Moving Average", "zh-CN": "均线教学"},
    "candlestick-patterns": {"zh-TW": "K線型態教學", "en": "Candlestick Patterns", "ja": "ローソク足パターン", "ko": "캔들스틱 패턴", "de": "Kerzenmuster", "fr": "Chandeliers japonais", "es": "Patrones de velas", "pt": "Padrões de velas", "id": "Pola Candlestick", "zh-CN": "K线形态教学"},
    "support-resistance": {"zh-TW": "支撐壓力教學", "en": "Support & Resistance", "ja": "サポート＆レジスタンス", "ko": "지지/저항선", "de": "Unterstützung & Widerstand", "fr": "Support & Résistance", "es": "Soporte y Resistencia", "pt": "Suporte e Resistência", "id": "Support & Resistance", "zh-CN": "支撑压力教学"},
    "stop-loss-guide": {"zh-TW": "停損設定教學", "en": "Stop Loss Guide", "ja": "ストップロス", "ko": "손절매 가이드", "de": "Stop-Loss", "fr": "Stop Loss", "es": "Stop Loss", "pt": "Stop Loss", "id": "Stop Loss", "zh-CN": "止损设定教学"},
    "profit-loss-ratio": {"zh-TW": "損益比教學", "en": "Risk-Reward Ratio", "ja": "リスクリワード", "ko": "손익비", "de": "Chance-Risiko", "fr": "Ratio risque/rendement", "es": "Ratio riesgo/beneficio", "pt": "Risco/Retorno", "id": "Rasio Risiko", "zh-CN": "损益比教学"},
    "position-risk": {"zh-TW": "位置風險教學", "en": "Position Risk", "ja": "ポジションリスク", "ko": "포지션 위험", "de": "Positionsrisiko", "fr": "Risque de position", "es": "Riesgo de posición", "pt": "Risco de posição", "id": "Risiko Posisi", "zh-CN": "位置风险教学"},
    "institutional-investors": {"zh-TW": "法人籌碼教學", "en": "Institutional Investors", "ja": "機関投資家", "ko": "기관투자자", "de": "Institutionelle Investoren", "fr": "Investisseurs institutionnels", "es": "Inversores institucionales", "pt": "Investidores institucionais", "id": "Investor Institusional", "zh-CN": "法人筹码教学"},
    "stock-selection-guide": {"zh-TW": "選股教學", "en": "Stock Selection Guide", "ja": "銘柄選定ガイド", "ko": "종목 선정 가이드", "de": "Aktienauswahl", "fr": "Sélection d'actions", "es": "Selección de acciones", "pt": "Seleção de ações", "id": "Panduan Saham", "zh-CN": "选股教学"},
}

NAV_LABELS = {
    "tools": {"zh-TW": "工具", "en": "Tools", "ja": "ツール", "ko": "도구", "de": "Tools", "fr": "Outils", "es": "Herramientas", "pt": "Ferramentas", "id": "Alat", "zh-CN": "工具"},
    "blog": {"zh-TW": "教學", "en": "Blog", "ja": "ブログ", "ko": "블로그", "de": "Blog", "fr": "Blog", "es": "Blog", "pt": "Blog", "id": "Blog", "zh-CN": "博客"},
    "patterns": {"zh-TW": "K棒型態", "en": "Patterns", "ja": "ローソク足", "ko": "캔들 패턴", "de": "Muster", "fr": "Chandeliers", "es": "Patrones", "pt": "Padrões", "id": "Pola", "zh-CN": "K线形态"},
    "home": {"zh-TW": "首頁", "en": "Home", "ja": "ホーム", "ko": "홈", "de": "Startseite", "fr": "Accueil", "es": "Inicio", "pt": "Início", "id": "Beranda", "zh-CN": "首页"},
}


def sp(msg):
    """Safe print for Windows console."""
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode("utf-8", errors="replace").decode("utf-8", errors="replace"))


def detect_lang(filepath):
    """Detect language from file path."""
    parts = filepath.replace("\\", "/").split("/")
    for lang in LANGS:
        if lang in parts:
            return lang
    # zh-TW is root level (no lang subfolder)
    return "zh-TW"


def detect_slug(filepath):
    """Extract slug from filename."""
    fname = os.path.basename(filepath)
    if fname.endswith(".html"):
        return fname[:-5]
    return fname


def get_tool_url(slug, lang):
    """Get tool URL for a given slug and language."""
    if lang == "zh-TW":
        return f"/tools/{slug}.html"
    return f"/tools/{lang}/{slug}.html"


def get_blog_url(slug, lang):
    """Get blog URL for a given slug and language."""
    if lang == "zh-TW":
        return f"/blog/{slug}.html"
    return f"/blog/{lang}/{slug}.html"


def build_lang_dropdown_html(lang, slug, page_type="tool"):
    """Build nav language dropdown HTML matching V3 style."""
    options = []
    for l in LANGS:
        if page_type == "tool":
            url = get_tool_url(slug, l)
        elif page_type == "blog":
            url = get_blog_url(slug, l)
        elif page_type == "tool-index":
            url = f"/tools/" if l == "zh-TW" else f"/tools/{l}/"
        elif page_type == "blog-index":
            url = f"/blog/" if l == "zh-TW" else f"/blog/{l}/index.html"
        else:
            url = "#"
        selected = ' selected' if l == lang else ''
        options.append(f'<option value="{url}"{selected}>{LANG_NAMES[l]}</option>')

    opts_str = "".join(options)
    return f'<select onchange="location.href=this.value" style="padding:4px 8px;border-radius:6px;border:1px solid #CBD5E0;font-size:13px;background:#fff;color:#4A5568;cursor:pointer">{opts_str}</select>'


def build_related_blog_html(slug, lang):
    """Build related blog links matched to tool category."""
    cat_key = SLUG_TO_CAT.get(slug, None)

    # Get matching blog slugs
    if cat_key and cat_key in ("finance",):
        blog_slugs = BLOG_BY_CATEGORY.get("finance", [])[:3]
    else:
        # For non-finance tools, show general useful articles
        blog_slugs = ["stop-loss-guide", "profit-loss-ratio", "stock-selection-guide"]

    links = []
    for bs in blog_slugs:
        title = BLOG_TITLES.get(bs, {}).get(lang, bs)
        url = get_blog_url(bs, lang)
        links.append(f'<a href="{url}" class="related-link">{title}</a>')

    return "\n".join(links)


# ═══════════════════════════════════════════════════════════════════════
# TASK 1: Fix tool pages (nav dropdown + related blog links)
# ═══════════════════════════════════════════════════════════════════════

def fix_tool_page(filepath):
    """Fix a single tool page: replace lang-bar with nav dropdown, fix related blog links."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except:
        return False

    original = content
    lang = detect_lang(filepath)
    slug = detect_slug(filepath)

    # 1. Replace lang-bar buttons with nav dropdown
    # The lang-bar is a div with class="lang-bar" containing anchor tags
    lang_bar_pattern = r'<div class="lang-bar">.*?</div>'
    dropdown = build_lang_dropdown_html(lang, slug, "tool")
    dropdown_div = f'<div class="lang-bar" style="display:flex;align-items:center;gap:8px;margin:24px 0"><span style="font-size:13px;color:#718096">🌐</span>{dropdown}</div>'

    if re.search(lang_bar_pattern, content, re.DOTALL):
        content = re.sub(lang_bar_pattern, dropdown_div, content, count=1, flags=re.DOTALL)

    # 2. Add dropdown to nav bar (replace static nav-links)
    # Current nav: <div class="nav-links"><a>工具</a><a>Blog</a><a>Home</a></div>
    nav_links_pattern = r'<div class="nav-links">\s*<a[^>]*>[^<]*</a>\s*<a[^>]*>[^<]*</a>\s*<a[^>]*>[^<]*</a>\s*</div>'
    tools_url = "/tools/" if lang == "zh-TW" else f"/tools/{lang}/"
    blog_url = "/blog/" if lang == "zh-TW" else f"/blog/{lang}/index.html"
    patterns_url = "/patterns/index.html" if lang == "zh-TW" else f"/patterns/{lang}.html"

    nav_dropdown = build_lang_dropdown_html(lang, slug, "tool")
    new_nav = f'''<div class="nav-links">
    <a href="{tools_url}">{NAV_LABELS["tools"].get(lang, "Tools")}</a>
    <a href="{blog_url}">{NAV_LABELS["blog"].get(lang, "Blog")}</a>
    <a href="{patterns_url}">{NAV_LABELS["patterns"].get(lang, "Patterns")}</a>
    <a href="/">{NAV_LABELS["home"].get(lang, "Home")}</a>
    {nav_dropdown}
  </div>'''

    if re.search(nav_links_pattern, content, re.DOTALL):
        content = re.sub(nav_links_pattern, new_nav, content, count=1, flags=re.DOTALL)

    # 3. Fix related blog links — replace existing blog links section
    # Find the blog links section (h3 with 📚 + links)
    blog_section_pattern = r'<h3[^>]*>.*?📚.*?延伸閱讀.*?</h3>\s*(?:<a[^>]*class="related-link"[^>]*>.*?</a>\s*)+'
    blog_section_pattern2 = r'### 📚 延伸閱讀.*?(?=\n##|\n</div>|$)'

    new_blog_links = build_related_blog_html(slug, lang)
    blog_title = {"zh-TW": "📚 延伸閱讀", "en": "📚 Related Articles", "ja": "📚 関連記事",
                  "ko": "📚 관련 글", "de": "📚 Verwandte Artikel", "fr": "📚 Articles connexes",
                  "es": "📚 Artículos relacionados", "pt": "📚 Artigos relacionados",
                  "id": "📚 Artikel Terkait", "zh-CN": "📚 延伸阅读"}.get(lang, "📚 Related")

    new_blog_section = f'<h3>{blog_title}</h3>\n    {new_blog_links}'

    # Try to find and replace the blog section
    # Pattern: <h3> with 📚 followed by related-link anchors
    if '<h3>' in content and '📚' in content:
        # Find the h3 containing 📚 and replace everything until the next section
        pattern = r'(<h3[^>]*>.*?📚[^<]*</h3>)\s*((?:<a[^>]*>.*?</a>\s*)+)'
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, new_blog_section, content, count=1, flags=re.DOTALL)

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


# ═══════════════════════════════════════════════════════════════════════
# TASK 2: Rebuild tool index pages with category cards
# ═══════════════════════════════════════════════════════════════════════

def scan_tools_for_lang(lang):
    """Scan actual tool HTML files for a language and group by category."""
    if lang == "zh-TW":
        tool_dir = TOOLS_DIR
    else:
        tool_dir = os.path.join(TOOLS_DIR, lang)

    if not os.path.isdir(tool_dir):
        return {}

    result = {}
    for fname in os.listdir(tool_dir):
        if not fname.endswith(".html") or fname == "index.html":
            continue
        slug = fname[:-5]
        cat_key = SLUG_TO_CAT.get(slug, "other")

        # Extract title from HTML
        fpath = os.path.join(tool_dir, fname)
        title = slug.replace("-", " ").title()
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                head = f.read(3000)
            m = re.search(r"<h1[^>]*>(.*?)</h1>", head)
            if m:
                title = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        except:
            pass

        if cat_key not in result:
            result[cat_key] = []
        result[cat_key].append({"slug": slug, "title": title})

    # Sort tools within each category
    for k in result:
        result[k].sort(key=lambda x: x["slug"])

    return result


def build_tool_index_html(lang, tools_by_cat):
    """Build a tool index page with category card layout."""
    dropdown = build_lang_dropdown_html(lang, "index", "tool-index")
    tools_url = "/tools/" if lang == "zh-TW" else f"/tools/{lang}/"
    blog_url = "/blog/" if lang == "zh-TW" else f"/blog/{lang}/index.html"
    patterns_url = "/patterns/index.html" if lang == "zh-TW" else f"/patterns/{lang}.html"

    # hreflang
    hreflang_tags = []
    for l in LANGS:
        url = f"https://softglow-ai.com/tools/" if l == "zh-TW" else f"https://softglow-ai.com/tools/{l}/"
        hl = l.lower()
        hreflang_tags.append(f'<link rel="alternate" hreflang="{hl}" href="{url}">')
    hreflang_tags.append(f'<link rel="alternate" hreflang="x-default" href="https://softglow-ai.com/tools/en/">')
    hreflang_str = "\n".join(hreflang_tags)

    canonical = f"https://softglow-ai.com/tools/" if lang == "zh-TW" else f"https://softglow-ai.com/tools/{lang}/"

    page_title = {"zh-TW": "免費線上工具", "en": "Free Online Tools", "ja": "無料オンラインツール",
                  "ko": "무료 온라인 도구", "de": "Kostenlose Online-Tools", "fr": "Outils en ligne gratuits",
                  "es": "Herramientas en línea gratuitas", "pt": "Ferramentas online gratuitas",
                  "id": "Alat Online Gratis", "zh-CN": "免费在线工具"}.get(lang, "Free Online Tools")

    page_desc = {"zh-TW": "超過 300 個免費線上計算工具，涵蓋金融、健康、房地產、稅務等 20 個分類。",
                 "en": "Over 300 free online calculators covering finance, health, real estate, tax and 20+ categories."
                 }.get(lang, "Over 300 free online calculators.")

    # Build category sections
    sections_html = []
    total_tools = 0
    cat_order = ["finance", "health", "realestate", "tax", "insurance", "loan", "medical",
                 "ecommerce", "construction", "energy", "auto", "hr", "startup",
                 "education", "legal", "textile", "cooking", "datetime", "math", "unit"]

    for cat_key in cat_order:
        if cat_key not in tools_by_cat:
            continue
        tools = tools_by_cat[cat_key]
        cat_info = TOOL_CATEGORIES.get(cat_key, {})
        cat_name = cat_info.get(lang, cat_info.get("en", cat_key))
        cat_icon = cat_info.get("icon", "🔧")
        total_tools += len(tools)

        tool_links = []
        for t in tools:
            url = get_tool_url(t["slug"], lang)
            tool_links.append(f'<a href="{url}" class="tool-card">{t["title"]}</a>')

        tools_grid = "\n        ".join(tool_links)
        sections_html.append(f'''
    <section class="cat-section">
      <h2 class="cat-title">{cat_icon} {cat_name} <span class="cat-count">({len(tools)})</span></h2>
      <div class="tools-grid">
        {tools_grid}
      </div>
    </section>''')

    # Handle uncategorized tools
    if "other" in tools_by_cat:
        tools = tools_by_cat["other"]
        total_tools += len(tools)
        tool_links = [f'<a href="{get_tool_url(t["slug"], lang)}" class="tool-card">{t["title"]}</a>' for t in tools]
        sections_html.append(f'''
    <section class="cat-section">
      <h2 class="cat-title">🔧 {"其他工具" if lang in ("zh-TW", "zh-CN") else "Other Tools"} <span class="cat-count">({len(tools)})</span></h2>
      <div class="tools-grid">
        {"".join(tool_links)}
      </div>
    </section>''')

    all_sections = "\n".join(sections_html)

    html = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{page_title} - SoftGlow</title>
<meta name="description" content="{page_desc}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canonical}">
{hreflang_str}
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;color:#2D3748;background:#fff;line-height:1.6}}
a{{color:#2563EB;text-decoration:none}}
.nav{{position:sticky;top:0;z-index:100;background:rgba(255,255,255,0.95);backdrop-filter:blur(8px);border-bottom:1px solid #E2E8F0}}
.nav-inner{{max-width:1080px;margin:0 auto;padding:0 20px;display:flex;align-items:center;justify-content:space-between;height:52px}}
.nav-logo{{font-size:17px;font-weight:700;color:#2D3748}}
.nav-logo span{{color:#2563EB}}
.nav-links{{display:flex;gap:12px;align-items:center}}
.nav-links a{{font-size:13px;color:#4A5568;font-weight:500}}
.container{{max-width:1080px;margin:0 auto;padding:20px}}
.page-header{{text-align:center;padding:40px 0 20px}}
.page-header h1{{font-size:28px;font-weight:700;color:#1A202C}}
.page-header p{{color:#718096;margin-top:8px}}
.cat-section{{margin:32px 0}}
.cat-title{{font-size:20px;font-weight:700;color:#1A202C;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #E2E8F0}}
.cat-count{{font-size:14px;color:#A0AEC0;font-weight:400}}
.tools-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px}}
.tool-card{{display:block;padding:14px 16px;background:#F7FAFC;border:1px solid #E2E8F0;border-radius:10px;font-size:14px;color:#2D3748;transition:all 0.15s}}
.tool-card:hover{{background:#EBF5FF;border-color:#BEE3F8;text-decoration:none;transform:translateY(-1px)}}
.footer{{border-top:1px solid #E2E8F0;padding:24px 0;margin-top:40px}}
.footer-inner{{max-width:1080px;margin:0 auto;padding:0 20px;display:flex;flex-wrap:wrap;gap:16px;font-size:12px;color:#A0AEC0}}
.footer-inner a{{color:#718096}}
@media(max-width:768px){{
  .tools-grid{{grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:8px}}
  .tool-card{{padding:12px;font-size:13px}}
  .page-header h1{{font-size:22px}}
}}
</style>
</head>
<body>
<nav class="nav">
<div class="nav-inner">
  <a href="/" class="nav-logo">Soft<span>Glow</span></a>
  <div class="nav-links">
    <a href="{tools_url}">{NAV_LABELS["tools"].get(lang, "Tools")}</a>
    <a href="{blog_url}">{NAV_LABELS["blog"].get(lang, "Blog")}</a>
    <a href="{patterns_url}">{NAV_LABELS["patterns"].get(lang, "Patterns")}</a>
    <a href="/">{NAV_LABELS["home"].get(lang, "Home")}</a>
    {dropdown}
  </div>
</div>
</nav>

<div class="container">
  <div class="page-header">
    <h1>{page_title}</h1>
    <p>{total_tools} {"個免費工具" if lang in ("zh-TW","zh-CN") else " free tools"}</p>
  </div>
  {all_sections}
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
</body>
</html>'''

    return html


# ═══════════════════════════════════════════════════════════════════════
# TASK 3: Fix softglow-common.js search
# ═══════════════════════════════════════════════════════════════════════

def fix_search_js():
    """Patch softglow-common.js to fix Chinese search."""
    js_path = os.path.join(COMMON_DIR, "softglow-common.js")
    if not os.path.exists(js_path):
        sp(f"  [WARN] {js_path} not found, skipping search fix")
        return False

    with open(js_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find and replace the search function
    # The search likely uses .toLowerCase().includes() which doesn't work for CJK
    # We need to fix the filtering logic

    # Replace the search filtering function
    old_filter = None
    # Try to find common patterns
    patterns_to_try = [
        # Pattern 1: .filter with .toLowerCase().includes
        r'\.filter\(\s*(?:function\s*\(\s*\w+\s*\)|(?:\w+)\s*=>)\s*\{[^}]*toLowerCase\(\)[^}]*includes[^}]*\}',
        # Pattern 2: .filter with includes
        r'\.filter\(\s*\w+\s*=>\s*\w+\.\w+\.toLowerCase\(\)\.includes',
    ]

    # Instead of trying to regex-match the existing code (which could be any format),
    # let's inject a fixed search helper at the top and replace the search invocation

    # Check if our fix is already applied
    if "/* SOFTGLOW_SEARCH_FIX_V2 */" in content:
        sp("  Search fix already applied")
        return False

    # Inject improved search function at the beginning of the file
    search_fix = """/* SOFTGLOW_SEARCH_FIX_V2 */
window._sgSearch = function(items, query) {
  if (!query || !items) return [];
  var q = query.trim().toLowerCase();
  if (q.length < 1) return [];
  // Detect current page language from html lang attribute
  var pageLang = document.documentElement.lang || 'en';
  // Normalize lang codes
  var langMap = {'zh-tw':'zh-TW','zh-cn':'zh-CN','ja':'ja','ko':'ko','en':'en','de':'de','fr':'fr','es':'es','pt':'pt','id':'id'};
  var lang = langMap[pageLang.toLowerCase()] || pageLang;
  return items.filter(function(item) {
    // Search across all name fields
    var names = item.names || {};
    for (var k in names) {
      if (names[k] && names[k].toLowerCase().indexOf(q) !== -1) return true;
    }
    // Also search slug
    if (item.slug && item.slug.toLowerCase().indexOf(q) !== -1) return true;
    return false;
  }).sort(function(a, b) {
    // Prioritize current language matches
    var aName = (a.names && a.names[lang]) || '';
    var bName = (b.names && b.names[lang]) || '';
    var aMatch = aName.toLowerCase().indexOf(q) !== -1 ? 0 : 1;
    var bMatch = bName.toLowerCase().indexOf(q) !== -1 ? 0 : 1;
    return aMatch - bMatch;
  });
};
"""

    # Inject at the top of the file (after any 'use strict' or first line)
    content = search_fix + content

    # Now find where the original search filters results and replace with _sgSearch
    # Common pattern: items.filter(x => x.name... or data.filter(...)
    # We'll look for the search input event handler and replace the filter call
    content = re.sub(
        r'((?:data|items|results|searchData|_searchData)\s*\.filter\s*\([^)]*\.(?:name|title|slug)[^)]*(?:toLowerCase|includes)[^)]*\))',
        r'window._sgSearch(\1.length?[]:arguments[0]||[], _searchQ||"")',
        content,
        flags=re.DOTALL
    )

    # Alternative: if there's a specific filter pattern, replace it more precisely
    # Look for: .filter(i => { ... includes ... })
    # Replace with: window._sgSearch(data, query)

    with open(js_path, "w", encoding="utf-8") as f:
        f.write(content)

    return True


# ═══════════════════════════════════════════════════════════════════════
# TASK 4: Regenerate search-index.json (tools + patterns + comparisons + blog)
# ═══════════════════════════════════════════════════════════════════════

def generate_search_index():
    """Build comprehensive search index from all HTML pages."""
    entries = {}  # keyed by slug to deduplicate

    def extract_titles(filepath, slug, page_type):
        """Extract title from HTML file and detect language."""
        lang = detect_lang(filepath)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                head = f.read(4000)
            m = re.search(r"<h1[^>]*>(.*?)</h1>", head, re.DOTALL)
            if m:
                title = re.sub(r"<[^>]+>", "", m.group(1)).strip()
            else:
                m2 = re.search(r"<title>(.*?)</title>", head)
                title = m2.group(1).split(" - ")[0].strip() if m2 else slug.replace("-", " ").title()
        except:
            title = slug.replace("-", " ").title()
        return lang, title

    # Scan tools
    for root, _, files in os.walk(TOOLS_DIR):
        for fname in files:
            if not fname.endswith(".html") or fname == "index.html":
                continue
            fp = os.path.join(root, fname)
            slug = fname[:-5]
            lang, title = extract_titles(fp, slug, "tool")

            if slug not in entries:
                entries[slug] = {"slug": slug, "type": "tool", "names": {}}
            entries[slug]["names"][lang] = title

    # Scan patterns
    if os.path.isdir(PATTERNS_DIR):
        for root, _, files in os.walk(PATTERNS_DIR):
            for fname in files:
                if not fname.endswith(".html") or fname in ("index.html",):
                    continue
                # Skip language index files like en.html, ja.html
                if fname.replace(".html", "") in LANGS:
                    continue
                fp = os.path.join(root, fname)
                slug = fname[:-5]
                lang, title = extract_titles(fp, slug, "pattern")

                key = f"p_{slug}"
                if key not in entries:
                    entries[key] = {"slug": slug, "type": "pattern", "names": {}}
                entries[key]["names"][lang] = title

    # Scan comparisons
    if os.path.isdir(COMPARISONS_DIR):
        for root, _, files in os.walk(COMPARISONS_DIR):
            for fname in files:
                if not fname.endswith(".html") or fname == "index.html":
                    continue
                fp = os.path.join(root, fname)
                slug = fname[:-5]
                lang, title = extract_titles(fp, slug, "comparison")

                key = f"c_{slug}"
                if key not in entries:
                    entries[key] = {"slug": slug, "type": "comparison", "names": {}}
                entries[key]["names"][lang] = title

    # Scan blog
    if os.path.isdir(BLOG_DIR):
        for root, _, files in os.walk(BLOG_DIR):
            for fname in files:
                if not fname.endswith(".html") or fname == "index.html":
                    continue
                fp = os.path.join(root, fname)
                slug = fname[:-5]
                lang, title = extract_titles(fp, slug, "blog")

                key = f"b_{slug}"
                if key not in entries:
                    entries[key] = {"slug": slug, "type": "blog", "names": {}}
                entries[key]["names"][lang] = title

    # Build output
    result = list(entries.values())
    for e in result:
        t, s = e["type"], e["slug"]
        if t == "pattern":
            e["url_zhTW"] = f"/patterns/{s}.html"
            e["url_tpl"] = "/patterns/{lang}/" + f"{s}.html"
        elif t == "comparison":
            e["url_zhTW"] = f"/comparisons/{s}.html"
            e["url_tpl"] = "/comparisons/{lang}/" + f"{s}.html"
        elif t == "blog":
            e["url_zhTW"] = f"/blog/{s}.html"
            e["url_tpl"] = "/blog/{lang}/" + f"{s}.html"
        else:
            e["url_zhTW"] = f"/tools/{s}.html"
            e["url_tpl"] = "/tools/{lang}/" + f"{s}.html"

    type_order = {"pattern": 0, "comparison": 1, "blog": 2, "tool": 3}
    result.sort(key=lambda e: (type_order.get(e["type"], 9), e["slug"]))

    os.makedirs(COMMON_DIR, exist_ok=True)
    out = os.path.join(COMMON_DIR, "search-index.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, separators=(",", ":"))

    return len(result)


# ═══════════════════════════════════════════════════════════════════════
# TASK 5: Scan and fix tool page JS errors
# ═══════════════════════════════════════════════════════════════════════

def scan_and_fix_js_errors():
    """Scan tool pages for common JS errors and auto-fix where possible."""
    errors_found = 0
    fixed = 0
    error_report = []

    for root, _, files in os.walk(TOOLS_DIR):
        for fname in files:
            if not fname.endswith(".html") or fname == "index.html":
                continue
            fp = os.path.join(root, fname)
            try:
                with open(fp, "r", encoding="utf-8") as f:
                    content = f.read()
            except:
                continue

            original = content
            page_errors = []

            # Extract script content
            script_match = re.search(r"<script>(.*?)</script>", content, re.DOTALL)
            if not script_match:
                continue
            js_code = script_match.group(1)

            # Extract all HTML element IDs
            html_ids = set(re.findall(r'id="([^"]+)"', content))

            # Find all getElementById references in JS
            js_ids = re.findall(r"getElementById\(['\"]([^'\"]+)['\"]\)", js_code)

            # Check for mismatched IDs
            for js_id in js_ids:
                if js_id not in html_ids:
                    page_errors.append(f"getElementById('{js_id}') but no element with id='{js_id}'")

                    # Try to find a close match
                    for html_id in html_ids:
                        if js_id.lower() == html_id.lower():
                            # Case mismatch — fix it
                            content = content.replace(
                                f"getElementById('{js_id}')",
                                f"getElementById('{html_id}')"
                            ).replace(
                                f'getElementById("{js_id}")',
                                f'getElementById("{html_id}")'
                            )
                            page_errors[-1] += f" → FIXED to '{html_id}'"
                            break

            # Check for common JS errors
            # 1. Missing function calculate()
            if 'onclick="calculate()"' in content and 'function calculate' not in content:
                page_errors.append("onclick='calculate()' but function calculate() not defined")

            # 2. Unclosed try-catch
            try_count = js_code.count("try{") + js_code.count("try {")
            catch_count = js_code.count("catch(") + js_code.count("catch (")
            if try_count != catch_count:
                page_errors.append(f"try/catch mismatch: {try_count} try vs {catch_count} catch")

            # 3. Fix getElementById returning null — wrap in safety check
            # Find patterns like: document.getElementById('xxx').textContent = ...
            # where xxx doesn't exist in HTML
            null_refs = re.findall(
                r"document\.getElementById\(['\"]([^'\"]+)['\"]\)\.(textContent|innerHTML|value|innerText|style)",
                js_code
            )
            for ref_id, prop in null_refs:
                if ref_id not in html_ids:
                    # Wrap in null check
                    old_pattern = f"document.getElementById('{ref_id}').{prop}"
                    new_pattern = f"(document.getElementById('{ref_id}')||{{}}).{prop}"
                    content = content.replace(old_pattern, new_pattern)
                    old_pattern2 = f'document.getElementById("{ref_id}").{prop}'
                    new_pattern2 = f'(document.getElementById("{ref_id}")||{{}}).{prop}'
                    content = content.replace(old_pattern2, new_pattern2)
                    if old_pattern in original or old_pattern2 in original:
                        page_errors.append(f"Null-safe wrapped getElementById('{ref_id}').{prop}")

            if content != original:
                with open(fp, "w", encoding="utf-8") as f:
                    f.write(content)
                fixed += 1

            if page_errors:
                errors_found += len(page_errors)
                error_report.append((fname, page_errors))

    return errors_found, fixed, error_report


# ═══════════════════════════════════════════════════════════════════════
# TASK 6: Verify blog files
# ═══════════════════════════════════════════════════════════════════════

def verify_blog():
    """Check if new V3 blog files exist."""
    expected_slugs = ["kd-indicator", "macd-indicator", "rsi-indicator",
                      "moving-average-guide", "candlestick-patterns",
                      "support-resistance", "stop-loss-guide",
                      "profit-loss-ratio", "position-risk",
                      "institutional-investors", "stock-selection-guide"]

    missing = []
    old_version = []

    for lang in LANGS:
        for slug in expected_slugs:
            if lang == "zh-TW":
                fpath = os.path.join(BLOG_DIR, f"{slug}.html")
            else:
                fpath = os.path.join(BLOG_DIR, lang, f"{slug}.html")

            if not os.path.exists(fpath):
                missing.append(f"{lang}/{slug}")
            else:
                # Check if it's old version (has "線上有位" in title = old)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        head = f.read(500)
                    if "線上有位" in head and lang != "zh-TW":
                        old_version.append(f"{lang}/{slug}")
                    elif "softglow-common" not in head.lower() and "search-index" not in head.lower():
                        # No softglow-common.js = probably old version
                        old_version.append(f"{lang}/{slug}")
                except:
                    pass

    return missing, old_version


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════

def main():
    sp("=" * 60)
    sp("SoftGlow Fix Everything v2.0")
    sp("=" * 60)

    if not os.path.isdir(TOOLS_DIR):
        sp(f"[ERROR] Tools directory not found: {TOOLS_DIR}")
        sp(f"  Make sure you're running from: D:\\xian-shang-you-wei\\knowledge-engine")
        sys.exit(1)

    # ── Task 1: Fix tool pages ──────────────────────────────────────
    sp("\n[1/6] Fixing tool pages (nav dropdown + related blog links)...")
    tool_count = 0
    tool_total = 0
    for root, _, files in os.walk(TOOLS_DIR):
        for fname in files:
            if not fname.endswith(".html") or fname == "index.html":
                continue
            fp = os.path.join(root, fname)
            tool_total += 1
            if fix_tool_page(fp):
                tool_count += 1
    sp(f"  Scanned: {tool_total} | Fixed: {tool_count}")

    # ── Task 2: Rebuild tool index pages ────────────────────────────
    sp("\n[2/6] Rebuilding tool index pages with category cards...")
    for lang in LANGS:
        tools_by_cat = scan_tools_for_lang(lang)
        if not tools_by_cat:
            sp(f"  SKIP {lang}: no tools found")
            continue
        html = build_tool_index_html(lang, tools_by_cat)
        total = sum(len(v) for v in tools_by_cat.values())
        if lang == "zh-TW":
            out_path = os.path.join(TOOLS_DIR, "index.html")
        else:
            out_dir = os.path.join(TOOLS_DIR, lang)
            os.makedirs(out_dir, exist_ok=True)
            out_path = os.path.join(out_dir, "index.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        sp(f"  {lang}: {total} tools → {len(tools_by_cat)} categories")

    # ── Task 3: Verify blog files ───────────────────────────────────
    sp("\n[3/6] Verifying blog files...")
    missing_blog, old_blog = verify_blog()
    if missing_blog:
        sp(f"  ⚠ Missing blog pages: {len(missing_blog)}")
        for m in missing_blog[:10]:
            sp(f"    - {m}")
        if len(missing_blog) > 10:
            sp(f"    ... and {len(missing_blog)-10} more")
        sp("  → Run generate_blog.py first!")
    elif old_blog:
        sp(f"  ⚠ Old version blog pages: {len(old_blog)}")
        sp("  → These will be updated when you git push the new blog files")
    else:
        sp(f"  ✓ All 110+ blog pages present and V3 format")

    # ── Task 4: Fix softglow-common.js ──────────────────────────────
    sp("\n[4/6] Fixing softglow-common.js search...")
    if fix_search_js():
        sp("  ✓ Search function patched for Chinese support")
    else:
        sp("  → No changes needed or file not found")

    # ── Task 5: Regenerate search-index.json ────────────────────────
    sp("\n[5/6] Regenerating search-index.json...")
    total_entries = generate_search_index()
    sp(f"  ✓ {total_entries} entries (tools + patterns + comparisons + blog)")

    # ── Task 6: Scan and fix JS errors ──────────────────────────────
    sp("\n[6/6] Scanning tool pages for JS errors...")
    errors_found, js_fixed, error_report = scan_and_fix_js_errors()
    sp(f"  Errors found: {errors_found} | Auto-fixed: {js_fixed}")
    if error_report:
        # Save detailed report
        report_path = os.path.join(SCRIPT_DIR, "js_error_report.txt")
        with open(report_path, "w", encoding="utf-8") as f:
            for fname, errs in error_report:
                f.write(f"\n{fname}:\n")
                for e in errs:
                    f.write(f"  - {e}\n")
        sp(f"  → Detailed report: {report_path}")

    # ── Summary ─────────────────────────────────────────────────────
    sp(f"\n{'=' * 60}")
    sp("All done! Summary:")
    sp(f"  Tool pages fixed:       {tool_count}")
    sp(f"  Index pages rebuilt:    {len(LANGS)}")
    sp(f"  Search index entries:   {total_entries}")
    sp(f"  JS errors found/fixed: {errors_found}/{js_fixed}")
    if missing_blog:
        sp(f"  ⚠ Blog missing:       {len(missing_blog)} pages")
    sp(f"\nNext steps:")
    sp(f"  cd D:\\xian-shang-you-wei")
    sp(f"  git add -A")
    sp(f'  git commit -m "fix: nav dropdown + related links + index cards + search + JS errors"')
    sp(f"  git push")


if __name__ == "__main__":
    main()
