"""
Timestamp utilities for logging and debugging operations.

Provides standardized timestamp formatting for consistent logging
across the price bot application.
"""

from datetime import datetime

def get_timestamp():
    """
    Generate a standardized timestamp string for logging purposes.
    
    Returns:
        str: Current timestamp in YYYY-MM-DD HH:MM:SS format
        
    Usage:
        print(f"[{get_timestamp()}] Operation completed")
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
