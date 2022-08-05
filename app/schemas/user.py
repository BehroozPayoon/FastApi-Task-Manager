from typing import Optional
from enum import Enum
from pydantic import BaseModel, validator

import re


class UserRoleEnum(str, Enum):
    PROJECT_MANAGER = 'manager'
    DEVELOPER = 'developer'


class UserBase(BaseModel):
    full_name: str
    username: str = None
    role: UserRoleEnum = None


class UserCreate(UserBase):
    password: str

    @validator('username')
    def username_min_length(cls, v):
        if len(v) < 5:
            raise ValueError('Username must have at least 5 characters')
        return v

    @validator('password')
    def password_is_strong(cls, v):
        if re.match(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{6,12}$", v):
            return v
        else:
            raise ValueError("Password must have have one lower character, one upper character,one special character and one number and at least 6 characters long")

class UserUpdate(UserBase):
    pass


class UserLogin(BaseModel):
    username: str
    password: str

    @validator('username')
    def username_min_length(cls, v):
        if len(v) < 5:
            raise ValueError('Username must have at least 5 characters')
        return v

    @validator('password')
    def password_is_strong(cls, v):
        if re.match(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{6,12}$", v):
            return v
        else:
            raise ValueError("Password must have have one lower character, one upper character,one special character and one number and at least 6 characters long")


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class UserInDB(UserInDBBase):
    password: str


class User(UserInDBBase):
    pass