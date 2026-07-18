#!/usr/bin/env python3
"""add_blog_svgs.py — Inject SVG educational diagrams into blog articles.
Each article gets 1-2 SVG diagrams inserted after the first <h2> section.
Handles all 10 languages with translated labels.
Skips files that already have SVG diagrams.

Usage:
  python add_blog_svgs.py              # dry-run
  python add_blog_svgs.py --execute    # real run
"""
import os, sys, re, glob, shutil

BASE = r"D:\xian-shang-you-wei\backend\frontend\blog"
DRY = '--execute' not in sys.argv

# ── Language labels ──
LABELS = {
    'zh-TW': {'overbought':'超買區','oversold':'超賣區','golden_cross':'黃金交叉','death_cross':'死亡交叉',
              'k_line':'K線','d_line':'D線','signal':'訊號線','histogram':'柱體','divergence':'背離',
              'bullish':'看漲','bearish':'看跌','price':'價格','volume':'成交量','time':'時間',
              'support':'支撐','resistance':'壓力','ma5':'MA5','ma20':'MA20','ma60':'MA60',
              'entry':'進場','exit':'出場','stop_loss':'停損','target':'目標價','risk':'風險',
              'reward':'報酬','high_risk':'高風險','mid_risk':'中風險','low_risk':'低風險',
              'buy_signal':'買進訊號','sell_signal':'賣出訊號','trend_up':'上升趨勢','trend_down':'下降趨勢',
              'reversal':'反轉型態','continuation':'持續型態','foreign':'外資','trust':'投信','dealer':'自營商',
              'step':'步驟','confirm_trend':'確認大盤','select_sector':'選產業','pick_stock':'選個股',
              'check_technical':'看技術面','calc_rr':'算損益比'},
    'en': {'overbought':'Overbought','oversold':'Oversold','golden_cross':'Golden Cross','death_cross':'Death Cross',
           'k_line':'%K','d_line':'%D','signal':'Signal','histogram':'Histogram','divergence':'Divergence',
           'bullish':'Bullish','bearish':'Bearish','price':'Price','volume':'Volume','time':'Time',
           'support':'Support','resistance':'Resistance','ma5':'MA5','ma20':'MA20','ma60':'MA60',
           'entry':'Entry','exit':'Exit','stop_loss':'Stop Loss','target':'Target','risk':'Risk',
           'reward':'Reward','high_risk':'High Risk','mid_risk':'Medium','low_risk':'Low Risk',
           'buy_signal':'Buy Signal','sell_signal':'Sell Signal','trend_up':'Uptrend','trend_down':'Downtrend',
           'reversal':'Reversal','continuation':'Continuation','foreign':'Foreign','trust':'Mutual Fund','dealer':'Dealer',
           'step':'Step','confirm_trend':'Check Market','select_sector':'Pick Sector','pick_stock':'Pick Stock',
           'check_technical':'Technical Check','calc_rr':'Risk/Reward'},
    'ja': {'overbought':'買われすぎ','oversold':'売られすぎ','golden_cross':'ゴールデンクロス','death_cross':'デッドクロス',
           'k_line':'%K','d_line':'%D','signal':'シグナル','histogram':'ヒストグラム','divergence':'ダイバージェンス',
           'bullish':'強気','bearish':'弱気','price':'価格','volume':'出来高','time':'時間',
           'support':'サポート','resistance':'レジスタンス','ma5':'MA5','ma20':'MA20','ma60':'MA60',
           'entry':'エントリー','exit':'利確','stop_loss':'損切り','target':'目標','risk':'リスク',
           'reward':'リワード','high_risk':'高リスク','mid_risk':'中リスク','low_risk':'低リスク',
           'buy_signal':'買いシグナル','sell_signal':'売りシグナル','trend_up':'上昇トレンド','trend_down':'下降トレンド',
           'reversal':'反転','continuation':'継続','foreign':'外国人','trust':'投信','dealer':'自己売買',
           'step':'ステップ','confirm_trend':'相場確認','select_sector':'業種選択','pick_stock':'銘柄選択',
           'check_technical':'テクニカル確認','calc_rr':'損益比計算'},
    'ko': {'overbought':'과매수','oversold':'과매도','golden_cross':'골든크로스','death_cross':'데드크로스',
           'k_line':'%K','d_line':'%D','signal':'시그널','histogram':'히스토그램','divergence':'다이버전스',
           'bullish':'강세','bearish':'약세','price':'가격','volume':'거래량','time':'시간',
           'support':'지지','resistance':'저항','ma5':'MA5','ma20':'MA20','ma60':'MA60',
           'entry':'진입','exit':'청산','stop_loss':'손절','target':'목표가','risk':'위험',
           'reward':'보상','high_risk':'고위험','mid_risk':'중위험','low_risk':'저위험',
           'buy_signal':'매수신호','sell_signal':'매도신호','trend_up':'상승추세','trend_down':'하락추세',
           'reversal':'반전','continuation':'지속','foreign':'외국인','trust':'투신','dealer':'자기매매',
           'step':'단계','confirm_trend':'시장확인','select_sector':'업종선택','pick_stock':'종목선택',
           'check_technical':'기술확인','calc_rr':'손익비계산'},
}
# Fallback: other languages use English labels
for lang in ['de','fr','es','pt','id','zh-CN']:
    if lang == 'zh-CN':
        LABELS[lang] = dict(LABELS['zh-TW'])  # Simplified Chinese uses same terms
        LABELS[lang]['overbought'] = '超买区'
        LABELS[lang]['oversold'] = '超卖区'
        LABELS[lang]['golden_cross'] = '黄金交叉'
        LABELS[lang]['death_cross'] = '死亡交叉'
        LABELS[lang]['support'] = '支撑'
        LABELS[lang]['resistance'] = '压力'
        LABELS[lang]['stop_loss'] = '止损'
        LABELS[lang]['buy_signal'] = '买进信号'
        LABELS[lang]['sell_signal'] = '卖出信号'
        LABELS[lang]['reversal'] = '反转形态'
        LABELS[lang]['continuation'] = '持续形态'
    else:
        LABELS[lang] = dict(LABELS['en'])

