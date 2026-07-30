from __future__ import annotations

import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base, GUID


class AssessmentQuestion(Base):
    __tablename__ = "assessment_question"

    question_id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    assessment_id = Column(
        GUID(),
        ForeignKey("assessment.assessment_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    question_number = Column(Integer, nullable=False)
    version = Column(Integer, nullable=False, default=1)

    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    options = Column(JSON, nullable=False, default=list)

    question_type = Column(String(50), nullable=False)
    difficulty = Column(String(20), nullable=False)
    bloom_level = Column(String(50), nullable=False)

    learning_outcomes = Column(JSON, nullable=False, default=list)
    marks = Column(Integer, nullable=False, default=1)

    image = Column(Text)
    images = Column(JSON, nullable=False, default=list)

    needs_review = Column(Boolean, nullable=False, default=False)

    generated_by = Column(String(100))
    generated_on = Column(DateTime, server_default=func.now())
    updated_by = Column(String(100))
    updated_on = Column(DateTime, server_default=func.now(), onupdate=func.now())

    assessment = relationship("Assessment", back_populates="questions")
