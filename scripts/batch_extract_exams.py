# -*- coding: utf-8 -*-
r"""
國中教育會考 PDF 批次拆題腳本（可處理整個資料夾的多年度多科目）

用法（在 D:\xian-shang-you-wei\scripts\ 底下執行）：
  python3 batch_extract_exams.py --dir cap_exam_pdfs --out exam_questions_all.sql

前置需求（第一次用要先裝套件，之後不用重裝）：
  pip install pdfplumber --break-system-packages

檔名規則（照你目前 exam_links.csv 下載下來的命名方式）：
  題目卷：{年度}_{科目}科.pdf   例如 111_國文科.pdf、112_數學科.pdf
  答案卷：{年度}_參考答案.pdf

支援科目關鍵字對應：國文→chinese、數學→math、社會→social、自然→science、
                    英語(閱讀)→english_reading
  （英語聽力題型跟其他科不同、寫作測驗非選擇題，這兩種不在此腳本處理範圍內）

執行後會輸出：
  1. exam_questions_all.sql — 可直接貼Supabase SQL Editor執行
  2. extract_report.txt — 每份PDF拆解成功/失敗統計，方便你知道哪幾份需要人工複查
"""
import re
import json
import argparse
import glob
import os
import pdfplumber


SUBJECT_KEYWORDS = {
    "國文": "chinese",
    "數學": "math",
    "社會": "social",
    "自然": "science",
    "英語": "english_reading",
}

QNUM_RE = re.compile(r'(?m)^(\d{1,2})\.\s+')
OPT_RE = re.compile(r'\(\s*([A-D])\s*\)\s*([^\(\n]*?)(?=(?:\s*\(\s*[A-D]\s*\))|\n|$)')


# ---------- 題目卷拆解（沿用單份版本邏輯） ----------

