from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid

from database import Base


class AssessmentQuestion(Base):

    __tablename__ = "assessment_question"

    question_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    assessment_id = Column(
        UUID(as_uuid=True),
        ForeignKey("assessment.assessment_id"),
        nullable=False
    )

    question_number = Column(Integer)

    question = Column(Text)

    answer = Column(Text)

    question_type = Column(String(50))

    difficulty = Column(String(20))

    bloom_level = Column(String(50))

    learning_outcome = Column(Text)

    marks = Column(Integer)

    image = Column(Text)

    images = Column(JSONB)

    generated_by = Column(String(100))

    generated_on = Column(DateTime, server_default=func.now())

    updated_by = Column(String(100))

    updated_on = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )