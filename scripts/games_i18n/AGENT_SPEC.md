# 遊戲多語言化：單一遊戲作業規格

你要把 SoftGlow 網站的一款既有繁中網頁小遊戲，改造成「邏輯共用一份 + 10 語言各自獨立頁面」的架構。
2048 已經做完並通過全部驗證，**它就是唯一的範本，一切照它做**。

工作目錄：`/home/claude/gi18n`（所有指令都在這個目錄下跑）

---

## 0. 動工前必讀（照順序看完再開始）

1. `shared/2048.js` — 範本：抽出來的共用邏輯長什麼樣
2. `templates/2048.body.html` 和 `templates/2048.css` — 範本：版面樣板
3. `content/g2048.py` — 範本：10 語言內容檔（**最重要，格式要完全照抄**）
4. `locales.py` — 共用外框字典（**唯讀，絕對不要改**），你要用到裡面的 `CHROME[loc]` 有哪些 key
5. `build.py` 與 `tests/verify.py` — 產生器與驗證器（**唯讀，絕對不要改**）

原始繁中遊戲檔在 `/mnt/user-data/uploads/games/{slug}.html`。

---

## 1. 你要產出的四個檔案

假設你負責的遊戲 slug 是 `snake`：

| 檔案 | 內容 |
|---|---|
| `shared/snake.js` | 遊戲全部邏輯（語言無關，**不得含任何使用者可見文字**） |
| `templates/snake.css` | 原始檔 `<head>` 裡那段 `<style>` 的內容，原樣搬過來（沒有 `<style>` 就不要建這個檔） |
| `templates/snake.body.html` | 遊戲卡片內部版面，文字換成 `{{ui.xxx}}` / `{{chrome.xxx}}` 佔位符 |
| `content/gsnake.py` | 10 語言的文字內容 |

**檔名規則**：`content/g{slug 的減號換成底線}.py`。例如
`whack-a-mole` → `content/gwhack_a_mole.py`、`reaction-time-test` → `content/greaction_time_test.py`。

---

## 2. `shared/{slug}.js` 的作法

把原始 HTML 裡「遊戲那一段 `<script>`」整段搬進來，然後：

### 2-1 文字全部改走字典
新增一個取字函式，**函式名一定要是 `g` + slug去掉減號 + `T`**（驗證器靠這個名字掃key）：

| slug | 函式名 |
|---|---|
| `snake` | `gsnakeT` |
| `whack-a-mole` | `gwhackamoleT` |
| `reaction-time-test` | `greactiontimetestT` |
| `sliding-puzzle` | `gslidingpuzzleT` |
| `halloween-spell-draw` | `ghalloweenspelldrawT` |

函式本體直接照抄 2048 的 `g2048T`（含 `{變數}` 代入與缺 key 回傳空字串的防錯），只改名字。

原本寫死的中文一律換成 `gXxxT('someKey')`；有變數的用 `gXxxT('key', { s: score })` 這種形式。

### 2-2 CONFIG 只留數字，文字移到字典
原始檔常見這種寫法：
```js
ratings: [ { max: 128, label: '剛開始暖身' }, ... ]
```
改成 CONFIG 裡只留門檻陣列（例如 `ratingThresholds: [128, 512, ...]`），
文字放進各語言字典的 `ratings: [...]` 陣列（**順序要對應**），
並提供一個 `ratingIndex(score)` 純函式回傳第幾級。照 2048 的作法做。
其他像難度名稱、怪物名稱、勝負訊息等清單型文字，一律同樣處理：
**JS 留索引/數值，文字留在字典的同名陣列**。

### 2-3 避免全域變數撞名
原始檔的頁面級 `const CONFIG` 要改名成該遊戲專屬名稱，例如 `SNAKE_CONFIG`、`CHESS_CONFIG`。
（因為現在多個檔案會在同一個全域範圍載入，叫 CONFIG 會撞。）
其他明顯太通用的頂層變數名（如 `state`、`board`、`init`）也一併加上遊戲前綴。

### 2-4 無 DOM 環境要能載入（單元測試需要）
* 操作 DOM 的 IIFE 開頭加：`if (typeof document === 'undefined') return;`
* 抓不到關鍵元素時提早 return，例如：`if (!boardEl) return;`
* **任何頂層直接呼叫 `document.` 的程式碼**（例如 FAQ 展開那段）要包在
  `if (typeof document !== 'undefined') { ... }` 裡
* 用到 `window` 的地方一律 `typeof window !== 'undefined' &&` 先判斷

### 2-5 不要搬進來的東西
* AdSense 載入那段 `<script>`（產生器會自己產）
* `gaMountAuthWidget(...)` / `gaMountLeaderboard(...)` / `gaInitFullscreenToggle()` /
  `gaInitLoginReminder(...)` 這幾行掛載呼叫（產生器會自己產）
* `<script src="/games/games-auth.js">` 等外部引用

### 2-6 邏輯本身不准改
這是純重構。**遊戲規則、演算法、數值、難度曲線一律原封不動**。
只做三件事：文字外移、變數改名、無DOM防護。
如果你發現原始碼有真正的 bug，**先不要順手改**，在最後回報裡寫出來讓主流程判斷。

---

## 3. `templates/{slug}.body.html` 的作法

取原始檔 `<div class="game-card">` 裡面的內容，但**不包含**：
* `<h1>` 與 `<p class="game-subtitle">`（產生器會自己產）
* `<div class="ga-widget">` 和 `<div class="ga-leaderboard">` 整塊（產生器會自己產）

