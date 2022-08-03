from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "Task Manager"
    db_user: str
    db_password: str
    db_name: str


@lru_cache()
def get_settings():
    return Settings()