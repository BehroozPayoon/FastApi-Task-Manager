from pydantic import BaseModel


class TaskUserBase(BaseModel):
    task_id: int
    user_id: int


class TaskUserCreate(TaskUserBase):
    pass


class TaskUserUpdate(TaskUserBase):
    pass
