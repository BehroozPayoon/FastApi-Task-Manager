from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    full_name: Optional[str]
    username: Optional[str] = None
    role: Optional[str]


class UserCreate(UserBase):
    full_name: str
    username: str
    password: str
    role: str


class UserUpdate(UserBase):
    pass


class UserLogin(BaseModel):
    username: str
    password: str


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class UserInDB(UserInDBBase):
    password: str


class User(UserInDBBase):
    pass