from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    iin: Optional[int] = None
    role: Optional[str] = None
    # photo_path: Optional[str]
