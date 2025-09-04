"""
SKU processing module for concurrent price and availability data collection.

Orchestrates the main business logic for processing individual product SKUs,
including smart caching, concurrent web scraping, and data aggregation from
multiple e-commerce platforms and B2B distributors.

Key features:
- Intelligent caching for SKU variants to reduce API calls
- Concurrent scraping from multiple sources with rate limiting
- Integration with Geizhals, Campuspoint, edustore, and ITScope platforms
- Error handling and retry mechanisms for robust operation
"""

import json
import asyncio
from utils import Colors, get_timestamp, retry_after_timeout
from scrapers import *

async def process_sku(row, last_prices, semaphore):
    """
    Process a single SKU to collect price and availability data from multiple sources.
    
    Implements intelligent caching for SKU variants (e.g., different configurations
    of the same base product) to minimize redundant API calls. Orchestrates
    concurrent data collection from e-commerce sites and B2B distributors.
    
    Args:
        row (dict): Spreadsheet row data containing SKU and URLs
        last_prices (dict): Previously collected prices for caching optimization  
        semaphore (asyncio.Semaphore): Rate limiting semaphore for concurrent requests
        
    Returns:
        tuple: (sku_string, prices_dict) containing SKU and collected price data
        
    Usage:
        sku, prices = await process_sku(row_data, cache, semaphore)
    """
    # Extract SKU components and URLs from spreadsheet row
    sku = row["SKU"]
    url_gh = row["Geizhals link"]
    url_camp = row["Campuspoint link"]
    url_edu = row["edustore link"]
    itclient = ITscopeClient()

    # Extract base SKU for caching comparison (before first hyphen)
    sku_first_block = sku.split('-')[0]
    
    print(f"[{get_timestamp()}] {Colors.BLUE}Processing SKU: {sku}{Colors.END}")

    tasks = []

    # Implement smart caching: reuse data for SKU variants of the same base product
    if last_prices and any(item in set(sku.split('-')) for item in set(last_prices["SKU"].split('-'))):
        print(f"[{get_timestamp()}]     {Colors.YELLOW}Using cached prices for SKU group: {sku_first_block}{Colors.END}")
        
        # Reuse cached values for same SKU group (reduces API calls)
        tasks.append(("Geizhals Preis", asyncio.create_task(asyncio.sleep(0.1, result=last_prices["Geizhals Preis"]))))
        tasks.append(("Campuspoint Preis", asyncio.create_task(asyncio.sleep(0.1, result=last_prices["Campuspoint Preis"]))))
        tasks.append(("Verfügbar", asyncio.create_task(asyncio.sleep(0.1, result=last_prices["Verfügbar"]))))
        tasks.append(("edustore VK", retry_after_timeout(get_price_from_edustore, url_edu, semaphore)))
        tasks.append(("INGRAM", asyncio.create_task(asyncio.sleep(0.1, result=last_prices["INGRAM"]))))
        tasks.append(("ALSO", asyncio.create_task(asyncio.sleep(0.1, result=last_prices["ALSO"]))))
        tasks.append(("TD Synnex", asyncio.create_task(asyncio.sleep(0.1, result=last_prices["TD Synnex"]))))
            
    else:
        print(f"[{get_timestamp()}]     {Colors.YELLOW}Fetching new prices for SKU group: {sku_first_block}{Colors.END}")
        
        # Scrape fresh data from all sources with rate limiting
        if url_gh != "^":
            tasks.append(("Geizhals Preis", retry_after_timeout(get_price_from_geizhals, url_gh, semaphore)))
        else:
            tasks.append(("Geizhals Preis", asyncio.create_task(asyncio.sleep(0.1, result="No valid URL"))))
        
        # Stagger requests to avoid overwhelming servers
        await asyncio.sleep(1)
        
        if url_camp != "^":
            tasks.append(("Campuspoint Preis", retry_after_timeout(get_price_from_campuspoint, url_camp, semaphore)))
        else:
            tasks.append(("Campuspoint Preis", asyncio.create_task(asyncio.sleep(0.1, result="No valid URL"))))

        # Continue staggered scraping for remaining sources
        await asyncio.sleep(1)

        if url_edu != "^":
            tasks.append(("edustore VK", retry_after_timeout(get_price_from_edustore, url_edu, semaphore)))
            tasks.append(("Verfügbar", retry_after_timeout(get_stock_from_edustore, url_edu, semaphore)))
        else:
            tasks.append(("edustore VK", asyncio.create_task(asyncio.sleep(0.1, result="No valid URL"))))
            tasks.append(("Verfügbar", asyncio.create_task(asyncio.sleep(0.1, result="No valid URL"))))

        await asyncio.sleep(1)

        # Query ITScope B2B distributors for availability data
        try:
            print(f"[{get_timestamp()}]     {Colors.CYAN}Calling ITScope for SKU: {sku}{Colors.END}")
            data = itclient.get_product_by_id(sku_first_block)
            print(f"[{get_timestamp()}]     {Colors.CYAN}ITScope returned:\n {json.dumps(data, indent=4, ensure_ascii=False)}{Colors.END}")

            if data:
                # Process availability data for each Austrian distributor
                ingram_availability = get_availability_for_ingram(data)
                print(f"[{get_timestamp()}]     {Colors.GREEN}Ingram availability result: {ingram_availability}{Colors.END}")

                also_availability = get_availability_for_also(data)
                print(f"[{get_timestamp()}]     {Colors.GREEN}ALSO availability result: {also_availability}{Colors.END}")

                tdsynnex_availability = get_availability_for_tdsynnex(data)
                print(f"[{get_timestamp()}]     {Colors.GREEN}TD Synnex availability result: {tdsynnex_availability}{Colors.END}")
            else:
                print(f"[{get_timestamp()}]     {Colors.RED}ITScope returned empty data{Colors.END}")
                ingram_availability = "no data"
                also_availability = "no data"
                tdsynnex_availability = "no data"
                
            # Add distributor availability data to task list
            tasks.append(("INGRAM", asyncio.create_task(asyncio.sleep(0.1, result=ingram_availability))))
            tasks.append(("ALSO", asyncio.create_task(asyncio.sleep(0.1, result=also_availability))))
            tasks.append(("TD Synnex", asyncio.create_task(asyncio.sleep(0.1, result=tdsynnex_availability))))

        except json.JSONDecodeError as e:
            print(f"[{get_timestamp()}]     {Colors.RED}ITScope error for {sku}: No such product found.{Colors.END}")
            tasks.append(("INGRAM", asyncio.create_task(asyncio.sleep(0.1, result="no such product"))))
            tasks.append(("ALSO", asyncio.create_task(asyncio.sleep(0.1, result="no such product"))))
            tasks.append(("TD Synnex", asyncio.create_task(asyncio.sleep(0.1, result="no such product"))))
        except Exception as e:
            print(f"[{get_timestamp()}]     {Colors.RED}ITScope error for {sku}: {e}{Colors.END}")
            tasks.append(("INGRAM", asyncio.create_task(asyncio.sleep(0.1, result="error fetching data"))))
            tasks.append(("ALSO", asyncio.create_task(asyncio.sleep(0.1, result="error fetching data"))))
            tasks.append(("TD Synnex", asyncio.create_task(asyncio.sleep(0.1, result="error fetching data"))))

    # Execute all data collection tasks concurrently
    results = await asyncio.gather(*[task[1] for task in tasks])
    
    # Build structured prices dictionary from task results
    prices = {}
    for i, (key, _) in enumerate(tasks):
        prices[key] = results[i]
    
    return sku, prices
