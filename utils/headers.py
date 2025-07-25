import random
from config import USER_AGENTS

def get_random_headers(referer=None):
    """Generate random headers to mimic real browser requests"""
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': random.choice([
            'en-US,en;q=0.9',
            'de-DE,de;q=0.9,en;q=0.8',
            'en-GB,en;q=0.9'
        ]),
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0'
    }
    
    if referer:
        headers['Referer'] = referer
        
    return headers