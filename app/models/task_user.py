from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class TaskUser(Base):
    __tablename__ = "tasks_users"

    task_id = Column(Integer, ForeignKey('tasks.id'), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True, nullable=False)

    task = relationship('Task', back_populates="users")
    user = relationship('User', back_populates="tasks")
