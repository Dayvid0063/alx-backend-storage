#!/usr/bin/env python3
"""Request caching and tracking"""


import requests
import redis


cli = redis.Redis()


def get_page(url: str) -> str:
    """Gets the HTML content and caches it with expiry"""
    count_key = f"count:{url}"
    cli.incr(count_key)

    response = requests.get(url)
    hc = response.text

    cache_key = f"content:{url}"
    cli.setex(cache_key, 10, hc)

    return hc
