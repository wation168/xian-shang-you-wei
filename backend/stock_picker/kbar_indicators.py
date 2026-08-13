# -*- coding: utf-8 -*-
"""
kbar_indicators.py — K棒型態偵測（2026/08/13新增，供深度選股使用）

背景：main.py 的個股解析（_do_analyze）已經有完整的K棒型態偵測（detect_kbar_pattern）
與突破/跌破訊號偵測（calc_breakout_signals），深度選股原本完全沒有這個維度，導致
「突破隔日拉回」這類敘事沒辦法做（那是靠K棒型態=孕線 + 前一天有沒有突破組出來的）。

這支檔案的兩個函式是「逐字從 main.py 複製過來」，不是重寫第二份邏輯：
  - detect_kbar_pattern() 複製自 main.py detect_kbar_pattern()（main.py內約5462行起）
  - calc_breakout_signals() 複製自 main.py calc_breakout_signals()（main.py內約2581行起）
兩者原本就是純函式（只吃K線陣列當參數，不依賴main.py的任何全域變數/DB/其他函式），
不能直接 import main.py 進 stock_picker（main.py 本身在啟動時會初始化DB/排程器等，
而且 main.py 已經反過來 import stock_picker 的模組，直接 import 回main.py會造成
循環引用），所以用「複製檔案」取代「import主程式」。

⚠️ 維護提醒：main.py 那兩個函式之後如果修改判斷邏輯（新增型態、調整門檻等），
這裡要記得同步更新，否則深度選股的K棒判斷會跟個股解析的判斷邏輯兜不起來，
又製造新的一致性問題。

用途：目前只用於深度選股的「白話結論」敘事文字（見 generator.py _deep_conclusion()），
刻意不接入 finmind_filter.py 的評分（_score）與風險分級（_risk_level），
所以這裡的K棒判斷只會讓深度選股的文字說明更豐富，不會改變任何一支股票入不入選、
落在低/中/高哪個風險等級——維持選股機制本身不變。
"""

import numpy as np


