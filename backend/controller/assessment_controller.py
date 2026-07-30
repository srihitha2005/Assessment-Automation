import logging
import re
import shutil
from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from config import settings
from constants import DEFAULT_GENERATED_BY
from data.google_sheets import GoogleSheetsDataSource
from database import get_db
from schema import GenerateAssessmentRequest, QuestionInput, RegenerateQuestionRequest, RollbackRequest, UpdateAssessmentRequest
from service.assessment_service import AssessmentService
from service.document_service import DocumentService

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Assessment Automation"])


def service(db: Session = Depends(get_db)) -> AssessmentService:
    return AssessmentService(db)


def response(message: str, data=None):
    return {"success": True, "message": message, "data": data}


def not_found(message: str):
    raise HTTPException(status_code=404, detail=message)


@router.get("/health")
def health():
    return response("Assessment Automation API is running.", {"ollamaModel": settings.ollama_model})


@router.get("/curriculum")
def get_curriculum():
    return response("Curriculum loaded.", GoogleSheetsDataSource().get_curriculum())


@router.get("/planners")
def get_planners():
    return response("Planners loaded.", GoogleSheetsDataSource().get_planners())


@router.get("/assessments")
@router.get("/assessment/all")
def get_assessments(assessment_service: AssessmentService = Depends(service)):
    return response("Assessments loaded.", assessment_service.get_all())


@router.get("/assessments/{assessment_id}")
@router.get("/assessment/{assessment_id}")
def get_assessment(assessment_id: UUID, assessment_service: AssessmentService = Depends(service)):
    assessment = assessment_service.get_by_id(assessment_id)
    if not assessment:
        not_found("Assessment not found.")
    return response("Assessment loaded.", assessment)


@router.post("/assessments/generate")
@router.post("/assessment/generate")
def generate_assessment(request: GenerateAssessmentRequest, assessment_service: AssessmentService = Depends(service)):
    try:
        return response("Assessment generated successfully.", assessment_service.generate(request.planner_id, request.generated_by))
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error


@router.put("/assessments/{assessment_id}/regenerate")
@router.put("/assessment/{assessment_id}/re-generate")
def regenerate_assessment(assessment_id: UUID, request: UpdateAssessmentRequest, assessment_service: AssessmentService = Depends(service)):
    try:
        return response("Assessment regenerated successfully.", assessment_service.regenerate_assessment(assessment_id, request.updated_by))
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error


@router.put("/assessments/{assessment_id}")
@router.put("/assessment/{assessment_id}/update")
def update_assessment(assessment_id: UUID, request: UpdateAssessmentRequest, assessment_service: AssessmentService = Depends(service)):
    try:
        return response("Assessment updated successfully.", assessment_service.update_assessment(assessment_id, request.model_dump(exclude_none=True)))
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.delete("/assessments/{assessment_id}")
@router.delete("/assessment/{assessment_id}/delete")
def delete_assessment(assessment_id: UUID, assessment_service: AssessmentService = Depends(service)):
    try:
        assessment_service.delete_assessment(assessment_id)
        return response("Assessment deleted successfully.")
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.post("/assessments/{assessment_id}/publish")
@router.post("/assessment/{assessment_id}/publish")
def publish_assessment(assessment_id: UUID, request: UpdateAssessmentRequest, assessment_service: AssessmentService = Depends(service)):
    try:
        return response("Assessment published successfully.", assessment_service.publish(assessment_id, request.updated_by))
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except RuntimeError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error


@router.post("/assessments/{assessment_id}/parse")
@router.post("/assessment/{assessment_id}/parse")
def parse_assessment(assessment_id: UUID, assessment_service: AssessmentService = Depends(service)):
    try:
        return response("Assessment document parsed successfully.", assessment_service.parse_document(assessment_id))
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.get("/assessments/{assessment_id}/versions")
def get_versions(assessment_id: UUID, assessment_service: AssessmentService = Depends(service)):
    try:
        return response("Assessment versions loaded.", assessment_service.list_versions(assessment_id))
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.post("/assessments/{assessment_id}/rollback")
@router.post("/versions/assessment/{assessment_id}")
def rollback_assessment(assessment_id: UUID, request: RollbackRequest, assessment_service: AssessmentService = Depends(service)):
    try:
        return response("Assessment rolled back successfully.", assessment_service.rollback(assessment_id, request.version, request.updated_by))
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.get("/assessments/{assessment_id}/questions")
@router.get("/questions/assessment/{assessment_id}")
def get_questions(assessment_id: UUID, assessment_service: AssessmentService = Depends(service)):
    if not assessment_service.get_by_id(assessment_id):
        not_found("Assessment not found.")
    return response("Questions loaded.", assessment_service.get_questions(assessment_id))


