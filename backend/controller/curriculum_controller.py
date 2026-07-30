from fastapi import APIRouter

router = APIRouter(
    prefix = "/curriculum",
    tags = ["Curriculum"]
)

# 1. Get all grades
@router.get("/grades")
def get_all_grades():
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

#2. Get all courses in a grade
@router.get("/grades/{grade_id}/courses")
def get_courses_by_grade(grade_id: int):

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

#3. Get all units in a course
@router.get("/courses/{course_id}/units")
def get_units_by_course(course_id: int):

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

#4. Get all chapters in a unit
@router.get("/units/{unit_id}/chapters")
def get_chapters_by_unit(unit_id: int):

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

#5. Get curriculum id
@router.post("/id")
def get_curriculum_id( grade_id: int, course_id: int, unit_id: int, chapter_id: int ):
    return {
        "curriculumId": 55
    }

#6. Get assesment for a curriculum
@router.get("/{curriculum_id}/assessments")
def get_assessments(curriculum_id: int):
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
                "status": "Geenrated",
                "marks": 40,
                "numberOfQuestions": 12
            }
        ]
    }