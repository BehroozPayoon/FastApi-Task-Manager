from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm.session import Session
from app import crud

from app.models.user import User
from app.api.deps import get_current_user
from app.schemas.task import TaskCreate, TaskUpdate
from app.api import deps
from app.core.response import send_success_response


router = APIRouter()


@router.post("/")
def create_task(*, task_in: TaskCreate, db: Session = Depends(deps.get_db), user: User = Depends(get_current_user)):
    db_obj = crud.task.create(db=db, obj_in=task_in)
    return send_success_response(db_obj)

@router.put("/{id}")
def update_task(*, task_id: int, obj_in: TaskUpdate, db: Session = Depends(deps.get_db), user: User = Depends(get_current_user)):
    db_obj = crud.task.get(task_id)
    if db_obj is None:
        raise HTTPException(404)
    db_obj = crud.task.update(db=db, db_obj=db_obj, obj_in=obj_in)
    return send_success_response(db_obj)


@router.delete("/{id}")
def delete_task(*, task_id: int, db: Session = Depends(deps.get_db), user: User = Depends(get_current_user)):
    db_obj = crud.task.remove(db=db, id=task_id)
    return send_success_response(db_obj)