from fastapi import APIRouter

router = APIRouter(
    prefix = "/assessments",
    tags=["Assessment"]
)

#7. Add assessments
@router.post("")
def add_assessment( curriculum_id: int, prompt: str = "" ):
    return {
        "success": True,
        "message": "Assessment generated successfully."
    }

# 8. Delete assessment
@router.delete("/{assessment_id}")
def delete_assessment( assessment_id: int):
    return {
        "success": True,
        "message": "Assessment deleted successfully."
    }

# 9. View Assessment Details
@router.get("/{assessment_id}/details")
def get_assessment_details( assessment_id: int):
    return {
        "assessmentId": assessment_id,
        "assessmentNumber": 2,
        "version": 3,
        "generatedOn": "2026-07-30",
        "generatedBy": "SYSTEM",
        "updatedOn": "2026-07-30",
        "updatedBy": "SYSTEM",
        "marks": 50,
        "numberOfQuestions": 15,
        "learningOutcomes" : 23,
        "status" : "Generated"
    }

#10. View Assessment
@router.get("/{assessment_id}")
def get_assessment(assessment_id: int):
    return {
        "assessmentId": assessment_id,
        "questions": [
            {
                "questionId": 1001,
                "question": "What is digestion?",
                "answer": "The process of breaking down food.",
                "marks": 2
            },
            {
                "questionId": 1002,
                "question": "Name one digestive organ.",
                "answer": "Stomach",
                "marks": 1
            }
        ]
    }

#11. Regenarate Assessment
@router.post("/{assessment_id}/regenerate")
def regenerate_assessment( assessment_id: int, prompt: str = ""):
    return {
        "success": True,
        "message": "Assessment regenerated successfully."
    }

#12. Genrate Docs
@router.get("/{assessment_id}/docx")
def generate_docx( assessment_id: int):
    return {
        "success": True,
        "message": "DOCX generated successfully.",
        "downloadUrl": "/downloads/assessment.docx"
    }

#13. publish Assessment
@router.post("/{assessment_id}/publish")
def publish_assessment( assessment_id: int):
    return {
        "success": True,
        "message": "Assessment published successfully."
    }

#14. Rolback assessments
@router.post("/{assessment_id}/rollback")
def rollback_assessment(assessment_id: int):
    return {
        "success": True,
        "message": "Assessment rolled back successfully."
    }

#15. Generate More Questions
@router.post("/{assessment_id}/questions/generate")
def generate_more_questions( assessment_id: int):
    return {
        "success": True,
        "message": "Additional questions generated successfully."
    }