@router.get("/questions/{question_id}")
def get_question(question_id: UUID, assessment_service: AssessmentService = Depends(service)):
    question = assessment_service.get_question(question_id)
    if not question:
        not_found("Question not found.")
    return response("Question loaded.", question)


@router.post("/assessments/{assessment_id}/questions")
@router.post("/questions/{assessment_id}/add")
def add_question(assessment_id: UUID, request: QuestionInput, assessment_service: AssessmentService = Depends(service)):
    try:
        return response("Question added successfully.", assessment_service.add_question(assessment_id, request.model_dump()))
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.put("/questions/{question_id}")
@router.put("/questions/{question_id}/update")
def update_question(question_id: UUID, request: QuestionInput, assessment_service: AssessmentService = Depends(service)):
    try:
        return response("Question updated successfully.", assessment_service.update_question(question_id, request.model_dump()))
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.delete("/questions/{question_id}")
@router.delete("/questions/{question_id}/delete")
def delete_question(question_id: UUID, assessment_service: AssessmentService = Depends(service)):
    try:
        assessment_service.delete_question(question_id)
        return response("Question deleted successfully.")
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.post("/questions/{question_id}/regenerate")
def regenerate_question(question_id: UUID, request: RegenerateQuestionRequest, assessment_service: AssessmentService = Depends(service)):
    try:
        return response("Question regenerated successfully.", assessment_service.regenerate_question(question_id, request.prompt, request.updated_by))
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error


@router.post("/questions/{question_id}/regenerate-answer")
def regenerate_answer(question_id: UUID, request: RegenerateQuestionRequest, assessment_service: AssessmentService = Depends(service)):
    try:
        return response("Answer regenerated successfully.", assessment_service.regenerate_answer(question_id, request.updated_by))
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error


@router.post("/documents/{assessment_id}/generate")
@router.post("/document/{assessment_id}/generate-document")
def generate_document(assessment_id: UUID, assessment_service: AssessmentService = Depends(service)):
    try:
        path = assessment_service.create_document(assessment_id)
        return response("Document generated successfully.", {"assessmentId": str(assessment_id), "documentName": path.name, "downloadUrl": f"/documents/{assessment_id}/download"})
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.get("/documents/{assessment_id}/download")
def download_document(assessment_id: UUID, assessment_service: AssessmentService = Depends(service)):
    try:
        path = assessment_service.create_document(assessment_id)
        return FileResponse(path, filename=path.name, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.post("/documents/parse")
async def parse_uploaded_document(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".docx"):
        raise HTTPException(status_code=422, detail="Only .docx files are currently supported.")
    settings.generated_document_root.mkdir(parents=True, exist_ok=True)
    safe_name = re.sub(r"[^A-Za-z0-9._-]", "_", file.filename)
    path = settings.generated_document_root / safe_name
    with path.open("wb") as target:
        shutil.copyfileobj(file.file, target)
    return response("Document parsed successfully.", DocumentService().parse_docx(path))


@router.post("/questions/{question_id}/images")
async def upload_image(question_id: UUID, file: UploadFile = File(...), assessment_service: AssessmentService = Depends(service)):
    question = assessment_service.get_question(question_id)
    if not question:
        not_found("Question not found.")
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in {".png", ".jpg", ".jpeg", ".webp"}:
        raise HTTPException(status_code=422, detail="Upload a PNG, JPG, JPEG, or WEBP image.")
    image_root = settings.question_bank_root / "images"
    image_root.mkdir(parents=True, exist_ok=True)
    file_name = f"{question_id}{suffix}"
    with (image_root / file_name).open("wb") as target:
        shutil.copyfileobj(file.file, target)
    data = {"images": [*question.get("images", []), f"images/{file_name}"], "updated_by": DEFAULT_GENERATED_BY}
    return response("Image uploaded successfully.", assessment_service.update_question(question_id, data))
