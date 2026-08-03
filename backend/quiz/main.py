"""
學測評量系統 — 子服務進入點。

⚠️ 這支已經是「被 softglow main.py 用 app.mount('/quiz-api', ...) 掛載」版本，
跟原本獨立運作時的版本有兩個差異，已在下面標註：
  1. import 改成相對路徑（因為現在是 backend/quiz/ package，不是獨立專案根目錄）
  2. 拿掉了自己的 CORSMiddleware（外層 softglow main.py 已經處理過 CORS，
     子服務不需要再管一次；如果之後真的切成獨立服務，把這段加回來即可）

故意保持精簡——只做「建立 app、掛路由」，不放業務邏輯。
"""
from fastapi import FastAPI

from .routers import subjects, curriculum, exam_sessions, exam_practice

app = FastAPI(title="學測評量系統 API")

app.include_router(subjects.router)
app.include_router(curriculum.router)
app.include_router(exam_sessions.router)
app.include_router(exam_practice.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
