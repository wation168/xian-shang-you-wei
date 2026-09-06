"""
主程式進入點。
故意保持精簡——只做「建立 app、掛路由、設定 CORS」，
不要在這裡寫任何業務邏輯，避免這支檔案越長越大。
之後要加新功能，就去 routers/ 底下新增一支檔案，再到這裡掛進來一行就好。
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from routers import subjects, curriculum, exam_sessions

load_dotenv()

app = FastAPI(title="學測評量系統 API")

allowed_origins = os.environ.get("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(subjects.router)
app.include_router(curriculum.router)
app.include_router(exam_sessions.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
