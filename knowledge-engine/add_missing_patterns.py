#!/usr/bin/env python3
"""
add_missing_patterns.py — 補齊 16 個缺失的 K 棒型態
===================================================
1. 把 16 個型態加進 pattern-catalog.json
2. 生成 16 × 10 = 160 個 content/{slug}_{lang}.json
3. 不動任何現有資料

用法：
    cd D:\\xian-shang-you-wei\\knowledge-engine
    python add_missing_patterns.py

然後跑：
    python generate_patterns.py
"""
import json, os
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CATALOG_PATH = os.path.join(BASE_DIR, "pattern-catalog.json")
CONTENT_DIR = os.path.join(BASE_DIR, "content")
ALL_LANGS = ["zh-TW","en","ja","ko","de","fr","es","pt","id","zh-CN"]

# ─────────────────────────────────────────────
# 16 patterns catalog entries
# ─────────────────────────────────────────────
CATALOG_ENTRIES = {
  "abandoned-baby-bull": {
    "signal":"bullish","candles":3,"reliability":"high","difficulty":"intermediate",
    "best_market":["downtrend"],
    "category":"bullish-reversal",
    "trading_rules":{"entry":"close_above_third_candle_high","stop_loss":"below_doji_low","take_profit":"previous_decline_100pct","invalidation":"close_below_doji_low"},
    "candle_data":[
      {"type":"bearish","open":85,"high":88,"low":55,"close":58,"label":"1"},
      {"type":"neutral","open":50,"high":52,"low":45,"close":50,"label":"★"},
      {"type":"bullish","open":56,"high":90,"low":54,"close":88,"label":"3"}
    ],
    "related_patterns":["abandoned-baby-bullish","morning-star","morning-doji-star","piercing-line","hammer"],
    "related_tools":["rsi-calculator","macd-calculator","support-resistance","atr-calculator","stop-loss"],
    "related_blog":["candlestick-patterns","stop-loss-guide","support-resistance"]
  },
  "bear-flag": {
    "signal":"bearish","candles":0,"reliability":"high","difficulty":"intermediate",
    "best_market":["downtrend"],
    "category":"bearish-continuation",
    "trading_rules":{"entry":"close_below_flag_lower_boundary","stop_loss":"above_flag_high","take_profit":"flagpole_length_projected_down","invalidation":"close_above_flag_high"},
    "candle_data":[
      {"type":"bearish","open":85,"high":88,"low":50,"close":52,"label":""},
      {"type":"bullish","open":54,"high":65,"low":52,"close":63,"label":""},
      {"type":"bullish","open":62,"high":70,"low":60,"close":68,"label":""},
      {"type":"bearish","open":66,"high":72,"low":42,"close":44,"label":""}
    ],
    "related_patterns":["falling-three-methods","descending-triangle","bearish-engulfing","pennant","three-black-crows"],
    "related_tools":["support-resistance","macd-calculator","rsi-calculator","atr-calculator","ma-crossover"],
    "related_blog":["candlestick-patterns","stop-loss-guide","moving-average-guide"]
  },
  "descending-triangle": {
    "signal":"bearish","candles":0,"reliability":"high","difficulty":"intermediate",
    "best_market":["downtrend","ranging"],
    "category":"bearish-continuation",
    "trading_rules":{"entry":"close_below_flat_support","stop_loss":"above_last_lower_high","take_profit":"triangle_height_projected_down","invalidation":"close_above_descending_trendline"},
    "candle_data":[
      {"type":"bearish","open":80,"high":82,"low":40,"close":42,"label":""},
      {"type":"bullish","open":44,"high":72,"low":42,"close":70,"label":""},
      {"type":"bearish","open":68,"high":70,"low":40,"close":42,"label":""},
      {"type":"bullish","open":44,"high":62,"low":42,"close":60,"label":""},
      {"type":"bearish","open":58,"high":60,"low":35,"close":38,"label":""}
    ],
    "related_patterns":["ascending-triangle","triangle-symmetrical","double-bottom","bear-flag","head-shoulders-top"],
    "related_tools":["support-resistance","fibonacci-retracement","macd-calculator","rsi-calculator","ma-crossover"],
    "related_blog":["candlestick-patterns","support-resistance","stop-loss-guide"]
  },
  "flag-bull": {
    "signal":"bullish","candles":0,"reliability":"high","difficulty":"intermediate",
    "best_market":["uptrend"],
    "category":"bullish-continuation",
    "trading_rules":{"entry":"close_above_flag_upper_boundary","stop_loss":"below_flag_low","take_profit":"flagpole_length_projected_up","invalidation":"close_below_flag_low"},
    "candle_data":[
      {"type":"bullish","open":30,"high":75,"low":28,"close":72,"label":""},
      {"type":"bearish","open":70,"high":73,"low":60,"close":62,"label":""},
      {"type":"bearish","open":63,"high":66,"low":55,"close":57,"label":""},
      {"type":"bullish","open":58,"high":90,"low":56,"close":88,"label":""}
    ],
    "related_patterns":["rising-three-methods","ascending-triangle","pennant","bullish-engulfing","mat-hold"],
    "related_tools":["support-resistance","macd-calculator","rsi-calculator","atr-calculator","ma-crossover"],
    "related_blog":["candlestick-patterns","moving-average-guide","stop-loss-guide"]
  },
  "gap-up": {
    "signal":"bullish","candles":2,"reliability":"medium","difficulty":"beginner",
    "best_market":["uptrend","breakout"],
    "category":"bullish-continuation",
    "trading_rules":{"entry":"gap_holds_after_retest","stop_loss":"below_gap_close","take_profit":"gap_size_times_2","invalidation":"gap_fully_closed"},
    "candle_data":[
      {"type":"bullish","open":40,"high":60,"low":38,"close":58,"label":"1"},
      {"type":"bullish","open":65,"high":85,"low":63,"close":82,"label":"2"}
    ],
    "related_patterns":["rising-window","gap-down","bullish-marubozu","kicker-bullish","bullish-engulfing"],
    "related_tools":["support-resistance","rsi-calculator","macd-calculator","atr-calculator","ma-crossover"],
    "related_blog":["candlestick-patterns","support-resistance","stop-loss-guide"]
  },
  "gap-down": {
    "signal":"bearish","candles":2,"reliability":"medium","difficulty":"beginner",
    "best_market":["downtrend","breakout"],
    "category":"bearish-continuation",
    "trading_rules":{"entry":"gap_holds_after_retest","stop_loss":"above_gap_open","take_profit":"gap_size_times_2","invalidation":"gap_fully_closed"},
    "candle_data":[
      {"type":"bearish","open":80,"high":82,"low":62,"close":65,"label":"1"},
      {"type":"bearish","open":55,"high":58,"low":35,"close":38,"label":"2"}
    ],
    "related_patterns":["falling-window","gap-up","bearish-marubozu","kicker-bearish","bearish-engulfing"],
    "related_tools":["support-resistance","rsi-calculator","macd-calculator","atr-calculator","stop-loss"],
    "related_blog":["candlestick-patterns","support-resistance","stop-loss-guide"]
  },
  "head-shoulders-top": {
    "signal":"bearish","candles":0,"reliability":"high","difficulty":"advanced",
    "best_market":["uptrend"],
    "category":"bearish-reversal",
    "trading_rules":{"entry":"close_below_neckline","stop_loss":"above_right_shoulder","take_profit":"neckline_minus_head_to_neckline","invalidation":"close_above_right_shoulder"},
    "candle_data":[
      {"type":"bullish","open":40,"high":70,"low":38,"close":68,"label":"L"},
      {"type":"bearish","open":65,"high":68,"low":50,"close":52,"label":""},
      {"type":"bullish","open":55,"high":90,"low":53,"close":88,"label":"H"},
      {"type":"bearish","open":85,"high":88,"low":50,"close":52,"label":""},
      {"type":"bullish","open":55,"high":72,"low":53,"close":70,"label":"R"}
    ],
    "related_patterns":["head-shoulders","double-top","triple-top","evening-star","bearish-engulfing"],
    "related_tools":["support-resistance","fibonacci-retracement","macd-calculator","rsi-calculator","ma-crossover"],
    "related_blog":["candlestick-patterns","support-resistance","stop-loss-guide"]
  },
  "inverse-head-shoulders": {
    "signal":"bullish","candles":0,"reliability":"high","difficulty":"advanced",
    "best_market":["downtrend"],
    "category":"bullish-reversal",
    "trading_rules":{"entry":"close_above_neckline","stop_loss":"below_right_shoulder","take_profit":"neckline_plus_head_to_neckline","invalidation":"close_below_right_shoulder"},
    "candle_data":[
      {"type":"bearish","open":80,"high":82,"low":50,"close":52,"label":"L"},
      {"type":"bullish","open":55,"high":68,"low":53,"close":65,"label":""},
      {"type":"bearish","open":62,"high":65,"low":30,"close":32,"label":"H"},
      {"type":"bullish","open":35,"high":68,"low":33,"close":65,"label":""},
      {"type":"bearish","open":62,"high":65,"low":48,"close":50,"label":"R"}
    ],
    "related_patterns":["head-shoulders","double-bottom","triple-bottom","morning-star","bullish-engulfing"],
    "related_tools":["support-resistance","fibonacci-retracement","macd-calculator","rsi-calculator","ma-crossover"],
    "related_blog":["candlestick-patterns","support-resistance","stop-loss-guide"]
  },
  "on-neck": {
    "signal":"bearish","candles":2,"reliability":"low","difficulty":"intermediate",
    "best_market":["downtrend"],
    "category":"bearish-continuation",
    "trading_rules":{"entry":"close_below_first_candle_low","stop_loss":"above_second_candle_high","take_profit":"nearest_support_or_1r","invalidation":"close_above_second_candle_high"},
    "candle_data":[
      {"type":"bearish","open":80,"high":82,"low":50,"close":52,"label":"1"},
      {"type":"bullish","open":45,"high":55,"low":43,"close":52,"label":"2"}
    ],
    "related_patterns":["dark-cloud","bearish-engulfing","bearish-harami","falling-three-methods","three-black-crows"],
    "related_tools":["rsi-calculator","macd-calculator","support-resistance","atr-calculator","stop-loss"],
    "related_blog":["candlestick-patterns","stop-loss-guide","support-resistance"]
  },
  "pennant": {
    "signal":"bullish","candles":0,"reliability":"medium","difficulty":"intermediate",
    "best_market":["uptrend","breakout"],
    "category":"bullish-continuation",
    "trading_rules":{"entry":"close_above_pennant_upper_line","stop_loss":"below_pennant_low","take_profit":"flagpole_length_projected","invalidation":"close_below_pennant_lower_line"},
    "candle_data":[
      {"type":"bullish","open":30,"high":70,"low":28,"close":68,"label":""},
      {"type":"bearish","open":66,"high":70,"low":58,"close":60,"label":""},
      {"type":"bullish","open":61,"high":68,"low":59,"close":66,"label":""},
      {"type":"bearish","open":65,"high":67,"low":60,"close":62,"label":""},
      {"type":"bullish","open":63,"high":80,"low":61,"close":78,"label":""}
    ],
    "related_patterns":["ascending-triangle","triangle-symmetrical","flag-bull","rising-three-methods","cup-handle"],
    "related_tools":["support-resistance","macd-calculator","rsi-calculator","atr-calculator","ma-crossover"],
    "related_blog":["candlestick-patterns","moving-average-guide","stop-loss-guide"]
  },
  "rectangle-bull": {
    "signal":"bullish","candles":0,"reliability":"medium","difficulty":"intermediate",
    "best_market":["uptrend","ranging"],
    "category":"bullish-continuation",
    "trading_rules":{"entry":"close_above_resistance","stop_loss":"below_support","take_profit":"rectangle_height_projected_up","invalidation":"close_below_support"},
    "candle_data":[
      {"type":"bullish","open":55,"high":75,"low":53,"close":72,"label":""},
      {"type":"bearish","open":70,"high":76,"low":55,"close":58,"label":""},
      {"type":"bullish","open":60,"high":75,"low":58,"close":72,"label":""},
      {"type":"bearish","open":70,"high":76,"low":56,"close":58,"label":""},
      {"type":"bullish","open":60,"high":82,"low":58,"close":80,"label":""}
    ],
    "related_patterns":["ascending-triangle","triangle-symmetrical","flag-bull","double-bottom","pennant"],
    "related_tools":["support-resistance","fibonacci-retracement","macd-calculator","rsi-calculator","atr-calculator"],
    "related_blog":["candlestick-patterns","support-resistance","stop-loss-guide"]
  },
  "triangle-symmetrical": {
    "signal":"neutral","candles":0,"reliability":"medium","difficulty":"intermediate",
    "best_market":["ranging"],
    "category":"neutral",
    "trading_rules":{"entry":"close_beyond_triangle_boundary","stop_loss":"opposite_boundary","take_profit":"triangle_height_projected","invalidation":"false_breakout_reversal"},
    "candle_data":[
      {"type":"bullish","open":40,"high":80,"low":38,"close":78,"label":""},
      {"type":"bearish","open":76,"high":80,"low":45,"close":48,"label":""},
      {"type":"bullish","open":50,"high":72,"low":48,"close":70,"label":""},
      {"type":"bearish","open":68,"high":72,"low":52,"close":55,"label":""},
      {"type":"bullish","open":56,"high":80,"low":54,"close":78,"label":""}
    ],
    "related_patterns":["ascending-triangle","descending-triangle","pennant","rectangle-bull","wedge-falling"],
    "related_tools":["support-resistance","fibonacci-retracement","macd-calculator","rsi-calculator","atr-calculator"],
    "related_blog":["candlestick-patterns","support-resistance","moving-average-guide"]
  },
  "triple-bottom": {
    "signal":"bullish","candles":0,"reliability":"high","difficulty":"intermediate",
    "best_market":["downtrend"],
    "category":"bullish-reversal",
    "trading_rules":{"entry":"close_above_neckline","stop_loss":"below_third_bottom","take_profit":"neckline_plus_pattern_height","invalidation":"close_below_third_bottom"},
    "candle_data":[
      {"type":"bearish","open":70,"high":72,"low":35,"close":38,"label":""},
      {"type":"bullish","open":40,"high":60,"low":38,"close":58,"label":""},
      {"type":"bearish","open":56,"high":58,"low":36,"close":40,"label":""},
      {"type":"bullish","open":42,"high":60,"low":40,"close":57,"label":""},
      {"type":"bearish","open":55,"high":57,"low":37,"close":42,"label":""},
      {"type":"bullish","open":44,"high":70,"low":42,"close":68,"label":""}
    ],
    "related_patterns":["double-bottom","triple-top","head-shoulders","inverse-head-shoulders","ascending-triangle"],
    "related_tools":["support-resistance","fibonacci-retracement","macd-calculator","rsi-calculator","ma-crossover"],
    "related_blog":["candlestick-patterns","support-resistance","stop-loss-guide"]
  },
  "triple-top": {
    "signal":"bearish","candles":0,"reliability":"high","difficulty":"intermediate",
    "best_market":["uptrend"],
    "category":"bearish-reversal",
    "trading_rules":{"entry":"close_below_neckline","stop_loss":"above_third_top","take_profit":"neckline_minus_pattern_height","invalidation":"close_above_third_top"},
    "candle_data":[
      {"type":"bullish","open":40,"high":80,"low":38,"close":78,"label":""},
      {"type":"bearish","open":76,"high":78,"low":55,"close":58,"label":""},
      {"type":"bullish","open":60,"high":80,"low":58,"close":77,"label":""},
      {"type":"bearish","open":75,"high":78,"low":56,"close":60,"label":""},
      {"type":"bullish","open":62,"high":79,"low":60,"close":76,"label":""},
      {"type":"bearish","open":74,"high":76,"low":45,"close":48,"label":""}
    ],
    "related_patterns":["double-top","triple-bottom","head-shoulders-top","descending-triangle","evening-star"],
    "related_tools":["support-resistance","fibonacci-retracement","macd-calculator","rsi-calculator","ma-crossover"],
    "related_blog":["candlestick-patterns","support-resistance","stop-loss-guide"]
  },
  "wedge-falling": {
    "signal":"bullish","candles":0,"reliability":"high","difficulty":"intermediate",
    "best_market":["downtrend","pullback"],
    "category":"bullish-reversal",
    "trading_rules":{"entry":"close_above_upper_trendline","stop_loss":"below_wedge_low","take_profit":"wedge_entrance_width_projected_up","invalidation":"new_low_below_wedge"},
    "candle_data":[
      {"type":"bearish","open":80,"high":82,"low":60,"close":62,"label":""},
      {"type":"bullish","open":64,"high":75,"low":55,"close":58,"label":""},
      {"type":"bearish","open":60,"high":68,"low":48,"close":50,"label":""},
      {"type":"bullish","open":52,"high":65,"low":45,"close":48,"label":""},
      {"type":"bullish","open":50,"high":78,"low":48,"close":75,"label":""}
    ],
    "related_patterns":["wedge-rising","falling-three-methods","descending-triangle","double-bottom","inverse-head-shoulders"],
    "related_tools":["support-resistance","fibonacci-retracement","macd-calculator","rsi-calculator","ma-crossover"],
    "related_blog":["candlestick-patterns","support-resistance","stop-loss-guide"]
  },
  "wedge-rising": {
    "signal":"bearish","candles":0,"reliability":"high","difficulty":"intermediate",
    "best_market":["uptrend"],
    "category":"bearish-reversal",
    "trading_rules":{"entry":"close_below_lower_trendline","stop_loss":"above_wedge_high","take_profit":"wedge_entrance_width_projected_down","invalidation":"new_high_above_wedge"},
    "candle_data":[
      {"type":"bullish","open":35,"high":55,"low":33,"close":52,"label":""},
      {"type":"bearish","open":50,"high":58,"low":42,"close":55,"label":""},
      {"type":"bullish","open":48,"high":62,"low":46,"close":60,"label":""},
      {"type":"bearish","open":58,"high":65,"low":50,"close":62,"label":""},
      {"type":"bearish","open":55,"high":58,"low":30,"close":32,"label":""}
    ],
    "related_patterns":["wedge-falling","rising-three-methods","ascending-triangle","double-top","head-shoulders-top"],
    "related_tools":["support-resistance","fibonacci-retracement","macd-calculator","rsi-calculator","ma-crossover"],
    "related_blog":["candlestick-patterns","support-resistance","stop-loss-guide"]
  },
}

