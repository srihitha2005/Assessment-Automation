import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GOOGLE_CREDENTIALS_FILE = os.path.join(
    BASE_DIR,
    "config",
    "google_credentials.json"
)

SPREADSHEET_ID = "1BwAjPu36ydXHcJwBXrcSJFq_UwE0Ax2Me-D_EMnjuZ4"
CURRICULUM_SHEET = "Curriculum"
PLANNERS_SHEET = "Planners"