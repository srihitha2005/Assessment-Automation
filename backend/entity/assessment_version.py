import uuid

from sqlalchemy import Column, DateTime, Integer, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from database import Base


class AssessmentVersion(Base):
    """Immutable snapshot created before an assessment is changed or regenerated."""

    __tablename__ = "assessment_version"

    version_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assessment_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    version = Column(Integer, nullable=False)
    action = Column(String(50), nullable=False)
    snapshot = Column(JSON, nullable=False)
    created_by = Column(String(100), nullable=False)
    created_on = Column(DateTime, server_default=func.now(), nullable=False)
