# 國中會考PDF拆題原型 — 交接說明（2026/08/02）

你出門的時候我把技術原型做完並實測跑通了，用的是你上傳的111年5份PDF
（國文、自然、社會、數學、參考答案）。結果如下。

## 做了什麼

1. **`parse_answers.py`**：解析參考答案PDF（表格格式）。
   這份很乾淨，用 `pdfplumber` 的表格抽取功能，**6科全部100%正確對應**
   （國文42題、自然50題、社會54題、數學25題、英語閱讀43題、英語聽力21題）。

2. **`parse_exam.py`**：解析單科試題PDF，抓出「題號＋題幹＋(A)(B)(C)(D)選項」。
   這份是文字段落，格式沒有表格那麼工整，用正則表達式切分，
   **第一版就抓到全部題號**（國文42/42、自然50/50、社會54/54、數學25/25），
   但選項完整抽出的比例沒有100%——原因見下方「限制」。

3. **`merged_questions_with_answers.json`**：把題目＋正確答案合併成一份，
   這是最終可以用來寫進資料庫的格式，範例：
   ```json
   {
     "question_number": 1,
     "question_text": "這張圖最可能在傳達下列何種訊息？",
     "options": [{"key":"A","text":"..."}, ...],
     "correct_option": "D",
     "needs_visual_asset": false
   }
   ```

## 統計結果（111年四科選擇題）

| 科目 | 總題數 | 選項完整抽出 | 需要圖表才能作答 | 答案已對上 |
|---|---:|---:|---:|---:|
| 國文 | 42 | 40 | 0 | 42/42 |
| 自然 | 50 | 46 | 29 | 50/50 |
| 社會 | 54 | 47 | 33 | 54/54 |
| 數學 | 25 | 21 | 14 | 25/25 |

## 限制（這是原型必然會遇到的，不是bug）

1. **「需要圖表才能作答」的題目沒辦法只靠純文字解決。**
   例如社會科36題、自然科38題這種題目，連「選項本身」都是圖片
   （不是題幹配圖，是A/B/C/D四個選項各自是一張圖），這種純文字解析
   永遠抓不到選項內容，只能：
   - 人工把圖片另外裁切存成圖片檔，用 `questions.image_url` 欄位放整題圖，
     或
   - 乾脆放棄純選擇題形式，改成這幾題另外標記為「暫緩收錄」
   自然/社會這兩科比例偏高（自然58%、社會61%題目有圖表），是這兩科考題
   本身圖表多，不是拆題邏輯抓得不夠仔細。

2. **少數題目選項抽出不完整（國文2題、數學4題）**，這批不是圖表題，
   是文字排版問題（例如選項裡本身有括號、或跨欄排版被pdfplumber讀亂），
   需要另外寫規則修或直接人工校對，比例不高（國文95%、數學84%），
   可以之後補強regex，不影響先跑通其他80-90%的題目。

3. **英文閱讀科這次沒有寫解析器**——你上傳的 `111_英語_閱讀.pdf` 排版
   跟中文科目差異較大（有題組、超連結格式的閱讀素材），需要另外設計，
   這次先集中把中文四科的技術路徑跑通。

## 一個重要的架構問題，需要你決定

`schema.sql` 裡的 `questions` 表設計是**綁著 `curriculum_id`**（哪個年級/
學期/版本/第幾課），但**會考題目不是照課次出的**，是綜合性測驗，沒有
「這題屬於哪一課」這回事。

所以會考題庫不適合直接塞進現有的 `questions` 表，我建議另外開兩張表：

```sql
create table exam_papers (
  id uuid primary key default gen_random_uuid(),
  year smallint not null,           -- 111, 112...
  subject text not null,            -- 國文/英語/數學/社會/自然
  source text not null default '教育部國民及學前教育署',
  created_at timestamptz not null default now()
);

create table exam_questions (
  id uuid primary key default gen_random_uuid(),
  exam_paper_id uuid not null references exam_papers(id) on delete cascade,
  question_number smallint not null,
  question_text text not null,
  image_url text,              -- 題幹或選項需要圖片時使用
  options jsonb not null,      -- [{"key":"A","text":"..."}]
  correct_option text not null,
  needs_visual_asset boolean not null default false,  -- 標記還缺圖片的題目
  created_at timestamptz not null default now()
);
```

跟既有 `questions`/`answer_keys`（課本生字用）分開，兩套題庫各司其職，
之後前端「國中會考題庫」跟「課本隨堂練習」可以是兩個不同入口，但都用
同一個 `exam_sessions`/`attempts` 記錄作答，不用改動那兩張表。

**這個schema異動需要你確認要不要照這樣加**，我沒有動你原本的
`schema.sql`，這份新表的SQL先放在這份說明裡，等你確認後我再正式寫成
migration檔案。

## 下次對話開始建議先做的事

1. 你看一下 `merged_questions_with_answers.json`，抽幾題核對正確性
   （尤其確認「需要圖表」判斷得準不準，有沒有漏標或多標的）
2. 確認上面的 `exam_papers`/`exam_questions` 表設計要不要採用
3. 決定：**先把其餘111年的英語/寫作測驗也做完，還是直接把這套腳本
   套用到112-115年剩下的PDF（先求廣度）？**
4. 「需要圖表」的題目要不要人工裁圖，還是這批先跳過只做純文字題

原始腳本、拆解結果、答案JSON都在這個資料夾，之後要跑112-115年，
只要把 `parse_exam.py` 開頭 `configs` 清單裡的檔名跟max_q換掉就能重跑，
不用重寫邏輯。
