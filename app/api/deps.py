from typing import Generator
from app import crud
from app.db.session import SessionLocal

from sqlalchemy.orm.session import Session
from fastapi import Depends

from app.models.user import User
from app.core.auth import bearer_scheme, decodeJWT
from app.core.exceptions import NotAuthenticatedExceptiion


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

def get_current_user(db: Session = Depends(get_db), token: str = Depends(bearer_scheme)) -> User:
    try:
        payload = decodeJWT(token=token)
        user_id = payload["user_id"]
        if user_id is None:
            raise NotAuthenticatedExceptiion()
        user = crud.user.get(db=db, id=user_id)
        if user is None:
            raise NotAuthenticatedExceptiion()
        return user
    except:
        raise NotAuthenticatedExceptiion()

    