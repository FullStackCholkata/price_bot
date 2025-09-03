"""
Web scraping modules for different e-commerce sites.

This package provides web scrapers for various Austrian e-commerce platforms:
- Geizhals: Price comparison platform scraper
- Campuspoint: Educational technology retailer scraper  
- edustore: Educational products retailer scraper with price and stock checking
- ITScope: B2B technology distributor API client and availability parsers

All scrapers are designed to work asynchronously with proper error handling
and rate limiting through semaphores.
"""

from .geizhals import get_price_from_geizhals
from .campuspoint import get_price_from_campuspoint
from .edustore import get_price_from_edustore, get_stock_from_edustore
from .ITScope import *

__all__ = [
    # E-commerce site scrapers
    "get_price_from_geizhals",          # Async price scraper for Geizhals.at
    "get_price_from_campuspoint",       # Async price scraper for Campuspoint
    "get_price_from_edustore",          # Async price scraper for edustore
    "get_stock_from_edustore",          # Async stock availability checker for edustore
    
    # ITScope B2B distributor integration
    "ITscopeClient",                    # API client for ITScope distributor platform
    "get_availability_for_ingram",      # Availability parser for Ingram Micro Austria
    "get_availability_for_also",        # Availability parser for ALSO Austria  
    "get_availability_for_tdsynnex"     # Availability parser for TD SYNNEX Austria
]
