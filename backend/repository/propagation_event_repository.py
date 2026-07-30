from __future__ import annotations

from sqlalchemy.orm import Session

from entity.propagation_event import PropagationEvent


class PropagationEventRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, event: PropagationEvent) -> PropagationEvent:
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event

    def get_all(self) -> list[PropagationEvent]:
        return (
            self.db.query(PropagationEvent)
            .order_by(PropagationEvent.created_on.desc())
            .all()
        )

    def get_by_planner(self, planner_id: str) -> list[PropagationEvent]:
        return (
            self.db.query(PropagationEvent)
            .filter(PropagationEvent.planner_id == planner_id)
            .order_by(PropagationEvent.created_on.desc())
            .all()
        )
