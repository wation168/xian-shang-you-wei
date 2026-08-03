from fastapi import APIRouter, HTTPException
from ..database import get_supabase
from ..models.exam_session import StartSessionIn, StartSessionOut
from ..models.question import QuestionOut, SubmitAnswerIn, SubmitAnswerOut
from ..services.grading_service import grade_answer

router = APIRouter(prefix="/api/exam-sessions", tags=["exam-sessions"])


@router.post("", response_model=StartSessionOut)
def start_session(payload: StartSessionIn):
    """
    依照使用者在下拉選單選的（年級/學期/出版社/課次範圍），
    找出對應課次 -> 找出對應題目 -> 開一個新的測驗場次。
    """
    sb = get_supabase()

    curriculum_res = (
        sb.table("curriculum")
        .select("id")
        .eq("subject_id", payload.subject_id)
        .eq("grade", payload.grade)
        .eq("semester", payload.semester)
        .eq("publisher", payload.publisher)
        .gte("lesson_number", payload.lesson_from)
        .lte("lesson_number", payload.lesson_to)
        .execute()
    )
    curriculum_ids = [row["id"] for row in curriculum_res.data]
    if not curriculum_ids:
        raise HTTPException(404, "找不到對應課次，請確認課次資料是否已匯入")

    questions_res = (
        sb.table("questions").select("id").in_("curriculum_id", curriculum_ids).execute()
    )
    question_count = len(questions_res.data)
    if question_count == 0:
        raise HTTPException(404, "這個範圍還沒有題目")

    session_res = (
        sb.table("exam_sessions")
        .insert(
            {
                "student_id": payload.student_id,
                "subject_id": payload.subject_id,
                "grade": payload.grade,
                "semester": payload.semester,
                "publisher": payload.publisher,
                "lesson_from": payload.lesson_from,
                "lesson_to": payload.lesson_to,
                "total_count": question_count,
            }
        )
        .execute()
    )
    session_id = session_res.data[0]["id"]

    return StartSessionOut(exam_session_id=session_id, question_count=question_count)


@router.get("/{session_id}/questions", response_model=list[QuestionOut])
def get_session_questions(session_id: str):
    """回傳該場次的題目（不含正確答案，避免作弊）"""
    sb = get_supabase()

    session_res = sb.table("exam_sessions").select("*").eq("id", session_id).single().execute()
    session = session_res.data
    if not session:
        raise HTTPException(404, "找不到這個測驗場次")

    curriculum_res = (
        sb.table("curriculum")
        .select("id")
        .eq("subject_id", session["subject_id"])
        .eq("grade", session["grade"])
        .eq("semester", session["semester"])
        .eq("publisher", session["publisher"])
        .gte("lesson_number", session["lesson_from"])
        .lte("lesson_number", session["lesson_to"])
        .execute()
    )
    curriculum_ids = [row["id"] for row in curriculum_res.data]

    questions_res = (
        sb.table("questions")
        .select("id,curriculum_id,question_type,question_text,image_url,options,difficulty")
        .in_("curriculum_id", curriculum_ids)
        .execute()
    )
    return questions_res.data


@router.post("/{session_id}/answers", response_model=SubmitAnswerOut)
def submit_answer(session_id: str, payload: SubmitAnswerIn):
    """
    收到學生的一個答案 -> 查出題目正確答案 -> 即時比對 -> 存進 attempts -> 回傳結果。
    這支是「即時閱卷」的核心進入點。

    驗證邏輯（補上，避免答案被亂塞或跨場次作答）：
    1. body 裡的 exam_session_id 必須跟網址路徑的 session_id 一致
    2. question_id 必須屬於這個場次當初設定的課次範圍內，不能亂傳別課的題目id進來
    """
    sb = get_supabase()

    if payload.exam_session_id != session_id:
        raise HTTPException(400, "exam_session_id 與網址路徑的場次不一致")

    session_res = sb.table("exam_sessions").select("*").eq("id", session_id).single().execute()
    session = session_res.data
    if not session:
        raise HTTPException(404, "找不到這個測驗場次")

    curriculum_res = (
        sb.table("curriculum")
        .select("id")
        .eq("subject_id", session["subject_id"])
        .eq("grade", session["grade"])
        .eq("semester", session["semester"])
        .eq("publisher", session["publisher"])
        .gte("lesson_number", session["lesson_from"])
        .lte("lesson_number", session["lesson_to"])
        .execute()
    )
    allowed_curriculum_ids = {row["id"] for row in curriculum_res.data}

    question_res = (
        sb.table("questions").select("*").eq("id", payload.question_id).single().execute()
    )
    question = question_res.data
    if not question:
        raise HTTPException(404, "找不到這一題")

    if question["curriculum_id"] not in allowed_curriculum_ids:
        raise HTTPException(400, "這一題不屬於此場次的課次範圍")

    accepted_answers = None
    if question["question_type"] == "fill_blank":
        ak_res = (
            sb.table("answer_keys")
            .select("accepted_answer")
            .eq("question_id", payload.question_id)
            .execute()
        )
        accepted_answers = [row["accepted_answer"] for row in ak_res.data]

    is_correct = grade_answer(
        question_type=question["question_type"],
        submitted_answer=payload.submitted_answer,
        correct_option=question.get("correct_option"),
        correct_order=question.get("correct_order"),
        accepted_answers=accepted_answers,
    )

    sb.table("attempts").insert(
        {
            "exam_session_id": session_id,
            "question_id": payload.question_id,
            "submitted_answer": payload.submitted_answer,
            "is_correct": is_correct,
        }
    ).execute()

    return SubmitAnswerOut(
        question_id=payload.question_id,
        is_correct=is_correct,
        correct_option=question.get("correct_option"),
        correct_order=question.get("correct_order"),
        accepted_answers=accepted_answers,
        explanation=question.get("explanation"),
    )


@router.post("/{session_id}/finish")
def finish_session(session_id: str):
    """結束測驗，統計對錯題數並回傳成績摘要"""
    sb = get_supabase()

    attempts_res = (
        sb.table("attempts").select("is_correct").eq("exam_session_id", session_id).execute()
    )
    total = len(attempts_res.data)
    correct = sum(1 for a in attempts_res.data if a["is_correct"])

    sb.table("exam_sessions").update(
        {"correct_count": correct, "finished_at": "now()"}
    ).eq("id", session_id).execute()

    return {"exam_session_id": session_id, "total_answered": total, "correct_count": correct}
