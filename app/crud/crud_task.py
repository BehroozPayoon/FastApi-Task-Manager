from typing import Union, Dict, Any
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import crud

from app.crud.base import CRUDBase
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.schemas.task_user import TaskUserCreate


class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    def create(self, db: Session, obj_in: TaskCreate):
        users = crud.user.get_multi_by_ids(db=db, id_list=obj_in.user_ids)
        if len(users) != len(obj_in.user_ids):
            raise HTTPException(400)
        created_data = obj_in.dict()
        created_data.pop("user_ids")
        db_obj = Task(**created_data)
        db.add(db_obj)
        db.commit()

        for user_id in obj_in.user_ids:
            crud.task_user.create(db=db, obj_in=TaskUserCreate(task_id=db_obj.id, user_id=user_id))

        db.refresh(db_obj)
        return db_obj


    def update(self, db: Session, *, db_obj: Task, obj_in: Union[TaskUpdate, Dict[str, Any]]) -> Task:
        update_data = obj_in.dict()
        update_data.pop("user_ids")
        db_obj = super().update(db, db_obj=db_obj, obj_in=update_data)
        
        crud.task_user.remove_by_task_id(db=db, task_id=db_obj.id)
        for user_id in obj_in.user_ids:
            crud.task_user.create(db=db, obj_in=TaskUserCreate(task_id=db_obj.id, user_id=user_id))

        db.refresh(db_obj)
        return db_obj
    
    # def update(self, db: Session, id: int, obj_in: TaskUpdate):
    #     db_obj = self.get(id)
    #     if db_obj is None:
    #         raise HTTPException(404)
        
    #     update_data = obj_in.dict()
    #     update_data.pop("user_ids")
    #     db_obj = Task(**created_data)
    #     db.add(db_obj)
    #     db.commit()


task = CRUDTask(Task)