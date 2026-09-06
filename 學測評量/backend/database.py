"""
資料庫連線模組。
只做一件事：建立並提供 Supabase client，不放任何業務邏輯，
避免以後這支檔案被塞進一堆不相干的東西。
"""
import os
from functools import lru_cache
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()


@lru_cache
def get_supabase() -> Client:
    url = os.environ["SUPABASE_URL"]
    key = os.environ["SUPABASE_KEY"]
    return create_client(url, key)
