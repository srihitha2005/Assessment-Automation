from sqlalchemy.orm import Session
from uuid import UUID

from entity.assessment_question import AssessmentQuestion


class AssessmentQuestionRepository:

    def __init__(self, db: Session):
        self.db = db

    def save_all(self, questions):

        self.db.add_all(questions)
        self.db.commit()

    def get_by_id(self, question_id):
        if isinstance(question_id, str):
            question_id = UUID(question_id)
        return (
            self.db.query(AssessmentQuestion)
            .filter(AssessmentQuestion.question_id == question_id)
            .first()
        )

    def save(self, question):
        self.db.add(question)
        self.db.commit()
        self.db.refresh(question)
        return question

    def get_by_assessment(self, assessment_id):

        return (
            self.db.query(AssessmentQuestion)
            .filter(
                AssessmentQuestion.assessment_id == assessment_id
            )
            .order_by(
                AssessmentQuestion.question_number
            )
            .all()
        )

    def delete_by_assessment(self, assessment_id):

        (
            self.db.query(AssessmentQuestion)
            .filter(
                AssessmentQuestion.assessment_id == assessment_id
            )
            .delete()
        )

        self.db.commit()

    def delete(self, question):
        self.db.delete(question)
        self.db.commit()
