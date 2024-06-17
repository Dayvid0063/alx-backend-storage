#!/usr/bin/env python3
"""Func that changes all topics of a school document"""


def update_topics(mongo_collection, name, topics):
    """Many rows update"""
    return mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
