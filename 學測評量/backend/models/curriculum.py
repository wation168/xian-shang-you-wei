from pydantic import BaseModel


class CurriculumItem(BaseModel):
    id: str
    subject_id: str
    grade: int
    semester: str
    publisher: str
    lesson_number: int
    lesson_name: str | None = None
