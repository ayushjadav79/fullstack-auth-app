from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    photo_url: Optional[str] = None
    dob: str
    gender: str
    hobbies: list[str]