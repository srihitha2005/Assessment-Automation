from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from database import Base


class Assessment(Base):
    __tablename__ = "assessment"

    assessment_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    planner_id = Column(String(50), nullable=False, index=True)

    assessment_number = Column(Integer, nullable=False)

    version = Column(Integer, default=1)

    total_marks = Column(Integer, nullable=False)

    status = Column(String(50), nullable=False, default="Generated")

    curriculum_id = Column(String(50))

    grade = Column(String(30))

    course_name = Column(String(150))

    unit_name = Column(String(150))

    chapter_name = Column(String(200))

    learning_outcomes = Column(JSON, nullable=False, default=list)

    generated_by = Column(String(100))

    generated_on = Column(DateTime, server_default=func.now())

    updated_by = Column(String(100))

    updated_on = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    questions = relationship(
        "AssessmentQuestion",
        back_populates="assessment",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
