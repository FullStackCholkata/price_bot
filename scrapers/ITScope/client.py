"""
ITScope B2B distributor platform API client module.

Provides HTTP API client functionality for accessing ITScope's B2B technology
distribution platform. Handles authentication, product lookups, and supplier
data filtering for Austrian distributors (Ingram Micro, ALSO, TD SYNNEX).
"""

import requests
from requests.auth import HTTPBasicAuth
from .itscope_config import *

class ITscopeClient:
    """
    HTTP API client for ITScope B2B distributor platform.
    
    Provides authenticated access to ITScope's product database and real-time
    stock information from major Austrian technology distributors. Handles
    API authentication, request formatting, and response processing.
    
    Attributes:
        base (str): Base URL for ITScope API endpoints
        auth (HTTPBasicAuth): HTTP Basic authentication credentials
        headers (dict): Standard HTTP headers for API requests
    """
    
    def __init__(self):
        """Initialize ITScope API client with authentication credentials."""
        self.base = BASE_URL
        self.auth = HTTPBasicAuth(ACCOUNT_ID, API_KEY)
        self.headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}

    def get_product_by_id(self, sku: str, developer: bool = True, realtime: bool = True) -> dict:
        """
        Retrieve product information and supplier stock data by SKU.
        
        Queries ITScope API for detailed product information including
        real-time stock levels from Austrian distributors. Filters results
        to include only relevant suppliers for the Austrian market.
        
        Args:
            sku (str): Product SKU/part number to lookup
            developer (bool): Use developer format for detailed response (default: True)
            realtime (bool): Include real-time stock information (default: True)
            
        Returns:
            list: Filtered supplier data for Ingram Micro, ALSO, and TD SYNNEX Austria
            
        Raises:
            requests.RequestException: If API request fails
            
        Usage:
            client = ITscopeClient()
            data = client.get_product_by_id("ABC123")
        """
        # Format API endpoint based on developer flag
        return_format = "developer" if developer else "standard"
        url = f"{self.base}/products/search/hstpid={sku}/{return_format}.json"
        
        # Make authenticated API request with realtime parameter
        ret = requests.get(url, params={"realtime": str(realtime).lower()},
                         auth=self.auth, headers=self.headers, timeout=20)
        ret.raise_for_status()
        
        # Parse JSON response
        raw_data = ret.json()
        
        # Filter to only include relevant Austrian suppliers
        filtered_json = self._get_suppliers(raw_data)
        return filtered_json

    def _get_suppliers(self, json_data: dict) -> list:
        # Define Austrian B2B distributors to include in results
        suppliers_to_keep = {"Ingram Micro Österreich", "TD SYNNEX Austria", "ALSO Österreich"}

        # Handle empty or invalid response data
        if not json_data:
            return []
            
        products = json_data.get("product", [])
        
        if not products:
            return []
            
        # Extract supplier items from first product
        supplier_items = products[0].get("supplierItems", [])
        
        # Filter suppliers and format response data
        filtered = []
        for item in supplier_items:
            supplier = item.get("supplier", {})
            name = supplier.get("name")
            
            # Only include relevant Austrian suppliers
            if name in suppliers_to_keep:
                filtered.append({
                    "supplier_id": supplier.get("id"),
                    "supplier_name": name,
                    "supplierStockInfo": item.get("supplierStockInfo", [])
                })
        
        return filtered