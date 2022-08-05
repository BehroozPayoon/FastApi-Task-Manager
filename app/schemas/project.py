from pydantic import BaseModel, validator


class ProjectBase(BaseModel):
    title: str
    description: str


class ProjectCreate(ProjectBase):
    
    @validator('title')
    def title_min_length(cls, v):
        if len(v) < 5:
            raise ValueError('Title must have at least 5 characters')
        return v


class ProjectUpdate(ProjectCreate):
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

