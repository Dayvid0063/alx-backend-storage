#!/usr/bin/env python3
"""Web caching using Redis"""


import redis
import requests


cl = redis.Redis()
num = 0


def get_page(url: str) -> str:
    """Gets page and caches its content using Redis"""
    cl.set(f"cached:{url}", num)

    r = requests.get(url)

    cl.setex(f"cached:{url}", 10, cl.get(f"cached:{url}"))
    cl.incr(f"count:{url}")
    return r.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
