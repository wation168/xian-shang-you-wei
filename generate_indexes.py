#!/usr/bin/env python3
"""
generate_indexes.py — 掃描 frontend/tools/ 產生 10 語言索引頁
用法：python generate_indexes.py
"""
import os, re, html

BASE = r"D:\xian-shang-you-wei\backend\frontend\tools"

LANGS = [
    ("zh-TW", None),       # zh-TW 在根目錄
    ("en", "en"),
    ("ja", "ja"),
    ("ko", "ko"),
    ("de", "de"),
    ("fr", "fr"),
    ("es", "es"),
    ("pt", "pt"),
    ("id", "id"),
    ("zh-CN", "zh-CN"),
]

LANG_LABELS = {
    "zh-TW": "🇹🇼 繁體中文", "en": "🇺🇸 English", "ja": "🇯🇵 日本語",
    "ko": "🇰🇷 한국어", "de": "🇩🇪 Deutsch", "fr": "🇫🇷 Français",
    "es": "🇪🇸 Español", "pt": "🇧🇷 Português", "id": "🇮🇩 Indonesia",
    "zh-CN": "🇨🇳 简体中文",
}

# ── 分類映射（slug → category_id）──
CAT_MAP = {}
_CATS = {
    "finance": [
        "compound-interest","roi-calculator","risk-reward","position-size","stop-loss",
        "dividend-yield","pe-ratio","dca-calculator","cagr","fibonacci-retracement",
        "pivot-point","rsi-calculator","macd-calculator","bollinger-bands","atr-calculator",
        "sharpe-ratio","ma-crossover","candlestick-identifier","support-resistance",
        "stock-gain-loss","trading-fee","stock-split","average-down","break-even",
        "rule-of-72","asset-allocation","dcf-calculator","intrinsic-value","options-profit",
        "bond-yield","eps-calculator","pb-ratio","forex-profit","future-value",
        "present-value","simple-interest","irr-calculator","kelly-criterion",
        "gross-profit-margin","net-profit-margin","working-capital","debt-to-equity",
        "inventory-turnover","margin-calculator","markup-margin","compound-interest-debt",
        "annuity-calculator","annuity-income","currency-converter","pip-value",
    ],
    "health": [
        "bmi-calculator","bmr-calculator","body-fat-calculator","calorie-calculator",
        "heart-rate-zone","ideal-weight","lean-body-mass","macro-calculator",
        "one-rep-max","protein-calculator","tdee-calculator","waist-hip-ratio",
        "blood-pressure-chart","water-intake","sleep-calculator","pace-calculator",
        "baby-growth","ovulation-calculator","pregnancy-due-date","caffeine-calculator",
        "glycemic-load","bac-calculator","calorie-density","sodium-calculator",
        "vitamin-calculator",
    ],
    "realestate": [
        "home-mortgage","mortgage","mortgage-refinance","rent-vs-buy",
        "home-affordability","home-equity","rental-yield","rental-income-tax",
        "cap-rate","cash-on-cash","property-tax","down-payment",
        "refinance-break-even","stamp-duty","rehab-cost-estimator","renovation-cost",
        "heloc-vs-personal-loan",
    ],
    "tax": [
        "income-tax","effective-tax-rate","capital-gains-tax","bonus-tax",
        "payroll-tax","take-home-pay","salary-to-hourly","salary-raise",
        "overtime-calculator","overtime-limit","minimum-wage","vat-calculator",
        "freelancer-tax","severance-calculator",
    ],
    "insurance": [
        "life-insurance-calc","life-insurance-needs","term-vs-whole-life",
        "car-insurance-calc","car-insurance-estimate","home-insurance-calc",
        "health-insurance-estimate","health-deductible-calc","pet-insurance-calc",
        "renters-insurance","travel-insurance-calc","disability-insurance",
        "critical-illness-calc","business-insurance","umbrella-insurance",
        "insurance-premium-compare","long-term-care","roi-of-insurance",
        "coverage-gap-finder","oop-maximum-calc","premium-vs-hdhp",
        "income-replacement","fsa-savings-calc","hsa-contribution-calc","liability-insurance",
    ],
    "loan": [
        "loan-comparison","loan-affordability","personal-loan-calc","car-loan",
        "student-loan","student-loan-refi","debt-consolidation","debt-to-income",
        "credit-card-payoff","credit-score-impact","extra-payment","balloon-payment",
        "payday-loan-cost","business-loan-calc","apr-calculator","late-payment-interest",
        "loan-vs-lease","0-percent-financing","penalty-interest","legal-interest",
        "cost-of-living",
    ],
    "medical": [
        "medical-cost-estimator","dental-cost-calculator","surgery-cost-estimator",
        "lasik-cost-calculator","ivf-cost-calculator","therapy-cost-calc",
        "medication-cost-compare","medical-tourism-saving","nursing-home-cost",
    ],
    "ecommerce": [
        "amazon-profit","fba-fee-calculator","shopee-profit","dropship-margin",
        "cbm-calculator","container-load","shipping-cost","dimensional-weight",
        "pallet-calculator","customs-duty","landed-cost","influencer-rate",
        "email-roi","conversion-rate","pricing-calculator","youtube-revenue",
        "roas-calculator",
    ],
    "construction": [
        "concrete-calculator","brick-calculator","gravel-calculator","lumber-calculator",
        "rebar-calculator","asphalt-calculator","deck-calculator","fence-calculator",
        "drywall-calculator","flooring-calculator","tile-calculator","paint-calculator",
        "wallpaper-calculator","roof-area","room-area","staircase-calculator",
        "insulation-calculator","window-size","pool-volume","pipe-weight",
    ],
    "energy": [
        "electricity-cost","solar-panel-count","solar-roi","led-savings",
        "ev-charging-cost","ev-range","ev-vs-gas","generator-size","gas-bill",
        "home-energy-audit","appliance-energy","battery-calculator","carbon-footprint",
        "water-bill",
    ],
    "auto": [
        "car-depreciation","car-lease-vs-buy","fuel-cost","fuel-efficiency",
        "trip-fuel","tire-size","engine-horsepower","parking-cost","commute-cost",
        "bike-gear-ratio","gear-ratio",
    ],
    "business": [
        "employee-cost","meeting-cost","burn-rate-calculator","churn-rate",
        "mrr-calculator","ltv-calculator","saas-ltv-cac","customer-acquisition",
        "startup-valuation","startup-cost-estimator","runway-calculator","equity-dilution",
        "company-registration","payback-period","ebitda-valuation","business-exit-value",
        "valuation-calculator","franchise-roi","freelance-rate","annual-leave","work-days",
        "sales-commission",
    ],
    "retirement": [
        "retirement","retirement-savings-gap","retirement-income-need","retirement-age",
        "fire-number-calc","coast-fire-calc","withdrawal-rate","401k-contribution",
        "catch-up-contribution","roth-vs-traditional","pension-vs-lump-sum",
        "required-minimum-dist","college-savings",
    ],
    "education": [
        "gpa-calculator","grade-calculator","final-grade","class-rank","study-time",
        "reading-time","word-count","typing-speed","flashcard-spacing","toefl-ielts",
        "ielts-band","scholarship-calculator","tuition-cost","sample-size",
    ],
    "legal": [
        "court-fee","lawyer-fee","notary-fee","patent-cost","trademark-fee",
        "child-support","alimony-calculator","statute-of-limitations","gdpr-fine",
        "ab-test-significance",
    ],
    "textile": [
        "denier-calculator","gsm-converter","fabric-shrinkage","yarn-weight",
        "paper-weight","clothing-size","shoe-size-converter","ring-size-converter",
    ],
    "cooking": [
        "recipe-scaler","cooking-converter","cooking-weight-volume","food-cost",
        "serving-size","meat-cooking-time","oven-converter","bread-hydration",
        "sourdough-calculator","pizza-dough","coffee-ratio","tip-calculator",
    ],
    "datetime": [
        "date-difference","age-calculator","time-zone-converter","speed-distance-time",
    ],
    "math": [
        "percentage-calculator","standard-deviation","probability-calculator",
        "confidence-interval","regression-calculator","correlation-calculator",
        "weighted-average","ohms-law",
    ],
    "unit": [
        "land-area-converter","temperature-converter","metal-weight","steel-weight",
        "wire-gauge","bolt-torque","air-conditioner-size",
    ],
}
for _cid, _slugs in _CATS.items():
    for _s in _slugs:
        CAT_MAP[_s] = _cid

