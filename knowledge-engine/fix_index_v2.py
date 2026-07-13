#!/usr/bin/env python3
"""
fix_index_v2.py — Fix tool index pages (use <title> for names) + blog lang dropdown
Run from: D:\\xian-shang-you-wei\\knowledge-engine
"""
import os, re, json, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(SCRIPT_DIR, "..", "backend", "frontend")
TOOLS_DIR = os.path.join(BASE, "tools")
BLOG_DIR = os.path.join(BASE, "blog")

LANGS = ["zh-TW", "en", "ja", "ko", "de", "fr", "es", "pt", "id", "zh-CN"]
LANG_NAMES = {
    "zh-TW": "繁中", "en": "EN", "ja": "日本語", "ko": "한국어",
    "de": "DE", "fr": "FR", "es": "ES", "pt": "PT",
    "id": "ID", "zh-CN": "简中"
}

NAV_LABELS = {
    "tools": {"zh-TW": "工具", "en": "Tools", "ja": "ツール", "ko": "도구", "de": "Tools", "fr": "Outils", "es": "Herramientas", "pt": "Ferramentas", "id": "Alat", "zh-CN": "工具"},
    "blog": {"zh-TW": "教學", "en": "Blog", "ja": "ブログ", "ko": "블로그", "de": "Blog", "fr": "Blog", "es": "Blog", "pt": "Blog", "id": "Blog", "zh-CN": "博客"},
    "patterns": {"zh-TW": "K棒型態", "en": "Patterns", "ja": "ローソク足", "ko": "캔들 패턴", "de": "Muster", "fr": "Chandeliers", "es": "Patrones", "pt": "Padrões", "id": "Pola", "zh-CN": "K线形态"},
    "home": {"zh-TW": "首頁", "en": "Home", "ja": "ホーム", "ko": "홈", "de": "Startseite", "fr": "Accueil", "es": "Inicio", "pt": "Início", "id": "Beranda", "zh-CN": "首页"},
}

