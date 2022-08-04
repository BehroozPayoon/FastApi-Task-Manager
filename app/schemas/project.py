from pydantic import BaseModel


class ProjectBase(BaseModel):
    title: str
    description: str


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    pass


class ProjectInDBBase(ProjectBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
    

class Project(ProjectInDBBase):
    pass


class ProjectInDB(ProjectInDBBase):
    pass
