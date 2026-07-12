# SoftGlow 全球多語言工具站｜Master Blueprint v5.0（Locked）

本文件為 SoftGlow 全球多語言工具平台最高層級規格書（Master Blueprint），作為後續開發、SEO、內容生成、部署、維護、商業化及網站出售（Website Exit）的唯一執行標準。

---

## 一、專案定位
SoftGlow 已由單一工具網站，正式轉型為以 Programmatic SEO 為核心的全球多語言 Web Application 平台。
* **核心目標：** 建立可持續成長、可規模化營運、可出售（Website Exit）的全球 SEO 數位資產。
* **最終定位：** Web Application / Programmatic SEO / AI Content Platform / Digital Asset

---

## 二、網站規模
所有系統皆以 50,000+ Pages 為設計基準。
* **第一階段：** 323 Tools × 10 Languages = 約 3,230 Pages
* **中期目標：** 500+ Tools = 約 25,000 Pages
* **長期目標：** 50,000+ SEO Pages

---

## 三、語言策略

### 資源分配矩陣
* **Tier A（70% 資源）：** English, Deutsch, 日本語（主要收入來源）
* **Tier B（20% 資源）：** Français, Español（主要流量成長市場）
* **Tier C（10% 資源）：** 繁體中文, 簡體中文, 한국어, Português, Bahasa Indonesia

### Tier C 主要任務
1. 提升 Domain Authority
2. 增加網站規模
3. 累積 Organic Traffic
4. 導流 Email List
5. 支援 Tier A Topic Cluster

### 網域架構原則
初期全部使用子目錄（如 `/tools/de/`），以集中 Domain Authority，不拆分獨立網域。待流量與各國市場成熟後，再依據數據評估是否有獨立拆分（如 `.jp` 網域）之必要。

---

## 四、SEO 技術架構
全面採用以下最佳化規格：
* **Static HTML：** 純靜態網頁，極致極速。
* **Flat URL：** zh-TW 置於 `/tools/{slug}.html` 根目錄，其餘語系置於 `/tools/{lang}/{slug}.html`。
* **Canonical Tag：** 自動防止重複內容判定。
* **hreflang：** 腳本自動生成 10 語言 + x-default 互指。
* **XML Sitemap：** 全自動化定量生成。
* **FAQSchema JSON-LD：** 每頁自動整合 5 題固定 FAQ。
* **WebApplication Schema**
* **Breadcrumb**
* **Internal Link**
* **PageSpeed & Core Web Vitals 最佳化**

### AdSense 審核期間特別防禦
* **線上完全凍結：** 審核期間絕對不動線上任何檔案與首頁設計。
* **Sitemap 分段：** 線上 Sitemap 僅提交 English + zh-TW 頁面，其餘語言先不暴露。
* **本機全面跑盤：** 所有工具生成、模板重構與 Bug 修復，一律在本機環境完成並做好快取。

---

## 五、內容品質分級 (Tiered Content)
AI Token 與人力資源應 80% 集中投入 A Tier。

### A Tier（約 50 個核心工具）
* **核心工具賽道：** Mortgage（房貸）、Loan（貸款）、Insurance（保險）、Investment（投資）、Retirement（退休）、Tax（稅務）、Credit Card（信用卡）。
* **規格：** 深度客製化內容、Pillar Guide 整合、精緻客製化 FAQ、高度關聯內鏈、滿配置聯盟行銷。

### B Tier（約 100 個熱門工具）
* **規格：** 採用完整標準 SEO 生產品質模板、大眾化 FAQ、一般數據分析。

### C Tier（其餘所有長尾工具）
* **規格：** 維持輕量化基本模板，追求最快載入速度，作為長尾流量海量入口，並將權重導流至 A、B 級頁面。

---

## 六、Topic Cluster (主題群)
建立主題金字塔閉環傳遞權重。

```
Pillar Guide (頂層指南) <──> Tool (中層工具) <──> Blog (底層文章) ──> FAQ ──> Affiliate
```

