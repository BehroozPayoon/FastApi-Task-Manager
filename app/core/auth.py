

from typing import Optional
import time

from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm.session import Session
import jwt

from app.models.user import User
from app.core.security import verify_password
from app import crud
from app.core.config import get_settings
from app.core.exceptions import NotAuthenticatedExceptiion
from app.schemas.user import User

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise NotAuthenticatedExceptiion()
            if not self.verify_jwt(credentials.credentials):
                raise NotAuthenticatedExceptiion()
            return credentials.credentials
        else:
            raise NotAuthenticatedExceptiion()

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid


bearer_scheme = JWTBearer()


def authenticate(
    *,
    username: str,
    password: str,
    db: Session,
) -> Optional[User]:
    user = crud.user.find_by_username(db, username=username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def create_access_token(*, user_id: str) -> str:
    payload = {
        "user_id": user_id,
        "expires": time.time() + get_settings().jwt_lifetime
    }
    return jwt.encode(payload, get_settings().jwt_secret, algorithm=get_settings().jwt_algorithm)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, get_settings().jwt_secret, algorithms=[get_settings().jwt_algorithm])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}


def format_user_to_show(user):
    return User(full_name=user.full_name, username=user.username, role=user.role, id=user.id)