#!/usr/bin/env python3
"""
generate_tools_v2.py — SoftGlow v2.1
用法：
  cd D:\\xian-shang-you-wei\\backend
  set ANTHROPIC_API_KEY=sk-ant-api03-你的key
  python generate_tools_v2.py --langs de,fr,es,pt,ko,id,zh-CN
  python generate_tools_v2.py --langs en,zh-TW,ja --rebuild-only  (用快取套新模板)
"""
import os,sys,re,json,time,glob,argparse,traceback
import codecs
if hasattr(sys.stdout,'buffer'):
    sys.stdout=codecs.getwriter('utf-8')(sys.stdout.buffer,errors='replace')
    sys.stderr=codecs.getwriter('utf-8')(sys.stderr.buffer,errors='replace')
try:
    import requests
except ImportError:
    print("[ERROR] pip install requests"); sys.exit(1)

API_URL="https://api.anthropic.com/v1/messages"
MODEL="claude-haiku-4-5-20251001"
MAX_TOKENS=4096
BASE=os.path.dirname(os.path.abspath(__file__))
EN_DIR=os.path.join(BASE,"backend","frontend","tools","en")
OUT_DIR=os.path.join(os.path.dirname(BASE),"output","tools")
CACHE=os.path.join(os.path.dirname(BASE),"output",".cache")
TPL_PATH=os.path.join(BASE,"tool-template-v2.html")
PUB="ca-pub-1768270548115739"
SLOT_SIDE="1655301946"; SLOT_CALC="4182262477"; SLOT_ART="2793159185"
ALL_LANGS=["en","zh-TW","ja","de","fr","es","pt","ko","id","zh-CN"]

LM={
 "en":   {"code":"en","name":"English","nav":"Tools","btn":"Calculate","faq":"FAQ","rel":"Related Tools","more":"More Tools","blog":"Related Articles","pr":"Print","sh":"Share","cp":"Copied!","interp":"What does this mean?"},
 "zh-TW":{"code":"zh-TW","name":"繁體中文","nav":"工具","btn":"計算","faq":"常見問題","rel":"相關工具","more":"更多工具","blog":"延伸閱讀","pr":"列印","sh":"分享","cp":"已複製！","interp":"這代表什麼？"},
 "ja":   {"code":"ja","name":"日本語","nav":"ツール","btn":"計算する","faq":"よくある質問","rel":"関連ツール","more":"その他のツール","blog":"関連記事","pr":"印刷","sh":"共有","cp":"コピー済","interp":"これは何を意味しますか？"},
 "de":   {"code":"de","name":"Deutsch","nav":"Werkzeuge","btn":"Berechnen","faq":"Häufig gestellte Fragen","rel":"Verwandte Rechner","more":"Weitere Werkzeuge","blog":"Weiterführende Artikel","pr":"Drucken","sh":"Teilen","cp":"Kopiert!","interp":"Was bedeutet das?"},
 "fr":   {"code":"fr","name":"Français","nav":"Outils","btn":"Calculer","faq":"Questions fréquentes","rel":"Outils connexes","more":"Plus d'outils","blog":"Articles connexes","pr":"Imprimer","sh":"Partager","cp":"Copié !","interp":"Qu'est-ce que cela signifie ?"},
 "es":   {"code":"es","name":"Español","nav":"Herramientas","btn":"Calcular","faq":"Preguntas frecuentes","rel":"Herramientas relacionadas","more":"Más herramientas","blog":"Artículos relacionados","pr":"Imprimir","sh":"Compartir","cp":"¡Copiado!","interp":"¿Qué significa esto?"},
 "pt":   {"code":"pt","name":"Português","nav":"Ferramentas","btn":"Calcular","faq":"Perguntas frequentes","rel":"Ferramentas relacionadas","more":"Mais ferramentas","blog":"Artigos relacionados","pr":"Imprimir","sh":"Compartilhar","cp":"Copiado!","interp":"O que isso significa?"},
 "ko":   {"code":"ko","name":"한국어","nav":"도구","btn":"계산하기","faq":"자주 묻는 질문","rel":"관련 계산기","more":"더 많은 도구","blog":"관련 기사","pr":"인쇄","sh":"공유","cp":"복사됨!","interp":"이것은 무엇을 의미합니까?"},
 "id":   {"code":"id","name":"Bahasa Indonesia","nav":"Alat","btn":"Hitung","faq":"Pertanyaan Umum","rel":"Kalkulator Terkait","more":"Alat Lainnya","blog":"Artikel Terkait","pr":"Cetak","sh":"Bagikan","cp":"Disalin!","interp":"Apa artinya ini?"},
 "zh-CN":{"code":"zh-CN","name":"简体中文","nav":"工具","btn":"计算","faq":"常见问题","rel":"相关工具","more":"更多工具","blog":"延伸阅读","pr":"打印","sh":"分享","cp":"已复制！","interp":"这代表什么？"},
}

