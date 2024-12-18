from fastapi import APIRouter
from models import User
from minio_file import upload_photo_minio
from mongo_file import mongo_insert_one, mongo_update_one, mongo_delete_one, mongo_get

router = APIRouter()


@router.post("/")
def create_user(employee: User):
    file_path = upload_photo_minio(employee.name, employee.surname, employee.iin)
    print(file_path)
    mongo_insert_one(employee, file_path)
    return "Данные загружены"


# @router.get("/")
# def get_users():
#     result = mongo_get()
#     return [{"data": data} for data in result]


@router.put("/{id}")
def update_user(id: str, employee: User):
    update_data = {}
    if employee.name:
        update_data["name"] = employee.name
    if employee.surname:
        update_data["surname"] = employee.surname
    if employee.iin:
        update_data["iin"] = employee.iin
    if employee.role:
        update_data["role"] = employee.role
    

    mongo_update_one(id, update_data)
    return "Данные успешно обновлены"


@router.delete("/{id}")
def delete_user(id: str):
    mongo_delete_one(id)
    return "Пользователь удален"
