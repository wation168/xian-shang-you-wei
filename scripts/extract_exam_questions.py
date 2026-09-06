# -*- coding: utf-8 -*-
"""
國中教育會考 PDF 拆題腳本（MVP版，先用111年國文/數學驗證，之後可推廣到全部39份）

用法：
  python3 extract_exam_questions.py <pdf路徑> --subject chinese|math --year 111 --out out.json

限制（重要，先講清楚）：
1. 這支腳本只拆「純文字題幹＋4選項」的題目。含圖表/圖片的題目（如國文Q1讀書示意圖、
   Q4篆體字表、Q25死因統計表；數學Q1數線圖、Q4展開圖等），題幹文字通常能抓到，
   但圖片/表格本身的圖像內容不會被還原，這類題目會被標記 has_figure=true，
   需要人工補圖或之後再開發圖表擷取。
2. 這份題目卷本身「沒有正確答案」，正確答案要另外比對官方公布的答案卷
   （帥哥鴻之前已抓到的40筆Google Drive連結裡應該包含「參考答案」檔案，
   目前這次對話沒有上傳，correct_option 欄位先留空，之後比對後再補上）。
3. 題組（共用一段閱讀材料的多題）目前把「共用文章」跟「各小題」都各自抓出來，
   但沒有自動把文章內容關聯進每小題的 question_text 內，這部分是題組題型
   之後要加強的地方（目前先讓單題可以正確跑出來）。
"""
import re
import json
import argparse
import pdfplumber


def extract_all_text(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        pages_text = [p.extract_text() or "" for p in pdf.pages]
    return pages_text


# 題號開頭：行首 1-2位數字 + "." + 空白，且下一個字元不是純數字延續（避免誤判年份等）
QNUM_RE = re.compile(r'(?m)^(\d{1,2})\.\s+')
OPT_RE = re.compile(r'\(([A-D])\)\s*([^\(\n]*?)(?=(?:\s*\([A-D]\))|\n|$)')


def split_questions(full_text):
    """把整份文字依題號切成區塊，回傳 [(qnum, block_text), ...]"""
    matches = list(QNUM_RE.finditer(full_text))
    blocks = []
    for i, m in enumerate(matches):
        qnum = int(m.group(1))
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(full_text)
        block = full_text[start:end].strip()
        blocks.append((qnum, block))
    return blocks


def parse_block(qnum, block):
    """從一個題目區塊拆出 stem + options"""
    opts = OPT_RE.findall(block)
    if not opts:
        return None  # 抓不到4個選項，可能是題組共用文章或圖表題，先跳過丟進 unmatched

    # stem = 第一個 (A) 出現之前的文字
    first_opt_pos = block.find('(A)')
    stem = block[:first_opt_pos].strip() if first_opt_pos > 0 else block.strip()

    options = []
    seen_keys = set()
    for key, text in opts:
        text = text.strip()
        if key in seen_keys:
            continue
        seen_keys.add(key)
        options.append({"key": key, "text": text})

    has_figure = len(stem) < 6  # 題幹太短，極可能是圖表/圖片題（文字被圖片吃掉）

    return {
        "question_number": qnum,
        "question_text": stem,
        "options": options,
        "correct_option": None,   # 需比對官方答案卷後補上
        "has_figure": has_figure,
        "option_count": len(options),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf_path")
    ap.add_argument("--subject", required=True)
    ap.add_argument("--year", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    pages_text = extract_all_text(args.pdf_path)
    full_text = "\n".join(pages_text)

    blocks = split_questions(full_text)
    questions = []
    unmatched = []
    for qnum, block in blocks:
        parsed = parse_block(qnum, block)
        if parsed is None:
            unmatched.append({"question_number": qnum, "raw": block[:200]})
            continue
        parsed["subject"] = args.subject
        parsed["year"] = args.year
        questions.append(parsed)

    result = {
        "source_pdf": args.pdf_path,
        "subject": args.subject,
        "year": args.year,
        "total_detected": len(blocks),
        "parsed_ok": len(questions),
        "unmatched": len(unmatched),
        "questions": questions,
        "unmatched_blocks": unmatched,
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"[{args.subject}] 偵測到題號 {len(blocks)} 個，成功解析 {len(questions)} 題，"
          f"無法直接解析(可能是題組/圖表題) {len(unmatched)} 題 → {args.out}")


if __name__ == "__main__":
    main()
