from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
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

    planner_id = Column(Integer, nullable=False)

    assessment_number = Column(Integer, nullable=False)

    version = Column(Integer, default=1)

    total_marks = Column(Integer, nullable=False)

    generated_by = Column(String(100))

    generated_on = Column(DateTime, server_default=func.now())

    updated_by = Column(String(100))

    updated_on = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )