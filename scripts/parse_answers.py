# -*- coding: utf-8 -*-
"""解析111年參考答案PDF (表格式) -> {科目: {題號: 答案}}"""
import pdfplumber, json

SUBJECT_COLS = ["國文", "英語_閱讀", "英語_聽力", "數學", "社會", "自然"]

def parse_answer_pdf(path):
    result = {s: {} for s in SUBJECT_COLS}
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables():
                for row in table:
                    if not row or not row[0] or not row[0].strip().isdigit():
                        continue
                    qnum = int(row[0].strip())
                    # row 結構: [題號, None, 國文, 閱讀, 聽力, 數學, 社會, 自然]
                    vals = row[2:8] if len(row) >= 8 else row[2:]
                    for i, s in enumerate(SUBJECT_COLS):
                        if i < len(vals) and vals[i] and vals[i].strip():
                            result[s][qnum] = vals[i].strip()
    return result

if __name__ == "__main__":
    ans = parse_answer_pdf("/mnt/user-data/uploads/111_參考答案.pdf")
    for s, d in ans.items():
        print(s, f"{len(d)}題", dict(list(d.items())[:3]), "...")
    json.dump(ans, open("/home/claude/exam_work/parsed_answers.json", "w", encoding="utf-8"),
               ensure_ascii=False, indent=2)
