from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from database import get_db
from schema import (
    ApiResponse,
    GenerateAssessmentRequest,
    PublishRequest,
    QuestionInput,
    RegenerateRequest,
    RollbackRequest,
)
from service.assessment_service import AssessmentService


router = APIRouter(prefix="/api/assessments", tags=["Assessment"])


def _service(db: Session) -> AssessmentService:
    return AssessmentService(db)


@router.get("", response_model=ApiResponse)
def list_assessments(db: Session = Depends(get_db)):
    data = _service(db).get_all()
    return ApiResponse(success=True, message="OK", data=data)


@router.post("", response_model=ApiResponse)
def generate_assessment(request: GenerateAssessmentRequest, db: Session = Depends(get_db)):
    data = _service(db).generate(
        planner_id=request.planner_id,
        curriculum_id=request.curriculum_id,
        teacher_prompt=request.prompt,
        generated_by=request.generated_by,
    )
    return ApiResponse(success=True, message="Assessment generated.", data=data)


@router.get("/{assessment_id}", response_model=ApiResponse)
def get_assessment(assessment_id: str, db: Session = Depends(get_db)):
    data = _service(db).get_by_id(assessment_id)
    if not data:
        raise LookupError("Assessment not found.")
    return ApiResponse(success=True, message="OK", data=data)


@router.get("/{assessment_id}/details", response_model=ApiResponse)
def assessment_details(assessment_id: str, db: Session = Depends(get_db)):
    return get_assessment(assessment_id, db)


@router.get("/{assessment_id}/questions", response_model=ApiResponse)
def assessment_questions(assessment_id: str, db: Session = Depends(get_db)):
    return ApiResponse(success=True, message="OK", data=_service(db).get_questions(assessment_id))


@router.post("/{assessment_id}/regenerate", response_model=ApiResponse)
def regenerate_assessment(
    assessment_id: str, request: RegenerateRequest, db: Session = Depends(get_db),
):
    data = _service(db).regenerate(assessment_id, request.prompt, request.updated_by)
    return ApiResponse(success=True, message="Assessment regenerated.", data=data)


@router.delete("/{assessment_id}", response_model=ApiResponse)
def delete_assessment(assessment_id: str, db: Session = Depends(get_db)):
    _service(db).delete(assessment_id)
    return ApiResponse(success=True, message="Assessment deleted.")


@router.get("/{assessment_id}/docx")
def download_docx(assessment_id: str, db: Session = Depends(get_db)):
    path = _service(db).create_docx(assessment_id)
    return FileResponse(
        path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=path.name,
    )


@router.get("/{assessment_id}/pdf")
def download_pdf(assessment_id: str, db: Session = Depends(get_db)):
    path = _service(db).create_pdf(assessment_id)
    return FileResponse(path, media_type="application/pdf", filename=path.name)


@router.post("/{assessment_id}/parse", response_model=ApiResponse)
def parse_assessment(assessment_id: str, db: Session = Depends(get_db)):
    data = _service(db).parse(assessment_id)
    return ApiResponse(success=True, message="Assessment parsed.", data=data)


@router.post("/{assessment_id}/publish", response_model=ApiResponse)
def publish_assessment(
    assessment_id: str, request: PublishRequest = PublishRequest(), db: Session = Depends(get_db),
):
    data = _service(db).publish(assessment_id, request.updated_by)
    return ApiResponse(success=True, message="Assessment published.", data=data)


@router.post("/{assessment_id}/rollback", response_model=ApiResponse)
def rollback_assessment(
    assessment_id: str, request: RollbackRequest, db: Session = Depends(get_db),
):
    data = _service(db).rollback(assessment_id, request.version, request.updated_by)
    return ApiResponse(success=True, message="Assessment rolled back.", data=data)


@router.get("/{assessment_id}/versions", response_model=ApiResponse)
def list_versions(assessment_id: str, db: Session = Depends(get_db)):
    return ApiResponse(success=True, message="OK", data=_service(db).list_versions(assessment_id))


@router.post("/{assessment_id}/questions", response_model=ApiResponse)
def add_question(assessment_id: str, request: QuestionInput, db: Session = Depends(get_db)):
    data = _service(db).add_question(assessment_id, request.model_dump(by_alias=False))
    return ApiResponse(success=True, message="Question added.", data=data)
