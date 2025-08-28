from .client import *
import json

cl = ITscopeClient()

data = cl.get_product_by_id('21SQ0008GE')
print(data)
