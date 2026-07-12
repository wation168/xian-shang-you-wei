# -*- coding: utf-8 -*-
"""
fix_tools.py — 線上有位 Tools 頁面一次修正腳本（v2，含全部 35 個工具字典）
修正：結果標籤翻譯、副標題/meta 翻譯、金額/百分比單位、RSI 訊號本地化、
      視覺化（複利/RSI/損益平衡）、手機體驗。不呼叫 API、可重複執行。
用法：  python fix_tools.py output\\tools
"""
import os, re, json, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "output/tools"
LANGS = ["zh","en","ja","ko","es","pt","id","vi","th","de"]
GUARD = "<!--uifix-v1-->"
MONEY = {"zh":"元","en":"$","ja":"円","ko":"₩","es":"€","pt":"R$","id":"Rp","vi":"₫","th":"฿","de":"€"}

def L(zh,en,ja,ko,es,pt,id_,vi,th,de):
    return {"zh":zh,"en":en,"ja":ja,"ko":ko,"es":es,"pt":pt,"id":id_,"vi":vi,"th":th,"de":de}

LABELS = {
 "interest":      L("賺得利息","Interest Earned","受取利息","이자 수익","Intereses ganados","Juros ganhos","Bunga diperoleh","Lãi nhận được","ดอกเบี้ยที่ได้รับ","Verdiente Zinsen"),
 "totalDeposit":  L("總投入本金","Total Deposited","投資元本合計","총 투자 원금","Total depositado","Total depositado","Total disetor","Tổng tiền gốc","เงินต้นรวม","Gesamteinzahlung"),
 "rs":            L("RS 相對強度","RS (Relative Strength)","RS（相対力）","RS (상대강도)","RS (fuerza relativa)","RS (força relativa)","RS (kekuatan relatif)","RS (sức mạnh tương đối)","RS (ความแข็งแกร่งสัมพัทธ์)","RS (relative Stärke)"),
 "signal":        L("訊號","Signal","シグナル","신호","Señal","Sinal","Sinyal","Tín hiệu","สัญญาณ","Signal"),
 "beRevenue":     L("損益平衡營收","Break-Even Revenue","損益分岐点売上高","손익분기 매출","Ingresos de equilibrio","Receita de equilíbrio","Pendapatan impas","Doanh thu hòa vốn","รายได้จุดคุ้มทุน","Break-even-Umsatz"),
 "margin":        L("每單位邊際貢獻","Contribution Margin / Unit","単位あたり限界利益","단위당 공헌이익","Margen por unidad","Margem por unidade","Margin per unit","Lợi nhuận góp/đơn vị","กำไรส่วนเกินต่อหน่วย","Deckungsbeitrag/Einheit"),
 "stocks":        L("股票配置","Stocks","株式","주식","Acciones","Ações","Saham","Cổ phiếu","หุ้น","Aktien"),
 "bonds":         L("債券配置","Bonds","債券","채권","Bonos","Títulos","Obligasi","Trái phiếu","พันธบัตร","Anleihen"),
 "atrPct":        L("ATR 百分比","ATR %","ATR（%）","ATR(%)","ATR %","ATR %","ATR %","ATR %","ATR %","ATR %"),
 "totalShares":   L("總股數","Total Shares","合計株数","총 주식 수","Acciones totales","Total de ações","Total saham","Tổng số cổ phiếu","จำนวนหุ้นรวม","Aktien gesamt"),
 "totalCost":     L("總成本","Total Cost","総コスト","총비용","Costo total","Custo total","Total biaya","Tổng chi phí","ต้นทุนรวม","Gesamtkosten"),
 "bandwidth":     L("通道寬度","Bandwidth","バンド幅","밴드폭","Ancho de banda","Largura da banda","Lebar pita","Độ rộng dải","ความกว้างแบนด์","Bandbreite"),
 "middle":        L("中軌","Middle Band","ミドルバンド","중간 밴드","Banda media","Banda média","Pita tengah","Dải giữa","เส้นกลาง","Mittleres Band"),
 "totalReturn":   L("總報酬率","Total Return","トータルリターン","총 수익률","Rendimiento total","Retorno total","Total imbal hasil","Tổng lợi nhuận","ผลตอบแทนรวม","Gesamtrendite"),
 "profit":        L("獲利金額","Profit","利益","수익","Beneficio","Lucro","Keuntungan","Lợi nhuận","กำไร","Gewinn"),
 "bodySize":      L("K棒實體大小","Body Size","実体の大きさ","몸통 크기","Tamaño del cuerpo","Tamanho do corpo","Ukuran badan","Kích thước thân nến","ขนาดตัวเทียน","Körpergröße"),
 "range":         L("K棒全距","Range","レンジ","범위","Rango","Amplitude","Rentang","Biên độ","ช่วงราคา","Spanne"),
 "usdValue":      L("換算結果","Converted Amount","換算後の金額","환산 금액","Importe convertido","Valor convertido","Jumlah hasil konversi","Số tiền quy đổi","จำนวนที่แปลงแล้ว","Umgerechneter Betrag"),
 "exchangeRate":  L("匯率","Exchange Rate","為替レート","환율","Tipo de cambio","Taxa de câmbio","Nilai tukar","Tỷ giá","อัตราแลกเปลี่ยน","Wechselkurs"),
 "pvCashFlows":   L("現金流現值","PV of Cash Flows","キャッシュフロー現在価値","현금흐름 현재가치","VP de flujos de caja","VP dos fluxos de caixa","Nilai kini arus kas","Giá trị hiện tại dòng tiền","มูลค่าปัจจุบันกระแสเงินสด","Barwert der Cashflows"),
 "pvTerminal":    L("終值現值","PV of Terminal Value","ターミナルバリュー現在価値","잔존가치 현재가치","VP del valor terminal","VP do valor terminal","Nilai kini nilai terminal","Giá trị hiện tại giá trị cuối","มูลค่าปัจจุบันมูลค่าสุดท้าย","Barwert des Endwerts"),
 "monthlyIncome": L("每月被動收入","Monthly Income","月間収入","월 수입","Ingreso mensual","Renda mensal","Pendapatan bulanan","Thu nhập hàng tháng","รายได้ต่อเดือน","Monatliches Einkommen"),
 "lost":          L("損失購買力","Purchasing Power Lost","失われた購買力","잃은 구매력","Poder adquisitivo perdido","Poder de compra perdido","Daya beli yang hilang","Sức mua mất đi","กำลังซื้อที่สูญเสีย","Verlorene Kaufkraft"),
 "lostPct":       L("購買力損失率","Loss %","損失率","손실률","% perdido","% perdido","% kerugian","% mất","% สูญเสีย","Verlust %"),
 "buyBelow":      L("建議買進價以下","Buy Below","これ以下で買う","매수 권장가 이하","Comprar por debajo de","Comprar abaixo de","Beli di bawah","Mua dưới mức","ซื้อต่ำกว่า","Kaufen unter"),
 "futureEPS":     L("預估未來EPS","Future EPS","将来予想EPS","미래 EPS","BPA futuro","LPA futuro","EPS masa depan","EPS tương lai","EPS ในอนาคต","Künftiger EPS"),
 "spread":        L("均線乖離","Spread","乖離","스프레드","Diferencial","Spread","Selisih","Chênh lệch","ส่วนต่าง","Spread"),
 "histogram":     L("MACD 柱狀值","Histogram","ヒストグラム","히스토그램","Histograma","Histograma","Histogram","Biểu đồ cột","ฮิสโตแกรม","Histogramm"),
 "trend":         L("趨勢方向","Trend","トレンド","추세","Tendencia","Tendência","Tren","Xu hướng","แนวโน้ม","Trend"),
 "posValue":      L("部位市值","Position Value","ポジション価値","포지션 가치","Valor de la posición","Valor da posição","Nilai posisi","Giá trị vị thế","มูลค่าสถานะ","Positionswert"),
 "marginPct":     L("保證金比率","Margin %","証拠金率","증거금 비율","Margen %","Margem %","Margin %","Tỷ lệ ký quỹ","อัตรามาร์จิน","Margin %"),
 "totalPayment":  L("總還款金額","Total Payment","総支払額","총 상환액","Pago total","Pagamento total","Total pembayaran","Tổng thanh toán","ยอดชำระรวม","Gesamtzahlung"),
 "totalInterest": L("總利息支出","Total Interest","総利息","총 이자","Intereses totales","Juros totais","Total bunga","Tổng lãi","ดอกเบี้ยรวม","Gesamtzinsen"),
 "breakEven":     L("損益平衡價","Break-Even Price","損益分岐点価格","손익분기 가격","Precio de equilibrio","Preço de equilíbrio","Harga impas","Giá hòa vốn","ราคาคุ้มทุน","Break-even-Preis"),
 "intrinsic":     L("內在價值","Intrinsic Value","本質的価値","내재가치","Valor intrínseco","Valor intrínseco","Nilai intrinsik","Giá trị nội tại","มูลค่าที่แท้จริง","Innerer Wert"),
 "earningsYield": L("盈餘殖利率","Earnings Yield","益利回り","이익수익률","Rendimiento de beneficios","Rendimento dos lucros","Imbal hasil laba","Tỷ suất lợi nhuận","อัตราผลตอบแทนกำไร","Gewinnrendite"),
 "totalUnits":    L("合約單位數","Total Units","総単位数","총 단위 수","Unidades totales","Total de unidades","Total unit","Tổng số đơn vị","จำนวนหน่วยรวม","Einheiten gesamt"),
 "riskAmt":       L("風險金額","Risk Amount","リスク額","위험 금액","Importe en riesgo","Valor de risco","Jumlah risiko","Số tiền rủi ro","จำนวนเงินเสี่ยง","Risikobetrag"),
 "years":         L("需投資年數","Years","年数","연수","Años","Anos","Tahun","Số năm","จำนวนปี","Jahre"),
 "rewardAmt":     L("報酬金額","Reward Amount","リワード額","보상 금액","Importe de recompensa","Valor de recompensa","Jumlah imbalan","Số tiền lợi nhuận","จำนวนผลตอบแทน","Ertragsbetrag"),
 "exact":         L("精確翻倍年數","Exact Years","正確な年数","정확한 연수","Años exactos","Anos exatos","Tahun tepat","Số năm chính xác","จำนวนปีที่แม่นยำ","Genaue Jahre"),
 "diff":          L("與72法則誤差","Difference","誤差","차이","Diferencia","Diferença","Selisih","Chênh lệch","ส่วนต่าง","Differenz"),
 "rating":        L("評級","Rating","評価","등급","Calificación","Classificação","Peringkat","Xếp hạng","การจัดอันดับ","Bewertung"),
 "pctChange":     L("漲跌幅","Change %","変化率","등락률","Cambio %","Variação %","Perubahan %","Thay đổi %","เปลี่ยนแปลง %","Änderung %"),
 "newPrice":      L("分割後股價","New Price","分割後株価","분할 후 가격","Nuevo precio","Novo preço","Harga baru","Giá mới","ราคาใหม่","Neuer Kurs"),
 "totalValue":    L("總市值","Total Value","総評価額","총 가치","Valor total","Valor total","Total nilai","Tổng giá trị","มูลค่ารวม","Gesamtwert"),
 "slPct":         L("停損百分比","Stop-Loss %","損切り率","손절 %","Stop-loss %","Stop-loss %","Stop-loss %","% cắt lỗ","% ตัดขาดทุน","Stop-Loss %"),
 "buyFee":        L("買進手續費","Buy Fee","買付手数料","매수 수수료","Comisión de compra","Taxa de compra","Biaya beli","Phí mua","ค่าธรรมเนียมซื้อ","Kaufgebühr"),
 "sellFee":       L("賣出手續費","Sell Fee","売却手数料","매도 수수료","Comisión de venta","Taxa de venda","Biaya jual","Phí bán","ค่าธรรมเนียมขาย","Verkaufsgebühr"),
 "tax":           L("交易稅","Tax","税金","세금","Impuesto","Imposto","Pajak","Thuế","ภาษี","Steuer"),
}

