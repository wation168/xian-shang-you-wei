#!/usr/bin/env python3
# fix_titles_all.py
# Rewrite Title + Meta Description for all striking distance pages
# Philosophy: "Pull people IN" + cross-sell breadth
#
# Usage:
#   cd D:\xian-shang-you-wei\knowledge-engine
#   python fix_titles_all.py

import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
FRONTEND = os.path.join(REPO_ROOT, "backend", "frontend")
if not os.path.isdir(FRONTEND):
    FRONTEND = os.path.join(REPO_ROOT, "frontend")
if not os.path.isdir(FRONTEND):
    print(f"[ERROR] Cannot find frontend directory")
    sys.exit(1)

# ================================================================
# TITLE + DESCRIPTION MAP
# Title: Answer question + breadth hook
# Description: Specific value + cross-sell 500+ tools / 12 pickers
# ================================================================

REWRITES = {
    # ============================================================
    # TOOLS - zh-TW
    # ============================================================
    "tools/work-days.html": (
        "兩個日期間有幾個工作天？自動扣除週末假日｜500+ 免費工具",
        "輸入起始和結束日期，自動計算工作天數、扣除週末與國定假日。還有年假計算、時薪換算、排班表等 500+ 免費線上工具。"
    ),
    "tools/salary-raise.html": (
        "加薪後實領多少？輸入調幅算出新月薪年薪｜薪資工具系列",
        "輸入目前薪資和調薪%，一鍵算出新月薪、年薪、實際增加金額。同系列還有時薪換算、離職率、人事成本等 20+ 薪資工具。"
    ),
    "tools/pool-volume.html": (
        "泳池要裝多少水？輸入長寬深算公升噸數｜工程計算工具",
        "輸入泳池長寬深，立即算出需要幾公升、幾噸水。同類工具：碎石用量、油漆面積、磁磚數量、瀝青噸數等 30+ 工程計算機。"
    ),
    "tools/paper-weight.html": (
        "這批紙有多重？輸入尺寸磅數張數秒算｜GSM 換算 + 500 工具",
        "輸入紙張尺寸、基重(GSM)、數量，立即算出總重量。還有 GSM 磅重換算、材積重、毛線重量等 500+ 免費計算工具。"
    ),
    "tools/probability-calculator.html": (
        "這件事發生的機率多大？機率 × 排列組合計算機｜數學工具",
        "輸入事件條件，算出發生機率、期望值、排列組合數。同系列：標準差、複利、百分比、統計分析等 20+ 數學統計工具。"
    ),
    "tools/shipping-cost.html": (
        "寄這個包裹要多少錢？運費估算工具｜材積重 + 物流計算",
        "輸入包裹重量和尺寸，估算運費並比較材積重與實重。同系列：材積重計算、關稅估算、物流成本等電商物流工具。"
    ),
    "tools/ohms-law.html": (
        "電壓電流電阻怎麼算？歐姆定律 V=IR 計算機｜電子工具",
        "輸入 V、I、R 任意兩個值，自動算出第三個＋功率(W)。還有電池續航、電費估算、電動車里程等電力能源工具。"
    ),
    "tools/standard-deviation.html": (
        "標準差怎麼算？貼上數據一鍵算出｜統計工具 + 500 計算機",
        "輸入數據，立即算出標準差、變異數、平均值、中位數。同系列：機率計算、複利、迴歸分析等 500+ 免費計算工具。"
    ),
    "tools/churn-rate.html": (
        "客戶流失率多少才正常？Churn Rate 計算機｜SaaS 指標工具",
        "輸入期初客戶數和流失數，算出月/年 Churn Rate＋產業平均對照。同系列：LTV、CAC、ARR、MRR 等 20+ SaaS 指標工具。"
    ),
    "tools/ev-range.html": (
        "電動車充滿能跑多遠？續航里程計算機｜汽車 + 能源工具",
        "輸入電池容量(kWh)和能耗(Wh/km)，算出滿電續航。同系列：油耗計算、輪胎尺寸換算、停車費、車貸試算等汽車工具。"
    ),
    "tools/gravel-calculator.html": (
        "鋪路要幾噸碎石？輸入面積厚度秒算｜建築工程計算工具",
        "輸入面積和厚度，算出碎石噸數和費用。同系列：瀝青、磁磚、油漆、混凝土、壁紙等 30+ 建築裝修計算工具。"
    ),
    "tools/dimensional-weight.html": (
        "包裹材積重多少？輸入長寬高算運費計費重｜物流工具",
        "輸入包裹長寬高，算出材積重並對比實重。支援 DHL/FedEx/UPS 係數。同系列：運費估算、關稅、物流成本等電商工具。"
    ),
    "tools/startup-valuation.html": (
        "你的新創值多少錢？公司估值計算機｜創業 + 財務工具",
        "輸入營收、成長率、產業別，用 DCF 和乘數法估算估值。同系列：EBITDA 估值、股權稀釋、損益兩平等 50+ 財務工具。"
    ),
    "tools/cost-of-living.html": (
        "搬到那個城市要花多少？生活費比較工具｜500+ 計算機",
        "比較兩個城市的房租、餐飲、交通、日用品開銷差異。還有薪資換算、匯率、稅務、退休金等 500+ 免費計算工具。"
    ),
    "tools/gsm-converter.html": (
        "GSM 磅重怎麼換算？紙張布料克重轉換｜單位換算工具",
        "GSM(g/m2) 與磅重(lb)一鍵互轉＋常用克重對照表。同系列：料理單位、鞋碼、輪胎尺寸、時區等 20+ 單位換算工具。"
    ),
    "tools/markup-margin.html": (
        "Markup 和 Margin 差多少？輸入成本售價秒算｜定價工具",
        "一鍵算出加成率(Markup)和毛利率(Margin)的差異＋公式對照表。同系列：營收計算、損益兩平、ROI 等 50+ 商業工具。"
    ),
    "tools/cooking-weight-volume.html": (
        "1杯麵粉幾克？廚房重量容量換算｜30+ 食材 + 料理工具",
        "杯、湯匙、茶匙、毫升、公克互轉，涵蓋 30+ 食材。同系列：食譜份量調整、卡路里、營養素、咖啡因等料理健康工具。"
    ),
    "tools/paint-calculator.html": (
        "粉刷牆壁要買幾桶油漆？輸入坪數秒算｜裝修計算工具",
        "輸入牆面面積、門窗數、層數，算出油漆公升數。同系列：磁磚、碎石、壁紙、混凝土等 30+ 裝修工程計算工具。"
    ),
    "tools/salary-to-hourly.html": (
        "月薪換時薪是多少？一鍵換算｜薪資計算工具系列",
        "輸入月薪或年薪，算出時薪。支援週 40/44 小時制。同系列：加薪計算、離職率、人事成本、年假天數等 20+ 人資工具。"
    ),
    "tools/stock-gain-loss.html": (
        "這筆股票賺了還是賠了？損益計算機｜50+ 投資工具",
        "輸入買賣價、股數、手續費，算出淨損益和報酬率。同系列：複利、ROI、殖利率、本益比、風險報酬比等 50+ 投資工具。"
    ),
    "tools/cooking-converter.html": (
        "杯 湯匙 毫升 盎司怎麼換？料理單位換算｜廚房工具",
        "杯、大匙、小匙、毫升、盎司一鍵互轉。同系列：食材重量換算、卡路里、食譜份量、咖啡因攝取量等料理健康工具。"
    ),
    "tools/yarn-weight.html": (
        "毛線幾號？紗線粗細 × 建議針號對照｜手作工具",
        "查詢紗線重量等級（Lace~Jumbo）對應的棒針鉤針號數和 gauge。還有紙張重量、布料 GSM、料理換算等實用工具。"
    ),
    "tools/ebitda-valuation.html": (
        "用 EBITDA 算公司值多少？企業估值計算機｜財務工具",
        "輸入 EBITDA 和產業乘數，算出企業價值(EV)。同系列：新創估值、股權稀釋、DCF、本益比等 50+ 財務分析工具。"
    ),
    "tools/time-zone-converter.html": (
        "現在那邊幾點？全球時區換算｜500+ 城市 + 日期時間工具",
        "選擇兩個時區立即看對應時間，支援 500+ 城市＋夏令時間。同系列：工作天數、年假、倒數日等日期時間計算工具。"
    ),
    "tools/rental-yield.html": (
        "這間房租金報酬率多少？投報率計算機｜房地產工具",
        "輸入房價和月租金，算出毛/淨報酬率。同系列：房貸試算、裝修成本、坪數換算、印花稅等 15+ 房地產計算工具。"
    ),
    "tools/compound-interest.html": (
        "你的錢20年後變多少？複利計算機｜定期定額 + 50 投資工具",
        "輸入本金、利率、年數，算出複利終值＋每月定期定額試算。同系列：ROI、殖利率、退休金、CAGR 等 50+ 投資工具。"
    ),

    # ============================================================
    # TOOLS - English
    # ============================================================
    "tools/en/battery-calculator.html": (
        "How Long Will Your Battery Last? mAh to Hours Calculator | 500+ Tools",
        "Enter battery capacity (mAh) and consumption (mA) to calculate battery life in hours. Works for phones, power banks, IoT, RC. Plus 500+ free calculators for finance, health, engineering."
    ),
    "tools/en/class-rank.html": (
        "What's Your Class Rank? GPA Percentile Calculator | Education Tools",
        "Enter your GPA or scores and class size to see your exact rank and percentile. Also: grade calculators, study planners, and 500+ free online tools."
    ),
    "tools/en/parking-cost.html": (
        "How Much Will Parking Cost? Rate & Duration Calculator | Auto Tools",
        "Enter hourly/daily rate and duration to get total parking cost. Also: fuel cost, tire size converter, EV range, car loan — 15+ auto calculators."
    ),
    "tools/en/court-fee.html": (
        "How Much Are Court Fees? Filing Cost Calculator | Legal Tools",
        "Enter case type and claim amount to estimate filing fees. Also: notary fees, trademark costs, and 15+ legal compliance calculators."
    ),
    "tools/en/equity-dilution.html": (
        "How Much Equity Will You Lose? Dilution Calculator | Startup Tools",
        "Enter ownership %, investment, and valuation to see post-round equity. Also: startup valuation, EBITDA, break-even — 20+ startup and finance tools."
    ),
    "tools/en/medication-cost-compare.html": (
        "Which Medication Is Cheaper? Drug Price Comparison | Health Tools",
        "Compare monthly costs of two medications side by side. Also: BMI, calorie, caffeine, water intake — 20+ free health calculators."
    ),
    "tools/en/notary-fee.html": (
        "How Much Does a Notary Cost? Fee Calculator | Legal Tools",
        "Estimate notary fees by document type and state. Also: court fees, trademark costs, and 500+ free online calculators."
    ),
    "tools/en/pb-ratio.html": (
        "Is This Stock Undervalued? P/B Ratio Calculator | 50+ Finance Tools",
        "Calculate Price-to-Book ratio + industry benchmarks. Also: P/E ratio, ROI, dividend yield, DCF — 50+ free investment calculators."
    ),

    # ============================================================
    # TOOLS - Japanese
    # ============================================================
    "tools/ja/asphalt-calculator.html": (
        "アスファルト何トン必要？面積から即計算｜30+ 建設ツール",
        "面積と厚さを入力してアスファルト量・費用を即計算。砂利・タイル・ペンキ・コンクリートなど30以上の建設計算ツールも。"
    ),
    "tools/ja/caffeine-calculator.html": (
        "カフェイン摂りすぎ？1日の摂取量チェック｜健康ツール",
        "体重と飲料を入力して安全範囲をチェック。BMI・カロリー・水分摂取量など20以上の無料健康計算ツールも。"
    ),
    "tools/ja/tile-calculator.html": (
        "タイル何枚必要？面積から枚数・費用を計算｜リフォームツール",
        "部屋面積とタイルサイズで必要枚数を即計算。ペンキ・砂利・壁紙・アスファルトなど30以上のリフォーム計算ツールも。"
    ),
    "tools/ja/paper-weight.html": (
        "紙の重さは何kg？坪量から即計算｜GSM換算 + 500 ツール",
        "サイズ・坪量・枚数から紙の総重量を即計算。GSM換算・材積重量・生地重量など500以上の無料計算ツールも。"
    ),
    "tools/ja/cooking-weight-volume.html": (
        "大さじ1は何グラム？調味料の変換ツール｜料理計算",
        "大さじ・小さじ・カップ・mL・gを相互変換。30種以上の食材対応。カロリー・レシピ分量・カフェイン量などの料理ツールも。"
    ),
    "tools/ja/gear-ratio.html": (
        "ギア比はいくつ？歯数から変速比を即計算｜エンジニアツール",
        "駆動・被動歯車の歯数からギア比・回転数を即計算。オームの法則・単位換算・標準偏差など500以上のエンジニア向けツール。"
    ),

    # ============================================================
    # TOOLS - Indonesian
    # ============================================================
    "tools/id/future-value.html": (
        "Uangmu Jadi Berapa? Kalkulator Investasi | 500+ Alat Gratis",
        "Masukkan jumlah, bunga, dan waktu untuk hitung nilai investasi masa depan. Plus 500+ kalkulator gratis: KPR, pajak, kesehatan, dan lainnya."
    ),

    # ============================================================
    # BLOG
    # ============================================================
    "blog/profit-loss-ratio.html": (
        "損益比怎麼算？圖解教學＋免費損益比計算機｜投資入門",
        "最簡單的方式教你算損益比，判斷一筆交易值不值得做。含實戰範例、進出場圖解，還有 50+ 免費投資計算工具。"
    ),
    "blog/en/kd-indicator.html": (
        "KD Indicator: How to Read Signals and Avoid Fakeouts | Trading Guide",
        "Learn KD (Stochastic) indicator: overbought/oversold, golden cross, divergence. With chart examples. Plus 50+ free trading and investment tools."
    ),
    "blog/support-resistance.html": (
        "支撐位和壓力位怎麼找？3種方法畫出關鍵價位｜股票教學",
        "教你用均線、前高前低、量價三種方法找支撐壓力。搭配免費個股分析工具（多空雷達＋K棒辨識），一鍵產出報告。"
    ),
}

