#!/usr/bin/env python3
"""Class definition for Redis cache"""


import redis
import uuid
from functools import wraps
from typing import Union, Callable, Optional


def count_calls(method: Callable) -> Callable:
    """Count the times a method is called"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper func for the method"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Store the history of inputs and outputs"""
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper func for the method"""
        self._redis.rpush(inputs, str(args))
        res = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(res))
        return res
    return wrapper


def replay(method: Callable) -> None:
    """Replays the history of a method"""
    key = method.__qualname__
    redis_client = redis.Redis()
    call_count = redis_client.get(key).decode("utf-8")
    print("{} was called {} times:".format(key, call_count))

    inputs = redis_client.lrange(key + ":inputs", 0, -1)
    outputs = redis_client.lrange(key + ":outputs", 0, -1)
    for in_arg, out in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(key, in_arg.decode('utf-8'),
                                     out.decode('utf-8')))


class Cache:
    """Methods to handle Redis cache"""
    def __init__(self) -> None:
        """Initialize Redis"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis cache"""
        info = str(uuid.uuid4())
        self._redis.set(info, data)
        return info

    def get(self, key: str, fn: Optional[Callable] = None)\
            -> Union[str, bytes, int, float, None]:
        """Get data from redis cache"""
        data = self._redis.get(key)
        if data is not None and fn is not None and callable(fn):
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """Get data as a str"""
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """Get data as an integer"""
        return self.get(key, int)
