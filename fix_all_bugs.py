#!/usr/bin/env python3
"""
SoftGlow 全站 Bug 修復腳本 — 一次到位
=============================================
修復項目：
  B2: 掃描工具頁 JS 錯誤 + 自動修復可修的
  B3: 延伸閱讀改為按分類匹配
  B4: 重建所有語言的工具索引頁（35→323+ 工具）
  B5: 語言選擇器統一（移除 vi/th，加入 zh-CN/fr）

用法：
  cd D:\\xian-shang-you-wei
  python fix_all_bugs.py

  或指定路徑：
  python fix_all_bugs.py --root "D:\\xian-shang-you-wei"
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from collections import defaultdict
from html.parser import HTMLParser

# ============================================================
# 0. 自動偵測專案路徑
# ============================================================

CANDIDATE_ROOTS = [
    r"D:\xian-shang-you-wei",
    r"C:\xian-shang-you-wei",
    r"E:\xian-shang-you-wei",
    os.path.expanduser("~/xian-shang-you-wei"),
    os.path.dirname(os.path.abspath(__file__)),  # 腳本所在目錄
    os.getcwd(),  # 當前工作目錄
]

def find_project_root(override=None):
    """自動尋找專案根目錄"""
    if override and os.path.isdir(override):
        tools_dir = os.path.join(override, "backend", "frontend", "tools")
        if os.path.isdir(tools_dir):
            return override
        # 也許直接指向 backend 或 frontend
        tools_dir2 = os.path.join(override, "frontend", "tools")
        if os.path.isdir(tools_dir2):
            return override

    for root in CANDIDATE_ROOTS:
        tools_dir = os.path.join(root, "backend", "frontend", "tools")
        if os.path.isdir(tools_dir):
            return root
    
    # 往上找
    current = os.path.abspath(__file__) if '__file__' in dir() else os.getcwd()
    for _ in range(5):
        current = os.path.dirname(current)
        tools_dir = os.path.join(current, "backend", "frontend", "tools")
        if os.path.isdir(tools_dir):
            return current
    
    return None

# ============================================================
# 1. 常數定義
# ============================================================

# 正確的 10 語言
LANGUAGES = {
    "zh-TW": {"name": "繁體中文", "flag": "🇹🇼", "path": "", "nav_tools": "財務工具", "nav_blog": "教學", "nav_patterns": "K線型態", "nav_home": "首頁"},
    "en":    {"name": "English",   "flag": "🇺🇸", "path": "en/", "nav_tools": "Tools", "nav_blog": "Blog", "nav_patterns": "Patterns", "nav_home": "Home"},
    "ja":    {"name": "日本語",    "flag": "🇯🇵", "path": "ja/", "nav_tools": "ツール", "nav_blog": "記事", "nav_patterns": "ローソク足", "nav_home": "ホーム"},
    "ko":    {"name": "한국어",    "flag": "🇰🇷", "path": "ko/", "nav_tools": "도구", "nav_blog": "블로그", "nav_patterns": "캔들패턴", "nav_home": "홈"},
    "de":    {"name": "Deutsch",   "flag": "🇩🇪", "path": "de/", "nav_tools": "Tools", "nav_blog": "Blog", "nav_patterns": "Kerzenmuster", "nav_home": "Startseite"},
    "fr":    {"name": "Français",  "flag": "🇫🇷", "path": "fr/", "nav_tools": "Outils", "nav_blog": "Blog", "nav_patterns": "Chandeliers", "nav_home": "Accueil"},
    "es":    {"name": "Español",   "flag": "🇪🇸", "path": "es/", "nav_tools": "Herramientas", "nav_blog": "Blog", "nav_patterns": "Patrones", "nav_home": "Inicio"},
    "pt":    {"name": "Português", "flag": "🇧🇷", "path": "pt/", "nav_tools": "Ferramentas", "nav_blog": "Blog", "nav_patterns": "Padrões", "nav_home": "Início"},
    "id":    {"name": "Indonesia", "flag": "🇮🇩", "path": "id/", "nav_tools": "Alat", "nav_blog": "Blog", "nav_patterns": "Pola", "nav_home": "Beranda"},
    "zh-CN": {"name": "简体中文",  "flag": "🇨🇳", "path": "zh-CN/", "nav_tools": "工具", "nav_blog": "博客", "nav_patterns": "K线形态", "nav_home": "首页"},
}

# 錯誤的語言（要移除）
WRONG_LANGUAGES = ["vi", "th"]

# 語言選擇器 HTML（nav 下拉式）
def build_lang_dropdown_html(current_lang, page_type="tool", slug=""):
    """生成統一的語言下拉選擇器"""
    items = []
    for lang_code, info in LANGUAGES.items():
        if page_type == "index":
            if lang_code == "zh-TW":
                href = "/tools/"
            else:
                href = f"/tools/{info['path']}"
        else:
            if lang_code == "zh-TW":
                href = f"/tools/{slug}.html"
            else:
                href = f"/tools/{info['path']}{slug}.html"
        
        active = ' class="active"' if lang_code == current_lang else ''
        items.append(f'<a href="{href}"{active}>{info["flag"]} {info["name"]}</a>')
    
    return "\n".join(items)

# 20 個工具分類 — 關鍵字對應
CATEGORY_KEYWORDS = {
    "investment": {
        "zh-TW": "投資理財", "en": "Investment & Finance", "ja": "投資・資産運用",
        "ko": "투자 & 금융", "de": "Investition & Finanzen", "fr": "Investissement & Finance",
        "es": "Inversión y Finanzas", "pt": "Investimento & Finanças",
        "id": "Investasi & Keuangan", "zh-CN": "投资理财",
        "slugs": ["compound-interest", "roi-calculator", "dividend-yield", "dca-calculator",
                  "cagr", "sharpe-ratio", "rule-of-72", "asset-allocation", "stock-gain-loss",
                  "average-down", "dcf-calculator", "intrinsic-value", "pe-ratio",
                  "kelly-criterion", "portfolio-rebalance", "bond-yield", "bond-duration",
                  "preferred-stock-yield", "stock-return", "mutual-fund-fee",
                  "etf-expense-ratio", "investment-growth", "systematic-withdrawal",
                  "wealth-tax", "capital-gains-tax", "real-return", "inflation-adjusted-return",
                  "future-value", "present-value", "annuity-income", "perpetuity-value",
                  "time-value-money", "weighted-average-cost-capital", "earnings-per-share",
                  "price-to-book", "price-to-sales", "ev-ebitda", "free-cash-flow",
                  "net-asset-value", "alpha-calculator", "beta-calculator", "treynor-ratio",
                  "sortino-ratio", "information-ratio", "tracking-error", "max-drawdown",
                  "var-calculator", "monte-carlo-simulation"]
    },
    "trading": {
        "zh-TW": "交易工具", "en": "Trading Tools", "ja": "トレーディング",
        "ko": "트레이딩", "de": "Trading-Tools", "fr": "Outils de Trading",
        "es": "Trading", "pt": "Trading", "id": "Alat Trading", "zh-CN": "交易工具",
        "slugs": ["risk-reward", "position-size", "stop-loss", "margin-calculator",
                  "options-profit", "pip-value", "trading-fee", "stock-split",
                  "break-even", "margin-call", "lot-size", "spread-calculator",
                  "swap-calculator", "profit-loss", "drawdown-calculator"]
    },
    "technical": {
        "zh-TW": "技術分析", "en": "Technical Analysis", "ja": "テクニカル分析",
        "ko": "기술적 분석", "de": "Technische Analyse", "fr": "Analyse Technique",
        "es": "Análisis Técnico", "pt": "Análise Técnica",
        "id": "Analisis Teknikal", "zh-CN": "技术分析",
        "slugs": ["fibonacci-retracement", "pivot-point", "rsi-calculator",
                  "macd-calculator", "bollinger-bands", "atr-calculator",
                  "ma-crossover", "candlestick-identifier", "support-resistance",
                  "stochastic-oscillator", "williams-r", "cci-calculator",
                  "ichimoku-cloud", "parabolic-sar", "adx-calculator",
                  "obv-calculator", "vwap-calculator", "elliott-wave",
                  "gann-calculator", "heikin-ashi"]
    },
    "realestate": {
        "zh-TW": "房地產與房貸", "en": "Real Estate & Mortgage", "ja": "不動産・住宅ローン",
        "ko": "부동산 & 모기지", "de": "Immobilien & Hypothek", "fr": "Immobilier & Hypothèque",
        "es": "Inmobiliario & Hipoteca", "pt": "Imóveis & Hipoteca",
        "id": "Properti & Hipotek", "zh-CN": "房地产与房贷",
        "slugs": ["mortgage", "mortgage-refinance", "home-affordability", "rent-vs-buy",
                  "rental-yield", "property-tax", "home-equity", "amortization",
                  "down-payment", "closing-cost", "heloc-calculator", "home-value",
                  "cap-rate", "cash-on-cash", "gross-rent-multiplier"]
    },
    "tax": {
        "zh-TW": "稅務薪資", "en": "Tax & Salary", "ja": "税金・給与",
        "ko": "세금 & 급여", "de": "Steuern & Gehalt", "fr": "Impôts & Salaire",
        "es": "Impuestos & Salario", "pt": "Impostos & Salário",
        "id": "Pajak & Gaji", "zh-CN": "税务薪资",
        "slugs": ["income-tax", "take-home-pay", "salary-raise", "overtime-pay",
                  "freelance-tax", "self-employment-tax", "payroll-tax",
                  "sales-tax", "vat-calculator", "tax-bracket",
                  "effective-tax-rate", "marginal-tax-rate", "w4-calculator",
                  "1099-tax", "bonus-tax"]
    },
    "insurance": {
        "zh-TW": "保險估算", "en": "Insurance", "ja": "保険",
        "ko": "보험", "de": "Versicherung", "fr": "Assurance",
        "es": "Seguros", "pt": "Seguros", "id": "Asuransi", "zh-CN": "保险估算",
        "slugs": ["life-insurance-needs", "life-insurance-calc", "car-insurance-calc",
                  "health-insurance-estimate", "health-insurance-calc",
                  "renters-insurance", "homeowners-insurance",
                  "business-insurance", "disability-insurance",
                  "critical-illness-calc", "coverage-gap-finder",
                  "pet-insurance", "umbrella-insurance", "travel-insurance-calc",
                  "long-term-care", "dental-cost-calculator",
                  "insurance-needs", "term-life-quote", "whole-life-quote",
                  "insurance-premium"]
    },
    "loan": {
        "zh-TW": "貸款信用", "en": "Loans & Credit", "ja": "ローン・クレジット",
        "ko": "대출 & 신용", "de": "Kredite", "fr": "Prêts & Crédit",
        "es": "Préstamos & Crédito", "pt": "Empréstimos & Crédito",
        "id": "Pinjaman & Kredit", "zh-CN": "贷款信用",
        "slugs": ["car-loan", "personal-loan", "student-loan", "loan-comparison",
                  "credit-card-payoff", "debt-snowball", "debt-avalanche",
                  "debt-consolidation", "loan-refinance", "auto-lease",
                  "line-of-credit", "interest-rate-converter",
                  "emi-calculator", "loan-to-value", "debt-to-income"]
    },
    "retirement": {
        "zh-TW": "創業與退休", "en": "Business & Retirement", "ja": "起業・退休",
        "ko": "창업 & 은퇴", "de": "Gründung & Ruhestand", "fr": "Entreprise & Retraite",
        "es": "Empresa & Jubilación", "pt": "Negócio & Aposentadoria",
        "id": "Bisnis & Pensiun", "zh-CN": "创业与退休",
        "slugs": ["retirement", "401k-contribution", "roth-ira", "pension-calculator",
                  "social-security", "fire-calculator", "savings-goal",
                  "emergency-fund", "net-worth", "startup-cost-estimator",
                  "startup-valuation", "business-loan", "profit-margin",
                  "markup-calculator", "cash-flow-forecast",
                  "revenue-growth", "customer-lifetime-value",
                  "break-even-business", "payback-period", "roi-business"]
    },
    "health": {
        "zh-TW": "健康體適能", "en": "Health & Fitness", "ja": "健康・フィットネス",
        "ko": "건강 & 피트니스", "de": "Gesundheit & Fitness", "fr": "Santé & Fitness",
        "es": "Salud & Fitness", "pt": "Saúde & Fitness",
        "id": "Kesehatan & Kebugaran", "zh-CN": "健康体适能",
        "slugs": ["bmi-calculator", "bmr-calculator", "calorie-calculator",
                  "body-fat", "ideal-weight", "heart-rate-zone",
                  "pace-calculator", "one-rep-max", "protein-intake",
                  "water-intake", "sleep-calculator", "macro-calculator",
                  "waist-hip-ratio", "vo2max", "pregnancy-due-date",
                  "ovulation-calculator", "blood-alcohol", "steps-to-calories",
                  "running-calorie", "cycling-calorie"]
    },
    "medical": {
        "zh-TW": "醫療費用", "en": "Medical Costs", "ja": "医療費",
        "ko": "의료비", "de": "Medizinische Kosten", "fr": "Coûts Médicaux",
        "es": "Costos Médicos", "pt": "Custos Médicos",
        "id": "Biaya Medis", "zh-CN": "医疗费用",
        "slugs": ["medical-cost-estimator", "surgery-cost-estimator",
                  "hospital-stay-cost", "medication-cost",
                  "health-savings-account", "hsa-calculator",
                  "fsa-calculator", "copay-calculator",
                  "deductible-tracker", "out-of-pocket-max",
                  "medical-debt", "healthcare-cost-compare",
                  "prescription-savings", "medical-leave-pay",
                  "nursing-home-cost"]
    },
    "ecommerce": {
        "zh-TW": "電商物流", "en": "E-Commerce & Logistics", "ja": "EC・物流",
        "ko": "이커머스", "de": "E-Commerce & Logistik", "fr": "E-Commerce & Logistique",
        "es": "E-Commerce & Logística", "pt": "E-Commerce & Logística",
        "id": "E-Commerce & Logistik", "zh-CN": "电商物流",
        "slugs": ["fba-fee", "shipping-cost", "customs-duty", "dropship-profit",
                  "ebay-fee", "etsy-fee", "shopify-profit", "amazon-roi",
                  "product-pricing", "wholesale-markup", "inventory-turnover",
                  "order-fulfillment-cost", "return-rate", "conversion-rate",
                  "average-order-value"]
    },
    "construction": {
        "zh-TW": "建築裝修", "en": "Construction & Renovation", "ja": "建築・リフォーム",
        "ko": "건설 & 인테리어", "de": "Bau & Renovierung", "fr": "Construction & Rénovation",
        "es": "Construcción & Renovación", "pt": "Construção & Reforma",
        "id": "Konstruksi & Renovasi", "zh-CN": "建筑装修",
        "slugs": ["paint-calculator", "tile-calculator", "flooring-calculator",
                  "concrete-calculator", "lumber-calculator", "roofing-calculator",
                  "fence-calculator", "deck-calculator", "drywall-calculator",
                  "insulation-calculator", "carpet-calculator", "wallpaper-calculator",
                  "gravel-calculator", "mulch-calculator", "brick-calculator",
                  "staircase-calculator", "pool-volume", "renovation-cost",
                  "contractor-markup", "square-footage"]
    },
    "energy": {
        "zh-TW": "電力能源", "en": "Energy & Utilities", "ja": "エネルギー",
        "ko": "에너지", "de": "Energie", "fr": "Énergie",
        "es": "Energía", "pt": "Energia", "id": "Energi", "zh-CN": "电力能源",
        "slugs": ["electricity-cost", "solar-panel", "solar-roi",
                  "ev-charging-cost", "ev-savings", "energy-efficiency",
                  "carbon-footprint", "water-bill", "gas-bill",
                  "hvac-calculator", "led-savings", "battery-calculator",
                  "generator-size", "power-consumption", "kwh-calculator"]
    },
    "auto": {
        "zh-TW": "汽車交通", "en": "Auto & Transport", "ja": "自動車・交通",
        "ko": "자동차", "de": "Auto & Verkehr", "fr": "Auto & Transport",
        "es": "Auto & Transporte", "pt": "Auto & Transporte",
        "id": "Otomotif & Transportasi", "zh-CN": "汽车交通",
        "slugs": ["fuel-cost", "gas-mileage", "car-depreciation",
                  "car-lease-calculator", "car-payment", "car-affordability",
                  "total-cost-ownership", "tire-size", "towing-capacity",
                  "commute-cost", "ride-share-cost", "parking-cost",
                  "license-renewal", "vehicle-tax", "mileage-reimbursement"]
    },
    "hr": {
        "zh-TW": "人資企業", "en": "HR & Business", "ja": "人事・企業",
        "ko": "인사 & 기업", "de": "HR & Unternehmen", "fr": "RH & Entreprise",
        "es": "RRHH & Empresa", "pt": "RH & Empresa",
        "id": "SDM & Bisnis", "zh-CN": "人资企业",
        "slugs": ["employee-cost", "turnover-cost", "hiring-cost",
                  "benefit-cost", "productivity-calculator", "absenteeism-cost",
                  "training-roi", "salary-benchmark", "commission-calculator",
                  "bonus-calculator", "severance-pay", "labor-cost",
                  "headcount-planning", "retention-rate", "time-to-hire"]
    },
    "education": {
        "zh-TW": "教育學術", "en": "Education", "ja": "教育",
        "ko": "교육", "de": "Bildung", "fr": "Éducation",
        "es": "Educación", "pt": "Educação", "id": "Pendidikan", "zh-CN": "教育学术",
        "slugs": ["gpa-calculator", "grade-calculator", "college-cost",
                  "student-loan-payoff", "scholarship-calculator",
                  "study-abroad-cost", "tuition-comparison",
                  "education-roi", "student-budget", "textbook-cost",
                  "sat-score", "act-score", "class-rank",
                  "credit-hour-cost", "graduation-countdown"]
    },
    "cooking": {
        "zh-TW": "烹飪營養", "en": "Cooking & Nutrition", "ja": "料理・栄養",
        "ko": "요리 & 영양", "de": "Kochen & Ernährung", "fr": "Cuisine & Nutrition",
        "es": "Cocina & Nutrición", "pt": "Culinária & Nutrição",
        "id": "Masak & Nutrisi", "zh-CN": "烹饪营养",
        "slugs": ["recipe-scaler", "cooking-conversion", "baking-ratio",
                  "meal-cost", "grocery-budget", "food-waste",
                  "portion-size", "nutrition-label", "caffeine-calculator",
                  "alcohol-unit", "tip-calculator-food", "catering-cost",
                  "food-cost-percentage", "menu-pricing", "recipe-nutrition"]
    },
    "datetime": {
        "zh-TW": "日期時間", "en": "Date & Time", "ja": "日付・時間",
        "ko": "날짜 & 시간", "de": "Datum & Zeit", "fr": "Date & Heure",
        "es": "Fecha & Hora", "pt": "Data & Hora",
        "id": "Tanggal & Waktu", "zh-CN": "日期时间",
        "slugs": ["age-calculator", "date-difference", "business-days",
                  "countdown-timer", "timezone-converter"]
    },
    "math": {
        "zh-TW": "數學統計", "en": "Math & Statistics", "ja": "数学・統計",
        "ko": "수학 & 통계", "de": "Mathematik & Statistik", "fr": "Maths & Statistiques",
        "es": "Matemáticas & Estadísticas", "pt": "Matemática & Estatística",
        "id": "Matematika & Statistik", "zh-CN": "数学统计",
        "slugs": ["percentage-calculator", "fraction-calculator", "ratio-calculator",
                  "standard-deviation", "probability-calculator",
                  "compound-growth", "logarithm-calculator", "scientific-notation"]
    },
    "unit": {
        "zh-TW": "單位換算", "en": "Unit Conversion", "ja": "単位変換",
        "ko": "단위 변환", "de": "Einheitenumrechnung", "fr": "Conversion d'Unités",
        "es": "Conversión de Unidades", "pt": "Conversão de Unidades",
        "id": "Konversi Satuan", "zh-CN": "单位换算",
        "slugs": ["currency-converter", "length-converter", "weight-converter",
                  "temperature-converter", "volume-converter"]
    },
    "textile": {
        "zh-TW": "紡織工業", "en": "Textile Industry", "ja": "繊維産業",
        "ko": "섬유 산업", "de": "Textilindustrie", "fr": "Industrie Textile",
        "es": "Industria Textil", "pt": "Indústria Têxtil",
        "id": "Industri Tekstil", "zh-CN": "纺织工业",
        "slugs": ["fabric-calculator", "yarn-calculator", "dyeing-cost",
                  "gsm-calculator", "thread-count", "sewing-yardage",
                  "knitting-gauge", "pattern-grading", "textile-weight",
                  "shrinkage-calculator"]
    },
    "legal": {
        "zh-TW": "法律合規", "en": "Legal & Compliance", "ja": "法務",
        "ko": "법률", "de": "Recht & Compliance", "fr": "Juridique",
        "es": "Legal", "pt": "Jurídico", "id": "Hukum", "zh-CN": "法律合规",
        "slugs": ["court-fee", "legal-fee", "settlement-calculator",
                  "child-support", "alimony-calculator", "probate-cost",
                  "trademark-cost", "patent-cost", "llc-cost",
                  "incorporation-cost", "notary-fee", "contract-value",
                  "statute-limitations", "fine-calculator", "bail-calculator"]
    },
}

# Blog 文章對應分類
BLOG_ARTICLES = {
    "finance_trading": [
        {"slug": "kd-indicator", "zh-TW": "KD 指標教學", "en": "KD Indicator Guide"},
        {"slug": "macd-indicator", "zh-TW": "MACD 指標教學", "en": "MACD Guide"},
        {"slug": "rsi-indicator", "zh-TW": "RSI 指標教學", "en": "RSI Guide"},
    ],
    "general_finance": [
        {"slug": "stop-loss-guide", "zh-TW": "停損設定教學", "en": "Stop Loss Strategy"},
        {"slug": "profit-loss-ratio", "zh-TW": "損益比教學", "en": "Profit/Loss Ratio Guide"},
        {"slug": "stock-selection-guide", "zh-TW": "選股指南", "en": "Stock Selection Guide"},
    ],
    "technical_analysis": [
        {"slug": "moving-average-guide", "zh-TW": "均線教學", "en": "Moving Average Guide"},
        {"slug": "candlestick-patterns", "zh-TW": "K線型態教學", "en": "Candlestick Patterns"},
        {"slug": "support-resistance", "zh-TW": "支撐壓力教學", "en": "Support & Resistance"},
    ],
    "default": [
        {"slug": "profit-loss-ratio", "zh-TW": "損益比教學", "en": "Profit/Loss Ratio Guide"},
        {"slug": "stop-loss-guide", "zh-TW": "停損設定教學", "en": "Stop Loss Strategy"},
        {"slug": "stock-selection-guide", "zh-TW": "選股指南", "en": "Stock Selection Guide"},
    ]
}

# 分類 → Blog 文章對應
CATEGORY_TO_BLOG = {
    "investment": "general_finance",
    "trading": "finance_trading",
    "technical": "technical_analysis",
    "realestate": "general_finance",
    "tax": "general_finance",
    "insurance": "default",
    "loan": "general_finance",
    "retirement": "general_finance",
    "health": "default",
    "medical": "default",
    "ecommerce": "default",
    "construction": "default",
    "energy": "default",
    "auto": "default",
    "hr": "default",
    "education": "default",
    "cooking": "default",
    "datetime": "default",
    "math": "default",
    "unit": "default",
    "textile": "default",
    "legal": "default",
}

# ============================================================
# 2. 工具掃描器
# ============================================================

def detect_lang_from_path(filepath, tools_dir):
    """從檔案路徑偵測語言"""
    rel = os.path.relpath(filepath, tools_dir).replace("\\", "/")
    parts = rel.split("/")
    if len(parts) == 1:
        return "zh-TW"  # 根目錄 = 繁中
    elif parts[0] in [info["path"].rstrip("/") for info in LANGUAGES.values() if info["path"]]:
        for lang_code, info in LANGUAGES.items():
            if info["path"].rstrip("/") == parts[0]:
                return lang_code
    return None

def extract_tool_info(filepath):
    """從 HTML 檔案提取工具資訊"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return None
    
    info = {"path": filepath, "content": content}
    
    # 提取 slug
    basename = os.path.basename(filepath)
    if basename.startswith("index") or not basename.endswith(".html"):
        return None
    info["slug"] = basename.replace(".html", "")
    
    # 提取 H1
    h1_match = re.search(r"<h1[^>]*>(.*?)</h1>", content, re.DOTALL)
    info["h1"] = h1_match.group(1).strip() if h1_match else info["slug"]
    # 清除 H1 中的 HTML tags
    info["h1"] = re.sub(r"<[^>]+>", "", info["h1"]).strip()
    
    # 提取 title
    title_match = re.search(r"<title>(.*?)</title>", content)
    info["title"] = title_match.group(1).strip() if title_match else info["h1"]
    
    return info

