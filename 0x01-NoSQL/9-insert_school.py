#!/usr/bin/env python3
"""Func inserts new document in a collection based on kwargs"""


def insert_school(mongo_collection, **kwargs):
    """Inserts and returns new ID"""
    return mongo_collection.insert_one(kwargs).inserted_id