def L(lang, key):
    return LABELS.get(lang, LABELS['en']).get(key, key)


# ── SVG Templates ──
# Each returns an SVG string with localized labels.

def svg_kd(lang):
    """KD indicator: K/D lines with golden cross, death cross, overbought/oversold zones"""
    return f'''<div style="margin:24px 0;text-align:center">
<svg viewBox="0 0 600 320" xmlns="http://www.w3.org/2000/svg" style="max-width:600px;width:100%;background:#FAFBFC;border-radius:12px;border:1px solid #E2E8F0">
  <defs><linearGradient id="kd-ob" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#EF4444" stop-opacity="0.12"/><stop offset="1" stop-color="#EF4444" stop-opacity="0.03"/></linearGradient>
  <linearGradient id="kd-os" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#10B981" stop-opacity="0.03"/><stop offset="1" stop-color="#10B981" stop-opacity="0.12"/></linearGradient></defs>
  <rect x="60" y="30" width="510" height="52" fill="url(#kd-ob)" rx="4"/>
  <rect x="60" y="228" width="510" height="52" fill="url(#kd-os)" rx="4"/>
  <line x1="60" y1="82" x2="570" y2="82" stroke="#EF4444" stroke-width="1" stroke-dasharray="6,4" opacity="0.5"/>
  <line x1="60" y1="228" x2="570" y2="228" stroke="#10B981" stroke-width="1" stroke-dasharray="6,4" opacity="0.5"/>
  <text x="54" y="40" font-size="11" fill="#EF4444" text-anchor="end">100</text>
  <text x="54" y="86" font-size="11" fill="#EF4444" text-anchor="end">80</text>
  <text x="54" y="160" font-size="11" fill="#94A3B8" text-anchor="end">50</text>
  <text x="54" y="232" font-size="11" fill="#10B981" text-anchor="end">20</text>
  <text x="54" y="285" font-size="11" fill="#10B981" text-anchor="end">0</text>
  <text x="572" y="76" font-size="10" fill="#EF4444" font-weight="600">{L(lang,"overbought")}</text>
  <text x="572" y="248" font-size="10" fill="#10B981" font-weight="600">{L(lang,"oversold")}</text>
  <polyline points="80,200 120,230 160,250 200,240 230,210 260,160 300,100 340,65 370,55 400,60 430,80 460,130 490,180 520,220 550,245" fill="none" stroke="#2563EB" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
  <polyline points="80,210 120,238 160,255 200,248 230,220 260,175 300,115 340,75 370,62 400,68 430,95 460,145 490,195 520,232 550,252" fill="none" stroke="#F59E0B" stroke-width="2" stroke-dasharray="6,3" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="260" cy="160" r="6" fill="#10B981" stroke="#fff" stroke-width="2"/>
  <text x="260" y="150" font-size="10" fill="#10B981" text-anchor="middle" font-weight="600">↑ {L(lang,"golden_cross")}</text>
  <circle cx="460" cy="130" r="6" fill="#EF4444" stroke="#fff" stroke-width="2"/>
  <text x="460" y="120" font-size="10" fill="#EF4444" text-anchor="middle" font-weight="600">↓ {L(lang,"death_cross")}</text>
  <rect x="80" y="295" width="14" height="3" rx="1" fill="#2563EB"/><text x="98" y="298" font-size="10" fill="#334155">{L(lang,"k_line")}</text>
  <rect x="150" y="295" width="14" height="3" rx="1" fill="#F59E0B"/><text x="168" y="298" font-size="10" fill="#334155">{L(lang,"d_line")}</text>
</svg></div>'''

