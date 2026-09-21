# SoftGlow 產品 Freemium 資訊架構（交接）

> 路徑：`/workspace/product-freemium/`  
> 更新：2026-09-21（Asia/Taipei）

## 原則（使用者已確認）

| 層級 | 使用者得到什麼 |
|------|----------------|
| **免費** | 看懂：即時／示範掃描結果、四支柱、白話問題群組、影響與短建議、證據層（第 2 層）、AI 誠實標「尚未測量」 |
| **付費（僅產品呈現／鎖定，無真實金流）** | 完整逐步解法、文案草稿提示、AI「已測量」能力（標為付費；證據未接前仍顯示尚未測量）、修復後再測 |

硬性約束：

- 不重做整套視覺（沿用現有 dark glass）。
- 不發明 GEO／AI 分數。
- 不呼叫 OpenAI；助手回答不可冒充「已測量」。

## 檔案

- `js/app.js` — `SOLUTION_PLAYBOOKS`、群組卡 paywall、AI 支柱／詳情付費文案、示範解鎖
- `css/styles.css` — `.paywall` / `.lock-badge` / `.plan-chip` 等
- `index.html` — 未改結構（僅沿用）
- `data/` — 示範 JSON（自既有 product 複製）

## 示範解鎖（無金流）

- 按鈕：`data-demo-unlock`，文案「預覽解法（產品示範）」
- 點擊後寫入 `state.demoUnlock[id]`（僅此工作階段）
- 解鎖後顯示完整 steps + draft + verify，並掛「付費功能預覽」
- 再點可收起；重新整理頁面即恢復鎖定

## 群組 playbook key

`meta_bundle` · `content_similar` · `url_uncertain` · `i18n` · `links_opportunity` · `other`

## 來源說明

本目錄工作時，box executor **沒有** `CopyToBox` 工具可用；因此以 box 上最新 SoftGlow product UI（`/workspace/scanner-live/product/`，含 live scan + AI 誠實標示）為基底實作 freemium。若需與 POS-01 `Documents\seo-scanner-gpt-mirror\product\` 位元組對齊，請由具 CopyToBox 的 agent 再覆寫一次後 diff。
