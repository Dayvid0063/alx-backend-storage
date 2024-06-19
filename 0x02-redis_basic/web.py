#!/usr/bin/env python3
"""Request caching and tracking"""


import requests
import redis


redis_client = redis.Redis()


def get_page(url: str) -> str:
    """Gets the HTML content and caches it with expiry"""
    count_key = f"count:{url}"
    redis_client.incr(count_key)

    cache_key = f"content:{url}"
    cc = redis_client.get(cache_key)
    if cc:
        return cc.decode('utf-8')

    response = requests.get(
        f"http://slowwly.robertomurray.co.uk/delay/1000/url/{url}")
    hc = response.text
    redis_client.setex(cache_key, 10, hc)

    return hc
