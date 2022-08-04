from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm.session import Session
from app import crud
from app.core.response import send_success_response

from app.models.user import User
from app.api.deps import get_current_user
from app.schemas.project import ProjectCreate
from app.api import deps

router = APIRouter()


@router.post('/')
async def create_project(*, project_in: ProjectCreate, db: Session = Depends(deps.get_db), user: User = Depends(get_current_user)):
    project = crud.project.create(db=db, obj_in=project_in, user_id=user.id)
    return send_success_response(project)


@router.get('/{id}/tasks')
async def project_tasks(project_id: int, db: Session = Depends(deps.get_db)):
    return send_success_response(crud.project.get_tasks(db=db, project_id=project_id))


@router.get("/{id}/userTasks")
def list_project_user_tasks(*, db: Session = Depends(deps.get_db), user: User = Depends(get_current_user)):
    pass