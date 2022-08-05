from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from app.schemas.user import UserCreate, UserLogin
from app.api import deps
from app import crud
from app.core.auth import authenticate, create_access_token, format_user_to_show
from app.core.response import send_success_response
from app.core.exceptions import UsernameTakenException, NotFoundException

router = APIRouter()


@router.post("/register")
def register(*, db: Session = Depends(deps.get_db), register: UserCreate):
    user = crud.user.find_by_username(db=db, username=register.username)
    if user:
        raise UsernameTakenException()
    db_obj = crud.user.create(db, obj_in=register)
    return send_success_response(format_user_to_show(db_obj))


@router.post("/login")
def login(login: UserLogin, db: Session = Depends(deps.get_db)):
    user = authenticate(username=login.username, password=login.password, db=db)
    if user is None:
        raise NotFoundException()
    access_token = create_access_token(user_id=user.id)
    return send_success_response({'user': format_user_to_show(user), 'access_token': access_token})

