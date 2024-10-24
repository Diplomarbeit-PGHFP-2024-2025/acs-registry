import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


def _get_database():
    client = MongoClient(os.getenv("CONNECTION_STRING"))
    return client["station_db"]


def get_collection():
    collection = _get_database()["stations"]
    collection.create_index([("expireAt", 1)], expireAfterSeconds=0)
    collection.create_index([("location", "2dsphere")])
    return collection
