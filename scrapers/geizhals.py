from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from utils import Colors, get_timestamp, standardize_price_format, get_random_headers

# ASYNC - Scrapes the passed URL (should be a Geizhals link) for the product price
async def get_price_from_geizhals(url, semaphore):
    # In cases where no URL is provided
    if url == "-":
        return "N/A"

    async with semaphore:
        try:
            async with async_playwright() as pw:
                browser = await pw.chromium.launch(headless=True)
                page = await browser.new_page()
                headers = get_random_headers(referer=url) 
                await page.goto(url, timeout=10000)
                price_handle = await page.wait_for_selector('.offerlist', timeout=10000)
                html = await price_handle.inner_html()

                soup = BeautifulSoup(html, "html.parser")
                price = soup.find(class_="gh_price")
                if price is None:
                    return "No listings"
                else:
                    price_text = price.text    

                await browser.close()

                

                # Debug line
                print(f"[{get_timestamp()}]     {Colors.GREEN}Geizhals scrape completed{Colors.END}")

                return standardize_price_format(price_text)
        except Exception as e:
            print(f"[{get_timestamp()}]     {Colors.RED}Error getting Geizhals price for {url}: {e}{Colors.END}")
            return "Error in get_price_from_geizhals()"
