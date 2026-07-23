# -*- coding: utf-8 -*-
"""
enrich_lottery_v2.py - Fixed version
1. FAQ injection: checks for actual FAQ HTML content, not just CSS class
2. Sidebar: replaces entire broken sidebar with proper lottery links
3. Index: shows all 15 lotteries, links to en/ for missing local pages
"""
import os, re, json, html as html_mod

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend", "frontend", "lottery")

LOTTERIES = {
    "powerball": {"name":"Powerball","country":"USA","pick":5,"range":69,"bonus":1,"brange":26,"days":"Mon/Wed/Sat","time":"22:59 ET","odds":"1:292,201,338","bet":"$2","currency":"USD","tax":"37% federal + state tax","claim":"Winners have 180 days to 1 year depending on state. Jackpots can be taken as annuity (30 years) or lump sum (approx. 60% of advertised amount)."},
    "mega-millions": {"name":"Mega Millions","country":"USA","pick":5,"range":70,"bonus":1,"brange":24,"days":"Tue/Fri","time":"23:00 ET","odds":"1:302,575,350","bet":"$2","currency":"USD","tax":"37% federal + state tax","claim":"Winners have 180 days to 1 year depending on state."},
    "euromillions": {"name":"EuroMillions","country":"Europe","pick":5,"range":50,"bonus":2,"brange":12,"days":"Tue/Fri","time":"21:00 CET","odds":"1:139,838,160","bet":"\u20ac2.50","currency":"EUR","tax":"Varies by country. UK, France, Germany: tax-free. Spain: 20% over \u20ac40,000.","claim":"Winners typically have 90 days to 1 year depending on country."},
    "lotto-max": {"name":"Lotto Max","country":"Canada","pick":7,"range":50,"bonus":0,"brange":0,"days":"Tue/Fri","time":"22:30 ET","odds":"1:33,294,800","bet":"$5 CAD","currency":"CAD","tax":"Tax-free in Canada.","claim":"Winners have 1 year from the draw date."},
    "uk-lotto": {"name":"UK Lotto","country":"UK","pick":6,"range":59,"bonus":0,"brange":0,"days":"Wed/Sat","time":"20:00 GMT","odds":"1:45,057,474","bet":"\u00a32","currency":"GBP","tax":"Tax-free in the UK.","claim":"Winners have 180 days."},
    "el-gordo": {"name":"El Gordo","country":"Spain","pick":5,"range":54,"bonus":0,"brange":0,"days":"Sun","time":"21:30 CET","odds":"1:31,625,100","bet":"\u20ac1.50","currency":"EUR","tax":"20% on amounts over \u20ac40,000.","claim":"Winners have 3 months."},
    "superenalotto": {"name":"SuperEnalotto","country":"Italy","pick":6,"range":90,"bonus":1,"brange":90,"days":"Tue/Thu/Fri/Sat","time":"20:00 CET","odds":"1:622,614,630","bet":"\u20ac1","currency":"EUR","tax":"20% on amounts over \u20ac500.","claim":"Winners have 90 days."},
    "lotto-6aus49": {"name":"Lotto 6aus49","country":"Germany","pick":6,"range":49,"bonus":1,"brange":9,"days":"Wed/Sat","time":"18:25 CET","odds":"1:139,838,160","bet":"\u20ac1.20","currency":"EUR","tax":"Tax-free in Germany.","claim":"Winners have 13 weeks."},
    "oz-lotto": {"name":"Oz Lotto","country":"Australia","pick":7,"range":47,"bonus":2,"brange":47,"days":"Tue","time":"20:30 AEST","odds":"1:45,379,620","bet":"A$1.50","currency":"AUD","tax":"Tax-free in Australia.","claim":"Winners typically have 6 years (varies by state)."},
    "taiwan-bingo": {"name_zh":"\u5a01\u529b\u5f69","name":"Power Lottery","country":"Taiwan","pick":6,"range":38,"bonus":1,"brange":8,"days":"Mon/Thu","time":"20:30 CST","odds":"1:22,085,448","bet":"NT$100","currency":"TWD","tax":"10% (NT$5,001-20M), 20% (over NT$20M)","claim":"Winners have 3 months. Prizes are paid in full."},
    "taiwan-lotto": {"name_zh":"\u5927\u6a02\u900f","name":"Super Lotto","country":"Taiwan","pick":6,"range":49,"bonus":1,"brange":49,"days":"Tue/Fri","time":"20:30 CST","currency":"TWD","bet":"NT$50","odds":"1:13,983,816","tax":"10% (NT$5,001-20M), 20% (over NT$20M)","claim":"Winners have 3 months."},
    "daily-cash": {"name_zh":"\u4eca\u5f69539","name":"Daily Cash 539","country":"Taiwan","pick":5,"range":39,"bonus":0,"brange":0,"days":"Mon-Sat","time":"20:30 CST","currency":"TWD","bet":"NT$50","odds":"1:575,757","tax":"10% (NT$5,001-20M), 20% (over NT$20M)","claim":"Fixed first prize NT$8 million. Winners have 3 months."},
    "mega-sena": {"name":"Mega-Sena","country":"Brazil","pick":6,"range":60,"bonus":0,"brange":0,"days":"Tue/Thu/Sat","time":"20:00 BRT","currency":"BRL","bet":"R$5","odds":"1:50,063,860","tax":"30% on amounts over R$1,903.98.","claim":"Winners have 90 days."},
    "korea-lotto": {"name_ko":"\ub85c\ub610 6/45","name":"Korea Lotto 6/45","country":"Korea","pick":6,"range":45,"bonus":1,"brange":45,"days":"Sat","time":"20:45 KST","currency":"KRW","bet":"\u20a91,000","odds":"1:8,145,060","tax":"22% on amounts over \u20a950 million.","claim":"Winners have 1 year."},
    "japan-loto6": {"name_ja":"\u30ed\u30c86","name":"Japan Loto 6","country":"Japan","pick":6,"range":43,"bonus":1,"brange":43,"days":"Mon/Thu","time":"18:45 JST","currency":"JPY","bet":"\u00a5200","odds":"1:6,096,454","tax":"20.315% on all winnings.","claim":"Winners have 1 year."},
}

