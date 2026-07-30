from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from entity.assessment import Assessment
from entity.assessment_version import AssessmentVersion


def _as_uuid(value):
    return value if isinstance(value, UUID) else UUID(str(value))


class AssessmentVersionRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, version: AssessmentVersion) -> AssessmentVersion:
        self.db.add(version)
        self.db.commit()
        self.db.refresh(version)
        return version

    def get(self, assessment_id, version_number: int) -> AssessmentVersion | None:
        return (
            self.db.query(AssessmentVersion)
            .filter(
                AssessmentVersion.assessment_id == _as_uuid(assessment_id),
                AssessmentVersion.version == version_number,
            )
            .order_by(AssessmentVersion.created_on.desc())
            .first()
        )

    def get_all(self, assessment_id) -> list[AssessmentVersion]:
        return (
            self.db.query(AssessmentVersion)
            .filter(AssessmentVersion.assessment_id == _as_uuid(assessment_id))
            .order_by(AssessmentVersion.created_on.desc())
            .all()
        )

    def get_question_texts_for_planner(self, planner_id: str) -> set[str]:
        """Return normalised question text previously used for a planner.

        Scoped by planner_id via a join to `assessment`, so we scan only the
        versions that could contain repeats, not the entire history table.
        """
        rows = (
            self.db.query(AssessmentVersion)
            .join(Assessment, Assessment.assessment_id == AssessmentVersion.assessment_id)
            .filter(Assessment.planner_id == planner_id)
            .all()
        )
        seen: set[str] = set()
        for version in rows:
            for question in version.snapshot.get("questions", []) or []:
                text = (question.get("question") or "").strip().lower()
                if text:
                    seen.add(text)
        return seen
