from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm.session import Session
from app import crud
from app.core.response import send_success_response

from app.models.user import User
from app.schemas.project import ProjectCreate
from app.api import deps
from app.core.authorization import authorize_to_create_project

router = APIRouter()

@router.post('/')
@authorize_to_create_project
def create_project(*, project_in: ProjectCreate, db: Session = Depends(deps.get_db),
     user: User = Depends(deps.get_current_user)):
    project = crud.project.create(db=db, obj_in=project_in, user_id=user.id)
    return send_success_response(project)


@router.get('/{id}/tasks')
async def project_tasks(project_id: int, db: Session = Depends(deps.get_db)):
    return send_success_response(crud.project.get_tasks(db=db, project_id=project_id))
