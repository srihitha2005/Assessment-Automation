"""FastAPI entry point."""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from config import settings
from controller.assessment_controller import router as assessment_router
from controller.curriculum_controller import router as curriculum_router
from controller.dashboard_controller import router as dashboard_router
from controller.propagation_controller import router as propagation_router
from controller.question_controller import router as question_router
from controller.submission_controller import router as submission_router
from data.question_bank_index import QuestionBankIndex
from database import init_db


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(name)s  %(message)s",
)
logger = logging.getLogger(__name__)


# Init happens eagerly so the app is usable even under test clients that
# skip lifespan events. The lifespan below still runs demo bootstrapping.
settings.generated_document_root.mkdir(parents=True, exist_ok=True)
settings.uploaded_image_root.mkdir(parents=True, exist_ok=True)
init_db()
QuestionBankIndex.refresh()


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.bootstrap_demo_data:
        _bootstrap_demo()
    yield


def _bootstrap_demo() -> None:
    """Seed one sample assessment on first boot so the UI has something to render."""
    from database import SessionLocal
    from service.assessment_service import AssessmentService

    session = SessionLocal()
    try:
        service = AssessmentService(session)
        if service.get_all():
            return
        try:
            service.generate(planner_id="P004", generated_by="BOOTSTRAP")
            logger.info("Bootstrapped demo assessment for planner P004.")
        except Exception:
            logger.exception("Bootstrap generation failed; the API will still start.")
    finally:
        session.close()


app = FastAPI(
    title="Assessment Automation API",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin] if settings.frontend_origin != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(LookupError)
async def not_found_handler(_: Request, exc: LookupError):
    return JSONResponse(status_code=404, content={"success": False, "message": str(exc), "data": None})


@app.exception_handler(ValueError)
async def bad_request_handler(_: Request, exc: ValueError):
    return JSONResponse(status_code=400, content={"success": False, "message": str(exc), "data": None})


@app.exception_handler(RuntimeError)
async def upstream_handler(_: Request, exc: RuntimeError):
    return JSONResponse(status_code=502, content={"success": False, "message": str(exc), "data": None})


# Static mounts serve question-bank images and uploaded question images.
app.mount("/static", StaticFiles(directory=str(settings.question_bank_root)), name="static")
app.mount("/uploads", StaticFiles(directory=str(settings.uploaded_image_root)), name="uploads")
app.mount("/downloads", StaticFiles(directory=str(settings.generated_document_root)), name="downloads")


app.include_router(curriculum_router)
app.include_router(assessment_router)
app.include_router(question_router)
app.include_router(submission_router)
app.include_router(dashboard_router)
app.include_router(propagation_router)


@app.get("/")
def root():
    return {
        "success": True,
        "message": "Assessment automation backend running.",
        "data": {
            "version": app.version,
            "docs": "/docs",
            "api": settings.api_prefix,
        },
    }
