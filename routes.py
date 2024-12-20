from fastapi import APIRouter
from models import User, UserRead
from minio_file import upload_photo_minio
from mongo_file import mongo_insert_and_return, mongo_update_one, mongo_delete_one, mongo_get, mongo_get_by_id
from typing import List

router = APIRouter(tags=["users"])


@router.post("/", status_code=201, response_model=UserRead)
def create_user(employee: User):
    file_path = upload_photo_minio(employee.name, employee.surname, employee.iin)
    result = UserRead(**employee.dict(), img_path=file_path)
    print(result)
    mongo_insert_and_return(result)

    return result


# @router.get("/", status_code=200, response_model=List[UserRead])
# def get_users():
#     result = mongo_get()
#     return [UserRead(**data) for data in result]


@router.patch("/{id}", status_code=200, response_model=dict)
def update_user(id: str, employee: dict):
    update_data = {k: v for k, v in employee.items() if v is not None}
    mongo_update_one(id, update_data)
    return {"updated": "Данные успешно обновлены"}


@router.delete("/{id}", status_code=200, response_model=dict)
def delete_user(id: str):
    mongo_delete_one(id)
    return {"deleted": "Пользователь удален"}
