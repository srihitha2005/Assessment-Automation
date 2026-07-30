from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schema import ApiResponse, PlannerOutcomesUpdate
from service.propagation_service import PropagationService


router = APIRouter(prefix="/api", tags=["Propagation"])


@router.post("/planners/{planner_id}/outcomes", response_model=ApiResponse)
def update_planner_outcomes(
    planner_id: str, request: PlannerOutcomesUpdate, db: Session = Depends(get_db),
):
    data = PropagationService(db).update_planner_outcomes(
        planner_id, request.learning_outcomes, request.updated_by,
    )
    return ApiResponse(success=True, message="Planner outcomes updated.", data=data)


@router.get("/propagation/events", response_model=ApiResponse)
def list_events(db: Session = Depends(get_db)):
    return ApiResponse(success=True, message="OK", data=PropagationService(db).list_events())
