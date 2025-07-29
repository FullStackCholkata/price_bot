import asyncio
import random
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

async def retry_with_backoff(func, max_retries=3, base_delay=1):
    for attempt in range(max_retries):
        try:
            return await func()
        except (TimeoutError, PlaywrightTimeoutError, asyncio.TimeoutError) as e:
            if attempt == max_retries - 1:
                print(f"Max retries reached. Final error: {e}")
                return "Timeout after retries"
            
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            print(f"Timeout on attempt {attempt + 1}, retrying in {delay:.2f} seconds...")
            await asyncio.sleep(delay)
        except Exception as e:
            print(f"Non-timeout error: {e}")
            raise e