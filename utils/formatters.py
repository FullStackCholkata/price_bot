import re
from .colors import Colors
from .timing import get_timestamp

# Standardizes price format to '€ XXXX,XX'
def standardize_price_format(price_text):
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

# Formats the availabilitycomun in the spreadsheet
def format_availability_column(worksheet, row_index, availability_value):
    """Formats cell based on availability value with conditional colors."""
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
    """Formats cell based on availability value with conditional colors."""
    try:
        
        # Determine the background color based on availability
        if "auf Lager" in availability_value:
            background_color = {"red": 0.69, "green": 1.0, "blue": 0.686}  # Green

        elif re.match(r'\d{2}/\d{2}/\d{2}', availability_value):
            background_color = {"red": 0.808, "green": 1.0, "blue": 0.804}  # Light green

        elif availability_value == "nicht verfügbar" or availability_value == "No data":
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