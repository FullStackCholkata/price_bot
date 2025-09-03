"""
Data processing modules for SKU and price handling.

This package provides core business logic for processing product SKUs:
- Concurrent processing of product data from multiple sources
- Smart caching for SKU variants to reduce API calls
- Integration with all scraper modules and Google Sheets
- Error handling and logging for robust data collection

The main processor orchestrates data collection from:
- Geizhals (price comparison)
- Campuspoint (educational technology)  
- edustore (educational products)
- ITScope (B2B distributors)
"""

from .sku_processor import process_sku

__all__ = [
    "process_sku"    # Main async function for processing individual SKUs with concurrent scraping
]
