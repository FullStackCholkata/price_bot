"""
Utility modules for the price reader package.

This package provides common utilities used throughout the price bot application:
- Colors: Terminal color formatting for better logging readability
- Formatters: Price and availability data formatting functions
- Timing: Timestamp utilities for logging and debugging
- Error handling: Retry mechanisms for robust network operations
- Headers: Random user agent generation for web scraping
"""

from .colors import Colors
from .formatters import standardize_price_format, format_availability_column, format_itscope_availability_columns
from .timing import get_timestamp
from .error_retry import retry_after_timeout
from .headers import get_random_headers

__all__ = [
    # Terminal color formatting
    "Colors",
    
    # Timestamp utilities
    "get_timestamp", 
    
    # Price and data formatting
    "standardize_price_format",          # Standardizes price format to '€ XXXX,XX'
    "format_availability_column",        # Formats availability data in Google Sheets
    "format_itscope_availability_columns", # Formats ITScope availability data with colors
    
    # Network utilities
    "get_random_headers",               # Generates random headers for web scraping
    "retry_after_timeout"               # Async retry mechanism for failed operations
]
