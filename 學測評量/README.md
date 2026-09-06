# 學測評量系統 — 基礎架構

國小／國中線上評量網站（之後擴充高中）。這份是**基本骨架**，先跑通「選範圍 → 出題 → 即時閱卷 → 看成績」這條主線，之後再慢慢加強（簡答題答案庫擴充、成績分析報表、老師後台等）。

## 資料夾結構

```
xue-ce-assessment/
├── database/
│   └── schema.sql          資料庫建表 SQL（貼到 Supabase SQL Editor 執行）
├── backend/
│   ├── main.py              主程式（只掛路由，不寫邏輯）
│   ├── database.py          Supabase 連線
│   ├── models/               資料格式定義（依主題拆檔）
│   ├── routers/               API 路由（依功能拆檔，不會塞成一支大檔）
│   │   ├── subjects.py        學制／科目
│   │   ├── curriculum.py      課次對照
│   │   └── exam_sessions.py   開始測驗／提交答案／結束測驗
│   └── services/
│       └── grading_service.py 閱卷邏輯（獨立於資料庫存取之外）
└── frontend/
    └── quiz-selector.html   測驗設定選單介面（先前做的下拉選單版本）
```

每一支檔案只負責一件事，之後要加新功能就「新增檔案」，不要回頭把新東西塞進舊檔案裡。

## 部署步驟（照順序做）

### 1. 建立 Supabase 專案
1. 到 supabase.com 建立新專案（免費方案即可）
2. 進入專案的 SQL Editor，貼上 `database/schema.sql` 全部內容並執行
3. 到「Project Settings → API」複製 `Project URL` 和 `anon public key`

### 2. 設定後端環境變數
1. 複製 `backend/.env.example` 為 `backend/.env`
2. 填入剛剛複製的 `SUPABASE_URL`、`SUPABASE_KEY`
3. `ALLOWED_ORIGINS` 填你之後前端會用的網址（例如 `https://quiz.softglow-ai.com`）

### 3. 本機測試（可跳過，直接部署也可以）
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
打開 http://127.0.0.1:8000/health 看到 `{"status":"ok"}` 就代表正常。

### 4. 部署到 Zeabur
跟你「線上有位」專案一樣的流程：
1. 把這個資料夾推上 GitHub repo
2. Zeabur 新增服務，指向這個 repo 的 `backend/` 目錄
3. 在 Zeabur 服務設定裡加上跟 `.env` 一樣的環境變數（`SUPABASE_URL`、`SUPABASE_KEY`、`ALLOWED_ORIGINS`）
4. 部署完成後會拿到一個網址，例如 `api-quiz.softglow-ai.com`

### 5. 前端
`frontend/quiz-selector.html` 目前是純示意介面（選項是寫死的假資料）。
下一步要做的：把裡面「開始出題」按鈕改成呼叫後端 API：
- `GET /api/subjects?school_level_id=...` 取得科目
- `GET /api/curriculum?...` 取得課次
- `POST /api/exam-sessions` 開始測驗
- `GET /api/exam-sessions/{id}/questions` 取得題目
- `POST /api/exam-sessions/{id}/answers` 提交答案（即時閱卷）
- `POST /api/exam-sessions/{id}/finish` 結束測驗看成績

## 資料來源與蒐集狀況

**已完成（乾淨、可直接用）**：
- 國小 1-6 年級「國語」：407筆，來源教育百科，涵蓋南一/康軒/翰林三版本（`seed_curriculum_chinese.sql`）
- 國小「數學/生活/自然/健體/藝術/社會/綜合活動」**康軒版**：352筆，來源康軒官網XML（`seed_curriculum_math.sql` + `seed_curriculum_others.sql`）
- 國小「數學/生活/自然/健體/社會/綜合/藝術（僅六年級）」**南一版**：358筆，來源因材網API（`seed_curriculum_nani.sql`）
- 國小「數學/生活/自然/社會/綜合/藝術（三上除外）」**翰林版**：265筆，來源因材網API（`seed_curriculum_hanlin.sql`）

**目前累計約1382筆真實課次資料，國小三大版本的數學/生活/自然/綜合活動都已經三版本齊全或接近齊全。**

**國小仍不完整的部分（來源本身的限制，沒有強行湊資料）**：
- **健體、社會**：南一/翰林版部分年級的來源網站本身只有「第X單元」分隔線，沒有附上單元標題文字，這種情況沒有用猜測或學習單標題頂替，直接留空
- **英語**：三個版本都還沒有可用資料（唯一嘗試過的來源內容混亂，含自然發音/主課文/文化補充教材混雜，無法直接使用）
- **藝術**：南一版只有六年級，翰林版缺三年級上學期

**國中（7-9年級）**：完全還沒開始蒐集，是下一個大缺口

## 目前還沒做（等基礎跑通再加）

- 上面列的資料缺口要補齊（英語、國小健體/社會/藝術的零星缺漏、整個國中）
- 題目資料是空的，需要建題庫（國小主要科目課次資料已經相當完整，可以開始出題）
- 簡答題的多重答案比對邏輯已經寫好（`grading_service.py`），但答案庫要實際填資料
- 老師/家長後台（新增題目、查看學生成績）還沒做
- 學生登入機制還沒做（目前 `students` 表只是最簡欄位）