def svg_macd(lang):
    """MACD: histogram bars + MACD line + signal line"""
    bars = ''
    vals = [-8,-12,-6,-3,2,8,14,18,22,16,10,4,-2,-6,-10,-14,-10,-5,0,5,10,15,18,14,8]
    for i,v in enumerate(vals):
        x = 80 + i*20
        h = abs(v)*5
        y = 150 - (h if v>0 else 0)
        c = '#10B981' if v>0 else '#EF4444'
        bars += f'<rect x="{x}" y="{y}" width="16" height="{h}" rx="2" fill="{c}" opacity="0.6"/>'
    return f'''<div style="margin:24px 0;text-align:center">
<svg viewBox="0 0 600 300" xmlns="http://www.w3.org/2000/svg" style="max-width:600px;width:100%;background:#FAFBFC;border-radius:12px;border:1px solid #E2E8F0">
  <line x1="60" y1="150" x2="580" y2="150" stroke="#CBD5E0" stroke-width="1"/>
  <text x="54" y="154" font-size="10" fill="#94A3B8" text-anchor="end">0</text>
  {bars}
  <polyline points="88,170 108,185 128,168 148,158 168,142 188,125 208,112 228,100 248,92 268,98 288,110 308,125 328,142 348,158 368,172 388,180 408,170 428,155 448,148 468,135 488,118 508,105 528,98 548,108 568,120" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round"/>
  <polyline points="88,175 108,180 128,175 148,165 168,150 188,135 208,120 228,108 248,100 268,100 288,108 308,120 328,138 348,155 368,168 388,178 408,178 428,168 448,158 468,145 488,130 508,115 528,108 548,110 568,118" fill="none" stroke="#F59E0B" stroke-width="2" stroke-dasharray="5,3" stroke-linecap="round"/>
  <text x="56" y="20" font-size="12" fill="#334155" font-weight="600">MACD</text>
  <rect x="100" y="275" width="14" height="3" rx="1" fill="#2563EB"/><text x="118" y="278" font-size="10" fill="#334155">MACD</text>
  <rect x="170" y="275" width="14" height="3" rx="1" fill="#F59E0B"/><text x="188" y="278" font-size="10" fill="#334155">{L(lang,"signal")}</text>
  <rect x="250" y="272" width="10" height="8" rx="1" fill="#10B981" opacity="0.6"/><text x="264" y="280" font-size="10" fill="#334155">{L(lang,"histogram")}</text>
</svg></div>'''

def svg_rsi(lang):
    """RSI oscillator with overbought/oversold zones"""
    return f'''<div style="margin:24px 0;text-align:center">
<svg viewBox="0 0 600 280" xmlns="http://www.w3.org/2000/svg" style="max-width:600px;width:100%;background:#FAFBFC;border-radius:12px;border:1px solid #E2E8F0">
  <rect x="60" y="25" width="510" height="45" fill="#EF4444" opacity="0.08" rx="4"/>
  <rect x="60" y="200" width="510" height="45" fill="#10B981" opacity="0.08" rx="4"/>
  <line x1="60" y1="70" x2="570" y2="70" stroke="#EF4444" stroke-width="1" stroke-dasharray="6,4" opacity="0.5"/>
  <line x1="60" y1="200" x2="570" y2="200" stroke="#10B981" stroke-width="1" stroke-dasharray="6,4" opacity="0.5"/>
  <line x1="60" y1="135" x2="570" y2="135" stroke="#CBD5E0" stroke-width="1" stroke-dasharray="3,3"/>
  <text x="54" y="74" font-size="10" fill="#EF4444" text-anchor="end">70</text>
  <text x="54" y="139" font-size="10" fill="#94A3B8" text-anchor="end">50</text>
  <text x="54" y="204" font-size="10" fill="#10B981" text-anchor="end">30</text>
  <text x="572" y="64" font-size="10" fill="#EF4444" font-weight="600">{L(lang,"overbought")}</text>
  <text x="572" y="220" font-size="10" fill="#10B981" font-weight="600">{L(lang,"oversold")}</text>
  <polyline points="80,140 110,125 140,100 170,75 200,55 230,50 255,58 280,80 310,110 340,135 370,160 400,190 430,210 455,220 480,215 505,195 530,170 555,140" fill="none" stroke="#7C3AED" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="230" cy="50" r="5" fill="#EF4444" stroke="#fff" stroke-width="2"/>
  <text x="230" y="42" font-size="10" fill="#EF4444" text-anchor="middle" font-weight="600">{L(lang,"sell_signal")}</text>
  <circle cx="455" cy="220" r="5" fill="#10B981" stroke="#fff" stroke-width="2"/>
  <text x="455" y="240" font-size="10" fill="#10B981" text-anchor="middle" font-weight="600">{L(lang,"buy_signal")}</text>
  <text x="56" y="18" font-size="12" fill="#334155" font-weight="600">RSI</text>
</svg></div>'''