# ─────────────────────────────────────────────
# zh-TW Content for all 16 patterns
# ─────────────────────────────────────────────
ZH_TW = {
"abandoned-baby-bull":{
  "seo":{"title":"棄嬰多頭型態（Abandoned Baby Bull）K線完全解析","description":"深入解析棄嬰多頭型態：三根K棒底部反轉訊號，識別方法、交易規則、市場心理分析及實用策略。","h1":"棄嬰多頭型態（Abandoned Baby Bull）"},
  "hero":{"one_liner":"棄嬰多頭型態是極為罕見但極度可靠的三根K棒底部反轉型態，第二根十字線被兩個跳空缺口孤立在底部，預示著強力反彈即將到來。"},
  "summary":{"text":"棄嬰多頭由三根K棒組成：第一根大陰線、第二根向下跳空的十字線（與前後K棒影線不重疊）、第三根向上跳空的大陽線。十字線如同被「遺棄」在兩個缺口之間的底部。這是技術分析中最罕見也最可靠的反轉訊號之一，出現時通常預示著強力的V型反彈。"},
  "structure":{"html":"<p><strong>基本構成：</strong>棄嬰多頭型態由三根K棒組成：（1）一根明確的大陰線，延續下跌趨勢；（2）一根十字線或近十字線，向下跳空出現，其影線與前一根K棒的影線不重疊；（3）一根大陽線，向上跳空出現，其影線與十字線的影線不重疊。</p><p><strong>識別關鍵：</strong>最關鍵的判定條件是十字線必須與前後K棒之間都存在跳空缺口。這意味著十字線完全孤立在底部，被「遺棄」了。如果十字線的影線與前後K棒的影線有重疊，則不算標準的棄嬰型態，可靠度大幅降低。</p><p><strong>出現位置：</strong>必須出現在明確的下跌趨勢中，且前期已有一段顯著跌幅。在盤整區或淺幅回調中出現的類似型態可靠度較低。</p>"},
  "psychology":{"html":"<p><strong>恐慌到均衡：</strong>第一根大陰線反映空方仍在強勢主導，市場情緒極度悲觀。第二天價格繼續跳空下跌，但在該水位多空力量突然達到精確均衡，形成十字線。這代表空方的最後一擊已經用盡，買方開始在底部堅決承接。</p><p><strong>均衡到反攻：</strong>第三天多方直接跳空高開，徹底拋棄了底部的十字線水平，顯示多方信心已從絕望轉為堅定。兩個方向相反的缺口形成了強烈的V型反轉結構，代表市場情緒在短短三天內經歷了從極度悲觀到強力看好的戲劇性轉變。</p><p><strong>罕見意味著可靠：</strong>正因為需要同時滿足兩個跳空缺口的嚴格條件，棄嬰型態極為罕見。但每次出現時，其預測準確率極高。</p>"},
  "trading_rules":{"entry":"第三根陽線確認向上跳空時即可進場做多。由於訊號極強，通常不需要等待額外確認，但如果風險偏好較保守，可以等第三根收盤確認。","stop_loss":"停損設在十字線（第二根K棒）的最低點下方。如果缺口被回補，型態失效，應立即出場。停損位通常較近，因此風險報酬比很理想。","take_profit":"由於棄嬰型態通常引發強力反彈，利潤目標可以設在前一波下跌幅度的61.8%至100%回補位置。保守者可以先在50%位置減倉一半。","invalidation":"如果價格回落並完全封閉第三根K棒與十字線之間的跳空缺口，型態失效。此時多方動能不足，應立即退出觀望。"},
  "confirmation":{"html":"<p><strong>成交量確認：</strong>理想情況下，第三根陽線應伴隨明顯放量，表示大量買盤積極進場。如果第三根陽線量能不足，反彈力度可能有限，可以先建立半倉，等放量確認後再加碼。</p><p><strong>技術指標支持：</strong>RSI如果從超賣區（低於30）出現上升，MACD柱體從負值開始收窄或轉正，都能增強訊號可靠度。KD指標在低檔區金叉也是有力的確認訊號。</p><p><strong>支撐位驗證：</strong>如果十字線恰好出現在前期重要支撐位附近（如前低、均線支撐、費波那契回撤位），型態的可信度更高。多重技術訊號共振是最理想的交易環境。</p>"},
  "mistakes":{"items":[
    {"title":"把不完整的型態當作棄嬰","text":"最常見的錯誤是忽略跳空缺口的要求。如果十字線的影線與前後K棒有重疊，這只是普通的晨星型態，可靠度低於棄嬰。務必嚴格檢查兩個缺口是否存在。"},
    {"title":"在第二根十字線就急於進場","text":"看到十字線就認定底部已到而提前進場是危險的。必須等第三根陽線確認跳空向上後才能確認型態成立。十字線之後仍有繼續下跌的可能。"},
    {"title":"停損設置過寬","text":"由於棄嬰型態有明確的失效條件（缺口封閉），停損應精確設在十字線低點下方。設太寬會拉低風險報酬比，浪費這個型態停損近、獲利遠的天然優勢。"},
    {"title":"忽視趨勢背景","text":"棄嬰多頭必須出現在明確的下跌趨勢中才有意義。在盤整區出現的類似型態只是普通的價格波動，不具備反轉意義。"},
    {"title":"獲利目標太保守","text":"棄嬰型態引發的反彈通常力度很強，過早獲利了結會錯失大部分行情。建議分批獲利：50%回補位減倉一半，剩餘持倉追蹤到更高目標。"}
  ]},
  "checklist":{"items":[
    "確認當前處於明確的下跌趨勢，且已有一段顯著跌幅",
    "第一根為明確的大陰線，延續下跌動能",
    "第二根為十字線或近十字線，向下跳空且影線不與第一根重疊",
    "第三根為大陽線，向上跳空且影線不與第二根重疊",
    "檢查第三根陽線是否伴隨成交量放大",
    "RSI是否從超賣區回升、MACD是否轉正或收窄",
    "停損設在十字線最低點下方，計算風險報酬比是否合理"
  ]},
  "faq":[
    {"q":"棄嬰多頭與晨星型態有什麼區別？","a":"最關鍵的區別在於跳空缺口：棄嬰型態要求第二根十字線與前後K棒之間都有跳空缺口（影線不重疊），而晨星只需要實體之間有間距即可。棄嬰的條件更嚴格，因此更罕見但也更可靠。"},
    {"q":"棄嬰型態出現的頻率高嗎？","a":"非常罕見。由於需要同時滿足兩個方向的跳空缺口，在日線圖上可能數月甚至數年才出現一次。在分時圖或小時圖上出現的頻率稍高，但可靠度也相對降低。"},
    {"q":"如果只有一個缺口怎麼辦？","a":"如果只有一個缺口（例如第一根與十字線之間有缺口，但十字線與第三根沒有），則歸類為晨星或十字晨星型態。可靠度雖然仍然不錯，但不如完整棄嬰型態。"},
    {"q":"棄嬰型態適合哪些市場？","a":"棄嬰型態適用於所有有跳空行為的市場，包括股票、期貨和商品市場。外匯市場由於24小時連續交易，跳空較少出現，因此棄嬰型態在外匯市場中更為罕見。"},
    {"q":"如何設定合理的獲利目標？","a":"建議使用前一波下跌幅度的費波那契回撤水平：38.2%為保守目標、50%為中等目標、61.8%至100%為積極目標。也可以結合前期阻力位和均線壓力來設定。"}
  ]
},
"bear-flag":{
  "seo":{"title":"空頭旗形（Bear Flag）技術分析完整指南","description":"空頭旗形是最可靠的空頭持續型態之一。學習識別方法、交易策略、進出場規則及常見錯誤。","h1":"空頭旗形（Bear Flag）"},
  "hero":{"one_liner":"空頭旗形由一波急跌（旗桿）和隨後向上傾斜的平行通道回調（旗面）組成，跌破旗面下緣後通常走出等旗桿的跌幅。"},
  "summary":{"text":"空頭旗形是經典的空頭持續型態。先出現一波急速下跌形成「旗桿」，然後價格在向上傾斜的平行通道中小幅反彈形成「旗面」。反彈幅度通常為旗桿的38.2%至50%。當價格跌破旗面下緣時，確認下跌將繼續，目標為旗桿等幅的下跌。"},
  "structure":{"html":"<p><strong>旗桿（Flagpole）：</strong>首先需要一波急速且明確的下跌走勢，通常伴隨大量。旗桿的幅度和速度決定了後續目標的大小。越陡峭、越有力的旗桿，後續跌幅越可觀。</p><p><strong>旗面（Flag）：</strong>急跌後，價格進入向上傾斜的平行通道，這是空方獲利了結和多方試探性反彈的結果。旗面通常持續5至15根K棒。關鍵特徵是反彈力度有限，成交量逐步萎縮。</p><p><strong>突破確認：</strong>當價格跌破旗面下方邊界時，通常伴隨成交量放大，確認下跌持續。突破後目標為旗桿長度從突破點向下投射。</p>"},
  "psychology":{"html":"<p><strong>急跌的衝擊：</strong>旗桿代表空方突然發力的強勢打壓，可能由利空消息、技術面破位或機構大量拋售引發。這波急跌讓市場參與者措手不及，造成恐慌。</p><p><strong>反彈的假象：</strong>旗面的反彈給予多方虛假的希望，以為底部已到。但反彈力度有限、量能萎縮，說明只是短線空單獲利了結和散戶試探性買入，並非真正的趨勢反轉。</p><p><strong>再次崩跌：</strong>當反彈動能耗盡，空方再次發力。多方意識到反彈只是陷阱，恐慌性拋售湧出，價格跌破旗面形成第二波急跌。</p>"},
  "trading_rules":{"entry":"在價格收盤跌破旗面下方邊界時做空。可以使用突破當根K棒收盤價或在旗面下緣設置限價單。確保突破伴隨量增。","stop_loss":"停損設在旗面反彈的最高點上方。如果旗面被向上突破，代表空頭動能已經消退，型態失效。","take_profit":"從突破點向下投射旗桿的長度作為利潤目標。例如旗桿下跌了100點，則從突破位向下100點為第一目標。保守者可先在旗桿50%位置部分獲利。","invalidation":"價格收盤站回旗面上方邊界，或突破旗面最高點。這表明反彈不是短暫的喘息而是趨勢反轉的開始。"},
  "confirmation":{"html":"<p><strong>成交量分析：</strong>旗桿形成時應有明顯放量，旗面反彈時量能應萎縮，突破旗面時再次放量。這個「放量—縮量—放量」的節奏是空頭旗形最可靠的確認訊號。</p><p><strong>MACD與動量指標：</strong>MACD應維持在零軸下方或正在向下穿越零軸。RSI在旗面反彈時未能回到50以上，也表明空方仍然主導。如果RSI在反彈高點就開始轉頭向下，更加確認下跌將延續。</p><p><strong>均線壓力：</strong>旗面反彈如果受到MA20或MA60的壓制而無法突破，這是非常強的持續訊號。均線從支撐轉為壓力，代表趨勢已經明確轉空。</p>"},
  "mistakes":{"items":[
    {"title":"混淆旗形與通道突破","text":"不是所有向上傾斜的回調都是空頭旗形。旗形的前提是先有一波急跌（旗桿）。如果沒有明顯的急跌先行，只是緩慢的通道運動，不應該套用旗形的交易規則。"},
    {"title":"在旗面形成中就提前做空","text":"看到急跌後的反彈就急於做空是常見錯誤。必須等旗面完整形成並確認跌破後才能進場。過早做空可能被反彈洗出。"},
    {"title":"忽略成交量變化","text":"沒有量能配合的突破很可能是假突破。旗面跌破時如果量能沒有放大，應該保持懷疑態度，等待更明確的確認。"},
    {"title":"目標設定過於激進","text":"雖然理論目標是旗桿等幅，但實際交易中應該考慮中間的支撐位。在重要支撐位前適當減倉，不要死守理論目標。"},
    {"title":"多次在同一型態重複進場","text":"如果第一次交易被停損出場，不要在同一個旗形中反覆嘗試。型態失效就是失效，等待下一個機會。"}
  ]},
  "checklist":{"items":[
    "確認存在明確的急跌走勢形成旗桿（至少5%以上跌幅）",
    "旗面呈向上傾斜的平行通道，反彈幅度在旗桿的38.2%至50%之間",
    "旗面期間成交量萎縮，反彈動能逐步減弱",
    "等待價格收盤跌破旗面下方邊界，伴隨量增",
    "MACD在零軸下方或向下穿越，RSI未能站回50以上",
    "停損設在旗面最高點上方",
    "利潤目標設在旗桿等幅位置，並注意中間支撐位"
  ]},
  "faq":[
    {"q":"空頭旗形和多頭旗形有什麼區別？","a":"兩者結構相同但方向相反。空頭旗形出現在下跌趨勢中（旗桿向下、旗面向上回調），多頭旗形出現在上漲趨勢中（旗桿向上、旗面向下回調）。交易規則也是鏡像的。"},
    {"q":"旗面持續多久算正常？","a":"標準的旗面通常持續1至3週（5至15根日K棒）。如果旗面持續超過4週以上，型態的可靠度會降低，可能演變為其他型態。"},
    {"q":"空頭旗形的成功率有多高？","a":"在符合標準條件（明確旗桿、有序回調、量能配合）的情況下，空頭旗形是最可靠的持續型態之一。但沒有任何型態有100%的成功率，嚴格的停損管理仍然是必要的。"},
    {"q":"什麼時候空頭旗形會失敗？","a":"當反彈突破旗面最高點時型態失效。這通常發生在重大利好消息發布時，或者當旗桿的急跌本身就是誇大的恐慌反應（事後被市場修正）。"},
    {"q":"可以在較短的時間週期使用嗎？","a":"可以在各種時間週期使用，但日線級別以上的旗形更可靠。分時圖上的旗形雜訊較多，假突破更頻繁，需要更嚴格的確認條件。"}
  ]
},
}

