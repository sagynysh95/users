from pymongo import MongoClient
from bson import ObjectId
from core.config import settings


mongo_client = MongoClient(
    host=settings.DATABASE_HOST,
    port=settings.DATABASE_PORT,
    username=settings.DATABASE_USERNAME,
    password=settings.DATABASE_PASSWORD
)
db = mongo_client[settings.DATABASE_NAME]
collection = db[settings.COLLECTION_NAME]


def mongo_insert_and_return(employee, file_path):   
    result = collection.insert_one({
                    "name": employee.name,
                    "surname": employee.surname,
                    "iin": employee.iin,
                    "role": employee.role,
                    "photo_link": file_path
                })
    inserted_id = result.inserted_id
    str_id = str(inserted_id)
    updated_result = collection.update_one(
        {"_id": inserted_id},
        {"$set": {"id": str_id}}
    )
    result_return = collection.find_one({"id": str_id}, {"_id": 0})
    return result_return


def mongo_get():
    return collection.find({}, {"_id": 0})


def mongo_get_by_id(id):
    return collection.find_one({"id": id}, {"_id": 0})


def mongo_update_one(id: str, employee: dict):
    filter = {"_id": ObjectId(id)}
    new_values = {"$set": employee}
    collection.update_one(filter, new_values)


def mongo_delete_one(id: str):
    collection.delete_one({"_id": ObjectId(id)})


def mongo_get_username(username):
    if collection.find_one({"username": username}):
        return True
    return False
    