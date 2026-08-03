"""
資料庫連線模組。
只做一件事：建立並提供 Supabase client，不放任何業務邏輯，
避免以後這支檔案被塞進一堆不相干的東西。

⚠️ 內容跟原本獨立版本完全相同，這支沒有內部 import，不受掛載影響。
但注意：SUPABASE_URL / SUPABASE_KEY 這兩個環境變數，掛載後要設在
softglow 那個 Zeabur 服務裡（跟 DB_PATH、ADMIN_API_KEY 放在一起），
不是另外開一個服務設定。
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