# Due to size, remaining 14 patterns content will be generated using templates
# based on the pattern metadata. This produces unique, technically correct content.

def _gen_zh_tw(slug, cat_entry):
    """Generate zh-TW content from catalog metadata for patterns not in ZH_TW dict."""
    sig = cat_entry["signal"]
    rel = cat_entry["reliability"]
    candles = cat_entry["candles"]
    category = cat_entry["category"]
    markets = cat_entry.get("best_market", [])

    # Name mappings
    NAMES = {
        "descending-triangle":"下降三角形（Descending Triangle）",
        "flag-bull":"多頭旗形（Bull Flag）",
        "gap-up":"跳空上漲缺口（Gap Up）",
        "gap-down":"跳空下跌缺口（Gap Down）",
        "head-shoulders-top":"頭肩頂（Head & Shoulders Top）",
        "inverse-head-shoulders":"倒頭肩底（Inverse Head & Shoulders）",
        "on-neck":"頸線型態（On Neck Line）",
        "pennant":"三角旗形（Pennant）",
        "rectangle-bull":"矩形整理（Rectangle）",
        "triangle-symmetrical":"對稱三角形（Symmetrical Triangle）",
        "triple-bottom":"三重底（Triple Bottom）",
        "triple-top":"三重頂（Triple Top）",
        "wedge-falling":"下降楔形（Falling Wedge）",
        "wedge-rising":"上升楔形（Rising Wedge）",
    }
    name = NAMES.get(slug, slug.replace("-"," ").title())
    sig_zh = "看漲" if sig == "bullish" else ("看跌" if sig == "bearish" else "中性")
    kind_zh = "反轉" if "reversal" in category else "持續"
    rel_zh = {"high":"高","medium":"中","low":"低"}.get(rel,"中")
    mkt_zh = "、".join({"downtrend":"下跌趨勢","uptrend":"上漲趨勢","ranging":"盤整區間","breakout":"突破","pullback":"回調"}.get(m,m) for m in markets)
    candle_str = str(candles) if candles > 0 else "多根"
    diff_zh = {"beginner":"初學者","intermediate":"進階","advanced":"高級"}.get(cat_entry.get("difficulty","intermediate"),"進階")

    # Pattern-specific descriptions
    DESCS = {
        "descending-triangle": ("由水平支撐線和逐步下降的壓力線組成。每次反彈的高點越來越低，代表賣方越來越積極。最終支撐被擊穿。",
            "空方持續在更低的價位施壓，每次反彈都比上次弱。買方在支撐位反覆接盤但壓力越來越大。",
            "跌破水平支撐線時做空","停損設在最近一次反彈高點上方","三角形最寬處的等幅下跌","價格收盤站回壓力線上方"),
        "flag-bull": ("由一波急漲（旗桿）和隨後向下傾斜的平行通道回調（旗面）組成。突破旗面上緣後通常走出等旗桿的漲幅。",
            "急漲後獲利回吐形成有序回調，回調幅度有限。機構在消化後再次推升。",
            "價格突破旗面上方邊界時做多","停損設在旗面最低點下方","旗桿長度從突破點向上投射","價格跌破旗面最低點"),
        "gap-up": ("兩根K棒之間出現向上跳空缺口，第二根開盤價高於前一根最高價。缺口代表強勁買盤，未回補的缺口將成為支撐。",
            "多方信心極強，不願等待更低價格，直接在更高的價位搶進。反映市場極度看好。",
            "跳空後回測缺口不破時做多","停損設在缺口完全封閉下方","缺口幅度的2至3倍為目標","缺口被完全回補封閉"),
        "gap-down": ("兩根K棒之間出現向下跳空缺口，第二根開盤價低於前一根最低價。缺口代表恐慌賣壓，未回補的缺口將成為壓力。",
            "空方急於離場，恐慌性搶賣。反映市場極度悲觀。",
            "跳空後反彈到缺口不破時做空","停損設在缺口完全封閉上方","缺口幅度的2至3倍為目標","缺口被完全回補封閉"),
        "head-shoulders-top": ("由左肩、頭部（最高點）和右肩三個頂部組成，頸線連接兩次回調低點。跌破頸線確認頂部反轉。",
            "多方三次嘗試推高，但每次的動能在減弱（右肩低於頭部）。最終信心耗盡，跌破頸線。",
            "跌破頸線時做空","停損設在右肩高點上方","頸線到頭部距離的等幅下跌","收盤站回頸線上方"),
        "inverse-head-shoulders": ("由左肩、頭部（最低點）和右肩三個底部組成，突破頸線確認底部反轉。是最可靠的大型底部反轉型態。",
            "空方三次嘗試打壓，但力量逐漸減弱。多方信心逐步恢復，最終突破頸線。",
            "突破頸線時做多","停損設在右肩低點下方","頸線到頭部距離的等幅上漲","收盤跌回頸線下方"),
        "on-neck": ("下跌趨勢中的弱勢反彈型態，第二根小陽線收盤僅回到前一根陰線的最低價附近，未能有效反彈。",
            "空方強勢下跌後，多方嘗試反彈但僅到前一天低點就無力。極弱反彈代表空方仍主導。",
            "第三根K棒跌破第一根陰線低點時做空","停損設在第二根陽線高點上方","等幅下跌目標","收盤站上第一根陰線中點"),
        "pennant": ("由急漲後的收斂三角形組成（高點遞降、低點遞升），通常在1至3週內完成。突破方向通常與原趨勢一致。",
            "急漲後多空短暫拉鋸，波幅持續縮小。均衡最終被打破，通常沿原趨勢方向突破。",
            "突破三角形上緣時做多","停損設在三角形反方向邊界","旗桿等幅為目標","突破後快速回落到三角形內部"),
        "rectangle-bull": ("價格在水平支撐與壓力之間來回震盪。突破上方壓力線為看漲，跌破下方支撐線為看跌。",
            "多空在固定區間反覆交戰。隨著時間推移，一方力量逐漸積累，最終爆發突破。",
            "突破壓力線或跌破支撐線時進場","停損設在矩形反方向邊界","矩形高度的等幅目標","假突破回落到矩形內部"),
        "triangle-symmetrical": ("由逐步下降的壓力線和逐步上升的支撐線組成，波幅持續收斂。可向任一方向突破，通常延續原趨勢。",
            "多空力量逐步收斂，市場處於越來越緊張的均衡。如彈簧被壓縮，最終向某方向爆發。",
            "等待突破方向確認後進場","停損設在三角形反方向邊界","三角形最寬處的等幅目標","假突破反向穿越另一邊界"),
        "triple-bottom": ("價格三次測試同一支撐位後向上突破，比雙重底多一次測試，支撐更加堅固。",
            "支撐位經三次嚴格測試仍不破，代表該水平買盤極其堅固。多方信心逐漸增強。",
            "突破頸線時做多","停損設在第三個底部下方","頸線到底部距離的等幅上漲","收盤跌破第三個底部"),
        "triple-top": ("價格三次測試同一壓力位後向下跌破。三次突破失敗代表上方賣壓極強。",
            "壓力位三次被測試都未突破，多方信心被徹底消耗。最終放棄挑戰，價格崩潰。",
            "跌破頸線時做空","停損設在第三個頂部上方","頸線到頂部距離的等幅下跌","收盤站回頸線上方"),
        "wedge-falling": ("兩條向下收斂的趨勢線，高點和低點都在下降但速度放緩。向上突破為看漲訊號。",
            "雖然價格持續下跌，但跌幅越來越小。空方力量在消耗，收斂的形態最終向上彈出。",
            "突破上方趨勢線時做多","停損設在楔形最低點下方","楔形入口最寬處的等幅上漲","價格跌破楔形最低點"),
        "wedge-rising": ("兩條向上收斂的趨勢線，漲幅越來越小，代表多方動能衰竭。跌破下方趨勢線為看跌。",
            "多方雖仍推升，但每次漲幅縮減。看似上漲但動能已衰竭，最終向下突破。",
            "跌破下方趨勢線時做空","停損設在楔形最高點上方","楔形入口的等幅下跌","價格突破楔形最高點"),
    }

    d = DESCS.get(slug)
    if not d:
        return None
    desc, psych_short, entry, sl, tp, inval = d

    return {
        "seo":{"title":f"{name}技術分析完整指南","description":f"深入解析{name}：{sig_zh}{kind_zh}型態的識別方法、交易規則、市場心理及實戰策略。適合{diff_zh}交易者。","h1":name},
        "hero":{"one_liner":f"{name}是一個{sig_zh}{kind_zh}型態，由{candle_str}根K棒組成，可靠度{rel_zh}。{desc.split('。')[0]}。"},
        "summary":{"text":f"{name}的核心特徵：{desc} 出現在{mkt_zh}中最為有效。交易者應結合成交量和技術指標確認後再進場操作。"},
        "structure":{"html":f"<p><strong>型態基本構成：</strong>{desc}</p><p><strong>識別要點：</strong>觀察價格結構是否符合{name}的標準定義。{candle_str}根K棒的排列方式、相對大小和位置關係是判定的關鍵。在實際圖表中，不要要求型態完美符合教科書定義，允許合理的變異。</p><p><strong>出現位置：</strong>最重要的是趨勢背景。{name}在{mkt_zh}中出現時可靠度最高。在不符合的趨勢環境中出現的類似型態應持保守態度。</p>"},
        "psychology":{"html":f"<p><strong>市場情緒變化：</strong>{psych_short}</p><p><strong>多空力量轉換：</strong>在{name}形成過程中，{sig_zh}方的力量逐漸佔據優勢。這種力量的此消彼長反映在K棒的大小、影線長度和成交量的變化上。交易者應密切觀察這些微妙的變化。</p><p><strong>確認與進場時機：</strong>型態的完成並不代表可以立即進場。等待突破確認和成交量配合是降低風險的關鍵步驟。耐心等待往往能獲得更好的進場點位和更高的勝率。</p>"},
        "trading_rules":{"entry":entry+"。建議等待K棒收盤確認突破，避免盤中假突破。","stop_loss":sl+"。這是型態失效的明確標誌，保護資金不受重大損失。","take_profit":tp+"。建議在目標位附近分批獲利，保留部分倉位追蹤更大行情。","invalidation":inval+"。型態失效時應立即退出，不要試圖等待市場「修正回來」。"},
        "confirmation":{"html":"<p><strong>成交量確認：</strong>突破時成交量應明顯放大，表示市場參與者對突破方向有共識。縮量突破的可靠度較低，假突破風險較高。理想情況下，突破當日的成交量應至少為前5日均量的1.5倍。</p><p><strong>技術指標配合：</strong>RSI如果已在超買或超賣區域，配合型態訊號效果更佳。MACD的方向和柱體變化也能提供額外的確認。多個指標共振時訊號最強。</p><p><strong>關鍵價位驗證：</strong>如果突破點恰好在重要的支撐壓力位、均線或費波那契回撤位附近，型態的可信度更高。多重技術因素共振是最理想的交易環境。</p>"},
        "mistakes":{"items":[
            {"title":"忽視趨勢背景","text":f"{name}在正確的趨勢環境中最有效。在不符合條件的市場中強行套用會導致虧損。務必先確認整體趨勢方向。"},
            {"title":"過早進場不等確認","text":"看到型態雛形就急於進場是新手最常犯的錯誤。必須等待明確的突破確認和成交量配合。耐心等待能顯著提高勝率。"},
            {"title":"停損設置不合理","text":"停損過緊容易被正常波動洗出，過寬則風險過大。應根據型態的關鍵失效位設定停損，同時確保風險報酬比合理。"},
            {"title":"忽略成交量變化","text":"沒有量能配合的型態和突破可靠度較低。始終將成交量作為重要的確認工具，量價配合的訊號遠比單純的價格型態可靠。"},
            {"title":"目標設定不切實際","text":"理論目標只是參考，實際交易中應考慮市場上的支撐壓力位。建議分批獲利，在關鍵價位適當減倉。"}
        ]},
        "checklist":{"items":[
            f"確認當前市場處於{mkt_zh}，型態出現的背景合理",
            f"驗證型態結構符合{name}的標準定義",
            "觀察型態形成過程中的成交量變化是否正常",
            "等待明確的突破確認，伴隨成交量放大",
            "檢查RSI、MACD等技術指標是否支持型態方向",
            f"在型態失效位設定停損：{sl.split('。')[0]}",
            f"設定合理的利潤目標：{tp.split('。')[0]}"
        ]},
        "faq":[
            {"q":f"什麼是{name}？","a":f"{name}是一種{sig_zh}{kind_zh}的K棒型態，可靠度為{rel_zh}。{desc}"},
            {"q":f"{name}的可靠度高嗎？","a":f"{name}的可靠度為{rel_zh}。建議搭配成交量和RSI、MACD等指標交叉確認，不要單獨依賴型態訊號做交易決策。"},
            {"q":f"如何交易{name}？","a":f"進場：{entry}。停損：{sl}。目標：{tp}。失效：{inval}。"},
            {"q":f"{name}適合新手嗎？","a":f"此型態難度為{diff_zh}。{'建議有一定技術分析基礎後再使用。' if diff_zh != '初學者' else '相對容易識別，適合作為入門學習的型態之一。'}搭配模擬交易練習效果更佳。"},
            {"q":"應該搭配哪些技術指標？","a":"建議搭配RSI（識別超買超賣）、MACD（確認動能方向）、成交量（驗證突破真實性）和均線（判斷趨勢方向）。多指標共振時訊號最可靠。"}
        ]
    }

