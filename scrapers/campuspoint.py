"""
Campuspoint educational technology retailer scraper module.

Provides asynchronous web scraping functionality for extracting product prices
from Campuspoint, an Austrian educational technology e-commerce platform.
Uses Playwright for browser automation with proper availability detection
and anti-bot measures.
"""

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from utils import Colors, get_timestamp, standardize_price_format, get_random_headers

async def get_price_from_campuspoint(url, semaphore):
    """
    Scrape product price from Campuspoint using browser automation.
    
    Extracts current product price from Campuspoint product pages with
    automatic detection of product availability. Handles out-of-stock
    scenarios and implements anti-detection measures.
    
    Args:
        url (str): Campuspoint product URL to scrape, or "-" for no URL
        semaphore (asyncio.Semaphore): Rate limiting semaphore for concurrent requests
        
    Returns:
        str: Standardized price text (€ format) or availability status
        
    Usage:
        price = await get_price_from_campuspoint(url, semaphore)
    """
    # Handle cases where no URL is provided
    if url == "-":
        return "N/A"

    async with semaphore:
        try:
            async with async_playwright() as pw:
                # Launch browser with anti-detection headers
                browser = await pw.chromium.launch(headless=True)
                context = await browser.new_context(extra_http_headers=get_random_headers(referer=url))
                page = await context.new_page()
                await page.goto(url, timeout=10000)
                
                # Check for product availability warnings
                product_not_available = await page.query_selector('div.warning.message.flex.items-center')
                if product_not_available:
                    print(f"[{get_timestamp()}]     {Colors.YELLOW}No Campuspoint listings found{Colors.END}")
                    return "No listings"
                    
                # Extract current price from product page
                price_handle = await page.wait_for_selector(".price-box span.price--current", state="visible", timeout=10_000)
                price = await price_handle.inner_text()
                await browser.close()

                print(f"[{get_timestamp()}]     {Colors.GREEN}Campuspoint scrape completed{Colors.END}")

                return standardize_price_format(price)
        except Exception as e:
            print(f"[{get_timestamp()}]     {Colors.RED}Error getting Campuspoint price for {url}: {e}{Colors.END}")
            return "Error get_price_from_campuspoint()"
