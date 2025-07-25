from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from utils.colors import Colors
from utils.timing import get_timestamp
from utils.formatters import standardize_price_format

# ASYNC - Scrapes the passed URL (should be a edustore link) for the product price
async def get_price_from_edustore(url, semaphore):
    # In cases where no URL is provided
    if url == "-":
        return "N/A"

    async with semaphore:
        try:
            async with async_playwright() as pw:
                browser = await pw.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(url, timeout=10000)
                await page.wait_for_selector('.price-wrapper', timeout=10000)
                html = await page.content()
                
                soup = BeautifulSoup(html, "html.parser")
                price_text = soup.find(class_="price").text
                
                await browser.close()

                # Debug line
                print(f"[{get_timestamp()}]     {Colors.GREEN}edustore scrape completed{Colors.END}")

                return standardize_price_format(price_text)
        except Exception as e:
            print(f"[{get_timestamp()}]     {Colors.RED}Error getting Edustore price for {url}: {e}{Colors.END}")
            return "Error get_price_from_edustore()"


# ASYNC - Scrapes the passed URL (should be a edustore link) for the product stock/availability
async def get_stock_from_edustore(url, semaphore):
    if url == "-":
        return "N/A"
    
    async with semaphore:
        try:
            async with async_playwright() as pw:
                browser = await pw.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(url, timeout=10000)
                await page.wait_for_selector('.product-info-stock-sku', timeout=10000)
                available_element = await page.query_selector('.product-info-stock-sku .stock.available')
                preoderable_element = await page.query_selector('.product-info-stock-sku .stock.lagerstatus.lagerstatus-green')
                unavailable_element = await page.query_selector('.product-info-stock-sku .stock.unavailable')

                await browser.close()

                # Debug line
                print(f"[{get_timestamp()}]     {Colors.GREEN}edustore availability scrape completed{Colors.END}")
                
                if available_element:
                    return "Ja"
                elif unavailable_element:
                    return "Nein"
                elif preoderable_element:
                    return "Vorbestellbar"
                else:
                    return "?"
        except Exception as e:
            print(f"[{get_timestamp()}]     {Colors.RED}Error getting Edustore stock for {url}: {e}{Colors.END}")
            return "Error get_stock_from_edustore()"