# ── 分類名稱 10 語言 ──
CAT_NAMES = {
    "finance":      {"zh-TW":"投資理財","en":"Finance & Investment","ja":"投資・金融","ko":"투자 & 금융","de":"Finanzen & Investitionen","fr":"Finance & Investissement","es":"Finanzas e Inversión","pt":"Finanças e Investimento","id":"Keuangan & Investasi","zh-CN":"投资理财"},
    "health":       {"zh-TW":"健康體適能","en":"Health & Fitness","ja":"健康・フィットネス","ko":"건강 & 피트니스","de":"Gesundheit & Fitness","fr":"Santé & Fitness","es":"Salud y Fitness","pt":"Saúde e Fitness","id":"Kesehatan & Kebugaran","zh-CN":"健康体适能"},
    "realestate":   {"zh-TW":"房地產","en":"Real Estate","ja":"不動産","ko":"부동산","de":"Immobilien","fr":"Immobilier","es":"Bienes Raíces","pt":"Imóveis","id":"Properti","zh-CN":"房地产"},
    "tax":          {"zh-TW":"稅務薪資","en":"Tax & Salary","ja":"税金・給与","ko":"세금 & 급여","de":"Steuern & Gehalt","fr":"Impôts & Salaire","es":"Impuestos y Salario","pt":"Impostos e Salário","id":"Pajak & Gaji","zh-CN":"税务薪资"},
    "insurance":    {"zh-TW":"保險估算","en":"Insurance","ja":"保険","ko":"보험","de":"Versicherung","fr":"Assurance","es":"Seguros","pt":"Seguros","id":"Asuransi","zh-CN":"保险估算"},
    "loan":         {"zh-TW":"貸款信用","en":"Loans & Credit","ja":"ローン・信用","ko":"대출 & 신용","de":"Kredite","fr":"Prêts & Crédit","es":"Préstamos y Crédito","pt":"Empréstimos e Crédito","id":"Pinjaman & Kredit","zh-CN":"贷款信用"},
    "medical":      {"zh-TW":"醫療費用","en":"Medical Costs","ja":"医療費用","ko":"의료비","de":"Medizinische Kosten","fr":"Coûts Médicaux","es":"Costos Médicos","pt":"Custos Médicos","id":"Biaya Medis","zh-CN":"医疗费用"},
    "ecommerce":    {"zh-TW":"電商物流","en":"E-Commerce & Logistics","ja":"EC・物流","ko":"이커머스 & 물류","de":"E-Commerce & Logistik","fr":"E-Commerce & Logistique","es":"E-Commerce y Logística","pt":"E-Commerce e Logística","id":"E-Commerce & Logistik","zh-CN":"电商物流"},
    "construction": {"zh-TW":"建築裝修","en":"Construction","ja":"建築・リフォーム","ko":"건축 & 인테리어","de":"Bau & Renovierung","fr":"Construction","es":"Construcción","pt":"Construção","id":"Konstruksi","zh-CN":"建筑装修"},
    "energy":       {"zh-TW":"電力能源","en":"Energy & Utilities","ja":"エネルギー","ko":"에너지 & 유틸리티","de":"Energie","fr":"Énergie","es":"Energía","pt":"Energia","id":"Energi","zh-CN":"电力能源"},
    "auto":         {"zh-TW":"汽車交通","en":"Auto & Transport","ja":"自動車・交通","ko":"자동차 & 교통","de":"Auto & Verkehr","fr":"Auto & Transport","es":"Auto y Transporte","pt":"Auto e Transporte","id":"Otomotif & Transportasi","zh-CN":"汽车交通"},
    "business":     {"zh-TW":"創業企業","en":"Business & Startup","ja":"ビジネス・起業","ko":"비즈니스 & 창업","de":"Business & Startup","fr":"Business & Startup","es":"Negocios y Startups","pt":"Negócios e Startups","id":"Bisnis & Startup","zh-CN":"创业企业"},
    "retirement":   {"zh-TW":"退休規劃","en":"Retirement Planning","ja":"退職計画","ko":"은퇴 계획","de":"Ruhestandsplanung","fr":"Planification Retraite","es":"Planificación Jubilación","pt":"Planejamento Aposentadoria","id":"Perencanaan Pensiun","zh-CN":"退休规划"},
    "education":    {"zh-TW":"教育學術","en":"Education","ja":"教育","ko":"교육","de":"Bildung","fr":"Éducation","es":"Educación","pt":"Educação","id":"Pendidikan","zh-CN":"教育学术"},
    "legal":        {"zh-TW":"法律合規","en":"Legal & Compliance","ja":"法律・コンプライアンス","ko":"법률 & 규정","de":"Recht & Compliance","fr":"Juridique","es":"Legal y Cumplimiento","pt":"Jurídico","id":"Hukum & Kepatuhan","zh-CN":"法律合规"},
    "textile":      {"zh-TW":"紡織尺寸","en":"Textile & Sizing","ja":"テキスタイル・サイズ","ko":"섬유 & 사이즈","de":"Textil & Größen","fr":"Textile & Tailles","es":"Textil y Tallas","pt":"Têxtil e Tamanhos","id":"Tekstil & Ukuran","zh-CN":"纺织尺寸"},
    "cooking":      {"zh-TW":"烹飪營養","en":"Cooking & Nutrition","ja":"料理・栄養","ko":"요리 & 영양","de":"Kochen & Ernährung","fr":"Cuisine & Nutrition","es":"Cocina y Nutrición","pt":"Culinária e Nutrição","id":"Memasak & Nutrisi","zh-CN":"烹饪营养"},
    "datetime":     {"zh-TW":"日期時間","en":"Date & Time","ja":"日付・時間","ko":"날짜 & 시간","de":"Datum & Zeit","fr":"Date & Heure","es":"Fecha y Hora","pt":"Data e Hora","id":"Tanggal & Waktu","zh-CN":"日期时间"},
    "math":         {"zh-TW":"數學統計","en":"Math & Statistics","ja":"数学・統計","ko":"수학 & 통계","de":"Mathematik & Statistik","fr":"Maths & Statistiques","es":"Matemáticas y Estadística","pt":"Matemática e Estatística","id":"Matematika & Statistik","zh-CN":"数学统计"},
    "unit":         {"zh-TW":"單位換算","en":"Unit Conversion","ja":"単位変換","ko":"단위 변환","de":"Einheitenumrechnung","fr":"Conversion d'Unités","es":"Conversión de Unidades","pt":"Conversão de Unidades","id":"Konversi Satuan","zh-CN":"单位换算"},
    "other":        {"zh-TW":"其他工具","en":"Other Tools","ja":"その他","ko":"기타 도구","de":"Sonstige","fr":"Autres Outils","es":"Otras Herramientas","pt":"Outras Ferramentas","id":"Lainnya","zh-CN":"其他工具"},
}

