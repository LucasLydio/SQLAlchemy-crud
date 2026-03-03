from pydantic import BaseModel, EmailStr
from typing import Optional
from app.schemas.profile import ProfileRead, ProfileCreate

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    profile: Optional[ProfileCreate]

class UserRead(UserBase):
    id: int
    profile: Optional[ProfileRead]

    class Config:
        orm_mode = True