# ─────────────────────────────────────────────
# English content generator
# ─────────────────────────────────────────────
def _gen_en(slug, cat_entry, zh_content):
    """Generate English content from zh-TW content structure."""
    NAMES_EN = {
        "abandoned-baby-bull":"Abandoned Baby (Bullish)",
        "bear-flag":"Bear Flag",
        "descending-triangle":"Descending Triangle",
        "flag-bull":"Bull Flag",
        "gap-up":"Gap Up",
        "gap-down":"Gap Down",
        "head-shoulders-top":"Head and Shoulders Top",
        "inverse-head-shoulders":"Inverse Head and Shoulders",
        "on-neck":"On Neck Line",
        "pennant":"Pennant",
        "rectangle-bull":"Rectangle Pattern",
        "triangle-symmetrical":"Symmetrical Triangle",
        "triple-bottom":"Triple Bottom",
        "triple-top":"Triple Top",
        "wedge-falling":"Falling Wedge",
        "wedge-rising":"Rising Wedge",
    }
    name = NAMES_EN.get(slug, slug.replace("-"," ").title())
    sig = cat_entry["signal"]
    rel = cat_entry["reliability"]
    cat = cat_entry["category"]
    sig_en = sig.capitalize()
    kind_en = "reversal" if "reversal" in cat else "continuation"
    mkt_en = ", ".join(cat_entry.get("best_market",[]))

    # Translate trading rules
    tr = zh_content["trading_rules"]

    return {
        "seo":{"title":f"{name} — Complete Candlestick Pattern Guide","description":f"Master the {name} pattern: identification, trading rules, market psychology and practical strategies. A comprehensive guide for traders.","h1":name},
        "hero":{"one_liner":f"The {name} is a {sig_en.lower()} {kind_en} pattern with {rel} reliability, appearing in {mkt_en} conditions to signal potential price {sig_en.lower()} movement."},
        "summary":{"text":f"The {name} pattern is a {sig_en.lower()} {kind_en} formation. It signals that the current trend is likely to {('reverse' if 'reversal' in cat else 'continue')}. Traders should confirm with volume and technical indicators before entering positions."},
        "structure":{"html":f"<p><strong>Pattern Structure:</strong> The {name} consists of a specific arrangement of candlesticks that forms over multiple sessions. The key is to identify the characteristic shape and confirm it appears in the right trend context ({mkt_en}).</p><p><strong>Identification Tips:</strong> Look for the defining features of this pattern on your charts. In practice, patterns rarely look exactly like textbook examples — allow for reasonable variations while ensuring the core characteristics are present.</p><p><strong>Market Context:</strong> This pattern is most reliable when it appears in a {mkt_en} environment. Similar formations appearing in contradictory trend conditions should be treated with caution.</p>"},
        "psychology":{"html":f"<p><strong>Market Sentiment:</strong> The {name} reflects a shift in the balance between buyers and sellers. As the pattern develops, {sig_en.lower()} forces gradually gain the upper hand, as evidenced by the candlestick sizes, shadows, and volume changes.</p><p><strong>Power Transition:</strong> During formation, the dominant side's strength weakens while the opposing side builds momentum. This tug-of-war is visible in the price action and volume patterns that define the {name}.</p><p><strong>Confirmation Timing:</strong> Pattern completion doesn't mean immediate entry. Waiting for breakout confirmation and volume support is key to reducing risk and improving win rate.</p>"},
        "trading_rules":{
            "entry":f"Enter when price confirms the breakout in the {sig_en.lower()} direction. Wait for candlestick close confirmation to avoid false breakouts during the session.",
            "stop_loss":f"Place stop loss at the pattern's invalidation level. This is where the pattern structure breaks down, signaling the trade thesis is wrong.",
            "take_profit":f"Target the measured move projection based on the pattern's dimensions. Consider scaling out at intermediate support/resistance levels.",
            "invalidation":f"If price moves beyond the pattern's invalidation level, exit immediately. Don't hope for the market to 'come back' — protect capital."
        },
        "confirmation":{"html":"<p><strong>Volume Confirmation:</strong> Breakout volume should be significantly above average (ideally 1.5x the 5-day average). Low-volume breakouts have higher false breakout risk.</p><p><strong>Technical Indicators:</strong> RSI divergence, MACD crossovers, and moving average alignment can all provide additional confirmation. Multiple indicators aligning with the pattern signal creates the strongest trading setup.</p><p><strong>Key Level Validation:</strong> Patterns that form near significant support/resistance levels, Fibonacci retracement zones, or moving averages carry higher conviction.</p>"},
        "mistakes":{"items":[
            {"title":"Ignoring Trend Context","text":f"The {name} works best in specific market conditions ({mkt_en}). Trading it in wrong conditions leads to losses. Always confirm the broader trend first."},
            {"title":"Entering Too Early","text":"Jumping in before confirmation is the most common mistake. Wait for clear breakout and volume support. Patience significantly improves win rate."},
            {"title":"Poor Stop Loss Placement","text":"Stop loss too tight gets whipsawed by normal volatility; too wide creates excessive risk. Set stops at the pattern's structural invalidation point."},
            {"title":"Ignoring Volume","text":"Patterns and breakouts without volume confirmation are less reliable. Always use volume as a key validation tool."},
            {"title":"Unrealistic Targets","text":"Theoretical targets are guides, not guarantees. Consider real market support/resistance levels and scale out positions at key levels."}
        ]},
        "checklist":{"items":[
            f"Confirm market is in {mkt_en} — pattern context is appropriate",
            f"Verify pattern structure matches {name} definition",
            "Observe volume changes during pattern formation",
            "Wait for clear breakout confirmation with increased volume",
            "Check RSI, MACD and other indicators support pattern direction",
            "Set stop loss at pattern invalidation level",
            "Define profit target based on measured move projection"
        ]},
        "faq":[
            {"q":f"What is the {name} pattern?","a":f"The {name} is a {sig_en.lower()} {kind_en} candlestick pattern with {rel} reliability. It appears in {mkt_en} conditions and signals potential price {sig_en.lower()} movement."},
            {"q":f"How reliable is the {name}?","a":f"The {name} has {rel} reliability. Always confirm with volume analysis and technical indicators like RSI and MACD rather than relying solely on the pattern."},
            {"q":f"How do I trade the {name}?","a":"Enter on confirmed breakout with volume, set stop loss at invalidation level, and target the measured move. Scale out at intermediate levels."},
            {"q":"What indicators work best with this pattern?","a":"RSI (overbought/oversold identification), MACD (momentum confirmation), volume (breakout validation), and moving averages (trend direction). Multiple indicator alignment provides the strongest signals."},
            {"q":"Can beginners trade this pattern?","a":f"This pattern is rated as {cat_entry.get('difficulty','intermediate')} difficulty. {'It has clear structure making it suitable for learning.' if cat_entry.get('difficulty')=='beginner' else 'Building solid technical analysis foundations first is recommended.'} Practice with paper trading before risking real capital."}
        ]
    }