CAT_ORDER = ["finance","health","realestate","tax","insurance","loan","medical",
             "ecommerce","construction","energy","auto","business","retirement",
             "education","legal","textile","cooking","datetime","math","unit","other"]

# ── 頁面翻譯 ──
PAGE_I18N = {
    "zh-TW": {"title":"免費財務計算機與工具","desc":"用於投資、交易和財務規劃的免費線上計算機。","h1":"免費財務計算機與工具","subtitle":"用於投資、交易和財務規劃的免費線上計算機。","nav_tools":"財務工具","count_suffix":"個工具"},
    "en":    {"title":"Free Financial Calculators & Tools","desc":"Free online calculators for investing, trading, and financial planning.","h1":"Free Financial Calculators & Tools","subtitle":"Free online calculators for investing, trading, and financial planning.","nav_tools":"Tools","count_suffix":"tools"},
    "ja":    {"title":"無料金融計算ツール","desc":"投資、取引、財務計画のための無料オンライン計算機。","h1":"無料金融計算ツール","subtitle":"投資、取引、財務計画のための無料オンライン計算機。","nav_tools":"ツール","count_suffix":"ツール"},
    "ko":    {"title":"무료 금융 계산기 & 도구","desc":"투자, 거래, 재무 계획을 위한 무료 온라인 계산기.","h1":"무료 금융 계산기 & 도구","subtitle":"투자, 거래, 재무 계획을 위한 무료 온라인 계산기.","nav_tools":"도구","count_suffix":"도구"},
    "de":    {"title":"Kostenlose Finanzrechner & Tools","desc":"Kostenlose Online-Rechner für Investitionen, Handel und Finanzplanung.","h1":"Kostenlose Finanzrechner & Tools","subtitle":"Kostenlose Online-Rechner für Investitionen, Handel und Finanzplanung.","nav_tools":"Tools","count_suffix":"Tools"},
    "fr":    {"title":"Calculatrices Financières Gratuites","desc":"Calculatrices en ligne gratuites pour l'investissement, le trading et la planification financière.","h1":"Calculatrices Financières Gratuites","subtitle":"Calculatrices en ligne gratuites pour l'investissement, le trading et la planification financière.","nav_tools":"Outils","count_suffix":"outils"},
    "es":    {"title":"Calculadoras Financieras Gratuitas","desc":"Calculadoras en línea gratuitas para inversión, trading y planificación financiera.","h1":"Calculadoras Financieras Gratuitas","subtitle":"Calculadoras en línea gratuitas para inversión, trading y planificación financiera.","nav_tools":"Herramientas","count_suffix":"herramientas"},
    "pt":    {"title":"Calculadoras Financeiras Gratuitas","desc":"Calculadoras online gratuitas para investimento, trading e planejamento financeiro.","h1":"Calculadoras Financeiras Gratuitas","subtitle":"Calculadoras online gratuitas para investimento, trading e planejamento financeiro.","nav_tools":"Ferramentas","count_suffix":"ferramentas"},
    "id":    {"title":"Kalkulator Keuangan Gratis","desc":"Kalkulator online gratis untuk investasi, trading, dan perencanaan keuangan.","h1":"Kalkulator Keuangan Gratis","subtitle":"Kalkulator online gratis untuk investasi, trading, dan perencanaan keuangan.","nav_tools":"Alat","count_suffix":"alat"},
    "zh-CN": {"title":"免费财务计算器与工具","desc":"用于投资、交易和财务规划的免费在线计算器。","h1":"免费财务计算器与工具","subtitle":"用于投资、交易和财务规划的免费在线计算器。","nav_tools":"财务工具","count_suffix":"个工具"},
}

