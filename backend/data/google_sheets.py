"""Planner and curriculum data source.

Reads Google Sheets when credentials are configured; falls back to a bundled
dataset that covers every question-bank chapter so the demo runs offline.
"""
from __future__ import annotations

import logging
from copy import deepcopy

from config import settings

logger = logging.getLogger(__name__)


FALLBACK_CURRICULUM: list[dict] = [
    # Science
    {"curriculumId": "CURR001", "gradeId": 6, "grade": "Grade 6", "courseId": 101, "courseName": "Science", "unitId": 11, "unitName": "Living World", "chapterId": 1101, "chapterName": "Cell Structure"},
    {"curriculumId": "CURR002", "gradeId": 7, "grade": "Grade 7", "courseId": 101, "courseName": "Science", "unitId": 11, "unitName": "Living World", "chapterId": 1102, "chapterName": "Plant and Animal Cells"},
    {"curriculumId": "CURR003", "gradeId": 6, "grade": "Grade 6", "courseId": 101, "courseName": "Science", "unitId": 11, "unitName": "Living World", "chapterId": 1103, "chapterName": "Microorganisms"},
    {"curriculumId": "CURR004", "gradeId": 8, "grade": "Grade 8", "courseId": 101, "courseName": "Science", "unitId": 12, "unitName": "Human Body", "chapterId": 1201, "chapterName": "Digestive System"},
    {"curriculumId": "CURR005", "gradeId": 7, "grade": "Grade 7", "courseId": 101, "courseName": "Science", "unitId": 12, "unitName": "Human Body", "chapterId": 1202, "chapterName": "Respiratory System"},
    {"curriculumId": "CURR006", "gradeId": 8, "grade": "Grade 8", "courseId": 101, "courseName": "Science", "unitId": 12, "unitName": "Human Body", "chapterId": 1203, "chapterName": "Circulatory System"},
    {"curriculumId": "CURR007", "gradeId": 6, "grade": "Grade 6", "courseId": 101, "courseName": "Science", "unitId": 13, "unitName": "Matter", "chapterId": 1301, "chapterName": "States of Matter"},
    {"curriculumId": "CURR008", "gradeId": 7, "grade": "Grade 7", "courseId": 101, "courseName": "Science", "unitId": 13, "unitName": "Matter", "chapterId": 1302, "chapterName": "Physical and Chemical Changes"},

    # Mathematics
    {"curriculumId": "CURR009", "gradeId": 6, "grade": "Grade 6", "courseId": 102, "courseName": "Mathematics", "unitId": 21, "unitName": "Number Systems", "chapterId": 2101, "chapterName": "Whole Numbers"},
    {"curriculumId": "CURR010", "gradeId": 6, "grade": "Grade 6", "courseId": 102, "courseName": "Mathematics", "unitId": 21, "unitName": "Number Systems", "chapterId": 2102, "chapterName": "Fractions"},
    {"curriculumId": "CURR011", "gradeId": 7, "grade": "Grade 7", "courseId": 102, "courseName": "Mathematics", "unitId": 21, "unitName": "Number Systems", "chapterId": 2103, "chapterName": "Decimals"},
    {"curriculumId": "CURR012", "gradeId": 7, "grade": "Grade 7", "courseId": 102, "courseName": "Mathematics", "unitId": 22, "unitName": "Algebra", "chapterId": 2201, "chapterName": "Variables and Expressions"},
    {"curriculumId": "CURR013", "gradeId": 8, "grade": "Grade 8", "courseId": 102, "courseName": "Mathematics", "unitId": 22, "unitName": "Algebra", "chapterId": 2202, "chapterName": "Linear Equations"},
    {"curriculumId": "CURR014", "gradeId": 7, "grade": "Grade 7", "courseId": 102, "courseName": "Mathematics", "unitId": 23, "unitName": "Geometry", "chapterId": 2301, "chapterName": "Lines and Angles"},
    {"curriculumId": "CURR015", "gradeId": 7, "grade": "Grade 7", "courseId": 102, "courseName": "Mathematics", "unitId": 23, "unitName": "Geometry", "chapterId": 2302, "chapterName": "Triangles"},
    {"curriculumId": "CURR016", "gradeId": 8, "grade": "Grade 8", "courseId": 102, "courseName": "Mathematics", "unitId": 23, "unitName": "Geometry", "chapterId": 2303, "chapterName": "Circles"},

    # English
    {"curriculumId": "CURR017", "gradeId": 6, "grade": "Grade 6", "courseId": 103, "courseName": "English", "unitId": 31, "unitName": "Reading Skills", "chapterId": 3101, "chapterName": "Reading Comprehension"},
    {"curriculumId": "CURR018", "gradeId": 7, "grade": "Grade 7", "courseId": 103, "courseName": "English", "unitId": 31, "unitName": "Reading Skills", "chapterId": 3102, "chapterName": "Inference Skills"},
    {"curriculumId": "CURR019", "gradeId": 6, "grade": "Grade 6", "courseId": 103, "courseName": "English", "unitId": 31, "unitName": "Reading Skills", "chapterId": 3103, "chapterName": "Vocabulary Building"},
    {"curriculumId": "CURR020", "gradeId": 7, "grade": "Grade 7", "courseId": 103, "courseName": "English", "unitId": 32, "unitName": "Writing Skills", "chapterId": 3201, "chapterName": "Paragraph Writing"},
    {"curriculumId": "CURR021", "gradeId": 8, "grade": "Grade 8", "courseId": 103, "courseName": "English", "unitId": 32, "unitName": "Writing Skills", "chapterId": 3202, "chapterName": "Letter Writing"},
    {"curriculumId": "CURR022", "gradeId": 8, "grade": "Grade 8", "courseId": 103, "courseName": "English", "unitId": 32, "unitName": "Writing Skills", "chapterId": 3203, "chapterName": "Story Writing"},

    # Social Studies
    {"curriculumId": "CURR023", "gradeId": 6, "grade": "Grade 6", "courseId": 104, "courseName": "Social Studies", "unitId": 41, "unitName": "Geography", "chapterId": 4101, "chapterName": "Continents and Oceans"},
    {"curriculumId": "CURR024", "gradeId": 7, "grade": "Grade 7", "courseId": 104, "courseName": "Social Studies", "unitId": 41, "unitName": "Geography", "chapterId": 4102, "chapterName": "Maps and Globes"},
    {"curriculumId": "CURR025", "gradeId": 7, "grade": "Grade 7", "courseId": 104, "courseName": "Social Studies", "unitId": 42, "unitName": "Ancient Civilizations", "chapterId": 4201, "chapterName": "Indus Valley"},
    {"curriculumId": "CURR026", "gradeId": 8, "grade": "Grade 8", "courseId": 104, "courseName": "Social Studies", "unitId": 42, "unitName": "Ancient Civilizations", "chapterId": 4202, "chapterName": "Egyptian"},

    # Computer Science
    {"curriculumId": "CURR027", "gradeId": 7, "grade": "Grade 7", "courseId": 105, "courseName": "Computer Science", "unitId": 51, "unitName": "Programming Basics", "chapterId": 5101, "chapterName": "Algorithms"},
    {"curriculumId": "CURR028", "gradeId": 7, "grade": "Grade 7", "courseId": 105, "courseName": "Computer Science", "unitId": 51, "unitName": "Programming Basics", "chapterId": 5102, "chapterName": "Flowcharts"},
    {"curriculumId": "CURR029", "gradeId": 6, "grade": "Grade 6", "courseId": 105, "courseName": "Computer Science", "unitId": 52, "unitName": "Scratch Programming", "chapterId": 5201, "chapterName": "Loops"},
    {"curriculumId": "CURR030", "gradeId": 6, "grade": "Grade 6", "courseId": 105, "courseName": "Computer Science", "unitId": 52, "unitName": "Scratch Programming", "chapterId": 5202, "chapterName": "Motion Blocks"},
]


