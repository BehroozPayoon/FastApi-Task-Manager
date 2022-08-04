from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(256), nullable=False)
    description = Column(String(1024), nullable=True)

    user = relationship("User", back_populates="projects")
    tasks = relationship(
        "Task",
        cascade="all,delete-orphan",
        back_populates="project",
        uselist=True,
    )

