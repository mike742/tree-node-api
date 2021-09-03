from pymongo import MongoClient

# client = pymongo.MongoClient(
#     "mongodb+srv://adcore:adcore@cluster0.agwmf.mongodb.net/test?retryWrites=true&w=majority")
# db = client.test
# print(db)
# print(client.list_database_names())

cluster = MongoClient(
    "mongodb+srv://adcore:adcore@cluster0.agwmf.mongodb.net/test?retryWrites=true&w=majority")
db = cluster["test"]
collection = db["test"]

# insert doculent
#post = {"_id": 0, "name": "Mark", "score": 12}
# collection.insert_one(post)

# insert collection
# post1 = {"_id": 1, "name": "Lucy", "score": 15}
# post2 = {"_id": 2, "name": "Tracy", "score": 11}
# collection.insert_many([post1, post2])

# searching
#res = collection.find({"name": "Tracy"})
# res = collection.find_one({"name": "Tracy"})
# print(res)

# for r in res:
#     print(r)


# delete
# res = collection.delete_one({"_id": 0})
# res = collection.delete_many({})


# update
res = collection.update_one({"_id": 0}, {"$set": {"name": "MIKE"}})


post_count = collection.count_documents({})
print(post_count)
