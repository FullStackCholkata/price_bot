import asyncio
from utils import Colors, get_timestamp, retry_after_timeout
from scrapers import *

# Processes a single SKU's data concurrently
async def process_sku(row, last_prices, semaphore):
    sku = row["SKU"]
    url_gh = row["Geizhals link"]
    url_camp = row["Campuspoint link"]
    url_edu = row["edustore link"]
    url_it = row["ITScope link"]
    itclient = ITscopeClient()

    # Extracts first block for comparison
    sku_first_block = sku.split('-')[0]
    
    # Debug line
    print(f"[{get_timestamp()}] {Colors.BLUE}Processing SKU: {sku}{Colors.END}")

    tasks = []

    # Checks to make sure the SKU isn't the first being processed and that it is a sub-SKU of the privious one
    if last_prices and any(item in set(sku.split('-')) for item in set(last_prices["SKU"].split('-'))):
        print(f"[{get_timestamp()}]     {Colors.YELLOW}Using cached prices for SKU group: {sku_first_block}{Colors.END}")
        
        # Use cached values for same SKU group
        tasks.append(("Geizhals Preis", asyncio.create_task(asyncio.sleep(0.1, result=last_prices["Geizhals Preis"]))))
        tasks.append(("Campuspoint Preis", asyncio.create_task(asyncio.sleep(0.1, result=last_prices["Campuspoint Preis"]))))
        tasks.append(("Verfügbar", asyncio.create_task(asyncio.sleep(0.1, result=last_prices["Verfügbar"]))))
        tasks.append(("edustore VK", retry_after_timeout(get_price_from_edustore, url_edu, semaphore)))
        tasks.append(("INGRAM", asyncio.create_task(asyncio.sleep(0.1, result=last_prices["INGRAM"]))))
            
    else:
        print(f"[{get_timestamp()}]     {Colors.YELLOW}Fetching new prices for SKU group: {sku_first_block}{Colors.END}")
        
        if url_gh != "^":
            tasks.append(("Geizhals Preis", retry_after_timeout(get_price_from_geizhals, url_gh, semaphore)))
        else:
            tasks.append(("Geizhals Preis", asyncio.create_task(asyncio.sleep(0.1, result="No valid URL"))))
        
        # Add small delay before next scraper
        await asyncio.sleep(1)
        
        if url_camp != "^":
            tasks.append(("Campuspoint Preis", retry_after_timeout(get_price_from_campuspoint, url_camp, semaphore)))
        else:
            tasks.append(("Campuspoint Preis", asyncio.create_task(asyncio.sleep(0.1, result="No valid URL"))))

        # Add small delay before next scraper
        await asyncio.sleep(1)

        if url_edu != "^":
            tasks.append(("edustore VK", retry_after_timeout(get_price_from_edustore, url_edu, semaphore)))
            tasks.append(("Verfügbar", retry_after_timeout(get_stock_from_edustore, url_edu, semaphore)))
        else:
            tasks.append(("edustore VK", asyncio.create_task(asyncio.sleep(0.1, result="No valid URL"))))
            tasks.append(("Verfügbar", asyncio.create_task(asyncio.sleep(0.1, result="No valid URL"))))

        # Add small delay before next scraper
        await asyncio.sleep(1)

        # Fix ITScope integration - get data synchronously then process
        try:
            print(f"[{get_timestamp()}] {Colors.CYAN}Calling ITScope for SKU: {sku}{Colors.END}")
            data = itclient.get_product_by_id(sku)
            print(f"[{get_timestamp()}] {Colors.CYAN}ITScope returned: {data}{Colors.END}")
            
            if data:
                ingram_availability = get_availability_for_ingram(data)
                print(f"[{get_timestamp()}] {Colors.CYAN}Ingram availability result: {ingram_availability}{Colors.END}")
            else:
                print(f"[{get_timestamp()}] {Colors.RED}ITScope returned empty data{Colors.END}")
                ingram_availability = "No data from ITScope"
                
            tasks.append(("INGRAM", asyncio.create_task(asyncio.sleep(0.1, result=ingram_availability))))
        except Exception as e:
            print(f"[{get_timestamp()}] {Colors.RED}ITScope error for {sku}: {e}{Colors.END}")
            tasks.append(("INGRAM", asyncio.create_task(asyncio.sleep(0.1, result="Error fetching data"))))

    results = await asyncio.gather(*[task[1] for task in tasks])
    
    # Builds prices dictionary from results
    prices = {}
    for i, (key, _) in enumerate(tasks):
        prices[key] = results[i]
    
    return sku, prices
