import pymongo


class Model:
    mongoClient = pymongo.MongoClient("mongodb+srv://dbUser:123@cluster0.mvg33.mongodb.net/myFirstDatabase"
                                      "?retryWrites=true&w=majority")
    db = mongoClient["school"]

    def __init__(self, col):
        self.client = self.db[col]

    def find_all(self, query: object):
        return self.client.find(query)

    def insert_one(self, obj):
        return self.client.insert_one(obj)

    def update(self, query, setter):
        self.client.update(query, setter)