# 單位型別：money=金額符號  percent=百分比  none=無
KEY_UNIT = {
 "interest":"money","totalDeposit":"money","beRevenue":"money","margin":"money","totalCost":"money",
 "profit":"money","middle":"money","pvCashFlows":"money","pvTerminal":"money","monthlyIncome":"money",
 "lost":"money","buyBelow":"money","futureEPS":"money","posValue":"money","totalPayment":"money",
 "totalInterest":"money","breakEven":"money","intrinsic":"money","riskAmt":"money","rewardAmt":"money",
 "newPrice":"money","totalValue":"money","buyFee":"money","sellFee":"money","tax":"money",
 "atrPct":"percent","bandwidth":"percent","totalReturn":"percent","lostPct":"percent","marginPct":"percent",
 "earningsYield":"percent","pctChange":"percent","slPct":"percent",
}  # 其餘（rs,signal,stocks,bonds,totalShares,bodySize,range,usdValue,exchangeRate,spread,histogram,trend,totalUnits,years,exact,diff,rating）= none

SUBTITLE = L(
 "免費線上{T}，輸入數字即可立即試算，支援手機與電腦。",
 "Free online {T} — enter your numbers and get instant results, no sign-up.",
 "無料オンライン{T}。数値を入力するとすぐに計算できます。",
 "무료 온라인 {T} — 숫자만 입력하면 바로 결과를 확인할 수 있습니다.",
 "{T} en línea y gratis: introduce tus cifras y obtén resultados al instante.",
 "{T} online e grátis: insira seus números e veja resultados na hora.",
 "{T} online gratis — masukkan angka dan dapatkan hasil instan.",
 "{T} trực tuyến miễn phí — nhập số liệu và nhận kết quả ngay.",
 "{T} ออนไลน์ฟรี — กรอกตัวเลขแล้วคำนวณได้ทันที",
 "Kostenloser {T} — Zahlen eingeben und sofort Ergebnisse erhalten.")
