from pymongo import MongoClient
from models import User
from bson import ObjectId


mongo_client = MongoClient(
    host="mongo",
    port=27017,
    username="root",
    password="root123"
)
db = mongo_client["employees_db"]
collection = db["employees_collection"]


def mongo_insert_one(employee: User, file_path: str):   
    collection.insert_one({
        "name": employee.name,
        "surname": employee.surname,
        "iin": employee.iin,
        "role": employee.role,
        "photo_link": file_path
    })


def mongo_get():
    return collection.find()


def mongo_update_one(id: str, employee: dict):
    filter = {"_id": ObjectId(id)}
    new_values = {"$set": employee}
    collection.update_one(filter, new_values)


def mongo_delete_one(id: str):
    collection.delete_one({"_id": ObjectId(id)})
    