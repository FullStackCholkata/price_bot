from datetime import datetime
from utils import Colors, get_timestamp

def get_availability_for_ingram(json_data) -> str:
    ret = 'No data'

    for item in json_data:
        if item['supplier_name'] == 'Ingram Micro Österreich':
            stock_info = item['supplierStockInfo']

            # If there are multiple occurenses of Ingram, it will skip the invalid one
            if stock_info[0]['stockStatus'] == "6" and stock_info[1]['stockStatus'] == "8":
                print("ENTERED IF 1")
                ret = stock_info[0]['stockStatusText']
                continue

            # if the stock status is either 'available' or 'unavailable', just return this
            if stock_info[1]['stockStatus'] in ("1", "6"):
                print("ENTERED IF 2")
                ret = stock_info[1]['stockStatusText']
                return ret

            # if is something else, it checks when it will be available 
            if stock_info[1]['stockStatus'] not in ("1", "6", "8"):
                print("ENTERED IF 3")
                ret = _format_date(stock_info[1]['stockAvailabilityDate'])
                return ret

            # finally secures the case where the real-time info might be unknown, in which case it falls back to
            # not-real-time info
            # teh acse where the not-real-time info is 'unavailable' is already checked on top
            elif stock_info[1]['stockStatus'] == "8":
                print("ENTERED IF 4")
                ret = _format_date(stock_info[0]['stockAvailabilityDate'])
                return ret
    
    return ret

def get_availability_for_also (json_data) -> str:
    ret = 'No data'

    for item in json_data:
        if item['supplier_name'] == 'ALSO Österreich':
            stock_info = item['supplierStockInfo']

            # If there are multiple occurenses of Ingram, it will skip the invalid one
            if stock_info[0]['stockStatus'] == "6" and stock_info[1]['stockStatus'] == "8":
                print("ENTERED IF 1")
                ret = stock_info[0]['stockStatusText']
                continue

            # if the stock status is either 'available' or 'unavailable', just return this
            if stock_info[1]['stockStatus'] in ("1", "6"):
                print("ENTERED IF 2")
                ret = stock_info[1]['stockStatusText']
                return ret

            # if is something else, it checks when it will be available 
            if stock_info[1]['stockStatus'] not in ("1", "6", "8"):
                print("ENTERED IF 3")
                ret = _format_date(stock_info[1]['stockAvailabilityDate'])
                return ret

            # finally secures the case where the real-time info might be unknown, in which case it falls back to
            # not-real-time info
            # teh acse where the not-real-time info is 'unavailable' is already checked on top
            elif stock_info[1]['stockStatus'] == "8":
                print("ENTERED IF 4")

                if stock_info[0]['stockStatus'] in ("1", "8"):
                    ret = stock_info[0]['stockStatusText']
                    return ret

                ret = _format_date(stock_info[0]['stockAvailabilityDate'])
                return ret
    
    return ret

def get_availability_for_tdsynnex(json_data) -> str:
    ret = 'No data'

    for item in json_data:
        if item['supplier_name'] == 'TD SYNNEX Austria':
            stock_info = item['supplierStockInfo']

            # If there are multiple occurenses of Ingram, it will skip the invalid one
            if stock_info[0]['stockStatus'] == "6" and stock_info[1]['stockStatus'] == "8":
                print("ENTERED IF 1")
                ret = stock_info[0]['stockStatusText']
                continue

            # if the stock status is either 'available' or 'unavailable', just return this
            if stock_info[1]['stockStatus'] in ("1", "6"):
                print("ENTERED IF 2")
                ret = stock_info[1]['stockStatusText']
                return ret

            # if is something else, it checks when it will be available 
            if stock_info[1]['stockStatus'] not in ("1", "6", "8"):
                print("ENTERED IF 3")
                ret = _format_date(stock_info[1]['stockAvailabilityDate'])
                return ret

            # finally secures the case where the real-time info might be unknown, in which case it falls back to
            # not-real-time info
            # teh acse where the not-real-time info is 'unavailable' is already checked on top
            elif stock_info[1]['stockStatus'] == "8":
                print("ENTERED IF 4")
                ret = _format_date(stock_info[0]['stockAvailabilityDate'])
                return ret
    
    return ret

def _format_date(date: str) -> str:
    parsed = datetime.fromisoformat(date)
    ret = parsed.strftime("%d/%m/%y")
    return ret
