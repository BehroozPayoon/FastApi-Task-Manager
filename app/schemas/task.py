from typing import List
from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: str


class TaskCreate(TaskBase):
    project_id: int
    user_ids: List[int]


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

