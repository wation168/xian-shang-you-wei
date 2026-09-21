# SoftGlow 本機 SEO Scanner v2

發現問題 → 判斷原因 → 建議怎麼修 → 排出優先順序。

只掃**本機靜態 HTML**，不連網、不做 SaaS／付費閘門。專為 SoftGlow 大量 programmatic SEO 頁（lottery / tools / patterns / glossary）設計。

## 動機

人工一頁頁查 title、重複內容、hreflang、內部連結太慢。  
本工具批次掃描部署用的靜態檔（與 Google 看到的內容一致），輸出單一深色 HTML dashboard。

**重要觀念：高 raw 相似度 ≠ 自動等於 SEO 有問題。**  
合理的「模板 + 變數填充」會被標成 `shared_template_ok`（低優先／資訊性）；真套殼才升到 P0/P1。

## 與 Claude 版（sg_seo_parse / sg_seo_analyze）的差異

| 項目 | Claude 版 | 本 v2 |
|------|-----------|--------|
| 位置 | 他處腳本（兩段式 parse→analyze） | `D:\xian-shang-you-wei\scripts\seo-scanner\v2\\` 模組化套件 |
| 入口 | 兩個 py | 單一 `run_scan.py` |
| Issue 模型 | 偏分析結果 | 固定 problem / cause / fix / priority / evidence |
| hreflang | 偏 lottery 的 zh-Hant-TW | **雙對照**：同時支援 zh-Hant-TW（lottery）與 zh-TW（tools/patterns/glossary） |
| 版型 | 實務上兩種為主 | 自動偵測 article→card→main 後備，含 glossary |
| 依賴 | 類似 | beautifulsoup4、scikit-learn、numpy |

**不要改、不要覆蓋 Claude 版檔案。** 本專案為全新實作。

## 安裝

```bat
cd /d D:\xian-shang-you-wei\scripts\seo-scanner\v2
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Linux / macOS：

```bash
cd D:/xian-shang-you-wei/scripts/seo-scanner/v2
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 怎麼跑

```bat
python run_scan.py --root "D:/xian-shang-you-wei/backend/frontend/lottery" --site-name "樂透站" --out dashboard_lottery.html
```

只掃某一語言（加速）：

```bat
python run_scan.py --root "D:/.../tools" --lang zh-TW --site-name "323工具" --out dashboard_tools.html
```

可選 GSC CSV（欄位含 Page/網頁 與 Impressions/曝光）：

```bat
python run_scan.py --root "D:/.../lottery" --gsc-csv gsc_export.csv --out dashboard.html
```

終端機會印：頁數、P0–P3 計數、耗時。用瀏覽器開啟產出的 HTML（支援 `file://`）。

### Windows 對 lottery 的完整指令範例

```bat
cd /d D:\seo-scanner-v2
.venv\Scripts\activate
python run_scan.py --root "D:/xian-shang-you-wei/backend/frontend/lottery" --site-name "樂透站" --out dashboard_lottery.html
```

路徑用正斜線 `/` 或雙反斜線 `\\` 皆可。

## 目錄結構

```
seo-scanner-v2/
  README.md
  requirements.txt
  run_scan.py
  seo_scanner/
    models.py        # Page, Issue
    parse.py         # 掃描擷取（多版型 + 雙 hreflang 對照）
    normalize.py     # 變數正規化、遊戲家族
    similarity.py    # raw/norm 相似度與分類
    checks_meta.py   # title/meta/h1/canonical/薄內容
    checks_links.py  # 內部連結建議
    checks_i18n.py   # hreflang 缺漏與互指
    diagnose.py      # 彙整
    report.py        # 自包含 HTML dashboard
  fixtures/          # 假資料
  tests/test_similarity.py
```

## 相似度分類規則（門檻最終值）

對**同語言**頁面：

1. **raw cosine**（TF-IDF `char_wb` ngram 3–5）≥ **0.90** → 進候選  
2. 正文正規化後再算 **norm_sim**：數字、百分比、日期、貨幣、號碼序列、title/h1/slug 推得的遊戲名、過長專有詞 → 佔位符  
3. slug 後綴屬同一遊戲（overview / history / results / statistics / number-generator…）→ `same_game_family`  

| 分類 | 條件（摘要） | 優先序 |
|------|----------------|--------|
| `template_shell` | norm ≥ **0.97**，且非同遊戲家族 | P0（norm≥0.99）／P1 |
| `near_duplicate` | norm ≥ **0.93** | P1（邊界可 P2） |
| `shared_template_ok` | raw≥0.90 且 (raw−norm) ≥ **0.05** | P3（資訊） |
| `same_game_family` | slug 家族判定 | P3（可摺疊） |

常數定義於 `seo_scanner/similarity.py`：`RAW_CANDIDATE`、`NORM_SHELL`、`NORM_NEAR_DUP`、`DROP_OK`。

## 其他檢查

- title / meta：缺漏、過短／過長、同語言完全重複  
- H1：缺或多個  
- canonical：缺或可能非自我指向  
- 薄內容：正文 &lt; 200 字元  
- hreflang：以同 slug **實際存在的語言**為預期集合 + x-default；鍵名相容 lottery（zh-Hant-TW）與 tools（zh-TW）；互指檢查  
- 內部連結：主題相似建議互連；**跳過** template_shell / near_duplicate 配對；只報尚未連結者  

## 人工審核注意（數字風險）

- fix 欄位是**草稿方向**，不是可直接上線文案。  
- **不要**把工具建議裡的獎金、賠率、中獎率數字未經核對就貼上正式頁。  
- fixtures／範例中的金額僅供分類測試。  
- GSC 零曝光僅作優先序參考，需結合實際 Search Console 判讀。  

## 驗證

```bash
source .venv/bin/activate   # Windows: .venv\Scripts\activate
python tests/test_similarity.py
python run_scan.py --root fixtures --site-name "Fixture" --out /tmp/dash_fix.html
```

## 已知限制

- 不抓 JS 動態渲染內容；只看靜態 HTML。  
- 正文擷取依 CSS 慣例啟發式，極端自訂版型可能偏短（會進薄內容，可回報改進）。  
- canonical／hreflang 自我指向為路徑粗判，CDN／別名網域需人工確認。  
- 內部連結只掃 sidebar / subnav / more-tools / related-card / nav，正文中的零星連結可能漏計。  
- 相似度兩兩比對，頁數極大時記憶體與時間上升；可用 `--lang` 分段掃。  
- 不做線上爬蟲、不提交索引、不自動改檔。  