def detect_kbar_pattern(opens, highs, lows, closes, volumes=None):
    """
    辨識最近 K 棒型態（單根/兩根/三根），含量能確認
    回傳：
      kbar_pattern: str  已確認的型態名稱（空字串=無）
      kbar_warning: str  預警文字（明天若...將形成...）
    """
    n = len(closes)
    if n < 3:
        return "", "", "neutral", 0.50

    o1,h1,l1,c1 = opens[-1],highs[-1],lows[-1],closes[-1]  # 最新根
    o2,h2,l2,c2 = opens[-2],highs[-2],lows[-2],closes[-2]  # 前一根
    o3,h3,l3,c3 = opens[-3],highs[-3],lows[-3],closes[-3]  # 前兩根

    # 量能確認（今日量 vs 前一日量）
    _vol_up = False   # 今日量 > 昨日量
    _vol_down = False # 今日量 < 昨日量 * 0.7
    if volumes is not None and len(volumes) >= 2:
        v1, v2 = float(volumes[-1]), float(volumes[-2])
        if v2 > 0:
            _vol_up = v1 > v2 * 1.1     # 量增 10% 以上
            _vol_down = v1 < v2 * 0.7    # 量縮 30% 以上

    body1 = abs(c1 - o1)
    body2 = abs(c2 - o2)
    body3 = abs(c3 - o3)
    range1 = h1 - l1 or 0.001
    range2 = h2 - l2 or 0.001
    range3 = h3 - l3 or 0.001

    upper_shadow1 = h1 - max(o1, c1)
    lower_shadow1 = min(o1, c1) - l1
    upper_shadow2 = h2 - max(o2, c2)
    lower_shadow2 = min(o2, c2) - l2

    is_red1 = c1 > o1
    is_red2 = c2 > o2
    is_red3 = c3 > o3

    patterns = []
    warnings = []

    # ── 跳空判斷（今日K棒範圍與昨日完全不重疊）──
    # 2026/08/06 新增：原本完全沒有跳空偵測，缺這塊資訊
    _gap_up = l1 > h2
    _gap_down = h1 < l2
    _gap_tag = "跳空" if (_gap_up or _gap_down) else ""

    # ── 單根型態（最新K棒）──

    # 一字線（漲跌停鎖死：開=高=低=收，全日幾乎零波動）
    # 2026/08/06 新增：原本完全沒有這個型態，數值特徵(body/range<0.1)跟十字星重疊，
    # 一直被誤判成十字星——但一字線代表極端一致的單邊情緒（搶著買或搶著賣到鎖死），
    # 跟十字星代表的「方向不明、多空拉鋸」意義完全相反，混在一起會誤導使用者。
    # 用 range/price 是否極小（而非 body/range 比例）當判斷依據，才能跟十字星區分開。
    if range1 / (c1 or 1) < 0.002:
        if c1 > c2 * 1.001:
            patterns.append(f"{_gap_tag}一字線（漲停鎖死，強勢惜售）")
            warnings.append("今日一字鎖死漲停，若明天開盤不跳空回補，多方強勢未變")
        elif c1 < c2 * 0.999:
            patterns.append(f"{_gap_tag}一字線（跌停鎖死，恐慌出逃）")
            warnings.append("今日一字鎖死跌停，若明天無法收復，空方強勢未變")
        else:
            patterns.append(f"{_gap_tag}一字線（平盤鎖死，極端惜售惜買）")
            warnings.append("今日一字線但接近平盤，方向不明，觀察明天開盤方向")

    # 錘頭（底部，下引線長，出現在下跌後）
    elif (lower_shadow1 >= body1 * 2 and upper_shadow1 <= body1 * 0.3
            and body1 / range1 < 0.4):
        if not is_red1:
            patterns.append(f"{_gap_tag}錘頭線（底部反轉訊號）")
            warnings.append("出現錘頭線，若明天收紅確認，底部支撐訊號成立")
        else:
            patterns.append(f"{_gap_tag}錘頭線（底部反轉，紅K更佳）")
            warnings.append("出現紅K錘頭線，底部支撐訊號，明天若繼續收紅則確認")

    # 流星/射擊之星（頂部，上引線長）
    elif (upper_shadow1 >= body1 * 2 and lower_shadow1 <= body1 * 0.3
            and body1 / range1 < 0.4):
        patterns.append(f"{_gap_tag}射擊之星（頂部壓力訊號）")
        warnings.append("出現射擊之星，若明天收黑確認，注意頂部形成風險")

    # 十字星（開收盤接近，但範圍正常，非鎖死一字線）
    elif body1 / range1 < 0.1 and range1 > 0:
        if h1 > max(h2, h3):  # 高點在頂部
            patterns.append(f"{_gap_tag}十字星（高點出現，方向未定）")
            warnings.append("高點出現十字星，方向未明，明天若收黑須注意拉回")
        else:
            patterns.append(f"{_gap_tag}十字星（整理，等待方向）")
            warnings.append("出現十字星，整理中，等待明天方向確認")

    # 長上影黑K（假突破，高檔賣壓）／長下影紅K（假跌破，低檔承接）
    # 2026/08/07 新增：帥哥鴻用 3231 緯創 2026/08/05 實際K棒（開198／高202.5／低190／收193）
    # 發現的真實偵測漏洞——body1/range1=0.40，不夠格是大黑棒(>0.7)，上下影線比例也不到
    # 錘頭/射擊之星要求的2倍，導致這種「衝高被拉回、收黑、帶明顯上影線」的關鍵反轉訊號
    # 完全沒被任何型態捕捉到，kbar_pattern留空，連帶vp_exit_warn（爆量出場警訊）也不會觸發
    # （因為它是靠kbar_pattern字串比對關鍵字才會啟動）。
    # 這裡補上 body1/range1 在 0.1~0.7 之間、但帶有明顯單邊影線（≥range1*0.3）的情況：
    elif not is_red1 and body1 / range1 <= 0.7 and upper_shadow1 >= range1 * 0.3:
        patterns.append(f"{_gap_tag}長上影黑K（假突破，高檔賣壓）")
        warnings.append("今日收黑且帶明顯上影線，疑似衝高遭壓回，若明天無法收復今日高點一半，賣壓恐延續")

    elif is_red1 and body1 / range1 <= 0.7 and lower_shadow1 >= range1 * 0.3:
        patterns.append(f"{_gap_tag}長下影紅K（假跌破，低檔承接）")
        warnings.append("今日收紅且帶明顯下影線，疑似殺低後獲得承接，若明天延續收紅，止跌訊號增強")

    # 大紅棒（強攻）— 2026/08/06 拿掉「body1 > body2*1.5」這個門檻：
    # body1/range1>0.7 本身已經是「實體佔全天振幅七成以上」的絕對強度判斷，足以定義
    # 大紅棒，不需要再跟昨天比較。原本「比昨天大1.5倍」會導致連續強勢（例如連續兩天
    # 都是大紅棒）時，第二天因為沒有比第一天更大而被漏判成常態K線，是明確的邏輯錯誤。
    elif is_red1 and body1 / range1 > 0.7:
        patterns.append(f"{_gap_tag}大紅棒（強勢攻擊）")
        warnings.append("出現大紅棒，若明天不跌破今日一半，多頭強勢延續")

    # 大黑棒（強殺）— 同上，拿掉「比昨天大1.5倍」的門檻
    elif not is_red1 and body1 / range1 > 0.7:
        patterns.append(f"{_gap_tag}大黑棒（強勢賣壓）")
        warnings.append("出現大黑棒，若明天無法收復今日一半，空頭延續")

    # ── 兩根型態 ──

    # 多頭吞噬（紅吞黑）
    if (is_red1 and not is_red2
            and o1 <= c2 and c1 >= o2
            and body1 > body2):
        _vol_tag = "，量增確認" if _vol_up else ("，量未配合" if _vol_down else "")
        patterns.append(f"多頭吞噬（底部反轉{_vol_tag}）")
        warnings.append("出現多頭吞噬，明天若繼續收紅，底部反轉確認")

    # 空頭吞噬（黑吞紅）
    elif (not is_red1 and is_red2
            and o1 >= c2 and c1 <= o2
            and body1 > body2):
        _vol_tag = "，量增確認" if _vol_up else ""
        patterns.append(f"空頭吞噬（頂部反轉{_vol_tag}）")
        warnings.append("出現空頭吞噬，明天若繼續收黑，頂部反轉確認")

    # 孕線（母子）
    elif (body2 > body1 * 2
            and max(o1,c1) < max(o2,c2)
            and min(o1,c1) > min(o2,c2)):
        if is_red2:
            patterns.append("孕線（多頭孕線，整理後可能續漲）")
            warnings.append("出現多頭孕線，若明天收紅突破母線高點，多頭延續")
        else:
            patterns.append("孕線（空頭孕線，整理後可能續跌）")
            warnings.append("出現空頭孕線，若明天收黑跌破母線低點，空頭延續")

    # 穿刺線（黑後紅，收超過前根中段）
    elif (is_red1 and not is_red2
            and o1 < l2
            and c1 > (o2 + c2) / 2
            and c1 < o2):
        patterns.append("穿刺線（底部潛在反轉）")
        warnings.append("出現穿刺線，明天若繼續收紅，底部反轉訊號增強")

    # 烏雲蓋頂（紅後黑，收超過前根中段）
    elif (not is_red1 and is_red2
            and o1 > h2
            and c1 < (o2 + c2) / 2
            and c1 > o2):
        patterns.append("烏雲蓋頂（頂部潛在反轉）")
        warnings.append("出現烏雲蓋頂，明天若繼續收黑，頂部反轉訊號增強")

    # ── 三根型態 ──

    # 早晨之星（底部反轉：黑棒+小實體+紅棒）
    if (not is_red3 and body3 > range3 * 0.4
            and body2 < range2 * 0.3
            and is_red1 and c1 > (o3 + c3) / 2):
        patterns.append("早晨之星（底部強力反轉）")
        warnings.append("出現早晨之星，底部反轉訊號，明天若繼續收紅則強力確認")

    # 黃昏之星（頂部反轉：紅棒+小實體+黑棒）
    elif (is_red3 and body3 > range3 * 0.4
            and body2 < range2 * 0.3
            and not is_red1 and c1 < (o3 + c3) / 2):
        patterns.append("黃昏之星（頂部強力反轉）")
        warnings.append("出現黃昏之星，頂部反轉訊號，若明天繼續收黑須注意出場")

    # 三紅兵（強勢延續）
    elif (is_red1 and is_red2 and is_red3
            and c1 > c2 > c3
            and body1 > range1 * 0.5
            and body2 > range2 * 0.5
            and body3 > range3 * 0.5):
        patterns.append("三紅兵（強勢多頭延續）")
        warnings.append("出現三紅兵，多頭趨勢強，明天若再收紅趨勢持續，注意追高風險")

    # 三烏鴉（弱勢延續）
    elif (not is_red1 and not is_red2 and not is_red3
            and c1 < c2 < c3
            and body1 > range1 * 0.5
            and body2 > range2 * 0.5
            and body3 > range3 * 0.5):
        patterns.append("三烏鴉（強勢空頭延續）")
        warnings.append("出現三烏鴉，空頭趨勢強，明天若再收黑持續下跌壓力")

    # 預警：今天+明天可能形成的型態
    if not patterns:
        # 今天是大黑棒，若明天開高收在中段以上 → 穿刺線
        if not is_red1 and body1 / range1 > 0.6:
            warnings.append("今天出現大黑棒，若明天開低後拉回收超過今日一半，將形成穿刺線（底部反轉）")
        # 今天是大紅棒，若明天開高收黑超過中段 → 烏雲蓋頂
        elif is_red1 and body1 / range1 > 0.6:
            warnings.append("今天出現大紅棒，若明天開高後反轉收黑超過今日一半，將形成烏雲蓋頂（頂部反轉）")
        # 今天是小實體（前一根是大棒）
        elif body1 < range1 * 0.3 and body2 > range2 * 0.5:
            if is_red2:
                warnings.append("出現孕線雛形（前大紅棒+今小實體），若明天收紅突破今日高點，多頭延續")
            else:
                warnings.append("出現孕線雛形（前大黑棒+今小實體），若明天收黑跌破今日低點，空頭延續")

    pattern_str = "、".join(patterns) if patterns else ""
    warning_str = warnings[0] if warnings else ""

    # 方向標記（供前端配色用）
    bullish_keys = ["錘頭","多頭吞噬","早晨之星","三紅兵","穿刺線","大紅棒","頭肩底","W底","漲停","長下影紅K"]
    bearish_keys = ["射擊之星","空頭吞噬","黃昏之星","三烏鴉","烏雲蓋頂","大黑棒","頭肩頂","M頭","跌停","長上影黑K"]
    kbar_dir = "bullish" if any(k in pattern_str for k in bullish_keys) \
               else "bearish" if any(k in pattern_str for k in bearish_keys) \
               else "neutral"

    # B3: 統一勝率對照表（與原 detect_kline_patterns 一致，消除兩套判斷矛盾）
    _WIN_RATE_MAP = {
        "大紅棒": 0.62, "大黑棒": 0.62,
        "三紅兵": 0.60, "三烏鴉": 0.60,
        "早晨之星": 0.60, "黃昏之星": 0.60,
        "多頭吞噬": 0.58, "空頭吞噬": 0.58,
        "錘頭": 0.53, "射擊之星": 0.53,
        "穿刺線": 0.55, "烏雲蓋頂": 0.55,
        "十字星": 0.52, "孕線": 0.52,
        # 2026/08/07 新增：靜態預設值，屬保守估計（介於錘頭/射擊之星與穿刺線/烏雲蓋頂之間）；
        # 個股實際勝率仍以 _kbar_backtest（同股票歷史同型態統計）動態算出的結果為準，
        # 這裡只是資料不足時的靜態備援
        "長上影黑K": 0.54, "長下影紅K": 0.54,
    }
    win_rate = 0.50
    for key, rate in _WIN_RATE_MAP.items():
        if key in pattern_str:
            win_rate = rate
            break

    return pattern_str, warning_str, kbar_dir, win_rate


