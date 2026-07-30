from __future__ import annotations

import uuid

from sqlalchemy import Column, DateTime, Integer, JSON, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base, GUID


class Assessment(Base):
    __tablename__ = "assessment"

    assessment_id = Column(GUID(), primary_key=True, default=uuid.uuid4)

    planner_id = Column(String(50), nullable=False, index=True)
    curriculum_id = Column(String(50), index=True)

    assessment_number = Column(Integer, nullable=False)
    version = Column(Integer, nullable=False, default=1)
    total_marks = Column(Integer, nullable=False)

    status = Column(String(50), nullable=False, default="Generated")

    grade = Column(String(30))
    course_name = Column(String(150))
    unit_name = Column(String(150))
    chapter_name = Column(String(200))

    learning_outcomes = Column(JSON, nullable=False, default=list)
    validation_report = Column(JSON, nullable=False, default=dict)

    publish_target = Column(String(500))
    publish_digest = Column(String(128))
    published_on = Column(DateTime)

    generated_by = Column(String(100))
    generated_on = Column(DateTime, server_default=func.now())
    updated_by = Column(String(100))
    updated_on = Column(DateTime, server_default=func.now(), onupdate=func.now())

    questions = relationship(
        "AssessmentQuestion",
        back_populates="assessment",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="AssessmentQuestion.question_number",
    )