META = L(
 "{T}：免費線上工具，輸入金額與參數即可立即計算，附完整教學說明，支援手機與電腦。",
 "{T}: a free online tool. Enter your figures for instant results, with a full guide included. Works on mobile and desktop.",
 "{T}：無料オンラインツール。数値を入力するとすぐに計算でき、詳しい解説付き。スマホ・PC対応。",
 "{T}: 무료 온라인 도구. 숫자를 입력하면 즉시 계산되며 자세한 가이드를 제공합니다. 모바일·PC 지원.",
 "{T}: herramienta online gratuita. Introduce tus datos para obtener resultados al instante, con una guía completa. Móvil y escritorio.",
 "{T}: ferramenta online gratuita. Insira seus dados para resultados instantâneos, com guia completo. Celular e desktop.",
 "{T}: alat online gratis. Masukkan angka untuk hasil instan, dilengkapi panduan lengkap. Mendukung ponsel dan desktop.",
 "{T}: công cụ trực tuyến miễn phí. Nhập số liệu để có kết quả tức thì, kèm hướng dẫn đầy đủ. Hỗ trợ điện thoại và máy tính.",
 "{T}: เครื่องมือออนไลน์ฟรี กรอกตัวเลขเพื่อคำนวณทันที พร้อมคู่มือฉบับเต็ม รองรับมือถือและคอมพิวเตอร์",
 "{T}: kostenloses Online-Tool. Zahlen eingeben für sofortige Ergebnisse, inklusive ausführlicher Anleitung. Für Handy und Desktop.")

