#!/usr/bin/env python3
"""Web caching using Redis"""


import requests
import redis
from functools import wraps


cl = redis.Redis()


def count(method):
    """Count the times a URL is accessed"""
    @wraps(method)
    def wrapper(url):
        key = f"count:{url}"
        cl.incr(key)
        return method(url)
    return wrapper


def cache(method):
    """Cache URL responses with expiration"""
    @wraps(method)
    def wrapper(url):
        key = f"cache:{url}"
        c_res = cl.get(key)
        if c_res:
            return c_res.decode('utf-8')

        result = method(url)
        cl.setex(key, 10, result)
        return result
    return wrapper


@count
@cache
def get_page(url):
    """Gets the HTML content of a URL"""
    response = requests.get(url)
    return response.text