# ============================================================
# HOMEPAGE + LANDING
# ============================================================

SPECIAL_REWRITES = {
    "homepage.html": (
        "SoftGlow｜500+ 免費計算工具 × 台股 AI 分析 × 全球彩票選號",
        "500+ 免費線上計算工具（金融、房貸、健康、工程、料理），台股個股 AI 分析報告，15 國彩票開獎＋12 種智慧選號。10 種語言全球適用。"
    ),
    "landing.html": (
        "台股 AI 分析｜多空雷達 × K棒型態 × 支撐壓力，一鍵出報告",
        "輸入股票代號，AI 分析多空雷達四格訊號、K棒型態辨識、支撐壓力位、葛蘭碧買點。免費產出完整報告。還有 500+ 計算工具和全球彩票選號。"
    ),
}

# ============================================================
# main.py manual changes (printed at end)
# ============================================================

MAINPY_NOTES = """
=== main.py 需手動修改的 Title ===

1. /stock/landing <title>:
   新: 台股 AI 分析｜多空雷達 × K棒型態 × 支撐壓力，一鍵出報告

2. /report/{slug} <title>:
   新: {stock_name}({code}) 能買嗎？多空雷達＋支撐壓力完整分析｜線上有位

3. /picks <title>:
   新: 今日精選股｜AI 篩出的強勢股＋進場理由與停損位
"""

