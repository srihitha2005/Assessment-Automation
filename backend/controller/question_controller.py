from fastapi import APIRouter

router = APIRouter(
    prefix = "/questions",
    tags = ["Question"]
)

# 16.View Questions
@router.get("/{question_id}")
def get_question( question_id: int):
    return {
        "questionId": question_id,
        "questionNumber": 3,
        "question": "What is digestion?",
        "questionType": "MCQ",
        "options": [
            "Respiration",
            "Digestion",
            "Circulation",
            "Excretion"
        ],
        "answer": "Digestion",
        "marks": 2,
        "learningOutcome": "Explain the process of digestion.",
        "difficulty": "Medium",
        "bloomLevel": "Understand"
    }

#17. Delete Questions
@router.delete("/{question_id}")
def delete_question(question_id: int):
    return {
        "success": True,
        "message": "Question deleted successfully."
    }

#18. Edit Questions
@router.put("/{question_id}")
def edit_question(question_id: int,question: str,answer: str):
    return {
        "success": True,
        "message": "Question updated successfully."
    }

#19. Regenerate Question
@router.post("/{question_id}/regenerate")
def regenerate_question( question_id: int,prompt: str = ""):
    return {
        "success": True,
        "message": "Question regenerated successfully."
    }

#20. Regenerate Answer
@router.post("/{question_id}/answer/regenerate")
def regenerate_answer( question_id: int, prompt: str = ""):
    return {
        "success": True,
        "message": "Answer regenerated successfully."
    }

#21. Rollback Question
@router.post("/{question_id}/rollback")
def rollback_question( question_id: int):
    return {
        "success": True,
        "message": "Question rolled back successfully."
    }

#22. Upload Images
@router.post("/{question_id}/images")
def upload_images(question_id: int):
    return {
        "success": True,
        "message": "Image(s) uploaded successfully."
    }

#23. Delete image
@router.delete("/images/{image_id}")
def delete_image(image_id: int):
    return {
        "success": True,
        "message": "Image deleted successfully."
    }



