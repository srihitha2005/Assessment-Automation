"""Teacher analytics.

Aggregates assessment, submission, and propagation state into a compact
payload for the dashboard page. Called during publish so the teacher panel
updates atomically ("teacher dashboard synchronisation" stretch goal).
"""
from __future__ import annotations

from collections import Counter

from sqlalchemy.orm import Session

from constants import (
    ASSESSMENT_STATUS_GENERATED,
    ASSESSMENT_STATUS_OUTDATED,
    ASSESSMENT_STATUS_PARSED,
    ASSESSMENT_STATUS_PUBLISHED,
)
from repository.assessment_repository import AssessmentRepository
from repository.propagation_event_repository import PropagationEventRepository
from repository.submission_repository import SubmissionRepository


class DashboardService:
    def __init__(self, db: Session, assessment_response):
        self.assessments = AssessmentRepository(db)
        self.submissions = SubmissionRepository(db)
        self.events = PropagationEventRepository(db)
        self._assessment_response = assessment_response

    def summary(self) -> dict:
        all_assessments = self.assessments.get_all()
        statuses = Counter(item.status for item in all_assessments)
        published = [item for item in all_assessments if item.status == ASSESSMENT_STATUS_PUBLISHED]
        outdated = [item for item in all_assessments if item.status == ASSESSMENT_STATUS_OUTDATED]
        submissions = self.submissions.all()
        avg_marks = (
            round(sum(item.total_marks for item in all_assessments) / len(all_assessments), 1)
            if all_assessments
            else 0
        )
        recent = sorted(all_assessments, key=lambda item: item.generated_on or 0, reverse=True)[:5]
        return {
            "totals": {
                "assessments": len(all_assessments),
                "published": len(published),
                "outdated": len(outdated),
                "submissions": len(submissions),
                "propagationEvents": len(self.events.get_all()),
            },
            "statusBreakdown": {
                ASSESSMENT_STATUS_GENERATED: statuses.get(ASSESSMENT_STATUS_GENERATED, 0),
                ASSESSMENT_STATUS_PARSED: statuses.get(ASSESSMENT_STATUS_PARSED, 0),
                ASSESSMENT_STATUS_PUBLISHED: statuses.get(ASSESSMENT_STATUS_PUBLISHED, 0),
                ASSESSMENT_STATUS_OUTDATED: statuses.get(ASSESSMENT_STATUS_OUTDATED, 0),
            },
            "averageTotalMarks": avg_marks,
            "recentAssessments": [self._assessment_response(item) for item in recent],
            "recentSubmissions": [
                {
                    "submissionId": str(item.submission_id),
                    "assessmentId": str(item.assessment_id),
                    "studentId": item.student_id,
                    "studentName": item.student_name,
                    "score": item.score,
                    "maxScore": item.max_score,
                    "submittedOn": item.submitted_on.isoformat() if item.submitted_on else None,
                }
                for item in submissions[:5]
            ],
        }