def categorize_tool(slug):
    """根據 slug 判斷分類"""
    for cat_key, cat_info in CATEGORY_KEYWORDS.items():
        if slug in cat_info.get("slugs", []):
            return cat_key
    # 如果沒有精確匹配，嘗試模糊匹配
    slug_lower = slug.lower()
    keyword_map = {
        "insurance": "insurance", "mortgage": "realestate", "home": "realestate",
        "rent": "realestate", "property": "realestate", "house": "realestate",
        "tax": "tax", "salary": "tax", "pay": "tax", "income": "tax",
        "loan": "loan", "debt": "loan", "credit": "loan",
        "retire": "retirement", "401k": "retirement", "pension": "retirement",
        "bmi": "health", "calorie": "health", "body": "health", "heart": "health",
        "medical": "medical", "hospital": "medical", "surgery": "medical",
        "shipping": "ecommerce", "fba": "ecommerce", "ebay": "ecommerce",
        "paint": "construction", "tile": "construction", "floor": "construction",
        "electric": "energy", "solar": "energy", "energy": "energy", "battery": "energy",
        "car": "auto", "fuel": "auto", "gas": "auto", "vehicle": "auto",
        "employee": "hr", "hiring": "hr", "labor": "hr",
        "gpa": "education", "college": "education", "student": "education",
        "recipe": "cooking", "cooking": "cooking", "meal": "cooking",
        "date": "datetime", "time": "datetime", "age": "datetime",
        "percent": "math", "fraction": "math", "ratio": "math",
        "convert": "unit", "length": "unit", "weight": "unit",
        "fabric": "textile", "yarn": "textile", "sewing": "textile",
        "legal": "legal", "court": "legal", "patent": "legal",
        "rsi": "technical", "macd": "technical", "fibonacci": "technical",
        "bollinger": "technical", "pivot": "technical", "atr": "technical",
        "ichimoku": "technical", "stochastic": "technical",
        "compound": "investment", "roi": "investment", "dividend": "investment",
        "sharpe": "investment", "portfolio": "investment",
        "risk-reward": "trading", "position-size": "trading", "stop-loss": "trading",
        "margin": "trading", "options": "trading",
    }
    for keyword, cat in keyword_map.items():
        if keyword in slug_lower:
            return cat
    return "investment"  # 預設分類

