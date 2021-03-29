import pymongo
import os


class Model:
    mongoUrl = os.environ.get('MONGO_URL')
    mongoClient = pymongo.MongoClient(mongoUrl)
    db = mongoClient["school"]

    def __init__(self, col):
        self.client = self.db[col]

    def find_all(self, query: object):
        return self.client.find(query)

    def insert_one(self, obj):
        return self.client.insert_one(obj)

    def update(self, query, setter):
        self.client.update(query, setter)
