import logging
logger = logging.getLogger(__name__)

from fastapi import APIRouter
from service.question_service import QuestionService

router = APIRouter(
    prefix="/questions",
    tags=["Question"]
)

service = QuestionService()


# 16. View Question
@router.get("/{question_id}")
def get_question(question_id: int):
    logger.info(f"[QuestionController][get_question] Entered with question_id: {question_id}")
    return service.get_question(question_id)


# 17. Delete Question
@router.delete("/{question_id}")
def delete_question(question_id: int):
    logger.info(f"[QuestionController][delete_question] Entered with question_id: {question_id}")
    return service.delete_question(question_id)


# 18. Edit Question
@router.put("/{question_id}")
def edit_question(question_id: int, question: str, answer: str):
    logger.info(f"[QuestionController][edit_question] Entered with question_id: {question_id}, question: {question}, answer: {answer}")
    return service.edit_question(question_id, question, answer)


# 19. Regenerate Question
@router.post("/{question_id}/regenerate")
def regenerate_question(question_id: int, prompt: str = ""):
    logger.info(f"[QuestionController][regenerate_question] Entered with question_id: {question_id}, prompt: {prompt}")
    return service.regenerate_question(question_id, prompt)


# 20. Regenerate Answer
@router.post("/{question_id}/answer/regenerate")
def regenerate_answer(question_id: int, prompt: str = ""):
    logger.info(f"[QuestionController][regenerate_answer] Entered with question_id: {question_id}, prompt: {prompt}")
    return service.regenerate_answer(question_id, prompt)


# 21. Rollback Question
@router.post("/{question_id}/rollback")
def rollback_question(question_id: int):
    logger.info(f"[QuestionController][rollback_question] Entered with question_id: {question_id}")
    return service.rollback_question(question_id)


# 22. Upload Images
@router.post("/{question_id}/images")
def upload_images(question_id: int):
    logger.info(f"[QuestionController][upload_images] Entered with question_id: {question_id}")
    return service.upload_images(question_id)


# 23. Delete Image
@router.delete("/images/{image_id}")
def delete_image(image_id: int):
    logger.info(f"[QuestionController][delete_image] Entered with image_id: {image_id}")
    return service.delete_image(image_id)