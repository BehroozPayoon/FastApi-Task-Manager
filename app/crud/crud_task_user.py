from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.task_user import TaskUser
from app.schemas.task_user import TaskUserCreate, TaskUserUpdate


class CRUDTaskUser(CRUDBase[TaskUser, TaskUserCreate, TaskUserUpdate]):
    def create(self, db: Session, *, obj_in: TaskUserCreate):
        created_data = obj_in.dict()
        db_obj = TaskUser(**created_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)


    def remove_by_task_id(self, db: Session, task_id: int):
        db.query(TaskUser).filter(TaskUser.task_id == task_id).delete()
        

task_user = CRUDTaskUser(TaskUser)