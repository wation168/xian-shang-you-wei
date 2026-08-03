from fastapi import APIRouter
from ..database import get_supabase

router = APIRouter(prefix="/api/curriculum", tags=["curriculum"])


@router.get("")
def list_curriculum(subject_id: str, grade: int, semester: str, publisher: str):
    """
    回傳指定 科目+年級+學期+出版社 的課次清單，
    前端下拉選單的「第X課至第Y課」用這支填選項。
    """
    sb = get_supabase()
    res = (
        sb.table("curriculum")
        .select("*")
        .eq("subject_id", subject_id)
        .eq("grade", grade)
        .eq("semester", semester)
        .eq("publisher", publisher)
        .order("lesson_number")
        .execute()
    )
    return res.data