# ============================================================
# Lottery title suggestions (Next.js, different repo)
# ============================================================

LOTTERY_NOTES = """
=== lottery.softglow-ai.com Title 建議 ===
(需改 D:\\全球彩票資訊網\\lottery-hub 的 page.tsx)

/zh-TW (首頁):
  15國彩票即時開獎＋12種選號工具（星座、生日、夢境、AI、八字）

/zh-TW/taiwan-lotto:
  大樂透最新開獎號碼＋12種選號（星座、生日、夢境、AI）｜完整統計

/zh-TW/taiwan-lotto/history:
  大樂透歷期開獎號碼查詢｜搜尋任一期＋冷熱號分析＋選號工具

/zh-TW/japan-loto6:
  日本樂透6 最新開獎＋12種選號工具（生肖、八字、AI）｜中獎統計

/zh-TW/uk-lotto:
  英國樂透最新開獎號碼＋12種選號（星座、夢境、AI）｜歷史統計

/en/korea-lotto (192 impr!):
  Korea Lotto 6/45 Latest Results + 12 Number Pickers (Zodiac, Birthday, Dream, AI)

/en/japan-loto6/history (50 impr):
  Japan Loto 6 Past Results — Search Any Draw + Hot/Cold Numbers + 12 Picker Tools

/ko/korea-lotto/results (15 impr):
  로또 6/45 최신 당첨번호 + 12가지 번호 선택기 (별자리, 생일, 꿈, AI) | 통계 분석

/en/tools/tax-calculator (12 impr):
  How Much Tax on Lottery Winnings? Calculator for 15 Countries + Currency Converter

/en/euromillions/history:
  EuroMillions All Past Results — Searchable Since 2004 + Hot/Cold Analysis

/en/uk-lotto:
  UK Lotto Latest Numbers + 12 Smart Pickers (Zodiac, Birthday, AI) + Statistics

/en/mega-sena/statistics:
  Mega-Sena: Which Numbers Hit Most? Hot/Cold Stats + 12 Number Picker Tools

/ja/tools/odds-compare:
  どの宝くじが当たりやすい？15種の当選確率比較＋12種の番号選びツール

/en/powerball:
  Powerball Latest Draw + 12 Number Generators (Zodiac, Birthday, Dream, AI Picks)

/en/mega-millions:
  Mega Millions Tonight's Numbers + 12 Smart Pickers + Win Probability Calculator
"""