ALL_SLUGS = list(LOTTERIES.keys())
LANG_FOLDERS = {"zh-TW":"","en":"en","ja":"ja","ko":"ko","fr":"fr","de":"de","es":"es","pt":"pt","id":"id","zh-CN":"zh-CN"}

SIDEBAR_LINKS = {
    "en": [(s, LOTTERIES[s].get("name")) for s in ALL_SLUGS],
    "zh-TW": [(s, LOTTERIES[s].get("name_zh", LOTTERIES[s]["name"])) for s in ALL_SLUGS],
    "ja": [(s, LOTTERIES[s].get("name_ja", LOTTERIES[s]["name"])) for s in ALL_SLUGS],
    "ko": [(s, LOTTERIES[s].get("name_ko", LOTTERIES[s]["name"])) for s in ALL_SLUGS],
}

# ============================================================
# FAQ GENERATION
# ============================================================
def gen_faq(slug, lang):
    c = LOTTERIES[slug]
    n = c.get(f"name_{lang[:2]}", c["name"])
    bonus_text = f", plus {c['bonus']} bonus from 1 to {c['brange']}" if c['bonus']>0 else ""
    bonus_zh = f"\uff0c\u518d\u5f9e 1 \u5230 {c['brange']} \u4e2d\u9078 {c['bonus']} \u500b\u7279\u5225\u865f" if c['bonus']>0 else ""
    
    if lang.startswith("zh"):
        return [
            (f"{n}\u600e\u9ebc\u73a9\uff1f", f"\u5f9e 1 \u5230 {c['range']} \u4e2d\u9078 {c['pick']} \u500b\u865f\u78bc{bonus_zh}\u3002\u6bcf\u6ce8 {c['bet']}\uff0c\u6bcf\u9031 {c['days']} \u65bc {c['time']} \u958b\u734e\u3002"),
            (f"{n}\u7684\u4e2d\u734e\u6a5f\u7387\u662f\u591a\u5c11\uff1f", f"\u982d\u734e\u6a5f\u7387\u70ba {c['odds']}\u3002\u7121\u4eba\u4e2d\u734e\u6642\u734e\u91d1\u6ffe\u5165\u4e0b\u671f\u3002"),
            (f"{n}\u4e2d\u734e\u8981\u7e73\u7a05\u55ce\uff1f", c["tax"]),
            (f"{n}\u4e2d\u734e\u5f8c\u600e\u9ebc\u9818\u734e\uff1f", c["claim"]),
            (f"\u5728\u54ea\u88e1\u67e5\u770b{n}\u958b\u734e\u7d50\u679c\uff1f", f"\u672c\u9801\u63d0\u4f9b\u6700\u65b0\u958b\u734e\u865f\u78bc\u3001\u6b77\u53f2\u7d00\u9304\u3001\u7d71\u8a08\u5206\u6790\u548c\u514d\u8cbb\u9078\u865f\u5de5\u5177\uff0c\u6bcf\u65e5\u81ea\u52d5\u66f4\u65b0\u3002"),
        ]
    else:
        return [
            (f"How do I play {n}?", f"Pick {c['pick']} numbers from 1 to {c['range']}{bonus_text}. Draws: {c['days']} at {c['time']}. Cost: {c['bet']}."),
            (f"What are the odds of winning {n}?", f"Jackpot odds: {c['odds']}. Unclaimed jackpots roll over to the next draw."),
            (f"Are {n} winnings taxed?", c["tax"]),
            (f"How do I claim a {n} prize?", c["claim"]),
            (f"Where can I check {n} results?", f"This page provides latest winning numbers, draw history, statistical analysis, and free number generators. Updated daily."),
        ]


