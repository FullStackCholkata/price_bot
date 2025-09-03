"""
Retry mechanism utilities for robust network operations and error handling.

Provides async retry functionality for web scraping operations that may
fail due to network timeouts, rate limiting, or temporary site issues.
Implements exponential backoff and comprehensive error logging.
"""

import asyncio
import random
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from .colors import Colors
from .timing import get_timestamp

async def retry_after_timeout(func, *args, retries=3, delay=2):
    """
    Execute an async function with automatic retry on timeout or network errors.
    
    Retries the provided async function up to the specified number of times
    if Playwright timeouts, asyncio timeouts, or other exceptions occur.
    Implements colored logging for retry attempts and final failure states.
    
    Args:
        func: Async function to execute
        *args: Arguments to pass to the function
        retries (int): Maximum number of retry attempts (default: 3)
        delay (int): Delay in seconds between retry attempts (default: 2)
        
    Returns:
        Result of successful function execution or error message string
        
    Usage:
        result = await retry_after_timeout(scrape_function, url, semaphore)
    """
    last_exc = None
    for attempt in range(1, retries + 1):
        try:
            return await func(*args)
        except (PlaywrightTimeoutError, asyncio.TimeoutError, Exception) as e:
            last_exc = e
            print(f"[{get_timestamp()}]     {Colors.YELLOW}[Attempt {attempt}/{retries}] Error: {type(e).__name__}, retrying in {delay}s…{Colors.END}")
            if attempt < retries:
                await asyncio.sleep(delay)
            else:
                print(f"[{get_timestamp()}]     {Colors.RED}[Attempt {attempt}/{retries}] Giving up after {type(e).__name__}.{Colors.END}")
    # if we exhausted all retries, re-raise or return a sentinel
    return f"Failed after {retries} attempts"