* **內鏈路由原則：** 80~90% 內鏈嚴格維持在同一 Topic 群組（Silo 結構）；10~20% 允許具備明確語意關聯的跨主題連結。

---

## 七、Pillar Guide 標準
所有 A Tier 工具對應的頂層指南（Pillar Page）必須包含以下技術組件：
* Table of Contents（TOC，自動目錄）
* Named Anchor & Jump Link（命名錨點與跳轉連結）
* 深度 FAQ 區塊
* Breadcrumb（麵包屑）
* Related Tools（相關工具推薦群）
* Related Articles（相關教學文章）

---

## 八、Localization (多語言在地化)
所有工具的數據與文字輸出必須完全符合各國當地規範，採用 Locale 輸出，嚴禁寫死格式。

### 在地化格式規範
* **en：** `$1,234,567.89` (USD) | `03 Jul 2026` | 英制/公制並存 | Sunday | 12 小時制 | `5%`
* **zh-TW：** `$1,234,567` (TWD) | `2026/07/03` | 台制/公制 | Monday | 24 小時制 | `5%`
* **zh-CN：** `￥1,234,567.89` (CNY) | `2026年7月3日` | 公制 | Monday | 24 小時制 | `5%`
* **ja：** `￥1,234,567` (JPY) | `2026年7月3日` | 日制/公制 | Monday | 24 小時制 | `5%`
* **de：** `1.234.567,89 €` (EUR) | `03.07.2026` | 公制 | Monday | 24 小時制 | `5 %`
* **fr：** `1 234 567,89 €` (EUR) | `03/07/2026` | 公制 | Monday | 24 小時制 | `5 %`
* **es：** `1.234.567,89 €` (EUR) | `03/07/2026` | 公制 | Monday | 24 小時制 | `5%`
* **pt：** `R$ 1.234.567,89` (BRL) | `03/07/2026` | 公制 | Sunday | 24 小時制 | `5%`
* **ko：** `₩1,234,567` (KRW) | `2026. 07. 03.` | 公制 | Sunday | 24 小時制 | `5%`
* **id：** `Rp 1.234.567,89` (IDR) | `03-07-2026` | 公制 | Monday | 24 小時制 | `5%`

---

## 九、多元變現
採取階梯式、多渠道變現模式：

```
AdSense ──> Affiliate ──> Ezoic ──> Email List ──> Mediavine ──> First-party Data ──> Raptive ──> LiveRamp / Lotame ──> Website Exit
```

* **目標收入比例：** 40% 廣告收益 + 40% 聯盟行銷 + 20% 第一方數據變現。

---

## 十、Affiliate (聯盟行銷策略)
AdSense 通過後立即發動。
* **核心版位佈局：** 計算結果 ──> 數據分析 ──> Affiliate 核心推薦 ──> FAQ
* **第二階段升級：** 導入 Dynamic Affiliate Parameters。根據使用者在前端輸入的「地區、金額、年齡、利率」等即時數據，動態將參數帶入 Affiliate 追蹤連結中。

---

## 十一、廣告策略與 CLS 防禦
* **營運期加載規範：** 首屏廣告立即載入；內文/Sidebar 廣告全面實施 Lazy Load；Anchor Ads 開啟自動廣告。
* **CLS 防禦規格：** 所有首屏立即載入的廣告容器，必須在 CSS/HTML 中預留固定的佔位最小高度（Min-height，如 `min-height: 250px;`），防止非同步載入推擠 DOM。

---

## 十二、安全策略
全站部署 Cloudflare。啟用：WAF、Super Bot Fight Mode、Rate Limiting、Cache Rules 與 Bot Protection。
* **簡體中文（zh-CN）區加強：** 針對該目錄實施更嚴格的 WAF 阻擋與受管理挑戰；編譯期將所有核心計算邏輯與參數直接注入並死化在 HTML 中，不暴露任何可供整庫打包的 JSON API 端點。

---

