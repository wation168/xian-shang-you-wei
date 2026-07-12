import os, json

OUT = "/home/claude/patterns-gen/out"
os.makedirs(OUT, exist_ok=True)

# ── Locale UI strings ─────────────────────────────────────────────────────────
UI = {
    "zh-tw": {
        "site": "線上有位", "home": "首頁", "learn": "教學",
        "title": "K棒與型態完全解析",
        "subtitle": "從K棒基礎到50+型態，附實戰勝率統計",
        "badge": "技術分析教學",
        "back": "← 回到型態總覽",
        "signal_lbl": "信號方向", "wr_lbl": "勝率", "move_lbl": "平均幅度",
        "rel_lbl": "可信度", "vol_lbl": "需配合量能",
        "def_lbl": "型態定義", "psy_lbl": "形成原因（市場心理）",
        "app_lbl": "實戰應用", "cau_lbl": "注意事項",
        "sig": {"bullish":"多頭","bearish":"空頭","neutral":"中性"},
        "rel": {"high":"可信度高","medium":"可信度中","low":"可信度低"},
        "yes": "是", "no": "否",
        "index_sub": "完整學習50+種K棒與圖表型態，每種型態含SVG圖解、市場心理分析、實戰應用與統計勝率。",
        "sec": {"single":"單根K棒型態","combo":"組合型態","reversal":"頭肩型態","continuation":"整理型態"},
        "tips_title": "實戰注意事項",
        "tips": [
            "單一K棒型態勝率約50~74%，需搭配均線、成交量、趨勢方向才能提高準確率。",
            "型態出現在關鍵支撐壓力位置時，信號可信度大幅提升。",
            "成交量是確認型態有效性最重要的輔助指標，量縮的突破或反轉可靠性低。",
            "頭肩與整理型態需要在週線或日線圖上確認，分鐘圖雜訊過多。",
            "任何型態都有失敗案例，嚴格執行停損是保護資金的唯一方法。",
        ],
        "free": "免費", "footer": "專業台股技術分析平台，提供即時K棒分析、多空雷達、深度選股等功能。",
        "upgrade": "立即升級會員",
    },
    "en": {
        "site": "SoftGlow AI", "home": "Home", "learn": "Learn",
        "title": "Complete Guide to Candlestick Patterns",
        "subtitle": "From candlestick basics to 50+ patterns with win-rate statistics",
        "badge": "Technical Analysis Guide",
        "back": "← Back to Pattern Index",
        "signal_lbl": "Signal", "wr_lbl": "Win Rate", "move_lbl": "Avg. Move",
        "rel_lbl": "Reliability", "vol_lbl": "Volume Required",
        "def_lbl": "Pattern Definition", "psy_lbl": "Market Psychology",
        "app_lbl": "Trading Application", "cau_lbl": "Caution",
        "sig": {"bullish":"Bullish","bearish":"Bearish","neutral":"Neutral"},
        "rel": {"high":"High Reliability","medium":"Medium Reliability","low":"Low Reliability"},
        "yes": "Yes", "no": "No",
        "index_sub": "Master 50+ candlestick and chart patterns. Each includes SVG diagrams, market psychology, trading applications, and historical win-rate statistics.",
        "sec": {"single":"Single Candlestick Patterns","combo":"Combination Patterns","reversal":"Head & Shoulders","continuation":"Continuation Patterns"},
        "tips_title": "Trading Tips",
        "tips": [
            "Single candlestick patterns have win rates of 50–74%. Combine with moving averages, volume, and trend direction to improve accuracy.",
            "Patterns appearing at key support and resistance levels carry significantly higher reliability.",
            "Volume is the most important confirmation indicator. Low-volume breakouts or reversals are less reliable.",
            "Head & shoulders and continuation patterns should be confirmed on daily or weekly charts.",
            "Every pattern has failure cases. Strict stop-loss execution is the only way to protect your capital.",
        ],
        "free": "Free", "footer": "Professional Taiwan stock technical analysis platform with real-time candlestick analysis, bull-bear radar, and deep stock screening.",
        "upgrade": "Upgrade to Premium",
    },
    "ja": {
        "site": "SoftGlow AI", "home": "ホーム", "learn": "学習",
        "title": "ローソク足・チャートパターン完全解説",
        "subtitle": "ローソク足の基礎から50以上のパターンまで、実際の勝率統計付き",
        "badge": "テクニカル分析ガイド",
        "back": "← パターン一覧に戻る",
        "signal_lbl": "シグナル", "wr_lbl": "勝率", "move_lbl": "平均変動幅",
        "rel_lbl": "信頼性", "vol_lbl": "出来高確認",
        "def_lbl": "パターンの定義", "psy_lbl": "市場心理（形成の理由）",
        "app_lbl": "実戦での活用", "cau_lbl": "注意点",
        "sig": {"bullish":"強気","bearish":"弱気","neutral":"中立"},
        "rel": {"high":"信頼性高","medium":"信頼性中","low":"信頼性低"},
        "yes": "要", "no": "不要",
        "index_sub": "50種類以上のローソク足・チャートパターンを完全解説。各パターンにSVG図解、市場心理の分析、実戦活用法と統計的勝率を掲載。",
        "sec": {"single":"単一ローソク足パターン","combo":"組み合わせパターン","reversal":"ヘッドアンドショルダー","continuation":"継続パターン"},
        "tips_title": "実戦での注意点",
        "tips": [
            "単一ローソク足パターンの勝率は50〜74%です。移動平均線・出来高・トレンド方向と組み合わせることで精度が向上します。",
            "主要なサポート・レジスタンスラインで出現したパターンは信頼性が大幅に高まります。",
            "出来高はパターンの有効性を確認するための最重要補助指標です。",
            "ヘッドアンドショルダーや継続パターンは日足・週足チャートで確認してください。",
            "すべてのパターンには失敗例があります。厳格なロスカットの実行が資金を守る唯一の方法です。",
        ],
        "free": "無料", "footer": "台湾株式市場向けテクニカル分析プラットフォーム。リアルタイムローソク足分析、強弱レーダー、銘柄スクリーニング機能を提供。",
        "upgrade": "プレミアムにアップグレード",
    },
    "ko": {
        "site": "SoftGlow AI", "home": "홈", "learn": "학습",
        "title": "캔들스틱 패턴 완전 가이드",
        "subtitle": "캔들 기초부터 50+ 패턴까지, 실전 승률 통계 포함",
        "badge": "기술적 분석 가이드",
        "back": "← 패턴 목록으로 돌아가기",
        "signal_lbl": "신호", "wr_lbl": "승률", "move_lbl": "평균 변동폭",
        "rel_lbl": "신뢰도", "vol_lbl": "거래량 확인",
        "def_lbl": "패턴 정의", "psy_lbl": "시장 심리 (형성 이유)",
        "app_lbl": "실전 활용", "cau_lbl": "주의사항",
        "sig": {"bullish":"강세","bearish":"약세","neutral":"중립"},
        "rel": {"high":"신뢰도 높음","medium":"신뢰도 보통","low":"신뢰도 낮음"},
        "yes": "필요", "no": "불필요",
        "index_sub": "50가지 이상의 캔들스틱 및 차트 패턴을 완벽 해설. 각 패턴마다 SVG 도해, 시장 심리 분석, 실전 활용법, 통계적 승률을 제공합니다.",
        "sec": {"single":"단일 캔들 패턴","combo":"조합 패턴","reversal":"헤드앤숄더","continuation":"지속 패턴"},
        "tips_title": "실전 주의사항",
        "tips": [
            "단일 캔들 패턴의 승률은 50~74%입니다. 이동평균선, 거래량, 추세 방향과 함께 활용하면 정확도가 높아집니다.",
            "주요 지지·저항 구간에서 나타나는 패턴은 신뢰도가 크게 높아집니다.",
            "거래량은 패턴의 유효성을 확인하는 가장 중요한 보조 지표입니다.",
            "헤드앤숄더와 지속 패턴은 일봉 또는 주봉 차트에서 확인하세요.",
            "모든 패턴에는 실패 사례가 있습니다. 철저한 손절 실행만이 자금을 보호하는 방법입니다.",
        ],
        "free": "무료", "footer": "대만 주식 전문 기술적 분석 플랫폼. 실시간 캔들스틱 분석, 강약세 레이더, 종목 스크리닝 기능 제공.",
        "upgrade": "프리미엄으로 업그레이드",
    },
}

LOCALE_FILE = {"zh-tw": "index.html", "en": "en.html", "ja": "ja.html", "ko": "ko.html"}
LOCALE_LANG = {"zh-tw": "zh-TW", "en": "en", "ja": "ja", "ko": "ko"}

