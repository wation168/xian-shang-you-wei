# -*- coding: utf-8 -*-
"""
enrich_lottery_pages.py
One-time post-processing: inject FAQ, Schema, How-to-Play, tax info,
fix sidebar bug, add lottery-live.js include to all lottery HTML pages.

Usage:
  cd D:\\xian-shang-you-wei
  python enrich_lottery_pages.py
"""
import os, re, json, html as html_mod

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend", "frontend", "lottery")

# ============================================================
# LOTTERY CONFIG (matches generate_lottery_final.py)
# ============================================================
LOTTERIES = {
    "powerball": {"name":"Powerball","country":"USA","pick":5,"range":69,"bonus":1,"brange":26,"days":"Mon/Wed/Sat","time":"22:59 ET","odds":"1:292,201,338","bet":"$2","currency":"USD","tax":"37% federal + state tax","claim":"Winners have 180 days to 1 year depending on state. Jackpots can be taken as annuity (30 years) or lump sum (approx. 60% of advertised amount)."},
    "mega-millions": {"name":"Mega Millions","country":"USA","pick":5,"range":70,"bonus":1,"brange":24,"days":"Tue/Fri","time":"23:00 ET","odds":"1:302,575,350","bet":"$2","currency":"USD","tax":"37% federal + state tax","claim":"Winners have 180 days to 1 year depending on state. Lump sum is approximately 60% of the advertised jackpot."},
    "euromillions": {"name":"EuroMillions","country":"Europe","pick":5,"range":50,"bonus":2,"brange":12,"days":"Tue/Fri","time":"21:00 CET","odds":"1:139,838,160","bet":"\u20ac2.50","currency":"EUR","tax":"Varies by country. UK, France, Germany: tax-free. Spain: 20% over \u20ac40,000.","claim":"Winners typically have 90 days to 1 year depending on the participating country."},
    "lotto-max": {"name":"Lotto Max","country":"Canada","pick":7,"range":50,"bonus":0,"brange":0,"days":"Tue/Fri","time":"22:30 ET","odds":"1:33,294,800","bet":"$5 CAD","currency":"CAD","tax":"Tax-free in Canada.","claim":"Winners have 1 year from the draw date to claim prizes."},
    "uk-lotto": {"name":"UK Lotto","country":"UK","pick":6,"range":59,"bonus":0,"brange":0,"days":"Wed/Sat","time":"20:00 GMT","odds":"1:45,057,474","bet":"\u00a32","currency":"GBP","tax":"Tax-free in the UK.","claim":"Winners have 180 days from the draw date to claim."},
    "el-gordo": {"name":"El Gordo","country":"Spain","pick":5,"range":54,"bonus":0,"brange":0,"days":"Sun","time":"21:30 CET","odds":"1:31,625,100","bet":"\u20ac1.50","currency":"EUR","tax":"20% on amounts over \u20ac40,000.","claim":"Winners have 3 months from the draw date."},
    "superenalotto": {"name":"SuperEnalotto","country":"Italy","pick":6,"range":90,"bonus":1,"brange":90,"days":"Tue/Thu/Fri/Sat","time":"20:00 CET","odds":"1:622,614,630","bet":"\u20ac1","currency":"EUR","tax":"20% on amounts over \u20ac500.","claim":"Winners have 90 days from the draw date."},
    "lotto-6aus49": {"name":"Lotto 6aus49","country":"Germany","pick":6,"range":49,"bonus":1,"brange":9,"days":"Wed/Sat","time":"18:25 CET","odds":"1:139,838,160","bet":"\u20ac1.20","currency":"EUR","tax":"Tax-free in Germany.","claim":"Winners have 13 weeks from the draw date."},
    "oz-lotto": {"name":"Oz Lotto","country":"Australia","pick":7,"range":47,"bonus":2,"brange":47,"days":"Tue","time":"20:30 AEST","odds":"1:45,379,620","bet":"A$1.50","currency":"AUD","tax":"Tax-free in Australia.","claim":"Winners typically have 6 years to claim (varies by state)."},
    "taiwan-bingo": {"name_zh":"\u5a01\u529b\u5f69","name":"Power Lottery","country":"Taiwan","pick":6,"range":38,"bonus":1,"brange":8,"days":"Mon/Thu","time":"20:30 CST","odds":"1:22,085,448","bet":"NT$100","currency":"TWD","tax":"10% (NT$5,001-20M), 20% (over NT$20M)","claim":"Winners have 3 months from the draw date. Prizes are paid in full (no lump sum discount)."},
    "taiwan-lotto": {"name_zh":"\u5927\u6a02\u900f","name":"Super Lotto","country":"Taiwan","pick":6,"range":49,"bonus":1,"brange":49,"days":"Tue/Fri","time":"20:30 CST","currency":"TWD","bet":"NT$50","odds":"1:13,983,816","tax":"10% (NT$5,001-20M), 20% (over NT$20M)","claim":"Winners have 3 months. Jackpot rolls over if unclaimed."},
    "daily-cash": {"name_zh":"\u4eca\u5f69539","name":"Daily Cash 539","country":"Taiwan","pick":5,"range":39,"bonus":0,"brange":0,"days":"Mon-Sat","time":"20:30 CST","currency":"TWD","bet":"NT$50","odds":"1:575,757","tax":"10% (NT$5,001-20M), 20% (over NT$20M)","claim":"Fixed first prize of NT$8 million. Winners have 3 months."},
    "mega-sena": {"name":"Mega-Sena","country":"Brazil","pick":6,"range":60,"bonus":0,"brange":0,"days":"Tue/Thu/Sat","time":"20:00 BRT","currency":"BRL","bet":"R$5","odds":"1:50,063,860","tax":"30% on amounts over R$1,903.98.","claim":"Winners have 90 days from the draw date."},
    "korea-lotto": {"name_ko":"\ub85c\ub610 6/45","name":"Korea Lotto 6/45","country":"Korea","pick":6,"range":45,"bonus":1,"brange":45,"days":"Sat","time":"20:45 KST","currency":"KRW","bet":"\u20a91,000","odds":"1:8,145,060","tax":"22% on amounts over \u20a950 million.","claim":"Winners have 1 year from the draw date."},
    "japan-loto6": {"name_ja":"\u30ed\u30c86","name":"Japan Loto 6","country":"Japan","pick":6,"range":43,"bonus":1,"brange":43,"days":"Mon/Thu","time":"18:45 JST","currency":"JPY","bet":"\u00a5200","odds":"1:6,096,454","tax":"20.315% on all winnings (income tax + special reconstruction tax).","claim":"Winners have 1 year from the draw date."},
}

