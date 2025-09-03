"""
Google Sheets integration modules.

This package provides integration with Google Sheets API for:
- Authentication and worksheet setup
- Data reading and writing operations
- SKU list management and processing

The module handles Google Sheets authentication using service account
credentials and provides utilities for reading product data and 
updating price information in the spreadsheet.
"""

from .client import setup_google_worksheet
from .data_manager import get_data, get_sku_list

__all__ = [
    # Google Sheets client setup
    "setup_google_worksheet",    # Sets up authenticated Google Sheets worksheet connection
    
    # Data management operations
    "get_data",                  # Retrieves all data from the worksheet as dictionary
    "get_sku_list"              # Extracts SKU list from worksheet for processing
]