def scan_all_tools(tools_dir):
    """掃描所有工具頁面"""
    tools_by_lang = defaultdict(list)
    all_tools = []
    
    for root, dirs, files in os.walk(tools_dir):
        for filename in files:
            if not filename.endswith(".html"):
                continue
            if filename.startswith("index"):
                continue
            
            filepath = os.path.join(root, filename)
            lang = detect_lang_from_path(filepath, tools_dir)
            if lang is None:
                continue
            
            info = extract_tool_info(filepath)
            if info is None:
                continue
            
            info["lang"] = lang
            info["category"] = categorize_tool(info["slug"])
            tools_by_lang[lang].append(info)
            all_tools.append(info)
    
    return tools_by_lang, all_tools

# ============================================================
# 3. B2: JS 錯誤掃描與修復
# ============================================================

def scan_js_errors(tool_info):
    """掃描單個工具頁的 JS 錯誤"""
    content = tool_info["content"]
    errors = []
    
    # 提取 script 區塊
    script_match = re.search(r"<script>(.*?)</script>", content, re.DOTALL)
    if not script_match:
        errors.append("NO_SCRIPT: 沒有找到 <script> 區塊")
        return errors
    
    script = script_match.group(1)
    
    # 檢查 getElementById 是否有對應的 id
    get_ids = re.findall(r"""getElementById\(['"](.*?)['"]\)""", script)
    for gid in get_ids:
        # 在 HTML 中找對應的 id
        id_pattern = rf'id\s*=\s*["\']({re.escape(gid)})["\']'
        if not re.search(id_pattern, content):
            errors.append(f"MISSING_ID: getElementById('{gid}') 但 HTML 中沒有 id='{gid}'")
    
    # 檢查 calculate() 函式是否存在
    if 'onclick="calculate()"' in content or "onclick=\"calculate()\"" in content:
        if "function calculate" not in script:
            errors.append("MISSING_FUNC: 按鈕呼叫 calculate() 但 script 中沒有定義")
    
    # 檢查括號配對
    open_braces = script.count("{")
    close_braces = script.count("}")
    if open_braces != close_braces:
        errors.append(f"BRACE_MISMATCH: {{ 有 {open_braces} 個，}} 有 {close_braces} 個")
    
    open_parens = script.count("(")
    close_parens = script.count(")")
    if abs(open_parens - close_parens) > 2:  # 允許小誤差（字串中可能有）
        errors.append(f"PAREN_MISMATCH: ( 有 {open_parens} 個，) 有 {close_parens} 個")
    
    return errors