CATS={
 "finance":["compound-interest","roi-calculator","risk-reward","position-size","stop-loss","dividend-yield","pe-ratio","dca-calculator","cagr","margin-calculator","stock-gain-loss","break-even","rule-of-72","dcf-calculator","intrinsic-value","bond-yield","asset-allocation","sharpe-ratio","debt-to-equity","ebitda-valuation","average-down"],
 "mortgage":["mortgage","down-payment","refinance-calc","home-affordability","rent-vs-buy","cap-rate","cash-on-cash","property-tax","stamp-duty","heloc-calculator"],
 "loan":["car-loan","student-loan","debt-consolidation","credit-card-payoff","business-loan-calc","balloon-payment","0-percent-financing","debt-to-income","personal-loan","loan-comparison"],
 "tax":["capital-gains-tax","effective-tax-rate","bonus-tax","self-employment-tax","tax-bracket","income-tax","payroll-tax","vat-calculator","sales-tax"],
 "insurance":["life-insurance-calc","car-insurance-calc","health-insurance-calc","business-insurance","disability-insurance","critical-illness-calc","coverage-gap-finder","renters-insurance","pet-insurance","dental-cost-calculator"],
 "health":["bmi-calculator","bmr-calculator","body-fat-calculator","calorie-calculator","macro-calculator","protein-intake","heart-rate-zone","blood-pressure-chart","baby-growth","bac-calculator","caffeine-calculator","hydration-calculator","sleep-calculator"],
 "trading":["fibonacci-retracement","pivot-point","rsi-calculator","macd-calculator","bollinger-bands","atr-calculator","ma-crossover","candlestick-identifier","support-resistance","pip-value","options-profit","stock-split","trading-fee"],
 "business":["burn-rate-calculator","customer-acquisition","conversion-rate","churn-rate","email-roi","dropship-margin","amazon-profit","employee-cost","business-exit-value","company-registration"],
 "retirement":["retirement","401k-contribution","coast-fire-calc","catch-up-contribution","annuity-calculator","annuity-income","pension-calculator","social-security","roth-conversion"],
 "construction":["concrete-calculator","brick-calculator","deck-calculator","drywall-calculator","asphalt-calculator","fence-calculator","flooring-calculator","gravel-calculator","paint-calculator","roofing-calculator"],
 "auto":["car-loan","car-depreciation","car-insurance-calc","car-insurance-estimate","car-lease-vs-buy","commute-cost","fuel-cost","ev-savings","gas-mileage"],
 "cooking":["cooking-converter","cooking-weight-volume","bread-hydration","coffee-ratio","calorie-density"],
 "education":["gpa-calculator","class-rank","college-savings","student-loan","scholarship-calc"],
 "utility":["electricity-cost","solar-panel","water-usage","carbon-footprint","appliance-energy","battery-calculator","air-conditioner-size"],
}

BLOGS={
 "finance":[{"s":"kd-indicator","t":"KD Indicator Guide"},{"s":"macd-indicator","t":"MACD Guide"},{"s":"stop-loss-guide","t":"Stop Loss Strategy"}],
 "trading":[{"s":"candlestick-patterns","t":"Candlestick Patterns"},{"s":"support-resistance","t":"Support & Resistance"},{"s":"moving-average-guide","t":"Moving Average Guide"}],
}

