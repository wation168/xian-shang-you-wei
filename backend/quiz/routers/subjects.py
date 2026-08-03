from fastapi import APIRouter
from ..database import get_supabase

router = APIRouter(prefix="/api", tags=["subjects"])


@router.get("/school-levels")
def list_school_levels():
    """回傳 國小/國中/高中 選項"""
    sb = get_supabase()
    res = sb.table("school_levels").select("*").order("id").execute()
    return res.data


@router.get("/subjects")
def list_subjects(school_level_id: int):
    """依學制回傳科目清單（前面的科目色標籤用這個）"""
    sb = get_supabase()
    res = (
        sb.table("subjects")
        .select("*")
        .eq("school_level_id", school_level_id)
        .execute()
    )
    return res.data
