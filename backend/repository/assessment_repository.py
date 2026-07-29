from sqlalchemy.orm import Session

from entity.assessment import Assessment


class AssessmentRepository:

    def __init__(self, db: Session):
        self.db = db

    def save(self, assessment: Assessment):

        self.db.add(assessment)
        self.db.commit()
        self.db.refresh(assessment)

        return assessment

    def get_by_id(self, assessment_id):

        return (
            self.db.query(Assessment)
            .filter(
                Assessment.assessment_id == assessment_id
            )
            .first()
        )

    def get_latest_by_planner(self, planner_id):

        return (
            self.db.query(Assessment)
            .filter(
                Assessment.planner_id == planner_id
            )
            .order_by(
                Assessment.assessment_number.desc()
            )
            .first()
        )

    def delete(self, assessment_id):

        assessment = self.get_by_id(assessment_id)

        if assessment:

            self.db.delete(assessment)
            self.db.commit()

    def get_next_assessment_number(self, planner_id):

        latest = self.get_latest_by_planner(planner_id)

        if latest is None:
            return 1

        return latest.assessment_number + 1