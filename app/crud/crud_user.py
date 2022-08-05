from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def find_by_username(self, db: Session, *, username: str) -> Optional[User]:
        return db.query(User).filter(func.lower(User.username) == username.lower()).first()

    def get_multi_by_ids(self, db: Session, id_list: List[int]):
        return db.query(User).filter(User.id.in_(id_list)).all()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        created_data = obj_in.dict()
        created_data.pop("password")
        db_obj = User(**created_data)
        db_obj.password = get_password_hash(obj_in.password)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_project_tasks(self, db: Session, user: User, project_id: int):
        tasks = filter(lambda item: item.task.project_id == project_id, user.tasks)
        return list(map(lambda item: item.task, tasks))


user = CRUDUser(User)
