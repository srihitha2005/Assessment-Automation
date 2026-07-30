import gspread
from google.oauth2.service_account import Credentials
from config.sheetsConfig import GOOGLE_CREDENTIALS_FILE, SPREADSHEET_ID

class GoogleSheetHelper:
    def __init__(self):
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        credentials = Credentials.from_service_account_file(
            GOOGLE_CREDENTIALS_FILE,
            scopes = scope
        )

        client = gspread.authorize(credentials)
        self.spreadsheet = client.open_by_key(SPREADSHEET_ID)

    def get_sheet(self, sheet_name):
        return self.spreadsheet.worksheet(sheet_name)

    def get_all_records(self,sheet_name):
        sheet = self.get_sheet(sheet_name)
        return sheet.get_all_records()