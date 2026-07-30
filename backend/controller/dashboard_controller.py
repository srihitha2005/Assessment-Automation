from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schema import ApiResponse
from service.assessment_service import AssessmentService
from service.dashboard_service import DashboardService


router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/summary", response_model=ApiResponse)
def dashboard_summary(db: Session = Depends(get_db)):
    service = DashboardService(db, AssessmentService(db)._assessment_response)
    return ApiResponse(success=True, message="OK", data=service.summary())