# ============================================================
# FAQ TEMPLATES (per language)
# ============================================================
def gen_faq(slug, lang):
    c = LOTTERIES[slug]
    n = c.get(f"name_{lang[:2]}", c["name"])
    
    if lang.startswith("zh"):
        qs = [
            (f"{n}\u600e\u9ebc\u73a9\uff1f",
             f"\u5f9e 1 \u5230 {c['range']} \u4e2d\u9078\u51fa {c['pick']} \u500b\u865f\u78bc" + 
             (f"\uff0c\u518d\u5f9e 1 \u5230 {c['brange']} \u4e2d\u9078 {c['bonus']} \u500b\u7279\u5225\u865f" if c['bonus']>0 else "") +
             f"\u3002\u6bcf\u6ce8 {c['bet']}\uff0c\u6bcf\u9031 {c['days']} \u65bc {c['time']} \u958b\u734e\u3002"),
            (f"{n}\u7684\u4e2d\u734e\u6a5f\u7387\u662f\u591a\u5c11\uff1f",
             f"\u982d\u734e\u6a5f\u7387\u70ba {c['odds']}\u3002\u96d6\u7136\u6a5f\u7387\u4e0d\u9ad8\uff0c\u4f46\u63a1\u7528\u7d2f\u7a4d\u578b\u734e\u91d1\u6a5f\u5236\uff0c\u7576\u671f\u7121\u4eba\u4e2d\u734e\u6642\u734e\u91d1\u6703\u6efe\u5165\u4e0b\u4e00\u671f\u3002"),
            (f"{n}\u4e2d\u734e\u5f8c\u8981\u7e73\u7a05\u55ce\uff1f",
             c["tax"]),
            (f"{n}\u4e2d\u734e\u5f8c\u600e\u9ebc\u9818\u734e\uff1f",
             c["claim"]),
            (f"\u5728\u54ea\u88e1\u53ef\u4ee5\u67e5\u770b{n}\u7684\u958b\u734e\u7d50\u679c\uff1f",
             f"\u672c\u9801\u63d0\u4f9b{n}\u6700\u65b0\u958b\u734e\u865f\u78bc\u3001\u6b77\u53f2\u7d00\u9304\u3001\u7d71\u8a08\u5206\u6790\u548c\u514d\u8cbb\u9078\u865f\u5de5\u5177\u3002\u958b\u734e\u7d50\u679c\u6bcf\u65e5\u81ea\u52d5\u66f4\u65b0\u3002"),
        ]
    elif lang == "ja":
        qs = [
            (f"{n}\u306e\u904a\u3073\u65b9\u306f\uff1f",
             f"1\u304b\u3089{c['range']}\u306e\u4e2d\u304b\u3089{c['pick']}\u3064\u306e\u756a\u53f7\u3092\u9078\u3073\u307e\u3059" +
             (f"\u3002\u3055\u3089\u306b1\u304b\u3089{c['brange']}\u306e\u4e2d\u304b\u3089{c['bonus']}\u3064\u306e\u30dc\u30fc\u30ca\u30b9\u756a\u53f7\u3092\u9078\u3073\u307e\u3059" if c['bonus']>0 else "") +
             f"\u3002{c['days']}\u306b\u62bd\u9078\u304c\u884c\u308f\u308c\u307e\u3059\u3002"),
            (f"{n}\u306e\u5f53\u9078\u78ba\u7387\u306f\uff1f", f"\u30b8\u30e3\u30c3\u30af\u30dd\u30c3\u30c8\u306e\u78ba\u7387\u306f {c['odds']} \u3067\u3059\u3002\u30ad\u30e3\u30ea\u30fc\u30aa\u30fc\u30d0\u30fc\u5236\u5ea6\u306b\u3088\u308a\u3001\u8cde\u91d1\u304c\u7d2f\u7a4d\u3055\u308c\u308b\u3053\u3068\u304c\u3042\u308a\u307e\u3059\u3002"),
            (f"{n}\u306e\u8cde\u91d1\u306b\u7a0e\u91d1\u306f\u304b\u304b\u308a\u307e\u3059\u304b\uff1f", c["tax"]),
            (f"\u8cde\u91d1\u306e\u53d7\u3051\u53d6\u308a\u65b9\u306f\uff1f", c["claim"]),
            (f"{n}\u306e\u7d50\u679c\u306f\u3069\u3053\u3067\u78ba\u8a8d\u3067\u304d\u307e\u3059\u304b\uff1f", f"\u3053\u306e\u30da\u30fc\u30b8\u3067\u6700\u65b0\u306e\u5f53\u9078\u756a\u53f7\u3001\u904e\u53bb\u306e\u7d50\u679c\u3001\u7d71\u8a08\u5206\u6790\u3001\u7121\u6599\u306e\u30ca\u30f3\u30d0\u30fc\u30b8\u30a7\u30cd\u30ec\u30fc\u30bf\u30fc\u3092\u63d0\u4f9b\u3057\u3066\u3044\u307e\u3059\u3002"),
        ]
    elif lang == "ko":
        qs = [
            (f"{n} \ud50c\ub808\uc774 \ubc29\ubc95\uc740?", f"1\ubd80\ud130 {c['range']}\uae4c\uc9c0 {c['pick']}\uac1c\uc758 \ubc88\ud638\ub97c \uc120\ud0dd\ud569\ub2c8\ub2e4" + (f". \uadf8\ub9ac\uace0 1\ubd80\ud130 {c['brange']}\uae4c\uc9c0 {c['bonus']}\uac1c\uc758 \ubcf4\ub108\uc2a4 \ubc88\ud638\ub97c \uc120\ud0dd\ud569\ub2c8\ub2e4" if c['bonus']>0 else "") + f". \ucd94\ucca8\uc77c: {c['days']}."),
            (f"{n} \ub2f9\ucca8 \ud655\ub960\uc740?", f"\uc7ad\ud31f \ud655\ub960\uc740 {c['odds']}\uc785\ub2c8\ub2e4."),
            (f"{n} \ub2f9\ucca8\uae08\uc5d0 \uc138\uae08\uc774 \ubd80\uacfc\ub418\ub098\uc694?", c["tax"]),
            (f"\ub2f9\ucca8\uae08 \uc218\ub839 \ubc29\ubc95\uc740?", c["claim"]),
            (f"{n} \uacb0\uacfc\ub97c \uc5b4\ub514\uc11c \ud655\uc778\ud560 \uc218 \uc788\ub098\uc694?", f"\uc774 \ud398\uc774\uc9c0\uc5d0\uc11c \ucd5c\uc2e0 \ub2f9\ucca8 \ubc88\ud638, \uacfc\uac70 \uacb0\uacfc, \ud1b5\uacc4 \ubd84\uc11d \ubc0f \ubb34\ub8cc \ubc88\ud638 \uc0dd\uc131\uae30\ub97c \uc81c\uacf5\ud569\ub2c8\ub2e4."),
        ]
    elif lang == "de":
        qs = [
            (f"Wie spielt man {n}?", f"W\u00e4hlen Sie {c['pick']} Zahlen von 1 bis {c['range']}" + (f" und {c['bonus']} Bonuszahl(en) von 1 bis {c['brange']}" if c['bonus']>0 else "") + f". Ziehungen: {c['days']} um {c['time']}. Einsatz: {c['bet']}."),
            (f"Wie hoch sind die Gewinnchancen bei {n}?", f"Die Jackpot-Chance betr\u00e4gt {c['odds']}. Nicht gewonnene Jackpots werden auf die n\u00e4chste Ziehung \u00fcbertragen."),
            (f"Muss man {n}-Gewinne versteuern?", c["tax"]),
            (f"Wie kann man {n}-Gewinne einl\u00f6sen?", c["claim"]),
            (f"Wo kann man {n}-Ergebnisse pr\u00fcfen?", f"Auf dieser Seite finden Sie die neuesten Ziehungsergebnisse, historische Daten, Statistiken und kostenlose Zahlengeneratoren."),
        ]
    elif lang == "fr":
        qs = [
            (f"Comment jouer au {n} ?", f"Choisissez {c['pick']} num\u00e9ros de 1 \u00e0 {c['range']}" + (f" et {c['bonus']} num\u00e9ro(s) bonus de 1 \u00e0 {c['brange']}" if c['bonus']>0 else "") + f". Tirages : {c['days']} \u00e0 {c['time']}. Mise : {c['bet']}."),
            (f"Quelles sont les chances de gagner au {n} ?", f"Les chances du jackpot sont de {c['odds']}. Les jackpots non r\u00e9clam\u00e9s sont report\u00e9s au tirage suivant."),
            (f"Les gains du {n} sont-ils impos\u00e9s ?", c["tax"]),
            (f"Comment r\u00e9clamer un gain au {n} ?", c["claim"]),
            (f"O\u00f9 v\u00e9rifier les r\u00e9sultats du {n} ?", f"Cette page fournit les derniers r\u00e9sultats, l'historique, les statistiques et des g\u00e9n\u00e9rateurs de num\u00e9ros gratuits."),
        ]
    elif lang == "es":
        qs = [
            (f"\u00bfC\u00f3mo se juega al {n}?", f"Elija {c['pick']} n\u00fameros del 1 al {c['range']}" + (f" y {c['bonus']} n\u00famero(s) extra del 1 al {c['brange']}" if c['bonus']>0 else "") + f". Sorteos: {c['days']} a las {c['time']}. Apuesta: {c['bet']}."),
            (f"\u00bfCu\u00e1les son las probabilidades de ganar en {n}?", f"Las probabilidades del premio mayor son {c['odds']}. Los premios no reclamados se acumulan."),
            (f"\u00bfSe pagan impuestos por los premios de {n}?", c["tax"]),
            (f"\u00bfC\u00f3mo cobrar un premio de {n}?", c["claim"]),
            (f"\u00bfD\u00f3nde ver los resultados de {n}?", f"Esta p\u00e1gina ofrece los \u00faltimos resultados, historial, estad\u00edsticas y generadores de n\u00fameros gratuitos."),
        ]
    elif lang == "pt":
        qs = [
            (f"Como jogar no {n}?", f"Escolha {c['pick']} n\u00fameros de 1 a {c['range']}" + (f" e {c['bonus']} n\u00famero(s) b\u00f4nus de 1 a {c['brange']}" if c['bonus']>0 else "") + f". Sorteios: {c['days']} \u00e0s {c['time']}. Aposta: {c['bet']}."),
            (f"Quais as chances de ganhar no {n}?", f"As chances do pr\u00eamio principal s\u00e3o de {c['odds']}. Pr\u00eamios n\u00e3o reclamados acumulam para o pr\u00f3ximo sorteio."),
            (f"Os pr\u00eamios do {n} s\u00e3o tributados?", c["tax"]),
            (f"Como resgatar um pr\u00eamio do {n}?", c["claim"]),
            (f"Onde verificar os resultados do {n}?", f"Esta p\u00e1gina oferece os \u00faltimos resultados, hist\u00f3rico, estat\u00edsticas e geradores de n\u00fameros gratuitos."),
        ]
    elif lang == "id":
        qs = [
            (f"Bagaimana cara bermain {n}?", f"Pilih {c['pick']} nomor dari 1 hingga {c['range']}" + (f" dan {c['bonus']} nomor bonus dari 1 hingga {c['brange']}" if c['bonus']>0 else "") + f". Undian: {c['days']} pukul {c['time']}. Taruhan: {c['bet']}."),
            (f"Berapa peluang menang di {n}?", f"Peluang jackpot adalah {c['odds']}. Jackpot yang tidak diklaim akan diakumulasi ke undian berikutnya."),
            (f"Apakah hadiah {n} dikenakan pajak?", c["tax"]),
            (f"Bagaimana cara mengklaim hadiah {n}?", c["claim"]),
            (f"Di mana melihat hasil {n}?", f"Halaman ini menyediakan hasil terbaru, riwayat, statistik, dan generator nomor gratis."),
        ]
    else:  # en default
        qs = [
            (f"How do I play {n}?",
             f"Pick {c['pick']} numbers from 1 to {c['range']}" +
             (f", plus {c['bonus']} bonus number(s) from 1 to {c['brange']}" if c['bonus']>0 else "") +
             f". Draws are held on {c['days']} at {c['time']}. Each entry costs {c['bet']}."),
            (f"What are the odds of winning the {n} jackpot?",
             f"The jackpot odds are {c['odds']}. If no one wins, the prize rolls over to the next draw, often creating massive jackpots."),
            (f"Are {n} winnings taxed?", c["tax"]),
            (f"How do I claim a {n} prize?", c["claim"]),
            (f"Where can I check {n} results?",
             f"This page provides the latest winning numbers, complete draw history, statistical analysis, and free number generator tools. Results are updated daily."),
        ]
    return qs


