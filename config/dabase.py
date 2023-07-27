from pymongo import MongoClient 


client = MongoClient()

db = client.todo_db

collection = db["todo_collection"]