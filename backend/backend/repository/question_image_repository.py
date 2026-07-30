from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from entity.question_image import QuestionImage


def _as_uuid(value):
    return value if isinstance(value, UUID) else UUID(str(value))


class QuestionImageRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, image: QuestionImage) -> QuestionImage:
        self.db.add(image)
        self.db.commit()
        self.db.refresh(image)
        return image

    def get_by_id(self, image_id) -> QuestionImage | None:
        return (
            self.db.query(QuestionImage)
            .filter(QuestionImage.image_id == _as_uuid(image_id))
            .first()
        )

    def get_by_question(self, question_id) -> list[QuestionImage]:
        return (
            self.db.query(QuestionImage)
            .filter(QuestionImage.question_id == _as_uuid(question_id))
            .order_by(QuestionImage.uploaded_on.asc())
            .all()
        )

    def delete(self, image: QuestionImage) -> None:
        self.db.delete(image)
        self.db.commit()