TOOL_CATEGORIES = {
    "finance": {
        "names": {"zh-TW": "金融投資", "en": "Finance & Investment", "ja": "金融投資", "ko": "금융 투자", "de": "Finanzen & Investition", "fr": "Finance & Investissement", "es": "Finanzas e Inversión", "pt": "Finanças & Investimento", "id": "Keuangan & Investasi", "zh-CN": "金融投资"},
        "icon": "💰",
        "slugs": ["compound-interest","roi-calculator","risk-reward","position-size","stop-loss","dividend-yield","pe-ratio","dca-calculator","cagr","margin-calculator","stock-gain-loss","break-even","rule-of-72","asset-allocation","dcf-calculator","intrinsic-value","options-profit","fibonacci-retracement","pivot-point","rsi-calculator","macd-calculator","bollinger-bands","atr-calculator","sharpe-ratio","ma-crossover","candlestick-identifier","support-resistance","trading-fee","stock-split","average-down","pip-value","currency-converter","kelly-criterion","retirement","savings-goal","bond-yield","portfolio-rebalance","expense-ratio","earnings-per-share","price-to-book","debt-to-equity","current-ratio","quick-ratio","free-cash-flow","wacc-calculator","payback-period","npv-calculator","irr-calculator","annuity-calculator","sip-calculator"]
    },
    "health": {
        "names": {"zh-TW": "健康體適能", "en": "Health & Fitness", "ja": "健康・フィットネス", "ko": "건강 & 피트니스", "de": "Gesundheit & Fitness", "fr": "Santé & Fitness", "es": "Salud y Fitness", "pt": "Saúde & Fitness", "id": "Kesehatan & Kebugaran", "zh-CN": "健康体适能"},
        "icon": "🏥",
        "slugs": ["bmi-calculator","bmr-calculator","tdee-calculator","body-fat","ideal-weight","calorie-calculator","macro-calculator","water-intake","heart-rate-zone","pace-calculator","one-rep-max","waist-hip-ratio","pregnancy-due-date","ovulation-calculator","blood-alcohol","sleep-calculator","vo2max-estimator","calorie-density","protein-calculator","blood-pressure"]
    },
    "realestate": {
        "names": {"zh-TW": "房地產與房貸", "en": "Real Estate & Mortgage", "ja": "不動産・住宅ローン", "ko": "부동산 & 주택담보대출", "de": "Immobilien & Hypothek", "fr": "Immobilier & Hypothèque", "es": "Inmobiliaria & Hipoteca", "pt": "Imóveis & Hipoteca", "id": "Properti & KPR", "zh-CN": "房地产与房贷"},
        "icon": "🏠",
        "slugs": ["mortgage","rent-vs-buy","home-affordability","closing-cost","property-tax","rental-yield","ltv-calculator","refinance-calculator","home-equity","stamp-duty","renovation-budget","sqft-price","amortization-schedule","down-payment","moving-cost"]
    },
    "tax": {
        "names": {"zh-TW": "稅務與薪資", "en": "Tax & Salary", "ja": "税金・給与", "ko": "세금 & 급여", "de": "Steuern & Gehalt", "fr": "Impôts & Salaire", "es": "Impuestos y Salario", "pt": "Impostos & Salário", "id": "Pajak & Gaji", "zh-CN": "税务与薪资"},
        "icon": "🧾",
        "slugs": ["income-tax","sales-tax","vat-calculator","payroll-tax","salary-to-hourly","hourly-to-salary","overtime-calculator","take-home-pay","tax-bracket","capital-gains-tax","self-employment-tax","bonus-tax","tip-calculator","inflation","cost-of-living"]
    },
    "insurance": {
        "names": {"zh-TW": "保險估算", "en": "Insurance", "ja": "保険", "ko": "보험", "de": "Versicherung", "fr": "Assurance", "es": "Seguros", "pt": "Seguros", "id": "Asuransi", "zh-CN": "保险估算"},
        "icon": "🛡️",
        "slugs": ["life-insurance","health-insurance","car-insurance","home-insurance","renters-insurance","disability-insurance","pet-insurance","travel-insurance","umbrella-insurance","term-life-quote","whole-life-value","insurance-needs","deductible-optimizer","coverage-gap","premium-comparison","long-term-care","critical-illness","dental-insurance","vision-insurance","liability-insurance"]
    },
    "loan": {
        "names": {"zh-TW": "貸款與信用", "en": "Loans & Credit", "ja": "ローン・クレジット", "ko": "대출 & 신용", "de": "Kredit & Darlehen", "fr": "Prêts & Crédit", "es": "Préstamos y Crédito", "pt": "Empréstimos & Crédito", "id": "Pinjaman & Kredit", "zh-CN": "贷款与信用"},
        "icon": "💳",
        "slugs": ["loan-calculator","auto-loan","personal-loan","student-loan","credit-card-payoff","debt-snowball","debt-avalanche","debt-consolidation","interest-rate-converter","apr-calculator","emi-calculator","balloon-payment","heloc-calculator","loan-comparison","prepayment-calculator"]
    },
    "medical": {
        "names": {"zh-TW": "醫療費用", "en": "Medical Costs", "ja": "医療費", "ko": "의료비", "de": "Medizinische Kosten", "fr": "Frais médicaux", "es": "Costos médicos", "pt": "Custos médicos", "id": "Biaya Medis", "zh-CN": "医疗费用"},
        "icon": "⚕️",
        "slugs": ["medical-bill","hsa-calculator","fsa-calculator","copay-estimator","drug-cost","surgery-cost","dental-cost","vision-cost","therapy-cost","fertility-cost","emergency-cost","hospital-stay-cost","lab-test-cost","vaccination-cost","mental-health-cost"]
    },
    "ecommerce": {
        "names": {"zh-TW": "電商與物流", "en": "E-Commerce & Logistics", "ja": "EC・物流", "ko": "이커머스 & 물류", "de": "E-Commerce & Logistik", "fr": "E-Commerce & Logistique", "es": "E-Commerce y Logística", "pt": "E-Commerce & Logística", "id": "E-Commerce & Logistik", "zh-CN": "电商与物流"},
        "icon": "📦",
        "slugs": ["shipping-cost","fba-calculator","cbm-calculator","customs-duty","ebay-fee","amazon-fee","shopify-profit","etsy-fee","dropshipping-margin","cogs-calculator","markup-calculator","discount-calculator","wholesale-price","landed-cost","inventory-turnover"]
    },
    "construction": {
        "names": {"zh-TW": "建築與裝修", "en": "Construction & Renovation", "ja": "建築・リフォーム", "ko": "건축 & 인테리어", "de": "Bau & Renovierung", "fr": "Construction & Rénovation", "es": "Construcción y Renovación", "pt": "Construção & Renovação", "id": "Konstruksi & Renovasi", "zh-CN": "建筑与装修"},
        "icon": "🏗️",
        "slugs": ["concrete-calculator","paint-calculator","flooring-calculator","roofing-calculator","tile-calculator","brick-calculator","lumber-calculator","drywall-calculator","insulation-calculator","fence-calculator","deck-calculator","gravel-calculator","rebar-calculator","staircase-calculator","wallpaper-calculator","plumbing-estimate","electrical-load","hvac-sizing","window-cost","kitchen-remodel"]
    },
    "energy": {
        "names": {"zh-TW": "電力與能源", "en": "Energy & Utilities", "ja": "エネルギー", "ko": "에너지 & 유틸리티", "de": "Energie & Versorgung", "fr": "Énergie & Services", "es": "Energía y Servicios", "pt": "Energia & Utilidades", "id": "Energi & Utilitas", "zh-CN": "电力与能源"},
        "icon": "⚡",
        "slugs": ["electricity-cost","solar-panel","led-savings","ev-charging","carbon-footprint","kwh-calculator","generator-size","battery-capacity","energy-audit","heat-loss","air-conditioner-size","water-heater-cost","gas-bill","renewable-roi","power-consumption"]
    },
    "auto": {
        "names": {"zh-TW": "汽車與交通", "en": "Auto & Transport", "ja": "自動車・交通", "ko": "자동차 & 교통", "de": "Auto & Verkehr", "fr": "Auto & Transport", "es": "Auto y Transporte", "pt": "Auto & Transporte", "id": "Otomotif & Transportasi", "zh-CN": "汽车与交通"},
        "icon": "🚗",
        "slugs": ["fuel-cost","car-depreciation","car-lease","car-payment","mpg-calculator","tire-size","towing-capacity","commute-cost","car-maintenance","ev-vs-gas","road-trip-cost","taxi-fare","parking-cost","toll-calculator","vehicle-registration"]
    },
    "hr": {
        "names": {"zh-TW": "人資與企業", "en": "HR & Business", "ja": "人事・ビジネス", "ko": "인사 & 비즈니스", "de": "Personal & Business", "fr": "RH & Business", "es": "RRHH y Negocios", "pt": "RH & Negócios", "id": "SDM & Bisnis", "zh-CN": "人力资源与企业"},
        "icon": "👔",
        "slugs": ["employee-cost","turnover-cost","revenue-per-employee","break-even-analysis","profit-margin","burn-rate","runway-calculator","valuation-calculator","cac-calculator","ltv-calculator","churn-rate","conversion-rate","ab-test-calculator","roi-marketing","cpm-calculator"]
    },
    "startup": {
        "names": {"zh-TW": "創業與退休", "en": "Startup & Retirement", "ja": "起業・退職", "ko": "창업 & 은퇴", "de": "Gründung & Ruhestand", "fr": "Startup & Retraite", "es": "Startup y Jubilación", "pt": "Startup & Aposentadoria", "id": "Startup & Pensiun", "zh-CN": "创业与退休"},
        "icon": "🚀",
        "slugs": ["startup-cost","business-loan","franchise-cost","social-security","pension-calculator","401k-calculator","roth-ira","fire-calculator","withdrawal-rate","required-minimum-distribution","catch-up-contribution","retirement-income","spousal-benefit","early-retirement","side-hustle-income","gig-economy-tax","freelance-rate","consulting-fee","business-valuation","equity-dilution"]
    },
    "education": {
        "names": {"zh-TW": "教育與學術", "en": "Education", "ja": "教育", "ko": "교육", "de": "Bildung", "fr": "Éducation", "es": "Educación", "pt": "Educação", "id": "Pendidikan", "zh-CN": "教育与学术"},
        "icon": "🎓",
        "slugs": ["gpa-calculator","grade-calculator","college-cost","student-loan-repayment","scholarship-estimator","sat-score","act-score","study-abroad-cost","textbook-cost","tuition-inflation","education-roi","class-size","teacher-salary","school-budget","tutoring-rate"]
    },
    "legal": {
        "names": {"zh-TW": "法律與合規", "en": "Legal & Compliance", "ja": "法務・コンプライアンス", "ko": "법률 & 컴플라이언스", "de": "Recht & Compliance", "fr": "Juridique & Conformité", "es": "Legal y Cumplimiento", "pt": "Jurídico & Conformidade", "id": "Hukum & Kepatuhan", "zh-CN": "法律与合规"},
        "icon": "⚖️",
        "slugs": ["alimony-calculator","child-support","court-fee","legal-fee","settlement-calculator","statute-of-limitations","contract-penalty","compliance-cost","trademark-cost","patent-cost","immigration-fee","visa-cost","notary-fee","power-of-attorney","estate-tax"]
    },
    "textile": {
        "names": {"zh-TW": "紡織工業", "en": "Textile Industry", "ja": "繊維産業", "ko": "섬유 산업", "de": "Textilindustrie", "fr": "Industrie textile", "es": "Industria textil", "pt": "Indústria têxtil", "id": "Industri Tekstil", "zh-CN": "纺织工业"},
        "icon": "🧵",
        "slugs": ["fabric-calculator","yarn-calculator","dyeing-cost","gsm-calculator","shrinkage-calculator","thread-consumption","knitting-gauge","weaving-density","pattern-grading","cutting-yield"]
    },
    "cooking": {
        "names": {"zh-TW": "烹飪與營養", "en": "Cooking & Nutrition", "ja": "料理・栄養", "ko": "요리 & 영양", "de": "Kochen & Ernährung", "fr": "Cuisine & Nutrition", "es": "Cocina y Nutrición", "pt": "Culinária & Nutrição", "id": "Memasak & Nutrisi", "zh-CN": "烹饪与营养"},
        "icon": "🍳",
        "slugs": ["recipe-scaler","unit-converter-cooking","baking-conversion","nutrition-calculator","meal-prep-cost","food-cost-percentage","tip-split","restaurant-markup","coffee-cost","grocery-budget","food-waste","serving-size","alcohol-dilution","brine-calculator","sourdough-calculator"]
    },
    "datetime": {
        "names": {"zh-TW": "日期與時間", "en": "Date & Time", "ja": "日付・時刻", "ko": "날짜 & 시간", "de": "Datum & Zeit", "fr": "Date & Heure", "es": "Fecha y Hora", "pt": "Data & Hora", "id": "Tanggal & Waktu", "zh-CN": "日期与时间"},
        "icon": "📅",
        "slugs": ["age-calculator","date-difference","workday-calculator","timezone-converter","countdown-timer"]
    },
    "math": {
        "names": {"zh-TW": "數學與統計", "en": "Math & Statistics", "ja": "数学・統計", "ko": "수학 & 통계", "de": "Mathematik & Statistik", "fr": "Maths & Statistiques", "es": "Matemáticas y Estadística", "pt": "Matemática & Estatística", "id": "Matematika & Statistik", "zh-CN": "数学与统计"},
        "icon": "📐",
        "slugs": ["percentage-calculator","fraction-calculator","scientific-notation","standard-deviation","probability","permutation-combination","logarithm","quadratic-equation"]
    },
    "unit": {
        "names": {"zh-TW": "單位換算", "en": "Unit Conversion", "ja": "単位変換", "ko": "단위 변환", "de": "Einheitenumrechnung", "fr": "Conversion d'unités", "es": "Conversión de unidades", "pt": "Conversão de unidades", "id": "Konversi Satuan", "zh-CN": "单位换算"},
        "icon": "🔄",
        "slugs": ["length-converter","weight-converter","temperature-converter","area-converter","volume-converter"]
    },
}