LANG_CODE_MAP = {"zh-TW":"zh-Hant","zh-CN":"zh-Hans","en":"en","ja":"ja","ko":"ko","de":"de","fr":"fr","es":"es","pt":"pt","id":"id"}

def extract_h1(filepath):
    """從 HTML 讀 <h1> 標籤內容"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read(4000)
        m = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.DOTALL)
        if m:
            return html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()
    except:
        pass
    return None

def scan_tools(lang, subdir):
    """掃描目錄，回傳 {slug: display_name}"""
    if subdir:
        d = os.path.join(BASE, subdir)
    else:
        d = BASE
    tools = {}
    if not os.path.isdir(d):
        print(f"  ⚠ 目錄不存在: {d}")
        return tools
    for fn in sorted(os.listdir(d)):
        if fn.endswith(".html") and fn != "index.html":
            slug = fn.replace(".html", "")
            name = extract_h1(os.path.join(d, fn))
            if not name:
                name = slug.replace("-", " ").title()
            tools[slug] = name
    return tools

def tool_href(lang, subdir, slug):
    if subdir:
        return f"/tools/{subdir}/{slug}.html"
    else:
        return f"/tools/{slug}.html"

def index_href(lang, subdir):
    if subdir:
        return f"/tools/{subdir}/"
    else:
        return "/tools/"

def gen_hreflang(lang):
    tags = []
    for l, sd in LANGS:
        href = f"https://softglow-ai.com{index_href(l, sd)}"
        lc = LANG_CODE_MAP[l]
        tags.append(f'<link rel="alternate" hreflang="{lc}" href="{href}">')
    tags.append(f'<link rel="alternate" hreflang="x-default" href="https://softglow-ai.com/tools/">')
    return "\n".join(tags)

def generate_index(lang, subdir, tools):
    i18n = PAGE_I18N[lang]
    total = len(tools)

    # 分類
    grouped = {}
    for slug, name in tools.items():
        cat = CAT_MAP.get(slug, "other")
        grouped.setdefault(cat, []).append((slug, name))

    # 語言按鈕
    lang_btns = []
    for l, sd in LANGS:
        href = index_href(l, sd)
        cls = ' class="lang-btn active"' if l == lang else ' class="lang-btn"'
        lang_btns.append(f'<a href="{href}"{cls}>{LANG_LABELS[l]}</a>')

    # 分類 HTML
    sections = []
    for cid in CAT_ORDER:
        if cid not in grouped:
            continue
        cat_name = CAT_NAMES[cid][lang]
        items = grouped[cid]
        cnt = len(items)
        cards = []
        for slug, name in items:
            href = tool_href(lang, subdir, slug)
            cards.append(f'<a href="{href}" class="tool-card">{html.escape(name)}</a>')
        sections.append(f"""
