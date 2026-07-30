"""Curriculum + planner read APIs, backed by GoogleSheetsDataSource.

Kept intentionally read-only. Curriculum is the source of truth from the
sheet — the backend never writes back.
"""
from __future__ import annotations

from sqlalchemy.orm import Session

from data.google_sheets import GoogleSheetsDataSource
from repository.assessment_repository import AssessmentRepository


class CurriculumService:
    def __init__(self, db: Session, assessment_response):
        self.sheets = GoogleSheetsDataSource()
        self.assessments = AssessmentRepository(db)
        self._assessment_response = assessment_response

    # ---------------------------------------------------------------- grades

    def list_grades(self) -> dict:
        rows = self.sheets.get_curriculum()
        by_grade: dict[int, dict] = {}
        for row in rows:
            grade_id = row.get("gradeId") or 0
            grade = by_grade.setdefault(
                grade_id,
                {"gradeId": grade_id, "gradeName": row.get("grade", ""), "units": set(), "courses": set()},
            )
            grade["units"].add(row.get("unitId"))
            grade["courses"].add(row.get("courseId"))
        grades = [
            {
                "gradeId": grade["gradeId"],
                "gradeName": grade["gradeName"],
                "numberOfUnits": len(grade["units"]),
                "numberOfCourses": len(grade["courses"]),
            }
            for grade in sorted(by_grade.values(), key=lambda item: item["gradeId"])
        ]
        return {"totalGrades": len(grades), "grades": grades}

    # ---------------------------------------------------------------- courses

    def list_courses(self, grade_id: int) -> dict:
        rows = [row for row in self.sheets.get_curriculum() if row.get("gradeId") == grade_id]
        by_course: dict[int, dict] = {}
        for row in rows:
            course_id = row.get("courseId") or 0
            by_course.setdefault(
                course_id,
                {"courseId": course_id, "courseName": row.get("courseName", ""), "units": set()},
            )["units"].add(row.get("unitId"))
        courses = [
            {
                "courseId": course["courseId"],
                "courseName": course["courseName"],
                "numberOfUnits": len(course["units"]),
            }
            for course in sorted(by_course.values(), key=lambda item: item["courseId"])
        ]
        return {"gradeId": grade_id, "numberOfCourses": len(courses), "courses": courses}

    # ---------------------------------------------------------------- units

    def list_units(self, course_id: int) -> dict:
        rows = [row for row in self.sheets.get_curriculum() if row.get("courseId") == course_id]
        by_unit: dict[int, dict] = {}
        for row in rows:
            unit_id = row.get("unitId") or 0
            by_unit.setdefault(
                unit_id,
                {"unitId": unit_id, "unitName": row.get("unitName", ""), "chapters": set()},
            )["chapters"].add(row.get("chapterId"))
        units = [
            {
                "unitId": unit["unitId"],
                "unitName": unit["unitName"],
                "numberOfChapters": len(unit["chapters"]),
            }
            for unit in sorted(by_unit.values(), key=lambda item: item["unitId"])
        ]
        return {"courseId": course_id, "numberOfUnits": len(units), "units": units}

    # -------------------------------------------------------------- chapters

    def list_chapters(self, unit_id: int) -> dict:
        rows = [row for row in self.sheets.get_curriculum() if row.get("unitId") == unit_id]
        chapters = []
        for row in rows:
            assessments = self.assessments.get_by_curriculum(row.get("curriculumId"))
            chapters.append(
                {
                    "chapterId": row.get("chapterId"),
                    "chapterName": row.get("chapterName"),
                    "curriculumId": row.get("curriculumId"),
                    "numberOfAssessments": len(assessments),
                }
            )
        chapters.sort(key=lambda item: item["chapterId"])
        return {"unitId": unit_id, "numberOfChapters": len(chapters), "chapters": chapters}

    # ---------------------------------------------------- resolve curriculum

    def resolve(self, grade_id: int, course_id: int, unit_id: int, chapter_id: int) -> dict:
        match = next(
            (
                row
                for row in self.sheets.get_curriculum()
                if row.get("gradeId") == grade_id
                and row.get("courseId") == course_id
                and row.get("unitId") == unit_id
                and row.get("chapterId") == chapter_id
            ),
            None,
        )
        if not match:
            raise LookupError("No curriculum matches this grade/course/unit/chapter combination.")
        return {"curriculumId": match["curriculumId"], "chapterName": match["chapterName"]}

    # ------------------------------------------------ curriculum assessments

    def curriculum_assessments(self, curriculum_id: str) -> dict:
        curriculum_row = next(
            (row for row in self.sheets.get_curriculum() if row.get("curriculumId") == curriculum_id),
            None,
        )
        if not curriculum_row:
            raise LookupError(f"Curriculum '{curriculum_id}' not found.")
        planner = next(
            (item for item in self.sheets.get_planners() if item["curriculumId"] == curriculum_id),
            None,
        )
        assessments = self.assessments.get_by_curriculum(curriculum_id)
        return {
            "curriculumId": curriculum_id,
            "chapterName": curriculum_row["chapterName"],
            "grade": curriculum_row["grade"],
            "planner": planner,
            "learningOutcomes": planner["learningOutcomes"] if planner else [],
            "numberOfAssessments": len(assessments),
            "assessments": [self._assessment_response(item) for item in assessments],
        }

    # ----------------------------------------------------------- planners

    def list_planners(self) -> dict:
        curriculum_by_id = {row["curriculumId"]: row for row in self.sheets.get_curriculum()}
        planners = []
        for planner in self.sheets.get_planners():
            curriculum = curriculum_by_id.get(planner["curriculumId"], {})
            assessments = self.assessments.get_by_planner(planner["plannerId"])
            planners.append(
                {
                    **planner,
                    "grade": curriculum.get("grade"),
                    "courseName": curriculum.get("courseName"),
                    "unitName": curriculum.get("unitName"),
                    "chapterName": curriculum.get("chapterName"),
                    "numberOfAssessments": len(assessments),
                }
            )
        return {"totalPlanners": len(planners), "planners": planners}

    def get_planner(self, planner_id: str) -> dict:
        planner = self.sheets.get_planner_context(planner_id)
        if not planner:
            raise LookupError(f"Planner '{planner_id}' not found.")
        assessments = self.assessments.get_by_planner(planner_id)
        return {
            **planner,
            "assessments": [self._assessment_response(item) for item in assessments],
        }
