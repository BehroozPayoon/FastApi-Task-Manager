from sqlalchemy import Integer, String, Column
from app.db.base_class import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(256), nullable=True)
    email = Column(String, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

