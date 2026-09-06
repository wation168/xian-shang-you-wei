# -*- coding: utf-8 -*-
"""
國小生字/詞彙 → 練習題目 自動產生器

輸入：add_vocabulary_words.sql（593筆 curriculum_id + words_preview）
輸出：add_practice_questions.sql（可直接貼到 Supabase SQL Editor 執行）

題型設計說明（先講清楚資料限制，不是隨便設計的）：
- 來源資料 words_preview 只是「該課生字/詞彙的前幾筆節錄」，不是完整清單
  （593筆裡有557筆結尾是「...」代表還有更多字沒被抓到）。
- 因此題目設計刻意避開需要「完整性」的題型（例如「以下哪個字不是本課生字」
  這種需要確定排除法的題型不能做，因為未列出的字不代表不是本課的字）。
- 改用「認字歸類」題型：從A課的已知生字中挑1個當正確答案，從其他課的已知
  生字中挑3個當干擾選項，避免使用「正確答案課」自己清單裡已出現的字當干擾項
  （降低選項重疊風險，但無法100%排除——因為干擾項所屬的其他課可能剛好也教
  過同一個字只是沒被收錄進preview，這是資料來源本身的已知限制，非本腳本bug）。
- 每課視詞彙量產生 1 題單選題（single_choice）+ 最多 1 題是非題（true_false）。
"""
import re
import json
import random
import argparse

random.seed(42)  # 固定種子，重跑結果一致，方便帥哥鴻比對差異


def parse_vocab_sql(path):
    text = open(path, encoding="utf-8").read()
    blocks = re.findall(r"insert into vocabulary_words.*?\);", text, re.S)
    lessons = []
    for b in blocks:
        subj = re.search(r"code='(\w+)'", b)
        grade = re.search(r"grade=(\d+)", b)
        sem = re.search(r"semester='([^']+)'", b)
        pub = re.search(r"publisher='([^']+)'", b)
        ln = re.search(r"lesson_number=(\d+)", b)
        qs = re.findall(r"'([^']*)'", b)
        wtext = qs[-1] if qs else ""
        words = [w.strip() for w in wtext.rstrip(".").split(",") if w.strip()]
        if not (subj and grade and sem and pub and ln) or not words:
            continue
        lessons.append({
            "subject_code": subj.group(1),
            "grade": int(grade.group(1)),
            "semester": sem.group(1),
            "publisher": pub.group(1),
            "lesson_number": int(ln.group(1)),
            "words": words,
        })
    return lessons


SUBJECT_LABEL = {"chinese": "國語", "social": "社會", "science": "自然科學"}


def curriculum_subquery(lesson):
    return (
        "(select id from curriculum where subject_id="
        f"(select id from subjects where code='{lesson['subject_code']}' and school_level_id=1) "
        f"and grade={lesson['grade']} and semester='{lesson['semester']}' "
        f"and publisher='{lesson['publisher']}' and lesson_number={lesson['lesson_number']})"
    )


def lesson_label(lesson):
    subj = SUBJECT_LABEL.get(lesson["subject_code"], lesson["subject_code"])
    return f"{lesson['publisher']}版 {lesson['grade']}年級{lesson['semester']}學期 {subj}科 第{lesson['lesson_number']}課"


def build_distractor_pool(lessons):
    """依科目分組，之後只在同科目內抽干擾選項（避免跨科混題，難度失焦）"""
    pool = {}
    for lesson in lessons:
        pool.setdefault(lesson["subject_code"], []).append(lesson)
    return pool


def pick_distractors(lesson, pool_by_subject, n=3):
    same_subject_lessons = [
        l for l in pool_by_subject[lesson["subject_code"]]
        if not (l["grade"] == lesson["grade"] and l["semester"] == lesson["semester"]
                and l["publisher"] == lesson["publisher"] and l["lesson_number"] == lesson["lesson_number"])
    ]
    random.shuffle(same_subject_lessons)
    exclude = set(lesson["words"])
    distractors = []
    for l in same_subject_lessons:
        candidates = [w for w in l["words"] if w not in exclude]
        if candidates:
            distractors.append(random.choice(candidates))
            exclude.add(distractors[-1])
        if len(distractors) >= n:
            break
    return distractors[:n]