def build_faq_block(slug, lang):
    qs = gen_faq(slug, lang)
    title = {"zh-TW":"\u5e38\u898b\u554f\u984c","zh-CN":"\u5e38\u89c1\u95ee\u9898","ja":"FAQ","ko":"FAQ","de":"FAQ","fr":"FAQ","es":"FAQ","pt":"FAQ","id":"FAQ"}.get(lang, "FAQ")
    
    items = ""
    schema_items = []
    for q, a in qs:
        eq, ea = html_mod.escape(q), html_mod.escape(a)
        items += f'<div class="faq-item"><div class="faq-q">{eq}</div><div class="faq-a">{ea}</div></div>\n'
        schema_items.append({"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}})
    
    schema = json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":schema_items}, ensure_ascii=False)
    
    return f'''<div class="card" style="margin-top:20px">
    <h2>\u2753 {title}</h2>
    {items}
  </div>
  <script type="application/ld+json">{schema}</script>'''


def build_howto_block(slug, lang):
    c = LOTTERIES[slug]
    n = c.get(f"name_{lang[:2]}", c["name"])
    bonus_text = f", plus {c['bonus']} bonus from 1 to {c['brange']}" if c['bonus']>0 else ""
    bonus_zh = f"\uff0c\u518d\u5f9e 1 \u5230 {c['brange']} \u4e2d\u9078 {c['bonus']} \u500b\u7279\u5225\u865f" if c['bonus']>0 else ""
    
    if lang.startswith("zh"):
        steps = [f"\u5f9e 1 \u5230 {c['range']} \u9078 {c['pick']} \u500b\u865f\u78bc{bonus_zh}", f"\u6bcf\u6ce8 {c['bet']}", f"\u958b\u734e\uff1a{c['days']} {c['time']}", f"\u982d\u734e\u6a5f\u7387\uff1a{c['odds']}"]
        t_how, t_tax = f"\u600e\u9ebc\u73a9{n}", "\u7a05\u52d9\u8207\u9818\u734e"
    else:
        steps = [f"Pick {c['pick']} from 1-{c['range']}{bonus_text}", f"Cost: {c['bet']} per entry", f"Draws: {c['days']} at {c['time']}", f"Jackpot odds: {c['odds']}"]
        t_how, t_tax = f"How to Play {n}", "Tax & Prize Claim"
    
    step_html = "".join(f'<div style="display:flex;gap:12px;align-items:flex-start;margin-bottom:12px"><div style="min-width:28px;height:28px;background:#D97706;color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px">{i+1}</div><div style="font-size:14px;color:#4A5568;padding-top:4px">{s}</div></div>' for i,s in enumerate(steps))
    
    return f'''<div class="card" style="margin-top:20px">
    <h2>\U0001f4d6 {t_how}</h2>
    <div style="margin-top:16px">{step_html}</div>
  </div>
  <div class="card" style="margin-top:20px">
    <h2>\U0001f4b0 {t_tax}</h2>
    <p><strong>{"Tax" if not lang.startswith("zh") else "\u7a05\u7387"}:</strong> {c["tax"]}</p>
    <p><strong>{"Claiming" if not lang.startswith("zh") else "\u9818\u734e"}:</strong> {c["claim"]}</p>
  </div>'''


def build_sidebar(lang):
    """Build a proper sidebar with all 15 lotteries"""
    folder = LANG_FOLDERS.get(lang, "en")
    lang_path = f"/lottery/{folder}/" if folder else "/lottery/"
    en_path = "/lottery/en/"
    
    # Check which lotteries have local pages
    if folder:
        local_dir = os.path.join(BASE, folder)
    else:
        local_dir = BASE
    
    local_files = set(os.listdir(local_dir)) if os.path.isdir(local_dir) else set()
    
    links = ""
    for slug in ALL_SLUGS:
        name = LOTTERIES[slug].get(f"name_{lang[:2]}", LOTTERIES[slug]["name"])
        if f"{slug}.html" in local_files:
            href = f"{lang_path}{slug}.html"
        else:
            href = f"{en_path}{slug}.html"
        links += f'<a href="{href}">{name}</a>\n'
    
    gen_label = {"zh-TW":"\u751f\u6210 \u2192","zh-CN":"\u751f\u6210 \u2192","ja":"\u751f\u6210 \u2192","ko":"\uc0dd\uc131 \u2192"}.get(lang, "Generate \u2192")
    gen_title = {"zh-TW":"\U0001f3b2 \u9078\u865f\u5de5\u5177","zh-CN":"\U0001f3b2 \u9009\u53f7\u5de5\u5177","ja":"\U0001f3b2 \u756a\u53f7\u751f\u6210","ko":"\U0001f3b2 \ubc88\ud638 \uc0dd\uc131"}.get(lang, "\U0001f3b2 Number Generator")
    all_title = {"zh-TW":"\U0001f30f \u6240\u6709\u5f69\u7968","zh-CN":"\U0001f30f \u6240\u6709\u5f69\u7968","ja":"\U0001f30f \u5168\u5b9d\u304f\u3058","ko":"\U0001f30f \ubaa8\ub4e0 \ubcf5\uad8c"}.get(lang, "\U0001f30f All Lotteries")
    
    return f'''<aside class="sidebar"><div class="ad-slot" id="ad-side"></div>
  <div class="card"><h3>{gen_title}</h3>
    <a href="{lang_path}number-generator.html" class="btn" style="width:100%;display:block;text-align:center">{gen_label}</a></div>
  <div class="card"><h3>{all_title}</h3>
    {links}
  </div>
</aside>'''


# ============================================================
# ENRICHMENT
# ============================================================
def detect_slug(filepath):
    fname = os.path.basename(filepath).replace(".html","")
    for sfx in ["-results","-history","-statistics"]:
        fname = fname.replace(sfx, "")
    return fname

def detect_lang(filepath):
    parts = filepath.replace("\\","/").split("/")
    for p in parts:
        if p in ["en","ja","ko","fr","de","es","pt","id","zh-CN"]:
            return p
    return "zh-TW"

def detect_type(filepath):
    fname = os.path.basename(filepath)
    if "-results" in fname: return "results"
    if "-history" in fname: return "history"
    if "-statistics" in fname: return "statistics"
    return "intro"

def is_lottery_page(filepath):
    fname = os.path.basename(filepath)
    if fname in ["index.html","number-generator.html"]: return False
    tools = ["ai-pick","bazi-pick","birthday-pick","chinese-zodiac-pick","cold-pick",
        "divination-pick","dream-pick","hot-pick","life-event-pick","lucky-number","random-pick","zodiac-pick"]
    slug = detect_slug(filepath)
    return slug in LOTTERIES and slug not in tools

def enrich_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()
    
    slug = detect_slug(filepath)
    lang = detect_lang(filepath)
    ptype = detect_type(filepath)
    if slug not in LOTTERIES:
        return False
    
    modified = False
    
    # 1. Fix broken sidebar — replace entire <aside> block
    sidebar_match = re.search(r'<aside class="sidebar">.*?</aside>', html, re.DOTALL)
    if sidebar_match:
        old_sidebar = sidebar_match.group()
        # Check if sidebar is broken (truncated link or missing lotteries)
        if '<a href="#"' in old_sidebar or old_sidebar.count('<a ') < 5:
            new_sidebar = build_sidebar(lang)
            html = html.replace(old_sidebar, new_sidebar)
            modified = True
    
    # 2. Inject FAQ + How-to-Play for intro pages
    # Check for ACTUAL faq content (not just CSS class definition)
    has_real_faq = '<div class="faq-item"><div class="faq-q">' in html
    
    if ptype == "intro" and not has_real_faq:
        faq = build_faq_block(slug, lang)
        howto = build_howto_block(slug, lang)
        inject = howto + "\n" + faq
        
        # Find injection point: before lang-bar div
        if '<div class="lang-bar">' in html:
            html = html.replace('<div class="lang-bar">', inject + '\n  <div class="lang-bar">')
            modified = True
        # Or before </div> that closes .main
        elif '</div>\n<aside' in html:
            html = html.replace('</div>\n<aside', inject + '\n</div>\n<aside')
            modified = True
    
    # 3. Inject FAQ for results pages too
    if ptype == "results" and not has_real_faq:
        faq = build_faq_block(slug, lang)
        if '<div class="lang-bar">' in html:
            html = html.replace('<div class="lang-bar">', faq + '\n  <div class="lang-bar">')
            modified = True
    
    # 4. Add lottery-live.js if missing
    if 'lottery-live.js' not in html:
        html = html.replace('</body>', '<script src="/js/lottery-live.js" defer></script>\n</body>')
        modified = True
    
    # 5. Add cookie consent if missing
    if 'cookie-consent.css' not in html:
        html = html.replace('</head>', '<link rel="stylesheet" href="/js/cookie-consent.css">\n</head>')
        modified = True
    if 'softglow-cookies.js' not in html:
        html = html.replace('</body>', '<script src="/js/softglow-cookies.js" defer></script>\n</body>')
        modified = True
    
    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
    return modified


# ============================================================
# INDEX FIX — Show all 15 lotteries, fallback to en/
# ============================================================
def fix_all_indexes():
    """Update all index.html to show all 15 lotteries with fallback links"""
    
    I18N_REGIONS = {
        "zh-TW": {"usa":"\u7f8e\u570b","americas":"\u7f8e\u6d32","europe":"\u6b50\u6d32","asia":"\u4e9e\u6d32","oceania":"\u5927\u6d0b\u6d32"},
        "en": {"usa":"USA","americas":"Americas","europe":"Europe","asia":"Asia","oceania":"Oceania"},
        "ja": {"usa":"\u30a2\u30e1\u30ea\u30ab","americas":"\u5357\u5317\u30a2\u30e1\u30ea\u30ab","europe":"\u30e8\u30fc\u30ed\u30c3\u30d1","asia":"\u30a2\u30b8\u30a2","oceania":"\u30aa\u30bb\u30a2\u30cb\u30a2"},
        "ko": {"usa":"\ubbf8\uad6d","americas":"\uc544\uba54\ub9ac\uce74","europe":"\uc720\ub7fd","asia":"\uc544\uc2dc\uc544","oceania":"\uc624\uc138\uc544\ub2c8\uc544"},
        "de": {"usa":"USA","americas":"Amerika","europe":"Europa","asia":"Asien","oceania":"Ozeanien"},
        "fr": {"usa":"\u00c9tats-Unis","americas":"Am\u00e9riques","europe":"Europe","asia":"Asie","oceania":"Oc\u00e9anie"},
        "es": {"usa":"EE.UU.","americas":"Am\u00e9ricas","europe":"Europa","asia":"Asia","oceania":"Ocean\u00eda"},
        "pt": {"usa":"EUA","americas":"Am\u00e9ricas","europe":"Europa","asia":"\u00c1sia","oceania":"Oceania"},
        "id": {"usa":"AS","americas":"Amerika","europe":"Eropa","asia":"Asia","oceania":"Oseania"},
        "zh-CN": {"usa":"\u7f8e\u56fd","americas":"\u7f8e\u6d32","europe":"\u6b27\u6d32","asia":"\u4e9a\u6d32","oceania":"\u5927\u6d0b\u6d32"},
    }
    
    REGION_ORDER = ["usa","americas","europe","asia","oceania"]
    REGION_LOTTERIES = {
        "usa": ["powerball","mega-millions"],
        "americas": ["lotto-max","mega-sena"],
        "europe": ["euromillions","uk-lotto","el-gordo","superenalotto","lotto-6aus49"],
        "asia": ["taiwan-bingo","taiwan-lotto","daily-cash","korea-lotto","japan-loto6"],
        "oceania": ["oz-lotto"],
    }
    
    count = 0
    for lang, folder in LANG_FOLDERS.items():
        lang_dir = os.path.join(BASE, folder) if folder else BASE
        index_path = os.path.join(lang_dir, "index.html")
        if not os.path.exists(index_path):
            continue
        
        with open(index_path, "r", encoding="utf-8") as f:
            html = f.read()
        
        # Check which lotteries have local pages
        local_files = set(os.listdir(lang_dir))
        lang_path = f"/lottery/{folder}/" if folder else "/lottery/"
        en_path = "/lottery/en/"
        regions = I18N_REGIONS.get(lang, I18N_REGIONS["en"])
        
        # Build new lottery grid with ALL 15 lotteries
        sections = []
        for region in REGION_ORDER:
            region_name = regions[region]
            cards = []
            for slug in REGION_LOTTERIES[region]:
                name = LOTTERIES[slug].get(f"name_{lang[:2]}", LOTTERIES[slug]["name"])
                flag = {"powerball":"[USA]","mega-millions":"[USA]","lotto-max":"[CA]","mega-sena":"[BR]",
                    "euromillions":"[EU]","uk-lotto":"[UK]","el-gordo":"[ES]","superenalotto":"[IT]","lotto-6aus49":"[DE]",
                    "taiwan-bingo":"[TW]","taiwan-lotto":"[TW]","daily-cash":"[TW]",
                    "korea-lotto":"[KR]","japan-loto6":"[JP]","oz-lotto":"[AU]"}[slug]
                
                if f"{slug}.html" in local_files:
                    href = f"{lang_path}{slug}.html"
                    badge = ""
                else:
                    href = f"{en_path}{slug}.html"
                    badge = ' <span style="font-size:10px;color:#A0AEC0">(EN)</span>'
                
                cards.append(f'<a href="{href}" class="lottery-card"><div class="flag">{flag}</div><div class="lc-name">{name}{badge}</div></a>')
            
            sections.append(f'<div class="region-title">{region_name}</div><div class="lottery-grid">{"".join(cards)}</div>')
        
        new_grid = "\n  ".join(sections)
        
        # Replace the old lottery grid section
        # Find from first region-title to lang-bar
        grid_pattern = re.compile(r'(<div class="region-title">.*?)(<div class="lang-bar">)', re.DOTALL)
        match = grid_pattern.search(html)
        if match:
            html = html[:match.start(1)] + new_grid + "\n  " + html[match.start(2):]
        else:
            # Try finding the "no lotteries" message and replace
            no_lottery_pattern = re.compile(r'(<div style="background:#FEF3C7.*?</div>)\s*(<div class="lang-bar">)', re.DOTALL)
            match2 = no_lottery_pattern.search(html)
            if match2:
                html = html[:match2.start(1)] + new_grid + "\n  " + html[match2.start(2):]
        
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(html)
        
        local_count = sum(1 for s in ALL_SLUGS if f"{s}.html" in local_files)
        en_count = 15 - local_count
        print(f"  \u2705 {lang:6s} index: 15 lotteries ({local_count} local + {en_count} \u2192 en)")
        count += 1
    
    return count


# ============================================================
# MAIN
# ============================================================
def main():
    print("=" * 60)
    print("Enrich Lottery Pages v2")
    print("=" * 60)
    
    if not os.path.isdir(BASE):
        print(f"Error: {BASE} not found")
        return
    
    # Step 1: Fix indexes
    print("\n--- Fixing index pages (all 15 lotteries) ---")
    fix_all_indexes()
    
    # Step 2: Enrich lottery pages
    print("\n--- Enriching lottery content pages ---")
    enriched = 0
    total = 0
    for root, dirs, files in os.walk(BASE):
        for fname in files:
            if not fname.endswith(".html"):
                continue
            fpath = os.path.join(root, fname)
            if not is_lottery_page(fpath):
                continue
            total += 1
            if enrich_file(fpath):
                enriched += 1
                print(f"  \u2705 {detect_lang(fpath)}/{detect_slug(fpath)}-{detect_type(fpath)}")
    
    print(f"\n--- Summary ---")
    print(f"Lottery pages: {total} total, {enriched} enriched")
    print(f"Done!")


if __name__ == "__main__":
    main()
