# SoftGlow 產品 Freemium 資訊架構（交接）

> 路徑：`/workspace/product-freemium/`  
> 更新：2026-09-21（Asia/Taipei）

## 三層模型（使用者已確認）

| 層級 | 使用者得到什麼 |
|------|----------------|
| **會員（免費檢測）** | 必須先成為會員才能跑掃描／示範檢測。可見：四支柱、問題群組、影響、建議、證據；AI 誠實「尚未測量」。可見「誰來解決」三角色**摘要**。 |
| **付費（完整解法）** | **怎麼做**：完整逐步解法 + 草稿 + 修復後再測。**誰來解決**：DIY 完整清單、可匯出團隊交接、代做服務 CTA。AI 真實觀測屬付費（證據未接前仍「尚未測量」）。 |
| **看廣告** | 僅解鎖**一小部份**：每個問題群組最多解鎖解法／DIY 的**第 1 步**（badge「廣告解鎖・僅 1 步」），**不是**完整 playbook。 |

硬性約束：

- 示範狀態僅本工作階段（`state.member` / `state.paid` / `state.adUnlocks`）。
- **無真實金流、無真實廣告網路、不呼叫 OpenAI**。
- 不發明 GEO／AI 分數；會員免費版不測 AI、不造假分。
- 舊的「預覽解法」整本解鎖已移除；完整解法只靠付費（或廣告僅 1 步）。

## How + Who（每個問題群組）

每個群組解法區同時呈現：

1. **怎麼做（How）** — `paidSteps` + draft + verify  
2. **誰來解決（Who）** — 三角色：
   - **我自己做（DIY）** — `who.diySummary`（會員可見摘要）／`who.diySteps`（付費完整；廣告僅第 1 步）
   - **交給我的團隊** — `who.teamHandoff`（付費可複製／匯出交接）
   - **請你們代做** — `who.conciergeCta`（付費服務 CTA，示範按鈕、無下單）

## 狀態（`js/app.js`）

```
state.member = false;   // 免費會員（可檢測）
state.paid = false;     // 付費（完整解法）
state.adUnlocks = {};   // id -> 廣告解鎖步數（通常 0 或 1）
```

## Landing 門檻

- 非會員點「幫我看看」或示範 chips → glass modal：`免費檢測需先成為會員`
- 「以會員身分繼續（示範）」→ `member=true` 並繼續掃描
- 「先看看介紹」→ 關閉，不掃描

## Topbar／Landing plan chips

- 未登入／非會員 · 會員（免費檢測）· 付費（完整解法）
- 短句：會員可免費測；付費看完整解法；看廣告可解鎖一小部份
- 「示範升級付費」→ `paid=true`（session）

## 檔案

- `js/app.js` — 會員門檻、`SOLUTION_PLAYBOOKS`（含 `who`）、paywall How+Who、廣告 1 步、AI 付費文案
- `css/styles.css` — `.gate-modal`、`.plan-bar`、`.who-section`、`.ad-unlock-partial`
- `index.html` — 結構沿用（plan bar／modal 由 JS 注入）
- `data/` — 示範 JSON

## 群組 playbook key

`meta_bundle` · `content_similar` · `url_uncertain` · `i18n` · `links_opportunity` · `other`
