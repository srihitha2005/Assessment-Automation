from __future__ import annotations

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from database import get_db
from schema import ApiResponse, QuestionPatch, RegenerateRequest
from service.assessment_service import AssessmentService
from service.image_service import ImageService


router = APIRouter(prefix="/api", tags=["Question"])


def _service(db: Session) -> AssessmentService:
    return AssessmentService(db)


@router.get("/questions/{question_id}", response_model=ApiResponse)
def get_question(question_id: str, db: Session = Depends(get_db)):
    return ApiResponse(success=True, message="OK", data=_service(db).get_question(question_id))


@router.put("/questions/{question_id}", response_model=ApiResponse)
def update_question(question_id: str, request: QuestionPatch, db: Session = Depends(get_db)):
    payload = request.model_dump(by_alias=False, exclude_none=True)
    payload["updated_by"] = request.updated_by
    data = _service(db).update_question(question_id, payload)
    return ApiResponse(success=True, message="Question updated.", data=data)


@router.delete("/questions/{question_id}", response_model=ApiResponse)
def delete_question(question_id: str, db: Session = Depends(get_db)):
    _service(db).delete_question(question_id)
    return ApiResponse(success=True, message="Question deleted.")


@router.post("/questions/{question_id}/regenerate", response_model=ApiResponse)
def regenerate_question(
    question_id: str, request: RegenerateRequest, db: Session = Depends(get_db),
):
    data = _service(db).regenerate_question(question_id, request.prompt, request.updated_by)
    return ApiResponse(success=True, message="Question regenerated.", data=data)


@router.post("/questions/{question_id}/answer/regenerate", response_model=ApiResponse)
def regenerate_answer(
    question_id: str, request: RegenerateRequest, db: Session = Depends(get_db),
):
    data = _service(db).regenerate_answer(question_id, request.prompt, request.updated_by)
    return ApiResponse(success=True, message="Answer regenerated.", data=data)


@router.post("/questions/{question_id}/images", response_model=ApiResponse)
def upload_images(
    question_id: str,
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db),
):
    service = ImageService(db)
    uploaded = [service.upload(question_id, file.filename, file.file, "SYSTEM") for file in files]
    return ApiResponse(success=True, message=f"Uploaded {len(uploaded)} image(s).", data=uploaded)


@router.delete("/images/{image_id}", response_model=ApiResponse)
def delete_image(image_id: str, db: Session = Depends(get_db)):
    ImageService(db).delete(image_id)
    return ApiResponse(success=True, message="Image deleted.")