GENERIC_CAP = L("計算結果","Result","計算結果","계산 결과","Resultado","Resultado","Hasil","Kết quả","ผลลัพธ์","Ergebnis")

MAIN = {
 "compound-interest":{"unit":"money","cap":L("未來總價值","Future Value","将来の総額","미래 가치","Valor futuro","Valor futuro","Nilai masa depan","Giá trị tương lai","มูลค่าในอนาคต","Endkapital")},
 "rsi-calculator":{"unit":"none","cap":L("RSI 值（0–100）","RSI Value (0–100)","RSI値（0〜100）","RSI 값 (0–100)","Valor RSI (0–100)","Valor RSI (0–100)","Nilai RSI (0–100)","Giá trị RSI (0–100)","ค่า RSI (0–100)","RSI-Wert (0–100)")},
 "break-even":{"unit":"none","cap":L("損益平衡銷售量（單位）","Break-Even Units","損益分岐点の販売数量","손익분기 판매량","Unidades de equilibrio","Unidades de equilíbrio","Unit impas","Số đơn vị hòa vốn","จำนวนหน่วยจุดคุ้มทุน","Break-even-Stückzahl")},
}

SIG = {"zh":("超買","超賣","中性"),"en":("Overbought","Oversold","Neutral"),"ja":("買われすぎ","売られすぎ","中立"),"ko":("과매수","과매도","중립"),"es":("Sobrecompra","Sobreventa","Neutral"),"pt":("Sobrecomprado","Sobrevendido","Neutro"),"id":("Jenuh beli","Jenuh jual","Netral"),"vi":("Quá mua","Quá bán","Trung tính"),"th":("ซื้อมากเกินไป","ขายมากเกินไป","เป็นกลาง"),"de":("Überkauft","Überverkauft","Neutral")}

