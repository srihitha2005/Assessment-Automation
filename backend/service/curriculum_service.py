import logging
from helper.google_sheet_helper import GoogleSheetHelper
from config.sheetsConfig import CURRICULUM_SHEET

logger = logging.getLogger(__name__)


class CurriculumService:
    def __init__(self):
        self.google_sheet_helper = GoogleSheetHelper()

    # 1. Get All Grades
    def get_all_grades(self):
        logger.info("[CurriculumService][get_all_grades] Entered")

        try:
            rows = self.google_sheet_helper.get_all_records(CURRICULUM_SHEET)
            logger.info(f"[CurriculumService][get_all_grades] Retrieved {len(rows)} records from Google Sheet")
            grades = {}
            for row in rows:
                grade = row["Grade"]
                course_id = row["Course_ID"]
                if grade not in grades:
                    grades[grade] = set()
                grades[grade].add(course_id)

            grade_list = []
            grade_id = 1
            for grade_name in sorted(grades.keys()):
                grade_list.append({
                    "gradeId": grade_id,
                    "gradeName": grade_name,
                    "numberOfUnits": len(grades[grade_name])
                })
                grade_id += 1

            logger.info(f"[CurriculumService][get_all_grades] Successfully prepared {len(grade_list)} grades")

            return {
                "totalGrades": len(grade_list),
                "grades": grade_list
            }

        except KeyError as e:
            logger.error(f"[CurriculumService][get_all_grades] Missing column in Google Sheet: {str(e)}")
            raise Exception(f"Missing column in Google Sheet: {str(e)}")

        except Exception as e:
            logger.exception("[CurriculumService][get_all_grades] Failed to fetch grades")
            raise Exception(f"Failed to fetch grades: {str(e)}")

    # 2. Get Courses by Grade
    def get_courses_by_grade(self, grade_id: int):
        logger.info(f"[CurriculumService][get_courses_by_grade] Entered with grade_id: {grade_id}")
        return {
            "gradeId": grade_id,
            "numberOfCourses": 2,
            "courses": [
                {
                    "courseId": 101,
                    "courseName": "Science",
                    "numberOfUnits": 5
                },
                {
                    "courseId": 102,
                    "courseName": "Mathematics",
                    "numberOfUnits": 4
                }
            ]
        }


    # 3. Get Units by Course
    def get_units_by_course(self, course_id: int):
        logger.info(f"[CurriculumService][get_units_by_course] Entered with course_id: {course_id}")
        return {
            "courseId": course_id,
            "numberOfUnits": 3,
            "units": [
                {
                    "unitId": 11,
                    "unitName": "Human Body",
                    "numberOfChapters": 6
                },
                {
                    "unitId": 12,
                    "unitName": "Plants",
                    "numberOfChapters": 5
                },
                {
                    "unitId": 13,
                    "unitName": "Matter",
                    "numberOfChapters": 4
                }
            ]
        }


    # 4. Get Chapters by Unit
    def get_chapters_by_unit(self, unit_id: int):
        logger.info(f"[CurriculumService][get_chapters_by_unit] Entered with unit_id: {unit_id}")
        return {
            "unitId": unit_id,
            "numberOfChapters": 2,
            "chapters": [
                {
                    "chapterId": 101,
                    "chapterName": "Digestive System",
                    "numberOfAssessments": 3
                },
                {
                    "chapterId": 102,
                    "chapterName": "Respiratory System",
                    "numberOfAssessments": 2
                }
            ]
        }


    # 5. Get Curriculum ID
    def get_curriculum_id(self, grade_id: int, course_id: int, unit_id: int, chapter_id: int):
        logger.info(f"[CurriculumService][get_curriculum_id] Entered with grade_id: {grade_id}, course_id: {course_id}, unit_id: {unit_id}, chapter_id: {chapter_id}")
        return {
            "curriculumId": 55
        }


    # 6. Get Assessments
    def get_assessments(self, curriculum_id: int):
        logger.info(f"[CurriculumService][get_assessments] Entered with curriculum_id: {curriculum_id}")
        return {
            "Chapter Name": "Chapter Name",
            "learningOutcomes": [
                "Identify the organs of the digestive system.",
                "Explain the digestion process."
            ],
            "numberOfAssessments": 2,
            "assessments": [
                {
                    "assessmentId": 1,
                    "assessmentNumber": 1,
                    "status": "Published",
                    "marks": 50,
                    "numberOfQuestions": 15
                },
                {
                    "assessmentId": 2,
                    "assessmentNumber": 2,
                    "status": "Generated",
                    "marks": 40,
                    "numberOfQuestions": 12
                }
            ]
        }