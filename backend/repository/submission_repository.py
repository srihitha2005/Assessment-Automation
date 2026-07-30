from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from entity.submission import Submission


def _as_uuid(value):
    return value if isinstance(value, UUID) else UUID(str(value))


class SubmissionRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, submission: Submission) -> Submission:
        self.db.add(submission)
        self.db.commit()
        self.db.refresh(submission)
        return submission

    def get_by_assessment(self, assessment_id) -> list[Submission]:
        return (
            self.db.query(Submission)
            .filter(Submission.assessment_id == _as_uuid(assessment_id))
            .order_by(Submission.submitted_on.desc())
            .all()
        )

    def count(self) -> int:
        return self.db.query(Submission).count()

    def all(self) -> list[Submission]:
        return self.db.query(Submission).order_by(Submission.submitted_on.desc()).all()