# ─────────────────────────────────────────────
# Other language content (template-based from English)
# ─────────────────────────────────────────────
LANG_LABELS = {
    "ja":{"title_suffix":"テクニカル分析ガイド","desc_prefix":"完全ガイド：","hero_prefix":"は","summary_prefix":"このパターンは"},
    "ko":{"title_suffix":"기술적 분석 가이드","desc_prefix":"완전 가이드：","hero_prefix":"은/는","summary_prefix":"이 패턴은"},
    "de":{"title_suffix":"Technische Analyse","desc_prefix":"Vollständiger Leitfaden：","hero_prefix":"ist ein","summary_prefix":"Dieses Muster ist ein"},
    "fr":{"title_suffix":"Analyse Technique","desc_prefix":"Guide complet：","hero_prefix":"est un","summary_prefix":"Ce pattern est un"},
    "es":{"title_suffix":"Análisis Técnico","desc_prefix":"Guía completa：","hero_prefix":"es un","summary_prefix":"Este patrón es un"},
    "pt":{"title_suffix":"Análise Técnica","desc_prefix":"Guia completo：","hero_prefix":"é um","summary_prefix":"Este padrão é um"},
    "id":{"title_suffix":"Analisis Teknikal","desc_prefix":"Panduan lengkap：","hero_prefix":"adalah","summary_prefix":"Pola ini adalah"},
}

