"""
即時閱卷核心邏輯。
故意獨立成一支檔案、不直接碰資料庫，方便之後：
  1. 單獨寫測試
  2. 之後要加新題型時，只改這裡，不用動 router

⚠️ 內容跟原本獨立版本完全相同，這支沒有內部 import，不受掛載影響。
"""
from typing import Any


def normalize_text(value: str) -> str:
    """全形轉半形、去除頭尾空白，減少「格式不同被誤判成錯」的情況。"""
    if value is None:
        return ""
    full_to_half = str.maketrans(
        "０１２３４５６７８９ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ",
        "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    )
    return value.strip().translate(full_to_half)


def grade_single_choice(submitted_answer: str, correct_option: str) -> bool:
    return normalize_text(str(submitted_answer)) == normalize_text(str(correct_option))


def grade_true_false(submitted_answer: str, correct_option: str) -> bool:
    return normalize_text(str(submitted_answer)) == normalize_text(str(correct_option))


def grade_fill_blank(submitted_answer: str, accepted_answers: list[str]) -> bool:
    """比對「可接受答案清單」而非單一標準答案，降低通同字/多寫法誤判。"""
    normalized_submitted = normalize_text(str(submitted_answer))
    return normalized_submitted in {normalize_text(a) for a in accepted_answers}


def grade_ordering(submitted_answer: list, correct_order: list) -> bool:
    return [normalize_text(str(x)) for x in submitted_answer] == [
        normalize_text(str(x)) for x in correct_order
    ]


def grade_answer(
    question_type: str,
    submitted_answer: Any,
    correct_option: str | None,
    correct_order: list | None,
    accepted_answers: list[str] | None,
) -> bool:
    if question_type in ("single_choice",):
        return grade_single_choice(submitted_answer, correct_option or "")
    if question_type == "true_false":
        return grade_true_false(submitted_answer, correct_option or "")
    if question_type == "fill_blank":
        return grade_fill_blank(submitted_answer, accepted_answers or [])
    if question_type == "ordering":
        return grade_ordering(submitted_answer, correct_order or [])
    raise ValueError(f"未知的題型: {question_type}")
