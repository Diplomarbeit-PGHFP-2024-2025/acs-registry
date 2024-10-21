from pymongo import MongoClient


def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://python:python@democluster.w6aj9.mongodb.net/?retryWrites=true&w=majority&appName=DemoCluster"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client["station_db"]

def get_collection():
    return get_database()["stations"]