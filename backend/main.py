"""
線上有位 — 台股技術分析 API v2.0
啟動（本機）：uvicorn main:app --reload --port 8000
啟動（上線）：uvicorn main:app --host 0.0.0.0 --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import yfinance as yf
import pandas as pd
import numpy as np
from scipy.signal import argrelextrema
import os

# ══════════════════════════════════════════════════════════
# 環境設定（上線用環境變數，本機用 fallback）
# ══════════════════════════════════════════════════════════
FINMIND_TOKEN = os.environ.get("FINMIND_TOKEN", "")
if not FINMIND_TOKEN:
    raise RuntimeError("❌ 請設定環境變數 FINMIND_TOKEN")

# CORS：允許的前端來源
# 本機開發時設 ALLOWED_ORIGINS=* 或留空
# 上線後設為實際前端網址，例如 https://xian-shang-you-wei.zeabur.app
_origins_env = os.environ.get("ALLOWED_ORIGINS", "")
if _origins_env and _origins_env != "*":
    ALLOWED_ORIGINS = [o.strip() for o in _origins_env.split(",") if o.strip()]
else:
    # 開發環境：允許 localhost 各 port
    ALLOWED_ORIGINS = [
        "http://localhost:8080",
        "http://localhost:3000",
        "http://127.0.0.1:8080",
        "http://192.168.2.107:8080",
    ]

IS_PROD = os.environ.get("ZEABUR_SERVICE_ID") is not None  # Zeabur 會自動注入此變數


@asynccontextmanager
async def lifespan(app: FastAPI):
    env = "生產環境 🚀" if IS_PROD else "開發環境 💻"
    print(f"✅ 線上有位 API 啟動中（{env}）")
    print(f"   CORS 允許來源：{ALLOWED_ORIGINS}")
    yield
    print("🛑 線上有位 API 關閉")

# 上線時關閉 /docs 和 /redoc，避免 API 被掃描濫用
app = FastAPI(
    title="線上有位 API",
    version="2.0.0",
    lifespan=lifespan,
    docs_url=None if IS_PROD else "/docs",
    redoc_url=None if IS_PROD else "/redoc",
    openapi_url=None if IS_PROD else "/openapi.json",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET"],       # 只需要 GET
    allow_headers=["*"],
    allow_credentials=False,
)


# ══════════════════════════════════════════════════════════
# 工具函式
# ══════════════════════════════════════════════════════════
def resolve_symbol(stock_id: str) -> str:
    stock_id = stock_id.strip().upper()
    if stock_id.endswith((".TW", ".TWO")):
        return stock_id
    return stock_id + ".TW"


def safe_float(v):
    if v is None:
        return None
    try:
        f = float(v)
        return None if (np.isnan(f) or np.isinf(f)) else round(f, 2)
    except Exception:
        return None


def calc_ma(closes: np.ndarray, period: int) -> np.ndarray:
    ma = np.full(len(closes), np.nan)
    for i in range(period - 1, len(closes)):
        ma[i] = closes[i - period + 1: i + 1].mean()
    return ma


def fetch_df(symbol, period, interval):
    df = yf.download(symbol, period=period, interval=interval,
                     auto_adjust=True, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df


def try_fetch(stock_id, period, interval):
    symbol = resolve_symbol(stock_id)
    df = fetch_df(symbol, period, interval)
    if df.empty and not stock_id.upper().endswith((".TW", ".TWO")):
        symbol = stock_id.strip().upper() + ".TWO"
        df = fetch_df(symbol, period, interval)
    return symbol, df


# 股名快取（避免重複查詢）
_name_cache: dict[str, str] = {}

# 台股中文名稱對照表（常用股票，優先查表）
STOCK_NAMES = {
    "2330": "台積電", "2317": "鴻海", "2454": "聯發科", "2308": "台達電",
    "2412": "中華電", "6505": "台塑化", "2882": "國泰金", "2881": "富邦金",
    "2886": "兆豐金", "2891": "中信金", "2884": "玉山金", "2892": "第一金",
    "2883": "開發金", "2885": "元大金", "2887": "台新金", "2888": "新光金",
    "2890": "永豐金", "5880": "合庫金", "2801": "彰銀",
    "2002": "中鋼", "1301": "台塑", "1303": "南亞", "1326": "台化",
    "2303": "聯電", "2357": "華碩", "2382": "廣達", "2395": "研華",
    "2408": "南亞科", "2409": "友達", "2449": "京元電子", "2474": "可成",
    "2376": "技嘉", "2379": "瑞昱", "2385": "群光", "2392": "正崴",
    "3711": "日月光投控", "2301": "光寶科", "2325": "矽品",
    "3034": "聯詠", "3037": "欣興", "3045": "台灣大", "3702": "大聯大",
    "4904": "遠傳", "4938": "和碩", "5871": "中租KY", "6415": "矽力KY",
    "6669": "緯穎", "2610": "華航", "2618": "長榮航", "2615": "萬海",
    "2603": "長榮", "2609": "陽明", "2607": "榮運",
    "1216": "統一", "2912": "統一超", "2207": "和泰車", "2105": "正新",
    "1402": "遠東新", "1101": "台泥", "1102": "亞泥",
    "2823": "中壽", "2壽": "南山人壽",
    "3008": "大立光", "2352": "佳世達", "2344": "華邦電",
    "2337": "旺宏", "2360": "致茂", "2376": "技嘉",
}

def get_stock_name(symbol: str) -> str:
    """取得台股中文名稱：對照表 → FinMind → yfinance"""
    code = symbol.replace(".TWO", "").replace(".TW", "").strip()

    # 1. 先查對照表
    if code in STOCK_NAMES:
        return STOCK_NAMES[code]

    # 2. 查快取
    if code in _name_cache:
        return _name_cache[code]

    # 3. 查 FinMind（一次抓全部台股名稱存入快取）
    try:
        import urllib.request, json as _json
        url = (f"https://api.finmindtrade.com/api/v4/data"
               f"?dataset=TaiwanStockInfo&token={FINMIND_TOKEN}")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = _json.loads(resp.read())
        if data.get("status") == 200:
            for item in data.get("data", []):
                sid = str(item.get("stock_id", ""))
                sname = str(item.get("stock_name", ""))
                if sid and sname:
                    _name_cache[sid] = sname
        if code in _name_cache:
            return _name_cache[code]
    except Exception:
        pass

    # 4. 備援：yfinance
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        name = info.get("longName") or info.get("shortName") or ""
        for suffix in [" Co., Ltd.", " Co.,Ltd.", " Corporation", " Corp.",
                       " Ltd.", " Inc.", " Co.", "股份有限公司",
                       "Taiwan Semiconductor Manufacturing Company"]:
            name = name.replace(suffix, "")
        name = name.strip()[:20]
        if name:
            _name_cache[code] = name
        return name
    except Exception:
        return ""


def calc_rsi(closes: np.ndarray, period: int = 14) -> np.ndarray:
    n = len(closes)
    rsi = np.full(n, np.nan)
    if n < period + 1: return rsi
    deltas = np.diff(closes)
    gains = np.where(deltas > 0, deltas, 0.0)
    losses = np.where(deltas < 0, -deltas, 0.0)
    avg_gain = np.mean(gains[:period])
    avg_loss = np.mean(losses[:period])
    for i in range(period, n - 1):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        rs = avg_gain / avg_loss if avg_loss > 0 else 100
        rsi[i + 1] = 100 - 100 / (1 + rs)
    return rsi


def calc_macd(closes: np.ndarray, fast=12, slow=26, signal=9):
    n = len(closes)
    ema_fast = np.full(n, np.nan)
    ema_slow = np.full(n, np.nan)
    # EMA
    for arr, p in [(ema_fast, fast), (ema_slow, slow)]:
        k = 2 / (p + 1)
        start = p - 1
        if start >= n: continue
        arr[start] = np.mean(closes[:p])
        for i in range(start + 1, n):
            arr[i] = closes[i] * k + arr[i-1] * (1 - k)
    macd_line = ema_fast - ema_slow
    # Signal line (EMA of MACD)
    sig = np.full(n, np.nan)
    valid = np.where(~np.isnan(macd_line))[0]
    if len(valid) >= signal:
        s0 = valid[signal - 1]
        sig[s0] = np.mean(macd_line[valid[:signal]])
        k = 2 / (signal + 1)
        for i in range(s0 + 1, n):
            if not np.isnan(macd_line[i]):
                sig[i] = macd_line[i] * k + sig[i-1] * (1 - k)
    hist = macd_line - sig
    return macd_line, sig, hist


def calc_kd(highs: np.ndarray, lows: np.ndarray, closes: np.ndarray, period=9, smooth=3):
    n = len(closes)
    k_arr = np.full(n, np.nan)
    d_arr = np.full(n, np.nan)
    rsv   = np.full(n, np.nan)
    for i in range(period - 1, n):
        lo = lows[i-period+1:i+1].min()
        hi = highs[i-period+1:i+1].max()
        rsv[i] = (closes[i] - lo) / (hi - lo) * 100 if hi > lo else 50
    # Smooth K and D
    k_arr[period-1] = 50
    d_arr[period-1] = 50
    w = 1 / smooth
    for i in range(period, n):
        if np.isnan(rsv[i]): continue
        k_arr[i] = rsv[i] * w + k_arr[i-1] * (1 - w)
        d_arr[i] = k_arr[i] * w + d_arr[i-1] * (1 - w)
    return k_arr, d_arr


def calc_bollinger(closes: np.ndarray, period=20, std_dev=2):
    n = len(closes)
    mid = np.full(n, np.nan)
    upper = np.full(n, np.nan)
    lower = np.full(n, np.nan)
    for i in range(period - 1, n):
        seg = closes[i-period+1:i+1]
        m = seg.mean()
        s = seg.std(ddof=1)
        mid[i]   = round(float(m), 2)
        upper[i] = round(float(m + std_dev * s), 2)
        lower[i] = round(float(m - std_dev * s), 2)
    return mid, upper, lower


def calc_obv(closes: np.ndarray, volumes: np.ndarray):
    n = len(closes)
    obv = np.zeros(n)
    for i in range(1, n):
        if closes[i] > closes[i-1]:
            obv[i] = obv[i-1] + volumes[i]
        elif closes[i] < closes[i-1]:
            obv[i] = obv[i-1] - volumes[i]
        else:
            obv[i] = obv[i-1]
    return obv


def serialize_indicator(arr: np.ndarray, decimals=2) -> list:
    """Convert numpy array to JSON-serializable list, NaN → None"""
    return [None if np.isnan(v) else round(float(v), decimals) for v in arr]


def find_support_resistance(highs, lows, closes, volumes, price):
    n = len(closes)
    candidates = []

    order = max(3, min(10, n // 40))
    lo_idx = argrelextrema(lows, np.less_equal, order=order)[0]
    hi_idx = argrelextrema(highs, np.greater_equal, order=order)[0]

    # 均量（20日）
    vol_ma20 = np.full(n, np.nan)
    for i in range(19, n):
        vol_ma20[i] = volumes[i - 19: i + 1].mean()

    # ── 1. 回測後低點（突破壓力後拉回不破的低點，最具支撐意義）──
    # 邏輯：找轉折高點（舊壓力），突破後的第一個轉折低點就是回測低點
    for hi in reversed(hi_idx):
        resist_price = highs[hi]
        if resist_price >= price * 1.001:
            continue  # 此高點仍在現價上方，不是已突破的壓力
        # 找突破後（hi之後）有沒有收盤價站上此壓力
        breakout_i = None
        for i in range(hi + 1, n):
            if closes[i] > resist_price * 1.005:
                breakout_i = i
                break
        if breakout_i is None:
            continue
        # 找突破後的轉折低點（回測低點），且低點要在舊壓力附近（±5%）
        pullback_lows = [i for i in lo_idx
                         if i > breakout_i
                         and lows[i] >= resist_price * 0.95
                         and lows[i] < price * 0.999]
        if pullback_lows:
            best_pb = max(pullback_lows)  # 最近的回測低點
            ago = n - best_pb
            candidates.append((round(float(lows[best_pb]), 2), "pullback_low",
                                f"回測後低點（{ago}根前，突破{resist_price:.0f}後撐住）"))
            break  # 找到最近一次有效回測就夠了

    # ── 2. 低點密集區（多個轉折低點聚集在同一價位帶）──
    valid_lo = [i for i in lo_idx if lows[i] < price * 0.999]
    if len(valid_lo) >= 2:
        # 以每個轉折低點為中心，找 ±1.5% 內有幾個低點
        best_cluster_price = None
        best_cluster_count = 0
        best_cluster_recent = -1
        for anchor in valid_lo:
            ap = lows[anchor]
            band_lo, band_hi = ap * 0.985, ap * 1.015
            cluster = [i for i in valid_lo if band_lo <= lows[i] <= band_hi]
            if len(cluster) >= 2 and len(cluster) >= best_cluster_count:
                # 同樣數量時選較近的
                most_recent = max(cluster)
                if len(cluster) > best_cluster_count or most_recent > best_cluster_recent:
                    best_cluster_count = len(cluster)
                    best_cluster_recent = most_recent
                    best_cluster_price = float(np.mean([lows[i] for i in cluster]))
        if best_cluster_price and best_cluster_price < price * 0.999:
            ago = n - best_cluster_recent
            candidates.append((round(best_cluster_price, 2), "cluster_low",
                                f"低點密集區（{best_cluster_count}個低點聚集，最近{ago}根前）"))

    # ── 3. 整理平台低點（連續≥3根K棒波動≤2%，平台底部）──
    plat_start = 0
    best_plat = None
    best_plat_recent = -1
    for i in range(1, n):
        seg = range(plat_start, i + 1)
        seg_hi = max(highs[plat_start:i + 1])
        seg_lo = min(lows[plat_start:i + 1])
        if seg_lo > 0 and (seg_hi - seg_lo) / seg_lo * 100 > 2.0:
            length = i - plat_start
            if length >= 3:
                plo = min(lows[plat_start:i])
                if plo < price * 0.999 and i > best_plat_recent:
                    best_plat = (plo, plat_start, i - 1)
                    best_plat_recent = i
            plat_start = i
    # 檢查最後一段
    if n - plat_start >= 3:
        seg_hi = max(highs[plat_start:n])
        seg_lo = min(lows[plat_start:n])
        if seg_lo > 0 and (seg_hi - seg_lo) / seg_lo * 100 <= 2.0:
            plo = min(lows[plat_start:n])
            if plo < price * 0.999:
                best_plat = (plo, plat_start, n - 1)
                best_plat_recent = n - 1
    if best_plat:
        plo, ps, pe = best_plat
        length = pe - ps + 1
        ago = n - pe
        candidates.append((round(float(plo), 2), "platform_low",
                            f"整理平台低點（{length}根平台，{ago}根前結束）"))

    # ── 4. 爆量支撐 ──
    boom_idx = [i for i in range(20, n)
                if not np.isnan(vol_ma20[i])
                and volumes[i] > vol_ma20[i] * 1.5
                and lows[i] < price * 0.999]
    if boom_idx:
        recent = boom_idx[-3:]
        best = min(recent, key=lambda i: price - lows[i] if lows[i] < price else float('inf'))
        if lows[best] < price:
            ratio = volumes[best] / vol_ma20[best]
            candidates.append((round(float(lows[best]), 2), "volume_surge",
                               f"爆量支撐（{n - best}根前，{ratio:.1f}倍均量）"))

    # ── 5. 凹洞量支撐 ──
    hollow_idx = [i for i in range(20, n)
                  if not np.isnan(vol_ma20[i])
                  and volumes[i] < vol_ma20[i] * 0.5
                  and lows[i] < price * 0.999]
    if hollow_idx:
        recent = hollow_idx[-5:]
        best = min(recent, key=lambda i: price - lows[i] if lows[i] < price else float('inf'))
        if lows[best] < price:
            ratio = volumes[best] / vol_ma20[best]
            candidates.append((round(float(lows[best]), 2), "hollow_volume",
                               f"凹洞量支撐（{n - best}根前，量僅{ratio:.1f}倍均量）"))

    # ── 6. 均線動態支撐 ──
    for period, name in [(20, "MA20"), (60, "MA60")]:
        ma = calc_ma(closes, period)
        v = ma[-1]
        if not np.isnan(v) and v < price * 0.999:
            candidates.append((round(float(v), 2), f"ma{period}", f"{name} 動態支撐"))

    # ── 最終選擇：優先順序加權 ──
    # 來源權重：回測後低點 > 低點密集區 > 整理平台 > 爆量 > 凹洞量 > 均線
    SOURCE_WEIGHT = {
        "pullback_low": 6,
        "cluster_low":  5,
        "platform_low": 4,
        "volume_surge": 3,
        "hollow_volume":2,
        "ma20": 1, "ma60": 1,
    }
    below = [(p, src, desc) for p, src, desc in candidates if p < price]

    if below:
        # 分數 = 來源權重 + 距現價越近分數越高（最近現價 = 1，最遠 = 0）
        prices_only = [p for p, _, _ in below]
        price_range = (price - min(prices_only)) or 1
        def score(item):
            p, src, _ = item
            w = SOURCE_WEIGHT.get(src, 1)
            proximity = (p - min(prices_only)) / price_range  # 0~1，越接近現價越高
            return w * 2 + proximity
        best_item = max(below, key=score)
        support, support_source, support_desc = best_item
    else:
        support = round(float(lows[-20:].min()), 2)
        support_source = "recent_low"
        support_desc = "近20日最低點（備援）"

    # ── 壓力：轉折高點優先，再看近期最高 ──
    # 壓力選擇：現價以上最近的轉折高點，若多個則取最近且最低的（最容易被測試）
    valid_hi_idx = [i for i in hi_idx if highs[i] > price * 1.001]
    if valid_hi_idx:
        # 取最近30根內的轉折高點，沒有就取最近的一個
        recent_hi = [i for i in valid_hi_idx if i >= n - 60]
        pool = recent_hi if recent_hi else valid_hi_idx
        # 最近且最低的（最近壓力）
        nearest_hi = min(pool, key=lambda i: (highs[i], -(i)))
        resistance = round(float(highs[nearest_hi]), 2)
        resistance_desc = f"轉折高點（{n - nearest_hi}根前）"
    else:
        resistance = round(float(highs[-20:].max()), 2)
        resistance_desc = "近20日最高點（備援）"

    detail = {
        "support_source": support_source,
        "support_desc": support_desc,
        "resistance_desc": resistance_desc,
        "all_candidates": [
            {"price": p, "source": src, "desc": desc}
            for p, src, desc in sorted(below, key=lambda x: x[0], reverse=True)
        ],
    }
    return support, resistance, detail


# ══════════════════════════════════════════════════════════
# 風險評估與條列摘要
# ══════════════════════════════════════════════════════════
def calc_risk_level(price, support, resistance, rr_ratio, near_top, near_bot, pattern):
    """回傳風險等級與條列摘要"""
    sup_dist = (price - support) / price * 100
    res_dist = (resistance - price) / price * 100

    # 風險等級判斷
    if near_top or res_dist < 2:
        risk_level = "high"
        risk_label = "高風險"
        risk_color = "red"
    elif pattern in ["跌破型態"] or (near_bot and rr_ratio < 1):
        risk_level = "high"
        risk_label = "高風險"
        risk_color = "red"
    elif res_dist < 5 or rr_ratio < 1:
        risk_level = "medium"
        risk_label = "留意"
        risk_color = "amber"
    elif near_bot or sup_dist < 3:
        risk_level = "low"
        risk_label = "相對安全"
        risk_color = "green"
    else:
        risk_level = "watch"
        risk_label = "觀望"
        risk_color = "gray"

    return risk_level, risk_label, risk_color


def build_summary(price, support, support_desc, resistance, resistance_desc,
                  trend, pattern, rr_ratio, risk_level, risk_label,
                  near_top, near_bot, stop_loss, target1, rr_basis="防守位"):
    """條列式分析摘要"""
    sup_dist = (price - support) / price * 100
    res_dist = (resistance - price) / price * 100
    stop_dist = (price - stop_loss) / price * 100

    lines = []

    # 趨勢（加細節）
    trend_map = {
        "上升趨勢": "均線多頭排列，趨勢偏多，短均在長均之上，回測支撐是買點",
        "下降趨勢": "均線空頭排列，趨勢偏空，短均在長均之下，反彈壓力是賣點",
        "盤整":     "均線糾結，多空拉鋸，方向未明，等待突破方向再跟進",
    }
    lines.append(f"趨勢：{trend_map.get(trend, trend)}")

    # 現價位置
    lines.append(f"現價 {price}，距支撐 -{sup_dist:.1f}%，距壓力 +{res_dist:.1f}%")

    # 支撐說明
    lines.append(f"支撐 {support}（{support_desc}）")

    # 壓力說明
    lines.append(f"壓力 {resistance}（{resistance_desc}）")

    # 型態
    pattern_detail = {
        "突破型態": f"股價突破壓力 {resistance}，若縮量拉回不破壓力，壓力轉支撐，為強勢回測買點",
        "跌破型態": f"股價跌破支撐 {support}，前支撐轉壓力，應等穩定再重新評估，停損優先",
        "支撐整理": f"現價靠近支撐 {support}（-{sup_dist:.1f}%），為相對低風險觀察位，守住偏多，跌破停損",
        "壓力整理": f"現價靠近壓力 {resistance}（+{res_dist:.1f}%），追價風險高，等回測支撐 {support} 或放量突破再跟",
        "整理中":   f"現價位於支撐 {support} 與壓力 {resistance} 之間，等待方向訊號，不宜追高殺低",
    }
    lines.append(f"型態：{pattern_detail.get(pattern, pattern)}")

    # 風險（防守位）
    lines.append(f"防守位置 {stop_loss}（跌破停損，距現價 -{stop_dist:.1f}%）")

    # 損益比（說明計算基礎）
    if rr_ratio >= 2:
        rr_comment = "損益比良好，值得評估"
    elif rr_ratio >= 1.5:
        rr_comment = "損益比尚可"
    elif rr_ratio >= 1:
        rr_comment = "損益比偏低，需謹慎"
    else:
        rr_comment = "損益比不佳，風險大於報酬"
    lines.append(f"風險報酬 {rr_ratio}（以{rr_basis}為停損基準，{rr_comment}）")

    return lines


# ══════════════════════════════════════════════════════════
# 型態判斷
# ══════════════════════════════════════════════════════════
def detect_pattern(price, support, resistance, ch_lo, ch_hi):
    thr = 0.03
    if price > resistance * (1 + thr):
        return "突破型態", "現價突破壓力區"
    if price < support * (1 - thr):
        return "跌破型態", "現價跌破支撐區"
    if abs(price - support) / support < thr:
        return "支撐整理", "靠近支撐，觀察守住"
    if abs(price - resistance) / resistance < thr:
        return "壓力整理", "靠近壓力，注意量能"
    return "整理中", "位於區間中段"


# ══════════════════════════════════════════════════════════
# 葛蘭碧
# ══════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════
# 趨勢軌道計算
# ══════════════════════════════════════════════════════════
def calc_trend_line_y(x1, y1, x2, y2, x):
    if x2 == x1: return y1
    return y1 + (y2 - y1) / (x2 - x1) * (x - x1)


def find_trend_channel(highs, lows, closes):
    """
    用線性迴歸斜率找最佳軌道起點（R²最高）
    上升軌道：從最佳低點起，平行線複製到最高點
    下降軌道：從最佳高點起，平行線複製到最低點
    另外偵測水平支撐（橫盤區間下緣）
    """
    n_full = len(closes)
    if n_full < 30: return None
    price = closes[-1]

    # 只看最近 120 根，避免歷史走勢干擾近期軌道（用局部變數）
    LOOKBACK = min(n_full, 120)
    _offset  = n_full - LOOKBACK
    _highs   = highs[-LOOKBACK:]
    _lows    = lows[-LOOKBACK:]
    _closes  = closes[-LOOKBACK:]
    n        = LOOKBACK

    # ── 用 R² 找最佳上升軌道起點 ──────────────────────
    from scipy.stats import linregress
    order = max(3, min(8, n // 25))
    lo_idx = argrelextrema(_lows, np.less_equal, order=order)[0]
    hi_idx = argrelextrema(_highs, np.greater_equal, order=order)[0]

    best_up_r2    = 0.0
    best_up_start = None
    best_up_slope = 0.0
    best_up_intercept = 0.0

    # 從最近往回掃低點，找 R² 最高的上升軌道
    for start_lo in lo_idx:
        seg_idx = lo_idx[lo_idx >= start_lo]
        if len(seg_idx) < 2: continue
        x = seg_idx.astype(float)
        y = _lows[seg_idx]
        slope, intercept, r, _, _ = linregress(x, y)
        r2 = r ** 2
        if slope > 0 and r2 > best_up_r2:
            best_up_r2        = r2
            best_up_start     = start_lo
            best_up_slope     = slope
            best_up_intercept = intercept

    # ── 用 R² 找最佳下降軌道起點 ──────────────────────
    best_dn_r2    = 0.0
    best_dn_start = None
    best_dn_slope = 0.0
    best_dn_intercept = 0.0

    for start_hi in hi_idx:
        seg_idx = hi_idx[hi_idx >= start_hi]
        if len(seg_idx) < 2: continue
        x = seg_idx.astype(float)
        y = _highs[seg_idx]
        slope, intercept, r, _, _ = linregress(x, y)
        r2 = r ** 2
        if slope < 0 and r2 > best_dn_r2:
            best_dn_r2        = r2
            best_dn_start     = start_hi
            best_dn_slope     = slope
            best_dn_intercept = intercept

    curr = n - 1
    ext  = curr + 20

    # ── 決定主軌道類型 ──────────────────────────────────
    use_up = best_up_r2 >= 0.35
    use_dn = best_dn_r2 >= 0.35

    # 即使兩者都不足門檻，也選最佳的一個（避免沒有軌道線）
    if not use_up and not use_dn:
        if best_up_r2 > 0 or best_dn_r2 > 0:
            if best_up_r2 >= best_dn_r2:
                use_up = True
            else:
                use_dn = True

    def to_global(x_local):
        """將局部索引轉回全域索引（對應完整 bars 陣列）"""
        return int(x_local) + _offset

    if use_up and (not use_dn or best_up_r2 >= best_dn_r2):
        ctype, cdesc = "up", "上升軌道"
        s0 = int(best_up_start)
        lo_slope     = best_up_slope
        lo_intercept = best_up_intercept

        s_y_start = lo_intercept + lo_slope * s0
        s_y_curr  = lo_intercept + lo_slope * curr
        s_y_ext   = lo_intercept + lo_slope * ext
        s_line = {"x1": to_global(s0),   "y1": round(s_y_start, 2),
                  "x2": to_global(curr), "y2": round(s_y_curr,  2),
                  "x_ext": to_global(ext), "y_ext": round(s_y_ext, 2)}

        peak_idx = int(np.argmax(_highs[s0:])) + s0
        peak_y   = float(_highs[peak_idx])
        sup_at_peak = lo_intercept + lo_slope * peak_idx
        offset_y    = peak_y - sup_at_peak

        r_y_start = s_y_start + offset_y
        r_y_curr  = s_y_curr  + offset_y
        r_y_ext   = s_y_ext   + offset_y
        r_line = {"x1": to_global(s0),   "y1": round(r_y_start, 2),
                  "x2": to_global(curr), "y2": round(r_y_curr,  2),
                  "x_ext": to_global(ext), "y_ext": round(r_y_ext, 2)}

        support_now   = round(s_y_curr, 2)
        resist_now    = round(r_y_curr, 2)
        channel_width = abs(offset_y)

    elif use_dn:
        ctype, cdesc = "down", "下降軌道"
        s0 = int(best_dn_start)
        hi_slope     = best_dn_slope
        hi_intercept = best_dn_intercept

        r_y_start = hi_intercept + hi_slope * s0
        r_y_curr  = hi_intercept + hi_slope * curr
        r_y_ext   = hi_intercept + hi_slope * ext
        r_line = {"x1": to_global(s0),   "y1": round(r_y_start, 2),
                  "x2": to_global(curr), "y2": round(r_y_curr,  2),
                  "x_ext": to_global(ext), "y_ext": round(r_y_ext, 2)}

        trough_idx = int(np.argmin(_lows[s0:])) + s0
        trough_y   = float(_lows[trough_idx])
        res_at_trough = hi_intercept + hi_slope * trough_idx
        offset_y      = trough_y - res_at_trough

        s_y_start = r_y_start + offset_y
        s_y_curr  = r_y_curr  + offset_y
        s_y_ext   = r_y_ext   + offset_y
        s_line = {"x1": to_global(s0),   "y1": round(s_y_start, 2),
                  "x2": to_global(curr), "y2": round(s_y_curr,  2),
                  "x_ext": to_global(ext), "y_ext": round(s_y_ext, 2)}

        resist_now    = round(r_y_curr, 2)
        support_now   = round(s_y_curr, 2)
        channel_width = abs(offset_y)

    else:
        ctype, cdesc = "horizontal", "水平箱型整理"
        rec_lo = lo_idx[-2:] if len(lo_idx) >= 2 else lo_idx
        rec_hi = hi_idx[-2:] if len(hi_idx) >= 2 else hi_idx
        lo1, lo2 = int(rec_lo[-2]), int(rec_lo[-1])
        hi1, hi2 = int(rec_hi[-2]), int(rec_hi[-1])
        support_now = round(float(_lows[[lo1,lo2]].min()), 2)
        resist_now  = round(float(_highs[[hi1,hi2]].max()), 2)
        channel_width = abs(resist_now - support_now)
        s_line = {"x1":to_global(lo1),"y1":support_now,"x2":to_global(lo2),"y2":support_now,"x_ext":to_global(ext),"y_ext":support_now}
        r_line = {"x1":to_global(hi1),"y1":resist_now, "x2":to_global(hi2),"y2":resist_now, "x_ext":to_global(ext),"y_ext":resist_now}

    # ── 位置判斷 ────────────────────────────────────────
    dist_sup = (price - support_now) / support_now * 100 if support_now > 0 else 999
    dist_res = (resist_now - price)  / price * 100 if price > 0 else 999
    thr = 0.02

    if   price > resist_now * (1+thr):  pos,pdesc="breakout_up",  f"已突破上軌 {resist_now}，等幅目標 {round(resist_now+channel_width,2)}"
    elif price < support_now * (1-thr): pos,pdesc="breakout_dn",  f"已跌破下軌 {support_now}，注意下方空間"
    elif dist_res < 3:                  pos,pdesc="near_resist",  f"靠近上軌壓力 {resist_now}（+{dist_res:.1f}%），注意拉回設好防守"
    elif dist_sup < 3:                  pos,pdesc="near_support", f"靠近下軌支撐 {support_now}（-{dist_sup:.1f}%），相對低風險觀察位"
    else:                               pos,pdesc="middle",       f"位於軌道中段，距支撐 -{dist_sup:.1f}%，距壓力 +{dist_res:.1f}%"

    return {
        "type": ctype, "desc": cdesc,
        "r2": round(max(best_up_r2, best_dn_r2), 3),
        "position": pos, "position_desc": pdesc,
        "support_line": s_line, "resist_line": r_line,
        "support_now": support_now, "resist_now": resist_now,
        "channel_width": round(float(channel_width), 2),
        "target1": round(resist_now + channel_width, 2),
        "target2": round(resist_now + channel_width * 2, 2),
    }


def detect_triangle_channel(highs, lows, closes):
    """偵測三角形收斂/擴散型態"""
    from scipy.stats import linregress
    n_full = len(closes)
    if n_full < 20: return None
    LOOKBACK = min(n_full, 120)
    _offset  = n_full - LOOKBACK
    _highs   = highs[-LOOKBACK:]
    _lows    = lows[-LOOKBACK:]
    n        = LOOKBACK
    price    = closes[-1]
    order = max(3, min(8, n // 25))
    lo_idx = argrelextrema(_lows,  np.less_equal,    order=order)[0]
    hi_idx = argrelextrema(_highs, np.greater_equal, order=order)[0]
    if len(lo_idx) < 2 or len(hi_idx) < 2: return None
    def to_global(x): return int(x) + _offset
    xh = hi_idx.astype(float); yh = _highs[hi_idx]
    sh, ih, rh, _, _ = linregress(xh, yh)
    xl = lo_idx.astype(float); yl = _lows[lo_idx]
    sl, il, rl, _, _ = linregress(xl, yl)
    curr = n - 1; ext = curr + 20
    def line_y(s, i, x): return s * x + i
    converging = sh < -0.005 and sl > 0.005
    expanding  = sh > 0.005  and sl < -0.005
    mean_price = float(np.mean(closes[-LOOKBACK:]))
    asc_tri    = abs(sh) < 0.015 * mean_price / max(n, 1) and sl > 0.005
    desc_tri   = sh < -0.005 and abs(sl) < 0.015 * mean_price / max(n, 1)
    r2h = rh**2; r2l = rl**2
    if max(r2h, r2l) < 0.35: return None
    hi_curr = line_y(sh, ih, curr); lo_curr = line_y(sl, il, curr)
    hi_ext  = line_y(sh, ih, ext);  lo_ext  = line_y(sl, il, ext)
    hi_s0   = line_y(sh, ih, hi_idx[0]); lo_s0 = line_y(sl, il, lo_idx[0])
    channel_width = abs(hi_curr - lo_curr)
    s_line = {"x1": to_global(lo_idx[0]), "y1": round(lo_s0, 2),
              "x2": to_global(curr),       "y2": round(lo_curr, 2),
              "x_ext": to_global(ext),     "y_ext": round(lo_ext, 2)}
    r_line = {"x1": to_global(hi_idx[0]), "y1": round(hi_s0, 2),
              "x2": to_global(curr),       "y2": round(hi_curr, 2),
              "x_ext": to_global(ext),     "y_ext": round(hi_ext, 2)}
    support_now = round(lo_curr, 2); resist_now = round(hi_curr, 2)
    if converging:
        ctype, cdesc = "converging", "收斂三角形"
        target_up = round(resist_now + channel_width, 2)
        target_dn = round(support_now - channel_width, 2)
        pdesc = f"收斂三角整理，上破 {resist_now:.1f} 目標 {target_up}，下破 {support_now:.1f} 目標 {target_dn}"
    elif expanding:
        ctype, cdesc = "expanding", "擴散三角形（波動加大）"
        pdesc = f"擴散三角，上緣 {resist_now:.1f} / 下緣 {support_now:.1f}，操作難度高"
    elif asc_tri:
        ctype, cdesc = "ascending_tri", "上升三角形（偏多）"
        target = round(resist_now + channel_width, 2)
        pdesc = f"上升三角，壓力 {resist_now:.1f} 反覆測試，突破後目標 {target}"
    elif desc_tri:
        ctype, cdesc = "descending_tri", "下降三角形（偏空）"
        target = round(support_now - channel_width, 2)
        pdesc = f"下降三角，支撐 {support_now:.1f} 反覆測試，跌破後目標 {target}"
    else:
        return None
    dist_sup = (price - support_now) / support_now * 100 if support_now > 0 else 999
    dist_res = (resist_now - price)  / price * 100 if price > 0 else 999
    if   price > resist_now * 1.02:  pos = "breakout_up"
    elif price < support_now * 0.98: pos = "breakout_dn"
    elif dist_res < 3:               pos = "near_resist"
    elif dist_sup < 3:               pos = "near_support"
    else:                            pos = "middle"
    return {
        "type": ctype, "desc": cdesc, "r2": round((r2h+r2l)/2, 3),
        "position": pos, "position_desc": pdesc,
        "support_line": s_line, "resist_line": r_line,
        "support_now": support_now, "resist_now": resist_now,
        "channel_width": round(float(channel_width), 2),
        "target1": round(resist_now + channel_width, 2),
        "target2": round(resist_now + channel_width * 2, 2),
    }


def detect_reversal_pattern(highs, lows, closes):
    """偵測反轉型態：W底、M頭、頭肩底、頭肩頂"""
    LOOKBACK = min(len(closes), 120)
    _offset  = len(closes) - LOOKBACK
    _h = highs[-LOOKBACK:]; _l = lows[-LOOKBACK:]
    n  = LOOKBACK; price = closes[-1]
    order = max(3, min(8, n // 20))
    lo_idx = argrelextrema(_l, np.less_equal,    order=order)[0].tolist()
    hi_idx = argrelextrema(_h, np.greater_equal, order=order)[0].tolist()
    def to_global(x): return int(x) + _offset

    # W底
    if len(lo_idx) >= 2:
        for i in range(len(lo_idx)-1, 0, -1):
            l2, l1 = lo_idx[i], lo_idx[i-1]
            if l2 - l1 < 5: continue
            v1, v2 = _l[l1], _l[l2]
            if abs(v1-v2)/max(v1, 0.001) > 0.04: continue
            neck = float(_h[l1:l2].max())
            if price >= neck * 0.98:
                target = round(neck + (neck - min(v1, v2)), 2)
                broken = bool(price >= neck * 1.005)
                return {
                    "type": "double_bottom", "desc": "W底（雙底）",
                    "neckline": round(neck, 2), "target": float(target), "broken": broken,
                    "position_desc": f"{'已突破頸線' if broken else '接近頸線'} {neck:.1f}，目標 {target}",
                    "support_now": round(min(v1, v2)*0.99, 2), "resist_now": round(neck, 2),
                    "support_line": None, "resist_line": None,
                    "channel_width": round(neck-min(v1, v2), 2),
                    "target1": target, "target2": round(target+(target-neck), 2),
                }
            break

    # M頭
    if len(hi_idx) >= 2:
        for i in range(len(hi_idx)-1, 0, -1):
            h2, h1 = hi_idx[i], hi_idx[i-1]
            if h2 - h1 < 5: continue
            v1, v2 = _h[h1], _h[h2]
            if abs(v1-v2)/max(v1, 0.001) > 0.04: continue
            neck = float(_l[h1:h2].min())
            if price <= neck * 1.02:
                target = round(neck - (max(v1, v2) - neck), 2)
                broken = bool(price <= neck * 0.995)
                return {
                    "type": "double_top", "desc": "M頭（雙頭）",
                    "neckline": round(neck, 2), "target": float(target), "broken": broken,
                    "position_desc": f"{'已跌破頸線' if broken else '接近頸線'} {neck:.1f}，下行目標 {target}",
                    "support_now": round(neck, 2), "resist_now": round(max(v1, v2), 2),
                    "support_line": None, "resist_line": None,
                    "channel_width": round(max(v1, v2)-neck, 2),
                    "target1": target, "target2": round(target-(neck-target), 2),
                }
            break

    # 頭肩頂
    if len(hi_idx) >= 3:
        for i in range(len(hi_idx)-1, 1, -1):
            rs, head, ls = hi_idx[i], hi_idx[i-1], hi_idx[i-2]
            if rs - ls < 10: continue
            ls_h, head_h, rs_h = _h[ls], _h[head], _h[rs]
            if not (head_h > ls_h*1.02 and head_h > rs_h*1.02): continue
            if abs(ls_h-rs_h)/max(ls_h, 0.001) > 0.06: continue
            neck = (float(_l[ls:head].min()) + float(_l[head:rs].min())) / 2
            if price <= neck * 1.02:
                target = round(neck - (head_h - neck), 2)
                broken = bool(price <= neck * 0.995)
                return {
                    "type": "head_shoulders_top", "desc": "頭肩頂",
                    "neckline": round(neck, 2), "target": float(target), "broken": broken,
                    "position_desc": f"頭肩頂，{'已跌破頸線' if broken else '頸線'} {neck:.1f}，下行目標 {target}",
                    "support_now": round(neck, 2), "resist_now": round(head_h, 2),
                    "support_line": None, "resist_line": None,
                    "channel_width": round(head_h-neck, 2),
                    "target1": target, "target2": round(target-(neck-target), 2),
                }
            break

    # 頭肩底
    if len(lo_idx) >= 3:
        for i in range(len(lo_idx)-1, 1, -1):
            rs, head, ls = lo_idx[i], lo_idx[i-1], lo_idx[i-2]
            if rs - ls < 10: continue
            ls_l, head_l, rs_l = _l[ls], _l[head], _l[rs]
            if not (head_l < ls_l*0.98 and head_l < rs_l*0.98): continue
            if abs(ls_l-rs_l)/max(ls_l, 0.001) > 0.06: continue
            neck = (float(_h[ls:head].max()) + float(_h[head:rs].max())) / 2
            if price >= neck * 0.98:
                target = round(neck + (neck - head_l), 2)
                broken = bool(price >= neck * 1.005)
                return {
                    "type": "head_shoulders_bottom", "desc": "頭肩底",
                    "neckline": round(neck, 2), "target": float(target), "broken": broken,
                    "position_desc": f"頭肩底，{'已突破頸線' if broken else '頸線'} {neck:.1f}，上行目標 {target}",
                    "support_now": round(head_l, 2), "resist_now": round(neck, 2),
                    "support_line": None, "resist_line": None,
                    "channel_width": round(neck-head_l, 2),
                    "target1": target, "target2": round(target+(target-neck), 2),
                }
            break

    return None
    """葛蘭碧 + 量能過濾 + 防守點"""
    n = len(closes)
    ma = np.full(n, np.nan)
    for i in range(ma_period-1, n):
        ma[i] = closes[i-ma_period+1:i+1].mean()
    vol_ma = np.full(n, np.nan)
    for i in range(19, n):
        vol_ma[i] = volumes[i-19:i+1].mean()
    buys, sells, stops = [], [], []
    for i in range(ma_period+1, n):
        if any(np.isnan(x) for x in [ma[i], ma[i-1], ma[i-2], vol_ma[i]]): continue
        ma_up   = ma[i] > ma[i-2]
        ma_dn   = ma[i] < ma[i-2]
        vol_big = volumes[i] > vol_ma[i] * 1.2
        if closes[i-1] < ma[i-1] and closes[i] > ma[i] and ma_up and vol_big:
            buys.append(i)
            stops.append(round(min(float(lows[i]), float(ma[i])), 2))
        elif closes[i-1] > ma[i-1] and closes[i] < ma[i] and ma_dn and vol_big:
            sells.append(i)
    return buys[-3:], sells[-3:], stops[-3:]


def gann_signals(closes, ma20):
    buys, sells = [], []
    for i in range(1, len(closes)):
        if np.isnan(ma20[i]) or np.isnan(ma20[i - 1]):
            continue
        if closes[i - 1] < ma20[i - 1] and closes[i] > ma20[i]:
            buys.append(i)
        elif closes[i - 1] > ma20[i - 1] and closes[i] < ma20[i]:
            sells.append(i)
    return buys[-3:], sells[-3:]


def calc_gann_filtered(closes, highs, lows, volumes, ma_period=20):
    """葛蘭碧 + 量能過濾 + 防守點"""
    n = len(closes)
    ma = np.full(n, np.nan)
    for i in range(ma_period-1, n):
        ma[i] = closes[i-ma_period+1:i+1].mean()
    vol_ma = np.full(n, np.nan)
    for i in range(19, n):
        vol_ma[i] = volumes[i-19:i+1].mean()
    buys, sells, stops = [], [], []
    for i in range(ma_period+1, n):
        if any(np.isnan(x) for x in [ma[i], ma[i-1], ma[i-2], vol_ma[i]]): continue
        ma_up   = ma[i] > ma[i-2]
        ma_dn   = ma[i] < ma[i-2]
        vol_big = volumes[i] > vol_ma[i] * 1.2
        if closes[i-1] < ma[i-1] and closes[i] > ma[i] and ma_up and vol_big:
            buys.append(i)
            stops.append(round(min(float(lows[i]), float(ma[i])), 2))
        elif closes[i-1] > ma[i-1] and closes[i] < ma[i] and ma_dn and vol_big:
            sells.append(i)
    return buys[-3:], sells[-3:], stops[-3:]


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


# ══════════════════════════════════════════════════════════
# API 快取（同股票+時間框架，5分鐘內不重複抓取）
# ══════════════════════════════════════════════════════════
import time as _time
_analyze_cache: dict = {}   # key: "{stock_id}_{tf}" → {"ts": float, "data": dict}
_CACHE_TTL = 300            # 5 分鐘

def _cache_get(key: str):
    entry = _analyze_cache.get(key)
    if entry and (_time.time() - entry["ts"]) < _CACHE_TTL:
        return entry["data"]
    return None

def _cache_set(key: str, data: dict):
    _analyze_cache[key] = {"ts": _time.time(), "data": data}
    # 清理過期快取，避免記憶體堆積（超過 200 筆時清掉舊的）
    if len(_analyze_cache) > 200:
        cutoff = _time.time() - _CACHE_TTL
        expired = [k for k, v in _analyze_cache.items() if v["ts"] < cutoff]
        for k in expired:
            _analyze_cache.pop(k, None)


# ══════════════════════════════════════════════════════════
# 端點
# ══════════════════════════════════════════════════════════
PERIOD_MAP = {"D": ("3y", "1d"), "W": ("5y", "1wk"), "M": ("10y", "1mo")}


@app.get("/api/kline/{stock_id}")
def get_kline(stock_id: str, tf: str = "D"):
    period, interval = PERIOD_MAP.get(tf.upper(), ("3y", "1d"))
    try:
        symbol, df = try_fetch(stock_id, period, interval)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"下載失敗：{e}")
    if df.empty:
        raise HTTPException(status_code=404, detail=f"找不到股票：{stock_id}")
    df = df[["Open", "High", "Low", "Close", "Volume"]].dropna()
    records = []
    for idx, row in df.iterrows():
        date_str = idx.strftime("%Y-%m-%d") if hasattr(idx, "strftime") else str(idx)[:10]
        records.append({
            "date": date_str,
            "open": safe_float(row["Open"]), "high": safe_float(row["High"]),
            "low": safe_float(row["Low"]),   "close": safe_float(row["Close"]),
            "volume": int(row["Volume"]) if not np.isnan(row["Volume"]) else 0,
        })
    return {"symbol": symbol, "tf": tf, "count": len(records), "bars": records}


@app.get("/api/analyze/{stock_id}")
def analyze(stock_id: str, tf: str = "D",
            ma1: int = 5, ma2: int = 10, ma3: int = 20, ma4: int = 60, ma5: int = 120):
    # 快取：同股票+時間框架 5 分鐘內直接回傳
    _cache_key = f"{stock_id.strip().upper()}_{tf.upper()}"
    cached = _cache_get(_cache_key)
    if cached:
        return cached

    period, interval = PERIOD_MAP.get(tf.upper(), ("3y", "1d"))
    try:
        symbol, df = try_fetch(stock_id, period, interval)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    if df.empty:
        raise HTTPException(status_code=404, detail=f"找不到股票：{stock_id}")

    df = df[["Open", "High", "Low", "Close", "Volume"]].dropna()
    opens      = df["Open"].values.astype(float)
    closes     = df["Close"].values.astype(float)
    closes_full= closes.copy()   # 保留完整序列供 MA 計算
    highs      = df["High"].values.astype(float)
    lows       = df["Low"].values.astype(float)
    volumes    = df["Volume"].values.astype(float)
    price      = round(float(closes[-1]), 2)

    # 股名
    stock_name = get_stock_name(symbol)

    # 均線
    ma_periods = [p for p in [ma1, ma2, ma3, ma4, ma5] if p and p > 0]
    ma_values = {f"ma{p}": safe_float(calc_ma(closes, p)[-1]) for p in ma_periods}

    # 趨勢
    avail = [(p, calc_ma(closes, p)[-1]) for p in sorted(ma_periods)
             if not np.isnan(calc_ma(closes, p)[-1])]
    trend = "觀察中"
    if len(avail) >= 2:
        s, l = avail[0][1], avail[-1][1]
        trend = "上升趨勢" if s > l * 1.005 else "下降趨勢" if s < l * 0.995 else "盤整"

    # 支撐壓力
    support, resistance, supp_detail = find_support_resistance(
        highs, lows, closes, volumes, price)

    # 軌道
    ch_hi    = round(float(highs[-20:].max()), 2)
    ch_lo    = round(float(lows[-20:].min()), 2)
    near_top = price > ch_hi * 0.97
    near_bot = price < ch_lo * 1.03

    # 趨勢軌道（先算，軌道上下緣納入支撐壓力）
    channel = find_trend_channel(highs, lows, closes)

    # 若直線軌道 R² 不高，嘗試三角形型態
    if not channel or channel.get("r2", 0) < 0.6:
        tri = detect_triangle_channel(highs, lows, closes)
        if tri and tri.get("r2", 0) > (channel.get("r2", 0) if channel else 0):
            channel = tri

    # 反轉型態（W底/M頭/頭肩）— 優先級最高，若找到則覆蓋軌道
    reversal = detect_reversal_pattern(highs, lows, closes)
    if reversal:
        # 反轉型態找到時，整合進 channel 但保留軌道線顯示
        reversal_desc = reversal["desc"]
        reversal_pos  = reversal["position_desc"]
        # 反轉型態的支撐壓力比軌道更重要
        if reversal.get("support_now") and reversal["support_now"] < price:
            support    = reversal["support_now"]
            supp_detail["support_desc"]   = f"{reversal['desc']} 支撐"
            supp_detail["support_source"] = reversal["type"]
        if reversal.get("resist_now") and reversal["resist_now"] > price:
            resistance = reversal["resist_now"]
            supp_detail["resistance_desc"] = f"{reversal['desc']} 頸線/壓力"
    else:
        reversal_desc = None
        reversal_pos  = None

    # 支撐距現價 >8% 時降級，改用 MA20 或 MA60 補位
    sup_dist_pct = (price - support) / price * 100
    if sup_dist_pct > 8:
        ma20_val = safe_float(calc_ma(closes_full, 20)[-1])
        ma60_val = safe_float(calc_ma(closes_full, 60)[-1])
        for ma_v, ma_name in [(ma20_val, "MA20"), (ma60_val, "MA60")]:
            if not np.isnan(ma_v) and ma_v < price * 0.999:
                new_dist = (price - ma_v) / price * 100
                if new_dist < sup_dist_pct:
                    support = round(float(ma_v), 2)
                    supp_detail["support_source"] = "ma_fallback"
                    supp_detail["support_desc"] = f"{ma_name} 動態支撐（原支撐過遠已降級）"
                    sup_dist_pct = new_dist
                    break

    # 軌道上下緣補充進支撐壓力
    if channel:
        ch_sup = channel.get("support_now", 0)
        ch_res = channel.get("resist_now", 0)
        # 軌道下緣：若在現價以下且比現有支撐更近，則取代
        if ch_sup > 0 and ch_sup < price * 0.999:
            if ch_sup > support:  # 更接近現價
                support = round(ch_sup, 2)
                supp_detail["support_source"] = "channel_low"
                supp_detail["support_desc"] = f"上升軌道下緣（{channel['desc']}）"
        # 軌道上緣：若在現價以上且比現有壓力更近，則取代
        if ch_res > 0 and ch_res > price * 1.001:
            if ch_res < resistance:  # 更接近現價
                resistance = round(ch_res, 2)
                supp_detail["resistance_desc"] = f"上升軌道上緣（{channel['desc']}）"

    # 型態
    pattern, pattern_sub = detect_pattern(price, support, resistance, ch_lo, ch_hi)

    # K棒型態辨識
    kbar_pattern, kbar_warning, kbar_dir = detect_kbar_pattern(opens, highs, lows, closes)

    # 葛蘭碧（加量能過濾）
    ma20_arr = calc_ma(closes, 20)
    buy_idx, sell_idx, buy_stops = calc_gann_filtered(closes, highs, lows, volumes, 20)

    # 突破壓力 / 跌破支撐訊號
    breakout_idx, breakdown_idx, breakout_stale, breakdown_stale = calc_breakout_signals(
        closes, highs, lows, volumes, support, resistance)

    # 防守位：支撐下 1.5%，最小距現價 2%，最大不超過現價 10%
    raw_stop  = round(support * 0.985, 2)
    min_stop  = round(price * 0.98, 2)   # 最近不能超過現價 2%
    max_stop  = round(price * 0.90, 2)   # 最遠不超過現價 10%
    stop_loss = min(min_stop, max(raw_stop, max_stop))

    # 目標價
    target1 = resistance
    if channel and channel.get("target1"):
        target2 = channel["target1"]
    else:
        target2 = round(resistance * 1.10, 2)

    # 風險報酬：改用「現價-防守位」當風險，防守位已有最小2%保護
    # 避免支撐太近時（如 -0.7%）導致 RR 爆大失真
    risk   = price - stop_loss          # 以防守位為停損基準
    reward = target1 - price
    rr_ratio = round(reward / risk, 2) if risk > 0 else 0
    rr_basis  = "防守位"               # 說明計算基礎，供前端顯示

    # 風險等級
    risk_level, risk_label, risk_color = calc_risk_level(
        price, support, resistance, rr_ratio, near_top, near_bot, pattern)

    # 條列摘要
    summary_lines = build_summary(
        price, support, supp_detail["support_desc"],
        resistance, supp_detail["resistance_desc"],
        trend, pattern, rr_ratio, risk_level, risk_label,
        near_top, near_bot, stop_loss, target1, rr_basis)

    # K棒型態加進摘要
    if kbar_pattern:
        summary_lines.append(f"K棒型態：{kbar_pattern}")
    if kbar_warning:
        summary_lines.append(f"⚠ {kbar_warning}")

    # ── 最終結論整合器 ──

    # 軌道與均線趨勢是否矛盾（需在使用 conflict_note 之前計算）
    channel_type = channel.get("type", "") if channel else ""
    trend_channel_conflict = (
        (trend == "上升趨勢" and channel_type == "down") or
        (trend == "下降趨勢" and channel_type == "up")
    )
    conflict_note = ""
    if trend_channel_conflict:
        if trend == "上升趨勢" and channel_type == "down":
            conflict_note = f"⚠ 注意：均線多頭但股價在下降軌道內，短線結構偏弱，均線支撐可能失守，建議觀望或輕倉"
        elif trend == "下降趨勢" and channel_type == "up":
            conflict_note = f"⚠ 注意：均線空頭但股價在上升軌道內，反彈動能存在但趨勢仍弱，等均線轉向確認再追"

    # 軌道趨勢矛盾警告（插在最前面，醒目位置）
    if conflict_note:
        summary_lines.insert(0, conflict_note)

    # 反轉/三角型態加進摘要
    if reversal:
        summary_lines.insert(0, f"圖形型態：{reversal['desc']}，{reversal['position_desc']}")

    # K棒方向判斷（含操作建議）
    kbar_bullish = any(k in kbar_pattern for k in ["錘頭","多頭吞噬","早晨之星","三紅兵","穿刺線","大紅棒"]) if kbar_pattern else False
    kbar_bearish = any(k in kbar_pattern for k in ["射擊之星","空頭吞噬","黃昏之星","三烏鴉","烏雲蓋頂","大黑棒"]) if kbar_pattern else False
    kbar_neutral = not kbar_bullish and not kbar_bearish

    # K棒操作說明對照（具體化）
    KBAR_ACTION = {
        "錘頭線":       f"明天收紅且量縮可試多，停損設今日低點 {round(float(lows[-1]),2)} 下方",
        "射擊之星":     f"明天若開低收黑，減碼或停損，停損設今日高點 {round(float(highs[-1]),2)} 上方",
        "十字星":       f"方向未定，等明天收盤確認，不宜追高也不宜殺低",
        "大紅棒":       f"今日強攻，明天若縮量整理不跌破今日收盤 {round(float(closes[-1]),2)}，多頭延續可持有",
        "大黑棒":       f"今日強殺，明天若無法收復今日一半 {round((float(opens[-1])+float(closes[-1]))/2,2)}，持續空頭，持有者停損",
        "多頭吞噬":     f"底部反轉訊號，明天收紅確認後可設防守位 {stop_loss} 試多",
        "空頭吞噬":     f"頂部反轉訊號，明天收黑確認後應減碼，停損設今日高點 {round(float(highs[-1]),2)}",
        "孕線":         f"整理型態，等突破今日高低點再進場，不宜在盤中追價",
        "穿刺線":       f"底部潛在反轉，明天若繼續收紅可加碼，停損設前低 {support}",
        "烏雲蓋頂":     f"頂部潛在反轉，明天若收黑應減碼，停損設今日高點 {round(float(highs[-1]),2)}",
        "早晨之星":     f"底部強力反轉，確認訊號，可設防守位 {stop_loss} 進場，目標看 {resistance}",
        "黃昏之星":     f"頂部強力反轉，應立即檢視持倉，停損設三根K棒最高點 {round(float(highs[-3:].max()),2)}",
        "三紅兵":       f"多頭強勢，可持有，但連漲三天後注意追高風險，不宜此時首次進場",
        "三烏鴉":       f"空頭強勢，持倉應全數停損，等企穩再重新評估",
    }

    # 找對應的操作說明
    kbar_action = ""
    for key, action in KBAR_ACTION.items():
        if kbar_pattern and key in kbar_pattern:
            kbar_action = action
            break

    near_sup = pattern in ("支撐整理",) or (price - support) / price < 0.04
    near_res = pattern in ("壓力整理",) or (resistance - price) / price < 0.04

    if near_sup:
        if rr_ratio >= 1.5 and kbar_bullish:
            conclusion = f"靠近支撐 {support}，出現多頭K棒（{kbar_pattern}），損益比 {rr_ratio} 佳。操作：{kbar_action or f'可設防守位 {stop_loss} 試多，目標壓力 {resistance}'}"
        elif rr_ratio >= 1.5 and kbar_neutral:
            conclusion = f"靠近支撐 {support}，K棒方向未定（{kbar_pattern or '無明確型態'}）。操作：等明天收盤確認方向再進場，防守位 {stop_loss}"
        elif rr_ratio >= 1.5 and kbar_bearish:
            conclusion = f"靠近支撐 {support}，但出現空頭K棒（{kbar_pattern}），支撐恐失守。操作：{kbar_action or f'先觀望，跌破 {support} 停損出場'}"
        else:
            conclusion = f"靠近支撐 {support}，但損益比 {rr_ratio} 偏低（壓力 {resistance} 太遠或太近）。操作：等支撐確認守住再評估，防守位 {stop_loss}"
    elif near_res:
        if kbar_bullish:
            conclusion = f"靠近壓力 {resistance}，出現多頭K棒（{kbar_pattern}）。操作：{kbar_action or f'等放量突破 {resistance} 再追，未突破先觀望，停損 {stop_loss}'}"
        elif kbar_bearish:
            conclusion = f"靠近壓力 {resistance}，出現空頭K棒（{kbar_pattern}），拉回風險高。操作：{kbar_action or f'減碼或觀望，回測支撐 {support} 再評估'}"
        else:
            conclusion = f"靠近壓力 {resistance}，追價風險高。操作：等放量突破確認後再跟，或等回測支撐 {support} 後進場，停損 {stop_loss}"
    elif pattern == "突破型態":
        conclusion = f"股價突破壓力 {resistance}。操作：{'縮量回測不破可加碼，停損設' + str(stop_loss) if not kbar_bearish else f'出現{kbar_pattern}，留意假突破，停損設 {stop_loss}'}"
    elif pattern == "跌破型態":
        conclusion = f"股價跌破支撐 {support}，前支撐轉壓力。操作：{'持倉停損 ' + str(stop_loss) + '，等止跌再重新評估' if not kbar_bullish else f'出現{kbar_pattern}，觀察是否為假跌破，守住 {support} 才考慮反彈操作'}"
    else:
        if kbar_bullish:
            conclusion = f"位於軌道中段，出現多頭K棒（{kbar_pattern}）。操作：{kbar_action or f'可小量試多，等突破壓力 {resistance} 確認再加碼，停損 {stop_loss}'}"
        elif kbar_bearish:
            conclusion = f"位於軌道中段，出現空頭K棒（{kbar_pattern}）。操作：{kbar_action or f'減碼觀望，跌破支撐 {support} 停損，等止跌再評估'}"
        else:
            conclusion = f"位於軌道中段，方向未明。操作：觀望為主，等突破 {resistance} 或跌破 {support} 再跟進，防守位 {stop_loss}"

    # 移除舊的 warning，改用整合結論
    warning = conclusion

    # 技術指標
    rsi_arr  = calc_rsi(closes)
    macd_line, macd_sig, macd_hist = calc_macd(closes)
    k_arr, d_arr = calc_kd(highs, lows, closes)
    bb_mid, bb_upper, bb_lower = calc_bollinger(closes)
    obv_arr  = calc_obv(closes, volumes)

    indicators = {
        "rsi":       serialize_indicator(rsi_arr, 1),
        "macd":      serialize_indicator(macd_line, 3),
        "macd_sig":  serialize_indicator(macd_sig, 3),
        "macd_hist": serialize_indicator(macd_hist, 3),
        "k":         serialize_indicator(k_arr, 1),
        "d":         serialize_indicator(d_arr, 1),
        "bb_mid":    serialize_indicator(bb_mid, 2),
        "bb_upper":  serialize_indicator(bb_upper, 2),
        "bb_lower":  serialize_indicator(bb_lower, 2),
        "obv":       serialize_indicator(obv_arr, 0),
    }

    # K 線資料
    bars = []
    for i in range(len(df)):
        d = df.index[i]
        date_str = d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else str(d)[:10]
        bars.append({
            "date": date_str,
            "open":   safe_float(df["Open"].iloc[i]),
            "high":   safe_float(df["High"].iloc[i]),
            "low":    safe_float(df["Low"].iloc[i]),
            "close":  safe_float(df["Close"].iloc[i]),
            "volume": int(df["Volume"].iloc[i]) if not np.isnan(df["Volume"].iloc[i]) else 0,
        })

    result = {
        "symbol": symbol, "stock_id": stock_id, "stock_name": stock_name, "tf": tf,
        "price": price,
        "support": support, "support_desc": supp_detail["support_desc"],
        "support_source": supp_detail["support_source"],
        "support_candidates": supp_detail["all_candidates"],
        "resistance": resistance, "resistance_desc": supp_detail["resistance_desc"],
        "upper_channel": ch_hi, "lower_channel": ch_lo,
        "trend": trend, "pattern": pattern, "pattern_sub": pattern_sub,
        "stop_loss": stop_loss, "target1": target1, "target2": target2,
        "risk_reward": rr_ratio, "rr_basis": rr_basis,
        "risk_level": risk_level, "risk_label": risk_label, "risk_color": risk_color,
        "summary": summary_lines,
        "warning": warning,
        "conflict_note": conflict_note,
        "kbar_pattern": kbar_pattern, "kbar_warning": kbar_warning,
        "kbar_dir": kbar_dir, "kbar_action": kbar_action,
        "near_top": near_top, "near_bot": near_bot,
        "ma_values": ma_values, "buy_signals": buy_idx, "sell_signals": sell_idx,
        "buy_stops": buy_stops, "channel": channel,
        "breakout_idx": breakout_idx,
        "breakdown_idx": breakdown_idx,
        "breakout_stale": breakout_stale,
        "breakdown_stale": breakdown_stale,
        "reversal_pattern": reversal,
        "indicators": indicators,
        "bars": bars,
    }
    _cache_set(_cache_key, result)
    return result


@app.get("/api/top_gainers")
def get_top_gainers(limit: int = 10):
    """
    當日（或最近交易日）漲幅前幾名
    用 FinMind TaiwanStockPrice 抓最新一日全市場資料
    """
    import urllib.request, json as _json
    from datetime import date, timedelta

    # 往回找最近 5 個交易日，避免假日
    token = FINMIND_TOKEN
    for days_back in range(1, 6):
        target = (date.today() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        try:
            url = (f"https://api.finmindtrade.com/api/v4/data"
                   f"?dataset=TaiwanStockPrice&start_date={target}&end_date={target}"
                   f"&token={token}")
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = _json.loads(resp.read())
            rows = data.get("data", [])
            # 過濾：只留4碼純數字、有成交量、股本不太小
            rows = [r for r in rows
                    if str(r.get("stock_id","")).isdigit()
                    and len(str(r.get("stock_id",""))) == 4
                    and r.get("Trading_Volume", 0) > 500000
                    and r.get("open", 0) > 0]
            if not rows:
                continue
            # 計算漲幅
            for r in rows:
                try:
                    r["change_pct"] = round(
                        (r["close"] - r["open"]) / r["open"] * 100, 2)
                except Exception:
                    r["change_pct"] = 0
            # 排序取前 limit 名
            top = sorted(rows, key=lambda r: r["change_pct"], reverse=True)[:limit]
            # 補上股名
            all_info = get_all_stock_info()
            name_map = {s["stock_id"]: s.get("stock_name","") for s in all_info}
            result = [{
                "stock_id": r["stock_id"],
                "stock_name": name_map.get(r["stock_id"], ""),
                "close": r["close"],
                "change_pct": r["change_pct"],
            } for r in top]
            return {"date": target, "gainers": result}
        except Exception as e:
            print(f"top_gainers 嘗試 {target} 失敗：{e}")
            continue

    # 全部失敗，回傳預設清單
    fallback = [
        {"stock_id":"2330","stock_name":"台積電","close":0,"change_pct":0},
        {"stock_id":"2317","stock_name":"鴻海","close":0,"change_pct":0},
        {"stock_id":"2454","stock_name":"聯發科","close":0,"change_pct":0},
        {"stock_id":"2308","stock_name":"台達電","close":0,"change_pct":0},
        {"stock_id":"2412","stock_name":"中華電","close":0,"change_pct":0},
        {"stock_id":"2882","stock_name":"國泰金","close":0,"change_pct":0},
        {"stock_id":"3008","stock_name":"大立光","close":0,"change_pct":0},
    ]
    return {"date": "", "gainers": fallback}


@app.get("/")
def root():
    return {"status": "ok", "app": "線上有位 API", "version": "1.3.0"}


# ── FinMind 股票資料快取 ──
_stock_info_cache: list = []
_stock_info_ts: float = 0.0

def get_all_stock_info() -> list:
    """取得全台股基本資料（帶快取，每天更新一次）"""
    import time
    global _stock_info_cache, _stock_info_ts
    if _stock_info_cache and (time.time() - _stock_info_ts) < 86400:
        return _stock_info_cache
    try:
        import urllib.request, json as _json
        url = (f"https://api.finmindtrade.com/api/v4/data"
               f"?dataset=TaiwanStockInfo&token={FINMIND_TOKEN}")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = _json.loads(resp.read())
        if data.get("status") == 200:
            _stock_info_cache = data.get("data", [])
            _stock_info_ts = time.time()
    except Exception as e:
        print(f"FinMind StockInfo 失敗：{e}")
    return _stock_info_cache



@app.get("/api/search")
def search_stock(q: str, limit: int = 10):
    """
    股票搜尋：支援代號（2330）或中文名稱（台積電、律勝）
    回傳最多 limit 筆匹配結果
    """
    q = q.strip()
    if not q:
        return {"results": []}

    all_stocks = get_all_stock_info()

    # 先用 STOCK_NAMES 對照表補充（確保常用股都查得到）
    static_map = {v: k for k, v in STOCK_NAMES.items()}  # 名稱 → 代號

    results = []
    q_lower = q.lower()

    # 1. 完全匹配代號（最高優先）
    exact = [s for s in all_stocks
             if str(s.get("stock_id","")).lower() == q_lower]

    # 2. 代號前綴匹配（如輸入 "235"）
    prefix_id = [s for s in all_stocks
                 if str(s.get("stock_id","")).startswith(q)
                 and str(s.get("stock_id","")).lower() != q_lower]

    # 3. 名稱包含關鍵字
    name_match = [s for s in all_stocks
                  if q in str(s.get("stock_name",""))
                  and str(s.get("stock_id","")).lower() != q_lower]

    # 合併去重，只取4碼純數字股票（排除ETF代號過長）
    seen = set()
    for s in exact + prefix_id + name_match:
        sid = str(s.get("stock_id",""))
        if sid in seen:
            continue
        if not sid.isdigit() or len(sid) not in (4, 5, 6):
            continue
        seen.add(sid)
        results.append({
            "stock_id":   sid,
            "stock_name": s.get("stock_name",""),
            "type":       s.get("type",""),
        })
        if len(results) >= limit:
            break

    # fallback：若 FinMind 沒資料，用靜態對照表
    if not results:
        for name, sid in static_map.items():
            if q in name or q in sid:
                results.append({"stock_id": sid, "stock_name": name, "type": ""})
        results = results[:limit]

    return {"query": q, "results": results}


@app.get("/api/peers/{stock_id}")
def get_peers(stock_id: str, limit: int = 15):
    """同產業個股列表"""
    code = stock_id.strip().replace(".TW", "").replace(".TWO", "")
    all_stocks = get_all_stock_info()
    if not all_stocks:
        raise HTTPException(status_code=503, detail="FinMind 資料暫時無法取得")

    # 找自己的產業
    this = next((s for s in all_stocks if s.get("stock_id") == code), None)
    if not this or not this.get("industry_category"):
        raise HTTPException(status_code=404, detail=f"找不到 {code} 的產業資料")

    industry = this["industry_category"]

    # 同產業（排除自己，只取4碼純數字股票，避免ETF/權證）
    peers = [
        {"stock_id": s["stock_id"], "stock_name": s.get("stock_name", ""),
         "type": s.get("type", "")}
        for s in all_stocks
        if s.get("industry_category") == industry
        and s.get("stock_id") != code
        and str(s.get("stock_id", "")).isdigit()
        and len(str(s.get("stock_id", ""))) == 4
    ][:limit]

    return {
        "stock_id": code,
        "industry": industry,
        "peers": peers,
        "count": len(peers),
    }


@app.get("/api/concept/{stock_id}")
def get_concept(stock_id: str):
    """所屬產業鏈 / 概念股"""
    import urllib.request, json as _json
    code = stock_id.strip().replace(".TW", "").replace(".TWO", "")
    try:
        url = (f"https://api.finmindtrade.com/api/v4/data"
               f"?dataset=TaiwanStockIndustryChain"
               f"&data_id={code}&token={FINMIND_TOKEN}")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = _json.loads(resp.read())
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"FinMind 連線失敗：{e}")

    if data.get("status") != 200:
        raise HTTPException(status_code=404, detail="查無產業鏈資料")

    raw = data.get("data", [])
    if not raw:
        return {"stock_id": code, "chains": [], "count": 0}

    # 整理：依 industry_chain_name 分組
    from collections import defaultdict
    groups: dict = defaultdict(list)
    for item in raw:
        chain = item.get("industry_chain_name") or "其他"
        sid   = item.get("stock_id2") or item.get("related_stock_id", "")
        sname = item.get("stock_name2") or item.get("related_stock_name", "")
        if sid and sid != code:
            groups[chain].append({"stock_id": sid, "stock_name": sname})

    chains = [{"chain_name": k, "stocks": v} for k, v in groups.items()]
    return {
        "stock_id": code,
        "chains": chains,
        "count": sum(len(c["stocks"]) for c in chains),
    }


def detect_kbar_pattern(opens, highs, lows, closes):
    """
    辨識最近 K 棒型態（單根/兩根/三根）
    回傳：
      kbar_pattern: str  已確認的型態名稱（空字串=無）
      kbar_warning: str  預警文字（明天若...將形成...）
    """
    n = len(closes)
    if n < 3:
        return "", ""

    o1,h1,l1,c1 = opens[-1],highs[-1],lows[-1],closes[-1]  # 最新根
    o2,h2,l2,c2 = opens[-2],highs[-2],lows[-2],closes[-2]  # 前一根
    o3,h3,l3,c3 = opens[-3],highs[-3],lows[-3],closes[-3]  # 前兩根

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

    # ── 單根型態（最新K棒）──

    # 錘頭（底部，下引線長，出現在下跌後）
    if (lower_shadow1 >= body1 * 2 and upper_shadow1 <= body1 * 0.3
            and body1 / range1 < 0.4):
        if not is_red1:
            patterns.append("錘頭線（底部反轉訊號）")
            warnings.append("出現錘頭線，若明天收紅確認，底部支撐訊號成立")
        else:
            patterns.append("錘頭線（底部反轉，紅K更佳）")
            warnings.append("出現紅K錘頭線，底部支撐訊號，明天若繼續收紅則確認")

    # 流星/射擊之星（頂部，上引線長）
    elif (upper_shadow1 >= body1 * 2 and lower_shadow1 <= body1 * 0.3
            and body1 / range1 < 0.4):
        patterns.append("射擊之星（頂部壓力訊號）")
        warnings.append("出現射擊之星，若明天收黑確認，注意頂部形成風險")

    # 十字星（開收盤接近）
    elif body1 / range1 < 0.1 and range1 > 0:
        if h1 > max(h2, h3):  # 高點在頂部
            patterns.append("十字星（高點出現，方向未定）")
            warnings.append("高點出現十字星，方向未明，明天若收黑須注意拉回")
        else:
            patterns.append("十字星（整理，等待方向）")
            warnings.append("出現十字星，整理中，等待明天方向確認")

    # 大紅棒（強攻）
    elif is_red1 and body1 / range1 > 0.7 and body1 > body2 * 1.5:
        patterns.append("大紅棒（強勢攻擊）")
        warnings.append("出現大紅棒，若明天不跌破今日一半，多頭強勢延續")

    # 大黑棒（強殺）
    elif not is_red1 and body1 / range1 > 0.7 and body1 > body2 * 1.5:
        patterns.append("大黑棒（強勢賣壓）")
        warnings.append("出現大黑棒，若明天無法收復今日一半，空頭延續")

    # ── 兩根型態 ──

    # 多頭吞噬（紅吞黑）
    if (is_red1 and not is_red2
            and o1 <= c2 and c1 >= o2
            and body1 > body2):
        patterns.append("多頭吞噬（底部反轉）")
        warnings.append("出現多頭吞噬，明天若繼續收紅，底部反轉確認")

    # 空頭吞噬（黑吞紅）
    elif (not is_red1 and is_red2
            and o1 >= c2 and c1 <= o2
            and body1 > body2):
        patterns.append("空頭吞噬（頂部反轉）")
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
    bullish_keys = ["錘頭","多頭吞噬","早晨之星","三紅兵","穿刺線","大紅棒","頭肩底","W底"]
    bearish_keys = ["射擊之星","空頭吞噬","黃昏之星","三烏鴉","烏雲蓋頂","大黑棒","頭肩頂","M頭"]
    kbar_dir = "bullish" if any(k in pattern_str for k in bullish_keys) \
               else "bearish" if any(k in pattern_str for k in bearish_keys) \
               else "neutral"

    return pattern_str, warning_str, kbar_dir


# ══════════════════════════════════════════════════════════
# 籌碼面 API
# ══════════════════════════════════════════════════════════
def _finmind_get(dataset: str, stock_id: str, start_date: str, end_date: str) -> list:
    """通用 FinMind 查詢"""
    import urllib.request, json as _json
    url = (f"https://api.finmindtrade.com/api/v4/data"
           f"?dataset={dataset}&data_id={stock_id}"
           f"&start_date={start_date}&end_date={end_date}"
           f"&token={FINMIND_TOKEN}")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = _json.loads(resp.read())
    if data.get("status") != 200:
        return []
    return data.get("data", [])


@app.get("/api/chips/{stock_id}")
def get_chips(stock_id: str, days: int = 30):
    """
    籌碼面：三大法人買賣超 + 融資融券
    回傳最近 N 天資料 + 統計摘要
    """
    from datetime import date, timedelta
    code = stock_id.strip().replace(".TW", "").replace(".TWO", "")
    end   = date.today().strftime("%Y-%m-%d")
    start = (date.today() - timedelta(days=days + 10)).strftime("%Y-%m-%d")

    result = {}

    # ── 1. 三大法人 ──
    try:
        rows = _finmind_get("TaiwanStockInstitutionalInvestorsBuySell", code, start, end)
        if rows:
            # 整理成 {date: {外資,投信,自營}} 格式
            daily: dict = {}
            for r in rows:
                d = r.get("date","")[:10]
                name = r.get("name","")
                net = r.get("buy", 0) - r.get("sell", 0)
                if d not in daily:
                    daily[d] = {"foreign": 0, "invest": 0, "dealer": 0}
                name_lower = name.replace(" ","")
                if "外資" in name_lower or "Foreign" in name or "QFII" in name:
                    daily[d]["foreign"] += net
                elif "投信" in name_lower or "Investment" in name:
                    daily[d]["invest"] += net
                elif "自營" in name_lower or "Dealer" in name:
                    daily[d]["dealer"] += net

            sorted_days = sorted(daily.keys())[-days:]
            inst_list = []
            for d in sorted_days:
                v = daily[d]
                total = v["foreign"] + v["invest"] + v["dealer"]
                inst_list.append({
                    "date": d,
                    "foreign": v["foreign"],
                    "invest":  v["invest"],
                    "dealer":  v["dealer"],
                    "total":   total,
                })

            # 統計摘要（近5日、近20日）
            def summarize(lst, n):
                sub = lst[-n:]
                f = sum(r["foreign"] for r in sub)
                i = sum(r["invest"]  for r in sub)
                de= sum(r["dealer"]  for r in sub)
                return {"foreign": f, "invest": i, "dealer": de, "total": f+i+de, "days": len(sub)}

            result["institutional"] = {
                "daily":   inst_list,
                "summary_5":  summarize(inst_list, 5),
                "summary_20": summarize(inst_list, 20),
            }
    except Exception as e:
        result["institutional"] = {"error": str(e)}

    # ── 2. 融資融券 ──
    try:
        rows = _finmind_get("TaiwanStockMarginPurchaseShortSale", code, start, end)
        if rows:
            margin_list = []
            for r in sorted(rows, key=lambda x: x.get("date",""))[-days:]:
                # FinMind 欄位名稱可能有大小寫差異，使用 fallback 容錯
                def _get(row, *keys, default=0):
                    for k in keys:
                        v = row.get(k)
                        if v is not None:
                            return v
                    return default

                # 融資餘額、融券餘額
                margin_list.append({
                    "date":        r.get("date","")[:10],
                    "margin_buy":  _get(r,"MarginPurchaseBuy","margin_purchase_buy"),
                    "margin_sell": _get(r,"MarginPurchaseSell","margin_purchase_sell"),
                    "margin_bal":  _get(r,"MarginPurchaseTodayBalance","margin_purchase_today_balance","MarginPurchaseBalance"),
                    "short_buy":   _get(r,"ShortSaleBuy","short_sale_buy"),
                    "short_sell":  _get(r,"ShortSaleSell","short_sale_sell"),
                    "short_bal":   _get(r,"ShortSaleTodayBalance","short_sale_today_balance","ShortSaleBalance"),
                    "offset":      _get(r,"OffsetLoanAndShort","offset_loan_and_short"),
                })

            # 近5日融資增減
            if len(margin_list) >= 2:
                recent = margin_list[-5:]
                margin_chg = margin_list[-1]["margin_bal"] - margin_list[-min(6,len(margin_list))]["margin_bal"]
                short_chg  = margin_list[-1]["short_bal"]  - margin_list[-min(6,len(margin_list))]["short_bal"]
            else:
                margin_chg = short_chg = 0

            result["margin"] = {
                "daily":       margin_list,
                "margin_latest": margin_list[-1]["margin_bal"] if margin_list else 0,
                "short_latest":  margin_list[-1]["short_bal"]  if margin_list else 0,
                "margin_chg_5":  margin_chg,
                "short_chg_5":   short_chg,
                "_raw_fields":   list(rows[0].keys()) if rows else [],  # debug 用：顯示實際欄位名稱
            }
    except Exception as e:
        result["margin"] = {"error": str(e)}

    result["stock_id"] = code
    result["query_days"] = days
    return result


