import gspread

# Gets all data from the table; separates the table header from the data rows;
# Returns a dictionary containing each row
def get_data(worksheet: gspread.Worksheet) -> dict:
    data = worksheet.get_all_values()
    headers = data[0]
    data_rows = data[1:]
    
    return [dict(zip(headers, row)) for row in data_rows]


# Returns a SKU look-up table for quick SKU-checks
def get_sku_list(worksheet: gspread.Worksheet) -> dict:
    all_values = worksheet.col_values(1)
    skus = all_values[1:]

    sku_to_index = {
        sku: index + 2
        for index, sku in enumerate(skus)
    }

    return sku_to_index