def sp(m):
    try: print(m)
    except UnicodeEncodeError: print(m.encode('utf-8',errors='replace').decode('utf-8',errors='replace'))

def get_cat(slug):
    for c,ss in CATS.items():
        if slug in ss: return c
    return "finance"

def extract_en(fp):
    with open(fp,"r",encoding="utf-8") as f: html=f.read()
    r={}
    m=re.search(r'<h1>(.*?)</h1>',html); r["h1"]=m.group(1) if m else ""
    m=re.search(r'class="calc-subtitle">(.*?)</p>',html); r["subtitle"]=m.group(1) if m else ""
    m=re.search(r'id="calcInputs">(.*?)</div>\s*<button',html,re.DOTALL); r["calc_inputs"]=m.group(1).strip() if m else ""
    m=re.search(r'id="results">(.*?)</div>\s*</div>\s*(?:<!--|\s*<div)',html,re.DOTALL)
    if not m: m=re.search(r'id="results">(.*?)</div>\s*</div>\s*</div>',html,re.DOTALL)
    r["calc_results"]=m.group(1).strip() if m else ""
    m=re.search(r'<script>\s*(function calculate[\s\S]*?)(?://\s*FAQ|//\s*Share|</script>)',html)
    if not m: m=re.search(r'<script>\s*(.*?)\s*(?://\s*FAQ|</script>)',html,re.DOTALL)
    r["calc_js"]=m.group(1).strip() if m else ""
    rel=re.findall(r'class="related-link"[^>]*href="([^"]*)"[^>]*>(.*?)</a>',html)
    r["related"]=[{"href":h,"text":t.strip()} for h,t in rel]
    m=re.search(r'<article class="article">(.*?)</article>',html,re.DOTALL); r["article"]=m.group(1).strip() if m else ""
    fq=re.findall(r'class="faq-q">(.*?)</div>\s*<div class="faq-a">(.*?)</div>',html,re.DOTALL)
    r["faqs"]=[{"q":q.strip(),"a":a.strip()} for q,a in fq]
    r["input_labels"]=re.findall(r'<label[^>]*>(.*?)</label>',r["calc_inputs"])
    r["result_labels"]=re.findall(r'class="result-label">(.*?)</span>',r["calc_results"])
    r["prefixes"]=re.findall(r'class="input-prefix">(.*?)</span>',r["calc_inputs"])
    r["suffixes"]=re.findall(r'class="input-suffix">(.*?)</span>',r["calc_inputs"])
    r["select_options"]=[o for o in re.findall(r'<option[^>]*>(.*?)</option>',r["calc_inputs"]) if o.strip()]
    r["placeholders"]=re.findall(r'placeholder="([^"]*)"',r["calc_inputs"])
    return r

def call_api(key,slug,lang,en):
    ln=LM[lang]["name"]
    cjk=lang in("zh-TW","zh-CN","ja","ko")
    wc="600+ characters" if cjk else "800+ words"
    prompt=f"""Translate this financial calculator to {ln} ({lang}).
Tool: {en['h1']}
Subtitle: {en['subtitle']}
Input labels: {json.dumps(en['input_labels'])}
Result labels: {json.dumps(en['result_labels'])}
Prefixes: {json.dumps(en['prefixes'])}
Suffixes: {json.dumps(en['suffixes'])}
Options: {json.dumps(en['select_options'])}
Placeholders: {json.dumps(en['placeholders'])}

Return ONLY valid JSON (no markdown fences):
{{
  "tool_name":"translated name",
  "subtitle":"one-line in {ln}",
  "seo_title":"under 60 chars in {ln}",
  "seo_desc":"under 155 chars in {ln}",
  "input_labels":["label1","label2",...],
  "input_helps":["short help text explaining what to enter for each field",...],
  "result_labels":["result1",...],
  "prefixes":["p1",...],
  "suffixes":["s1",...],
  "select_options":["opt1",...],
  "placeholders":["ph1",...],
  "result_interpret":"2-3 sentences explaining how to read the results, in {ln}",
  "article_html":"<h2>...</h2><p>...</p>... (4-6 sections, {wc}, ORIGINAL content in {ln} with locale currency/numbers)",
  "faqs":[{{"q":"q1","a":"a1"}},{{"q":"q2","a":"a2"}},{{"q":"q3","a":"a3"}},{{"q":"q4","a":"a4"}},{{"q":"q5","a":"a5"}}]
}}
RULES: Arrays same length as input. input_helps one per field. ONLY valid JSON."""

    hdr={"Content-Type":"application/json","x-api-key":key,"anthropic-version":"2023-06-01"}
    body={"model":MODEL,"max_tokens":MAX_TOKENS,"messages":[{"role":"user","content":prompt}]}
    for att in range(3):
        try:
            r=requests.post(API_URL,headers=hdr,json=body,timeout=120)
            if r.status_code==429: time.sleep(30*(att+1)); continue
            if r.status_code!=200: sp(f"    [ERR] {r.status_code}: {r.text[:200]}"); time.sleep(5); continue
            return parse_json(r.json()["content"][0]["text"])
        except Exception as e: sp(f"    [ERR] {e}"); time.sleep(5)
    return None