def fix_js_missing_ids(tool_info):
    """修復 getElementById 不符的問題"""
    content = tool_info["content"]
    script_match = re.search(r"<script>(.*?)</script>", content, re.DOTALL)
    if not script_match:
        return content, 0
    
    script = script_match.group(1)
    fixes = 0
    
    # 找所有 getElementById
    get_ids = re.findall(r"""getElementById\(['"](.*?)['"]\)""", script)
    for gid in get_ids:
        id_pattern = rf'id\s*=\s*["\']({re.escape(gid)})["\']'
        if not re.search(id_pattern, content):
            # 嘗試找相似的 id
            all_ids = re.findall(r'id\s*=\s*["\']([^"\']+)["\']', content)
            # 找最相似的
            best_match = None
            best_score = 0
            gid_lower = gid.lower().replace("-", "").replace("_", "")
            for aid in all_ids:
                aid_lower = aid.lower().replace("-", "").replace("_", "")
                # 簡單相似度
                if gid_lower in aid_lower or aid_lower in gid_lower:
                    score = len(set(gid_lower) & set(aid_lower)) / max(len(gid_lower), len(aid_lower), 1)
                    if score > best_score:
                        best_score = score
                        best_match = aid
            
            if best_match and best_score > 0.5:
                script = script.replace(f"getElementById('{gid}')", f"getElementById('{best_match}')")
                script = script.replace(f'getElementById("{gid}")', f'getElementById("{best_match}")')
                fixes += 1
    
    if fixes > 0:
        content = content[:script_match.start(1)] + script + content[script_match.end(1):]
    
    return content, fixes

# ============================================================
# 4. B3: 延伸閱讀修復
# ============================================================

def get_related_articles_html(category, lang):
    """根據分類生成對應的延伸閱讀 HTML"""
    blog_group = CATEGORY_TO_BLOG.get(category, "default")
    articles = BLOG_ARTICLES.get(blog_group, BLOG_ARTICLES["default"])
    
    lang_info = LANGUAGES.get(lang, LANGUAGES["en"])
    blog_path = f"/blog/{lang_info['path']}" if lang != "zh-TW" else "/blog/"
    
    # 延伸閱讀標題
    titles = {
        "zh-TW": "📚 延伸閱讀", "en": "📚 Related Articles",
        "ja": "📚 関連記事", "ko": "📚 관련 기사",
        "de": "📚 Weitere Artikel", "fr": "📚 Articles Connexes",
        "es": "📚 Artículos Relacionados", "pt": "📚 Artigos Relacionados",
        "id": "📚 Artikel Terkait", "zh-CN": "📚 延伸阅读",
    }
    
    # Blog 文章多語言名稱
    article_names = {
        "kd-indicator": {"zh-TW":"KD 指標教學","en":"KD Indicator Guide","ja":"KDインジケーター","ko":"KD 지표 가이드","de":"KD-Indikator","fr":"Guide KD","es":"Guía KD","pt":"Guia KD","id":"Panduan KD","zh-CN":"KD 指标教学"},
        "macd-indicator": {"zh-TW":"MACD 指標教學","en":"MACD Guide","ja":"MACDガイド","ko":"MACD 가이드","de":"MACD-Leitfaden","fr":"Guide MACD","es":"Guía MACD","pt":"Guia MACD","id":"Panduan MACD","zh-CN":"MACD 指标教学"},
        "rsi-indicator": {"zh-TW":"RSI 指標教學","en":"RSI Guide","ja":"RSIガイド","ko":"RSI 가이드","de":"RSI-Leitfaden","fr":"Guide RSI","es":"Guía RSI","pt":"Guia RSI","id":"Panduan RSI","zh-CN":"RSI 指标教学"},
        "stop-loss-guide": {"zh-TW":"停損設定教學","en":"Stop Loss Strategy","ja":"ストップロス戦略","ko":"손절매 전략","de":"Stop-Loss Strategie","fr":"Stratégie Stop Loss","es":"Estrategia Stop Loss","pt":"Estratégia Stop Loss","id":"Strategi Stop Loss","zh-CN":"止损设定教学"},
        "profit-loss-ratio": {"zh-TW":"損益比教學","en":"Profit/Loss Ratio","ja":"損益比ガイド","ko":"손익비 가이드","de":"Gewinn/Verlust-Verhältnis","fr":"Ratio Profit/Perte","es":"Ratio Beneficio/Pérdida","pt":"Ratio Lucro/Prejuízo","id":"Rasio Untung/Rugi","zh-CN":"损益比教学"},
        "stock-selection-guide": {"zh-TW":"選股指南","en":"Stock Selection Guide","ja":"銘柄選択ガイド","ko":"종목 선택 가이드","de":"Aktienauswahl","fr":"Guide de Sélection","es":"Guía de Selección","pt":"Guia de Seleção","id":"Panduan Seleksi Saham","zh-CN":"选股指南"},
        "moving-average-guide": {"zh-TW":"均線教學","en":"Moving Average Guide","ja":"移動平均線","ko":"이동평균선","de":"Gleitender Durchschnitt","fr":"Moyennes Mobiles","es":"Media Móvil","pt":"Média Móvel","id":"Moving Average","zh-CN":"均线教学"},
        "candlestick-patterns": {"zh-TW":"K線型態教學","en":"Candlestick Patterns","ja":"ローソク足パターン","ko":"캔들패턴","de":"Kerzenmuster","fr":"Chandeliers Japonais","es":"Patrones de Velas","pt":"Padrões de Candlestick","id":"Pola Candlestick","zh-CN":"K线形态教学"},
        "support-resistance": {"zh-TW":"支撐壓力教學","en":"Support & Resistance","ja":"サポート＆レジスタンス","ko":"지지 & 저항","de":"Unterstützung & Widerstand","fr":"Support & Résistance","es":"Soporte y Resistencia","pt":"Suporte e Resistência","id":"Support & Resistance","zh-CN":"支撑压力教学"},
    }
    
    section_title = titles.get(lang, titles["en"])
    links_html = ""
    for art in articles:
        name = article_names.get(art["slug"], {}).get(lang, art.get("en", art["slug"]))
        href = f"{blog_path}{art['slug']}.html"
        links_html += f'<a href="{href}" class="related-link">{name}→ Blog</a>\n'
    
    return f"""<h3>{section_title}</h3>
{links_html}"""

def fix_related_articles(content, category, lang):
    """替換延伸閱讀區塊"""
    new_html = get_related_articles_html(category, lang)
    
    # 找到延伸閱讀區塊並替換
    # 模式1: <h3>📚 Related Articles</h3> ... 到下一個 <h2> 或 </section> 或 <section
    patterns = [
        r'(<h3[^>]*>📚[^<]*</h3>\s*(?:<a[^>]*class="related-link"[^>]*>.*?</a>\s*)+)',
        r'(### 📚.*?(?=\n##|\n<section|\n<h2|\Z))',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, content, re.DOTALL)
        if match:
            content = content[:match.start()] + new_html + content[match.end():]
            return content, True
    
    return content, False

# ============================================================
# 5. B4: 索引頁重建
# ============================================================

