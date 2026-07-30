from fastapi import APIRouter

from service.curriculum_service import (
    get_all_grades as get_all_grades_service,
    get_courses_by_grade as get_courses_by_grade_service,
    get_units_by_course as get_units_by_course_service,
    get_chapters_by_unit as get_chapters_by_unit_service,
    get_curriculum_id as get_curriculum_id_service,
    get_assessments as get_assessments_service
)

router = APIRouter(
    prefix = "/curriculum",
    tags = ["Curriculum"]
)

# 1. Get all grades
@router.get("/grades")
def get_all_grades():
    return get_all_grades_service()

#2. Get all courses in a grade
@router.get("/grades/{grade_id}/courses")
def get_courses_by_grade(grade_id: int):
    return get_courses_by_grade_service(grade_id)

#3. Get all units in a course
@router.get("/courses/{course_id}/units")
def get_units_by_course(course_id: int):
    return get_units_by_course_service(course_id)

#4. Get all chapters in a unit
@router.get("/units/{unit_id}/chapters")
def get_chapters_by_unit(unit_id: int):
    return get_chapters_by_unit_service(unit_id)

#5. Get curriculum id
@router.post("/id")
def get_curriculum_id( grade_id: int, course_id: int, unit_id: int, chapter_id: int ):
    return get_curriculum_id_service(grade_id, course_id, unit_id, chapter_id)

#6. Get assesment for a curriculum
@router.get("/{curriculum_id}/assessments")
def get_assessments(curriculum_id: int):
    return get_assessments_service(curriculum_id)
