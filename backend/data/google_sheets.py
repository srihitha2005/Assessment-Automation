"""Planner and curriculum access.

Google Sheets is used when credentials are configured.  The small fallback data makes
the prototype usable immediately and mirrors the sample supplied in Design.pdf.
"""
import logging

from config import settings

logger = logging.getLogger(__name__)

FALLBACK_CURRICULUM = [
    {"curriculumId": "CURR001", "courseId": "C001", "courseName": "Science", "unitId": "U001", "unitName": "Living World", "chapterId": "CH001", "chapterName": "Cell Structure", "grade": "Grade 6"},
    {"curriculumId": "CURR002", "courseId": "C001", "courseName": "Science", "unitId": "U001", "unitName": "Living World", "chapterId": "CH002", "chapterName": "Plant and Animal Cells", "grade": "Grade 7"},
    {"curriculumId": "CURR003", "courseId": "C001", "courseName": "Science", "unitId": "U001", "unitName": "Living World", "chapterId": "CH003", "chapterName": "Microorganisms", "grade": "Grade 6"},
    {"curriculumId": "CURR004", "courseId": "C001", "courseName": "Science", "unitId": "U002", "unitName": "Human Body", "chapterId": "CH004", "chapterName": "Digestive System", "grade": "Grade 8"},
]

FALLBACK_PLANNERS = [
    {"plannerId": "P001", "curriculumId": "CURR001", "plannerName": "Cell Structure Planner", "learningOutcomes": ["Identify the parts of a cell", "Explain the function of each organelle", "Compare plant and animal cells"]},
    {"plannerId": "P002", "curriculumId": "CURR002", "plannerName": "Plant and Animal Cells Planner", "learningOutcomes": ["Differentiate plant and animal cells", "Identify unique cell structures", "Explain cell adaptations"]},
    {"plannerId": "P003", "curriculumId": "CURR003", "plannerName": "Microorganisms Planner", "learningOutcomes": ["Classify microorganisms", "Describe beneficial microorganisms", "Explain harmful microorganisms"]},
    {"plannerId": "P004", "curriculumId": "CURR004", "plannerName": "Digestive System Planner", "learningOutcomes": ["Identify digestive organs", "Explain digestion", "Describe nutrient absorption"]},
]


def _split_outcomes(value: str) -> list[str]:
    return [item.strip() for item in value.replace("\n", ";").split(";") if item.strip()]


class GoogleSheetsDataSource:
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
            values = build("sheets", "v4", credentials=credentials).spreadsheets().values().get(
                spreadsheetId=settings.google_spreadsheet_id, range=sheet_range
            ).execute().get("values", [])
            if not values:
                return []
            headers = [header.strip() for header in values[0]]
            return [dict(zip(headers, row)) for row in values[1:]]
        except Exception:
            logger.exception("Google Sheets read failed; using bundled fallback data.")
            return []

    def get_curriculum(self) -> list[dict]:
        rows = self._read_rows("Curriculum!A:H")
        if not rows:
            return FALLBACK_CURRICULUM
        return [
            {"curriculumId": row.get("Curriculum_ID", ""), "courseId": row.get("Course_ID", ""), "courseName": row.get("Course_Name", ""), "unitId": row.get("Unit_ID", ""), "unitName": row.get("Unit_Name", ""), "chapterId": row.get("Chapter_ID", ""), "chapterName": row.get("Chapter_Name", ""), "grade": row.get("Grade", "")}
            for row in rows
        ]

    def get_planners(self) -> list[dict]:
        rows = self._read_rows("Planners!A:D")
        if not rows:
            return FALLBACK_PLANNERS
        return [
            {"plannerId": row.get("Planner_ID", ""), "curriculumId": row.get("Curriculum_ID", ""), "plannerName": row.get("Planner_Name", ""), "learningOutcomes": _split_outcomes(row.get("Learning_Outcomes", ""))}
            for row in rows
        ]

    def get_planner_context(self, planner_id: str) -> dict | None:
        planner = next((item for item in self.get_planners() if item["plannerId"] == planner_id), None)
        if not planner:
            return None
        curriculum = next((item for item in self.get_curriculum() if item["curriculumId"] == planner["curriculumId"]), None)
        return {**planner, **(curriculum or {})}