def generate_index_page(lang, tools_list):
    """生成完整的工具索引頁"""
    lang_info = LANGUAGES[lang]
    
    # 分類整理
    categorized = defaultdict(list)
    for tool in tools_list:
        categorized[tool["category"]].append(tool)
    
    # 按分類順序排列
    category_order = ["investment", "trading", "technical", "realestate", "tax",
                      "insurance", "loan", "retirement", "health", "medical",
                      "ecommerce", "construction", "energy", "auto", "hr",
                      "education", "cooking", "datetime", "math", "unit",
                      "textile", "legal"]
    
    # 語言選擇器
    lang_links = []
    for lc, li in LANGUAGES.items():
        href = f"/tools/{li['path']}" if lc != "zh-TW" else "/tools/"
        active = " active" if lc == lang else ""
        lang_links.append(f'<a href="{href}" class="lang-btn{active}">{li["flag"]} {li["name"]}</a>')
    lang_switcher = "\n    ".join(lang_links)
    
    # 工具列表 HTML
    tools_html = ""
    for cat_key in category_order:
        if cat_key not in categorized:
            continue
        cat_tools = sorted(categorized[cat_key], key=lambda x: x["slug"])
        cat_name = CATEGORY_KEYWORDS.get(cat_key, {}).get(lang, cat_key)
        
        tools_html += f'\n<section class="tool-category">\n'
        tools_html += f'  <h2 class="cat-title">{cat_name}</h2>\n'
        tools_html += f'  <div class="tool-grid">\n'
        for tool in cat_tools:
            if lang == "zh-TW":
                href = f"/tools/{tool['slug']}.html"
            else:
                href = f"/tools/{lang_info['path']}{tool['slug']}.html"
            name = tool["h1"]
            tools_html += f'    <a href="{href}" class="tool-card">{name}</a>\n'
        tools_html += f'  </div>\n'
        tools_html += f'</section>\n'
    
    total_count = len(tools_list)
    
    # 頁面標題
    page_titles = {
        "zh-TW": f"免費線上計算工具 {total_count}+ 種 — SoftGlow",
        "en": f"{total_count}+ Free Online Calculators & Tools — SoftGlow",
        "ja": f"無料オンライン計算ツール {total_count}+ 種 — SoftGlow",
        "ko": f"무료 온라인 계산기 {total_count}+ 종 — SoftGlow",
        "de": f"{total_count}+ Kostenlose Online-Rechner — SoftGlow",
        "fr": f"{total_count}+ Calculateurs Gratuits en Ligne — SoftGlow",
        "es": f"{total_count}+ Calculadoras Gratuitas Online — SoftGlow",
        "pt": f"{total_count}+ Calculadoras Online Gratuitas — SoftGlow",
        "id": f"{total_count}+ Kalkulator Online Gratis — SoftGlow",
        "zh-CN": f"免费在线计算工具 {total_count}+ 种 — SoftGlow",
    }
    
    page_descs = {
        "zh-TW": f"超過 {total_count} 種免費線上計算工具，涵蓋投資理財、房貸、保險、退休、健康、稅務等 20 大分類，支援 10 種語言。",
        "en": f"Over {total_count} free online calculators covering investment, mortgage, insurance, retirement, health, tax, and 20+ categories in 10 languages.",
        "ja": f"{total_count}種以上の無料オンライン計算ツール。投資、住宅ローン、保険、退職、健康、税金など20以上のカテゴリー、10言語対応。",
        "ko": f"{total_count}개 이상의 무료 온라인 계산기. 투자, 모기지, 보험, 은퇴, 건강, 세금 등 20개 이상의 카테고리, 10개 언어 지원.",
        "de": f"Über {total_count} kostenlose Online-Rechner für Investitionen, Hypotheken, Versicherungen, Rente, Gesundheit und mehr in 10 Sprachen.",
        "fr": f"Plus de {total_count} calculateurs gratuits couvrant investissement, hypothèque, assurance, retraite, santé et plus en 10 langues.",
        "es": f"Más de {total_count} calculadoras gratuitas para inversión, hipoteca, seguros, jubilación, salud y más en 10 idiomas.",
        "pt": f"Mais de {total_count} calculadoras gratuitas para investimento, hipoteca, seguros, aposentadoria, saúde e mais em 10 idiomas.",
        "id": f"Lebih dari {total_count} kalkulator gratis untuk investasi, hipotek, asuransi, pensiun, kesehatan dan lainnya dalam 10 bahasa.",
        "zh-CN": f"超过 {total_count} 种免费在线计算工具，涵盖投资理财、房贷、保险、退休、健康、税务等 20 大分类，支持 10 种语言。",
    }

    h1_texts = {
        "zh-TW": f"免費線上計算工具（{total_count}+ 種）",
        "en": f"Free Online Calculators ({total_count}+ Tools)",
        "ja": f"無料オンライン計算ツール（{total_count}+ 種）",
        "ko": f"무료 온라인 계산기 ({total_count}+ 종)",
        "de": f"Kostenlose Online-Rechner ({total_count}+)",
        "fr": f"Calculateurs Gratuits en Ligne ({total_count}+)",
        "es": f"Calculadoras Gratuitas Online ({total_count}+)",
        "pt": f"Calculadoras Online Gratuitas ({total_count}+)",
        "id": f"Kalkulator Online Gratis ({total_count}+)",
        "zh-CN": f"免费在线计算工具（{total_count}+ 种）",
    }

    subtitle_texts = {
        "zh-TW": "涵蓋投資、房貸、保險、退休、健康、稅務等 20 大分類，支援 10 種語言。所有工具完全免費、無需註冊。",
        "en": "Covering investment, mortgage, insurance, retirement, health, tax & 20+ categories in 10 languages. All tools are 100% free, no sign-up required.",
        "ja": "投資、住宅ローン、保険、退職、健康、税金など20以上のカテゴリーを10言語でカバー。全ツール無料、登録不要。",
        "ko": "투자, 모기지, 보험, 은퇴, 건강, 세금 등 20개 이상의 카테고리를 10개 언어로 지원. 모든 도구 100% 무료, 가입 불필요.",
        "de": "Über 20 Kategorien in 10 Sprachen: Investitionen, Hypotheken, Versicherungen, Rente, Gesundheit und mehr. Alle Tools 100% kostenlos.",
        "fr": "Plus de 20 catégories en 10 langues : investissement, hypothèque, assurance, retraite, santé et plus. Tous les outils sont 100% gratuits.",
        "es": "Más de 20 categorías en 10 idiomas: inversión, hipoteca, seguros, jubilación, salud y más. Todas las herramientas son 100% gratuitas.",
        "pt": "Mais de 20 categorias em 10 idiomas: investimento, hipoteca, seguros, aposentadoria, saúde e mais. Todas as ferramentas são 100% gratuitas.",
        "id": "Lebih dari 20 kategori dalam 10 bahasa: investasi, hipotek, asuransi, pensiun, kesehatan dan lainnya. Semua alat 100% gratis.",
        "zh-CN": "涵盖投资、房贷、保险、退休、健康、税务等 20 大分类，支持 10 种语言。所有工具完全免费、无需注册。",
    }
    
    canonical = f"https://softglow-ai.com/tools/{lang_info['path']}" if lang != "zh-TW" else "https://softglow-ai.com/tools/"
    
    # hreflang tags
    hreflang_tags = ""
    for lc, li in LANGUAGES.items():
        href = f"https://softglow-ai.com/tools/{li['path']}" if lc != "zh-TW" else "https://softglow-ai.com/tools/"
        hreflang_tags += f'<link rel="alternate" hreflang="{lc}" href="{href}">\n'
    hreflang_tags += '<link rel="alternate" hreflang="x-default" href="https://softglow-ai.com/tools/en/">\n'

    nav_tools = lang_info["nav_tools"]
    nav_blog = lang_info["nav_blog"]
    nav_patterns = lang_info["nav_patterns"]
    nav_home = lang_info["nav_home"]
    blog_href = f"/blog/{lang_info['path']}" if lang != "zh-TW" else "/blog/"
    patterns_href = f"/patterns/{lang_info['path'].rstrip('/') + '.html' if lang_info['path'] else 'index.html'}"
    if lang == "zh-TW":
        patterns_href = "/patterns/index.html"

    html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{page_titles.get(lang, page_titles['en'])}</title>