def svg_ma(lang):
    """Moving averages: MA5/MA20/MA60 with price"""
    return f'''<div style="margin:24px 0;text-align:center">
<svg viewBox="0 0 600 300" xmlns="http://www.w3.org/2000/svg" style="max-width:600px;width:100%;background:#FAFBFC;border-radius:12px;border:1px solid #E2E8F0">
  <text x="56" y="20" font-size="12" fill="#334155" font-weight="600">{L(lang,"price")} + {L(lang,"ma5")}/{L(lang,"ma20")}/{L(lang,"ma60")}</text>
  <polyline points="60,220 90,200 120,180 150,170 180,155 210,145 240,130 270,118 300,105 330,100 360,110 390,125 420,140 450,135 480,120 510,108 540,100 570,95" fill="none" stroke="#94A3B8" stroke-width="1.5" opacity="0.5"/>
  <polyline points="60,215 90,198 120,182 150,168 180,158 210,148 240,135 270,122 300,110 330,105 360,112 390,122 420,135 450,130 480,118 510,106 540,98 570,94" fill="none" stroke="#EF4444" stroke-width="2" stroke-linecap="round"/>
  <polyline points="60,225 90,215 120,200 150,188 180,175 210,162 240,150 270,140 300,130 330,125 360,125 390,130 420,138 450,135 480,128 510,118 540,110 570,105" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round"/>
  <polyline points="60,240 90,235 120,225 150,215 180,205 210,195 240,185 270,175 300,168 330,162 360,158 390,155 420,152 450,150 480,148 510,145 540,140 570,135" fill="none" stroke="#F59E0B" stroke-width="2" stroke-linecap="round"/>
  <rect x="80" y="270" width="14" height="3" rx="1" fill="#EF4444"/><text x="98" y="274" font-size="10" fill="#334155">{L(lang,"ma5")}</text>
  <rect x="140" y="270" width="14" height="3" rx="1" fill="#2563EB"/><text x="158" y="274" font-size="10" fill="#334155">{L(lang,"ma20")}</text>
  <rect x="210" y="270" width="14" height="3" rx="1" fill="#F59E0B"/><text x="228" y="274" font-size="10" fill="#334155">{L(lang,"ma60")}</text>
  <rect x="280" y="270" width="14" height="3" rx="1" fill="#94A3B8"/><text x="298" y="274" font-size="10" fill="#334155">{L(lang,"price")}</text>
  <text x="330" y="92" font-size="10" fill="#2563EB" font-weight="600">↑ {L(lang,"trend_up")}</text>
</svg></div>'''