## 十三、Search Console（GSC）驅動持續優化流程
* **第一階段（每月固定）：** GSC ──> 分析 Impression、CTR、Position ──> 重新優化編譯 Title、Description、FAQ、Intro、Internal Link。
* **第二階段（全自動閉環）：** GSC 長尾提問 ──> AI 自動生成 ──> 自動插進網頁 HTML FAQ & Schema ──> 本機自動 Build ──> 部署上線。

---

## 十四、Data Source Policy (資料來源規範)
所有工具頁面必須清晰標示：Data Source（官方/權威機構公開數據優先，如 WHO, IRS, SSA, ECB）、Last Updated、Jurisdiction、Reference、Static / Dynamic。

---

## 十五、Content Version Policy (內容版本管理)
所有頁面於 HTML 原始碼底部保留 Metadata 註解，包含：Generator Version、Build Time、Model、Prompt Version。

---

## 十六、Tool Lifecycle Policy (工具生命週期)
每個工具皆具備明確的狀態管理：

```
Draft ──> Published ──> Optimized ──> Maintained ──> Archived ──> 301 Redirect
```

* **淘汰標準：** 連續 12 個月「Impression < 100、無流量、無收益」強制觸發 KPI Gate 機制，進入 Review ──> Rewrite ──> Merge ──> 301 Redirect ──> Archive 流程。

---

## 十七、AI Content Policy (AI 採集與模型解耦)
AI 內容生成採取分級動態調配策略。
* **模型路由架構：** 採用 Provider Adapter 抽象層配置（如設定 `TIER_A_PROVIDER = "anthropic"`, `TIER_A_MODEL = "sonnet"`），生成邏輯與 LLM SDK 完全解耦，不得將特定模型名稱寫死於核心生成程式碼中。

---

## 十八、Git & Build Policy (工程追蹤規範)
編譯引擎必須利用腳本自動捕獲並記錄以下變數：Git Branch、Git Commit ID、Build Time、Generator Version、Prompt Version、Translation Version、Schema Version。

---

## 十九、KPI Gate (運營監控指標)
每月嚴格審查以下維度指標：
* **SEO：** Index Rate、Crawl Rate、CTR、Average Position
* **流量：** Organic Session、Returning User、Engagement Time
* **收益：** RPM、EPC、Revenue / Tool
* **品質：** Quality Score、Content Version 更新頻率

---

## 二十、部署策略 (漸進式放量)
AdSense 審核通過後，禁止一次大量新增頁面。
* **放量配速：** 每週維持 300 ~ 600 Pages 緩步階梯式上線，同步監控 Sitemap、Crawl、Search Console 與 Quality Review。

---

## 二十一、核心執行原則
1. 品質優先於頁數。
2. A Tier 優先投入資源。
3. Search Console 驅動持續優化。
4. Topic Cluster 建立 Topical Authority。
5. Localization 優先於翻譯。
6. 收入來源必須多元。
7. 所有功能模板化、自動化、可擴充。
8. 所有頁面皆須可追蹤、可回滾、可維護。
9. 官方資料來源優先，建立網站可信度。
10. 每一頁皆視為長期資產，而非一次性內容。

---

## 二十二、Governance (專案治理宣告)
本專案之設計演進與技術規格遵循以下隔離治理原則：
* **Master Blueprint：** 本文件（唯一正式穩定規格，不記錄瑣碎變更）。
* **Architecture Decision Record (ADR)：** 記錄所有重大的底層技術與架構決策。
* **CHANGELOG：** 記錄版本變更。
* **Release Note：** 記錄每次正式部署內容。
* **修改規則：** 任何新策略不得直接修改 Master Blueprint，應先經 ADR 記錄與驗證，確認成熟後，再於新版 Master Blueprint 納入。

---

## 二十三、最終願景
打造全球化 Programmatic SEO 平台，具備高品質 Web Application、多語言 SEO 矩陣、Topic Cluster 架構、高 CPC 商業工具、完整 Localization、AI 自動生成與持續優化、多元收入來源、50,000+ Pages 可維護架構、高防禦能力、高估值 Website Exit 能力。SoftGlow 的核心不是追求最多頁數，而是建立一套可持續營運、可持續優化、可持續獲利，並具備長期出售價值的全球數位資產系統。
