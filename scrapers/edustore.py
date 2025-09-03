"""
edustore educational products retailer scraper module.

Provides asynchronous web scraping functionality for extracting both product
prices and stock availability from edustore, an Austrian educational products
e-commerce platform. Implements dual functionality for price and inventory
monitoring with robust error handling.
"""

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from utils import Colors, get_timestamp, standardize_price_format, get_random_headers

async def get_price_from_edustore(url, semaphore):
    """
    Scrape product price from edustore using browser automation.
    
    Extracts current product price from edustore product pages using
    Playwright browser automation. Waits for price elements to load
    and implements proper error handling for network issues.
    
    Args:
        url (str): edustore product URL to scrape, or "-" for no URL
        semaphore (asyncio.Semaphore): Rate limiting semaphore for concurrent requests
        
    Returns:
        str: Standardized price text (€ format) or error status
        
    Usage:
        price = await get_price_from_edustore(url, semaphore)
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
                
                # Wait for price wrapper to ensure content is loaded
                await page.wait_for_selector('.price-wrapper', timeout=10000)
                html = await page.content()
                
                # Extract price using BeautifulSoup
                soup = BeautifulSoup(html, "html.parser")
                price_text = soup.find(class_="price").text
                
                await browser.close()

                print(f"[{get_timestamp()}]     {Colors.GREEN}edustore scrape completed{Colors.END}")

                return standardize_price_format(price_text)
        except Exception as e:
            print(f"[{get_timestamp()}]     {Colors.RED}Error getting Edustore price for {url}: {e}{Colors.END}")
            raise e 


async def get_stock_from_edustore(url, semaphore):
    """
    Scrape product stock availability from edustore using browser automation.
    
    Extracts current stock status from edustore product pages to determine
    product availability. Provides stock information for inventory monitoring
    and procurement planning.
    
    Args:
        url (str): edustore product URL to scrape, or "-" for no URL
        semaphore (asyncio.Semaphore): Rate limiting semaphore for concurrent requests
        
    Returns:
        str: Stock availability status ("Ja", "Nein", "Vorbestellbar", etc.)
        
    Usage:
        stock = await get_stock_from_edustore(url, semaphore)
    """
    if url == "-":
        return "N/A"
    
    async with semaphore:
        try: 
            async with async_playwright() as pw:
                # Launch browser and navigate to product page
                browser = await pw.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(url, timeout=10000)
                
                # Wait for stock information section to load
                await page.wait_for_selector('.product-info-stock-sku', timeout=10000)
                
                # Check for different stock status indicators
                available_element = await page.query_selector('.product-info-stock-sku .stock.available')
                preoderable_element_green = await page.query_selector('.product-info-stock-sku .stock.lagerstatus.lagerstatus-green')
                preoderable_element_orange = await page.query_selector('.product-info-stock-sku .stock.lagerstatus.lagerstatus-orange')
                unavailable_element = await page.query_selector('.product-info-stock-sku .stock.unavailable')

                await browser.close()

                print(f"[{get_timestamp()}]     {Colors.GREEN}edustore availability scrape completed{Colors.END}")
                
                # Determine stock status based on available elements
                if available_element:
                    return "Ja"
                elif unavailable_element:
                    return "Nein"
                elif preoderable_element_green or preoderable_element_orange:
                    return "Vorbestellbar"
                else:
                    return "?"
        except Exception as e: 
            print(f"[{get_timestamp()}]     {Colors.RED}Error getting Edustore stock for {url}: {e}{Colors.END}")
            raise e 