def svg_candlestick(lang):
    """Candlestick patterns: hammer, engulfing, morning star"""
    return f'''<div style="margin:24px 0;text-align:center">
<svg viewBox="0 0 600 260" xmlns="http://www.w3.org/2000/svg" style="max-width:600px;width:100%;background:#FAFBFC;border-radius:12px;border:1px solid #E2E8F0">
  <text x="56" y="20" font-size="12" fill="#334155" font-weight="600">{L(lang,"reversal")} — {L(lang,"bullish")}</text>
  <g transform="translate(80,40)"><text x="25" y="-5" font-size="10" fill="#334155" text-anchor="middle" font-weight="600">Hammer</text>
    <line x1="25" y1="20" x2="25" y2="40" stroke="#10B981" stroke-width="2"/>
    <rect x="15" y="40" width="20" height="25" rx="2" fill="#10B981"/>
    <line x1="25" y1="65" x2="25" y2="150" stroke="#10B981" stroke-width="2"/>
    <text x="25" y="170" font-size="9" fill="#10B981" text-anchor="middle">{L(lang,"buy_signal")}</text></g>
  <g transform="translate(200,40)"><text x="30" y="-5" font-size="10" fill="#334155" text-anchor="middle" font-weight="600">Engulfing</text>
    <rect x="10" y="40" width="18" height="55" rx="2" fill="#EF4444"/>
    <line x1="19" y1="30" x2="19" y2="40" stroke="#EF4444" stroke-width="2"/>
    <line x1="19" y1="95" x2="19" y2="110" stroke="#EF4444" stroke-width="2"/>
    <rect x="30" y="25" width="22" height="90" rx="2" fill="#10B981"/>
    <line x1="41" y1="15" x2="41" y2="25" stroke="#10B981" stroke-width="2"/>
    <line x1="41" y1="115" x2="41" y2="130" stroke="#10B981" stroke-width="2"/>
    <text x="30" y="170" font-size="9" fill="#10B981" text-anchor="middle">{L(lang,"buy_signal")}</text></g>
  <g transform="translate(340,40)"><text x="45" y="-5" font-size="10" fill="#334155" text-anchor="middle" font-weight="600">Morning Star</text>
    <rect x="0" y="20" width="18" height="70" rx="2" fill="#EF4444"/>
    <line x1="9" y1="10" x2="9" y2="20" stroke="#EF4444" stroke-width="2"/>
    <line x1="9" y1="90" x2="9" y2="105" stroke="#EF4444" stroke-width="2"/>
    <rect x="30" y="85" width="14" height="12" rx="2" fill="#94A3B8" stroke="#94A3B8"/>
    <line x1="37" y1="78" x2="37" y2="85" stroke="#94A3B8" stroke-width="2"/>
    <line x1="37" y1="97" x2="37" y2="110" stroke="#94A3B8" stroke-width="2"/>
    <rect x="56" y="30" width="18" height="65" rx="2" fill="#10B981"/>
    <line x1="65" y1="20" x2="65" y2="30" stroke="#10B981" stroke-width="2"/>
    <line x1="65" y1="95" x2="65" y2="108" stroke="#10B981" stroke-width="2"/>
    <text x="45" y="170" font-size="9" fill="#10B981" text-anchor="middle">{L(lang,"buy_signal")}</text></g>
</svg></div>'''

def svg_support_resistance(lang):
    """Support and resistance levels with price bouncing"""
    return f'''<div style="margin:24px 0;text-align:center">
<svg viewBox="0 0 600 280" xmlns="http://www.w3.org/2000/svg" style="max-width:600px;width:100%;background:#FAFBFC;border-radius:12px;border:1px solid #E2E8F0">
  <line x1="60" y1="80" x2="570" y2="80" stroke="#EF4444" stroke-width="2" stroke-dasharray="8,4"/>
  <line x1="60" y1="200" x2="570" y2="200" stroke="#10B981" stroke-width="2" stroke-dasharray="8,4"/>
  <text x="572" y="76" font-size="11" fill="#EF4444" font-weight="600">{L(lang,"resistance")}</text>
  <text x="572" y="216" font-size="11" fill="#10B981" font-weight="600">{L(lang,"support")}</text>
  <polyline points="80,190 120,170 150,130 180,95 210,85 240,90 270,120 300,160 330,190 360,195 390,185 420,150 450,110 480,88 510,85 540,92 560,115" fill="none" stroke="#2563EB" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="210" cy="85" r="5" fill="#EF4444" stroke="#fff" stroke-width="2"/>
  <text x="210" y="72" font-size="9" fill="#EF4444" text-anchor="middle">↓</text>
  <circle cx="360" cy="195" r="5" fill="#10B981" stroke="#fff" stroke-width="2"/>
  <text x="360" y="215" font-size="9" fill="#10B981" text-anchor="middle">↑</text>
  <circle cx="480" cy="88" r="5" fill="#EF4444" stroke="#fff" stroke-width="2"/>
  <text x="480" y="72" font-size="9" fill="#EF4444" text-anchor="middle">↓</text>
  <text x="300" y="26" font-size="12" fill="#334155" font-weight="600" text-anchor="middle">{L(lang,"support")} &amp; {L(lang,"resistance")}</text>
</svg></div>'''

