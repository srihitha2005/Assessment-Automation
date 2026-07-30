from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from entity.assessment_question import AssessmentQuestion


def _as_uuid(value):
    return value if isinstance(value, UUID) else UUID(str(value))


class AssessmentQuestionRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, question: AssessmentQuestion) -> AssessmentQuestion:
        self.db.add(question)
        self.db.commit()
        self.db.refresh(question)
        return question

    def save_all(self, questions: list[AssessmentQuestion]) -> None:
        self.db.add_all(questions)
        self.db.commit()

    def get_by_id(self, question_id) -> AssessmentQuestion | None:
        return (
            self.db.query(AssessmentQuestion)
            .filter(AssessmentQuestion.question_id == _as_uuid(question_id))
            .first()
        )

    def get_by_assessment(self, assessment_id) -> list[AssessmentQuestion]:
        return (
            self.db.query(AssessmentQuestion)
            .filter(AssessmentQuestion.assessment_id == _as_uuid(assessment_id))
            .order_by(AssessmentQuestion.question_number.asc())
            .all()
        )

    def delete_by_assessment(self, assessment_id) -> None:
        (
            self.db.query(AssessmentQuestion)
            .filter(AssessmentQuestion.assessment_id == _as_uuid(assessment_id))
            .delete(synchronize_session=False)
        )
        self.db.commit()

    def delete(self, question: AssessmentQuestion) -> None:
        self.db.delete(question)
        self.db.commit()
