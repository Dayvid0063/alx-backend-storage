#!/usr/bin/env python3
"""Web caching using Redis"""


import redis
import requests
from functools import wraps
from typing import Callable


cl = redis.Redis()


def cache(method: Callable) -> Callable:
    """Cache the result of a method in Redis"""
    @wraps(method)
    def wrapper(url) -> str:
        """Wrapper func for the method"""
        cl.incr(f'count:{url}')
        result = cl.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        cl.set(f'count:{url}', 0)
        cl.setex(f'result:{url}', 10, result)
        return result
    return wrapper


@cache
def get_page(url: str) -> str:
    """Gets the HTML content of a URL"""
    res = requests.get(url)
    return res.text
