import asyncio
import random
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

async def retry_after_timeout(func, *args, retries = 3, delay = 2):
    """
    Calls an async `scrape_fn(*args, **kwargs)`, retrying up to `retries` times
    if a Playwright TimeoutError is hit. Waits `delay` seconds between tries.
    """
    last_exc = None
    for attempt in range(1, retries + 1):
        try:
            return await func(*args)
        except PlaywrightTimeoutError as e:
            last_exc = e
            print(f"[{get_timestamp()}]     {Colors.YELLOW}[Attempt {attempt}/{retries}] TimeoutError, retrying in {delay}s…{Colors.END}")
            if attempt < retries:
                await asyncio.sleep(delay)
            else:
                print(f"[{get_timestamp()}]     {Colors.RED}[Attempt {attempt}/{retries}] Giving up after timeout.")
    # if we exhausted all retries, re-raise or return a sentinel
    raise last_exc