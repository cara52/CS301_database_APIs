from pymongo import MongoClient

client = MongoClient() #connects to the local host, default port mongo server (which is what we have!)
db = client.db
collection = db['CS301']
print(collection.count_documents({}))

for doc in collection.find({"number_of_employees": {"$gte": 5000}, "founded_year": {"$gt": 2000}}, {"name": 1, "founded_year": 1, "number_of_employees": 1, "total_money_raised": 1, "_id": 0}):
    print(doc)