#!/usr/bin/env python3
"""Func list documents in the collection"""


def list_all(mongo_collection):
    """returns list of documents in the collection"""
    return [u for u in mongo_collection.find()]