def parse_json(t):
    t=t.strip()
    t=re.sub(r'^```json\s*','',t); t=re.sub(r'\s*```$','',t); t=t.strip()
    try: return json.loads(t)
    except: pass
    s=t.find('{')
    if s<0: return None
    d=0; lv=s
    for i in range(s,len(t)):
        if t[i]=='{':d+=1
        elif t[i]=='}':
            d-=1
            if d==0: lv=i; break
    if d>0:
        tr=t[s:]; tr=re.sub(r',\s*"[^"]*":\s*("[^"]*|[\[\{].*)?$','',tr)
        ob=tr.count('[')-tr.count(']'); oc=tr.count('{')-tr.count('}')
        tr+=']'*max(0,ob)+'}'*max(0,oc)
        try: return json.loads(tr)
        except: pass
    try: return json.loads(t[s:lv+1])
    except: return None

def hreflang(slug):
    tags=[]
    for l in ALL_LANGS:
        u=f"https://softglow-ai.com/tools/{slug}.html" if l=="zh-TW" else f"https://softglow-ai.com/tools/{l}/{slug}.html"
        tags.append(f'<link rel="alternate" hreflang="{l}" href="{u}">')
    tags.append(f'<link rel="alternate" hreflang="x-default" href="https://softglow-ai.com/tools/en/{slug}.html">')
    return '\n'.join(tags)

def lang_btns(slug,cur):
    bs=[]
    for l in ALL_LANGS:
        h=f"/tools/{slug}.html" if l=="zh-TW" else f"/tools/{l}/{slug}.html"
        a=' active' if l==cur else ''
        bs.append(f'<a href="{h}" class="lang-btn{a}">{LM[l]["name"]}</a>')
    return '\n    '.join(bs)

