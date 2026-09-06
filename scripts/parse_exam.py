# -*- coding: utf-8 -*-
"""
國中會考PDF拆題原型 v1
用途：從單科選擇題PDF抽取題號/題幹/選項，並標記是否依賴圖表(圖片OCR無法從純文字取得)
輸出：JSON，供人工核對後再寫入資料庫
"""
import pdfplumber
import re
import json
import sys

def extract_full_text(pdf_path, skip_pages=1):
    """skip_pages: 跳過封面說明頁數(通常第1頁是作答說明)"""
    texts = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            if i < skip_pages:
                continue
            t = page.extract_text() or ""
            texts.append(t)
    return "\n".join(texts)

# 題號開頭樣式：數字+半形或全形句點，行首出現 (含跨頁換行清乾淨後判斷)
QNUM_RE = re.compile(r'(?:^|\n)\s*(\d{1,2})\.\s?')
# 選項樣式，中文/英文題本共用 (A)... (B)... 或 (A) ... 半形全形皆抓
OPT_RE = re.compile(r'\(([A-D])\)\s*([^\(\n]+?)(?=\s*\([A-D]\)|\n|$)')

def split_questions(full_text, max_q=60):
    """依題號切分成 raw question blocks。
    關鍵修正：註腳(如「1.醪：音ㄌㄠˊ...」)也符合「數字+句點」樣式，
    會被誤判成新題號、把上一題切斷。做法是只接受「等於目前預期題號」
    的匹配當作真正的題目邊界，其餘一律視為雜訊（註腳、頁碼等）忽略。
    """
    matches = list(QNUM_RE.finditer(full_text))
    accepted = []  # (qnum, content_start, match_start)
    expected = 1
    for m in matches:
        qnum = int(m.group(1))
        if qnum == expected:
            accepted.append((qnum, m.end(), m.start()))
            expected += 1
        if expected > max_q:
            break
    blocks = {}
    for i, (qnum, content_start, _) in enumerate(accepted):
        end = accepted[i+1][2] if i+1 < len(accepted) else len(full_text)
        blocks[qnum] = full_text[content_start:end].strip()
    return blocks

def parse_block(qnum, block):
    """從單題原始區塊拆出題幹與選項"""
    opts = OPT_RE.findall(block)
    options = [{"key": k, "text": v.strip()} for k, v in opts]
    # 題幹 = 第一個選項出現位置之前的文字
    first_opt_pos = block.find("(A)")
    stem = block[:first_opt_pos].strip() if first_opt_pos > 0 else block.strip()
    needs_visual = bool(re.search(r'圖[\(（]|表[\(（]|如圖|如表', block))
    return {
        "question_number": qnum,
        "question_text": stem,
        "options": options,
        "option_count": len(options),
        "needs_visual_asset": needs_visual,
    }

def parse_subject_pdf(pdf_path, subject_name, max_q, skip_pages=1):
    full_text = extract_full_text(pdf_path, skip_pages=skip_pages)
    blocks = split_questions(full_text, max_q=max_q)
    questions = []
    for qnum in sorted(blocks.keys()):
        q = parse_block(qnum, blocks[qnum])
        q["subject"] = subject_name
        questions.append(q)
    return questions

if __name__ == "__main__":
    configs = [
        ("/mnt/user-data/uploads/111_國文科.pdf", "國文", 42),
        ("/mnt/user-data/uploads/111_自然科.pdf", "自然", 50),
        ("/mnt/user-data/uploads/111_社會科.pdf", "社會", 54),
        ("/mnt/user-data/uploads/111_數學科.pdf", "數學(選擇題)", 25),
    ]
    all_results = {}
    for path, name, maxq in configs:
        qs = parse_subject_pdf(path, name, maxq)
        all_results[name] = qs
        ok = sum(1 for q in qs if q["option_count"] == 4)
        visual = sum(1 for q in qs if q["needs_visual_asset"])
        print(f"{name}: 抓到 {len(qs)}/{maxq} 題, 選項數=4的有 {ok} 題, 依賴圖表的有 {visual} 題")

    with open("/home/claude/exam_work/parsed_questions.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
