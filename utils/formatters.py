"""
Data formatting utilities for price standardization and Google Sheets styling.

Provides comprehensive formatting functions for:
- Price text standardization to consistent EUR format
- Google Sheets cell formatting with conditional colors
- Availability data styling and color coding
- ITScope distributor data formatting with visual indicators

All functions handle edge cases and provide error recovery for robust operation.
"""

import re
from .colors import Colors
from .timing import get_timestamp

def standardize_price_format(price_text):
    """
    Standardize price text to consistent '€ XXXX,XX' format.
    
    Converts various price formats from different e-commerce sites
    into a standardized European format with euro symbol, thousands
    separators (dots), and decimal separators (commas).
    
    Args:
        price_text (str): Raw price text from web scraping
        
    Returns:
        str: Standardized price format or original text if parsing fails
        
    Examples:
        "867,22€" -> "€ 867,22"
        "1.039,00€" -> "€ 1.039,00"
        "€ 867,22" -> "€ 867,22" (already standardized)
    """
    if not price_text or price_text in ["N/A", "Error in get_price_from_geizhals()", "Error get_price_from_campuspoint()", "Error get_price_from_edustore()", "The product above is not related to this one!"]:
        return price_text
    
    # Removes any whitespace and non-breaking spaces
    price_text = price_text.replace('\xa0', ' ').strip()
    
    # Extract numbers and decimal separators
    # Matches patterns like: €867,22 | € 867,22 | 867,22€ | 1.039,00€ | €879,00
    price_match = re.search(r'[\d.,]+', price_text)
    
    if not price_match:
        return price_text
    
    price_number = price_match.group()
    
    # Handles thousands separator (dot) and decimal separator (comma)
    if ',' in price_number and '.' in price_number:
        # Format like 1.039,00 - dot is thousands separator
        price_number = price_number.replace('.', '').replace(',', '.')
    elif ',' in price_number:
        # Format like 867,22 - comma is decimal separator
        price_number = price_number.replace(',', '.')
    
    try:
        # Converts to float and back to standardized format
        price_float = float(price_number)
        return f"€ {price_float:,.2f}".replace(',', 'TEMP').replace('.', ',').replace('TEMP', '.')
    except ValueError:
        return price_text

def format_availability_column(worksheet, row_index, availability_value):
    """
    Format Google Sheets availability column with conditional color coding.
    
    Applies background colors to availability cells based on stock status:
    - Green: In stock ("Ja")
    - Light Green: Pre-orderable ("Vorbestellbar") 
    - Light Red: Out of stock ("Nein")
    - Light Yellow: Other status (dates, custom text)
    
    Args:
        worksheet: Google Sheets worksheet object
        row_index (int): Row number in the spreadsheet
        availability_value (str): Stock availability status text
        
    Usage:
        format_availability_column(worksheet, 5, "Ja")
    """
    try:
        
        # Determine the background color based on availability
        if availability_value == "Ja":
            background_color = {"red": 0.69, "green": 1.0, "blue": 0.686}  # Green

        elif availability_value == "Vorbestellbar":
            background_color = {"red": 0.808, "green": 1.0, "blue": 0.804}  # Light green

        elif availability_value == "Nein":
            background_color = {"red": 1.0, "green": 0.604, "blue": 0.604}  # Light red

        else:
            background_color = {"red": 1.0, "green": 0.812, "blue": 0.55}  # Light yellow
        
        # Create the formatting request
        requests = [{
            "repeatCell": {
                "range": {
                    "sheetId": worksheet.id,
                    "startRowIndex": row_index - 1,
                    "endRowIndex": row_index,
                    "startColumnIndex": 2,  # Column C (0-indexed, so C = 2)
                    "endColumnIndex": 3
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": background_color,
                        "horizontalAlignment": "CENTER"
                    }
                },
                "fields": "userEnteredFormat.backgroundColor,userEnteredFormat.horizontalAlignment,userEnteredFormat.textFormat.bold"
            }
        }]
        
        body = {"requests": requests}
        worksheet.spreadsheet.batch_update(body)
        
    except Exception as e:
        print(f"[{get_timestamp()}]     {Colors.RED}Error formatting availability cell: {e}{Colors.END}")

def format_itscope_availability_columns(worksheet, row_index, availability_value: str, startColumnIndex: int):
    """
    Format ITScope distributor availability columns with conditional color coding.
    
    Applies background colors to ITScope distributor columns based on stock status:
    - Green: In stock (contains "auf Lager")
    - Light Green: Available on date (DD/MM/YY format)
    - Light Red: Not available ("nicht verfügbar", "no data")
    - Light Yellow: Other status (unknown, pending, etc.)
    
    Args:
        worksheet: Google Sheets worksheet object
        row_index (int): Row number in the spreadsheet
        availability_value (str): Stock availability status from ITScope
        startColumnIndex (int): Starting column index (0-based) for formatting
        
    Usage:
        format_itscope_availability_columns(worksheet, 5, "126 auf Lager", 4)
    """
    try:
        
        # Determine the background color based on availability
        if "auf Lager" in availability_value:
            background_color = {"red": 0.69, "green": 1.0, "blue": 0.686}  # Green

        elif re.match(r'\d{2}/\d{2}/\d{2}', availability_value):
            background_color = {"red": 0.808, "green": 1.0, "blue": 0.804}  # Light green

        elif availability_value == "nicht verfügbar" or availability_value == "no data":
            background_color = {"red": 1.0, "green": 0.604, "blue": 0.604}  # Light red

        else:
            background_color = {"red": 1.0, "green": 0.812, "blue": 0.55}  # Light yellow
        
        # Create the formatting request
        requests = [{
            "repeatCell": {
                "range": {
                    "sheetId": worksheet.id,
                    "startRowIndex": row_index - 1,
                    "endRowIndex": row_index,
                    "startColumnIndex": startColumnIndex,
                    "endColumnIndex": startColumnIndex + 1
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": background_color,
                        "horizontalAlignment": "CENTER"
                    }
                },
                "fields": "userEnteredFormat.backgroundColor,userEnteredFormat.horizontalAlignment,userEnteredFormat.textFormat.bold"
            }
        }]
        
        body = {"requests": requests}
        worksheet.spreadsheet.batch_update(body)
        
    except Exception as e:
        print(f"[{get_timestamp()}]     {Colors.RED}Error formatting availability cell: {e}{Colors.END}")