# Build slug→category reverse lookup
SLUG_TO_CAT = {}
for ck, cd in TOOL_CATEGORIES.items():
    for s in cd["slugs"]:
        SLUG_TO_CAT[s] = ck


def sp(msg):
    try: print(msg)
    except: print(msg.encode("utf-8", errors="replace").decode("utf-8"))


def get_tool_url(slug, lang):
    return f"/tools/{slug}.html" if lang == "zh-TW" else f"/tools/{lang}/{slug}.html"


def build_lang_dropdown(lang, page_type="tool-index"):
    opts = []
    for l in LANGS:
        if page_type == "tool-index":
            url = "/tools/" if l == "zh-TW" else f"/tools/{l}/"
        elif page_type == "blog-index":
            url = "/blog/" if l == "zh-TW" else f"/blog/{l}/index.html"
        else:
            url = "#"
        sel = " selected" if l == lang else ""
        opts.append(f'<option value="{url}"{sel}>{LANG_NAMES[l]}</option>')
    return f'<select onchange="location.href=this.value" style="padding:4px 8px;border-radius:6px;border:1px solid #CBD5E0;font-size:13px;background:#fff;color:#4A5568;cursor:pointer">{"".join(opts)}</select>'


def scan_tools(lang):
    """Scan tool files for a language, extract name from <title>."""
    d = TOOLS_DIR if lang == "zh-TW" else os.path.join(TOOLS_DIR, lang)
    if not os.path.isdir(d):
        return {}

    result = {}
    for fname in os.listdir(d):
        if not fname.endswith(".html") or fname == "index.html":
            continue
        slug = fname[:-5]
        cat = SLUG_TO_CAT.get(slug, "other")
        fpath = os.path.join(d, fname)

        # Extract title from <title> tag, strip suffix after " - "
        title = slug.replace("-", " ").title()
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                head = f.read(2000)
            m = re.search(r"<title>(.*?)</title>", head)
            if m:
                raw = m.group(1).strip()
                # Strip " - SoftGlow" or " - 免費計算" etc suffix
                title = re.split(r"\s*[-–—|]\s*", raw)[0].strip()
                if not title:
                    title = raw
        except:
            pass

        if cat not in result:
            result[cat] = []
        result[cat].append({"slug": slug, "title": title})

    for k in result:
        result[k].sort(key=lambda x: x["slug"])
    return result


