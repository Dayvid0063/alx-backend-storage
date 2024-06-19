#!/usr/bin/env python3
"""Request caching and tracking"""


import requests
import redis


redis_client = redis.Redis()


def get_page(url: str) -> str:
    """Gets the HTML content and caches it with expiry"""
    count_key = f"count:{url}"
    redis_client.incr(count_key)

    response = requests.get(url)
    hc = response.text

    cache_key = f"content:{url}"
    redis_client.setex(cache_key, 10, hc)

    return hc