def sql_escape(s):
    return s.replace("'", "''")


def gen_single_choice(lesson, correct_word, distractors, subquery):
    options = [{"key": k, "text": w} for k, w in zip("ABCD", [correct_word] + distractors)]
    random.shuffle(options)
    for i, k in enumerate("ABCD"):
        options[i]["key"] = k
    correct_key = next(o["key"] for o in options if o["text"] == correct_word)
    options_json = json.dumps(options, ensure_ascii=False)
    label = lesson_label(lesson)
    stem = f"下列何者是「{label}」列出的生字／詞語之一？"
    explanation = (
        f"資料來源：教育部教育百科生字詞彙表（{label}節錄）。"
        f"正確答案「{correct_word}」出自該課詞彙節錄清單。"
    )
    return (
        f"insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (\n"
        f"  {subquery},\n"
        f"  'single_choice',\n"
        f"  '{sql_escape(stem)}',\n"
        f"  '{sql_escape(options_json)}'::jsonb,\n"
        f"  '{correct_key}',\n"
        f"  '{sql_escape(explanation)}'\n"
        f");"
    )


def gen_true_false(lesson, word, is_true, subquery):
    label = lesson_label(lesson)
    stem = f"「{word}」是「{label}」列出的生字／詞語之一。"
    options_json = json.dumps(
        [{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}], ensure_ascii=False
    )
    correct_key = "A" if is_true else "B"
    explanation = (
        f"資料來源：教育部教育百科生字詞彙表（{label}節錄）。"
        + (f"「{word}」出自該課詞彙節錄清單，故為正確。"
           if is_true else f"「{word}」出自其他課，非「{label}」節錄清單內的字詞，故為錯誤。")
    )
    return (
        f"insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (\n"
        f"  {subquery},\n"
        f"  'true_false',\n"
        f"  '{sql_escape(stem)}',\n"
        f"  '{sql_escape(options_json)}'::jsonb,\n"
        f"  '{correct_key}',\n"
        f"  '{sql_escape(explanation)}'\n"
        f");"
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="infile", default="add_vocabulary_words.sql")
    ap.add_argument("--out", dest="outfile", default="add_practice_questions.sql")
    args = ap.parse_args()

    lessons = parse_vocab_sql(args.infile)
    pool = build_distractor_pool(lessons)

    sqls = [
        "-- ============================================================",
        "-- 生字/詞彙練習題目 自動產生（由 generate_vocab_questions.py 產生）",
        "-- 題型：single_choice（認字歸類）+ true_false（是非題）",
        "-- ⚠️ 資料來源是節錄清單非完整清單，干擾選項理論上有極低機率誤判，",
        "--    詳見腳本檔頭說明，非程式bug",
        "-- ============================================================",
        "",
    ]
    n_single = 0
    n_tf = 0
    skipped = 0

    for lesson in lessons:
        distractors = pick_distractors(lesson, pool, n=3)
        if len(distractors) < 3:
            skipped += 1
            continue  # 該科目其他課詞彙不足以湊出3個干擾項，先跳過（極少數）

        subquery = curriculum_subquery(lesson)
        words = lesson["words"]

        # 單選題：用第一個字當正確答案
        sqls.append(gen_single_choice(lesson, words[0], distractors, subquery))
        n_single += 1

        # 是非題：若該課有第2個字，用它做題；奇偶課次決定出「正確」或「錯誤」版本，
        # 讓正確/錯誤題目大致各半，不是每題都對或都錯
        if len(words) >= 2:
            tf_word = words[1]
            is_true = (lesson["lesson_number"] % 2 == 0)
            if not is_true:
                # 錯誤版：改用別課的字
                tf_word = distractors[0]
            sqls.append(gen_true_false(lesson, tf_word, is_true, subquery))
            n_tf += 1

    with open(args.outfile, "w", encoding="utf-8") as f:
        f.write("\n".join(sqls) + "\n")

    print(f"共處理 {len(lessons)} 課，跳過 {skipped} 課（干擾項不足）")
    print(f"產生 single_choice {n_single} 題、true_false {n_tf} 題，"
          f"合計 {n_single + n_tf} 題 → {args.outfile}")


if __name__ == "__main__":
    main()
