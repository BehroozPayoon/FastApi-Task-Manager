from fastapi.testclient import TestClient

from app.main import app
from .base import login_developer, login_manager, override_get_db, test_db
from app.api.deps import get_db
from .base import login_manager, login_developer

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_create_project_not_authenticated(test_db):
    response = client.post(
        "/v1/projects/",
        json={"title": "abc", "description": "Description 1"},
    )
    assert response.status_code == 403


def test_create_project_not_authorized(test_db):
    access_token = login_developer(client)
    response = client.post(
        "/v1/projects/",
        json={"title": "abcde", "description": "Description 1"},
        headers={'Authorization': f"Bearer {access_token}"}
    )
    assert response.status_code == 403


def test_create_project_invalid_title(test_db):
    access_token = login_manager(client)
    response = client.post(
        "/v1/projects/",
        json={"title": "abc", "description": "Description 1"},
        headers={'Authorization': f"Bearer {access_token}"}
    )
    assert response.status_code == 400


def test_create_task_successful(test_db):
    access_token = login_manager(client)
    response = client.post(
        "/v1/projects/",
        json={"title": "abcde", "description": "Description 1"},
        headers={'Authorization': f"Bearer {access_token}"}
    )
    assert response.status_code == 200


