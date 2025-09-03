"""
Geizhals.at price comparison platform scraper module.

Provides asynchronous web scraping functionality for extracting product prices
from Geizhals.at, Austria's leading price comparison website. Uses Playwright
for browser automation with anti-bot detection measures including randomized
headers and proper user agent rotation.
"""

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from utils import Colors, get_timestamp, standardize_price_format, get_random_headers

async def get_price_from_geizhals(url, semaphore):
    """
    Scrape product price from Geizhals.at using browser automation.
    
    Extracts the lowest available price from Geizhals product listings using
    Playwright browser automation. Implements rate limiting via semaphore and
    anti-detection measures including randomized headers and referer spoofing.
    
    Args:
        url (str): Geizhals product URL to scrape, or "-" for no URL
        semaphore (asyncio.Semaphore): Rate limiting semaphore for concurrent requests
        
    Returns:
        str: Standardized price text (€ format) or error message
        
    Usage:
        price = await get_price_from_geizhals(url, semaphore)
    """
    # Handle cases where no URL is provided
    if url == "-":
        return "N/A"

    async with semaphore:
        try:
            async with async_playwright() as pw:
                # Launch headless browser with anti-detection measures
                browser = await pw.chromium.launch(headless=True)
                context = await browser.new_context(extra_http_headers=get_random_headers(referer=url))
                page = await context.new_page()

                try: 
                    await page.goto(url, timeout=10000)
                    html = await page.content()

                    # Parse HTML and extract price from offer listings
                    soup = BeautifulSoup(html, "html.parser")
                    price = soup.select_one("section#offerlist span.gh_price")
                    if price is None:
                        print(f"[{get_timestamp()}]     {Colors.YELLOW}No Geizhals listings found{Colors.END}")
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
