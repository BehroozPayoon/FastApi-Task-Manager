from collections import UserList
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(256), nullable=False)
    description = Column(String(1024), nullable=True)

    project = relationship("Project", back_populates="tasks")
    user = relationship("User", back_populates="createdTasks")
    users = relationship("TaskUser", back_populates="task", passive_deletes=True)