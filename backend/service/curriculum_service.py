import logging
logger = logging.getLogger(__name__)


class CurriculumService:

    # 1. Get All Grades
    def get_all_grades(self):
        logger.info("[CurriculumService][get_all_grades] Entered")
        return {
            "totalGrades": 3,
            "grades": [
                {
                    "gradeId": 1,
                    "gradeName": "Grade 6",
                    "numberOfUnits": 5
                },
                {
                    "gradeId": 2,
                    "gradeName": "Grade 7",
                    "numberOfUnits": 6
                },
                {
                    "gradeId": 3,
                    "gradeName": "Grade 8",
                    "numberOfUnits": 4
                }
            ]
        }


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