# ── SVG candle renderer ───────────────────────────────────────────────────────
def candle_svg(candles, width=200, height=130):
    cols = {"bull": "#22c55e", "bear": "#ef4444", "neutral": "#94a3b8"}
    n = len(candles)
    pad = 14
    slot_w = (width - pad * 2) / n
    vals = [v for c in candles for v in [c["o"], c["h"], c["l"], c["c"]]]
    vmin, vmax = min(vals), max(vals)
    rng = vmax - vmin or 1
    def y(v): return 8 + (1 - (v - vmin) / rng) * (height - 18)
    lines = [f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:{width}px">']
    for i, c in enumerate(candles):
        cx = pad + i * slot_w + slot_w / 2
        col = cols.get(c.get("color", "neutral"), "#94a3b8")
        yo, yc, yh, yl = y(c["o"]), y(c["c"]), y(c["h"]), y(c["l"])
        bt = min(yo, yc); bh = max(abs(yc - yo), 2); bw = slot_w * 0.52
        lines.append(f'<line x1="{cx:.1f}" y1="{yh:.1f}" x2="{cx:.1f}" y2="{yl:.1f}" stroke="{col}" stroke-width="1.5"/>')
        lines.append(f'<rect x="{cx-bw/2:.1f}" y="{bt:.1f}" width="{bw:.1f}" height="{bh:.1f}" fill="{col}" rx="1"/>')
    lines.append("</svg>")
    return "\n".join(lines)

# ── CSS (shared) ──────────────────────────────────────────────────────────────
CSS = """
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#0d1117;--surface:#161b22;--border:#21262d;
  --text:#e6edf3;--muted:#8b949e;--accent:#f59e0b;
  --bull:#22c55e;--bear:#ef4444;--blue:#3b82f6;
  --radius:8px;--font:'Inter',system-ui,sans-serif;
}
body{background:var(--bg);color:var(--text);font-family:var(--font);line-height:1.6;font-size:15px}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
/* nav */
nav{background:var(--surface);border-bottom:1px solid var(--border);padding:14px 24px;display:flex;align-items:center;gap:16px;position:sticky;top:0;z-index:100}
.nav-logo{font-weight:700;font-size:18px;color:var(--accent)}
.nav-links{display:flex;gap:16px;margin-left:auto;font-size:14px}
/* hero */
.hero{background:linear-gradient(135deg,#0d1117 0%,#1a1f2e 100%);padding:60px 24px 40px;text-align:center;border-bottom:1px solid var(--border)}
.hero-badge{display:inline-block;background:#1e3a5f;color:#60a5fa;border:1px solid #1d4ed8;border-radius:20px;padding:4px 14px;font-size:13px;margin-bottom:16px}
.hero h1{font-size:clamp(28px,5vw,48px);font-weight:800;letter-spacing:-1px;line-height:1.2}
.hero h1 span{background:linear-gradient(90deg,var(--bull),var(--accent));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.hero-sub{color:var(--muted);margin-top:12px;font-size:16px;max-width:640px;margin-inline:auto}
/* main layout */
.container{max-width:1100px;margin:0 auto;padding:0 24px}
/* index grid */
.section-header{margin:40px 0 20px;padding-bottom:10px;border-bottom:1px solid var(--border)}
.section-header h2{font-size:20px;font-weight:700;color:var(--accent)}
.pattern-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px;margin-bottom:16px}
.pattern-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:18px;transition:border-color .2s,transform .2s;cursor:pointer;display:block}
.pattern-card:hover{border-color:var(--accent);transform:translateY(-2px)}
.card-svg{height:90px;display:flex;align-items:center;justify-content:center;margin-bottom:12px}
.card-name{font-weight:700;font-size:15px;margin-bottom:6px}
.card-meta{display:flex;gap:8px;flex-wrap:wrap}
.tag{display:inline-block;padding:2px 8px;border-radius:12px;font-size:12px;font-weight:600}
.tag-bull{background:#14532d;color:var(--bull)}.tag-bear{background:#450a0a;color:var(--bear)}.tag-neutral{background:#1e293b;color:var(--muted)}
.tag-high{background:#1c2e1c;color:#86efac}.tag-medium{background:#2a2007;color:#fcd34d}.tag-low{background:#1e1e2e;color:#94a3b8}
/* detail page */
.detail-back{display:inline-block;margin:24px 0 0;color:var(--muted);font-size:14px}
.detail-back:hover{color:var(--accent)}
.detail-hero{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:28px;margin:16px 0 28px;display:grid;grid-template-columns:1fr auto;gap:24px;align-items:start}
.detail-title{font-size:clamp(22px,4vw,36px);font-weight:800;letter-spacing:-0.5px;margin-bottom:12px}
.detail-stats{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;min-width:220px}
.stat-box{background:var(--bg);border:1px solid var(--border);border-radius:6px;padding:10px 14px}
.stat-label{color:var(--muted);font-size:12px;margin-bottom:2px}
.stat-value{font-size:18px;font-weight:700}
.svg-box{background:var(--bg);border:1px solid var(--border);border-radius:var(--radius);padding:16px;display:flex;justify-content:center}
.content-section{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:22px;margin-bottom:16px}
.content-section h3{font-size:16px;font-weight:700;color:var(--accent);margin-bottom:12px;display:flex;align-items:center;gap:8px}
.content-section h3::before{content:'';display:inline-block;width:4px;height:16px;background:var(--accent);border-radius:2px}
.content-section p{color:#c9d1d9;line-height:1.75}
/* tips */
.tips-list{list-style:none;display:flex;flex-direction:column;gap:10px}
.tips-list li{display:flex;gap:10px;align-items:flex-start;color:#c9d1d9}
.tips-list li::before{content:"▸";color:var(--accent);flex-shrink:0;margin-top:2px}
/* footer */
footer{background:var(--surface);border-top:1px solid var(--border);padding:32px 24px;margin-top:60px;text-align:center;color:var(--muted);font-size:14px}
.footer-logo{color:var(--accent);font-weight:700;font-size:18px;margin-bottom:8px}
/* win rate bar */
.wr-bar-wrap{margin-top:8px;background:#21262d;border-radius:4px;height:6px;width:100%}
.wr-bar{height:6px;border-radius:4px;background:var(--bull)}
/* lang switcher */
.lang-switcher{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}
.lang-btn{padding:4px 12px;border:1px solid var(--border);border-radius:16px;font-size:13px;color:var(--muted);transition:.2s}
.lang-btn:hover,.lang-btn.active{border-color:var(--accent);color:var(--accent)}
/* responsive */
@media(max-width:680px){
  .detail-hero{grid-template-columns:1fr}
  .detail-stats{grid-template-columns:repeat(2,1fr)}
}
"""

# ── Pattern data ──────────────────────────────────────────────────────────────
PATTERNS = [
  # ── Single candles ──────────────────────────────────────────────────────────
  {"id":"big-bullish","section":"single","signal":"bullish","wr":68,"move":8.0,"rel":"medium","vol":True,
   "svg":[{"o":20,"h":92,"l":18,"c":90,"color":"bull"}],
   "names":{"zh-tw":"大陽線","en":"Big Bullish Candle","ja":"大陽線","ko":"대양선"},
   "content":{
     "zh-tw":{"def":"大陽線是實體極長、幾乎無上下影線的紅色K棒。開盤後買盤持續湧入，收盤價遠高於開盤價，代表市場極度樂觀。實體長度通常超過前幾根K棒均值的2倍以上才稱為大陽線。",
              "psy":"大陽線反映強烈的多頭共識。當天幾乎沒有空頭能夠阻擋買盤，賣方在盤中完全退縮，價格從早到晚單邊拉升。這種型態常出現在重大利多消息或突破長期壓力後，代表市場情緒從觀望轉為積極追多。成交量配合放大時，說明大量資金認同這個方向。",
              "app":"大陽線出現在盤整區突破時，是最強的進場信號之一，可在收盤前或次日開盤追入。若出現在均線糾結後，代表多頭正式確立，目標看前高或1.5倍實體延伸。搭配成交量放大超過5日均量的1.5倍效果最佳。也可用做停損參考，跌破大陽線實體中點即出場。",
              "cau":"大陽線出現在高點（距近期低點漲幅超過30%）時需謹慎，可能是最後一波軋空，主力出貨的跡象。連續三根大陽線後（三白兵）要特別注意是否出現量縮，量縮則是見頂訊號。"},
     "en":{"def":"A Big Bullish Candle features an exceptionally long body with little to no shadows. Buying pressure persists throughout the session, closing significantly higher than the open, reflecting extreme market optimism. The body is typically more than twice the average of recent candles.",
           "psy":"This candle reflects a strong bullish consensus. Bears are unable to push prices back during the session, and the price rises steadily from open to close. This pattern often appears after major positive news or a breakout above long-term resistance, signaling a shift in market sentiment from neutral to aggressively bullish. High volume confirms broad participation.",
           "app":"When a Big Bullish Candle appears at a breakout from a consolidation range, it is one of the strongest entry signals. Consider entering before the close or at the next day's open. If it appears after a moving average compression, a bullish trend is confirmed with a target at the prior high or 1.5x body extension. Best confirmed with volume exceeding 1.5x the 5-day average.",
           "cau":"Be cautious when this pattern appears at a high level (30%+ above recent lows), as it may signal a short squeeze or distribution by large players. Three consecutive big bullish candles with declining volume is a topping signal."},
     "ja":{"def":"大陽線は実体が極めて長く、上下のひげがほとんどない陽線です。取引開始から終了まで買いが続き、終値が始値を大きく上回り、市場の強い楽観ムードを示します。実体の長さは通常、直近の平均的なローソク足の2倍以上です。",
           "psy":"大陽線は強い強気の市場合意を反映しています。その日は売り方がほとんど抵抗できず、価格は朝から夕方まで一方的に上昇します。このパターンは重要なポジティブニュースや長期レジスタンスのブレイク後に現れることが多く、市場心理が様子見から積極的な買いへ転換したことを示します。出来高増加で多くの参加者の支持が確認できます。",
           "app":"保ち合いからのブレイク時に大陽線が現れた場合、最も強い買いシグナルの一つです。引け前か翌日の寄り付きに参入を検討してください。移動平均線の収束後に出現した場合は強気トレンドの確立を意味し、直近高値または実体の1.5倍が目標です。5日平均出来高の1.5倍以上の出来高で最も効果的です。",
           "cau":"直近安値から30%以上上昇した高値圏での大陽線は、踏み上げや大口の売り抜けの可能性があるため注意が必要です。大陽線が3本連続した後に出来高が減少した場合は天井のサインです。"},
     "ko":{"def":"대양선은 몸통이 매우 길고 위아래 꼬리가 거의 없는 양봉입니다. 장중 내내 매수세가 지속되어 종가가 시가보다 크게 높아지며 시장의 강한 낙관론을 반영합니다. 몸통 길이는 보통 최근 캔들 평균의 2배 이상입니다.",
           "psy":"대양선은 강한 강세 시장 합의를 반영합니다. 그날 매도 세력이 거의 저항하지 못하고 가격이 시작부터 끝까지 일방적으로 상승합니다. 이 패턴은 주요 호재 발표나 장기 저항선 돌파 후 자주 나타나며, 시장 심리가 관망에서 적극적인 매수로 전환됐음을 보여줍니다. 거래량 증가는 광범위한 참여를 확인해줍니다.",
           "app":"대양선이 횡보 구간 돌파 시 나타나면 가장 강력한 매수 신호 중 하나입니다. 종가 직전 또는 다음 날 시가에 진입을 고려하세요. 이동평균선 수렴 후 나타나면 강세 추세 확립을 의미하며 목표가는 이전 고점 또는 몸통의 1.5배 연장입니다. 5일 평균 거래량의 1.5배 이상일 때 가장 효과적입니다.",
           "cau":"최근 저점 대비 30% 이상 오른 고점에서 대양선이 나타나면 숏스퀴즈나 세력의 매도일 수 있으니 주의가 필요합니다. 대양선 3개 연속 후 거래량이 감소하면 천정 신호입니다."},
   }},
  {"id":"big-bearish","section":"single","signal":"bearish","wr":71,"move":-8.0,"rel":"medium","vol":True,
   "svg":[{"o":90,"h":92,"l":18,"c":20,"color":"bear"}],
   "names":{"zh-tw":"大陰線","en":"Big Bearish Candle","ja":"大陰線","ko":"대음선"},
   "content":{
     "zh-tw":{"def":"大陰線是實體極長、幾乎無上下影線的黑色K棒。開盤後賣壓持續湧現，收盤價遠低於開盤價，代表市場強烈看空。實體長度通常超過前幾根K棒均值的2倍以上。",
              "psy":"大陰線代表壓倒性的空頭力量。多頭完全無法在盤中抵抗賣壓，價格從開盤到收盤持續下殺。這種型態常見於重大利空消息或跌破重要支撐後，代表市場情緒快速由樂觀轉為恐慌。若成交量同步放大，代表大量持股人選擇出場，後續下跌風險高。",
              "app":"大陰線出現在整理區跌破時，是明確的做空或出場信號。持有多頭部位者應在大陰線收盤確認後立即減倉。若尚未進場，可觀察次日反彈至大陰線實體中段時做空，停損設在大陰線最高點。目標看下方支撐位或大陰線實體延伸1~1.5倍。",
              "cau":"大陰線若出現在已大幅下跌的低點（跌幅超過30%），可能是最後一波殺低後見底。此時量能若異常放大（是前幾天的3倍以上），反而可能是轉機。不宜在低點追空。"},
     "en":{"def":"A Big Bearish Candle features a very long body with little to no shadows. Selling pressure dominates the entire session, and the closing price is far below the open, signaling strong bearish sentiment. The body is typically more than twice the average of recent candles.",
           "psy":"This candle reflects overwhelming bearish force. Bulls are completely unable to resist selling pressure, and prices fall steadily from open to close. It commonly appears after major negative news or breakdowns below key support, indicating a rapid shift in sentiment from optimism to panic. High volume suggests mass exit by holders.",
           "app":"When a Big Bearish Candle breaks down from a consolidation zone, it is a clear signal to short or exit long positions. Long holders should reduce positions immediately after the candle closes. New short positions can be entered on a pullback to the midpoint of the bearish body. Target the next support level or 1–1.5x body extension downward.",
           "cau":"A Big Bearish Candle appearing at a significantly depressed level (down 30%+ already) may represent a final capitulation flush before a bottom. If volume is unusually high (3x+ recent average), it could signal a reversal opportunity. Avoid chasing shorts at low levels."},
     "ja":{"def":"大陰線は実体が極めて長く、上下のひげがほとんどない陰線です。取引時間中ずっと売りが優勢で、終値が始値を大きく下回り、強い弱気センチメントを示します。実体の長さは通常、直近の平均ローソク足の2倍以上です。",
           "psy":"大陰線は圧倒的な売り勢力を反映しています。買い方は値下がりに全く抵抗できず、価格は寄り付きから引けまで一方的に下落します。決算ショックや政策インパクトなどの重大な悪材料や、重要サポートの割れ後に多く見られ、楽観からパニックへの急転換を示します。出来高増加は大量の保有者が売却したことを示します。",
           "app":"保ち合いを割り込む大陰線は、売り建てまたはロング手仕舞いの明確なシグナルです。ロング保有者は大陰線の確定後すぐに減らすべきです。新規の売りは翌日に大陰線実体の中間点へ戻った際に建て、高値にストップを置きます。目標は次のサポートまたは実体の1〜1.5倍の下落幅です。",
           "cau":"大陰線がすでに大きく下落した安値圏（30%以上の下落）に出現した場合、底値付近での最終的な投げ売りの可能性があります。出来高が異常に多い場合は反転のサインかもしれません。安値圏での追い売りは避けてください。"},
     "ko":{"def":"대음선은 몸통이 매우 길고 위아래 꼬리가 거의 없는 음봉입니다. 장중 내내 매도세가 지속되어 종가가 시가보다 크게 낮아지며 강한 약세 심리를 반영합니다. 몸통 길이는 보통 최근 캔들 평균의 2배 이상입니다.",
           "psy":"대음선은 압도적인 매도 세력을 반영합니다. 매수 세력이 하락을 전혀 막지 못하고 가격이 시작부터 끝까지 일방적으로 하락합니다. 실적 쇼크나 정책 충격 같은 중대 악재 발표 후 또는 주요 지지선 이탈 후 자주 나타나며, 시장 심리가 낙관에서 공황으로 빠르게 전환됐음을 보여줍니다.",
           "app":"대음선이 횡보 구간 이탈 시 나타나면 공매도 진입 또는 롱 포지션 청산의 명확한 신호입니다. 롱 보유자는 대음선 확정 후 즉시 포지션을 줄여야 합니다. 신규 공매도는 다음 날 대음선 몸통 중간 지점으로 반등 시 진입하고 최고점에 손절을 설정합니다.",
           "cau":"대음선이 이미 크게 하락한 저점(30% 이상 하락)에서 나타나면 바닥 근처 마지막 투매일 수 있습니다. 거래량이 비정상적으로 많으면 반전 신호일 수 있습니다. 저점에서의 추격 공매도는 피하세요."},
   }},
  {"id":"doji","section":"single","signal":"neutral","wr":54,"move":0,"rel":"low","vol":False,
   "svg":[{"o":50,"h":80,"l":20,"c":50,"color":"neutral"}],
   "names":{"zh-tw":"標準十字","en":"Doji","ja":"十字線","ko":"도지"},
   "content":{
     "zh-tw":{"def":"標準十字線的開盤價與收盤價幾乎相同，形成極短或無實體的十字形狀，上下影線長度相近。代表當日多空力量完全均衡，市場陷入最大不確定性。",
              "psy":"十字線是多空完全平衡的表現。開盤後雙方交替控盤，但最終收回原點，任何一方都無法確立優勢。常出現在趨勢疲態時刻，代表原有動能正在消退。在長期上漲或下跌後出現十字線，是警示信號，表示趨勢力量衰竭，反轉機率上升。",
              "app":"十字線需配合趨勢和位置判斷。在上漲趨勢高點出現十字線，可考慮減倉或設更嚴格的停損。在下跌趨勢低點出現十字線，是可能觸底的早期暗示。次日收陽可多、次日收陰可空，以次日方向為主要依據。",
              "cau":"十字線單獨出現勝率只有54%，不能作為交易訊號。趨勢強勁時出現十字線只是短暫休息，不代表反轉。必須等待方向確認。"},
     "en":{"def":"A standard Doji has nearly identical open and close prices, forming a cross-like shape with little to no body and shadows of roughly equal length. It represents perfect equilibrium between bulls and bears, signaling maximum market uncertainty.",
           "psy":"The Doji is the purest expression of supply-demand balance. After the open, both sides take turns controlling price, but the market closes right where it started. This pattern often appears when an existing trend loses momentum. A Doji after a sustained rally or decline signals exhaustion and an elevated probability of reversal.",
           "app":"Interpret Doji in context of trend and location. After a strong uptrend, consider reducing longs or tightening stops. After a downtrend, it may hint at a potential bottom. The next candle is decisive: follow with a long if it's bullish, short if bearish.",
           "cau":"A standalone Doji has only a 54% win rate and cannot be used as a trading signal. In a strong trend, a Doji is just a brief pause, not a reversal. Always wait for confirmation."},
     "ja":{"def":"標準的な十字線は始値と終値がほぼ同じで、ほとんど実体がない十字形を形成し、上下のひげの長さはほぼ同じです。強気と弱気の完全なバランスを示し、市場の最大の不確実性を表します。",
           "psy":"十字線は需給の完全なバランスの最も純粋な表現です。寄り付き後、両者が交互に価格を支配しますが、市場は始値と同じ水準で引けます。このパターンは既存トレンドの勢いが衰えたときによく現れます。持続的な上昇または下落後の十字線は消耗を示し、反転確率が高まります。",
           "app":"十字線はトレンドと位置を踏まえて解釈してください。強い上昇トレンド後はロングを減らすかストップを引き上げます。下降トレンド後は底値の可能性を示唆します。次のローソク足が決め手です。",
           "cau":"単独の十字線の勝率はわずか54%で、取引シグナルには使えません。強いトレンド中の十字線は一時的な小休止に過ぎません。常に確認を待ってください。"},
     "ko":{"def":"표준 도지는 시가와 종가가 거의 같아 십자 모양을 형성하며 몸통이 거의 없고 위아래 꼬리 길이가 비슷합니다. 매수와 매도 세력의 완전한 균형을 나타내며 시장의 최대 불확실성을 의미합니다.",
           "psy":"도지는 수급의 완전한 균형의 가장 순수한 표현입니다. 시가 이후 양측이 번갈아 가격을 지배하지만 시장은 시작점에서 마감합니다. 기존 추세의 모멘텀이 소진될 때 자주 나타납니다. 지속적인 상승 또는 하락 후 도지는 소진을 나타내며 반전 확률이 높아집니다.",
           "app":"도지는 추세와 위치를 고려하여 해석하세요. 강한 상승 추세 후에는 롱 축소 또는 손절 강화를 고려하세요. 다음 캔들이 결정적입니다. 강세면 매수, 약세면 공매도를 추종하세요.",
           "cau":"단독 도지의 승률은 54%에 불과하여 거래 신호로 사용할 수 없습니다. 강한 추세 중 도지는 잠시 쉬어가는 것일 뿐입니다. 항상 확인을 기다리세요."},
   }},
  {"id":"hammer","section":"single","signal":"bullish","wr":60,"move":6.0,"rel":"medium","vol":True,
   "svg":[{"o":72,"h":75,"l":15,"c":75,"color":"bull"}],
   "names":{"zh-tw":"錘子線","en":"Hammer","ja":"ハンマー","ko":"해머"},
   "content":{
     "zh-tw":{"def":"錘子線是下影線長（通常是實體的2倍以上）、實體短小位於K棒上方、上影線極短或無的K棒，可以是紅K或黑K。型態出現在下跌趨勢之後，形似一把錘子。",
              "psy":"錘子線代表低點有強力買盤介入。開盤後空頭繼續壓低，但多頭在低點大量買入，把股價從最低點大幅拉升，幾乎收在當日高點。這代表空方力量衰竭，多方在關鍵低點建立防線。下跌趨勢中出現錘子線，說明空頭再也無法有效壓低，底部正在成形。",
              "app":"錘子線必須出現在下跌趨勢的低點才有意義。可於次日確認（出現陽線）後進場做多，停損設在錘子線最低點下方2%。目標看前高或下影線長度的2倍。若出現在MA60/MA120支撐位並配合量能放大，勝率顯著提升至70%以上。",
              "cau":"錘子線出現在上漲趨勢中意義不同（稱為上吊線，是空頭警訊）。紅色錘子線（收盤高於開盤）可信度略高於黑色。必須等次日方向確認再進場，不要在錘子線當天追多。"},
     "en":{"def":"A Hammer has a long lower shadow (typically 2x+ the body), a small body near the top, and little to no upper shadow. It can be bullish or bearish. It appears after a downtrend, resembling a hammer.",
           "psy":"The Hammer signals strong buying support at lows. After the open, bears continue pushing down, but bulls step in aggressively at the low and drive prices back up to near the session high. This indicates bear exhaustion and bull defense at a key low. In a downtrend, the Hammer signals that bears can no longer effectively push lower and a bottom may be forming.",
           "app":"The Hammer is only meaningful at the bottom of a downtrend. Enter long after next-day confirmation (a bullish close), with stop-loss 2% below the hammer's low. Target the prior high or 2x the shadow length. Confluence with MA60/MA120 support and volume expansion pushes win rate above 70%.",
           "cau":"A Hammer in an uptrend has a different meaning (Hanging Man — bearish warning). A red Hammer (close > open) is marginally more reliable. Always wait for next-day confirmation before entering."},
     "ja":{"def":"ハンマーは下ひげが長く（通常は実体の2倍以上）、実体が小さく上部に位置し、上ひげがほとんどないローソク足です。陽線・陰線どちらでも構いません。下降トレンドの後に現れ、形がハンマーに似ています。",
           "psy":"ハンマーは安値での強い買い支えを示します。寄り付き後も売り方が押し下げますが、安値で買い方が積極的に介入し、引けにかけて株価を当日高値近くまで押し上げます。これは弱気の消耗と、重要な安値での強気の防衛を示しています。下降トレンド中のハンマーは底値形成の可能性を示します。",
           "app":"ハンマーは下降トレンドの底でのみ意味があります。翌日に確認（陽線の引け）後にロングで参入し、ストップはハンマーの安値の2%下に設定します。目標は直近高値またはひげの2倍の距離です。MA60/MA120のサポートと出来高増加の合致で勝率が70%以上に向上します。",
           "cau":"上昇トレンド中のハンマーは意味が異なります（首吊り線 — 弱気の警告）。陽のハンマー（終値>始値）はわずかに信頼性が高いです。ハンマーの当日に追いかけて買わず、必ず翌日の確認を待ってから参入してください。"},
     "ko":{"def":"해머는 아래 꼬리가 길고(보통 몸통의 2배 이상), 몸통이 작고 위에 위치하며, 위 꼬리가 거의 없는 캔들입니다. 양봉 또는 음봉 모두 가능합니다. 하락 추세 후에 나타나며 망치처럼 생겼습니다.",
           "psy":"해머는 저점에서의 강한 매수 지지를 나타냅니다. 시가 후 매도 세력이 계속 밀어내지만 매수 세력이 저점에서 적극적으로 개입하여 가격을 당일 고가 근처까지 끌어올립니다. 이는 약세 소진과 핵심 저점에서의 강세 방어를 나타냅니다.",
           "app":"해머는 하락 추세 저점에서만 의미가 있습니다. 다음 날 확인(강세 마감) 후 롱 진입하고 손절은 해머 최저점 2% 아래에 설정합니다. 목표는 이전 고점 또는 꼬리 길이의 2배입니다. MA60/MA120 지지와 거래량 증가가 합쳐지면 승률이 70% 이상으로 높아집니다.",
           "cau":"상승 추세에서의 해머는 다른 의미를 가집니다(행잉맨 — 약세 경고). 빨간 해머(종가>시가)가 약간 더 신뢰할 수 있습니다. 해머 당일에 추격 매수하지 말고 반드시 다음 날 확인을 기다린 후 진입하세요."},
   }},
  {"id":"shooting-star","section":"single","signal":"bearish","wr":66,"move":-6.5,"rel":"medium","vol":True,
   "svg":[{"o":28,"h":85,"l":25,"c":25,"color":"bear"}],
   "names":{"zh-tw":"流星線","en":"Shooting Star","ja":"流れ星","ko":"슈팅스타"},
   "content":{
     "zh-tw":{"def":"流星線出現在上漲趨勢高點，具有長上影線（通常是實體的2倍以上）、小實體位於K棒下方、下影線極短或無。形狀如一顆流星墜落，是空頭反轉的明確警訊。",
              "psy":"流星線代表高點的強力賣壓。盤中多頭把股價推到高點，但空頭在高處猛烈反擊，把多頭的成果全部消化，最終收在低位。這說明高點有大量持股人趁機出貨，買方追高的意願正在快速降溫。上影線越長，代表高點的賣壓越強，反轉訊號越可靠。",
              "app":"流星線出現在上漲趨勢高點，是做空或出多頭倉位的強力訊號（勝率66%）。可在收盤前確認後出場多頭，或次日逢高做空，停損設在上影線最高點。目標看下方支撐或實體延伸1.5倍。配合量能放大可信度更高，是最可靠的頂部型態之一。",
              "cau":"流星線出現在低點（下跌趨勢中）則稱為倒錘線，意義不同（多頭反轉）。必須在明確上漲趨勢的高點才有效。若次日未出現明確陰線，需謹慎，可能是短暫回調後繼續上漲。"},
     "en":{"def":"A Shooting Star appears at the top of an uptrend with a long upper shadow (typically 2x+ the body), a small body near the bottom, and little to no lower shadow. It resembles a shooting star falling, and is a clear bearish reversal warning.",
           "psy":"The Shooting Star signals heavy selling pressure at the highs. Bulls push prices up strongly, but bears counterattack violently at the highs and push all gains back by the close. This indicates heavy distribution by holders and rapidly cooling buyer enthusiasm. The longer the upper shadow, the stronger the selling pressure and the more reliable the reversal signal.",
           "app":"A Shooting Star at the top of an uptrend is a strong signal to short or exit longs (66% win rate). Exit longs on confirmation before close, or short on the next day's strength with a stop above the shadow's high. Target the next support or 1.5x body extension downward. Volume confirmation makes it one of the most reliable topping patterns.",
           "cau":"A Shooting Star at a low is an Inverted Hammer (bullish reversal). Only valid at the top of a clear uptrend. If the next day is not clearly bearish, exercise caution. Two consecutive Shooting Stars create a much stronger bearish signal."},
     "ja":{"def":"流れ星は上昇トレンドの天井に現れ、長い上ひげ（通常は実体の2倍以上）、下部の小さな実体、ほとんどない下ひげを持ちます。落ちる流れ星に似た形で、明確な弱気反転の警告です。",
           "psy":"流れ星は高値での強い売り圧力を示します。強気が価格を高く押し上げますが、弱気が高値で猛烈に反撃し、引けまでに全ての上昇分を消します。これは保有者による大規模な売り逃げと急速に冷える買い意欲を示します。上ひげが長いほど、高値での売り圧力が強く、反転シグナルがより信頼できます。",
           "app":"上昇トレンドの天井での流れ星は売りまたはロング手仕舞いの強力なシグナルです（勝率66%）。確認後に引け前にロングを手仕舞いするか、翌日の高値で売りを建て、ひげの高値にストップを置きます。目標は次のサポートまたは実体の1.5倍の下落です。",
           "cau":"安値での流れ星は逆ハンマー（強気の反転）です。明確な上昇トレンドの天井でのみ有効です。翌日が明確に弱気でない場合は慎重に。"},
     "ko":{"def":"슈팅스타는 상승 추세 고점에서 나타나며 긴 위 꼬리(보통 몸통의 2배 이상), 아래쪽의 작은 몸통, 거의 없는 아래 꼬리를 가집니다. 떨어지는 유성처럼 생겼으며 명확한 약세 반전 경고입니다.",
           "psy":"슈팅스타는 고점에서의 강한 매도 압박을 나타냅니다. 매수 세력이 가격을 강하게 올리지만 매도 세력이 고점에서 격렬하게 반격하여 종가까지 모든 상승분을 되돌립니다. 위 꼬리가 길수록 고점의 매도 압박이 강하고 반전 신호가 더 신뢰할 수 있습니다.",
           "app":"상승 추세 고점에서 슈팅스타는 공매도 또는 롱 청산의 강력한 신호입니다(승률 66%). 확인 후 종가 전 롱을 청산하거나 다음 날 고점에서 공매도하고 손절은 위 꼬리 최고점 위에 설정합니다.",
           "cau":"저점에서의 슈팅스타는 역해머(강세 반전)입니다. 명확한 상승 추세의 고점에서만 유효합니다. 다음 날 명확한 약세가 없으면 주의가 필요합니다."},
   }},
  {"id":"morning-star","section":"combo","signal":"bullish","wr":72,"move":10.2,"rel":"high","vol":True,
   "svg":[{"o":75,"h":78,"l":48,"c":50,"color":"bear"},{"o":42,"h":47,"l":35,"c":40,"color":"neutral"},{"o":45,"h":82,"l":43,"c":80,"color":"bull"}],
   "names":{"zh-tw":"晨星","en":"Morning Star","ja":"明けの明星","ko":"모닝스타"},
   "content":{
     "zh-tw":{"def":"晨星是三根K棒組成的多頭反轉型態：第一根大陰線（延續下跌）、第二根跳空向下的小實體K棒（多空猶豫）、第三根大陽線（多頭反攻，收盤深入第一根陰線實體的一半以上）。",
              "psy":"晨星完整呈現了市場底部反轉的心理過程。第一根大陰線代表空頭最後的強力進攻，第二根小K棒跳空低開代表賣壓耗盡，多空均不確定接下來的方向。第三根大陽線代表多頭大舉反攻，宣告空頭徹底失敗，底部正式形成。",
              "app":"晨星是最可靠的底部反轉型態之一（勝率72%），適合在第三根大陽線收盤後進場做多。停損設在第二根K棒（星）的最低點下方。目標看前高或下跌幅度的50%~61.8%回測。第三根量能放大是最關鍵的確認。",
              "cau":"晨星的三根K棒需在下跌趨勢的低點出現才有效。第三根大陽線必須至少收回第一根陰線實體的50%才算有效晨星。整體空頭市場中的晨星可能只是熊市反彈，需配合量能和均線確認。"},
     "en":{"def":"The Morning Star is a three-candle bullish reversal pattern: a large bearish candle (continuing the downtrend), a small-body candle gapping down (indecision), and a large bullish candle (closing more than halfway into the first bearish candle's body).",
           "psy":"The Morning Star illustrates the complete psychological process of a market bottom. The first large bearish candle is the bears' final powerful push. The second small candle gapping down signals exhausted selling. The third large bullish candle is bulls' counter-offensive, reclaiming territory and declaring a confirmed bottom.",
           "app":"The Morning Star is one of the most reliable bottom reversal patterns (72% win rate). Enter long after the third bullish candle closes. Stop-loss below the second candle's (the star's) low. Target the prior high or 50–61.8% retracement of the decline. Volume on the third candle is the most critical confirmation.",
           "cau":"All three candles must appear at the low of a downtrend. The third candle must close at least 50% into the first candle's body. In an overall bear market, this may signal only a bear market bounce."},
     "ja":{"def":"明けの明星は3本のローソク足で構成される強気反転パターンです：大陰線（下降トレンドの継続）、下方向に窓を開けた小実体のローソク足（迷い）、大陽線（最初の陰線実体の半分以上まで入り込む）。",
           "psy":"明けの明星は市場の底値反転の心理過程を完全に示しています。最初の大陰線は売り方の最後の強力な攻撃です。2本目は売り圧力の消耗を示します。3本目の大陽線は強気の大反撃で、底値の確認を宣告します。",
           "app":"明けの明星は最も信頼できる底値反転パターンの一つです（勝率72%）。3本目の大陽線の引けでロングに参入します。ストップは2本目（星）の安値の下に設定します。目標は直近高値または下落幅の50〜61.8%戻しです。",
           "cau":"3本のローソク足は下降トレンドの底で出現する必要があります。3本目は最初の陰線の実体の少なくとも50%まで入り込む必要があります。全体的な弱気市場では一時的な戻りのみかもしれません。"},
     "ko":{"def":"모닝스타는 세 캔들로 구성된 강세 반전 패턴입니다: 대형 음봉(하락 추세 지속), 아래로 갭이 생긴 작은 몸통의 캔들(우유부단), 대형 양봉(첫 번째 음봉 몸통의 절반 이상을 되돌림).",
           "psy":"모닝스타는 시장 바닥 반전의 완전한 심리 과정을 보여줍니다. 첫 번째 대형 음봉은 약세 세력의 마지막 강력한 공세입니다. 두 번째 작은 캔들의 아래 갭은 매도 소진을 나타냅니다. 세 번째 대형 양봉은 강세 세력의 대반격으로 바닥 확인을 선언합니다.",
           "app":"모닝스타는 가장 신뢰할 수 있는 바닥 반전 패턴 중 하나입니다(승률 72%). 세 번째 양봉 마감 후 롱 진입합니다. 손절은 두 번째 캔들(별)의 최저점 아래에 설정합니다.",
           "cau":"세 캔들 모두 하락 추세의 저점에서 나타나야 합니다. 세 번째 캔들이 첫 번째 음봉 몸통의 50% 이상을 되돌려야 유효합니다."},
   }},
  {"id":"evening-star","section":"combo","signal":"bearish","wr":69,"move":-9.8,"rel":"high","vol":True,
   "svg":[{"o":25,"h":52,"l":23,"c":50,"color":"bull"},{"o":58,"h":65,"l":55,"c":60,"color":"neutral"},{"o":55,"h":57,"l":20,"c":22,"color":"bear"}],
   "names":{"zh-tw":"暮星","en":"Evening Star","ja":"宵の明星","ko":"이브닝스타"},
   "content":{
     "zh-tw":{"def":"暮星是三根K棒組成的空頭反轉型態：第一根大陽線（延續上漲）、第二根跳空向上的小實體K棒（多頭猶豫）、第三根大陰線（空頭反攻，收盤深入第一根陽線實體的一半以上）。是晨星的鏡像型態。",
              "psy":"暮星呈現市場頂部形成的完整心理過程。第一根大陽線是多頭最後的強力推升，第二根小K棒跳空高開但無法繼續上漲，代表多頭力量耗盡。第三根大陰線是空頭大舉反攻，宣告多頭徹底失敗，高點正式確認。",
              "app":"暮星是最可靠的頂部反轉型態之一（勝率69%）。可在第三根大陰線收盤後出場多頭或做空，停損設在第二根K棒（星）的最高點上方。目標看前低或上漲幅度的50%~61.8%回測。",
              "cau":"暮星必須出現在上漲趨勢的高點。第三根大陰線必須至少深入第一根陽線實體的50%。在整體多頭市場中暮星可能只是高點休整，需配合量能和均線確認是否真正反轉。"},
     "en":{"def":"The Evening Star is a three-candle bearish reversal pattern: a large bullish candle (continuing the uptrend), a small-body candle gapping up (bull exhaustion), and a large bearish candle (closing more than halfway into the first bullish candle's body).",
           "psy":"The Evening Star illustrates the complete psychological process of a market top. The first large bullish candle is bulls' final powerful push. The second small candle gaps up but fails to extend the rally. The third large bearish candle declares a complete bullish failure and confirms the top.",
           "app":"The Evening Star is one of the most reliable topping reversal patterns (69% win rate). Exit longs or short after the third bearish candle closes. Stop-loss above the second candle's (the star's) high. Target the prior low or 50–61.8% retracement of the rally.",
           "cau":"The Evening Star must appear at the top of an uptrend. The third candle must close at least 50% into the first candle's body. In an overall bull market, this may only signal a top-level consolidation."},
     "ja":{"def":"宵の明星は3本のローソク足で構成される弱気反転パターンです：大陽線（上昇トレンドの継続）、上方向に窓を開けた小実体のローソク足（強気の消耗）、大陰線（最初の陽線実体の半分以上まで入り込む）。明けの明星の鏡像パターンです。",
           "psy":"宵の明星は市場の天井形成の完全な心理過程を示しています。最初の大陽線は買い方の最後の強力な押し上げです。2本目は高く窓を開けますが上昇を継続できず、強気の消耗を示します。3本目の大陰線は強気の完全な失敗と天井を宣告します。",
           "app":"宵の明星は最も信頼できる天井反転パターンの一つです（勝率69%）。3本目の大陰線の引けでロングを手仕舞いするか売りを建てます。ストップは2本目（星）の高値の上に設定します。",
           "cau":"宵の明星は上昇トレンドの天井に出現する必要があります。3本目は最初の陽線の実体の少なくとも50%まで入り込む必要があります。"},
     "ko":{"def":"이브닝스타는 세 캔들로 구성된 약세 반전 패턴입니다: 대형 양봉(상승 추세 지속), 위로 갭이 생긴 작은 몸통의 캔들(강세 소진), 대형 음봉(첫 번째 양봉 몸통의 절반 이상을 되돌림). 모닝스타의 거울 이미지입니다.",
           "psy":"이브닝스타는 시장 천장 형성의 완전한 심리 과정을 보여줍니다. 첫 번째 대형 양봉은 강세 세력의 마지막 강력한 밀어올림입니다. 두 번째 캔들이 높게 갭이 생기지만 상승을 이어가지 못합니다. 세 번째 대형 음봉은 강세의 완전한 실패와 천장 확인을 선언합니다.",
           "app":"이브닝스타는 가장 신뢰할 수 있는 천장 반전 패턴 중 하나입니다(승률 69%). 세 번째 음봉 마감 후 롱 청산 또는 공매도합니다.",
           "cau":"이브닝스타는 상승 추세의 고점에서 나타나야 합니다. 세 번째 캔들이 첫 번째 양봉 몸통의 50% 이상을 되돌려야 합니다."},
   }},
  {"id":"bullish-engulfing","section":"combo","signal":"bullish","wr":63,"move":8.5,"rel":"medium","vol":True,
   "svg":[{"o":65,"h":68,"l":38,"c":40,"color":"bear"},{"o":35,"h":80,"l":33,"c":78,"color":"bull"}],
   "names":{"zh-tw":"多頭吞噬","en":"Bullish Engulfing","ja":"陽の包み足","ko":"강세 장악형"},
   "content":{
     "zh-tw":{"def":"多頭吞噬是由兩根K棒組成的反轉型態：第一根是黑K（下跌），第二根是紅K，且紅K的實體完全包住（吞噬）黑K的實體，即紅K開盤低於黑K收盤、紅K收盤高於黑K開盤。出現在下跌趨勢後。",
              "psy":"多頭吞噬代表多空力量的戲劇性逆轉。第一根黑K延續空頭優勢，但第二根紅K的多頭不只守住前日跌幅，還強力反攻，完全消化了空頭的成果。更開低後更高的收盤代表強力軋空，或是低點吸引大量新資金進場，共識快速反轉。",
              "app":"多頭吞噬出現在下跌趨勢的低點，是可靠的多頭反轉訊號（勝率63%）。可在吞噬紅K收盤後進場做多，停損設在吞噬型態最低點下方2%。目標看前高或吞噬實體大小的1.5倍。搭配成交量放大可信度大幅提升。",
              "cau":"多頭吞噬必須出現在明確的下跌趨勢後，在盤整區或上漲趨勢中出現意義有限。第二根K棒須完整包住第一根實體（僅影線吞噬不算）。"},
     "en":{"def":"Bullish Engulfing is a two-candle reversal pattern: a bearish candle followed by a bullish candle whose body completely engulfs the prior body. Appears after a downtrend.",
           "psy":"Bullish Engulfing signals a dramatic reversal of forces. The first bearish candle continues the downtrend, but the second bullish candle's buyers not only defend the losses but launch a powerful counter-attack, fully absorbing the bears' gains.",
           "app":"Bullish Engulfing at the low of a downtrend is a reliable bullish reversal signal (63% win rate). Enter long after the engulfing candle closes, with stop-loss 2% below the pattern's low. Volume confirmation (second candle 1.5x+ first candle volume) significantly improves reliability.",
           "cau":"Bullish Engulfing must appear after a clear downtrend. The second candle must fully engulf the first body (shadow engulfing doesn't count). In a major bear trend, this signals a temporary bounce only."},
     "ja":{"def":"陽の包み足は2本のローソク足で構成される反転パターンです：最初は陰線、次に陽線が続き、陽線の実体が前の陰線の実体を完全に包みます。下降トレンドの後に出現します。",
           "psy":"陽の包み足は力の劇的な逆転を示します。最初の陰線は下降トレンドを継続しますが、次の陽線の買い方は強力な反撃を開始し、売り方の成果を完全に消します。",
           "app":"下降トレンドの底での陽の包み足は信頼できる強気反転シグナルです（勝率63%）。包み足の引けでロングに参入し、ストップはパターンの安値の2%下に設定します。",
           "cau":"陽の包み足は明確な下降トレンドの後に出現する必要があります。2本目は1本目の実体を完全に包む必要があります。"},
     "ko":{"def":"강세 장악형은 두 캔들로 구성된 반전 패턴입니다: 음봉 후 양봉이 이전 음봉의 몸통을 완전히 감쌉니다. 하락 추세 후 나타납니다.",
           "psy":"강세 장악형은 세력의 극적인 반전을 나타냅니다. 첫 번째 음봉이 하락 추세를 지속하지만 두 번째 양봉의 매수 세력이 강력한 반격을 시작하여 약세 세력의 성과를 완전히 흡수합니다.",
           "app":"하락 추세 저점에서 강세 장악형은 신뢰할 수 있는 강세 반전 신호입니다(승률 63%). 장악 캔들 마감 후 롱 진입하고 손절은 패턴 최저점 2% 아래에 설정합니다.",
           "cau":"강세 장악형은 명확한 하락 추세 후에 나타나야 합니다. 두 번째 캔들이 첫 번째 몸통을 완전히 감싸야 합니다."},
   }},
  {"id":"three-white-soldiers","section":"combo","signal":"bullish","wr":78,"move":12.4,"rel":"high","vol":True,
   "svg":[{"o":20,"h":48,"l":18,"c":45,"color":"bull"},{"o":47,"h":68,"l":45,"c":65,"color":"bull"},{"o":67,"h":90,"l":65,"c":88,"color":"bull"}],
   "names":{"zh-tw":"三白兵","en":"Three White Soldiers","ja":"赤三兵","ko":"적삼병"},
   "content":{
     "zh-tw":{"def":"三白兵是連續三根大陽線，每根K棒的開盤接近前一根的收盤附近，且每根收盤都高於前一根收盤。三根都是長實體、幾乎無上下影線，代表多頭持續且強力地推升價格。",
              "psy":"三白兵是多頭最強力的延續型態之一，展示買方的持續主導。第一根大陽線引發關注，第二根確認多頭方向，第三根代表市場廣泛認同這個上漲走勢，大量資金持續流入。",
              "app":"三白兵出現在下跌後的低點，是最可靠的多頭反轉訊號（勝率78%）。出現後可積極追多，停損設在第一根陽線最低點下方。若出現在盤整突破後，目標看前高或三根陽線總高度的1.5倍。",
              "cau":"三白兵若出現在已大漲後的高點（上漲超過30%），反而是過熱警訊，很快會出現回調。每根K棒的量能應逐步放大，若第三根量縮代表追高者動能不足。"},
     "en":{"def":"Three White Soldiers consists of three consecutive large bullish candles, each opening near the prior close and closing higher. All three have long bodies with little to no shadows, signaling sustained and powerful buying.",
           "psy":"Three White Soldiers is one of the strongest continuation patterns, showing persistent buyer dominance. The first candle draws attention, the second confirms direction, and the third shows broad market agreement with strong capital inflows.",
           "app":"Three White Soldiers at the bottom of a downtrend is one of the most reliable bullish reversal signals (78% win rate). Aggressively enter long after the third candle closes. Volume should expand with each candle for best confirmation.",
           "cau":"Three White Soldiers after a large rally (30%+ already) signals overheating. Volume should expand with each candle — if the third has lower volume, the rally is losing momentum."},
     "ja":{"def":"赤三兵は連続する3本の大陽線で構成され、それぞれが前の終値近くで寄り付き、前の終値より高く引けます。3本すべてが長い実体でほとんどひげがなく、持続的で力強い買いを示します。",
           "psy":"赤三兵は最も強力な継続パターンの一つで、持続的な買い手の優位性を示します。1本目が注目を集め、2本目が方向を確認し、3本目は市場の広範な合意と強い資金流入を示します。",
           "app":"下降トレンドの底での赤三兵は最も信頼できる強気反転シグナルの一つです（勝率78%）。3本目の引けでロングに積極的に参入します。",
           "cau":"大幅上昇後の高値圏での赤三兵は過熱の警告です。各ローソク足で出来高が増加すべきで、3本目の出来高が少ない場合は上昇モメンタムが弱まっています。"},
     "ko":{"def":"적삼병은 연속된 세 개의 대형 양봉으로 구성되며, 각각이 이전 종가 근처에서 시작하여 이전 종가보다 높게 마감합니다. 세 개 모두 긴 몸통에 꼬리가 거의 없어 지속적이고 강력한 매수를 나타냅니다.",
           "psy":"적삼병은 가장 강력한 지속 패턴 중 하나로 지속적인 매수 세력의 우위를 보여줍니다. 첫 번째 캔들이 주목을 끌고, 두 번째가 방향을 확인하며, 세 번째는 강한 자금 유입과 함께 시장의 광범위한 합의를 보여줍니다.",
           "app":"하락 추세 저점에서 적삼병은 가장 신뢰할 수 있는 강세 반전 신호 중 하나입니다(승률 78%). 세 번째 캔들 마감 후 적극적으로 롱 진입합니다.",
           "cau":"큰 상승 후 고점(30% 이상 상승 후)에서의 적삼병은 과열 경고로 곧 조정이 옵니다. 각 캔들에서 거래량이 증가해야 합니다."},
   }},
  {"id":"three-black-crows","section":"combo","signal":"bearish","wr":76,"move":-11.9,"rel":"high","vol":True,
   "svg":[{"o":82,"h":84,"l":60,"c":62,"color":"bear"},{"o":60,"h":62,"l":38,"c":40,"color":"bear"},{"o":38,"h":40,"l":15,"c":17,"color":"bear"}],
   "names":{"zh-tw":"三黑鴉","en":"Three Black Crows","ja":"黒三兵","ko":"흑삼병"},
   "content":{
     "zh-tw":{"def":"三黑鴉是連續三根大陰線，每根K棒的開盤接近前一根的收盤附近，且每根收盤都低於前一根收盤。三根都是長實體、幾乎無上下影線，代表空頭持續且強力地壓低價格。",
              "psy":"三黑鴉是空頭最強力的延續型態之一。第一根大陰線引發警覺，第二根確認空頭方向，第三根代表市場廣泛認同下跌走勢，恐慌性賣出持續蔓延。",
              "app":"三黑鴉出現在高點，是最可靠的空頭反轉訊號（勝率76%）。可在第三根收盤後出場多頭或做空，停損設在第一根陰線最高點上方。目標看前低或三根陰線總高度的1.5倍向下延伸。",
              "cau":"三黑鴉若出現在已大跌後的低點，反而可能是最後殺盤後見底，不宜追空。每根量能應逐步放大，若第三根量縮代表追空動能不足。"},
     "en":{"def":"Three Black Crows consists of three consecutive large bearish candles, each opening near the prior close and closing lower. All three have long bodies with little to no shadows, signaling sustained and powerful selling.",
           "psy":"Three Black Crows is one of the strongest bearish continuation patterns. The first bearish candle triggers alarm, the second confirms direction, and the third shows broad market agreement with spreading panic selling.",
           "app":"Three Black Crows at a high is one of the most reliable bearish reversal signals (76% win rate). Exit longs or short after the third candle closes. Shorting on a bounce to near the second candle's high offers better risk-reward.",
           "cau":"Three Black Crows after a large decline may signal final capitulation before a bottom. Volume should expand with each candle; lower volume on the third signals weakening bearish momentum."},
     "ja":{"def":"黒三兵は連続する3本の大陰線で構成され、それぞれが前の終値近くで寄り付き、前の終値より低く引けます。3本すべてが長い実体でほとんどひげがなく、持続的で力強い売りを示します。",
           "psy":"黒三兵は最も強力な弱気継続パターンの一つです。1本目の大陰線が警戒を引き起こし、2本目が方向を確認し、3本目はパニック売りが広がる中で市場の広範な合意を示します。",
           "app":"高値圏での黒三兵は最も信頼できる弱気反転シグナルの一つです（勝率76%）。3本目の引けでロングを手仕舞いするか売りを建てます。",
           "cau":"大幅下落後の安値圏での黒三兵は底打ち前の最終的な投げ売りの可能性があります。追い売りは避けてください。"},
     "ko":{"def":"흑삼병은 연속된 세 개의 대형 음봉으로 구성되며, 각각이 이전 종가 근처에서 시작하여 이전 종가보다 낮게 마감합니다. 세 개 모두 긴 몸통에 꼬리가 거의 없어 지속적이고 강력한 매도를 나타냅니다.",
           "psy":"흑삼병은 가장 강력한 약세 지속 패턴 중 하나입니다. 첫 번째 음봉이 경보를 유발하고, 두 번째가 방향을 확인하며, 세 번째는 공황 매도가 확산되는 가운데 시장의 광범위한 합의를 보여줍니다.",
           "app":"고점에서 흑삼병은 가장 신뢰할 수 있는 약세 반전 신호 중 하나입니다(승률 76%). 세 번째 캔들 마감 후 롱 청산 또는 공매도합니다.",
           "cau":"큰 하락 후 저점에서 흑삼병은 바닥 전 마지막 투매일 수 있으니 추격 공매도는 피하세요."},
   }},
  # Head & Shoulders
  {"id":"head-shoulders-top","section":"reversal","signal":"bearish","wr":74,"move":-15.0,"rel":"high","vol":True,
   "svg":[{"o":30,"h":50,"l":28,"c":48,"color":"bull"},{"o":49,"h":70,"l":35,"c":37,"color":"bear"},{"o":38,"h":60,"l":36,"c":57,"color":"bull"},{"o":58,"h":85,"l":44,"c":46,"color":"bear"},{"o":47,"h":58,"l":29,"c":31,"color":"bear"}],
   "names":{"zh-tw":"頭肩頂","en":"Head & Shoulders Top","ja":"ヘッドアンドショルダートップ","ko":"헤드앤숄더 천장형"},
   "content":{
     "zh-tw":{"def":"頭肩頂是由左肩、頭部、右肩三個高點組成的頂部反轉型態。左肩和右肩高度相近，頭部最高。三個高點底部的連線稱為「頸線」，當價格跌破頸線時，確認反轉完成。是最經典的頂部反轉型態之一。",
              "psy":"頭肩頂展現多頭力量逐步衰竭的過程。左肩代表多頭第一次推升受阻回落。頭部代表多頭再度嘗試突破創新高，但隨即遭到更強力的賣壓打回。右肩代表多頭第三次反彈，但已無力再創頭部高點，賣方在更低的位置就開始出貨。跌破頸線代表多空易位完成。",
              "app":"頭肩頂確認進場點是跌破頸線時，可做空或出場多頭，停損設在右肩高點上方。目標距離=頭部到頸線的垂直距離，從跌破頸線點向下量。若頸線為斜線，以跌破點為準。可等待回測頸線後再入場，風險報酬更佳。",
              "cau":"頭肩頂必須在日線或週線圖上形成才有效，分鐘圖的頭肩頂可靠性低。右肩的成交量應比左肩縮小，頭部成交量最大。若右肩比頭部還高，則型態失敗。頸線若是向上傾斜，可靠性高於向下傾斜。"},
     "en":{"def":"Head & Shoulders Top is a classic topping reversal pattern consisting of a left shoulder, a head (the highest point), and a right shoulder. The line connecting the lows of each peak is called the neckline. A confirmed breakdown occurs when price closes below the neckline.",
           "psy":"H&S Top shows progressively exhausting bullish momentum. The left shoulder shows the first rejection. The head is bulls' final attempt at a new high — immediately met by stronger selling. The right shoulder shows bulls' third attempt, failing to reach the head's high as sellers begin distributing at lower levels. Breaking the neckline confirms the reversal.",
           "app":"Enter short or exit longs on a confirmed close below the neckline. Stop-loss above the right shoulder. Target = vertical distance from head to neckline, projected downward from the breakout point. Waiting for a neckline retest offers better risk-reward.",
           "cau":"H&S Top must form on a daily or weekly chart. Volume should be highest at the head, lower at the right shoulder. If the right shoulder exceeds the head's high, the pattern fails. An upward-sloping neckline is more reliable than a downward-sloping one."},
     "ja":{"def":"ヘッドアンドショルダートップは左肩、頭（最高点）、右肩の3つの高値で構成される典型的な天井打ち反転パターンです。各高値の安値を結んだ線をネックラインと呼び、価格がネックラインを割り込んだときに反転が確認されます。",
           "psy":"H&Sトップは強気モメンタムの段階的な消耗を示します。左肩は最初の拒絶を示します。頭は強気の最後の新高値の試みで、すぐに強い売りに遭います。右肩は強気の3回目の試みで、頭の高値に届かず、売り方がより低い水準で分散を始めています。",
           "app":"ネックライン割れの確定で売りまたはロング手仕舞いに参入します。ストップは右肩の高値の上に設定します。目標＝頭からネックラインまでの垂直距離をブレイクアウト点から下方に投影します。",
           "cau":"H&Sトップは日足または週足チャートで形成される必要があります。右肩の出来高は左肩より少ないべきです。右肩が頭の高値を超えた場合、パターンは無効です。"},
     "ko":{"def":"헤드앤숄더 천장형은 왼쪽 어깨, 머리(최고점), 오른쪽 어깨로 구성된 전형적인 천장 반전 패턴입니다. 각 고점의 저점을 연결한 선을 넥라인이라고 하며 가격이 넥라인 아래로 확정 마감하면 반전이 확인됩니다.",
           "psy":"헤드앤숄더 천장형은 단계적으로 소진되는 강세 모멘텀을 보여줍니다. 왼쪽 어깨는 첫 번째 거부를 나타냅니다. 머리는 강세의 마지막 신고점 시도로 즉시 강한 매도를 만납니다. 오른쪽 어깨는 강세의 세 번째 시도로 머리 고점에 도달하지 못합니다.",
           "app":"넥라인 이탈 확정 시 공매도 또는 롱 청산에 진입합니다. 손절은 오른쪽 어깨 고점 위에 설정합니다. 목표 = 머리에서 넥라인까지의 수직 거리를 돌파점에서 아래로 투영합니다.",
           "cau":"헤드앤숄더는 일봉 또는 주봉 차트에서 형성되어야 합니다. 오른쪽 어깨의 거래량은 왼쪽 어깨보다 적어야 합니다. 오른쪽 어깨가 머리의 고점을 넘으면 패턴이 무효입니다."},
   }},
  {"id":"inverse-head-shoulders","section":"reversal","signal":"bullish","wr":73,"move":15.5,"rel":"high","vol":True,
   "svg":[{"o":70,"h":72,"l":50,"c":52,"color":"bear"},{"o":51,"h":65,"l":30,"c":63,"color":"bull"},{"o":62,"h":65,"l":40,"c":43,"color":"bear"},{"o":44,"h":63,"l":15,"c":61,"color":"bull"},{"o":60,"h":72,"l":42,"c":70,"color":"bull"}],
   "names":{"zh-tw":"頭肩底","en":"Inverse Head & Shoulders","ja":"逆ヘッドアンドショルダー","ko":"역 헤드앤숄더"},
   "content":{
     "zh-tw":{"def":"頭肩底是頭肩頂的鏡像型態，由左肩、頭部（最低點）、右肩三個低點組成。頸線為三個低點頂部的連線，當價格突破頸線時確認底部反轉完成。是最可靠的底部反轉型態之一。",
              "psy":"頭肩底展現空頭力量逐步衰竭的過程。左肩代表空頭第一次壓低後反彈。頭部代表空頭再度嘗試創新低，但隨即遭到強烈買盤反彈。右肩代表空頭第三次下探，但已無力再創頭部低點，多方在更高的位置就開始積極承接。突破頸線代表多空易位完成。",
              "app":"頭肩底確認進場點是突破頸線時，可做多或出場空頭，停損設在右肩低點下方。目標距離=頭部到頸線的垂直距離，從突破頸線點向上量。突破頸線時配合成交量放大，可信度大幅提升。",
              "cau":"頭肩底必須在日線或週線圖上形成才有效。右肩底部應比左肩稍高（代表底部已抬高）。突破頸線後若快速跌回頸線下方，代表假突破，應止損出場。"},
     "en":{"def":"Inverse Head & Shoulders is the mirror image of H&S Top: three lows forming a left shoulder, head (the deepest low), and right shoulder. A confirmed breakout occurs when price closes above the neckline, completing the bottom reversal.",
           "psy":"Inverse H&S shows progressively exhausting bearish momentum. The left shoulder is the first low and bounce. The head is bears' deepest push, met immediately by strong buying. The right shoulder shows bears' third attempt, failing to reach the head's low as buyers step in higher. Breaking the neckline confirms the reversal.",
           "app":"Enter long or exit shorts on a confirmed close above the neckline. Stop-loss below the right shoulder's low. Target = vertical distance from head to neckline, projected upward. Volume expansion on the breakout significantly increases reliability.",
           "cau":"Must form on a daily or weekly chart. The right shoulder low should be slightly higher than the left (rising bottom). A quick return below the neckline after breakout signals a false breakout — exit immediately."},
     "ja":{"def":"逆ヘッドアンドショルダーはH&Sトップの鏡像パターンです：左肩、頭（最も深い安値）、右肩の3つの安値で構成されます。価格がネックラインを上抜けたときに底値反転が確認されます。",
           "psy":"逆H&Sは段階的に消耗する弱気モメンタムを示します。左肩は最初の安値と反発です。頭は弱気の最も深い押しで、すぐに強い買いに遭います。右肩は弱気の3回目の試みで、頭の安値に届かず、買い方がより高い水準で積極的に参入します。",
           "app":"ネックライン上抜けの確定でロングまたは空売りの手仕舞いに参入します。ストップは右肩安値の下に設定します。出来高増加のブレイクアウトで信頼性が大幅に向上します。",
           "cau":"日足または週足チャートで形成される必要があります。右肩の安値は左肩よりわずかに高いべきです（底値の切り上がり）。ブレイクアウト後にネックライン下に戻った場合はダマシです。"},
     "ko":{"def":"역 헤드앤숄더는 헤드앤숄더 천장형의 거울 이미지입니다: 왼쪽 어깨, 머리(가장 낮은 저점), 오른쪽 어깨의 세 저점으로 구성됩니다. 가격이 넥라인 위로 확정 마감하면 바닥 반전이 확인됩니다.",
           "psy":"역 헤드앤숄더는 단계적으로 소진되는 약세 모멘텀을 보여줍니다. 왼쪽 어깨는 첫 번째 저점과 반등입니다. 머리는 약세 세력의 가장 깊은 하락으로 즉시 강한 매수를 만납니다. 오른쪽 어깨는 약세의 세 번째 시도로 머리의 저점에 도달하지 못합니다.",
           "app":"넥라인 돌파 확정 시 롱 진입 또는 공매도 청산합니다. 손절은 오른쪽 어깨 저점 아래에 설정합니다. 거래량 증가를 동반한 돌파는 신뢰도를 크게 높입니다.",
           "cau":"일봉 또는 주봉 차트에서 형성되어야 합니다. 오른쪽 어깨 저점이 왼쪽 어깨보다 약간 높아야 합니다(바닥 상승). 돌파 후 넥라인 아래로 빠르게 복귀하면 가짜 돌파이니 즉시 청산하세요."},
   }},
  # Continuation patterns
  {"id":"flag-bull","section":"continuation","signal":"bullish","wr":67,"move":11.5,"rel":"high","vol":True,
   "svg":[{"o":15,"h":40,"l":13,"c":38,"color":"bull"},{"o":39,"h":45,"l":30,"c":32,"color":"bear"},{"o":33,"h":38,"l":28,"c":30,"color":"bear"},{"o":31,"h":55,"l":29,"c":52,"color":"bull"}],
   "names":{"zh-tw":"多頭旗型","en":"Bull Flag","ja":"強気フラッグ","ko":"강세 깃발형"},
   "content":{
     "zh-tw":{"def":"多頭旗型由兩部分組成：旗桿（急速大幅上漲的K棒）和旗面（小幅度的平行通道下跌整理）。整理期間量縮，突破旗面上緣時量增，代表上漲趨勢延續。",
              "psy":"多頭旗型是上漲中的正常獲利了結整理。急速上漲吸引大批買家後，短線獲利者賣出，形成小幅回調的旗面。但回調量縮代表賣方力道有限，持股信心仍在。突破旗面上緣放量代表新資金認同趨勢，繼續追買，趨勢加速延續。",
              "app":"多頭旗型的進場點為突破旗面上緣時，配合量能放大確認。停損設在旗面最低點下方。目標距離=旗桿長度，從突破點向上量。是趨勢交易中最常用的型態之一，勝率67%。",
              "cau":"旗面的回調幅度不應超過旗桿的50%，否則可能不是旗型而是更深的回調。旗面整理時間不宜過長（超過20根K棒要謹慎），時間過長代表趨勢力道不足。量縮是旗面的必要條件，量不縮則可靠性下降。"},
     "en":{"def":"Bull Flag consists of a flagpole (a sharp, strong rally) followed by a flag (a slight downward parallel channel consolidation with declining volume). A breakout above the upper flag boundary on increased volume signals trend continuation.",
           "psy":"The Bull Flag is a normal profit-taking consolidation within an uptrend. After a sharp rally attracts buyers, short-term traders sell, forming a slight pullback. Declining volume during the flag shows limited selling pressure and sustained holder confidence. A volume-accompanied breakout signals new money agreeing with the trend.",
           "app":"Enter long on a confirmed breakout above the upper flag boundary with volume. Stop-loss below the flag's low. Target = flagpole length projected upward from breakout. One of the most reliable continuation patterns with a 67% win rate.",
           "cau":"The flag's pullback should not exceed 50% of the flagpole — deeper corrections may signal something more significant. Flag consolidation lasting more than 20 candles suggests insufficient trend momentum. Declining volume during the flag is essential — without it, reliability drops."},
     "ja":{"def":"強気フラッグはフラッグポール（急速で力強い上昇）とフラッグ（出来高が縮小する中での緩やかな下向き平行チャンネルの保ち合い）で構成されます。出来高を伴ってフラッグの上限を上抜けするとトレンドの継続を示します。",
           "psy":"強気フラッグは上昇トレンド内の通常の利確調整です。急速な上昇が買い手を引き付けた後、短期トレーダーが売り、緩やかな押し目を形成します。フラッグ中の出来高縮小は売り圧力の限られさと保有者の信頼の持続を示します。",
           "app":"フラッグ上限のブレイクアウトに出来高を伴って確認でロングに参入します。ストップはフラッグの安値の下に設定します。目標＝フラッグポールの長さをブレイクアウト点から上方に投影します。",
           "cau":"フラッグの押し目はフラッグポールの50%を超えるべきではありません。フラッグの保ち合いが20本以上続くとトレンドモメンタムが不十分なことを示します。フラッグ中の出来高縮小は必須条件です。"},
     "ko":{"def":"강세 깃발형은 깃대(급격하고 강한 상승)와 깃발(거래량 감소를 동반한 완만한 하향 평행 채널 횡보)로 구성됩니다. 거래량 증가와 함께 깃발 상단 경계 돌파 시 추세 지속을 나타냅니다.",
           "psy":"강세 깃발형은 상승 추세 내의 정상적인 차익 실현 조정입니다. 급격한 상승이 매수자를 끌어들인 후 단기 트레이더들이 매도하여 완만한 되돌림을 형성합니다. 깃발 중 거래량 감소는 제한적인 매도 압박과 지속되는 보유자 확신을 나타냅니다.",
           "app":"깃발 상단 경계 돌파 확인 시 거래량과 함께 롱 진입합니다. 손절은 깃발 최저점 아래에 설정합니다. 목표 = 깃대 길이를 돌파점에서 위로 투영합니다.",
           "cau":"깃발의 되돌림이 깃대의 50%를 초과하면 안 됩니다. 깃발 횡보가 20개 이상의 캔들이 지속되면 추세 모멘텀이 부족함을 나타냅니다. 깃발 중 거래량 감소는 필수 조건입니다."},
   }},
  {"id":"cup-handle","section":"continuation","signal":"bullish","wr":65,"move":22.0,"rel":"high","vol":True,
   "svg":[{"o":75,"h":78,"l":55,"c":57,"color":"bear"},{"o":56,"h":60,"l":30,"c":32,"color":"bear"},{"o":31,"h":35,"l":28,"c":33,"color":"neutral"},{"o":34,"h":60,"l":32,"c":57,"color":"bull"},{"o":56,"h":73,"l":50,"c":52,"color":"bear"},{"o":53,"h":80,"l":51,"c":78,"color":"bull"}],
   "names":{"zh-tw":"杯柄型態","en":"Cup & Handle","ja":"カップウィズハンドル","ko":"컵앤핸들"},
   "content":{
     "zh-tw":{"def":"杯柄型態由兩部分組成：杯身（圓弧形的回落後緩慢回升，形狀如茶杯）和手柄（回到杯口附近後的小幅整理回調）。突破手柄上緣放量為進場信號。是中長期的多頭延續型態。",
              "psy":"杯柄型態代表多頭趨勢的完整修復過程。杯身的圓弧底部代表市場溫和且有序地消化前期漲幅，沒有恐慌性拋售。回到前高附近時（杯口）短線獲利者賣出形成手柄。手柄的整理讓剩餘浮籌出清，主力重新吸籌，突破後走勢乾淨有力。",
              "app":"進場點在突破手柄上緣（即前高附近）時，配合量能放大確認。停損設在手柄最低點下方。目標距離=杯身深度，從突破點向上量。是中長線操作最強的延續型態之一，尤其在週線圖上出現時可信度極高。",
              "cau":"杯柄型態形成時間通常需要數週到數月，分鐘圖上出現的可靠性低。手柄整理的回調幅度不應超過杯身深度的50%。杯底應是圓弧型，V型底的杯柄型態可靠性較差。"},
     "en":{"def":"Cup & Handle consists of a cup (a rounded bottom recovery resembling a teacup) followed by a handle (a small consolidation pullback near the rim of the cup). A volume breakout above the handle's upper boundary is the entry signal. It is a medium-to-long-term bullish continuation pattern.",
           "psy":"The Cup & Handle represents the complete recovery of a bullish trend. The rounded cup bottom shows orderly absorption of prior gains without panic. Near the prior high (the rim), short-term traders sell forming the handle. Handle consolidation flushes remaining weak hands and allows accumulation, setting up a powerful breakout.",
           "app":"Enter long on a confirmed volume breakout above the handle's upper boundary (near prior high). Stop-loss below the handle's low. Target = cup depth projected upward from breakout. One of the strongest long-term continuation patterns, especially reliable on weekly charts.",
           "cau":"Forming over weeks to months — unreliable on minute charts. Handle pullback should not exceed 50% of the cup depth. The cup bottom should be rounded — V-shaped cups are less reliable."},
     "ja":{"def":"カップウィズハンドルは、カップ（ティーカップに似た丸みを帯びた底値からの回復）とハンドル（カップのリム付近での小さな保ち合い押し目）で構成されます。ハンドルの上限を出来高を伴って上抜けするのが参入シグナルです。",
           "psy":"カップウィズハンドルは強気トレンドの完全な回復を表します。丸みを帯びたカップの底はパニックなしに前の上昇分を整然と消化していることを示します。前高（リム）付近で短期トレーダーが売り、ハンドルを形成します。ハンドルの保ち合いは残りの弱い手を一掃し、再蓄積を可能にします。",
           "app":"ハンドルの上限（前高付近）の出来高を伴ったブレイクアウトの確認でロングに参入します。ストップはハンドルの安値の下に設定します。目標＝カップの深さをブレイクアウト点から上方に投影します。",
           "cau":"形成に数週間から数ヶ月かかります。ハンドルの押し目はカップの深さの50%を超えるべきではありません。カップの底は丸みを帯びているべきで、V字型のカップは信頼性が低いです。"},
     "ko":{"def":"컵앤핸들은 컵(찻잔과 비슷한 둥근 바닥 회복)과 핸들(컵 테두리 근처의 작은 횡보 되돌림)로 구성됩니다. 핸들 상단 경계를 거래량과 함께 돌파하는 것이 진입 신호입니다. 중장기 강세 지속 패턴입니다.",
           "psy":"컵앤핸들은 강세 추세의 완전한 회복을 나타냅니다. 둥근 컵 바닥은 공황 없이 이전 상승분을 질서 있게 소화했음을 보여줍니다. 이전 고점(테두리) 근처에서 단기 트레이더들이 매도하여 핸들을 형성합니다.",
           "app":"핸들 상단 경계(이전 고점 근처) 거래량 증가 돌파 확인 시 롱 진입합니다. 손절은 핸들 최저점 아래에 설정합니다. 목표 = 컵 깊이를 돌파점에서 위로 투영합니다.",
           "cau":"형성에 수 주에서 수 개월이 걸립니다. 핸들 되돌림이 컵 깊이의 50%를 초과하면 안 됩니다. 컵 바닥이 둥글어야 하며 V자형 컵은 신뢰도가 낮습니다."},
   }},
]

SECTIONS = ["single","combo","reversal","continuation"]

# ── Lang switcher ─────────────────────────────────────────────────────────────
def lang_links(current_locale, pattern_id=None):
    pairs = [("zh-tw","繁中"),("en","EN"),("ja","日本語"),("ko","한국어")]
    bits = []
    for lc, label in pairs:
        if pattern_id:
            href = f"../{lc}/{pattern_id}.html" if lc != "zh-tw" else f"../../learn/patterns/{pattern_id}.html"
        else:
            href = f"{LOCALE_FILE[lc]}"
        active = "active" if lc == current_locale else ""
        bits.append(f'<a href="{href}" class="lang-btn {active}">{label}</a>')
    return f'<div class="lang-switcher">{"".join(bits)}</div>'

# ── Nav ───────────────────────────────────────────────────────────────────────
def nav_html(ui, locale, depth=0):
    prefix = "../" * depth
    return f'''<nav>
  <a class="nav-logo" href="{prefix}index.html">{ui["site"]}</a>
  <div class="nav-links">
    <a href="{prefix}index.html">{ui["home"]}</a>
    <a href="{prefix}learn/patterns/{LOCALE_FILE[locale]}">{ui["learn"]}</a>
  </div>
</nav>'''

# ── Footer ────────────────────────────────────────────────────────────────────
def footer_html(ui):
    return f'''<footer>
  <div class="footer-logo">{ui["site"]}</div>
  <p>{ui["footer"]}</p>
  <p style="margin-top:8px;font-size:12px">© 2025 {ui["site"]}. All rights reserved.</p>
</footer>'''

# ── Signal tag ────────────────────────────────────────────────────────────────
def sig_tag(signal, ui):
    cls = {"bullish":"tag-bull","bearish":"tag-bear","neutral":"tag-neutral"}.get(signal,"tag-neutral")
    return f'<span class="tag {cls}">{ui["sig"].get(signal, signal)}</span>'

def rel_tag(rel, ui):
    cls = {"high":"tag-high","medium":"tag-medium","low":"tag-low"}.get(rel,"tag-low")
    return f'<span class="tag {cls}">{ui["rel"].get(rel, rel)}</span>'

def wr_color(wr):
    if wr >= 70: return "#22c55e"
    if wr >= 60: return "#f59e0b"
    return "#ef4444"

# ── Build index page ──────────────────────────────────────────────────────────
def build_index(locale):
    ui = UI[locale]
    # group patterns by section
    by_section = {s: [] for s in SECTIONS}
    for p in PATTERNS:
        by_section[p["section"]].append(p)

    sections_html = ""
    for sec in SECTIONS:
        pats = by_section[sec]
        if not pats: continue
        sec_label = ui["sec"].get(sec, sec)
        cards = ""
        for p in pats:
            name = p["names"][locale]
            svg = candle_svg(p["svg"], width=160, height=90)
            href = f"{p['id']}.html" if locale == "zh-tw" else f"{locale}/{p['id']}.html"
            move_str = f"+{p['move']}%" if p["move"] > 0 else (f"{p['move']}%" if p["move"] != 0 else "—")
            cards += f'''<a class="pattern-card" href="{href}">
  <div class="card-svg">{svg}</div>
  <div class="card-name">{name}</div>
  <div class="card-meta">
    {sig_tag(p["signal"], ui)}
    {rel_tag(p["rel"], ui)}
    <span class="tag" style="background:#1e293b;color:#94a3b8;font-size:11px">{ui["wr_lbl"]} {p["wr"]}%</span>
  </div>
</a>'''
        sections_html += f'''<div class="section-header"><h2>{sec_label}</h2></div>
<div class="pattern-grid">{cards}</div>'''

    tips_items = "".join(f"<li>{t}</li>" for t in ui["tips"])

    html = f'''<!DOCTYPE html>
<html lang="{LOCALE_LANG[locale]}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{ui["title"]} | {ui["site"]}</title>
<meta name="description" content="{ui["index_sub"]}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
{nav_html(ui, locale)}
<div class="hero">
  <div class="hero-badge">{ui["badge"]}</div>
  <h1>{ui["title"].split("—")[0].strip()}<br><span>{ui["title"].split("—")[-1].strip() if "—" in ui["title"] else ""}</span></h1>
  <p class="hero-sub">{ui["index_sub"]}</p>
  {lang_links(locale)}
</div>
<div class="container">
{sections_html}
<div class="section-header"><h2>{ui["tips_title"]}</h2></div>
<div class="content-section">
  <ul class="tips-list">{tips_items}</ul>
</div>
</div>
{footer_html(ui)}
</body></html>'''
    return html

# ── Build detail page ─────────────────────────────────────────────────────────
def build_detail(locale, pattern):
    ui = UI[locale]
    c = pattern["content"][locale]
    name = pattern["names"][locale]
    svg = candle_svg(pattern["svg"], width=240, height=150)
    move_str = f"+{pattern['move']}%" if pattern["move"] > 0 else (f"{pattern['move']}%" if pattern["move"] != 0 else "—")
    wrc = wr_color(pattern["wr"])
    back_href = f"../{LOCALE_FILE[locale]}" if locale != "zh-tw" else f"../../learn/patterns/{LOCALE_FILE[locale]}"

    html = f'''<!DOCTYPE html>
<html lang="{LOCALE_LANG[locale]}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{name} — {ui["title"]} | {ui["site"]}</title>
<meta name="description" content="{c["def"][:120]}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
{nav_html(ui, locale, depth=2 if locale!="zh-tw" else 2)}
<div class="container">
  <a class="detail-back" href="{back_href}">{ui["back"]}</a>
  <div class="detail-hero">
    <div>
      <div class="detail-title">{name}</div>
      {lang_links(locale, pattern["id"])}
      <div class="detail-stats" style="margin-top:16px">
        <div class="stat-box">
          <div class="stat-label">{ui["signal_lbl"]}</div>
          <div class="stat-value">{sig_tag(pattern["signal"], ui)}</div>
        </div>
        <div class="stat-box">
          <div class="stat-label">{ui["wr_lbl"]}</div>
          <div class="stat-value" style="color:{wrc}">{pattern["wr"]}%</div>
          <div class="wr-bar-wrap"><div class="wr-bar" style="width:{pattern["wr"]}%;background:{wrc}"></div></div>
        </div>
        <div class="stat-box">
          <div class="stat-label">{ui["move_lbl"]}</div>
          <div class="stat-value" style="color:{wrc}">{move_str}</div>
        </div>
        <div class="stat-box">
          <div class="stat-label">{ui["rel_lbl"]}</div>
          <div class="stat-value">{rel_tag(pattern["rel"], ui)}</div>
        </div>
      </div>
    </div>
    <div class="svg-box">{svg}</div>
  </div>

  <div class="content-section">
    <h3>{ui["def_lbl"]}</h3>
    <p>{c["def"]}</p>
  </div>
  <div class="content-section">
    <h3>{ui["psy_lbl"]}</h3>
    <p>{c["psy"]}</p>
  </div>
  <div class="content-section">
    <h3>{ui["app_lbl"]}</h3>
    <p>{c["app"]}</p>
  </div>
  <div class="content-section">
    <h3>{ui["cau_lbl"]}</h3>
    <p>{c["cau"]}</p>
  </div>
</div>
{footer_html(ui)}
</body></html>'''
    return html

# ── Generate all files ────────────────────────────────────────────────────────
generated = []

for locale in ["zh-tw","en","ja","ko"]:
    if locale == "zh-tw":
        idx_dir = f"{OUT}/learn/patterns"
        detail_dir = f"{OUT}/learn/patterns"
    else:
        idx_dir = f"{OUT}/learn/patterns"
        detail_dir = f"{OUT}/learn/patterns/{locale}"

    os.makedirs(idx_dir, exist_ok=True)
    os.makedirs(detail_dir, exist_ok=True)

    # index
    idx_file = f"{idx_dir}/{LOCALE_FILE[locale]}"
    with open(idx_file, "w", encoding="utf-8") as f:
        f.write(build_index(locale))
    generated.append(idx_file)

    # details
    for p in PATTERNS:
        detail_file = f"{detail_dir}/{p['id']}.html"
        with open(detail_file, "w", encoding="utf-8") as f:
            f.write(build_detail(locale, p))
        generated.append(detail_file)

print(f"Generated {len(generated)} files")
for g in generated[:8]:
    print(" ", g)
print("  ...")
