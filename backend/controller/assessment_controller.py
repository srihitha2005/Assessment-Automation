import logging
logger = logging.getLogger(__name__)

from fastapi import APIRouter
from service.assessment_service import AssessmentService

router = APIRouter(
    prefix="/assessments",
    tags=["Assessment"]
)

service = AssessmentService()

# 7. Add Assessment
@router.post("")
def add_assessment(curriculum_id: int, prompt: str = ""):
    logger.info(f"[AssessmentController][add_assessment] Entered with curriculum_id: {curriculum_id}, prompt: {prompt}")
    return service.add_assessment(curriculum_id, prompt)


# 8. Delete Assessment
@router.delete("/{assessment_id}")
def delete_assessment(assessment_id: int):
    logger.info(f"[AssessmentController][delete_assessment] Entered with assessment_id: {assessment_id}")
    return service.delete_assessment(assessment_id)


# 9. View Assessment Details
@router.get("/{assessment_id}/details")
def get_assessment_details(assessment_id: int):
    logger.info(f"[AssessmentController][get_assessment_details] Entered with assessment_id: {assessment_id}")
    return service.get_assessment_details(assessment_id)


# 10. View Assessment
@router.get("/{assessment_id}")
def get_assessment(assessment_id: int):
    logger.info(f"[AssessmentController][get_assessment] Entered with assessment_id: {assessment_id}")
    return service.get_assessment(assessment_id)


# 11. Regenerate Assessment
@router.post("/{assessment_id}/regenerate")
def regenerate_assessment(assessment_id: int, prompt: str = ""):
    logger.info(f"[AssessmentController][regenerate_assessment] Entered with assessment_id: {assessment_id}, prompt: {prompt}")
    return service.regenerate_assessment(assessment_id, prompt)


# 12. Generate DOCX
@router.get("/{assessment_id}/docx")
def generate_docx(assessment_id: int):
    logger.info(f"[AssessmentController][generate_docx] Entered with assessment_id: {assessment_id}")
    return service.generate_docx(assessment_id)


# 13. Publish Assessment
@router.post("/{assessment_id}/publish")
def publish_assessment(assessment_id: int):
    logger.info(f"[AssessmentController][publish_assessment] Entered with assessment_id: {assessment_id}")
    return service.publish_assessment(assessment_id)


# 14. Rollback Assessment
@router.post("/{assessment_id}/rollback")
def rollback_assessment(assessment_id: int):
    logger.info(f"[AssessmentController][rollback_assessment] Entered with assessment_id: {assessment_id}")
    return service.rollback_assessment(assessment_id)


# 15. Generate More Questions
@router.post("/{assessment_id}/questions/generate")
def generate_more_questions(assessment_id: int):
    logger.info(f"[AssessmentController][generate_more_questions] Entered with assessment_id: {assessment_id}")
    return service.generate_more_questions(assessment_id)