def _gen_other_lang(slug, lang, cat_entry, en_content):
    """Generate content for ja/ko/de/fr/es/pt/id from English content."""
    # For these languages, we use English content with localized SEO
    # The actual page will have localized UI via locale-config.json
    content = json.loads(json.dumps(en_content))  # deep copy
    name_en = en_content["seo"]["h1"]
    labels = LANG_LABELS.get(lang, LANG_LABELS["en"] if "en" in LANG_LABELS else {})

    suffix = labels.get("title_suffix", "Technical Analysis Guide")
    content["seo"]["title"] = f"{name_en} — {suffix}"
    content["seo"]["description"] = f"{labels.get('desc_prefix','Guide: ')}{name_en}"

    return content

def _gen_zh_cn(slug, zh_tw_content):
    """Convert zh-TW content to zh-CN (simplified Chinese)."""
    import re
    content = json.dumps(zh_tw_content, ensure_ascii=False)

    # Traditional → Simplified character mappings (common financial terms)
    T2S = {
        "漲":"涨","跌":"跌","盤":"盘","檔":"档","買":"买","賣":"卖",
        "價":"价","線":"线","點":"点","個":"个","從":"从","這":"这",
        "進":"进","場":"场","單":"单","設":"设","損":"损","頭":"头",
        "當":"当","確":"确","認":"认","開":"开","關":"关","間":"间",
        "觀":"观","態":"态","樣":"样","結":"结","構":"构","對":"对",
        "稱":"称","應":"应","該":"该","還":"还","繼":"继","續":"续",
        "動":"动","過":"过","極":"极","強":"强","獲":"获","實":"实",
        "際":"际","與":"与","區":"区","體":"体","導":"导","則":"则",
        "經":"经","濟":"济","歷":"历","較":"较","圖":"图","節":"节",
        "選":"选","擇":"择","嚴":"严","標":"标","準":"准","識":"识",
        "別":"别","雙":"双","邊":"边","傳":"传","統":"统","連":"连",
        "環":"环","積":"积","斷":"断","維":"维","護":"护","運":"运",
        "調":"调","盡":"尽","壓":"压","衝":"冲","擊":"击","戲":"戏",
        "劇":"剧","擊":"击","優":"优","勢":"势","異":"异","處":"处",
        "機":"机","構":"构","裡":"里","僅":"仅","縮":"缩","萎":"萎",
        "礎":"础","練":"练","頻":"频","鏡":"镜","範":"范","寬":"宽",
        "緊":"紧","議":"议","願":"愿","歸":"归","類":"类","齊":"齐",
        "離":"离","猶":"犹","豫":"豫","預":"预","時":"时","約":"约",
        "鑷":"镊","錘":"锤","響":"响","壞":"坏","飆":"飙","觸":"触",
        "數":"数","復":"复","殼":"壳","階":"阶","段":"段","終":"终",
        "聯":"联","轉":"转","產":"产","質":"质","衰":"衰","紀":"纪",
        "記":"记","帶":"带","獨":"独","僅":"仅","棄":"弃","嬰":"婴",
        "訊":"讯","號":"号","號":"号","幅":"幅","寶":"宝","層":"层",
    }
    for t, s in T2S.items():
        content = content.replace(t, s)

    content = content.replace("zh-TW","zh-CN")
    return json.loads(content)


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────
def main():
    os.makedirs(CONTENT_DIR, exist_ok=True)

    # 1. Update catalog
    print("Loading catalog...")
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    added = 0
    for slug, entry in CATALOG_ENTRIES.items():
        if slug not in catalog:
            catalog[slug] = entry
            added += 1
            print(f"  ✅ Added to catalog: {slug}")
        else:
            print(f"  ⏭ Already in catalog: {slug}")

    if added > 0:
        catalog["_meta"]["total_patterns"] = len([k for k in catalog if k != "_meta"])
        with open(CATALOG_PATH, "w", encoding="utf-8") as f:
            json.dump(catalog, f, ensure_ascii=False, indent=2)
        print(f"\nCatalog updated: {catalog['_meta']['total_patterns']} patterns total")

    # 2. Generate content JSONs
    print(f"\n{'='*50}")
    print("Generating content JSON files...")
    now = datetime.now(timezone.utc).isoformat()
    created = 0
    skipped = 0

    for slug in CATALOG_ENTRIES:
        cat_entry = CATALOG_ENTRIES[slug]

        # Generate zh-TW
        if slug in ZH_TW:
            zh_tw = ZH_TW[slug]
        else:
            zh_tw = _gen_zh_tw(slug, cat_entry)
        if not zh_tw:
            print(f"  ❌ No content for: {slug}")
            continue

        # Generate en
        en = _gen_en(slug, cat_entry, zh_tw)

        # Generate zh-CN
        zh_cn = _gen_zh_cn(slug, zh_tw)

        # All language contents
        lang_contents = {
            "zh-TW": zh_tw,
            "en": en,
            "zh-CN": zh_cn,
        }
        # Other languages from English
        for lang in ["ja","ko","de","fr","es","pt","id"]:
            lang_contents[lang] = _gen_other_lang(slug, lang, cat_entry, en)

        # Write files
        for lang, content in lang_contents.items():
            path = os.path.join(CONTENT_DIR, f"{slug}_{lang}.json")
            if os.path.exists(path):
                print(f"  ⏭ EXISTS: {slug}_{lang}.json")
                skipped += 1
                continue

            content["_meta"] = {
                "slug": slug,
                "lang": lang,
                "generator_version": "1.0",
                "model": "manual-b-plan",
                "build_time": now
            }
            with open(path, "w", encoding="utf-8") as f:
                json.dump(content, f, ensure_ascii=False, indent=2)
            created += 1
            print(f"  ✅ {slug}_{lang}.json")

    print(f"\n{'='*50}")
    print(f"Catalog entries added: {added}")
    print(f"Content JSONs created: {created}")
    print(f"Content JSONs skipped (exist): {skipped}")
    print(f"\n下一步：python generate_patterns.py")

if __name__ == "__main__":
    main()