def schema_app(name,slug,lang,desc):
    u=f"https://softglow-ai.com/tools/{slug}.html" if lang=="zh-TW" else f"https://softglow-ai.com/tools/{lang}/{slug}.html"
    return json.dumps({"@context":"https://schema.org","@type":"WebApplication","name":name,"url":u,"description":desc,"applicationCategory":"FinanceApplication","operatingSystem":"Web","offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},"inLanguage":lang},ensure_ascii=False)

def schema_faq(faqs):
    return json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":f["q"],"acceptedAnswer":{"@type":"Answer","text":f["a"]}} for f in faqs]},ensure_ascii=False)

def faq_html(faqs):
    return '\n  '.join(f'<div class="faq-item"><div class="faq-q">{f["q"]}</div><div class="faq-a">{f["a"]}</div></div>' for f in faqs)

def tr_labels(html,orig,trans):
    if not orig or not trans: return html
    for o,t in zip(orig,trans):
        if o and t and o!=t: html=html.replace(f'>{o}<',f'>{t}<',1)
    return html

def tr_ph(html,orig,trans):
    if not orig or not trans: return html
    for o,t in zip(orig,trans):
        if o and t and o!=t: html=html.replace(f'placeholder="{o}"',f'placeholder="{t}"',1)
    return html

def inject_helps(ci,helps):
    if not helps: return ci
    groups=re.split(r'(<div class="input-group">)',ci)
    result=[]; hi=0
    for i,part in enumerate(groups):
        result.append(part)
        if part=='<div class="input-group">':
            # find the next group content and append help
            if i+1<len(groups) and hi<len(helps) and helps[hi]:
                # we'll inject after the closing </div> of input-row
                next_part=groups[i+1]
                last_div=next_part.rfind('</div>')
                if last_div>=0:
                    help_tag=f'\n  <small class="input-help">{helps[hi]}</small>'
                    groups[i+1]=next_part[:last_div+6]+help_tag+next_part[last_div+6:]
                hi+=1
    return ''.join(result) if len(result)>1 else ci

def split_art(art):
    h2s=[m.start() for m in re.finditer(r'<h2',art)]
    if len(h2s)>=3:
        sp_pos=h2s[len(h2s)//2]; return art[:sp_pos],art[sp_pos:]
    mid=len(art)//2; pp=art.find('</p>',mid)
    if pp>0: return art[:pp+4],art[pp+4:]
    return art,""

def blog_cards(slug,lang):
    cat=get_cat(slug); arts=BLOGS.get(cat,BLOGS.get("finance",[]))
    cs=[]
    for a in arts[:4]:
        bl="" if lang=="zh-TW" else f"{lang}/" if lang in("en","ja","ko") else "en/"
        cs.append(f'<a class="blog-card" href="/blog/{bl}{a["s"]}.html">{a["t"]}<span>→ Blog</span></a>')
    return '\n      '.join(cs)

def more_pills(slug,lang,names):
    cat=get_cat(slug); ss=CATS.get(cat,[])
    ps=[]
    for s in ss:
        if s==slug: continue
        n=names.get(s,s.replace('-',' ').title())
        h=f"/tools/{s}.html" if lang=="zh-TW" else f"/tools/{lang}/{s}.html"
        ps.append(f'<a class="tool-pill" href="{h}">{n}</a>')
    return '\n      '.join(ps[:12])

def ad_ins(slot,fmt="auto"):
    if fmt=="fluid":
        return f'<ins class="adsbygoogle" style="display:block;text-align:center;min-height:100px;" data-ad-layout="in-article" data-ad-format="fluid" data-ad-client="{PUB}" data-ad-slot="{slot}"></ins>'
    return f'<ins class="adsbygoogle" style="display:block;min-height:250px;" data-ad-client="{PUB}" data-ad-slot="{slot}" data-ad-format="auto" data-full-width-responsive="true"></ins>'

def rel_links(en_rel,lang,names):
    ls=[]
    for r in en_rel[:5]:
        h=r["href"]
        if lang=="zh-TW": h=re.sub(r'/tools/en/','/tools/',h)
        else: h=re.sub(r'/tools/en/',f'/tools/{lang}/',h)
        sm=re.search(r'/([a-z0-9-]+)\.html',h)
        t=names.get(sm.group(1),r["text"]) if sm and sm.group(1) in names else r["text"]
        ls.append(f'<a class="related-link" href="{h}">{t}</a>')
    return '\n    '.join(ls)

def gen_page(slug,lang,en,api,tpl,names):
    lm=LM[lang]
    ci=en["calc_inputs"]
    if api.get("input_labels"): ci=tr_labels(ci,en["input_labels"],api["input_labels"])
    if api.get("prefixes"): ci=tr_labels(ci,en["prefixes"],api["prefixes"])
    if api.get("suffixes"): ci=tr_labels(ci,en["suffixes"],api["suffixes"])
    if api.get("select_options"): ci=tr_labels(ci,en["select_options"],api["select_options"])
    if api.get("placeholders"): ci=tr_ph(ci,en["placeholders"],api["placeholders"])
    if api.get("input_helps"): ci=inject_helps(ci,api["input_helps"])

    cr=en["calc_results"]
    if api.get("result_labels"): cr=tr_labels(cr,en["result_labels"],api["result_labels"])

    art=api.get("article_html",en.get("article",""))
    a1,a2=split_art(art)
    faqs=api.get("faqs",en.get("faqs",[]))
    tn=api.get("tool_name",en["h1"])
    st=api.get("seo_title",tn); sd=api.get("seo_desc",api.get("subtitle",""))
    sub=api.get("subtitle",en["subtitle"])
    interp=api.get("result_interpret","")
    canon=f"{slug}.html" if lang=="zh-TW" else f"{lang}/{slug}.html"
    lp="" if lang=="zh-TW" else f"{lang}/"

    html=tpl
    reps={
        "{{LANG_CODE}}":lm["code"],"{{SEO_TITLE}}":st,"{{SEO_DESC}}":sd,
        "{{CANONICAL_PATH}}":canon,"{{HREFLANG_TAGS}}":hreflang(slug),
        "{{SCHEMA_WEBAPP}}":schema_app(tn,slug,lang,sd),
        "{{SCHEMA_FAQ}}":schema_faq(faqs),
        "{{NAV_TOOLS}}":lm["nav"],"{{LANG_PATH}}":lp,
        "{{TOOL_NAME}}":tn,"{{TOOL_SUBTITLE}}":sub,
        "{{CALC_INPUTS}}":ci,"{{BTN_CALCULATE}}":lm["btn"],
        "{{CALC_RESULTS}}":cr,
        "{{RESULT_INTERPRET}}":f'<strong>{lm["interp"]}</strong> {interp}' if interp else "",
        "{{BTN_PRINT}}":lm["pr"],"{{BTN_SHARE}}":lm["sh"],"{{COPIED_TEXT}}":lm["cp"],
        "{{ARTICLE_FIRST_HALF}}":a1,"{{ARTICLE_SECOND_HALF}}":a2,
        "{{BLOG_SECTION_TITLE}}":lm["blog"],"{{BLOG_CARDS}}":blog_cards(slug,lang),
        "{{FAQ_TITLE}}":lm["faq"],"{{FAQ_HTML}}":faq_html(faqs),
        "{{MORE_TOOLS_TITLE}}":lm["more"],"{{MORE_TOOLS_PILLS}}":more_pills(slug,lang,names),
        "{{LANG_BUTTONS}}":lang_btns(slug,lang),
        "{{RELATED_TITLE}}":lm["rel"],"{{RELATED_LINKS}}":rel_links(en["related"],lang,names),
        "{{CALC_JS}}":en["calc_js"],
    }
    for k,v in reps.items(): html=html.replace(k,v)
    html=html.replace('<div class="ad-container ad-container-lg" id="ad-calc"></div>',f'<div class="ad-container ad-container-lg" id="ad-calc">{ad_ins(SLOT_CALC)}</div>')
    html=html.replace('<div class="ad-container" id="ad-mid"></div>',f'<div class="ad-container" id="ad-mid">{ad_ins(SLOT_ART,"fluid")}</div>')
    html=html.replace('<div class="ad-container ad-container-lg" id="ad-bottom"></div>',f'<div class="ad-container ad-container-lg" id="ad-bottom">{ad_ins(SLOT_CALC)}</div>')
    html=html.replace('<div class="ad-container ad-container-lg" id="ad-side"></div>',f'<div class="ad-container ad-container-lg" id="ad-side">{ad_ins(SLOT_SIDE)}</div>')
    html=html.replace('<div class="ad-container" id="ad-side2"></div>',f'<div class="ad-container" id="ad-side2">{ad_ins(SLOT_ART,"fluid")}</div>')
    html+=f'\n<!-- gen:v2.1|{lang}|{slug}|{time.strftime("%Y-%m-%d")} -->\n'
    return html

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--langs",default="de,fr,es,pt,ko,id,zh-CN")
    ap.add_argument("--slugs",default="")
    ap.add_argument("--rebuild-only",action="store_true",help="只用快取套新模板")
    ap.add_argument("--dry-run",action="store_true")
    a=ap.parse_args()

    key=os.environ.get("ANTHROPIC_API_KEY","")
    if not key and not a.dry_run and not a.rebuild_only:
        print("[ERROR] set ANTHROPIC_API_KEY"); sys.exit(1)

    langs=[l.strip() for l in a.langs.split(",") if l.strip()]

    tpl_p=TPL_PATH
    if not os.path.exists(tpl_p): tpl_p=os.path.join(BASE,"tool-template.html")
    if not os.path.exists(tpl_p): print(f"[ERROR] No template at {TPL_PATH}"); sys.exit(1)
    with open(tpl_p,"r",encoding="utf-8") as f: tpl=f.read()
    sp(f"[OK] Template: {tpl_p}")

    if not os.path.isdir(EN_DIR): print(f"[ERROR] {EN_DIR} not found"); sys.exit(1)
    slugs=sorted([os.path.splitext(os.path.basename(f))[0] for f in glob.glob(os.path.join(EN_DIR,"*.html")) if os.path.basename(f)!="index.html"])
    if a.slugs: tgt=[s.strip() for s in a.slugs.split(",")]; slugs=[s for s in slugs if s in tgt]

    total=len(slugs)*len(langs)
    sp(f"\n{'='*60}\nSoftGlow v2.1 | {len(slugs)} tools x {len(langs)} langs = {total} pages")
    if a.rebuild_only: sp("MODE: REBUILD-ONLY (cache→new template, no API)")
    sp(f"{'='*60}\n")

    os.makedirs(CACHE,exist_ok=True)
    for l in langs:
        d=OUT_DIR if l=="zh-TW" else os.path.join(OUT_DIR,l)
        os.makedirs(d,exist_ok=True)

    done=0;skip=0;err=0;gen=0
    for lang in langs:
        sp(f"\n--- {lang} ({LM[lang]['name']}) ---")
        names={}
        for s in slugs:
            cf=os.path.join(CACHE,f"{s}_{lang}.json")
            if os.path.exists(cf):
                try:
                    with open(cf,"r",encoding="utf-8") as f: c=json.load(f)
                    if c.get("tool_name"): names[s]=c["tool_name"]
                except: pass

        for s in slugs:
            done+=1
            cf=os.path.join(CACHE,f"{s}_{lang}.json")
            of=os.path.join(OUT_DIR,f"{s}.html") if lang=="zh-TW" else os.path.join(OUT_DIR,lang,f"{s}.html")
            ef=os.path.join(EN_DIR,f"{s}.html")
            if not os.path.exists(ef): skip+=1; continue
            if a.rebuild_only and not os.path.exists(cf): skip+=1; continue
            if not a.rebuild_only and os.path.exists(cf) and os.path.exists(of): skip+=1; continue

            try: en=extract_en(ef)
            except Exception as e: sp(f"  [{done}/{total}] [ERR] {s}: {e}"); err+=1; continue

            api=None
            if os.path.exists(cf):
                try:
                    with open(cf,"r",encoding="utf-8") as f: api=json.load(f)
                except: pass

            if api is None:
                if a.rebuild_only: skip+=1; continue
                sp(f"  [{done}/{total}] {s} ({lang}) API...")
                api=call_api(key,s,lang,en)
                if api is None: err+=1; continue
                try:
                    with open(cf,"w",encoding="utf-8") as f: json.dump(api,f,ensure_ascii=False,indent=2)
                except: pass
                time.sleep(0.5)

            if api.get("tool_name"): names[s]=api["tool_name"]

            try:
                html=gen_page(s,lang,en,api,tpl,names)
                with open(of,"w",encoding="utf-8") as f: f.write(html)
                gen+=1
                sp(f"  [{done}/{total}] [OK] {s}")
            except Exception as e: sp(f"  [{done}/{total}] [ERR] {s}: {e}"); traceback.print_exc(); err+=1

        sp(f"  {lang}: {len(names)} names cached")

    sp(f"\n{'='*60}\nDone! Total:{total} Gen:{gen} Skip:{skip} Err:{err}")
    sp(f"\nNext:\n  1. xcopy /E /Y output\\tools\\* frontend\\tools\\\n  2. Upload Zeabur\n{'='*60}")

if __name__=="__main__": main()
