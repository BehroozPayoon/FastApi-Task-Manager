from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import get_settings

DATABASE_URI = f"postgresql://{get_settings().db_user}:{get_settings().db_password}@postgres/{get_settings().db_name}"


engine = create_engine(
    DATABASE_URI,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)