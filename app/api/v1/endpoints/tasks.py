from fastapi import APIRouter, Depends

from sqlalchemy.orm.session import Session
from app import crud

from app.models.user import User
from app.api.deps import get_current_user
from app.schemas.task import TaskCreate, TaskUpdate
from app.api import deps
from app.core.response import send_success_response
from app.core.authorization import authorize_to_update_or_delete_task
from app.core.exceptions import NotFoundException

router = APIRouter()


@router.post("/")
def create_task(*, task_in: TaskCreate, db: Session = Depends(deps.get_db), user: User = Depends(get_current_user)):
    db_obj = crud.task.create_item(db=db, obj_in=task_in, user=user)
    return send_success_response(db_obj)


@router.put("/{id}")
@authorize_to_update_or_delete_task
def update_task(*, id: int, obj_in: TaskUpdate, db: Session = Depends(deps.get_db), user: User = Depends(get_current_user)):
    db_obj = crud.task.get(db=db, id=id)
    if db_obj is None:
        raise NotFoundException()
    db_obj = crud.task.update(db=db, db_obj=db_obj, obj_in=obj_in)
    return send_success_response(db_obj)


@router.delete("/{id}")
@authorize_to_update_or_delete_task
def delete_task(*, id: int, db: Session = Depends(deps.get_db), user: User = Depends(get_current_user)):
    db_obj = crud.task.remove(db=db, id=id)
    return send_success_response(db_obj)