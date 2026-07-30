from fastapi import FastAPI

from controller.curriculum_controller import router as curriculum_router
from controller.assessment_controller import router as assessment_router
from controller.question_controller import router as question_router

app = FastAPI(
    title = "Assessment Automation API",
    version = "1.0.0"
)

app.include_router(curriculum_router)
app.include_router(assessment_router)
app.include_router(question_router)

@app.get("/")
def root():
    return {
        "message": "Assessment automation backend is running."
    }
