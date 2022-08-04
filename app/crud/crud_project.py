from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    def create(self, db: Session, *, obj_in: ProjectCreate, user_id: int):
        created_data = obj_in.dict()
        created_data['user_id'] = user_id
        db_obj = Project(**created_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


    def get_tasks(self, db: Session, *, project_id: int):
        project = self.get(db=db, id=project_id)
        if project is None:
            raise HTTPException(404)
        return list(map(lambda item: item, project.tasks)) 


project = CRUDProject(Project)