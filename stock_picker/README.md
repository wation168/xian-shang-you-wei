# 半自動選股名單生成器

## 流程

```
鉅亨 RSS（100則新聞）
       ↓ 萃取股票代號
       ↓ 必要條件：出現題材新聞 ← 沒新聞直接跳過，省 API 呼叫
FinMind 股價 + 法人資料
       ↓ 數值篩選（三條件全過）
  1. 有題材新聞（鉅亨出現過）
  2. 法人連續買超 ≥ 3 日
  3. 量能放大：近5日均量 ≥ 20日均量的 1.2x
       ↓
Claude API 評分（0~100）+ 說明
       ↓
output/stock_picks_YYYYMMDD_HHMM.html
output/latest.html（固定連結）
```

## 快速啟動

```bash
cd stock_picker

set FINMIND_TOKEN=你的Token
set ANTHROPIC_API_KEY=你的APIKey

# 手動執行一次
python main_picker.py

# 排程模式：每日 14:35 自動跑（常駐）
python main_picker.py --schedule

# 立刻跑一次排程（測試用）
python scheduler.py --now
```

## 檔案說明

| 檔案 | 說明 |
|---|---|
| `crawler.py` | 鉅亨 RSS 爬蟲 + FinMind 股價/法人資料 |
| `finmind_filter.py` | 數值篩選（題材+法人+量能） |
| `generator.py` | Claude API 評分 + HTML 卡片頁產出 |
| `main_picker.py` | 一鍵執行主程式 |
| `scheduler.py` | 每日 14:35 自動執行排程器 |
| `output/latest.html` | 最新選股頁面（固定路徑） |
| `logs/picker.log` | 執行 log |

## 調整篩選參數

編輯 `finmind_filter.py` 的 `CFG`：

```python
CFG = {
    "require_news": True,              # 必須有鉅亨題材新聞
    "min_consecutive_buy_days": 3,     # 法人連買天數
    "min_vol_ratio": 1.2,              # 量能放大倍數
    "min_avg_volume": 300,             # 最低均量（張）
    "min_price": 10.0,                 # 最低股價
}
```

## Windows 開機自動啟動

1. 建立 `run_scheduler.bat`：
```bat
cd /d D:\xian-shang-you-wei\stock_picker
set FINMIND_TOKEN=你的Token
set ANTHROPIC_API_KEY=你的APIKey
python main_picker.py --schedule
```
2. 按 Win+R → `shell:startup` → 把 .bat 捷徑放進去

## 整合到線上有位（付費會員頁面）

後端加一個端點，讀取 `latest.html` 回傳給付費會員：

```python
@app.get("/api/picks/latest")
def get_latest_picks(token: str = ""):  # 之後加會員驗證
    path = "stock_picker/output/latest.html"
    if not os.path.exists(path):
        raise HTTPException(404, "尚無選股名單")
    with open(path, encoding="utf-8") as f:
        return Response(content=f.read(), media_type="text/html")
```

## 預估成本

- FinMind：每次約 40~60 requests（免費 300/hr 足夠）
- Claude API：每檔約 500 tokens，20檔約 $0.02/次
- 每日自動執行成本極低
