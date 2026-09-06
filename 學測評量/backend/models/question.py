from typing import Any, Literal
from pydantic import BaseModel

QuestionType = Literal["single_choice", "true_false", "fill_blank", "ordering"]


class QuestionOut(BaseModel):
    """回傳給前端的題目格式——不包含正確答案，避免作弊。"""
    id: str
    curriculum_id: str
    question_type: QuestionType
    question_text: str
    image_url: str | None = None
    options: list[dict[str, Any]] | None = None
    difficulty: int = 1


class SubmitAnswerIn(BaseModel):
    exam_session_id: str
    question_id: str
    submitted_answer: Any  # 字串（選擇/填空）或陣列（排序題）


class SubmitAnswerOut(BaseModel):
    question_id: str
    is_correct: bool
    correct_option: str | None = None
    correct_order: list[str] | None = None
    accepted_answers: list[str] | None = None
    explanation: str | None = None
