import gspread
from google.oauth2.service_account import Credentials
from utils.colors import Colors
from utils.timing import get_timestamp
from config import GOOGLE_SHEETS_CONFIG

# Sets up the google spreadsheet that needs to be updated with this script
def setup_google_worksheet():

    # Scopes of the google spreadsheets; never changes
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    # download credentials file from google cloud
    credentials = Credentials.from_service_account_file(
        filename=GOOGLE_SHEETS_CONFIG["credentials_file"],
        scopes = SCOPES
    )

    client = gspread.authorize(credentials)
    spreadsheet = client.open(GOOGLE_SHEETS_CONFIG["spreadsheet_name"])
    worksheet = spreadsheet.worksheet(GOOGLE_SHEETS_CONFIG["worksheet_name"])

    # Debug line
    print(f"[{get_timestamp()}] {Colors.YELLOW}Worksheet set up: {worksheet}{Colors.END}")

    return worksheet
