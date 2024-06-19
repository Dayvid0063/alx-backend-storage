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
    inputs = f"{key}:inputs"
    outputs = f"{key}:outputs"

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
    redis_client = method.__self__._redis
    call_count = int(redis_client.get(key) or 0)
    print(f"{key} was called {call_count} times:")

    inputs = redis_client.lrange(f"{key}:inputs", 0, -1)
    outputs = redis_client.lrange(f"{key}:outputs", 0, -1)

    for input_args, output in zip(inputs, outputs):
        print(f"{key}(*{input_args.decode
                        ('utf-8')}) -> {output.decode('utf-8')}")


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

    def get(self,
            key: str,
            fn: Optional[Callable] = None) -> Union[
                str, bytes, int, float, None]:
        """Get data from Redis cache"""
        data = self._redis.get(key)
        if data is not None and fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """Get data as a str"""
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """Get data as an integer"""
        return self.get(key, int)
