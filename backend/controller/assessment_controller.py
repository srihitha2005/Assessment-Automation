from fastapi import APIRouter

from service.assessment_api_service import (
    add_assessment as add_assessment_service,
    delete_assessment as delete_assessment_service,
    get_assessment_details as get_assessment_details_service,
    get_assessment as get_assessment_service,
    regenerate_assessment as regenerate_assessment_service,
    generate_docx as generate_docx_service,
    publish_assessment as publish_assessment_service,
    rollback_assessment as rollback_assessment_service,
    generate_more_questions as generate_more_questions_service
)

router = APIRouter(
    prefix = "/assessments",
    tags=["Assessment"]
)

#7. Add assessments
@router.post("")
def add_assessment( curriculum_id: int, prompt: str = "" ):
    return add_assessment_service(curriculum_id, prompt)

# 8. Delete assessment
@router.delete("/{assessment_id}")
def delete_assessment( assessment_id: int):
    return delete_assessment_service(assessment_id)

# 9. View Assessment Details
@router.get("/{assessment_id}/details")
def get_assessment_details( assessment_id: int):
    return get_assessment_details_service(assessment_id)

#10. View Assessment
@router.get("/{assessment_id}")
def get_assessment(assessment_id: int):
    return get_assessment_service(assessment_id)

#11. Regenarate Assessment
@router.post("/{assessment_id}/regenerate")
def regenerate_assessment( assessment_id: int, prompt: str = ""):
    return regenerate_assessment_service(assessment_id, prompt)

#12. Genrate Docs
@router.get("/{assessment_id}/docx")
def generate_docx( assessment_id: int):
    return generate_docx_service(assessment_id)

#13. publish Assessment
@router.post("/{assessment_id}/publish")
def publish_assessment( assessment_id: int):
    return publish_assessment_service(assessment_id)

#14. Rolback assessments
@router.post("/{assessment_id}/rollback")
def rollback_assessment(assessment_id: int):
    return rollback_assessment_service(assessment_id)

#15. Generate More Questions
@router.post("/{assessment_id}/questions/generate")
def generate_more_questions( assessment_id: int):
    return generate_more_questions_service(assessment_id)