def svg_stop_loss(lang):
    """Stop loss positioning diagram"""
    return f'''<div style="margin:24px 0;text-align:center">
<svg viewBox="0 0 600 260" xmlns="http://www.w3.org/2000/svg" style="max-width:600px;width:100%;background:#FAFBFC;border-radius:12px;border:1px solid #E2E8F0">
  <text x="300" y="22" font-size="12" fill="#334155" font-weight="600" text-anchor="middle">{L(lang,"entry")} / {L(lang,"stop_loss")} / {L(lang,"target")}</text>
  <line x1="100" y1="140" x2="500" y2="140" stroke="#2563EB" stroke-width="2" stroke-dasharray="6,3"/>
  <text x="502" y="137" font-size="11" fill="#2563EB" font-weight="600">{L(lang,"entry")}</text>
  <line x1="100" y1="200" x2="500" y2="200" stroke="#EF4444" stroke-width="2" stroke-dasharray="6,3"/>
  <text x="502" y="197" font-size="11" fill="#EF4444" font-weight="600">{L(lang,"stop_loss")}</text>
  <line x1="100" y1="60" x2="500" y2="60" stroke="#10B981" stroke-width="2" stroke-dasharray="6,3"/>
  <text x="502" y="57" font-size="11" fill="#10B981" font-weight="600">{L(lang,"target")}</text>
  <line x1="300" y1="60" x2="300" y2="140" stroke="#10B981" stroke-width="1" opacity="0.5"/>
  <line x1="300" y1="140" x2="300" y2="200" stroke="#EF4444" stroke-width="1" opacity="0.5"/>
  <text x="310" y="105" font-size="11" fill="#10B981">{L(lang,"reward")}</text>
  <text x="310" y="175" font-size="11" fill="#EF4444">{L(lang,"risk")}</text>
  <rect x="250" y="95" width="100" height="14" rx="4" fill="#2563EB" opacity="0.1"/>
  <text x="300" y="106" font-size="10" fill="#2563EB" text-anchor="middle" font-weight="600">2:1 R/R</text>
</svg></div>'''

def svg_profit_loss(lang):
    """Risk reward ratio visualization"""
    return svg_stop_loss(lang)  # Same concept, reuse

def svg_position_risk(lang):
    """Position risk levels: near support, breakout, chasing"""
    return f'''<div style="margin:24px 0;text-align:center">
<svg viewBox="0 0 600 220" xmlns="http://www.w3.org/2000/svg" style="max-width:600px;width:100%;background:#FAFBFC;border-radius:12px;border:1px solid #E2E8F0">
  <text x="300" y="22" font-size="12" fill="#334155" font-weight="600" text-anchor="middle">{L(lang,"risk")} Level</text>
  <rect x="40" y="50" width="160" height="120" rx="12" fill="#10B981" opacity="0.1" stroke="#10B981" stroke-width="1.5"/>
  <text x="120" y="80" font-size="13" fill="#10B981" text-anchor="middle" font-weight="700">{L(lang,"low_risk")}</text>
  <text x="120" y="100" font-size="10" fill="#4A5568" text-anchor="middle">{L(lang,"support")} ↑</text>
  <text x="120" y="150" font-size="28" text-anchor="middle">✅</text>
  <rect x="220" y="50" width="160" height="120" rx="12" fill="#F59E0B" opacity="0.1" stroke="#F59E0B" stroke-width="1.5"/>
  <text x="300" y="80" font-size="13" fill="#F59E0B" text-anchor="middle" font-weight="700">{L(lang,"mid_risk")}</text>
  <text x="300" y="100" font-size="10" fill="#4A5568" text-anchor="middle">Breakout</text>
  <text x="300" y="150" font-size="28" text-anchor="middle">⚠️</text>
  <rect x="400" y="50" width="160" height="120" rx="12" fill="#EF4444" opacity="0.1" stroke="#EF4444" stroke-width="1.5"/>
  <text x="480" y="80" font-size="13" fill="#EF4444" text-anchor="middle" font-weight="700">{L(lang,"high_risk")}</text>
  <text x="480" y="100" font-size="10" fill="#4A5568" text-anchor="middle">{L(lang,"resistance")} ↓</text>
  <text x="480" y="150" font-size="28" text-anchor="middle">🚫</text>
</svg></div>'''