def extract_all_text(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return [p.extract_text() or "" for p in pdf.pages]


def split_questions(full_text):
    matches = list(QNUM_RE.finditer(full_text))
    blocks = []
    for i, m in enumerate(matches):
        qnum = int(m.group(1))
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(full_text)
        blocks.append((qnum, full_text[start:end].strip()))
    return blocks


def parse_block(qnum, block):
    opts = OPT_RE.findall(block)
    if not opts:
        return None
    first_opt_pos = block.find('(A)')
    stem = block[:first_opt_pos].strip() if first_opt_pos > 0 else block.strip()
    options, seen = [], set()
    for key, text in opts:
        text = text.strip()
        if key in seen:
            continue
        seen.add(key)
        options.append({"key": key, "text": text})
    if len(options) != 4:
        return None
    return {
        "question_number": qnum,
        "question_text": stem,
        "options": options,
        "has_figure": len(stem) < 6,
    }


def extract_questions_from_pdf(pdf_path):
    full_text = "\n".join(extract_all_text(pdf_path))
    blocks = split_questions(full_text)
    questions, unmatched = [], []
    for qnum, block in blocks:
        parsed = parse_block(qnum, block)
        if parsed is None:
            unmatched.append(qnum)
        else:
            questions.append(parsed)
    return questions, unmatched, len(blocks)


# ---------- 答案卷拆解（自動讀表格，不再人工抄） ----------

def extract_answer_key(pdf_path):
    """
    回傳 {subject_code: {question_number: answer_letter}}
    邏輯：逐頁抓表格，第一列是科目表頭（可能含中英語閱讀/聽力兩欄），
    之後每列第一欄是題號、其餘欄位對應各科答案。
    表頭關鍵字比對用 SUBJECT_KEYWORDS，抓不到的欄位（如英語聽力）直接略過。
    """
    answers = {}
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                if not table or len(table) < 2:
                    continue
                header = table[0]
                # 找出每一欄對應哪個科目代碼（None代表不認得/略過，如英語聽力）
                col_subject = []
                for cell in header:
                    cell = (cell or "").strip()
                    matched = None
                    for kw, code in SUBJECT_KEYWORDS.items():
                        if kw in cell:
                            matched = code
                            break
                    if "聽力" in cell:
                        matched = None  # 聽力題型不同，不併入 english_reading
                    col_subject.append(matched)
                for row in table[1:]:
                    if not row or not row[0] or not row[0].strip().isdigit():
                        continue
                    qnum = int(row[0].strip())
                    for i, cell in enumerate(row[1:], start=1):
                        if i >= len(col_subject) or col_subject[i] is None:
                            continue
                        val = (cell or "").strip()
                        if val in ("A", "B", "C", "D"):
                            answers.setdefault(col_subject[i], {})[qnum] = val
    return answers


# ---------- 主流程 ----------

def sql_escape(s):
    return s.replace("'", "''")


def gen_insert(exam_name, subject, rows):
    out = []
    for q in rows:
        options_json = json.dumps(q["options"], ensure_ascii=False)
        correct = f"'{q['correct_option']}'" if q.get("correct_option") else "null"
        out.append(
            "insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (\n"
            f"  '{sql_escape(exam_name)}',\n"
            f"  '{subject}',\n"
            f"  {q['question_number']},\n"
            f"  '{sql_escape(q['question_text'])}',\n"
            f"  '{sql_escape(options_json)}'::jsonb,\n"
            f"  {correct},\n"
            f"  {'true' if q['has_figure'] else 'false'}\n"
            f") on conflict (exam_name, subject, question_number) do update set\n"
            f"  question_text = excluded.question_text,\n"
            f"  options = excluded.options,\n"
            f"  correct_option = excluded.correct_option,\n"
            f"  has_figure = excluded.has_figure;"
        )
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True, help="放PDF的資料夾路徑")
    ap.add_argument("--out", default="exam_questions_all.sql")
    ap.add_argument("--report", default="extract_report.txt")
    args = ap.parse_args()

    pdf_files = glob.glob(os.path.join(args.dir, "*.pdf"))
    by_year = {}
    for path in pdf_files:
        fn = os.path.basename(path)
        m = re.match(r"(\d{3})_(.+?)\.pdf$", fn)
        if not m:
            continue
        year, label = m.groups()
        by_year.setdefault(year, {})[label] = path

    all_sql = [
        "create table if not exists exam_questions (",
        "  id              uuid primary key default gen_random_uuid(),",
        "  exam_name       text not null,",
        "  subject         text not null,",
        "  question_number smallint not null,",
        "  question_text   text not null,",
        "  options         jsonb not null,",
        "  correct_option  text,",
        "  has_figure      boolean not null default false,",
        "  created_at      timestamptz not null default now(),",
        "  unique (exam_name, subject, question_number)",
        ");",
        "",
    ]
    report_lines = []
    total_inserted = 0
    bad_files = []

    for year in sorted(by_year):
        files = by_year[year]
        answer_key_path = files.get("參考答案")
        answers = {}
        if answer_key_path:
            try:
                answers = extract_answer_key(answer_key_path)
            except Exception as e:
                bad_files.append(answer_key_path)
                report_lines.append(f"[{year}年-參考答案] ❌ 檔案無法讀取（可能是壞檔）：{e}")
        else:
            report_lines.append(f"[{year}年] ⚠️ 找不到 {year}_參考答案.pdf，這年答案全部留空")

        for label, path in files.items():
            if label == "參考答案":
                continue
            subject_code = None
            for kw, code in SUBJECT_KEYWORDS.items():
                if kw in label:
                    subject_code = code
                    break
            if not subject_code:
                report_lines.append(f"[{year}年] ⚠️ 無法辨識科目：{label}.pdf，已跳過")
                continue

            try:
                questions, unmatched, total_detected = extract_questions_from_pdf(path)
            except Exception as e:
                bad_files.append(path)
                report_lines.append(f"[{year}年-{label}] ❌ 檔案無法讀取（可能是壞檔），已跳過此檔繼續處理下一份：{e}")
                continue
            subj_answers = answers.get(subject_code, {})
            matched_ans, missing_ans = 0, []
            for q in questions:
                a = subj_answers.get(q["question_number"])
                q["correct_option"] = a
                if a:
                    matched_ans += 1
                else:
                    missing_ans.append(q["question_number"])

            exam_name = f"{year}年國中教育會考"
            all_sql += gen_insert(exam_name, subject_code, questions)
            total_inserted += len(questions)

            report_lines.append(
                f"[{year}年-{label}] 偵測題號{total_detected}｜成功解析{len(questions)}｜"
                f"解析失敗{unmatched}｜有答案{matched_ans}｜缺答案{missing_ans}"
            )

    with open(args.out, "w", encoding="utf-8") as f:
        f.write("\n".join(all_sql) + "\n")
    with open(args.report, "w", encoding="utf-8") as f:
        if bad_files:
            f.write(f"⚠️ 共有 {len(bad_files)} 份PDF無法讀取（可能是壞檔），已自動跳過：\n")
            for bf in bad_files:
                f.write(f"  - {bf}\n")
            f.write("\n")
        f.write("\n".join(report_lines) + "\n")

    print(f"共處理 {len(by_year)} 個年度，產生 {total_inserted} 筆題目 → {args.out}")
    if bad_files:
        print(f"⚠️ 有 {len(bad_files)} 份PDF讀取失敗（已跳過，詳見報告）：{bad_files}")
    print(f"詳細報告 → {args.report}（務必打開看一下每份PDF的解析成功率跟缺答案清單）")


if __name__ == "__main__":
    main()