所有中文換成佔位符：
* 這款遊戲自己的文字 → `{{ui.someKey}}`，並在內容檔的 `ui` 區塊定義
* 通用按鈕文字 → 優先用 `{{chrome.xxx}}`，可用的 key 只有這些：
  `startBtn`（▶️ 開始遊戲）、`restartBtn`（🔄 重新開始）、`playAgain`（🔄 再玩一次）、
  `shareBtn`（📤 分享成績）、`bestScore`（最佳分數）
  其餘一律走 `{{ui.xxx}}`。

縮排照 2048 的樣子（前面 4 個空格起跳）。

---

## 4. `content/g{slug}.py` 的作法

**格式完全照抄 `content/g2048.py`**，包含檔頭 `SLUG` / `EMOJI` / `HAS_LEADERBOARD` 與 `L = {...}`。

`HAS_LEADERBOARD` 的值：西洋棋 `chess` 與五子棋 `gomoku` 是 `False`（雙人對戰不上分數榜），
其餘 11 款都是 `True`。

`L` 必須包含全部 10 個語言，key 就是這 10 個字串：
`"zh-TW", "en", "de", "es", "fr", "id", "ja", "ko", "pt", "zh-CN"`

每個語言底下必須有：

| 欄位 | 說明 |
|---|---|
| `title` | `<title>`。格式：`{在地化遊戲名} - {賣點} \| SoftGlow` |
| `desc` | meta description，約 70–110 字（中日韓約 50–70 字） |
| `h1` | 頁面主標 |
| `subtitle` | 主標下面一行說明 |
| `tileDesc` | 遊戲總覽頁卡片上的一行簡述（很短） |
| `ldName` / `ldDesc` | JSON-LD 用的名稱與描述 |
| `ui` | 版面佔位符對應的文字（key 要跟 body.html 裡的 `{{ui.x}}` 完全一致） |
| `i18n` | 共用JS `gXxxT('key')` 用到的**每一個 key 都要有**，一個都不能少 |
| `articles` | 2 個區塊，每塊 2 個 `(標題, [段落])`，共 4 個 h2、4 段內文 |
| `faq` | 剛好 5 組 `(問題, 答案)` |

### 4-1 翻譯品質要求（這是這次工作的重點，不是走過場）

* **遊戲名稱一律用 `locales.py` 的 `GAME_NAMES[slug][loc]`，不要自己另外翻一個版本**，
  否則 `<h1>`、`<title>`、麵包屑、相關遊戲連結會互相對不起來。
* **關鍵字要在地化，不是逐字翻譯**。要用當地玩家真的會打進搜尋框的說法。
  例如踩地雷：西語 `Buscaminas`、法語 `Démineur`、葡語 `Campo Minado`、日語 `マインスイーパ`。
  日語的休閒遊戲頁面很常搭配 `暇つぶし ゲーム`（打發時間的遊戲）這類意圖詞，適合放進 desc。
* **文章跟 FAQ 是給搜尋引擎看的實質內容**，要照原文的資訊量重寫成該語言自然的表達，
  不要縮水成一兩句，也不要硬翻到讀起來很生硬。
* **絕對不要在非中文語言裡混進任何中日韓文字**（驗證器會擋，包含全形標點）。
  反過來，日/韓/簡中頁面也不能殘留繁體中文專用字串。
* 標點符號要跟著語言走：法語冒號前有空格（`Score : `）、西語疑問句用 `¿…?`、
  日語用全形括號與句號、簡中用簡體字。

### 4-2 `i18n` 字典的注意事項
* 變數佔位用大括號，例如 `"scoreLine": "分數：{s}"`，代入時 key 要跟 JS 呼叫端一致
* 陣列型（如 `ratings`、難度名稱）在 10 個語言的**長度必須一樣**
* emoji 保留（`💥`、`🎉` 這些跨語言通用，不要拿掉也不要換）

---

## 5. 驗證（沒過不准回報完成）

```bash
cd /home/claude/gi18n
node --check shared/{slug}.js          # 語法
python3 build.py {slug}                # 產出 10 語言
python3 tests/verify.py {slug}         # 結構驗證，必須 0 失敗
```

`verify.py` 會檢查：JSON-LD 能否解析、每段 inline script 語法、getElementById 的 id 是否存在、
div 開合配對、佔位符有沒有漏換、字典是否涵蓋共用JS所有 key、拉丁語系頁面有沒有殘留中日韓文字、
hreflang 與 canonical、html lang 屬性等。

**跑到 0 失敗為止。** 失敗訊息會直接指出是哪個語言的哪一項。

另外請自己寫一個小的純邏輯回歸測試 `tests/test_logic_{slug 底線版}.js`
（照抄 `tests/test_logic_2048.js` 的 vm 載入手法），至少涵蓋這款遊戲最核心的規則
（例如貪食蛇的碰撞判定、數獨的解答唯一性、西洋棋的走法合法性），確認重構沒有改到邏輯。
注意 vm 裡宣告的 `const` 不會外洩，要在同一次 eval 裡掛到 `globalThis` 上才能引用。
跑法：`node tests/test_logic_{底線版}.js`，也要全過。

---

## 6. 回報格式

完成後，用純文字回報（不要客套話）：
1. 你負責的每個 slug 各自的：verify 通過項數、邏輯測試通過項數
2. 抽出邏輯時遇到的特殊處理（例如某個遊戲有兩段 script、某個變數名撞名）
3. 你在原始碼裡發現但**沒有動**的可疑之處（如果有）
4. 翻譯上你刻意做的在地化決定（例如某語言的遊戲名用了當地慣用說法）
