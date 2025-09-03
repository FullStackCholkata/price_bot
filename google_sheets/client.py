"""
Google Sheets client integration module for authentication and worksheet setup.

Handles Google Sheets API authentication using service account credentials
and provides worksheet connection functionality for the price bot application.
Manages OAuth2 scopes and credential authorization for spreadsheet access.
"""

import gspread
from google.oauth2.service_account import Credentials
from utils.colors import Colors
from utils.timing import get_timestamp
from config import GOOGLE_SHEETS_CONFIG

def setup_google_worksheet():
    """
    Set up authenticated Google Sheets worksheet connection.
    
    Establishes connection to the target Google Sheets document using
    service account credentials. Configures proper OAuth2 scopes for
    both spreadsheet and drive access permissions.
    
    Returns:
        gspread.Worksheet: Authenticated worksheet object ready for data operations
        
    Raises:
        Exception: If authentication fails or worksheet cannot be accessed
        
    Usage:
        worksheet = setup_google_worksheet()
        data = worksheet.get_all_records()
    """

    # Define required Google API scopes for spreadsheet and drive access
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",  # Read/write spreadsheet data
        "https://www.googleapis.com/auth/drive"          # Access drive files
    ]

    # Load service account credentials from JSON file
    credentials = Credentials.from_service_account_file(
        filename=GOOGLE_SHEETS_CONFIG["credentials_file"],
        scopes=SCOPES
    )

    # Authorize client and open target spreadsheet and worksheet
    client = gspread.authorize(credentials)
    spreadsheet = client.open(GOOGLE_SHEETS_CONFIG["spreadsheet_name"])
    worksheet = spreadsheet.worksheet(GOOGLE_SHEETS_CONFIG["worksheet_name"])

    print(f"[{get_timestamp()}] {Colors.YELLOW}Worksheet set up: {worksheet}{Colors.END}")

    return worksheet
