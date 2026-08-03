"""
國中教育會考「考古題模式」路由。

跟 exam_sessions.py（課次出題模式）分開的原因：
會考題目是跨三年課程的綜合應用題，不像 questions 表掛在單一課次(curriculum_id)下，
資料存在獨立的 exam_questions 表。這裡故意不比照 exam_sessions 開一個場次表追蹤進度，
先做「整份考卷一次作答、送出後立刻算分」的簡化版（不記錄逐題作答歷程），
之後真的需要弱點分析/中途離開續作時再擴充成有場次表的版本。
"""
from typing import Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..database import get_supabase

router = APIRouter(prefix="/api/exam-practice", tags=["exam-practice"])

SUBJECT_LABEL = {
    "chinese": "國文",
    "math": "數學",
    "social": "社會",
    "science": "自然",
    "english_reading": "英語閱讀",
}


class ExamOption(BaseModel):
    exam_name: str
    subject: str
    subject_label: str
    question_count: int


class ExamQuestionOut(BaseModel):
    question_number: int
    question_text: str
    options: list[dict[str, Any]]
    has_figure: bool


class GradeIn(BaseModel):
    exam_name: str
    subject: str
    answers: dict[str, str]  # {"1": "A", "2": "C", ...} key用字串因為JSON物件key只能是字串


class GradeDetail(BaseModel):
    question_number: int
    submitted: str | None
    correct_option: str | None
    is_correct: bool


class GradeOut(BaseModel):
    exam_name: str
    subject: str
    total: int
    correct: int
    details: list[GradeDetail]


@router.get("/exams", response_model=list[ExamOption])
def list_exams():
    """列出所有可以練習的年度+科目組合，附題數，前端首頁選單用這支"""
    sb = get_supabase()
    res = sb.table("exam_questions").select("exam_name,subject").execute()
    counts: dict[tuple[str, str], int] = {}
    for row in res.data:
        key = (row["exam_name"], row["subject"])
        counts[key] = counts.get(key, 0) + 1

    options = [
        ExamOption(
            exam_name=exam_name,
            subject=subject,
            subject_label=SUBJECT_LABEL.get(subject, subject),
            question_count=count,
        )
        for (exam_name, subject), count in counts.items()
    ]
    options.sort(key=lambda o: (o.exam_name, o.subject), reverse=True)
    return options


@router.get("/questions", response_model=list[ExamQuestionOut])
def get_exam_questions(exam_name: str, subject: str):
    """回傳整份考卷題目（不含正確答案），依題號排序"""
    sb = get_supabase()
    res = (
        sb.table("exam_questions")
        .select("question_number,question_text,options,has_figure")
        .eq("exam_name", exam_name)
        .eq("subject", subject)
        .order("question_number")
        .execute()
    )
    if not res.data:
        raise HTTPException(404, "找不到這份考卷，請確認年度/科目是否正確")
    return res.data


@router.post("/grade", response_model=GradeOut)
def grade_exam(payload: GradeIn):
    """收到整份作答 -> 一次比對 -> 回傳總分+逐題詳解"""
    sb = get_supabase()
    res = (
        sb.table("exam_questions")
        .select("question_number,correct_option")
        .eq("exam_name", payload.exam_name)
        .eq("subject", payload.subject)
        .order("question_number")
        .execute()
    )
    if not res.data:
        raise HTTPException(404, "找不到這份考卷，請確認年度/科目是否正確")

    details = []
    correct_count = 0
    for row in res.data:
        qnum = row["question_number"]
        correct_option = row["correct_option"]
        submitted = payload.answers.get(str(qnum))
        is_correct = bool(submitted) and bool(correct_option) and submitted == correct_option
        if is_correct:
            correct_count += 1
        details.append(
            GradeDetail(
                question_number=qnum,
                submitted=submitted,
                correct_option=correct_option,
                is_correct=is_correct,
            )
        )

    return GradeOut(
        exam_name=payload.exam_name,
        subject=payload.subject,
        total=len(details),
        correct=correct_count,
        details=details,
    )
