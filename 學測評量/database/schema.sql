-- ============================================================
-- 學測評量系統 資料庫 Schema
-- 設計原則：每張表各司其職，之後新增功能就新增表，
-- 不會回頭把新東西塞進既有表裡造成單一結構越來越肥大。
-- ============================================================

-- 啟用 UUID 產生函式
create extension if not exists "pgcrypto";

-- ------------------------------------------------------------
-- 1. school_levels：學制（國小/國中/高中）
--    先建這張表是為了讓「高中之後再擴充」時不用改結構，只要加資料
-- ------------------------------------------------------------
create table school_levels (
  id            smallint primary key,      -- 1=國小 2=國中 3=高中
  code          text not null unique,      -- 'elementary' | 'middle' | 'high'
  name          text not null              -- 顯示用中文名稱
);

insert into school_levels (id, code, name) values
  (1, 'elementary', '國小'),
  (2, 'middle', '國中'),
  (3, 'high', '高中');

-- ------------------------------------------------------------
-- 2. subjects：科目
--    不同學制科目不同（國小有「生活」，國中把理化生地科合併），
--    所以科目要綁 school_level_id
-- ------------------------------------------------------------
create table subjects (
  id              uuid primary key default gen_random_uuid(),
  school_level_id smallint not null references school_levels(id),
  code            text not null,          -- 'chinese' | 'math' | 'english' ...
  name            text not null,          -- 國語 / 數學 ...
  color_hex       text,                   -- 對應介面色標（例如 #D94F4F）
  created_at      timestamptz not null default now(),
  unique (school_level_id, code)
);

-- ------------------------------------------------------------
-- 3. curriculum：課次對照表
--    年級 + 學期 + 出版社 + 課次 + 課名
--    這張表就是之前教育百科查到的「課名清單」要匯入的地方
-- ------------------------------------------------------------
create table curriculum (
  id            uuid primary key default gen_random_uuid(),
  subject_id    uuid not null references subjects(id),
  grade         smallint not null,        -- 1-6（國小）7-9（國中）
  semester      text not null check (semester in ('上','下')),
  publisher     text not null,            -- 南一 / 康軒 / 翰林
  lesson_number smallint not null,        -- 第幾課 / 第幾單元
  lesson_name   text,                     -- 課名（例如「春天的顏色」）
  created_at    timestamptz not null default now(),
  unique (subject_id, grade, semester, publisher, lesson_number)
);

-- ------------------------------------------------------------
-- 4. questions：題庫本體
--    question_type 決定要看 options 還是 correct_order
-- ------------------------------------------------------------
create table questions (
  id              uuid primary key default gen_random_uuid(),
  curriculum_id   uuid not null references curriculum(id),
  question_type   text not null check (
                    question_type in ('single_choice','true_false','fill_blank','ordering')
                  ),
  question_text   text not null,
  image_url       text,                   -- 圖片題用（自然/數學圖表題）
  options         jsonb,                  -- single_choice/true_false 用：[{"key":"A","text":"..."}]
  correct_option  text,                   -- single_choice/true_false 用：對應 options 的 key
  correct_order   jsonb,                  -- ordering 用（筆順排序）：["3","1","4","2"]
  explanation     text,                   -- 詳解
  difficulty      smallint default 1,     -- 1-5
  created_at      timestamptz not null default now()
);

create index idx_questions_curriculum on questions(curriculum_id);

-- ------------------------------------------------------------
-- 5. answer_keys：可接受答案清單（跟題目分開放）
--    fill_blank 題型用，一題可以對應多個正確答案（通同字、多種寫法）
--    這張表故意跟 questions 分開，之後要補答案不用動到題目本身
-- ------------------------------------------------------------
create table answer_keys (
  id              uuid primary key default gen_random_uuid(),
  question_id     uuid not null references questions(id) on delete cascade,
  accepted_answer text not null,
  is_primary      boolean not null default false,  -- 標示「標準答案」，其餘為同義可接受答案
  created_at      timestamptz not null default now()
);

create index idx_answer_keys_question on answer_keys(question_id);

-- ------------------------------------------------------------
-- 6. students：學生帳號（先用最簡欄位，之後要接 Supabase Auth 再擴充）
-- ------------------------------------------------------------
create table students (
  id              uuid primary key default gen_random_uuid(),
  display_name    text not null,
  school_level_id smallint references school_levels(id),
  grade           smallint,
  created_at      timestamptz not null default now()
);

-- ------------------------------------------------------------
-- 7. exam_sessions：一次測驗（把多題 attempts 分組起來）
--    對應介面上「二年級上學期 國語 康軒版 第一課至第六課」這組設定
-- ------------------------------------------------------------
create table exam_sessions (
  id            uuid primary key default gen_random_uuid(),
  student_id    uuid references students(id),
  subject_id    uuid not null references subjects(id),
  grade         smallint not null,
  semester      text not null,
  publisher     text not null,
  lesson_from   smallint not null,
  lesson_to     smallint not null,
  total_count   smallint,
  correct_count smallint,
  started_at    timestamptz not null default now(),
  finished_at   timestamptz
);

-- ------------------------------------------------------------
-- 8. attempts：每一題的作答紀錄
--    用來做「弱點分析」統計，跟 exam_sessions 是多對一
-- ------------------------------------------------------------
create table attempts (
  id                uuid primary key default gen_random_uuid(),
  exam_session_id   uuid not null references exam_sessions(id) on delete cascade,
  question_id       uuid not null references questions(id),
  submitted_answer  jsonb,          -- 文字答案存字串，排序題存陣列
  is_correct        boolean,
  answered_at       timestamptz not null default now()
);

create index idx_attempts_session on attempts(exam_session_id);
create index idx_attempts_question on attempts(question_id);