FALLBACK_PLANNERS: list[dict] = [
    {"plannerId": "P001", "curriculumId": "CURR001", "plannerName": "Cell Structure Planner",
     "learningOutcomes": ["Identify the parts of a cell", "Explain the function of each organelle", "Compare plant and animal cells"]},
    {"plannerId": "P002", "curriculumId": "CURR002", "plannerName": "Plant and Animal Cells Planner",
     "learningOutcomes": ["Differentiate plant and animal cells", "Identify unique cell structures", "Explain cell adaptations"]},
    {"plannerId": "P003", "curriculumId": "CURR003", "plannerName": "Microorganisms Planner",
     "learningOutcomes": ["Classify microorganisms", "Describe beneficial microorganisms", "Explain harmful microorganisms"]},
    {"plannerId": "P004", "curriculumId": "CURR004", "plannerName": "Digestive System Planner",
     "learningOutcomes": ["Identify digestive organs", "Explain digestion", "Describe nutrient absorption"]},
    {"plannerId": "P005", "curriculumId": "CURR005", "plannerName": "Respiratory System Planner",
     "learningOutcomes": ["Identify respiratory organs", "Explain gas exchange", "Differentiate breathing and respiration"]},
    {"plannerId": "P006", "curriculumId": "CURR006", "plannerName": "Circulatory System Planner",
     "learningOutcomes": ["Identify parts of the heart", "Trace blood flow", "Describe components of blood"]},
    {"plannerId": "P007", "curriculumId": "CURR013", "plannerName": "Linear Equations Planner",
     "learningOutcomes": ["Solve linear equations", "Model real-world problems as equations", "Verify solutions"]},
    {"plannerId": "P008", "curriculumId": "CURR017", "plannerName": "Reading Comprehension Planner",
     "learningOutcomes": ["Identify main ideas", "Draw inferences from a passage", "Summarise a passage"]},
    {"plannerId": "P009", "curriculumId": "CURR023", "plannerName": "Continents and Oceans Planner",
     "learningOutcomes": ["Name the seven continents", "Locate the five oceans", "Compare continents by size"]},
    {"plannerId": "P010", "curriculumId": "CURR027", "plannerName": "Algorithms Planner",
     "learningOutcomes": ["Define an algorithm", "Trace an algorithm step by step", "Write pseudo-code for a task"]},
]