def rewrite_title_desc(filepath, new_title, new_desc):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
    except FileNotFoundError:
        return False, "file not found"
    except Exception as e:
        return False, str(e)

    original = html

    # Replace <title>
    title_pat = r'<title>.*?</title>'
    if re.search(title_pat, html, re.DOTALL | re.IGNORECASE):
        html = re.sub(title_pat, f'<title>{new_title}</title>', html, count=1, flags=re.DOTALL | re.IGNORECASE)
    else:
        html = html.replace('<head>', f'<head>\n<title>{new_title}</title>', 1)

    # Replace <meta description>
    desc_pat = r'<meta\s+name="description"\s+content="[^"]*"'
    desc_pat2 = r'<meta\s+content="[^"]*"\s+name="description"'
    if re.search(desc_pat, html, re.IGNORECASE):
        html = re.sub(desc_pat, f'<meta name="description" content="{new_desc}"', html, count=1, flags=re.IGNORECASE)
    elif re.search(desc_pat2, html, re.IGNORECASE):
        html = re.sub(desc_pat2, f'<meta name="description" content="{new_desc}"', html, count=1, flags=re.IGNORECASE)
    else:
        html = html.replace('</title>', f'</title>\n<meta name="description" content="{new_desc}">', 1)

    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        return True, "ok"
    return False, "no change"