# ══════════════════════════════════════════════════════════
# 籌碼面 API
# ══════════════════════════════════════════════════════════



def calc_breakout_signals(closes, highs, lows, volumes, support, resistance):
    """
    突破壓力 / 跌破支撐訊號
    量能條件：爆量（>均量1.5倍）或凹洞量（<均量0.5倍，健康型突破）

    ⚠️ Bug fix：改用「滾動局部高低點」作為每根K棒當時的壓力/支撐參考，
       而非用分析當下的 support/resistance 去掃整段歷史（那樣會造成語義偏移）。
    策略：
      - 只在最近 LOOKBACK 根內尋找訊號，避免顯示太舊的標記
      - 每根K棒的「當時壓力」= 前 40 根的局部最高收盤；「當時支撐」= 前 40 根局部最低收盤
      - 最後一次訊號若距今 > 30 根，標記 stale=True，前端可選擇淡化或不顯示
    回傳：
      breakout_idx:  最近一次突破索引（全域），None = 無
      breakdown_idx: 最近一次跌破索引（全域），None = 無
      breakout_stale:  bool，訊號是否過舊
      breakdown_stale: bool，訊號是否過舊
    """
    n = len(closes)
    LOOKBACK = min(n, 120)   # 只掃最近 120 根
    WINDOW   = 40            # 每根K棒「往前看」幾根來決定當時的局部支撐/壓力
    STALE    = 30            # 超過幾根視為過舊

    vol_ma = np.full(n, np.nan)
    for i in range(19, n):
        vol_ma[i] = volumes[i - 19: i + 1].mean()

    breakout_idx  = None
    breakdown_idx = None

    scan_start = max(WINDOW + 1, n - LOOKBACK)

    for i in range(scan_start, n):
        if np.isnan(vol_ma[i]):
            continue
        vol_ok = (volumes[i] > vol_ma[i] * 1.5) or (volumes[i] < vol_ma[i] * 0.5)
        if not vol_ok:
            continue

        # 當時的局部壓力/支撐：往前 WINDOW 根的收盤高/低（不含當根）
        local_resist = closes[i - WINDOW: i].max()
        local_support = closes[i - WINDOW: i].min()

        # 突破：前一根收在局部壓力以下，這一根放量站上局部壓力 × 1.005
        if (closes[i - 1] < local_resist * 1.005
                and closes[i] >= local_resist * 1.005):
            breakout_idx = i

        # 跌破：前一根收在局部支撐以上，這一根放量跌破局部支撐 × 0.995
        if (closes[i - 1] > local_support * 0.995
                and closes[i] <= local_support * 0.995):
            breakdown_idx = i

    # 若訊號距今超過 STALE 根，標記為過舊
    breakout_stale  = (breakout_idx  is not None and (n - 1 - breakout_idx)  > STALE)
    breakdown_stale = (breakdown_idx is not None and (n - 1 - breakdown_idx) > STALE)

    return breakout_idx, breakdown_idx, breakout_stale, breakdown_stale

