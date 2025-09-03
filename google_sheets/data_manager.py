"""
Google Sheets data management utilities for reading and processing spreadsheet data.

Provides functions for extracting structured data from Google Sheets including
row-by-row data conversion and SKU lookup table generation for efficient
data processing and updates.
"""

import gspread

def get_data(worksheet: gspread.Worksheet) -> dict:
    """
    Extract all data from worksheet and convert to structured dictionary format.
    
    Reads the entire worksheet, separates headers from data rows, and creates
    a list of dictionaries where each row is represented as a key-value mapping
    using the header row as keys.
    
    Args:
        worksheet (gspread.Worksheet): Authenticated Google Sheets worksheet
        
    Returns:
        list[dict]: List of dictionaries, each representing a spreadsheet row
        
    Usage:
        data = get_data(worksheet)
        for row in data:
            print(row['SKU'], row['Geizhals Preis'])
    """
    # Read all worksheet data and separate headers from content
    data = worksheet.get_all_values()
    headers = data[0]
    data_rows = data[1:]
    
    return [dict(zip(headers, row)) for row in data_rows]


def get_sku_list(worksheet: gspread.Worksheet) -> dict:
    """
    Generate SKU lookup table mapping SKUs to their spreadsheet row numbers.
    
    Creates a dictionary that maps each SKU (from column A) to its corresponding
    row index in the spreadsheet. This enables efficient row lookups when
    updating price data for specific SKUs.
    
    Args:
        worksheet (gspread.Worksheet): Authenticated Google Sheets worksheet
        
    Returns:
        dict: Mapping of SKU strings to their row numbers (1-indexed)
        
    Usage:
        sku_lookup = get_sku_list(worksheet)
        row_number = sku_lookup['ABC123']  # Returns row number for SKU 'ABC123'
    """
    # Extract all SKUs from column A (excluding header row)
    all_values = worksheet.col_values(1)
    skus = all_values[1:]

    # Create mapping from SKU to spreadsheet row number (1-indexed)
    sku_to_index = {
        sku: index + 2  # +2 because: +1 for 1-based indexing, +1 to skip header
        for index, sku in enumerate(skus)
    }

    return sku_to_index
