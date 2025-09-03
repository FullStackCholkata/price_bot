"""
ITScope B2B distributor platform integration.

This module provides integration with the ITScope API, a B2B technology
distribution platform used in Austria. It includes:

- API client for product lookups and real-time stock information
- Availability parsers for major Austrian distributors:
  * Ingram Micro Österreich
  * ALSO Österreich  
  * TD SYNNEX Austria

The module handles complex stock status logic including real-time vs 
non-real-time data, availability dates, and supplier-specific formatting.
"""

from .client import ITscopeClient
from .getters import get_availability_for_ingram, get_availability_for_also, get_availability_for_tdsynnex

__all__ = [
    # API client
    "ITscopeClient",                    # Main API client for ITScope platform
    
    # Distributor availability parsers
    "get_availability_for_ingram",      # Parses Ingram Micro stock data
    "get_availability_for_also",        # Parses ALSO Austria stock data
    "get_availability_for_tdsynnex"     # Parses TD SYNNEX Austria stock data
]