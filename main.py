import asyncio
from datetime import datetime
from utils import Colors, get_timestamp, format_availability_column
from google_sheets import setup_google_worksheet, get_data, get_sku_list
from processors import process_sku
from config import COLUMN_MAP, SEMAPHORE_LIMIT

async def main_async():
    # Time stamp used for run-time calculation only; ignore
    start_time = datetime.now()
    
    try:
        # Setup
        worksheet = setup_google_worksheet()
        records = get_data(worksheet)
        sku_lookup_table = get_sku_list(worksheet)
        
        # Semaphore to limit concurrent requests
        semaphore = asyncio.Semaphore(SEMAPHORE_LIMIT)
        
        last_prices = {}

        for row in records:
            try:

                # Adds a 1 second delay between row processings, so there is some time between requests
                await asyncio.sleep(1)

                # Process SKU concurrently
                sku, prices = await process_sku(row, last_prices, semaphore)
                print(prices)

                if sku in sku_lookup_table:
                    row_index = sku_lookup_table[sku]

                    batch_data = []

                    for price_key, price_value in prices.items():
                        col_letter = COLUMN_MAP[price_key]   # e.g. "D"
                        cell_range = f"{col_letter}{row_index}"    # e.g. "D5"

                        batch_data.append({
                            "range":  cell_range,
                            "values": [[ price_value ]]      # must be a 2D array: rows → [cells]
                        })

                    # Debug line
                    print(f"[{get_timestamp()}]     {Colors.BLUE}Updating cells: {batch_data}{Colors.END}")  

                    try:
                        worksheet.batch_update(batch_data, value_input_option='RAW')

                        availability_value = prices.get("Verfügbar")
                        if availability_value is not None:
                            format_availability_column(worksheet, row_index, availability_value)

                        print(f"[{get_timestamp()}]     {Colors.GREEN}Successfully updated {sku}{Colors.END}")
                    except Exception as e:
                        print(f"[{get_timestamp()}]     {Colors.RED}Error updating spreadsheet for SKU {sku}: {e}{Colors.END}")

                    last_prices = prices
                    last_prices["SKU"] = sku
                else:
                    print(f"[{get_timestamp()}]     {Colors.RED}SKU {sku} not found in lookup table{Colors.END}")
                    
            except Exception as e:
                print(f"[{get_timestamp()}]     {Colors.RED}Error processing row for SKU {sku}: {e}{Colors.END}")
                continue
                
    except Exception as e:
        print(f"[{get_timestamp()}] {Colors.RED}Fatal error in main(): {e}{Colors.END}")
    
    # Calculates how long the script took to finish
    end_time = datetime.now()
    execution_time = end_time - start_time

    total_seconds = int(execution_time.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    # Removes 0s from the final runtime
    time_parts = []
    if hours > 0:
        time_parts.append(f"{hours}h")
    if minutes > 0:
        time_parts.append(f"{minutes}m")
    time_parts.append(f"{seconds}s")

    time_str = " ".join(time_parts)
    print(f"[{get_timestamp()}] {Colors.YELLOW}Script completed in {time_str}{Colors.END}")


def main():
    # Runs the async main function
    asyncio.run(main_async())


if __name__ == '__main__':
    main()