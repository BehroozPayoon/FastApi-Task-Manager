

from typing import Optional

from sqlalchemy.orm.session import Session

from app.models.user import User
from app.core.security import verify_password
from app import crud


def authenticate(
    *,
    email: str,
    password: str,
    db: Session,
) -> Optional[User]:
    user = crud.user.find_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user