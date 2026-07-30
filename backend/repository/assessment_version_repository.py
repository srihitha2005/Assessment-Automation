from sqlalchemy.orm import Session
from uuid import UUID

from entity.assessment_version import AssessmentVersion


class AssessmentVersionRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, version: AssessmentVersion):
        self.db.add(version)
        self.db.commit()
        self.db.refresh(version)
        return version

    def get(self, assessment_id, version_number: int):
        if isinstance(assessment_id, str):
            assessment_id = UUID(assessment_id)
        return (
            self.db.query(AssessmentVersion)
            .filter(
                AssessmentVersion.assessment_id == assessment_id,
                AssessmentVersion.version == version_number,
            )
            .first()
        )

    def get_all(self, assessment_id):
        if isinstance(assessment_id, str):
            assessment_id = UUID(assessment_id)
        return (
            self.db.query(AssessmentVersion)
            .filter(AssessmentVersion.assessment_id == assessment_id)
            .order_by(AssessmentVersion.version.desc())
            .all()
        )

    def get_question_texts_for_planner(self, planner_id: str):
        """Return question text from immutable snapshots for duplicate avoidance."""
        # JSON filtering differs between PostgreSQL and SQLite. Filtering in Python
        # keeps local development and PostgreSQL behaviour identical.
        versions = self.db.query(AssessmentVersion).all()
        return {
            question["question"].strip().lower()
            for version in versions
            if version.snapshot.get("plannerId") == planner_id
            for question in version.snapshot.get("questions", [])
            if question.get("question")
        }
