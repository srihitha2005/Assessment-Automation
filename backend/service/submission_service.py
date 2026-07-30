"""Student submissions with hard-locked snapshots.

When a student submits, we freeze the current assessment view (questions +
metadata) into ``locked_snapshot``. Later edits to the live assessment only
touch its own row; the submission's snapshot is never mutated. This is what
the assignment PDF calls "hard-saving historical score data".
"""
from __future__ import annotations

from sqlalchemy.orm import Session

from entity.submission import Submission
from repository.assessment_question_repository import AssessmentQuestionRepository
from repository.assessment_repository import AssessmentRepository
from repository.submission_repository import SubmissionRepository


class SubmissionService:
    def __init__(self, db: Session, assessment_response, question_response):
        self.assessments = AssessmentRepository(db)
        self.questions = AssessmentQuestionRepository(db)
        self.submissions = SubmissionRepository(db)
        self._assessment_response = assessment_response
        self._question_response = question_response

    def create(self, assessment_id, data: dict) -> dict:
        assessment = self.assessments.get_by_id(assessment_id)
        if not assessment:
            raise LookupError("Assessment not found.")
        question_rows = self.questions.get_by_assessment(assessment.assessment_id)
        snapshot = {
            "assessment": self._assessment_response(assessment),
            "questions": [self._question_response(row) for row in question_rows],
        }
        max_score = sum(question.marks for question in question_rows)
        score = self._auto_score(question_rows, data.get("answers", []))
        submission = Submission(
            assessment_id=assessment.assessment_id,
            assessment_version=assessment.version,
            student_id=data["student_id"],
            student_name=data.get("student_name"),
            answers=data.get("answers", []),
            score=score,
            max_score=max_score,
            locked_snapshot=snapshot,
        )
        return self._to_dict(self.submissions.save(submission))

    def list_for_assessment(self, assessment_id) -> list[dict]:
        return [self._to_dict(item) for item in self.submissions.get_by_assessment(assessment_id)]

    @staticmethod
    def _auto_score(question_rows, answers) -> int:
        """Very simple auto-grading: exact-match on the answer field."""
        by_number = {answer.get("questionNumber"): answer.get("answer", "") for answer in answers}
        earned = 0
        for question in question_rows:
            given = str(by_number.get(question.question_number, "")).strip().lower()
            expected = str(question.answer or "").strip().lower()
            if given and given == expected:
                earned += question.marks
        return earned

    @staticmethod
    def _to_dict(submission: Submission) -> dict:
        return {
            "submissionId": str(submission.submission_id),
            "assessmentId": str(submission.assessment_id),
            "assessmentVersion": submission.assessment_version,
            "studentId": submission.student_id,
            "studentName": submission.student_name,
            "answers": submission.answers or [],
            "score": submission.score,
            "maxScore": submission.max_score,
            "submittedOn": submission.submitted_on.isoformat() if submission.submitted_on else None,
            "lockedSnapshot": submission.locked_snapshot,
        }
