from fastapi import APIRouter

from service.question_service import (
    get_question as get_question_service,
    delete_question as delete_question_service,
    edit_question as edit_question_service,
    regenerate_question as regenerate_question_service,
    regenerate_answer as regenerate_answer_service,
    rollback_question as rollback_question_service,
    upload_images as upload_images_service,
    delete_image as delete_image_service
)

router = APIRouter(
    prefix = "/questions",
    tags = ["Question"]
)

# 16.View Questions
@router.get("/{question_id}")
def get_question( question_id: int):
    return get_question_service(question_id)

#17. Delete Questions
@router.delete("/{question_id}")
def delete_question(question_id: int):
    return delete_question_service(question_id)

#18. Edit Questions
@router.put("/{question_id}")
def edit_question(question_id: int,question: str,answer: str):
    return edit_question_service(question_id, question, answer)

#19. Regenerate Question
@router.post("/{question_id}/regenerate")
def regenerate_question( question_id: int,prompt: str = ""):
    return regenerate_question_service(question_id, prompt)

#20. Regenerate Answer
@router.post("/{question_id}/answer/regenerate")
def regenerate_answer( question_id: int, prompt: str = ""):
    return regenerate_answer_service(question_id, prompt)

#21. Rollback Question
@router.post("/{question_id}/rollback")
def rollback_question( question_id: int):
    return rollback_question_service(question_id)

#22. Upload Images
@router.post("/{question_id}/images")
def upload_images(question_id: int):
    return upload_images_service(question_id)

#23. Delete image
@router.delete("/images/{image_id}")
def delete_image(image_id: int):
    return delete_image_service(image_id)
