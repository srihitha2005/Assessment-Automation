# Assessment API service - returns dummy data for controller endpoints


def add_assessment(curriculum_id: int, prompt: str = ""):
    return {
        "success": True,
        "message": "Assessment generated successfully."
    }


def delete_assessment(assessment_id: int):
    return {
        "success": True,
        "message": "Assessment deleted successfully."
    }


def get_assessment_details(assessment_id: int):
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
        "learningOutcomes": 23,
        "status": "Generated"
    }


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


def regenerate_assessment(assessment_id: int, prompt: str = ""):
    return {
        "success": True,
        "message": "Assessment regenerated successfully."
    }


def generate_docx(assessment_id: int):
    return {
        "success": True,
        "message": "DOCX generated successfully.",
        "downloadUrl": "/downloads/assessment.docx"
    }


def publish_assessment(assessment_id: int):
    return {
        "success": True,
        "message": "Assessment published successfully."
    }


def rollback_assessment(assessment_id: int):
    return {
        "success": True,
        "message": "Assessment rolled back successfully."
    }


def generate_more_questions(assessment_id: int):
    return {
        "success": True,
        "message": "Additional questions generated successfully."
    }