VZ_PRINCIPAL = L("本金","Principal","元本","원금","Capital","Principal","Pokok","Vốn gốc","เงินต้น","Kapital")
VZ_INTEREST  = L("利息","Interest","利息","이자","Intereses","Juros","Bunga","Lãi","ดอกเบี้ย","Zinsen")
VZ_MARGINR   = L("邊際貢獻率","Margin Ratio","限界利益率","공헌이익률","Margen %","Margem %","Rasio margin","Tỷ lệ lãi góp","อัตรากำไรส่วนเกิน","Deckungsbeitrag %")
VZ_BESELL    = L("需賣出 {u} 單位才能回本","Sell {u} units to break even","損益分岐点まで {u} 単位の販売が必要","손익분기까지 {u} 단위 판매 필요","Vende {u} unidades para alcanzar el equilibrio","Venda {u} unidades para o equilíbrio","Jual {u} unit untuk impas","Bán {u} đơn vị để hòa vốn","ต้องขาย {u} หน่วยจึงคุ้มทุน","{u} Einheiten verkaufen, um break-even zu erreichen")

unknown_keys = set()

def lang_of(path):
    rel = os.path.relpath(path, ROOT).replace("\\","/").split("/")
    return rel[0] if len(rel)>=2 and rel[0] in LANGS else "zh"

def tool_of(path):
    return os.path.basename(path).replace(".html","")

def usuffix(lang, sym):
    return f"（{sym}）" if lang in ("zh","ja","ko") else f" ({sym})"

def label_text(key, lang):
    if key in LABELS:
        base = LABELS[key].get(lang, LABELS[key]["en"])
    else:
        unknown_keys.add(key)
        base = re.sub(r"(?<=[a-z])(?=[A-Z])"," ",key).title()
    u = KEY_UNIT.get(key)
    if u=="money":   base += usuffix(lang, MONEY[lang])
    elif u=="percent": base += usuffix(lang, "%")
    return base

CSS_ADD = """
/* ==== uifix-v1 視覺強化 ==== */
.input-group{margin-bottom:18px}
.input-group input,.input-group select{padding:14px;font-size:16px;border-radius:10px}
.btn{padding:16px;font-size:17px;border-radius:10px}
.result-row{padding:12px 0}
.result-cap{font-size:13px;color:#7fcfa6;letter-spacing:.02em;margin-bottom:2px}
.viz{margin-top:18px}
.viz .bar{display:flex;height:26px;border-radius:8px;overflow:hidden;background:#10210f}
.viz .seg{display:flex;align-items:center;justify-content:center;font-size:11px;color:#fff;white-space:nowrap}
.viz .legend{display:flex;gap:16px;margin-top:8px;font-size:12px;color:#bbb;flex-wrap:wrap}
.viz .dot{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:5px;vertical-align:middle}
.viz .gauge{position:relative;height:30px;border-radius:8px;overflow:hidden;display:flex}
.viz .gz{display:flex;align-items:center;justify-content:center;font-size:11px;color:#fff}
.viz .mark{position:absolute;top:-4px;width:2px;height:38px;background:#fff}
.viz .note{margin-top:10px;font-size:13px;color:#eee}
@media(max-width:520px){.container{padding:24px 16px}.result-main{font-size:28px}.btn{padding:18px}}
"""

