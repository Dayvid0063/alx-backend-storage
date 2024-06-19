#!/usr/bin/env python3
"""Web caching using Redis"""


import redis
import requests
from functools import wraps
from typing import Callable


cl = redis.Redis()


def count(method: Callable) -> Callable:
    """Count the times a method is called"""
    @wraps(method)
    def wrapper(url: str) -> str:
        """Wrapper func for the method"""
        key = f"count:{url}"
        cl.incr(key)
        return method(url)
    return wrapper


def cache(method: Callable) -> Callable:
    """Cache the result of a method in Redis"""
    @wraps(method)
    def wrapper(url: str) -> str:
        """Wrapper func for the method"""
        key = f"page:{url}"
        res = cl.get(key)
        if res:
            return res.decode('utf-8')

        result = method(url)
        cl.setex(key, 10, result)
        return result
    return wrapper


@count
@cache
def get_page(url: str) -> str:
    """Gets the HTML content of a URL"""
    response = requests.get(url)
    return response.text
