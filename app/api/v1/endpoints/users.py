from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from app import crud
from app.core.response import send_success_response

from app.models.user import User
from app.api import deps


router = APIRouter()


@router.post("/projects/{id}/tasks")
def get_project_tasks(id: int, db: Session = Depends(deps.get_db), user: User = Depends(deps.get_current_user)):
    return send_success_response(crud.user.get_project_tasks(db=db, user=user, project_id=id))