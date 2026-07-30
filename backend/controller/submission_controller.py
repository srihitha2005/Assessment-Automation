from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schema import ApiResponse, SubmissionCreate
from service.assessment_service import AssessmentService
from service.submission_service import SubmissionService


router = APIRouter(prefix="/api/assessments", tags=["Submission"])


def _service(db: Session) -> SubmissionService:
    assessment_service = AssessmentService(db)
    return SubmissionService(
        db, assessment_service._assessment_response, assessment_service._question_response,
    )


@router.post("/{assessment_id}/submissions", response_model=ApiResponse)
def create_submission(
    assessment_id: str, request: SubmissionCreate, db: Session = Depends(get_db),
):
    data = _service(db).create(assessment_id, request.model_dump(by_alias=False))
    return ApiResponse(success=True, message="Submission recorded.", data=data)


@router.get("/{assessment_id}/submissions", response_model=ApiResponse)
def list_submissions(assessment_id: str, db: Session = Depends(get_db)):
    return ApiResponse(success=True, message="OK", data=_service(db).list_for_assessment(assessment_id))
