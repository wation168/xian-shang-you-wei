# SoftGlow Website Intelligence — Product UI（即時掃描）

貼上網址，對**同網域**頁面做即時爬取＋網站可見度健檢。示範按鈕仍使用內建 JSON。

## 啟動（Windows）

```cmd
cd /d D:\xian-shang-you-wei\scripts\seo-scanner\v2\product
..\.venv\Scripts\python.exe server.py
```

瀏覽器開啟：<http://127.0.0.1:8765/>

可選參數：

```cmd
..\.venv\Scripts\python.exe server.py --bind 127.0.0.1 --port 8765
```

## 怎麼用

1. **真實掃描**：在輸入框貼上 `https://你的網域.com`，按「幫我看看這個網站」。
   - 伺服器同網域 BFS 爬取 HTML（預設最多 **40** 頁，硬上限 **60**）。
   - 成功後儀表板標籤顯示「**真實掃描**」。
   - **不會**靜默改走示範 JSON；伺服器未啟動會明確提示執行 `server.py`。
2. **示範資料**：點下方示範 chips，載入 `./data/*.json`，標籤為「**示範資料**」。不打 `/api/scan`。

## API

| 方法 | 路徑 | 說明 |
|------|------|------|
| GET | `/api/health` | `{"ok": true, "mode": "live"}` |
| POST | `/api/scan` | Body：`{"url":"...","max_pages":40}`（可選，上限 60）→ 產品 JSON |

一次只能跑一筆掃描；忙碌時回 **429**。抓不到頁面回 **422**（繁中錯誤訊息）。

## 部署檔案（複製到 v2）

```
v2/
  seo_scanner/live_crawl.py          ← 新增
  seo_scanner/product_payload.py     ← 新增
  product/server.py                  ← 新增
  product/js/app.js                  ← 覆蓋（接 API）
  product/README.md                  ← 覆蓋
  product/index.html / css / data…   ← 既有 UI（視覺不變）
```

`server.py` 會把 `Path(__file__).resolve().parent.parent`（v2）加入 `sys.path`。

## 限制

- 只抓靜態 HTML；重度 SPA／需登入／驗證碼的站可能抓不到內容。
- 同網域（`www` 與裸域視為同一主機）；不跟外站。
- 頁數預設 40、上限 60。
- 略過 pdf／圖片／css／js／zip 等。
- 診斷以 `http_live=False`（缺頁連結先當證據不足，不直接宣判 404）。
- **不會**顯示假的 AI／GEO 分數（UI 維持「尚未測量」）。
