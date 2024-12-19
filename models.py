from pydantic import BaseModel, Field, field_validator
from typing import Optional

class User(BaseModel):
    name: Optional[str] = Field(default=None)
    surname: Optional[str] = Field(default=None)
    iin: Optional[int] = Field(default=0)
    role: Optional[str] = Field(default=None)
    phone_number: Optional[str] = Field(default=None)


    @field_validator("iin")
    def validate_iin(cls, value):
        if value == 0:
            return value
        if len(str(value)) != 12:
            raise ValueError("ИИН должен содержать 12 цифр")
        return value
    

class UserRead(User):
    id: Optional[str] = Field(default=None)
    img_path: Optional[str] = Field(default=None)
    