<section class="cat-section">
  <div class="cat-header"><h2>{html.escape(cat_name)}</h2><span class="cat-count">{cnt} {i18n["count_suffix"]}</span></div>
  <div class="tool-grid">
    {"".join(cards)}
  </div>
</section>""")

    hreflang = gen_hreflang(lang)
    lc = LANG_CODE_MAP[lang]
    canonical = f"https://softglow-ai.com{index_href(lang, subdir)}"

    return f"""<!DOCTYPE html>
<html lang="{lc}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(i18n["title"])} | SoftGlow</title>
<meta name="description" content="{html.escape(i18n["desc"])}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canonical}">
{hreflang}
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;color:#2D3748;background:#fff;line-height:1.6}}
a{{color:#2563EB;text-decoration:none}}
.nav{{position:sticky;top:0;z-index:100;background:rgba(255,255,255,.97);backdrop-filter:blur(8px);border-bottom:1px solid #E2E8F0}}
.nav-inner{{max-width:1080px;margin:0 auto;padding:0 20px;display:flex;align-items:center;justify-content:space-between;height:52px}}
.nav-logo{{font-size:17px;font-weight:700;color:#2D3748}}.nav-logo span{{color:#2563EB}}
.nav-links{{display:flex;gap:16px}}.nav-links a{{font-size:13px;color:#4A5568;font-weight:500}}
.container{{max-width:1080px;margin:0 auto;padding:0 20px}}
.lang-bar{{display:flex;gap:6px;flex-wrap:wrap;padding:16px 0;border-bottom:1px solid #EDF2F7}}
.lang-btn{{font-size:12px;padding:5px 14px;border-radius:20px;background:#F7FAFC;border:1px solid #E2E8F0;color:#718096;white-space:nowrap}}
.lang-btn:hover{{background:#EBF5FF;border-color:#BEE3F8;text-decoration:none}}
.lang-btn.active{{background:#2563EB;color:#fff;border-color:#2563EB}}
.page-header{{padding:28px 0 12px}}
.page-header h1{{font-size:26px;font-weight:700;color:#1A202C}}
.page-header p{{font-size:15px;color:#718096;margin-top:4px}}
.total-badge{{display:inline-block;background:#EBF5FF;color:#2563EB;font-size:13px;font-weight:600;padding:3px 12px;border-radius:20px;margin-top:8px}}
.cat-section{{margin:28px 0}}
.cat-header{{display:flex;align-items:baseline;gap:10px;margin-bottom:12px;padding-bottom:8px;border-bottom:2px solid #2563EB}}
.cat-header h2{{font-size:18px;font-weight:700;color:#1A202C}}
.cat-count{{font-size:12px;color:#A0AEC0}}
.tool-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:10px}}
.tool-card{{display:block;padding:14px 16px;background:#F7FAFC;border:1px solid #E2E8F0;border-radius:10px;font-size:14px;color:#2D3748;font-weight:500;transition:all .15s}}
.tool-card:hover{{background:#EBF5FF;border-color:#BEE3F8;color:#2563EB;text-decoration:none;transform:translateY(-1px);box-shadow:0 2px 8px rgba(0,0,0,.06)}}
.footer{{border-top:1px solid #E2E8F0;padding:20px 0;margin-top:40px}}
.footer-inner{{max-width:1080px;margin:0 auto;padding:0 20px;display:flex;flex-wrap:wrap;gap:16px;font-size:12px;color:#A0AEC0}}
.footer-inner a{{color:#718096}}
@media(max-width:640px){{
  .page-header h1{{font-size:21px}}
  .tool-grid{{grid-template-columns:1fr}}
  .tool-card{{padding:16px}}
}}
</style>
</head>
<body>
<nav class="nav"><div class="nav-inner">
  <a href="/" class="nav-logo">Soft<span>Glow</span></a>
  <div class="nav-links">
    <a href="{index_href(lang, subdir)}">{html.escape(i18n["nav_tools"])}</a>
    <a href="/blog/">Blog</a>
    <a href="/">Home</a>
  </div>
</div></nav>

<div class="container">
  <div class="lang-bar">
    {"".join(lang_btns)}
  </div>
  <div class="page-header">
    <h1>{html.escape(i18n["h1"])}</h1>
    <p>{html.escape(i18n["subtitle"])}</p>
    <span class="total-badge">{total} {i18n["count_suffix"]}</span>
  </div>
  {"".join(sections)}
</div>

<footer class="footer"><div class="footer-inner">
  <a href="/about.html">About</a>
  <a href="/contact.html">Contact</a>
  <a href="/privacy.html">Privacy</a>
  <a href="/terms.html">Terms</a>
  <span style="margin-left:auto">&copy; 2026 SoftGlow</span>
</div></footer>

<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1768270548115739" crossorigin="anonymous"></script>
</body>
</html>"""

def main():
    print("=== 掃描工具頁面，產生 10 語言索引頁 ===\n")
    for lang, subdir in LANGS:
        print(f"[{lang}] 掃描中...")
        tools = scan_tools(lang, subdir)
        if not tools:
            print(f"  ⚠ 沒有找到工具頁面，跳過")
            continue
        print(f"  找到 {len(tools)} 個工具")

        html_content = generate_index(lang, subdir, tools)
        if subdir:
            out_dir = os.path.join(BASE, subdir)
        else:
            out_dir = BASE
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "index.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"  ✅ 已寫入 {out_path}")

    print("\n=== 完成！所有索引頁已產生 ===")

if __name__ == "__main__":
    main()
