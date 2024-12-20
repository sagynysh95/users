from pydantic import BaseModel, Field, field_validator, EmailStr, model_validator
from typing import Optional
from mongo_file import mongo_get_username
from utils.validate_password import validate_password
from utils.generate_password import generate_password
from utils.cyrillic_latin import cyrillic_to_latin
import re
import hashlib


class User(BaseModel):
    name: Optional[str] = Field(
        default=None,
        description="Имя пользователя на кириллице"
    )
    surname: Optional[str] = Field(
        default=None,
        description="Фамилия пользователя на кириллице"
    )
    father_name: Optional[str] = Field(
        default=None,
        description="Отчество пользователя на кириллице"
    )
    email: Optional[EmailStr] = Field(
        description="Валидный емайл"
    )
    iin: Optional[str] = Field(
        default=None,
        description="ИИН должен содержать 12 цифр",
        pattern=r"^\d{12}$"
    )
    role: Optional[str] = Field(
        default=None,
        examples=["employee", "guest"],
        description="Сотрудник или посетитель"
    )
    phone_number: Optional[str] = Field(
        default=None,
        pattern=r"^(?:\+7|8)\d{10}$"
    )
    rank: Optional[str] = Field(
        default=None,
        examples=["майор", "капитан", "полковник"],
        description="Военное звание пользователя если есть"
    )
    military_unit: Optional[str] = Field(
        default=None, 
        description="Наименование части где работает пользователь если есть"
    )
    

class UserCreate(User):
    user_id: Optional[str] = Field(
        default=None,
        description="Генерирует автоматический"
    )
    img_path: Optional[str] = Field(
        description="Вставляется автоматический, это ссылка на фото пользователя"
    )
    username: Optional[str] = Field(
        description="Генерируется автоматический"
    )
    password: Optional[str] = Field(
        default="@BIi#n3ArKXf",
        # default_factory=generate_password,
        description="Генерируется автоматический первый раз"
    )
    
    @model_validator(mode="before")
    def generate_username(cls, values):
        name = values.get("name").lower()
        surname = values.get("surname").lower()
        username = cyrillic_to_latin(f"{name[:1]}.{surname}")
        if mongo_get_username(username):
            values["username"] = username
        else:
            values["username"] = cyrillic_to_latin(f"{name}.{surname}")
        return values

    @model_validator(mode="before")
    def validate_password(cls, values):
        password = values.get("password", generate_password())
        # print(password)
        if not isinstance(password, str):
            raise ValueError("Пароль должен быть строкой.")
        # pattern = (
        #     r"^(?=.*[a-z])"        # хотя бы одна строчная буква
        #     r"(?=.*[A-Z])"         # хотя бы одна заглавная буква
        #     r"(?=.*\d)"            # хотя бы одна цифра
        #     r"(?=.*[!@#$%^&*])"    # хотя бы один специальный символ
        #     r".{8,20}$"            # длина от 8 до 20 символов
        # )
        # if not re.match(pattern, password):
        #     raise ValueError(
        #         "Пароль должен содержать от 8 до 20 символов, включая строчные и заглавные буквы, цифры и специальные символы."
        #     )
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        values["password"] = str(hashed_password)
        return values
    

class UserRead(User):
    user_id: Optional[str] = Field(
        description="Генерирует автоматический"
    )
    img_path: Optional[str] = Field(
        description="Вставляется автоматический, это ссылка на фото пользователя"
    )
    username: Optional[str] = Field(
        description="Генерируется автоматический"
    )
    password: Optional[str] = Field(
        description="Генерируется автоматический первый раз"
    )
    
    
