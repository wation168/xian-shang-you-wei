-- ============================================================
-- Migration: 新增會考題庫專用資料表
-- 日期：2026/08/02
-- 說明：國中會考題目不是照課本課次出的（不像 curriculum 表那樣
--       綁 年級/學期/版本/第幾課），所以另外開兩張表，跟原本
--       questions/answer_keys（課本生字題用）分開，各司其職。
--
-- 使用方式：把這份檔案的內容貼到 Supabase SQL Editor 執行，
--          或接在原本 schema.sql 後面一起執行都可以，
--          不會影響、也不會修改任何既有的表。
-- ============================================================

-- ------------------------------------------------------------
-- 1. exam_papers：一份考卷（某年度、某科目）
-- ------------------------------------------------------------
create table exam_papers (
  id          uuid primary key default gen_random_uuid(),
  year        smallint not null,              -- 111, 112, 113...
  subject     text not null,                  -- 國文 / 英語閱讀 / 英語聽力 / 數學 / 社會 / 自然 / 寫作測驗
  source      text not null default '教育部國民及學前教育署國中教育會考',
  total_questions smallint,                   -- 這份考卷選擇題總題數，方便前端顯示進度
  created_at  timestamptz not null default now(),
  unique (year, subject)
);

-- ------------------------------------------------------------
-- 2. exam_questions：考卷底下的每一題
-- ------------------------------------------------------------
create table exam_questions (
  id                 uuid primary key default gen_random_uuid(),
  exam_paper_id      uuid not null references exam_papers(id) on delete cascade,
  question_number    smallint not null,
  question_text      text not null,
  image_url          text,                    -- 題幹或選項需要圖片時使用，先留空
  options             jsonb not null,          -- [{"key":"A","text":"..."}, ...]
  correct_option      text not null,           -- "A" / "B" / "C" / "D"
  needs_visual_asset  boolean not null default false,  -- true = 選項本身是圖片，純文字題庫暫不收錄，待補圖後再開放
  created_at          timestamptz not null default now(),
  unique (exam_paper_id, question_number)
);

create index idx_exam_questions_paper on exam_questions(exam_paper_id);
create index idx_exam_questions_visual on exam_questions(needs_visual_asset);

-- ------------------------------------------------------------
-- 3. exam_attempts：學生作答會考題庫的紀錄
--    跟原本的 exam_sessions/attempts（課本題庫用）分開，
--    因為會考題庫沒有「範圍設定」（年級/學期/版本/第幾課到第幾課）
--    這個概念，是整份考卷或抽題作答。
-- ------------------------------------------------------------
create table exam_attempts (
  id                uuid primary key default gen_random_uuid(),
  student_id        uuid references students(id),
  exam_question_id  uuid not null references exam_questions(id),
  submitted_answer  text,
  is_correct        boolean,
  answered_at       timestamptz not null default now()
);

create index idx_exam_attempts_student on exam_attempts(student_id);
create index idx_exam_attempts_question on exam_attempts(exam_question_id);

-- ------------------------------------------------------------
-- 使用提示：
-- - needs_visual_asset = true 的題目，前端題庫先不要顯示，
--   等之後人工把圖片補上（image_url 填好）再打開。
-- - 匯入資料的順序：先 insert exam_papers 拿到 id，
--   再用該 id 批次 insert exam_questions。
-- - 每次拆解新一年度/新科目的PDF，重跑 parse_exam.py +
--   parse_answers.py 產生 JSON 後，寫一支小腳本把 JSON
--   轉成 INSERT 語句即可，不用手動一題一題貼。
-- ============================================================
