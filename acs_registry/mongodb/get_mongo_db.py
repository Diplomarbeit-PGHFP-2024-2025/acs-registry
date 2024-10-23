from pymongo import MongoClient

def get_database():
    CONNECTION_STRING = "mongodb://root:root@localhost:27017"
    client = MongoClient(CONNECTION_STRING)
    return client["station_db"]

def get_collection():
    collection = get_database()["stations"]
    collection.create_index([("expireAt", 1)], expireAfterSeconds=0)
    collection.create_index([("location", "2dsphere")])
    return collection