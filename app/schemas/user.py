from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    full_name: Optional[str]
    email: Optional[str] = None
    role: Optional[str]


class UserCreate(UserBase):
    full_name: str
    email: EmailStr
    password: str
    role: str


class UserUpdate(UserBase):
    ...


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class UserInDB(UserInDBBase):
    password: str


class User(UserInDBBase):
    pass