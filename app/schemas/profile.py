from pydantic import BaseModel

class ProfileCreate(BaseModel):
    profile_name: str

class ProfileRead(BaseModel):
    id: int
    profile_name: str

    class Config:
        orm_mode = True
