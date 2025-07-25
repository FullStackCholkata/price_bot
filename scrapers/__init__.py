"""
Web scraping modules for different e-commerce sites.
"""

from .geizhals import get_price_from_geizhals
from .campuspoint import get_price_from_campuspoint
from .edustore import get_price_from_edustore, get_stock_from_edustore

__all__ = [
    "get_price_from_geizhals",
    "get_price_from_campuspoint", 
    "get_price_from_edustore",
    "get_stock_from_edustore"
]
