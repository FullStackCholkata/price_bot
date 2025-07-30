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
                # Apply headers at the context level:
                context = await browser.new_context(extra_http_headers=get_random_headers(referer=url))
                page = await context.new_page()

                try: 
                    await page.goto(url, timeout=10000)
                    html = await page.content()

                    soup = BeautifulSoup(html, "html.parser")
                    price = soup.select_one("section#offerlist span.gh_price")
                    if price is None:
                        print(f"[{get_timestamp()}]     {Colors.YELLOW}No Geizhals listings founnd{Colors.END}")
                        return "No listings"
                    else:
                        price_text = price.text    
                finally:
                    await browser.close()

            
                # Debug line
                print(f"[{get_timestamp()}]     {Colors.GREEN}Geizhals scrape completed{Colors.END}")

                return standardize_price_format(price_text)
        except Exception as e:
            print(f"[{get_timestamp()}]     {Colors.RED}Error getting Geizhals price for {url}: {e}{Colors.END}")
            return "Error in get_price_from_geizhals()"