def faq_html(slug, lang):
    """Generate FAQ HTML + Schema JSON-LD"""
    qs = gen_faq(slug, lang)
    title = "FAQ" if lang == "en" else {"zh-TW":"\u5e38\u898b\u554f\u984c","zh-CN":"\u5e38\u89c1\u95ee\u9898","ja":"\u3088\u304f\u3042\u308b\u8cea\u554f","ko":"\uc790\uc8fc \ubb3b\ub294 \uc9c8\ubb38","de":"H\u00e4ufig gestellte Fragen","fr":"Questions fr\u00e9quentes","es":"Preguntas frecuentes","pt":"Perguntas frequentes","id":"Pertanyaan Umum"}.get(lang, "FAQ")
    
    items_html = ""
    schema_items = []
    for q, a in qs:
        items_html += f'<div class="faq-item"><div class="faq-q">{html_mod.escape(q)}</div><div class="faq-a">{html_mod.escape(a)}</div></div>\n'
        schema_items.append({"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}})
    
    schema = json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":schema_items}, ensure_ascii=False)
    
    return f'''
  <div class="card" style="margin-top:20px">
    <h2>\u2753 {title}</h2>
    {items_html}
  </div>
  <script type="application/ld+json">{schema}</script>
'''


def how_to_play_html(slug, lang):
    """Generate How-to-Play + Tax section"""
    c = LOTTERIES[slug]
    n = c.get(f"name_{lang[:2]}", c["name"])
    
    if lang.startswith("zh"):
        title_how = f"\u600e\u9ebc\u73a9{n}"
        title_tax = "\u7a05\u52d9\u8207\u9818\u734e\u8cc7\u8a0a"
        steps = [
            f"\u5f9e 1 \u5230 {c['range']} \u4e2d\u9078\u64c7 {c['pick']} \u500b\u865f\u78bc" + (f"\uff0c\u518d\u5f9e 1 \u5230 {c['brange']} \u4e2d\u9078 {c['bonus']} \u500b\u7279\u5225\u865f" if c['bonus']>0 else ""),
            f"\u6bcf\u6ce8\u6295\u6ce8\u91d1\u984d\u70ba {c['bet']}",
            f"\u958b\u734e\u6642\u9593\uff1a\u6bcf\u9031 {c['days']} {c['time']}",
            f"\u982d\u734e\u6a5f\u7387\uff1a{c['odds']}\uff0c\u7576\u671f\u7121\u4eba\u4e2d\u734e\u5247\u734e\u91d1\u6efe\u5165\u4e0b\u4e00\u671f",
        ]
        tax_text = f"<p><strong>\u7a05\u7387\uff1a</strong>{c['tax']}</p><p><strong>\u9818\u734e\uff1a</strong>{c['claim']}</p>"
    elif lang == "ja":
        title_how = f"{n}\u306e\u904a\u3073\u65b9"
        title_tax = "\u7a0e\u91d1\u3068\u8cde\u91d1\u53d7\u53d6"
        steps = [f"1\u304b\u3089{c['range']}\u306e\u4e2d\u304b\u3089{c['pick']}\u3064\u9078\u3076" + (f"\u3001\u30dc\u30fc\u30ca\u30b9{c['bonus']}\u3064\u3092{c['brange']}\u304b\u3089\u9078\u3076" if c['bonus']>0 else ""), f"\u4e00\u53e3{c['bet']}", f"\u62bd\u9078\u65e5: {c['days']} {c['time']}", f"\u30b8\u30e3\u30c3\u30af\u30dd\u30c3\u30c8\u78ba\u7387: {c['odds']}"]
        tax_text = f"<p><strong>\u7a0e\u91d1:</strong> {c['tax']}</p><p><strong>\u53d7\u53d6:</strong> {c['claim']}</p>"
    else:
        title_how = f"How to Play {n}"
        title_tax = "Tax & Prize Claim"
        steps = [
            f"Pick {c['pick']} numbers from 1 to {c['range']}" + (f", plus {c['bonus']} bonus from 1 to {c['brange']}" if c['bonus']>0 else ""),
            f"Each entry costs {c['bet']}",
            f"Draws are held on {c['days']} at {c['time']}",
            f"Jackpot odds: {c['odds']}. Unclaimed jackpots roll over to the next draw.",
        ]
        tax_text = f"<p><strong>Tax:</strong> {c['tax']}</p><p><strong>Claiming:</strong> {c['claim']}</p>"
    
    steps_html = "".join(f'<div style="display:flex;gap:12px;align-items:flex-start;margin-bottom:12px"><div style="min-width:28px;height:28px;background:#D97706;color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px">{i+1}</div><div style="font-size:14px;color:#4A5568;padding-top:4px">{s}</div></div>' for i,s in enumerate(steps))
    
    return f'''
  <div class="card" style="margin-top:20px">
    <h2>\ud83d\udcd6 {title_how}</h2>
    <div style="margin-top:16px">{steps_html}</div>
  </div>
  <div class="card" style="margin-top:20px">
    <h2>\ud83d\udcb0 {title_tax}</h2>
    {tax_text}
  </div>
'''


# ============================================================
# MAIN ENRICHMENT LOGIC
# ============================================================
def detect_slug_from_file(filepath):
    """Extract lottery slug from filename"""
    fname = os.path.basename(filepath)
    # Remove -results, -history, -statistics suffix
    slug = fname.replace(".html", "")
    for suffix in ["-results", "-history", "-statistics"]:
        slug = slug.replace(suffix, "")
    return slug


def detect_lang_from_path(filepath):
    """Detect language from path"""
    parts = filepath.replace("\\", "/").split("/")
    # Check for language subfolder
    for p in parts:
        if p in ["en","ja","ko","fr","de","es","pt","id","zh-CN"]:
            return p
    return "zh-TW"  # root = zh-TW


def detect_page_type(filepath):
    fname = os.path.basename(filepath)
    if "-results" in fname: return "results"
    if "-history" in fname: return "history"
    if "-statistics" in fname: return "statistics"
    return "intro"


def is_lottery_page(filepath):
    """Check if file is a lottery-specific page (not tool, index, or number-generator)"""
    fname = os.path.basename(filepath)
    if fname in ["index.html", "number-generator.html"]:
        return False
    tool_slugs = ["ai-pick","bazi-pick","birthday-pick","chinese-zodiac-pick","cold-pick",
        "divination-pick","dream-pick","hot-pick","life-event-pick","lucky-number",
        "random-pick","zodiac-pick"]
    slug = fname.replace(".html","").replace("-results","").replace("-history","").replace("-statistics","")
    if slug in tool_slugs:
        return False
    return slug in LOTTERIES


def enrich_file(filepath):
    """Enrich a single lottery HTML file"""
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()
    
    slug = detect_slug_from_file(filepath)
    lang = detect_lang_from_path(filepath)
    ptype = detect_page_type(filepath)
    
    if slug not in LOTTERIES:
        return False
    
    modified = False
    
    # 1. Fix sidebar truncation bug: find incomplete <a hr tags
    if '<a hr' in html and 'class="sidebar"' in html:
        # Fix truncated sidebar links
        html = re.sub(r'<a hr(?=[^e])', '<a href="#"', html)
        modified = True
    
    # 2. Add lottery-live.js before </body> if not already present
    if 'lottery-live.js' not in html:
        html = html.replace('</body>', '<script src="/js/lottery-live.js" defer></script>\n</body>')
        modified = True
    
    # 3. Add FAQ + How-to-Play for intro pages only
    if ptype == "intro" and 'faq-item' not in html:
        faq = faq_html(slug, lang)
        howto = how_to_play_html(slug, lang)
        
        # Insert before lang-bar
        if '<div class="lang-bar">' in html:
            html = html.replace('<div class="lang-bar">', 
                howto + faq + '\n  <div class="lang-bar">')
            modified = True
    
    # 4. Add FAQ for results pages
    if ptype == "results" and 'faq-item' not in html:
        faq = faq_html(slug, lang)
        if '<div class="lang-bar">' in html:
            html = html.replace('<div class="lang-bar">', faq + '\n  <div class="lang-bar">')
            modified = True
    
    # 5. Add FAQ toggle JS if FAQ was added
    if 'faq-item' in html and 'faq-q' in html and "classList.toggle('open')" not in html:
        js_toggle = """
<script>document.querySelectorAll('.faq-q').forEach(function(q){q.addEventListener('click',function(){this.parentElement.classList.toggle('open')})})</script>"""
        html = html.replace('</body>', js_toggle + '\n</body>')
        modified = True
    
    # 6. Add FAQ CSS if not present
    if 'faq-item' in html and '.faq-item' not in html:
        faq_css = """.faq-item{border-bottom:1px solid #E2E8F0;padding:16px 0}
.faq-q{font-size:15px;font-weight:600;color:#2D3748;cursor:pointer;display:flex;justify-content:space-between;align-items:center}
.faq-q::after{content:"+";font-size:18px;color:#A0AEC0;transition:transform 0.2s}
.faq-item.open .faq-q::after{content:"-"}
.faq-a{font-size:14px;color:#718096;line-height:1.7;max-height:0;overflow:hidden;transition:max-height 0.3s,padding 0.3s}
.faq-item.open .faq-a{max-height:500px;padding-top:10px}"""
        html = html.replace('</style>', faq_css + '\n</style>')
        modified = True
    
    # 7. Add cookie consent if missing
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


def main():
    print("=" * 60)
    print("Enriching lottery pages: FAQ + Schema + How-to + JS + fixes")
    print("=" * 60)
    
    if not os.path.isdir(BASE):
        print(f"Error: {BASE} not found")
        return
    
    enriched = 0
    skipped = 0
    total = 0
    
    for root, dirs, files in os.walk(BASE):
        for fname in files:
            if not fname.endswith(".html"):
                continue
            filepath = os.path.join(root, fname)
            
            if not is_lottery_page(filepath):
                continue
            
            total += 1
            if enrich_file(filepath):
                enriched += 1
                slug = detect_slug_from_file(filepath)
                lang = detect_lang_from_path(filepath)
                ptype = detect_page_type(filepath)
                print(f"  \u2705 {lang}/{slug}-{ptype}")
            else:
                skipped += 1
    
    print(f"\nTotal: {total} lottery pages")
    print(f"  Enriched: {enriched}")
    print(f"  Skipped: {skipped} (already enriched or no changes needed)")
    print(f"\nRemember to also copy lottery-live.js:")
    print(f"  copy D:\\downloads\\lottery-live.js D:\\xian-shang-you-wei\\backend\\frontend\\js\\lottery-live.js")


if __name__ == "__main__":
    main()
