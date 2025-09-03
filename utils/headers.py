"""
HTTP header generation utilities for web scraping operations.

Provides realistic browser header generation to avoid bot detection
and ensure successful web scraping across different e-commerce platforms.
Includes randomized user agents and browser-like request headers.
"""

import random
from config import USER_AGENTS

def get_random_headers(referer=None):
    """
    Generate randomized HTTP headers that mimic real browser requests.
    
    Creates realistic browser headers including randomized user agents,
    accept headers, and security attributes to avoid bot detection
    mechanisms commonly used by e-commerce websites.
    
    Args:
        referer (str, optional): Referer URL to include in headers
        
    Returns:
        dict: Complete set of HTTP headers for web requests
        
    Usage:
        headers = get_random_headers(referer="https://example.com")
        response = requests.get(url, headers=headers)
    """
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