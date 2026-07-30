from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from entity.assessment import Assessment


def _as_uuid(value):
    return value if isinstance(value, UUID) else UUID(str(value))


class AssessmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, assessment: Assessment) -> Assessment:
        self.db.add(assessment)
        self.db.commit()
        self.db.refresh(assessment)
        return assessment

    def get_by_id(self, assessment_id) -> Assessment | None:
        return (
            self.db.query(Assessment)
            .filter(Assessment.assessment_id == _as_uuid(assessment_id))
            .first()
        )

    def get_all(self) -> list[Assessment]:
        return (
            self.db.query(Assessment)
            .order_by(Assessment.generated_on.desc())
            .all()
        )

    def get_by_planner(self, planner_id: str) -> list[Assessment]:
        return (
            self.db.query(Assessment)
            .filter(Assessment.planner_id == planner_id)
            .order_by(Assessment.assessment_number.asc())
            .all()
        )

    def get_by_curriculum(self, curriculum_id: str) -> list[Assessment]:
        return (
            self.db.query(Assessment)
            .filter(Assessment.curriculum_id == curriculum_id)
            .order_by(Assessment.assessment_number.asc())
            .all()
        )

    def get_next_assessment_number(self, planner_id: str) -> int:
        latest = (
            self.db.query(Assessment)
            .filter(Assessment.planner_id == planner_id)
            .order_by(Assessment.assessment_number.desc())
            .first()
        )
        return 1 if latest is None else latest.assessment_number + 1

    def delete(self, assessment_id) -> None:
        assessment = self.get_by_id(assessment_id)
        if assessment:
            self.db.delete(assessment)
            self.db.commit()
