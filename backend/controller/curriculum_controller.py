import logging
logger = logging.getLogger(__name__)

from fastapi import APIRouter
from service.curriculum_service import CurriculumService

router = APIRouter(
    prefix="/curriculum",
    tags=["Curriculum"]
)

service = CurriculumService()


# 1. Get All Grades
@router.get("/grades")
def get_all_grades():
    logger.info("[CurriculumController][get_all_grades] Entered")
    return service.get_all_grades()


# 2. Get Courses by Grade
@router.get("/grades/{grade_id}/courses")
def get_courses_by_grade(grade_id: int):
    logger.info(f"[CurriculumController][get_courses_by_grade] Entered with grade_id: {grade_id}")
    return service.get_courses_by_grade(grade_id)


# 3. Get Units by Course
@router.get("/courses/{course_id}/units")
def get_units_by_course(course_id: int):
    logger.info(f"[CurriculumController][get_units_by_course] Entered with course_id: {course_id}")
    return service.get_units_by_course(course_id)


# 4. Get Chapters by Unit
@router.get("/units/{unit_id}/chapters")
def get_chapters_by_unit(unit_id: int):
    logger.info(f"[CurriculumController][get_chapters_by_unit] Entered with unit_id: {unit_id}")
    return service.get_chapters_by_unit(unit_id)


# 5. Get Curriculum ID
@router.post("/id")
def get_curriculum_id(grade_id: int, course_id: int, unit_id: int, chapter_id: int):
    logger.info(f"[CurriculumController][get_curriculum_id] Entered with grade_id: {grade_id}, course_id: {course_id}, unit_id: {unit_id}, chapter_id: {chapter_id}")
    return service.get_curriculum_id(grade_id, course_id, unit_id, chapter_id)


# 6. Get Assessments
@router.get("/{curriculum_id}/assessments")
def get_assessments(curriculum_id: int):
    logger.info(f"[CurriculumController][get_assessments] Entered with curriculum_id: {curriculum_id}")
    return service.get_assessments(curriculum_id)