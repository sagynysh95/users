from pymongo import MongoClient, ASCENDING
from bson import ObjectId
from core.config import settings

def setup_mongo():
    mongo_client = MongoClient(
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT,
        username=settings.DATABASE_USERNAME,
        password=settings.DATABASE_PASSWORD
    )
    db = mongo_client[settings.DATABASE_NAME]
    collection = db[settings.COLLECTION_NAME]

    collection.create_index([("iin", ASCENDING)], unique=True)
    return collection


def mongo_insert_and_return(employee):   
    result = setup_mongo().insert_one({
                    "name": employee.name,
                    "surname": employee.surname,
                    "father_name": employee.father_name,
                    "iin": employee.iin,
                    "role": employee.role,
                    "img_path": employee.img_path,
                    "email": employee.email,
                    "phone_number": employee.phone_number,
                    "rank": employee.rank,
                    "military_unit": employee.military_unit,
                    "username": employee.username,
                    "password": employee.password
                })
    inserted_id = result.inserted_id
    str_id = str(inserted_id)
    updated_result = setup_mongo().update_one(
        {"_id": inserted_id},
        {"$set": {"user_id": str_id}}
    )
    result_return: dict = setup_mongo().find_one({"user_id": str_id}, {"_id": 0})
    print(result_return)
    return result_return


def mongo_get():
    return setup_mongo().find({}, {"_id": 0})


def mongo_get_by_id(id):
    return setup_mongo().find_one({"user_id": id}, {"_id": 0})


def mongo_update_one(id: str, employee: dict):
    filter = {"_id": ObjectId(id)}
    new_values = {"$set": employee}
    setup_mongo().update_one(filter, new_values)


def mongo_delete_one(id: str):
    setup_mongo().delete_one({"_id": ObjectId(id)})


def mongo_get_username(username):
    if setup_mongo().find_one({"username": username}):
        return False
    return True

def mongo_get_query(query, skip, limit):
    result = list(
        setup_mongo().find(query, {"_id": 0}).skip(skip).limit(limit)
    )
    return result

def count_documents(query):
    return setup_mongo().count_documents(query)

# setup_mongo()
# print(mongo_get_username("b.ospan"))
    