from sqlalchemy.orm import Session

from entity.assessment_question import AssessmentQuestion


class AssessmentQuestionRepository:

    def __init__(self, db: Session):
        self.db = db

    def save_all(self, questions):

        self.db.add_all(questions)
        self.db.commit()

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