def svg_institutional(lang):
    """Institutional investors: foreign, mutual fund, dealer flow"""
    return f'''<div style="margin:24px 0;text-align:center">
<svg viewBox="0 0 600 240" xmlns="http://www.w3.org/2000/svg" style="max-width:600px;width:100%;background:#FAFBFC;border-radius:12px;border:1px solid #E2E8F0">
  <text x="300" y="22" font-size="12" fill="#334155" font-weight="600" text-anchor="middle">{L(lang,"foreign")} / {L(lang,"trust")} / {L(lang,"dealer")}</text>
  <rect x="60" y="60" width="140" height="35" rx="6" fill="#2563EB" opacity="0.85"/>
  <text x="130" y="82" font-size="12" fill="#fff" text-anchor="middle" font-weight="600">{L(lang,"foreign")} +520M</text>
  <rect x="230" y="60" width="90" height="35" rx="6" fill="#10B981" opacity="0.85"/>
  <text x="275" y="82" font-size="12" fill="#fff" text-anchor="middle" font-weight="600">{L(lang,"trust")} +80M</text>
  <rect x="350" y="60" width="60" height="35" rx="6" fill="#F59E0B" opacity="0.85"/>
  <text x="380" y="82" font-size="11" fill="#fff" text-anchor="middle" font-weight="600">{L(lang,"dealer")} -30M</text>
  <line x1="60" y1="130" x2="540" y2="130" stroke="#CBD5E0" stroke-width="1"/>
  <rect x="60" y="140" width="350" height="22" rx="4" fill="#2563EB" opacity="0.2"/>
  <rect x="60" y="140" width="350" height="22" rx="4" fill="#2563EB" opacity="0.15"/>
  <text x="235" y="156" font-size="10" fill="#2563EB" text-anchor="middle">{L(lang,"foreign")} 62%</text>
  <rect x="410" y="140" width="80" height="22" rx="4" fill="#10B981" opacity="0.2"/>
  <text x="450" y="156" font-size="10" fill="#10B981" text-anchor="middle">{L(lang,"trust")} 14%</text>
  <rect x="490" y="140" width="50" height="22" rx="4" fill="#F59E0B" opacity="0.2"/>
  <text x="515" y="156" font-size="10" fill="#F59E0B" text-anchor="middle">24%</text>
  <text x="300" y="200" font-size="10" fill="#718096" text-anchor="middle">{L(lang,"foreign")} = Key driver of market direction</text>
</svg></div>'''

def svg_stock_selection(lang):
    """5-step stock selection flowchart"""
    return f'''<div style="margin:24px 0;text-align:center">
<svg viewBox="0 0 600 200" xmlns="http://www.w3.org/2000/svg" style="max-width:600px;width:100%;background:#FAFBFC;border-radius:12px;border:1px solid #E2E8F0">
  <text x="300" y="22" font-size="12" fill="#334155" font-weight="600" text-anchor="middle">5 {L(lang,"step")}s</text>
  <rect x="20" y="50" width="95" height="55" rx="10" fill="#2563EB" opacity="0.1" stroke="#2563EB" stroke-width="1.5"/>
  <text x="67" y="72" font-size="10" fill="#2563EB" text-anchor="middle" font-weight="600">{L(lang,"step")} 1</text>
  <text x="67" y="90" font-size="9" fill="#334155" text-anchor="middle">{L(lang,"confirm_trend")}</text>
  <text x="128" y="80" font-size="16" fill="#2563EB">→</text>
  <rect x="138" y="50" width="95" height="55" rx="10" fill="#10B981" opacity="0.1" stroke="#10B981" stroke-width="1.5"/>
  <text x="185" y="72" font-size="10" fill="#10B981" text-anchor="middle" font-weight="600">{L(lang,"step")} 2</text>
  <text x="185" y="90" font-size="9" fill="#334155" text-anchor="middle">{L(lang,"select_sector")}</text>
  <text x="246" y="80" font-size="16" fill="#10B981">→</text>
  <rect x="256" y="50" width="95" height="55" rx="10" fill="#F59E0B" opacity="0.1" stroke="#F59E0B" stroke-width="1.5"/>
  <text x="303" y="72" font-size="10" fill="#F59E0B" text-anchor="middle" font-weight="600">{L(lang,"step")} 3</text>
  <text x="303" y="90" font-size="9" fill="#334155" text-anchor="middle">{L(lang,"pick_stock")}</text>
  <text x="364" y="80" font-size="16" fill="#F59E0B">→</text>
  <rect x="374" y="50" width="95" height="55" rx="10" fill="#7C3AED" opacity="0.1" stroke="#7C3AED" stroke-width="1.5"/>
  <text x="421" y="72" font-size="10" fill="#7C3AED" text-anchor="middle" font-weight="600">{L(lang,"step")} 4</text>
  <text x="421" y="90" font-size="9" fill="#334155" text-anchor="middle">{L(lang,"check_technical")}</text>
  <text x="482" y="80" font-size="16" fill="#7C3AED">→</text>
  <rect x="492" y="50" width="95" height="55" rx="10" fill="#EF4444" opacity="0.1" stroke="#EF4444" stroke-width="1.5"/>
  <text x="539" y="72" font-size="10" fill="#EF4444" text-anchor="middle" font-weight="600">{L(lang,"step")} 5</text>
  <text x="539" y="90" font-size="9" fill="#334155" text-anchor="middle">{L(lang,"calc_rr")}</text>
</svg></div>'''

