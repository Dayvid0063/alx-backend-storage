#!/usr/bin/env python3
"""Web caching using Redis"""


import redis
import requests


cl = redis.Redis()
count = 0


def get_page(url: str) -> str:
    """Gets page and caches its content using Redis"""
    cl.set(f"cached:{url}", count)

    r = requests.get(url)

    cl.incr(f"count:{url}")
    cl.setex(f"cached:{url}", 10, cl.get(f"cached:{url}"))
    return r.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
