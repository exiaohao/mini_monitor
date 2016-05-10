import pymongo
from config import App

def monogo_db():
    conn = pymongo.MongoClient(App.mongo_server, App.mongo_port)
    db = getattr(conn, App.mongo_collection)
    return db
