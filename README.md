# 線上有位 — 台股技術分析輔助系統

> 輸入台股代號，自動畫出支撐、壓力、均線、型態與損益比。

---

## 快速啟動

### 1. 安裝後端依賴

```bash
cd backend
pip install -r requirements.txt
```

### 2. 啟動 API 伺服器

```bash
uvicorn main:app --reload --port 8000
```

成功後會看到：
```
✅ 線上有位 API 啟動中...
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 3. 開啟前端

用瀏覽器直接開啟 `frontend/index.html`（雙擊即可）。

或用 VS Code 的 Live Server 插件開啟。

---

## API 端點

### 健康檢查
```
GET http://localhost:8000/
```

### K 線資料
```
GET http://localhost:8000/api/kline/{stock_id}?tf=D
```

參數：
- `tf`: `D`=日K(3年) / `W`=週K(5年) / `M`=月K(10年)

範例：
```
http://localhost:8000/api/kline/2330?tf=D
http://localhost:8000/api/kline/3260?tf=W   ← 上櫃加 .TWO 或直接打代號
```

### 完整技術分析
```
GET http://localhost:8000/api/analyze/{stock_id}?tf=D&ma1=5&ma2=10&ma3=20&ma4=60&ma5=120
```

參數：
- `tf`: D / W / M
- `ma1~ma5`: 自訂均線天數（預設 5/10/20/60/120）

回傳範例：
```json
{
  "symbol": "2330.TW",
  "price": 850.0,
  "support": 810.0,
  "resistance": 880.0,
  "upper_channel": 895.0,
  "lower_channel": 805.0,
  "trend": "上升趨勢",
  "pattern": "壓力整理",
  "pattern_sub": "靠近壓力，注意量能",
  "stop_loss": 793.8,
  "target1": 880.0,
  "target2": 968.0,
  "risk_reward": 0.52,
  "warning": "接近軌道上緣，不建議追價",
  "near_top": true,
  "near_bot": false,
  "ma_values": { "ma5": 855.2, "ma10": 848.1, "ma20": 835.0, "ma60": 810.5 },
  "buy_signals": [120, 180, 230],
  "sell_signals": [145, 200, 240],
  "bars": [ ... ]
}
```

---

## 支援股票

| 市場 | 代號格式 | 範例 |
|------|----------|------|
| 台灣上市 | 4碼數字 | 2330, 2317, 2454 |
| 台灣上市（完整） | 代號.TW | 2330.TW |
| 台灣上櫃 | 代號.TWO | 3260.TWO |

> 系統會自動先試 `.TW`，失敗再試 `.TWO`

---

## 技術架構

```
backend/
├── main.py           ← FastAPI 後端主程式
└── requirements.txt  ← Python 依賴

frontend/
└── index.html        ← 單頁前端（含 Chart.js）
```

### 後端技術
- **FastAPI** — API 框架
- **yfinance** — Yahoo Finance 資料抓取（盤後更新）
- **pandas / numpy** — 資料處理
- **scipy** — 局部高低點偵測（argrelextrema）

### 前端技術
- 純 HTML + CSS + JS（無框架依賴）
- **Chart.js 4.4** — K 線圖表

---

## 功能說明

### 均線系統
- 預設：MA5、MA10、MA20、MA60、MA120（可關閉）
- 可自訂任意天數（1~250日）
- 趨勢判斷：短均線 > 長均線 = 上升趨勢

### 支撐壓力
- 使用 `scipy.signal.argrelextrema` 找局部高低點
- 備援：若抓不到，使用近 20 日最高/最低

### 葛蘭碧買賣點
- 買點：股價由下往上突破 MA20
- 賣點：股價由上往下跌破 MA20
- 圖表顯示最近 3 個訊號

### 型態偵測（前端）
- 三角收斂、壓力突破、支撐跌破
- 雙頂（M頭）、雙底（W底）
- 上升旗型、下降旗型

### 損益比計算
- 停損：支撐 × 0.98
- 目標1：壓力
- 目標2：壓力 × 1.10
- 損益比 = (目標1 - 現價) / (現價 - 停損)

---

## 免責聲明

本系統僅提供技術分析輔助與風險評估，不構成任何投資建議、買賣建議或獲利保證。
投資有風險，使用者應自行判斷並承擔交易結果。
資料來源：Yahoo Finance，盤後更新，可能有延遲。
