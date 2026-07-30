from __future__ import annotations

import uuid

from sqlalchemy import Column, DateTime, Integer, JSON, String
from sqlalchemy.sql import func

from database import Base, GUID


class AssessmentVersion(Base):
    """Append-only snapshot written before every mutation to an Assessment.

    Rollback re-materialises an assessment from one of these snapshots. The
    snapshot payload is the same dict the API returns, so it is safe to reuse
    on the wire and safe to persist across schema migrations that preserve
    JSON shape.
    """

    __tablename__ = "assessment_version"

    version_id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    assessment_id = Column(GUID(), nullable=False, index=True)
    version = Column(Integer, nullable=False)
    action = Column(String(50), nullable=False)
    snapshot = Column(JSON, nullable=False)
    created_by = Column(String(100), nullable=False)
    created_on = Column(DateTime, server_default=func.now(), nullable=False)
