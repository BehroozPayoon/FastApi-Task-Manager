from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.schemas.user import UserRoleEnum

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(256), nullable=True)
    username = Column(String, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

    projects = relationship("Project", back_populates="user")
    createdTasks = relationship("Task", back_populates="user")
    tasks = relationship("TaskUser", back_populates="user")

    def is_manager(self):
        return self.role == UserRoleEnum.PROJECT_MANAGER
