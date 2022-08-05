from typing import List
from pydantic import BaseModel, validator


class TaskBase(BaseModel):
    title: str
    description: str


class TaskCreate(TaskBase):
    project_id: int
    user_ids: List[int]

    @validator('title')
    def title_min_length(cls, v):
        if len(v) < 5:
            raise ValueError('Title must have at least 5 characters')
        return v


class TaskUpdate(TaskBase):
    user_ids: List[int]


class TaskInDBBase(TaskBase):
    id: int
    project_id: int

    class Config:
        orm_mode = True
    

class Task(TaskInDBBase):
    pass


class TaskInDB(TaskInDBBase):
    pass

