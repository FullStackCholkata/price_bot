import requests, json
from requests.auth import HTTPBasicAuth
from .itscope_config import *

class ITscopeClient:
    def __init__(self):
        self.base = BASE_URL
        self.auth = HTTPBasicAuth(ACCOUNT_ID, API_KEY)
        self.headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}

    def get_product_by_id(self, sku: str, developer: bool = True, realtime: bool = True) -> dict:
        return_format = "developer" if developer else "standard"
        url = f"{self.base}/products/search/hstpid={sku}/{return_format}.json"
        print(f"DEBUG: Calling URL: {url}")
        
        ret = requests.get(url, params={"realtime": str(realtime).lower()},
                         auth=self.auth, headers=self.headers, timeout=20)
        ret.raise_for_status()
        
        raw_data = ret.json()
        print(f"DEBUG: Raw API response: {json.dumps(raw_data, indent=2)[:500]}...")
        
        filtered_json = self._get_suppliers(raw_data)
        print(f"DEBUG: Filtered result: {filtered_json}")
        return filtered_json

    def _get_suppliers(self, json_data: dict) -> list:
        suppliers_to_keep = {"Ingram Micro Österreich", "TD SYNNEX Austria", "ALSO Österreich"}
        print(f"DEBUG: Looking for suppliers: {suppliers_to_keep}")

        products = json_data.get("product", [])
        print(f"DEBUG: Found {len(products)} products")
        
        if products:
            supplier_items = products[0].get("supplierItems", [])
            print(f"DEBUG: Found {len(supplier_items)} supplier items")
            
            filtered = []
            for item in supplier_items:
                supplier = item.get("supplier", {})
                name = supplier.get("name")
                print(f"DEBUG: Checking supplier: {name}")
                
                if name in suppliers_to_keep:
                    print(f"DEBUG: Keeping supplier: {name}")
                    filtered.append({
                        "supplier_id": supplier.get("id"),
                        "supplier_name": name,
                        "supplierStockInfo": item.get("supplierStockInfo", [])
                    })
            
            print(f"DEBUG: Filtered {len(filtered)} suppliers")
            return filtered
        
        print("DEBUG: No products found")
        return []