from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from utils.colors import Colors
from utils.timing import get_timestamp
from utils.formatters import standardize_price_format

# ASYNC - Scrapes the passed URL (should be a Campuspoint link) for the product price
async def get_price_from_campuspoint(url, semaphore):
    # In cases where no URL is provided
    if url == "-":
        return "N/A"

    async with semaphore:
        try:
            async with async_playwright() as pw:
                browser = await pw.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(url, timeout=10000)
                price_handle = await page.wait_for_selector(".price-box span.price--current", state="visible", timeout=10_000)
                price = await price_handle.inner_text()
                await browser.close()
         

                # Debug line
                print(f"[{get_timestamp()}]     {Colors.GREEN}Campuspoint scrape completed{Colors.END}")

                return standardize_price_format(price)
        except Exception as e:
            print(f"[{get_timestamp()}]     {Colors.RED}Error getting Campuspoint price for {url}: {e}{Colors.END}")
            return "Error get_price_from_campuspoint()"
