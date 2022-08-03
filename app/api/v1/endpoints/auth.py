from re import L
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.session import Session

from app.schemas.user import UserCreate, UserLogin
from app.api import deps
from app import crud
from app.core.auth import authenticate
from app.core.response import send_success_response


router = APIRouter()


@router.post("/register")
def register(*, db: Session = Depends(deps.get_db), register: UserCreate):
    return send_success_response(crud.user.create(db, obj_in=register))


@router.post("/login")
def login(*, db: Session = Depends(deps.get_db), login: UserLogin):
    user = authenticate(email=login.email, password=login.password, db=db)
    if user is None:
        raise HTTPException(404)
    return crud.user.get_by_email(db=db, email=login.email)



