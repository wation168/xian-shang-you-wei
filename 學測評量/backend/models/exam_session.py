from pydantic import BaseModel


class StartSessionIn(BaseModel):
    student_id: str | None = None
    subject_id: str
    grade: int
    semester: str
    publisher: str
    lesson_from: int
    lesson_to: int


class StartSessionOut(BaseModel):
    exam_session_id: str
    question_count: int
