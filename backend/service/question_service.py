# Question service - returns dummy data for controller endpoints


def get_question(question_id: int):
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
        "bloomLevel": "Understand",
        "version": "v3",
        "lastModifiedAt": "28 July 2026 05:45 PM",
        "lastModifiedBy": "John Doe"
    }


def delete_question(question_id: int):
    return {
        "success": True,
        "message": "Question deleted successfully."
    }


def edit_question(question_id: int, question: str, answer: str):
    return {
        "success": True,
        "message": "Question updated successfully."
    }


def regenerate_question(question_id: int, prompt: str = ""):
    return {
        "success": True,
        "message": "Question regenerated successfully."
    }


def regenerate_answer(question_id: int, prompt: str = ""):
    return {
        "success": True,
        "message": "Answer regenerated successfully."
    }


def rollback_question(question_id: int):
    return {
        "success": True,
        "message": "Question rolled back successfully."
    }


def upload_images(question_id: int):
    return {
        "success": True,
        "message": "Image(s) uploaded successfully."
    }


def delete_image(image_id: int):
    return {
        "success": True,
        "message": "Image deleted successfully."
    }
