from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from utils import Colors, get_timestamp, standardize_price_format, get_random_headers

# Shared browser instance
_shared_browser = None
_playwright_instance = None

async def _get_or_create_browser():
    """Get shared browser or create new one"""
    global _shared_browser, _playwright_instance
    if _shared_browser is None:
        _playwright_instance = await async_playwright().start()
        _shared_browser = await _playwright_instance.chromium.launch(headless=True)
    return _shared_browser

async def _close_browser():
    """Internal function to close the shared browser"""
    global _shared_browser, _playwright_instance
    if _shared_browser:
        await _shared_browser.close()
        _shared_browser = None
    if _playwright_instance:
        await _playwright_instance.stop()
        _playwright_instance = None


# ASYNC - Scrapes the passed URL (should be a ITScope link) for the product availability
async def get_tdsynnex_from_itsocpe(url, semaphore, close_browser=False):
    # In cases where no URL is provided
    if url == "-":
        return "N/A"

    async with semaphore:
        try:
            # Automatically get or create shared browser
            browser = await _get_or_create_browser()
            
            # Apply headers at the context level:
            context = await browser.new_context(extra_http_headers=get_random_headers(referer=url))
            page = await context.new_page()

            try: 
                await page.goto(url, timeout=10000)
                html = await page.content()

                soup = BeautifulSoup(html, "html.parser")
                clt_group = soup.find('div', class_='v-clt-group')
                print(clt_group)
                if clt_group:
                    td_synnex = clt_group.find('a', string='TD SYNNEX Austria')

                    if td_synnex:
                        print(f"[{get_timestamp()}]     {Colors.GREEN}TD SYNNEX Austria available on ITScope{Colors.END}")
            
                    else:
                        print(f"[{get_timestamp()}]     {Colors.YELLOW}TD SYNNEX Austria not found on ITScope{Colors.END}")
             
                    
            finally:
                await context.close()
                
                # Close browser if requested
                if close_browser:
                    await _close_browser()

        except Exception as e:
            print(f"[{get_timestamp()}]     {Colors.RED}Error getting ITScope availability for {url}: {e}{Colors.END}")
            return "Error in get_availability_from_itsocpe()"

# async def get_availability_from_itsocpe2(url, semaphore, close_browser=False):
#     # In cases where no URL is provided
#     if url == "-":
#         return "N/A"

#     async with semaphore:
#         try:
#             # Automatically get or create shared browser
#             browser = await _get_or_create_browser()
                
#             # Apply headers at the context level:
#             context = await browser.new_context(extra_http_headers=get_random_headers(referer=url))
#             page = await context.new_page()

#             try: 
#                 await page.goto(url, timeout=10000)
#                 html = await page.content()

#                 soup = BeautifulSoup(html, "html.parser")
                
#                 # Different availability check for second function
#                 availability_elements = soup.find_all('div', class_='availability-status')
#                 if availability_elements:
#                     print(f"[{get_timestamp()}]     {Colors.GREEN}ITScope2 availability check completed{Colors.END}")
#                     return "Available"
#                 else:
#                     return "Not Available"
                    
#             finally:
#                 await context.close()
                
#                 # Close browser if requested
#                 if close_browser:
#                     await _close_browser()
                    
#         except Exception as e:
#             print(f"[{get_timestamp()}]     {Colors.RED}Error getting ITScope availability for {url}: {e}{Colors.END}")
#             return "Error in get_availability_from_itsocpe2()"