def build_index_html(lang, tools_by_cat):
    dropdown = build_lang_dropdown(lang, "tool-index")
    tools_url = "/tools/" if lang == "zh-TW" else f"/tools/{lang}/"
    blog_url = "/blog/" if lang == "zh-TW" else f"/blog/{lang}/index.html"
    patterns_url = "/patterns/index.html" if lang == "zh-TW" else f"/patterns/{lang}.html"

    # hreflang
    hrefs = []
    for l in LANGS:
        u = "https://softglow-ai.com/tools/" if l == "zh-TW" else f"https://softglow-ai.com/tools/{l}/"
        hrefs.append(f'<link rel="alternate" hreflang="{l.lower()}" href="{u}">')
    hrefs.append('<link rel="alternate" hreflang="x-default" href="https://softglow-ai.com/tools/en/">')
    hreflang_str = "\n".join(hrefs)

    canonical = "https://softglow-ai.com/tools/" if lang == "zh-TW" else f"https://softglow-ai.com/tools/{lang}/"
    page_title = {"zh-TW":"免費線上工具","en":"Free Online Tools","ja":"無料オンラインツール","ko":"무료 온라인 도구","de":"Kostenlose Online-Tools","fr":"Outils en ligne gratuits","es":"Herramientas en línea gratuitas","pt":"Ferramentas online gratuitas","id":"Alat Online Gratis","zh-CN":"免费在线工具"}.get(lang,"Free Online Tools")
    page_desc = {"zh-TW":"超過300個免費線上計算工具","en":"Over 300 free online calculators"}.get(lang,"Over 300 free online calculators")

    cat_order = ["finance","health","realestate","tax","insurance","loan","medical","ecommerce","construction","energy","auto","hr","startup","education","legal","textile","cooking","datetime","math","unit","other"]
    sections = []
    total = 0
    for ck in cat_order:
        if ck not in tools_by_cat:
            continue
        tools = tools_by_cat[ck]
        total += len(tools)
        ci = TOOL_CATEGORIES.get(ck, {"names":{"en":"Other"},"icon":"🔧"})
        cname = ci.get("names",{}).get(lang, ci.get("names",{}).get("en", ck))
        cicon = ci.get("icon","🔧")
        links = "\n        ".join(f'<a href="{get_tool_url(t["slug"],lang)}" class="tool-card">{t["title"]}</a>' for t in tools)
        sections.append(f'''
    <section class="cat-section">
      <h2 class="cat-title">{cicon} {cname} <span class="cat-count">({len(tools)})</span></h2>
      <div class="tools-grid">
        {links}
      </div>
    </section>''')

    count_label = "個免費工具" if lang in ("zh-TW","zh-CN") else " free tools"

    return f'''<!DOCTYPE html>
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
    <a href="{tools_url}">{NAV_LABELS["tools"].get(lang,"Tools")}</a>
    <a href="{blog_url}">{NAV_LABELS["blog"].get(lang,"Blog")}</a>
    <a href="{patterns_url}">{NAV_LABELS["patterns"].get(lang,"Patterns")}</a>
    <a href="/">{NAV_LABELS["home"].get(lang,"Home")}</a>
    {dropdown}
  </div>
</div>
</nav>
<div class="container">
  <div class="page-header">
    <h1>{page_title}</h1>
    <p>{total}{count_label}</p>
  </div>
  {"".join(sections)}
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


def fix_blog_dropdown():
    """Add language dropdown to blog pages that don't have one."""
    fixed = 0
    for root, _, files in os.walk(BLOG_DIR):
        for fname in files:
            if not fname.endswith(".html"):
                continue
            fp = os.path.join(root, fname)
            try:
                with open(fp, "r", encoding="utf-8") as f:
                    content = f.read()
            except:
                continue

            # Detect lang
            parts = fp.replace("\\", "/").split("/")
            lang = "zh-TW"
            for l in LANGS:
                if l in parts:
                    lang = l
                    break

            slug = fname[:-5]

            # Check if dropdown already exists
            if '<select onchange="location.href=this.value"' in content:
                continue

            # Build blog dropdown
            opts = []
            for l in LANGS:
                if slug == "index":
                    url = "/blog/" if l == "zh-TW" else f"/blog/{l}/index.html"
                else:
                    url = f"/blog/{slug}.html" if l == "zh-TW" else f"/blog/{l}/{slug}.html"
                sel = " selected" if l == lang else ""
                opts.append(f'<option value="{url}"{sel}>{LANG_NAMES[l]}</option>')
            dropdown = f'<select onchange="location.href=this.value" style="padding:4px 8px;border-radius:6px;border:1px solid #CBD5E0;font-size:13px;background:#fff;color:#4A5568;cursor:pointer">{"".join(opts)}</select>'

            # Try to insert into nav-links
            nav_pattern = r'(</div>\s*</div>\s*</nav>)'
            # Alternative: insert before </nav>
            if '</nav>' in content:
                # Find the nav closing area and insert dropdown
                # Look for nav-links div
                if 'class="nav-links"' in content:
                    content = content.replace('</div>\n</div>\n</nav>', f'{dropdown}\n</div>\n</div>\n</nav>')
                elif 'nav-links' in content:
                    content = re.sub(r'(class="nav-links"[^>]*>)', r'\1\n    ' + dropdown, content, count=1)
                else:
                    # Insert before </nav>
                    content = content.replace('</nav>', f'<div style="position:absolute;right:20px;top:14px">{dropdown}</div></nav>')

                with open(fp, "w", encoding="utf-8") as f:
                    f.write(content)
                fixed += 1

    return fixed


def main():
    sp("=" * 60)
    sp("Fix Index v2 — Use <title> for tool names + blog dropdown")
    sp("=" * 60)

    if not os.path.isdir(TOOLS_DIR):
        sp(f"[ERROR] {TOOLS_DIR} not found")
        sys.exit(1)

    # 1. Rebuild tool index pages
    sp("\n[1/2] Rebuilding tool index pages (using <title> for names)...")
    for lang in LANGS:
        tools_by_cat = scan_tools(lang)
        if not tools_by_cat:
            sp(f"  SKIP {lang}: no tools")
            continue
        total = sum(len(v) for v in tools_by_cat.values())
        html = build_index_html(lang, tools_by_cat)
        if lang == "zh-TW":
            out = os.path.join(TOOLS_DIR, "index.html")
        else:
            os.makedirs(os.path.join(TOOLS_DIR, lang), exist_ok=True)
            out = os.path.join(TOOLS_DIR, lang, "index.html")
        with open(out, "w", encoding="utf-8") as f:
            f.write(html)
        # Show sample tool name for verification
        sample = list(tools_by_cat.values())[0][0]["title"] if tools_by_cat else "?"
        sp(f"  {lang}: {total} tools | sample: {sample}")

    # 2. Fix blog dropdowns
    sp("\n[2/2] Adding language dropdown to blog pages...")
    blog_fixed = fix_blog_dropdown()
    sp(f"  Fixed: {blog_fixed} blog pages")

    sp(f"\n{'='*60}")
    sp("Done! Push:")
    sp("  cd D:\\xian-shang-you-wei")
    sp("  git add -A")
    sp('  git commit -m "fix: tool index names + blog lang dropdown"')
    sp("  git push")


if __name__ == "__main__":
    main()
