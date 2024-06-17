#!/usr/bin/env python3
"""Func that returns the list of school having a specific topic"""


def schools_by_topic(mongo_collection, topic):
    """Find and return list by topic"""
    return mongo_collection.find({"topics": topic})