# ── Article-to-SVG mapping ──
SVG_MAP = {
    'kd-indicator':     [svg_kd],
    'macd-indicator':   [svg_macd],
    'rsi-indicator':    [svg_rsi],
    'moving-average-guide': [svg_ma],
    'candlestick-patterns': [svg_candlestick],
    'support-resistance':   [svg_support_resistance],
    'stop-loss-guide':      [svg_stop_loss],
    'profit-loss-ratio':    [svg_profit_loss],
    'position-risk':        [svg_position_risk],
    'institutional-investors': [svg_institutional],
    'stock-selection-guide':   [svg_stock_selection],
}

# ── Detect language from file path ──
def detect_lang(fpath):
    parts = fpath.replace('\\','/').split('/')
    for p in parts:
        if p in ['en','ja','ko','de','fr','es','pt','id','zh-CN']:
            return p
    return 'zh-TW'

# ── Inject SVGs ──
def inject(fpath, slug, lang):
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Skip if already has SVG
    if '<svg viewBox=' in html and 'xmlns="http://www.w3.org/2000/svg"' in html:
        return 'skip'

    funcs = SVG_MAP.get(slug)
    if not funcs:
        return 'no-svg'

    svg_html = '\n'.join(fn(lang) for fn in funcs)

    # Insert after first </p> that follows the first <h2> in article-content
    # Pattern: find first <h2> then first </p> after it
    m = re.search(r'(<article[^>]*class="[^"]*article-content[^"]*"[^>]*>.*?<h2[^>]*>.*?</h2>.*?</p>)', html, re.DOTALL)
    if not m:
        # Fallback: insert after first </p> in article
        m = re.search(r'(<article[^>]*>.*?</p>)', html, re.DOTALL)
    if not m:
        return 'no-insert-point'

    insert_pos = m.end()
    new_html = html[:insert_pos] + '\n' + svg_html + '\n' + html[insert_pos:]

    if not DRY:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_html)

    return 'ok'


def main():
    if DRY:
        print("=== DRY RUN (add --execute to apply) ===\n")

    # Collect blog files
    files = []
    # zh-TW root
    for f in glob.glob(os.path.join(BASE, '*.html')):
        bn = os.path.basename(f)
        if bn == 'index.html':
            continue
        files.append(f)
    # Language subdirs
    for f in glob.glob(os.path.join(BASE, '*', '*.html')):
        bn = os.path.basename(f)
        if bn == 'index.html':
            continue
        files.append(f)

    files.sort()
    total = len(files)
    injected = 0
    skipped = 0
    no_svg = 0
    errors = 0

    for fpath in files:
        slug = os.path.basename(fpath).replace('.html', '')
        lang = detect_lang(fpath)
        try:
            result = inject(fpath, slug, lang)
            if result == 'ok':
                injected += 1
                print(f'  ✅ {lang}/{slug}')
            elif result == 'skip':
                skipped += 1
            elif result == 'no-svg':
                no_svg += 1
            else:
                errors += 1
                print(f'  ⚠ {result}: {fpath}')
        except Exception as e:
            errors += 1
            print(f'  ❌ {fpath}: {e}')

    print(f'\nTotal files: {total}')
    print(f'  Will inject SVG: {injected}')
    print(f'  Already has SVG (skip): {skipped}')
    print(f'  No SVG defined: {no_svg}')
    print(f'  Errors: {errors}')

    if DRY and injected > 0:
        print(f'\n👉 Run: python add_blog_svgs.py --execute')


if __name__ == '__main__':
    if '--execute' in sys.argv:
        bk = BASE + '_backup_svgs'
        if not os.path.exists(bk):
            print(f'Backing up {BASE} → {bk} ...')
            shutil.copytree(BASE, bk)
            print('Backup done.\n')
        else:
            print(f'Backup already exists: {bk}\n')

    main()
