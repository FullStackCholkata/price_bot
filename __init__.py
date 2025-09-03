"""
Price Reader Package

A comprehensive web scraping tool for extracting product prices from various 
Austrian e-commerce websites and updating Google Sheets with the collected data.

Features:
- Concurrent scraping from multiple e-commerce platforms (Geizhals, Campuspoint, edustore)
- B2B distributor integration (ITScope API for Ingram, ALSO, TD SYNNEX)
- Smart caching to reduce API calls for SKU variants
- Google Sheets integration with formatting and color coding
- Robust error handling and retry mechanisms
- Rate limiting and respectful scraping practices

The package is designed for educational technology retailers in Austria
to monitor competitor pricing and distributor availability.
"""

from .main import main, main_async
from .config import COLUMN_MAP, SEMAPHORE_LIMIT, GOOGLE_SHEETS_CONFIG, USER_AGENTS

__version__ = "1.0.0"
__author__ = "Lachezar Damyanov" 
__email__ = "lachezar@edustore.at"

__all__ = [
    # Main entry points
    "main",                      # Synchronous main function wrapper
    "main_async",               # Asynchronous main processing function
    
    # Configuration constants
    "COLUMN_MAP",               # Google Sheets column mapping configuration
    "SEMAPHORE_LIMIT",          # Concurrent request limit for rate limiting
    "GOOGLE_SHEETS_CONFIG",     # Google Sheets API configuration
    "USER_AGENTS"               # List of user agents for web scraping
]
