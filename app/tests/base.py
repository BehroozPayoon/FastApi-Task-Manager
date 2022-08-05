import pytest

from app.db.base_class import Base
from app.db.test_session import TestingSessionLocal, engine


Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def login_manager(client):
    client.post(
        "/v1/auth/register",
        json={"full_name": "Manager", "username": "manager", "password": "1As@11", "role": 'manager'},
    )
    response = client.post(
        "/v1/auth/login",
        json={"username": "manager", "password": "1As@11"},
    )
    return response.json()['data']['access_token']


def login_developer(client):
    client.post(
        "/v1/auth/register",
        json={"full_name": "Developer", "username": "developer", "password": "1As@11", "role": 'developer'},
    )
    response = client.post(
        "/v1/auth/login",
        json={"username": "developer", "password": "1As@11"},
    )
    return response.json()['data']['access_token']