<meta name="description" content="{page_descs.get(lang, page_descs['en'])}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canonical}">
{hreflang_tags}
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
.hero h1{{font-size:28px;font-weight:700;color:#1A202C;margin-bottom:8px}}
.hero p{{font-size:15px;color:#718096;max-width:700px;margin:0 auto 20px}}
.lang-bar{{display:flex;gap:6px;flex-wrap:wrap;justify-content:center;margin:20px auto;max-width:800px}}
.lang-btn{{font-size:12px;padding:4px 12px;border-radius:20px;background:#F7FAFC;border:1px solid #E2E8F0;color:#718096}}
.lang-btn:hover{{background:#EBF5FF;border-color:#BEE3F8;text-decoration:none}}
.lang-btn.active{{background:#2563EB;color:#fff;border-color:#2563EB}}
.container{{max-width:1080px;margin:0 auto;padding:0 20px 40px}}
.tool-category{{margin-bottom:32px}}
.cat-title{{font-size:18px;font-weight:700;color:#1A202C;margin-bottom:12px;padding-bottom:8px;border-bottom:2px solid #E2E8F0}}
.tool-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px}}
.tool-card{{display:block;padding:12px 16px;background:#F7FAFC;border:1px solid #E2E8F0;border-radius:8px;font-size:14px;color:#2D3748;font-weight:500;transition:all 0.15s}}
.tool-card:hover{{background:#EBF5FF;border-color:#BEE3F8;text-decoration:none;transform:translateY(-1px)}}
.footer{{border-top:1px solid #E2E8F0;padding:24px 0;margin-top:40px}}
.footer-inner{{max-width:1080px;margin:0 auto;padding:0 20px;display:flex;flex-wrap:wrap;gap:16px;font-size:12px;color:#A0AEC0}}
.footer-inner a{{color:#718096}}
@media(max-width:768px){{
  .hero h1{{font-size:22px}}
  .tool-grid{{grid-template-columns:1fr}}
}}
</style>
</head>
<body>

<nav class="nav">
<div class="nav-inner">
  <a href="/" class="nav-logo">Soft<span>Glow</span></a>
  <div class="nav-links">
    <a href="/tools/{lang_info['path']}">{nav_tools}</a>
    <a href="{blog_href}">{nav_blog}</a>
    <a href="{patterns_href}">{nav_patterns}</a>
    <a href="/">{nav_home}</a>
  </div>
</div>
</nav>

<div class="hero">
  <h1>{h1_texts.get(lang, h1_texts['en'])}</h1>
  <p>{subtitle_texts.get(lang, subtitle_texts['en'])}</p>
  <div class="lang-bar">
    {lang_switcher}
  </div>
</div>

<div class="container">
{tools_html}
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
</html>"""
    
    return html

# ============================================================
# 6. B5: 語言選擇器修復
# ============================================================

# 正確的語言按鈕列 HTML
def get_correct_lang_buttons(current_lang, slug=""):
    """生成正確的語言按鈕列"""
    buttons = []
    for lc, li in LANGUAGES.items():
        if slug:
            if lc == "zh-TW":
                href = f"/tools/{slug}.html"
            else:
                href = f"/tools/{li['path']}{slug}.html"
        else:
            if lc == "zh-TW":
                href = "/tools/"
            else:
                href = f"/tools/{li['path']}"
        
        active = ' class="lang-btn active"' if lc == current_lang else ' class="lang-btn"'
        buttons.append(f'<a href="{href}"{active}>{li["flag"]} {li["name"]}</a>')
    
    return "\n".join(buttons)

def fix_lang_selector(content, lang, slug):
    """修復語言選擇器"""
    fixed = False
    
    # 移除錯誤的語言連結
    for wrong_lang in WRONG_LANGUAGES:
        patterns = [
            rf'<a[^>]*href="[^"]*/{wrong_lang}/[^"]*"[^>]*>[^<]*</a>\s*',
            rf'<a[^>]*href="[^"]*/{wrong_lang}/"[^>]*>[^<]*</a>\s*',
        ]
        for p in patterns:
            if re.search(p, content):
                content = re.sub(p, "", content)
                fixed = True
    
    # 檢查是否缺少 zh-CN 和 fr 的連結
    if 'zh-CN' not in content and '/zh-CN/' not in content:
        # 需要加入 zh-CN 連結
        # 找到語言按鈕區域，在最後加入
        zh_cn_info = LANGUAGES["zh-CN"]
        fr_info = LANGUAGES["fr"]
        
        if slug:
            zh_cn_href = f"/tools/{zh_cn_info['path']}{slug}.html"
            fr_href = f"/tools/{fr_info['path']}{slug}.html"
        else:
            zh_cn_href = f"/tools/{zh_cn_info['path']}"
            fr_href = f"/tools/{fr_info['path']}"
        
        # 在最後一個語言按鈕後加入
        # 找 de 的連結（通常是最後一個），在後面加
        de_pattern = r'(<a[^>]*href="[^"]*?/de/[^"]*?"[^>]*>[^<]*</a>)'
        de_match = re.search(de_pattern, content)
        if de_match:
            insert_html = f'\n<a href="{fr_href}" class="lang-btn">{fr_info["flag"]} {fr_info["name"]}</a>'
            insert_html += f'\n<a href="{zh_cn_href}" class="lang-btn">{zh_cn_info["flag"]} {zh_cn_info["name"]}</a>'
            content = content[:de_match.end()] + insert_html + content[de_match.end():]
            fixed = True
    
    # 也檢查 nav 下拉中的語言
    # 修復 nav 中顯示 "繁中" 而非完整的下拉選單
    nav_wrong_patterns = [
        r'🇻🇳\s*Tiếng Việt',  # 越南文
        r'🇹🇭\s*ภาษาไทย',      # 泰文
    ]
    for p in nav_wrong_patterns:
        if re.search(p, content):
            # 移除包含這些文字的連結
            content = re.sub(rf'<a[^>]*>[^<]*{p}[^<]*</a>\s*', '', content)
            fixed = True
    
    return content, fixed

# ============================================================
# 7. 主程式
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="SoftGlow 全站 Bug 修復")
    parser.add_argument("--root", help="專案根目錄路徑")
    parser.add_argument("--dry-run", action="store_true", help="只掃描不修改")
    args = parser.parse_args()
    
    # 找專案根目錄
    project_root = find_project_root(args.root)
    if not project_root:
        print("❌ 找不到專案根目錄！")
        print("   請用 --root 參數指定，例如：")
        print('   python fix_all_bugs.py --root "D:\\xian-shang-you-wei"')
        sys.exit(1)
    
    tools_dir = os.path.join(project_root, "backend", "frontend", "tools")
    print(f"✅ 專案根目錄：{project_root}")
    print(f"✅ 工具目錄：{tools_dir}")
    print()
    
    # 掃描所有工具
    print("=" * 60)
    print("📋 Phase 1: 掃描所有工具頁面")
    print("=" * 60)
    tools_by_lang, all_tools = scan_all_tools(tools_dir)
    
    total_files = len(all_tools)
    print(f"   找到 {total_files} 個工具頁面")
    for lang, tools in sorted(tools_by_lang.items()):
        print(f"   {lang}: {len(tools)} 個")
    
    # 分類統計
    cat_counts = defaultdict(int)
    for tool in all_tools:
        cat_counts[tool["category"]] += 1
    print(f"\n   分類分佈：")
    for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1]):
        cat_name = CATEGORY_KEYWORDS.get(cat, {}).get("en", cat)
        print(f"   {cat_name}: {count} 頁")
    
    # ============================================================
    # B2: JS 錯誤掃描
    # ============================================================
    print(f"\n{'=' * 60}")
    print("🔍 Phase 2 (B2): JS 錯誤掃描")
    print("=" * 60)
    
    js_errors = {}
    js_fixable = 0
    js_total_errors = 0
    
    for tool in all_tools:
        errors = scan_js_errors(tool)
        if errors:
            js_errors[tool["path"]] = errors
            js_total_errors += len(errors)
            # 檢查可自動修復的
            for err in errors:
                if err.startswith("MISSING_ID"):
                    js_fixable += 1
    
    print(f"   有 JS 錯誤的頁面：{len(js_errors)} 個")
    print(f"   總錯誤數：{js_total_errors}")
    print(f"   可自動修復（MISSING_ID）：{js_fixable} 個")
    
    if js_errors and not args.dry_run:
        # 寫出錯誤報告
        report_path = os.path.join(project_root, "js_error_report.txt")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("SoftGlow 工具頁 JS 錯誤報告\n")
            f.write(f"掃描時間：{__import__('datetime').datetime.now()}\n")
            f.write(f"總頁數：{total_files}，有錯誤：{len(js_errors)}\n\n")
            for path, errors in sorted(js_errors.items()):
                f.write(f"\n📄 {os.path.relpath(path, tools_dir)}\n")
                for err in errors:
                    f.write(f"   ❌ {err}\n")
        print(f"   報告已寫入：{report_path}")
        
        # 自動修復 MISSING_ID
        id_fixes = 0
        for tool in all_tools:
            if tool["path"] in js_errors:
                new_content, fixes = fix_js_missing_ids(tool)
                if fixes > 0:
                    with open(tool["path"], "w", encoding="utf-8") as f:
                        f.write(new_content)
                    id_fixes += fixes
        print(f"   ✅ 自動修復 {id_fixes} 個 getElementById 不符")
    
    # ============================================================
    # B3: 延伸閱讀修復
    # ============================================================
    print(f"\n{'=' * 60}")
    print("📚 Phase 3 (B3): 延伸閱讀按分類匹配")
    print("=" * 60)
    
    b3_fixed = 0
    if not args.dry_run:
        for tool in all_tools:
            # 重新讀取（可能 B2 已修改）
            with open(tool["path"], "r", encoding="utf-8") as f:
                content = f.read()
            
            new_content, was_fixed = fix_related_articles(content, tool["category"], tool["lang"])
            if was_fixed:
                with open(tool["path"], "w", encoding="utf-8") as f:
                    f.write(new_content)
                b3_fixed += 1
        
        print(f"   ✅ 修復 {b3_fixed} 個頁面的延伸閱讀")
    else:
        # 統計有多少需要修
        for tool in all_tools:
            content = tool["content"]
            if re.search(r'📚', content):
                b3_fixed += 1
        print(f"   需要修復：{b3_fixed} 個頁面（dry-run，未修改）")
    
    # ============================================================
    # B4: 索引頁重建
    # ============================================================
    print(f"\n{'=' * 60}")
    print("📄 Phase 4 (B4): 重建所有語言索引頁")
    print("=" * 60)
    
    b4_count = 0
    if not args.dry_run:
        for lang, tools in tools_by_lang.items():
            if not tools:
                continue
            
            index_html = generate_index_page(lang, tools)
            lang_info = LANGUAGES.get(lang)
            if not lang_info:
                continue
            
            if lang == "zh-TW":
                index_path = os.path.join(tools_dir, "index.html")
            else:
                lang_dir = os.path.join(tools_dir, lang_info["path"].rstrip("/"))
                os.makedirs(lang_dir, exist_ok=True)
                index_path = os.path.join(lang_dir, "index.html")
            
            with open(index_path, "w", encoding="utf-8") as f:
                f.write(index_html)
            
            b4_count += 1
            print(f"   ✅ {lang}: {len(tools)} 個工具 → {index_path}")
    else:
        for lang, tools in tools_by_lang.items():
            if tools:
                b4_count += 1
                print(f"   {lang}: {len(tools)} 個工具（dry-run，未生成）")
    
    print(f"   共重建 {b4_count} 個索引頁")
    
    # ============================================================
    # B5: 語言選擇器修復
    # ============================================================
    print(f"\n{'=' * 60}")
    print("🌐 Phase 5 (B5): 語言選擇器統一")
    print("=" * 60)
    
    b5_fixed = 0
    if not args.dry_run:
        for tool in all_tools:
            with open(tool["path"], "r", encoding="utf-8") as f:
                content = f.read()
            
            new_content, was_fixed = fix_lang_selector(content, tool["lang"], tool["slug"])
            if was_fixed:
                with open(tool["path"], "w", encoding="utf-8") as f:
                    f.write(new_content)
                b5_fixed += 1
        
        print(f"   ✅ 修復 {b5_fixed} 個頁面的語言選擇器")
    else:
        for tool in all_tools:
            content = tool["content"]
            has_wrong = any(wl in content for wl in ["Tiếng Việt", "ภาษาไทย"])
            missing_new = "zh-CN" not in content
            if has_wrong or missing_new:
                b5_fixed += 1
        print(f"   需要修復：{b5_fixed} 個頁面（dry-run，未修改）")
    
    # ============================================================
    # Phase 6: 生成共用 Cookie JS 檔案
    # ============================================================
    print(f"\n{'=' * 60}")
    print("🍪 Phase 6: 生成 Cookie 功能（同意橫幅 + 語言記憶 + 最近使用）")
    print("=" * 60)
    
    frontend_dir = os.path.join(project_root, "backend", "frontend")
    js_dir = os.path.join(frontend_dir, "js")
    os.makedirs(js_dir, exist_ok=True)
    
    cookie_js = r'''/* SoftGlow Cookie Manager v1.0
 * 功能：1.GDPR同意橫幅 2.語言偏好記憶 3.最近使用工具
 * 所有資料存在使用者瀏覽器 localStorage，不傳伺服器
 */
(function(){
"use strict";

// ── 1. Cookie 同意橫幅（GDPR）──────────────────────
var CONSENT_KEY = "sg_cookie_consent";
var CONSENT_TEXTS = {
  "zh-TW":{msg:"本站使用 Cookie 來提供更好的瀏覽體驗和個人化廣告。",yes:"同意",no:"拒絕",more:"了解更多"},
  "zh-CN":{msg:"本站使用 Cookie 来提供更好的浏览体验和个性化广告。",yes:"同意",no:"拒绝",more:"了解更多"},
  "en":{msg:"We use cookies to improve your experience and show personalized ads.",yes:"Accept",no:"Decline",more:"Learn more"},
  "ja":{msg:"より良い体験とパーソナライズ広告のためCookieを使用します。",yes:"同意",no:"拒否",more:"詳細"},
  "ko":{msg:"더 나은 경험과 맞춤 광고를 위해 쿠키를 사용합니다.",yes:"동의",no:"거부",more:"자세히"},
  "de":{msg:"Wir verwenden Cookies für ein besseres Erlebnis und personalisierte Werbung.",yes:"Akzeptieren",no:"Ablehnen",more:"Mehr erfahren"},
  "fr":{msg:"Nous utilisons des cookies pour améliorer votre expérience et afficher des publicités personnalisées.",yes:"Accepter",no:"Refuser",more:"En savoir plus"},
  "es":{msg:"Usamos cookies para mejorar tu experiencia y mostrar anuncios personalizados.",yes:"Aceptar",no:"Rechazar",more:"Más información"},
  "pt":{msg:"Usamos cookies para melhorar sua experiência e exibir anúncios personalizados.",yes:"Aceitar",no:"Recusar",more:"Saiba mais"},
  "id":{msg:"Kami menggunakan cookie untuk pengalaman lebih baik dan iklan yang dipersonalisasi.",yes:"Terima",no:"Tolak",more:"Pelajari"}
};

function getLang(){
  var html = document.documentElement;
  return (html.getAttribute("lang")||"en").replace(/_.*/,"");
}

function showConsentBanner(){
  if(localStorage.getItem(CONSENT_KEY)) return;
  var lang = getLang();
  var t = CONSENT_TEXTS[lang] || CONSENT_TEXTS["en"];

  var banner = document.createElement("div");
  banner.id = "sg-consent";
  banner.innerHTML = '<div class="sg-consent-inner">' +
    '<p>' + t.msg + ' <a href="/privacy.html">' + t.more + '</a></p>' +
    '<div class="sg-consent-btns">' +
    '<button class="sg-btn-yes" onclick="sgAcceptCookies()">' + t.yes + '</button>' +
    '<button class="sg-btn-no" onclick="sgDeclineCookies()">' + t.no + '</button>' +
    '</div></div>';
  document.body.appendChild(banner);
}

window.sgAcceptCookies = function(){
  localStorage.setItem(CONSENT_KEY, "accepted");
  var el = document.getElementById("sg-consent");
  if(el) el.remove();
  // 同意後載入 AdSense（如果還沒載入）
  if(!document.querySelector('script[src*="googlesyndication"]')){
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1768270548115739";
    s.crossOrigin = "anonymous";
    document.head.appendChild(s);
  }
};

window.sgDeclineCookies = function(){
  localStorage.setItem(CONSENT_KEY, "declined");
  var el = document.getElementById("sg-consent");
  if(el) el.remove();
};

// ── 2. 語言偏好記憶 ──────────────────────────
var LANG_KEY = "sg_preferred_lang";

function detectCurrentLang(){
  var path = window.location.pathname;
  // /tools/en/xxx.html → en
  var m = path.match(/\/tools\/([a-z]{2}(?:-[A-Z]{2})?)\//);
  if(m) return m[1];
  // /tools/xxx.html → zh-TW
  if(path.match(/^\/tools\/[^/]+\.html$/) || path === "/tools/") return "zh-TW";
  return null;
}

function saveLangPreference(){
  var lang = detectCurrentLang();
  if(lang) localStorage.setItem(LANG_KEY, lang);
}

function checkLangRedirect(){
  var saved = localStorage.getItem(LANG_KEY);
  if(!saved) return;
  var current = detectCurrentLang();
  if(!current || current === saved) return;

  // 只在索引頁自動跳轉（工具頁不跳，避免干擾 SEO）
  var path = window.location.pathname;
  var isIndex = (path === "/tools/" || path.match(/^\/tools\/[a-z]{2}(-[A-Z]{2})?\/?$/));
  if(!isIndex) return;

  var target;
  if(saved === "zh-TW"){
    target = "/tools/";
  } else {
    target = "/tools/" + saved + "/";
  }
  if(path !== target){
    window.location.replace(target);
  }
}

// 攔截語言切換點擊，儲存偏好
function hookLangLinks(){
  document.addEventListener("click", function(e){
    var a = e.target.closest("a.lang-btn");
    if(!a) return;
    var href = a.getAttribute("href") || "";
    var m = href.match(/\/tools\/([a-z]{2}(?:-[A-Z]{2})?)\//);
    if(m){
      localStorage.setItem(LANG_KEY, m[1]);
    } else if(href === "/tools/" || href.match(/^\/tools\/[^/]+\.html$/)){
      localStorage.setItem(LANG_KEY, "zh-TW");
    }
  });
}

// ── 3. 最近使用工具 ──────────────────────────
var RECENT_KEY = "sg_recent_tools";
var MAX_RECENT = 5;

function saveRecentTool(){
  var path = window.location.pathname;
  // 只在工具頁觸發（排除索引頁）
  var m = path.match(/\/tools\/(?:([a-z]{2}(?:-[A-Z]{2})?)\/)?([^/]+)\.html$/);
  if(!m) return;

  var lang = m[1] || "zh-TW";
  var slug = m[2];
  var h1 = document.querySelector("h1");
  var name = h1 ? h1.textContent.trim() : slug;

  var recent = [];
  try{ recent = JSON.parse(localStorage.getItem(RECENT_KEY)) || []; } catch(e){}

  // 移除重複
  recent = recent.filter(function(r){ return r.slug !== slug || r.lang !== lang; });
  // 加到最前面
  recent.unshift({slug: slug, name: name, lang: lang, time: Date.now()});
  // 限制數量
  if(recent.length > MAX_RECENT) recent = recent.slice(0, MAX_RECENT);

  localStorage.setItem(RECENT_KEY, JSON.stringify(recent));
}

function renderRecentTools(){
  var path = window.location.pathname;
  // 只在索引頁顯示
  var isIndex = (path === "/tools/" || path.match(/^\/tools\/[a-z]{2}(-[A-Z]{2})?\/?$/));
  if(!isIndex) return;

  var recent = [];
  try{ recent = JSON.parse(localStorage.getItem(RECENT_KEY)) || []; } catch(e){}
  if(recent.length === 0) return;

  var lang = detectCurrentLang() || "zh-TW";
  var titles = {
    "zh-TW":"🕐 最近使用","en":"🕐 Recently Used","ja":"🕐 最近使用",
    "ko":"🕐 최근 사용","de":"🕐 Zuletzt verwendet","fr":"🕐 Récemment utilisé",
    "es":"🕐 Usado recientemente","pt":"🕐 Usado recentemente",
    "id":"🕐 Baru digunakan","zh-CN":"🕐 最近使用"
  };

  var html = '<section class="tool-category" id="sg-recent" style="margin-bottom:32px">';
  html += '<h2 class="cat-title" style="color:#2563EB">' + (titles[lang]||titles["en"]) + '</h2>';
  html += '<div class="tool-grid">';

  for(var i = 0; i < recent.length; i++){
    var r = recent[i];
    var href;
    if(r.lang === "zh-TW"){
      href = "/tools/" + r.slug + ".html";
    } else {
      href = "/tools/" + r.lang + "/" + r.slug + ".html";
    }
    html += '<a href="' + href + '" class="tool-card" style="border-color:#BEE3F8;background:#EBF5FF">' + r.name + '</a>';
  }
  html += '</div></section>';

  // 插入到 .container 的最前面
  var container = document.querySelector(".container");
  if(container){
    var div = document.createElement("div");
    div.innerHTML = html;
    container.insertBefore(div.firstChild, container.firstChild);
  }
}

// ── 初始化 ──────────────────────────────
function init(){
  // Cookie 同意（GDPR）
  var consent = localStorage.getItem(CONSENT_KEY);
  if(!consent){
    showConsentBanner();
  } else if(consent === "accepted"){
    // 已同意，確保 AdSense 載入
    // （AdSense script 已在 HTML 中，不需額外處理）
  }
  // 如果拒絕，AdSense 不會被延遲載入腳本觸發

  // 語言偏好
  checkLangRedirect();
  saveLangPreference();
  hookLangLinks();

  // 最近使用工具
  saveRecentTool();
  renderRecentTools();
}

// DOM ready
if(document.readyState === "loading"){
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}

})();
'''

    cookie_css = r'''/* Cookie Consent Banner */
#sg-consent{position:fixed;bottom:0;left:0;right:0;z-index:9999;background:rgba(26,32,44,0.95);backdrop-filter:blur(8px);padding:16px 20px;box-shadow:0 -2px 12px rgba(0,0,0,0.15)}
.sg-consent-inner{max-width:1080px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap}
#sg-consent p{color:#E2E8F0;font-size:14px;margin:0;flex:1;min-width:200px;line-height:1.5}
#sg-consent a{color:#63B3ED;text-decoration:underline}
.sg-consent-btns{display:flex;gap:8px;flex-shrink:0}
.sg-btn-yes{padding:8px 20px;background:#2563EB;color:#fff;border:none;border-radius:6px;font-size:14px;font-weight:600;cursor:pointer}
.sg-btn-yes:hover{background:#1D4ED8}
.sg-btn-no{padding:8px 20px;background:transparent;color:#A0AEC0;border:1px solid #4A5568;border-radius:6px;font-size:14px;cursor:pointer}
.sg-btn-no:hover{background:rgba(255,255,255,0.05);color:#E2E8F0}
@media(max-width:600px){.sg-consent-inner{flex-direction:column;text-align:center}.sg-consent-btns{justify-content:center;width:100%}}
'''
    
    if not args.dry_run:
        # 寫入 JS 檔案
        js_path = os.path.join(js_dir, "softglow-cookies.js")
        with open(js_path, "w", encoding="utf-8") as f:
            f.write(cookie_js)
        print(f"   ✅ 生成 {js_path}")
        
        # 寫入 CSS 檔案
        css_path = os.path.join(js_dir, "cookie-consent.css")
        with open(css_path, "w", encoding="utf-8") as f:
            f.write(cookie_css)
        print(f"   ✅ 生成 {css_path}")
    else:
        print("   會生成 js/softglow-cookies.js 和 js/cookie-consent.css（dry-run，未生成）")
    
    # ============================================================
    # Phase 7: 注入 Cookie JS/CSS 到所有工具頁
    # ============================================================
    print(f"\n{'=' * 60}")
    print("💉 Phase 7: 注入 Cookie 功能到所有工具頁")
    print("=" * 60)
    
    cookie_script_tag = '<link rel="stylesheet" href="/js/cookie-consent.css">\n'
    cookie_js_tag = '<script src="/js/softglow-cookies.js" defer></script>\n'
    
    inject_count = 0
    if not args.dry_run:
        # 掃描所有工具頁 + 索引頁
        for root_dir, dirs, files in os.walk(tools_dir):
            for filename in files:
                if not filename.endswith(".html"):
                    continue
                filepath = os.path.join(root_dir, filename)
                
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                
                modified = False
                
                # 注入 CSS（如果還沒有）
                if "cookie-consent.css" not in content:
                    content = content.replace("</head>", cookie_script_tag + "</head>", 1)
                    modified = True
                
                # 注入 JS（如果還沒有）
                if "softglow-cookies.js" not in content:
                    content = content.replace("</body>", cookie_js_tag + "</body>", 1)
                    modified = True
                
                if modified:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(content)
                    inject_count += 1
        
        # 也注入到 patterns 和 blog 頁面
        for subdir in ["patterns", "blog"]:
            sub_path = os.path.join(frontend_dir, subdir)
            if not os.path.isdir(sub_path):
                continue
            for root_dir, dirs, files in os.walk(sub_path):
                for filename in files:
                    if not filename.endswith(".html"):
                        continue
                    filepath = os.path.join(root_dir, filename)
                    
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    modified = False
                    if "cookie-consent.css" not in content:
                        content = content.replace("</head>", cookie_script_tag + "</head>", 1)
                        modified = True
                    if "softglow-cookies.js" not in content:
                        content = content.replace("</body>", cookie_js_tag + "</body>", 1)
                        modified = True
                    
                    if modified:
                        with open(filepath, "w", encoding="utf-8") as f:
                            f.write(content)
                        inject_count += 1
        
        # 注入到首頁 homepage.html
        homepage = os.path.join(frontend_dir, "homepage.html")
        if os.path.isfile(homepage):
            with open(homepage, "r", encoding="utf-8") as f:
                content = f.read()
            modified = False
            if "cookie-consent.css" not in content:
                content = content.replace("</head>", cookie_script_tag + "</head>", 1)
                modified = True
            if "softglow-cookies.js" not in content:
                content = content.replace("</body>", cookie_js_tag + "</body>", 1)
                modified = True
            if modified:
                with open(homepage, "w", encoding="utf-8") as f:
                    f.write(content)
                inject_count += 1
        
        # 注入到合規頁面
        for page in ["about.html", "contact.html", "privacy.html", "terms.html", "disclaimer.html", "refund.html"]:
            page_path = os.path.join(frontend_dir, page)
            if not os.path.isfile(page_path):
                continue
            with open(page_path, "r", encoding="utf-8") as f:
                content = f.read()
            modified = False
            if "cookie-consent.css" not in content:
                content = content.replace("</head>", cookie_script_tag + "</head>", 1)
                modified = True
            if "softglow-cookies.js" not in content:
                content = content.replace("</body>", cookie_js_tag + "</body>", 1)
                modified = True
            if modified:
                with open(page_path, "w", encoding="utf-8") as f:
                    f.write(content)
                inject_count += 1
        
        print(f"   ✅ 注入 Cookie 功能到 {inject_count} 個頁面")
    else:
        # 計算需要注入的頁面數
        for root_dir, dirs, files in os.walk(tools_dir):
            for filename in files:
                if filename.endswith(".html"):
                    inject_count += 1
        print(f"   需要注入：{inject_count} 個頁面（dry-run，未注入）")
    
    # ============================================================
    # Phase 8: 也處理 main.py 的路由（提示）
    # ============================================================
    print(f"\n{'=' * 60}")
    print("📋 Phase 8: main.py 路由提醒")
    print("=" * 60)
    
    mainpy_path = os.path.join(project_root, "backend", "main.py")
    if os.path.isfile(mainpy_path):
        with open(mainpy_path, "r", encoding="utf-8") as f:
            mainpy_content = f.read()
        
        needs_js_route = "/js/" not in mainpy_content
        if needs_js_route:
            print("   ⚠️ main.py 需要加 /js/ 路由來提供 Cookie JS/CSS")
            print("   加入以下程式碼（放在其他靜態路由附近）：")
            print()
            print('   @app.get("/js/{filename}")')
            print('   async def serve_js(filename: str):')
            print('       p = _FRONTEND / "js" / filename')
            print('       if p.is_file():')
            print('           ct = "text/css" if filename.endswith(".css") else "application/javascript"')
            print('           return FileResponse(p, media_type=ct)')
            print('       raise HTTPException(404)')
            print()
            
            if not args.dry_run:
                # 嘗試自動加入路由
                # 找到 patterns 路由附近插入
                patterns_route = '@app.get("/patterns/'
                if patterns_route in mainpy_content:
                    js_route_code = '''
@app.get("/js/{filename}")
async def serve_js_file(filename: str):
    """提供 Cookie JS/CSS 檔案"""
    p = _FRONTEND / "js" / filename
    if p.is_file():
        ct = "text/css" if filename.endswith(".css") else "application/javascript"
        return FileResponse(p, media_type=ct)
    raise HTTPException(404)

'''
                    # 在 patterns 路由前面插入
                    idx = mainpy_content.index(patterns_route)
                    # 往前找到 @app 或 def 的行首
                    line_start = mainpy_content.rfind("\n", 0, idx) + 1
                    mainpy_content = mainpy_content[:line_start] + js_route_code + mainpy_content[line_start:]
                    
                    with open(mainpy_path, "w", encoding="utf-8") as f:
                        f.write(mainpy_content)
                    print("   ✅ 已自動加入 /js/ 路由到 main.py")
                else:
                    print("   ❌ 找不到 patterns 路由，請手動加入上面的程式碼")
        else:
            print("   ✅ main.py 已有 /js/ 路由，不需要修改")
    else:
        print("   ⚠️ 找不到 main.py")
    
    # ============================================================
    # 總結
    # ============================================================
    print(f"\n{'=' * 60}")
    print("📊 修復總結")
    print("=" * 60)
    print(f"   總掃描頁面：{total_files}")
    print(f"   B2 JS 錯誤頁面：{len(js_errors)}（已自動修復 getElementById 不符）")
    print(f"   B3 延伸閱讀修復：{b3_fixed} 頁")
    print(f"   B4 索引頁重建：{b4_count} 個語言")
    print(f"   B5 語言選擇器修復：{b5_fixed} 頁")
    print(f"   🍪 Cookie 功能注入：{inject_count} 頁")
    print(f"   功能清單：")
    print(f"      ✅ GDPR Cookie 同意橫幅（10 語言）")
    print(f"      ✅ 語言偏好記憶（自動跳轉到上次選的語言）")
    print(f"      ✅ 最近使用工具（索引頁顯示最近 5 個）")
    
    if not args.dry_run:
        print(f"\n   ✅ 全部修復完成！")
        print(f"\n   下一步：")
        print(f"   1. 本機開啟瀏覽器檢查幾個頁面")
        print(f"   2. 確認 Cookie 同意橫幅正常顯示")
        print(f"   3. 確認沒問題後：")
        print(f"      cd {project_root}")
        print(f"      git add -A")
        print(f'      git commit -m "fix: B2-B5 bugs + cookie consent + lang memory + recent tools"')
        print(f"      git push")
        print(f"   4. 等 Zeabur 自動部署完成")
    else:
        print(f"\n   ℹ️ Dry-run 模式，未做任何修改")
        print(f"   移除 --dry-run 參數即可執行修復")

if __name__ == "__main__":
    main()