def main():
    print(f"Frontend: {FRONTEND}")
    print(f"Rewrites: {len(REWRITES) + len(SPECIAL_REWRITES)} pages")
    print()

    fixed = 0
    not_found = 0

    print("=" * 60)
    print("Tool + Blog pages")
    print("=" * 60)
    for rel, (t, d) in sorted(REWRITES.items()):
        fp = os.path.join(FRONTEND, rel)
        ok, msg = rewrite_title_desc(fp, t, d)
        if ok:
            fixed += 1
            print(f"  [OK] {rel}")
        else:
            not_found += 1
            print(f"  [SKIP] {rel} - {msg}")

    print()
    print("=" * 60)
    print("Homepage + Landing")
    print("=" * 60)
    for fn, (t, d) in SPECIAL_REWRITES.items():
        fp = os.path.join(FRONTEND, fn)
        ok, msg = rewrite_title_desc(fp, t, d)
        if ok:
            fixed += 1
            print(f"  [OK] {fn}")
        else:
            # Try alt name
            alt = "index.html" if fn == "homepage.html" else "homepage.html"
            fp2 = os.path.join(FRONTEND, alt)
            ok2, _ = rewrite_title_desc(fp2, t, d)
            if ok2:
                fixed += 1
                print(f"  [OK] {alt} (alt)")
            else:
                not_found += 1
                print(f"  [SKIP] {fn} - {msg}")

    print()
    print("=" * 60)
    print(f"DONE: {fixed} fixed, {not_found} skipped")
    print("=" * 60)

    print(MAINPY_NOTES)
    print(LOTTERY_NOTES)

    print("Next:")
    print("  cd D:\\xian-shang-you-wei")
    print('  git add -A && git commit -m "seo: titles rewrite for CTR" && git push')


if __name__ == '__main__':
    main()
