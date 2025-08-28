from datetime import datetime
from utils import Colors, get_timestamp

def get_availability_for_ingram(json_data):
    for item in json_data:
        if item['supplier_name'] == 'Ingram Micro Österreich':
            stock_info = item['supplierStockInfo']
            if stock_info[1]['stockStatus'] != 1:  # everythign but 'available' returns the date
                available_when = stock_info[1]['stockAvailabilityDate']
                parsed = datetime.fromisoformat(available_when)
                formatted_date = parsed.strftime("%d/%m/%y")
                print(f"[{get_timestamp()}]     {Colors.YELLOW}Currently not available at Ingram Micro Österreich{Colors.END}")
                return formatted_date

            elif stock_info[1]['stockStatus'] == 8: # when 'unknown', it returns the last known value
                available_when = stock_info[0]['stockAvailabilityDate']
                parsed = datetime.fromisoformat(available_when)
                formatted_date = parsed.strftime("%d/%m/%y")
                print(f"[{get_timestamp()}]     {Colors.YELLOW}Unknown stock status at Ingram Micro Österreich{Colors.END}")
                return formatted_date

            else:   # just returns 'available'
                print(f"[{get_timestamp()}]     {Colors.GREEN}Available at Ingram Micro Österreich{Colors.END}")
                return stock_info[1]['stockStatusText']