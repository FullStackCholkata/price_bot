import asyncio
import random
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from utils import Colors, get_timestamp  # ADD THIS LINE

async def retry_after_timeout(func, *args, retries = 3, delay = 2):
    """
    Calls an async `scrape_fn(*args, **kwargs)`, retrying up to `retries` times
    if a Playwright TimeoutError is hit. Waits `delay` seconds between tries.
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