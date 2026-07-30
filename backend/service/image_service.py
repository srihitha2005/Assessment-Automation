"""Upload and manage question images.

Files are written under ``settings.uploaded_image_root`` and served via a
static mount at ``/uploads`` (see ``main.py``). Metadata is persisted so
images can be deleted individually and DOCX/PDF export can embed them.
"""
from __future__ import annotations

import logging
import mimetypes
import uuid
from pathlib import Path
from typing import IO

from PIL import Image

from config import settings
from entity.question_image import QuestionImage
from repository.assessment_question_repository import AssessmentQuestionRepository
from repository.question_image_repository import QuestionImageRepository

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
MAX_DIMENSION = 1200


class ImageService:
    def __init__(self, db):
        self.db = db
        self.questions = AssessmentQuestionRepository(db)
        self.images = QuestionImageRepository(db)
        settings.uploaded_image_root.mkdir(parents=True, exist_ok=True)

    def upload(self, question_id, file_name: str, stream: IO[bytes], user: str) -> dict:
        question = self.questions.get_by_id(question_id)
        if not question:
            raise LookupError("Question not found.")

        extension = Path(file_name).suffix.lower()
        if extension not in ALLOWED_EXTENSIONS:
            raise ValueError(f"Unsupported image type '{extension}'.")

        safe_name = f"{uuid.uuid4().hex}{extension}"
        target = settings.uploaded_image_root / safe_name
        target.write_bytes(stream.read())

        try:
            with Image.open(target) as im:
                im.thumbnail((MAX_DIMENSION, MAX_DIMENSION))
                im.save(target)
        except Exception:
            logger.exception("Could not downscale %s", target)

        mime_type, _ = mimetypes.guess_type(target.name)
        record = QuestionImage(
            question_id=question.question_id,
            file_name=file_name,
            file_path=target.as_posix(),
            mime_type=mime_type,
            size_bytes=target.stat().st_size,
            uploaded_by=user,
        )
        saved = self.images.save(record)

        # Also update the question's own image list for legacy consumers.
        question.images = (question.images or []) + [
            {"imageId": str(saved.image_id), "url": f"/uploads/{safe_name}"}
        ]
        if not question.image:
            question.image = f"/uploads/{safe_name}"
        question.updated_by = user
        self.questions.save(question)

        return {
            "imageId": str(saved.image_id),
            "questionId": str(saved.question_id),
            "fileName": saved.file_name,
            "url": f"/uploads/{safe_name}",
            "mimeType": saved.mime_type,
            "sizeBytes": saved.size_bytes,
        }

    def delete(self, image_id) -> None:
        image = self.images.get_by_id(image_id)
        if not image:
            raise LookupError("Image not found.")
        Path(image.file_path).unlink(missing_ok=True)
        question = self.questions.get_by_id(image.question_id)
        if question:
            url = f"/uploads/{Path(image.file_path).name}"
            question.images = [item for item in (question.images or []) if item.get("imageId") != str(image.image_id)]
            if question.image == url:
                question.image = question.images[0]["url"] if question.images else None
            self.questions.save(question)
        self.images.delete(image)
