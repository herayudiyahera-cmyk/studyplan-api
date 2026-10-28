
from fastapi import FastAPI

from app.routers.study_plan_router import router as study_plan_router

app = FastAPI(
    title="StudyPlan API",
    description="API untuk mengelola target dan progres belajar mahasiswa.",
    version="1.0.0",
)

app.include_router(study_plan_router)


@app.get("/")
def home():
    return {
        "message": "StudyPlan API berhasil dijalankan",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
