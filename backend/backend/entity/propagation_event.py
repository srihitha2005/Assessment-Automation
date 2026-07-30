from __future__ import annotations

import uuid

from sqlalchemy import Column, DateTime, JSON, String
from sqlalchemy.sql import func

from database import Base, GUID


class PropagationEvent(Base):
    """Recorded whenever a planner's learning outcomes change.

    Downstream, `PropagationService` marks every assessment tied to the
    planner as `Outdated`, and the UI surfaces the diff so teachers can
    decide whether to regenerate.
    """

    __tablename__ = "propagation_event"

    event_id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    planner_id = Column(String(50), nullable=False, index=True)

    previous_outcomes = Column(JSON, nullable=False, default=list)
    new_outcomes = Column(JSON, nullable=False, default=list)
    added_outcomes = Column(JSON, nullable=False, default=list)
    removed_outcomes = Column(JSON, nullable=False, default=list)

    affected_assessment_ids = Column(JSON, nullable=False, default=list)
    resolution = Column(String(50), nullable=False, default="Pending")
    triggered_by = Column(String(100), nullable=False, default="SYSTEM")

    created_on = Column(DateTime, server_default=func.now(), nullable=False)
