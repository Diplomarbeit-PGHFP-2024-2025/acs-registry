from pymongo import MongoClient

def get_database():
    CONNECTION_STRING = "mongodb://root:root@localhost:27017"
    client = MongoClient(CONNECTION_STRING)
    return client["station_db"]

def get_collection():
    return get_database()["stations"]