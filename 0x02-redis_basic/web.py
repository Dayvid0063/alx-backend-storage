#!/usr/bin/env python3
"""Web caching using Redis"""


import redis
import requests


cl = redis.Redis()


def get_page(url: str) -> str:
    """Gets page and caches its content using Redis"""
    cont = cl.get(f"cached:{url}")
    if cont:
        return cont.decode('utf-8')

    r = requests.get(url)
    r.raise_for_status()

    cl.setex(f"cached:{url}", 10, r.text)
    cl.incr(f"count:{url}")
    return r.text
