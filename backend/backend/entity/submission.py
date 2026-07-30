from __future__ import annotations

import uuid

from sqlalchemy import Column, DateTime, Integer, JSON, String
from sqlalchemy.sql import func

from database import Base, GUID


class Submission(Base):
    """Student attempt against a specific assessment version.

    `locked_snapshot` captures the assessment (questions + metadata) as it
    existed at submission time. Later edits to the live assessment increment
    its `version` but must never mutate this row — this is what the PDF calls
    "hard-saving historical score data".
    """

    __tablename__ = "submission"

    submission_id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    assessment_id = Column(GUID(), nullable=False, index=True)
    assessment_version = Column(Integer, nullable=False)

    student_id = Column(String(100), nullable=False, index=True)
    student_name = Column(String(200))

    answers = Column(JSON, nullable=False, default=list)
    score = Column(Integer)
    max_score = Column(Integer)

    locked_snapshot = Column(JSON, nullable=False)

    submitted_on = Column(DateTime, server_default=func.now(), nullable=False)