def build_viz_js(tool, lang):
    common = """
<script>
(function(){
 var _o=window.calculate;if(typeof _o!=='function')return;
 function num(id){var e=document.getElementById(id);return e?parseFloat((e.textContent||'').replace(/[^0-9.\\-]/g,'')):0;}
 function box(){var b=document.getElementById('vizBox');if(b)b.innerHTML='';return b;}
 window.calculate=function(){_o();try{draw();}catch(e){}};
 function draw(){var b=box();if(!b)return;
"""
    end = "\n }\n})();\n</script>\n"
    if tool=="compound-interest":
        body = """
  var tot=num('result'),inte=num('interest'),dep=num('totalDeposit');if(tot<=0)return;
  var pd=Math.max(0,Math.min(100,dep/tot*100)),pi=100-pd;
  b.innerHTML='<div class="bar">'+
   '<div class="seg" style="width:'+pd+'%;background:#2f8f5e">'+(pd>12?Math.round(pd)+'%':'')+'</div>'+
   '<div class="seg" style="width:'+pi+'%;background:#f0b429;color:#1a1a18">'+(pi>12?Math.round(pi)+'%':'')+'</div></div>'+
   '<div class="legend"><span><span class="dot" style="background:#2f8f5e"></span>'+PR+'</span>'+
   '<span><span class="dot" style="background:#f0b429"></span>'+IN+'</span></div>';
""".replace("PR",json.dumps(VZ_PRINCIPAL[lang])).replace("IN",json.dumps(VZ_INTEREST[lang]))
        return common+body+end
    if tool=="rsi-calculator":
        ob,os_,nu = [json.dumps(x) for x in SIG[lang]]
        body = """
  var v=num('result');if(v<0)v=0;if(v>100)v=100;
  b.innerHTML='<div class="gauge">'+
   '<div class="gz" style="background:#2f8f5e;flex:0 0 30%">'+OS+'</div>'+
   '<div class="gz" style="background:#3a3a36;flex:0 0 40%">'+NU+'</div>'+
   '<div class="gz" style="background:#c0392b;flex:0 0 30%">'+OB+'</div>'+
   '<div class="mark" style="left:'+v+'%"></div></div>'+
   '<div class="note">RSI = '+v.toFixed(1)+'</div>';
""".replace("OS",os_).replace("NU",nu).replace("OB",ob)
        return common+body+end
    if tool=="break-even":
        body = """
  var marg=num('margin'),up=parseFloat((document.getElementById('unitPrice')||{}).value||0),u=num('result');
  if(up<=0)return;var pr=Math.max(0,Math.min(100,marg/up*100));
  b.innerHTML='<div class="bar"><div class="seg" style="width:'+pr+'%;background:#2f8f5e">'+Math.round(pr)+'%</div></div>'+
   '<div class="legend"><span><span class="dot" style="background:#2f8f5e"></span>'+MR+'</span></div>'+
   '<div class="note">'+SELL.replace('{u}',u.toLocaleString())+'</div>';
""".replace("MR",json.dumps(VZ_MARGINR[lang])).replace("SELL",json.dumps(VZ_BESELL[lang]))
        return common+body+end
    return ""

def process(path):
    html = open(path, encoding="utf-8").read()
    if GUARD in html: return "skip"
    lang = lang_of(path); tool = tool_of(path)
    m = re.search(r"<h1>(.*?)</h1>", html, re.S)
    T = m.group(1).strip() if m else tool

    if tool != "index":
        html = re.sub(r'(<p class="subtitle">).*?(</p>)',
                      lambda mm: mm.group(1)+SUBTITLE[lang].format(T=T)+mm.group(2), html, count=1, flags=re.S)
        html = re.sub(r'(<meta name="description" content=").*?(">)',
                      lambda mm: mm.group(1)+META[lang].format(T=T)+mm.group(2), html, count=1, flags=re.S)

    def repl_label(mm):
        key = mm.group(1)
        return f'<span class="result-label" data-key="{key}">{label_text(key, lang)}</span>'
    html = re.sub(r'<span class="result-label" data-key="([^"]+)">.*?</span>', repl_label, html, flags=re.S)

    if tool in MAIN:
        cap = MAIN[tool]["cap"].get(lang, MAIN[tool]["cap"]["en"])
        if MAIN[tool]["unit"]=="money": cap += usuffix(lang, MONEY[lang])
    else:
        cap = GENERIC_CAP[lang]
    html = html.replace('<div class="result-main" id="result">—</div>',
                        f'<div class="result-cap">{cap}</div><div class="result-main" id="result">—</div>', 1)

    html = html.replace('</div>\n    <div id="extraLevels"></div>',
                        '<div class="viz" id="vizBox"></div></div>\n    <div id="extraLevels"></div>', 1)

    if "'Overbought / 超買'" in html:
        ob,os_,nu = SIG[lang]
        html = html.replace("rsi>70?'Overbought / 超買':rsi<30?'Oversold / 超賣':'Neutral / 中性'",
                            f"rsi>70?'{ob}':rsi<30?'{os_}':'{nu}'")

    html = html.replace("</style>", CSS_ADD+"\n</style>", 1)
    vjs = build_viz_js(tool, lang)
    if vjs: html = html.replace("</body>", vjs+"</body>", 1)
    html = html.replace("</head>", GUARD+"</head>", 1)
    open(path, "w", encoding="utf-8").write(html)
    return "ok"

def main():
    done = skipped = 0
    for dp,_,files in os.walk(ROOT):
        for fn in files:
            if fn.endswith(".html"):
                r = process(os.path.join(dp, fn))
                done += (r=="ok"); skipped += (r=="skip")
    print(f"完成 {done} 個檔，跳過（已修過）{skipped} 個")
    print("⚠️ 未知 data-key：", sorted(unknown_keys) if unknown_keys else "無（全部都有對應翻譯）")

if __name__ == "__main__":
    main()