def _split_outcomes(value: str) -> list[str]:
    return [item.strip() for item in value.replace("\n", ";").split(";") if item.strip()]


class GoogleSheetsDataSource:
    """Read curriculum + planner rows from a Google Sheet (or the bundled fallback).

    An in-memory planner-outcomes overlay lets the propagation flow simulate a
    planner edit without touching the sheet.
    """

    _planner_overrides: dict[str, list[str]] = {}

    @classmethod
    def override_planner_outcomes(cls, planner_id: str, outcomes: list[str]) -> None:
        cls._planner_overrides[planner_id] = list(outcomes)

    def _read_rows(self, sheet_range: str) -> list[dict[str, str]]:
        if not settings.google_spreadsheet_id or not settings.google_service_account_file:
            return []
        try:
            from google.oauth2.service_account import Credentials
            from googleapiclient.discovery import build

            credentials = Credentials.from_service_account_file(
                settings.google_service_account_file,
                scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"],
            )
            values = (
                build("sheets", "v4", credentials=credentials)
                .spreadsheets()
                .values()
                .get(spreadsheetId=settings.google_spreadsheet_id, range=sheet_range)
                .execute()
                .get("values", [])
            )
            if not values:
                return []
            headers = [header.strip() for header in values[0]]
            return [dict(zip(headers, row)) for row in values[1:]]
        except Exception:
            logger.exception("Google Sheets read failed; using bundled fallback data.")
            return []

    def get_curriculum(self) -> list[dict]:
        rows = self._read_rows("Curriculum!A:I")
        if not rows:
            logger.warning("Curriculum data not found in Google Sheets; using bundled fallback data.")
            return deepcopy(FALLBACK_CURRICULUM)
        return [
            {
                "curriculumId": row.get("Curriculum_ID", ""),
                "gradeId": int(row.get("Grade_ID", "0") or 0),
                "grade": row.get("Grade", ""),
                "courseId": int(row.get("Course_ID", "0") or 0),
                "courseName": row.get("Course_Name", ""),
                "unitId": int(row.get("Unit_ID", "0") or 0),
                "unitName": row.get("Unit_Name", ""),
                "chapterId": int(row.get("Chapter_ID", "0") or 0),
                "chapterName": row.get("Chapter_Name", ""),
            }
            for row in rows
        ]

    def get_planners(self) -> list[dict]:
        rows = self._read_rows("Planner_details!A:E")
        if not rows:
            base = deepcopy(FALLBACK_PLANNERS)
        else:
            base = [
                {
                    "plannerId": row.get("Planner_ID", ""),
                    "curriculumId": row.get("Curriculum_ID", ""),
                    "plannerName": row.get("Planner_name", ""),
                    "plannerLink":row.get("Planner_link", ""),
                    "learningOutcomes": _split_outcomes(row.get("Learning_Outcomes", "")),
                }
                for row in rows
            ]
        for planner in base:
            if planner["plannerId"] in self._planner_overrides:
                planner["learningOutcomes"] = list(self._planner_overrides[planner["plannerId"]])
        return base

    def get_planner(self, planner_id: str) -> dict | None:
        return next((item for item in self.get_planners() if item["plannerId"] == planner_id), None)

    def get_planner_context(self, planner_id: str) -> dict | None:
        planner = self.get_planner(planner_id)
        if not planner:
            return None
        curriculum = next(
            (item for item in self.get_curriculum() if item["curriculumId"] == planner["curriculumId"]),
            None,
        )
        return {**planner, **(curriculum or {})}
