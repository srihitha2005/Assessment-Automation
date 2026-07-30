"""Track and react to planner learning-outcome changes.

When a planner is edited, we record the diff, mark every affected
assessment as ``Outdated``, and expose the event to the UI so teachers can
regenerate on their own timeline. The design keeps the responsibility for
regeneration explicit (auto-regenerating dozens of assessments in the
background would surprise users), but the notification is immediate.
"""
from __future__ import annotations

import logging

from sqlalchemy.orm import Session

from constants import (
    ASSESSMENT_STATUS_OUTDATED,
    ASSESSMENT_STATUS_PUBLISHED,
    ACTION_OUTCOMES_CHANGED,
)
from data.google_sheets import GoogleSheetsDataSource
from entity.propagation_event import PropagationEvent
from repository.assessment_repository import AssessmentRepository
from repository.propagation_event_repository import PropagationEventRepository

logger = logging.getLogger(__name__)


class PropagationService:
    def __init__(self, db: Session):
        self.db = db
        self.assessments = AssessmentRepository(db)
        self.events = PropagationEventRepository(db)
        self.sheets = GoogleSheetsDataSource()

    def update_planner_outcomes(self, planner_id: str, new_outcomes: list[str], user: str) -> dict:
        planner = self.sheets.get_planner(planner_id)
        if not planner:
            raise LookupError(f"Planner '{planner_id}' not found.")
        previous = list(planner.get("learningOutcomes") or [])
        added = [outcome for outcome in new_outcomes if outcome not in previous]
        removed = [outcome for outcome in previous if outcome not in new_outcomes]

        GoogleSheetsDataSource.override_planner_outcomes(planner_id, new_outcomes)

        affected = self.assessments.get_by_planner(planner_id)
        affected_ids: list[str] = []
        for assessment in affected:
            affected_ids.append(str(assessment.assessment_id))
            # Published assessments become "Outdated" (surface the drift);
            # everything else keeps its status but records the mismatch.
            if assessment.status == ASSESSMENT_STATUS_PUBLISHED:
                assessment.status = ASSESSMENT_STATUS_OUTDATED
                assessment.updated_by = user
                self.assessments.save(assessment)

        event = self.events.save(
            PropagationEvent(
                planner_id=planner_id,
                previous_outcomes=previous,
                new_outcomes=list(new_outcomes),
                added_outcomes=added,
                removed_outcomes=removed,
                affected_assessment_ids=affected_ids,
                resolution="Pending" if affected_ids else "NoAction",
                triggered_by=user,
            )
        )

        return {
            "eventId": str(event.event_id),
            "plannerId": planner_id,
            "action": ACTION_OUTCOMES_CHANGED,
            "previousOutcomes": previous,
            "newOutcomes": list(new_outcomes),
            "addedOutcomes": added,
            "removedOutcomes": removed,
            "affectedAssessmentIds": affected_ids,
            "resolution": event.resolution,
        }

    def list_events(self) -> list[dict]:
        return [self._to_dict(event) for event in self.events.get_all()]

    @staticmethod
    def _to_dict(event: PropagationEvent) -> dict:
        return {
            "eventId": str(event.event_id),
            "plannerId": event.planner_id,
            "previousOutcomes": event.previous_outcomes or [],
            "newOutcomes": event.new_outcomes or [],
            "addedOutcomes": event.added_outcomes or [],
            "removedOutcomes": event.removed_outcomes or [],
            "affectedAssessmentIds": event.affected_assessment_ids or [],
            "resolution": event.resolution,
            "triggeredBy": event.triggered_by,
            "createdOn": event.created_on.isoformat() if event.created_on else None,
        }
