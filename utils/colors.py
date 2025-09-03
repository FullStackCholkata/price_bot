"""
Terminal color formatting utilities for enhanced logging and console output.

Provides ANSI color codes for creating colored terminal output to improve
readability of logs, error messages, and status information during
price bot execution.
"""

class Colors:
    """
    ANSI color code constants for terminal text formatting.
    
    Provides standardized color schemes for different types of output:
    - RED: Error messages and critical issues
    - GREEN: Success confirmations and positive status
    - YELLOW: Warnings and informational messages
    - BLUE: Processing updates and workflow status
    - CYAN: Debug information and detailed logs
    - END: Reset formatting to default terminal colors
    
    Usage:
        print(f"{Colors.RED}Error occurred{Colors.END}")
    """
    RED = '\033[91m'      # Errors and critical issues
    GREEN = '\033[92m'    # Success messages and confirmations
    YELLOW = '\033[93m'   # Warnings and informational output
    BLUE = '\033[94m'     # Processing messages and workflow status
    CYAN = '\033[96m'     # Debug information and detailed logs
    END = '\033[0m'       # Reset to default terminal formatting
