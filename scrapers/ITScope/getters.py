"""
ITScope distributor stock availability retrieval module.

Provides specialized functions for extracting and formatting stock availability
information from major Austrian B2B technology distributors through the ITScope
platform. Handles complex stock status logic and date formatting for Ingram Micro,
ALSO, and TD SYNNEX Austria.
"""

from datetime import datetime

def get_availability_for_ingram(json_data) -> str:
    """
    Extract stock availability information for Ingram Micro Österreich.
    
    Processes ITScope API response data to determine current stock status
    and availability dates for Ingram Micro Austria. Handles multiple stock
    status codes and fallback logic for real-time vs. cached information.
    
    Args:
        json_data (list): Filtered supplier data from ITScope API
        
    Returns:
        str: Stock status text or formatted availability date, 'no data' if unavailable
        
    Stock Status Codes:
        1: Available
        6: Available/Special status  
        8: Unknown/No real-time data
        Other: Specific availability date
        
    Usage:
        availability = get_availability_for_ingram(supplier_data)
    """
    ret = 'no data'

    # Search for Ingram Micro supplier data
    for item in json_data:
        if item['supplier_name'] == 'Ingram Micro Österreich':
            stock_info = item['supplierStockInfo']
            
            # Validate stock_info structure - need at least 2 entries
            if not stock_info or len(stock_info) < 2:
                continue

            # Skip invalid combinations (status 6 + 8)
            if stock_info[0]['stockStatus'] == "6" and stock_info[1]['stockStatus'] == "8":
                ret = stock_info[0]['stockStatusText']
                continue

            # Check real-time stock status first (index 1)
            if stock_info[1]['stockStatus'] in ("1", "6"):
                ret = stock_info[1]['stockStatusText']
                return ret

            # Handle specific availability dates for non-standard statuses
            if stock_info[1]['stockStatus'] not in ("1", "6", "8"):
                ret = _format_date(stock_info[1]['stockAvailabilityDate'])
                return ret

            # Fallback to cached data when real-time is unknown (status 8)
            elif stock_info[1]['stockStatus'] == "8":
                # Use cached data (index 0) for fallback information
                if stock_info[0]['stockStatus'] in ("1", "8"):
                    ret = stock_info[0]['stockStatusText']
                    return ret
                ret = _format_date(stock_info[0]['stockAvailabilityDate'])
                return ret
    
    return ret

def get_availability_for_also (json_data) -> str:
    """
    Extract stock availability information for ALSO Österreich.
    
    Processes ITScope API response data to determine current stock status
    and availability dates for ALSO Austria. Implements similar logic to
    Ingram Micro with distributor-specific handling.
    
    Args:
        json_data (list): Filtered supplier data from ITScope API
        
    Returns:
        str: Stock status text or formatted availability date, 'no data' if unavailable
        
    Usage:
        availability = get_availability_for_also(supplier_data)
    """
    ret = 'no data'

    # Search for ALSO supplier data
    for item in json_data:
        if item['supplier_name'] == 'ALSO Österreich':
            stock_info = item['supplierStockInfo']
            
            # Validate stock_info structure - need at least 2 entries
            if not stock_info or len(stock_info) < 2:
                continue

            # Skip invalid combinations (status 6 + 8)
            if stock_info[0]['stockStatus'] == "6" and stock_info[1]['stockStatus'] == "8":
                ret = stock_info[0]['stockStatusText']
                continue

            # Check real-time stock status first (index 1)
            if stock_info[1]['stockStatus'] in ("1", "6"):
                ret = stock_info[1]['stockStatusText']
                return ret

            # Handle specific availability dates for non-standard statuses
            if stock_info[1]['stockStatus'] not in ("1", "6", "8"):
                ret = _format_date(stock_info[1]['stockAvailabilityDate'])
                return ret

            # Fallback to cached data when real-time is unknown (status 8)
            elif stock_info[1]['stockStatus'] == "8":
                # Use cached data (index 0) for fallback information
                if stock_info[0]['stockStatus'] in ("1", "8"):
                    ret = stock_info[0]['stockStatusText']
                    return ret

                ret = _format_date(stock_info[0]['stockAvailabilityDate'])
                return ret
    
    return ret

def get_availability_for_tdsynnex(json_data) -> str:
    """
    Extract stock availability information for TD SYNNEX Austria.
    
    Processes ITScope API response data to determine current stock status
    and availability dates for TD SYNNEX Austria. Follows the same logic
    pattern as other distributors with TD SYNNEX-specific handling.
    
    Args:
        json_data (list): Filtered supplier data from ITScope API
        
    Returns:
        str: Stock status text or formatted availability date, 'no data' if unavailable
        
    Usage:
        availability = get_availability_for_tdsynnex(supplier_data)
    """
    ret = 'no data'

    # Search for TD SYNNEX supplier data
    for item in json_data:
        if item['supplier_name'] == 'TD SYNNEX Austria':
            stock_info = item['supplierStockInfo']
            
            # Validate stock_info structure - need at least 2 entries
            if not stock_info or len(stock_info) < 2:
                continue

            # Skip invalid combinations (status 6 + 8)
            if stock_info[0]['stockStatus'] == "6" and stock_info[1]['stockStatus'] == "8":
                ret = stock_info[0]['stockStatusText']
                continue

            # Check real-time stock status first (index 1)
            if stock_info[1]['stockStatus'] in ("1", "6"):
                ret = stock_info[1]['stockStatusText']
                return ret

            # Handle specific availability dates for non-standard statuses
            if stock_info[1]['stockStatus'] not in ("1", "6", "8"):
                ret = _format_date(stock_info[1]['stockAvailabilityDate'])
                return ret

            # Fallback to cached data when real-time is unknown (status 8)
            elif stock_info[1]['stockStatus'] == "8":
                # Use cached data (index 0) for fallback information
                if stock_info[0]['stockStatus'] in ("1", "8"):
                    ret = stock_info[0]['stockStatusText']
                    return ret
                ret = _format_date(stock_info[0]['stockAvailabilityDate'])
                return ret
    
    return ret

def _format_date(date: str) -> str:
    """
    Format ISO date string to readable DD/MM/YY format.
    
    Converts ISO format datetime strings from ITScope API responses
    into user-friendly date format for availability information.
    Handles invalid or missing dates gracefully.
    
    Args:
        date (str): ISO format date string from API response
        
    Returns:
        str: Formatted date as DD/MM/YY or error message
        
    Usage:
        Internal helper function for formatting availability dates
    """
    # Handle empty or null date values
    try:
        if not date:
            return "No date available"
        
        # Parse ISO format date and convert to readable format
        parsed = datetime.fromisoformat(date)
        ret = parsed.strftime("%d/%m/%y")
        return ret
    except (ValueError, TypeError) as e:
        # Return descriptive error for invalid date formats
        return f"Invalid date: {date}"
