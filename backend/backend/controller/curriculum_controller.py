from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schema import ApiResponse, CurriculumRequest
from service.assessment_service import AssessmentService
from service.curriculum_service import CurriculumService


router = APIRouter(prefix="/api", tags=["Curriculum"])


def _curriculum(db: Session) -> CurriculumService:
    return CurriculumService(db, AssessmentService(db)._assessment_response)


@router.get("/grades", response_model=ApiResponse)
def list_grades(db: Session = Depends(get_db)):
    return ApiResponse(success=True, message="OK", data=_curriculum(db).list_grades())


@router.get("/grades/{grade_id}/courses", response_model=ApiResponse)
def list_courses(grade_id: int, db: Session = Depends(get_db)):
    return ApiResponse(success=True, message="OK", data=_curriculum(db).list_courses(grade_id))


@router.get("/courses/{course_id}/units", response_model=ApiResponse)
def list_units(course_id: int, db: Session = Depends(get_db)):
    return ApiResponse(success=True, message="OK", data=_curriculum(db).list_units(course_id))


@router.get("/units/{unit_id}/chapters", response_model=ApiResponse)
def list_chapters(unit_id: int, db: Session = Depends(get_db)):
    return ApiResponse(success=True, message="OK", data=_curriculum(db).list_chapters(unit_id))


@router.post("/curriculum", response_model=ApiResponse)
def resolve_curriculum(request: CurriculumRequest, db: Session = Depends(get_db)):
    resolved = _curriculum(db).resolve(
        request.grade_id, request.course_id, request.unit_id, request.chapter_id
    )
    return ApiResponse(success=True, message="OK", data=resolved)


@router.get("/curriculum/{curriculum_id}/assessments", response_model=ApiResponse)
def curriculum_assessments(curriculum_id: str, db: Session = Depends(get_db)):
    return ApiResponse(
        success=True, message="OK", data=_curriculum(db).curriculum_assessments(curriculum_id),
    )


@router.get("/planners", response_model=ApiResponse)
def list_planners(db: Session = Depends(get_db)):
    return ApiResponse(success=True, message="OK", data=_curriculum(db).list_planners())


@router.get("/planners/{planner_id}", response_model=ApiResponse)
def get_planner(planner_id: str, db: Session = Depends(get_db)):
    return ApiResponse(success=True, message="OK", data=_curriculum(db).get_planner(planner_id))
