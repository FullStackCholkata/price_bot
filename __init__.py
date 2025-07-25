"""
Price Reader Package

A web scraping tool for extracting product prices from various e-commerce websites
and updating Google Sheets with the collected data.
"""

from .main import main, main_async
from .config import COLUMN_MAP, SEMAPHORE_LIMIT, GOOGLE_SHEETS_CONFIG, USER_AGENTS

__version__ = "1.0.0"
__author__ = "Lachezar Damyanov"
__email__ = "lachezar@edustore.at"

__all__ = [
    "main",
    "main_async",
    "COLUMN_MAP", 
    "SEMAPHORE_LIMIT",
    "GOOGLE_SHEETS_CONFIG",
    "USER_AGENTS"
]
