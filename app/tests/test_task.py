from fastapi.testclient import TestClient

from app.main import app
from .base import login_manager, override_get_db, test_db
from app.api.deps import get_db
from .base import login_manager, login_developer

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_create_project_not_authenticated(test_db):
    response = client.post(
        "/v1/tasks/",
        json={"title": "abcde", "description": "Description 1", "project_id": 1, "user_ids": [1]},
    )
    assert response.status_code == 403


def test_create_project_invalid_title(test_db):
    access_token = login_manager(client)
    _create_project(access_token)
    response = client.post(
        "/v1/tasks/",
        json={"title": "abc", "description": "Description 1", "project_id": 1, "user_ids": [1]},
        headers={'Authorization': f"Bearer {access_token}"}
    )
    assert response.status_code == 400


def test_create_task_successful(test_db):
    access_token = login_manager(client)
    _create_project(access_token)
    response = client.post(
        "/v1/tasks/",
        json={"title": "abcde", "description": "Description 1", "project_id": 1, "user_ids": [1]},
        headers={'Authorization': f"Bearer {access_token}"}
    )
    assert response.status_code == 200


def test_tasks_of_project(test_db):
    access_token = login_manager(client)
    _create_project(access_token)
    response = client.get(
        "/v1/projects/1/tasks",
        headers={'Authorization': f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert len(response.json()['data']) == 0

    client.post(
        "/v1/tasks/",
        json={"title": "abcde", "description": "Description 1", "project_id": 1, "user_ids": [1]},
        headers={'Authorization': f"Bearer {access_token}"}
    )

    response = client.get(
        "/v1/projects/1/tasks",
        headers={'Authorization': f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert len(response.json()['data']) == 1


def test_task_update_manager(test_db):
    access_token = login_manager(client)
    _create_project(access_token)
    client.post(
        "/v1/tasks/",
        json={"title": "abcde", "description": "Description 1", "project_id": 1, "user_ids": [1]},
        headers={'Authorization': f"Bearer {access_token}"}
    )
    response = client.put(
        "/v1/tasks/1",
        json={"title": "changed by manager", "description": "Description 1", "user_ids": [1]},
        headers={'Authorization': f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert response.json()["data"]["title"] == "changed by manager"


def test_task_update_developer_not_authorized(test_db):
    access_token = login_manager(client)
    _create_project(access_token)
    client.post(
        "/v1/tasks/",
        json={"title": "abcde", "description": "Description 1", "project_id": 1, "user_ids": [1]},
        headers={'Authorization': f"Bearer {access_token}"}
    )
    developer_access_token = login_developer(client)
    response = client.put(
        "/v1/tasks/1",
        json={"title": "changed by developer", "description": "Description 1", "user_ids": [1]},
        headers={'Authorization': f"Bearer {developer_access_token}"}
    )
    assert response.status_code == 403



def test_task_update_developer_authorzied(test_db):
    access_token = login_manager(client)
    _create_project(access_token)
    access_token = login_developer(client)
    client.post(
        "/v1/tasks/",
        json={"title": "abcde", "description": "Description 1", "project_id": 1, "user_ids": [1]},
        headers={'Authorization': f"Bearer {access_token}"}
    )
    response = client.put(
        "/v1/tasks/1",
        json={"title": "changed by developer", "description": "Description 1", "user_ids": [1]},
        headers={'Authorization': f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert response.json()["data"]["title"] == "changed by developer"


def test_task_delete_manager(test_db):
    access_token = login_manager(client)
    _create_project(access_token)
    client.post(
        "/v1/tasks/",
        json={"title": "abcde", "description": "Description 1", "project_id": 1, "user_ids": [1]},
        headers={'Authorization': f"Bearer {access_token}"}
    )

    response = client.get(
        "/v1/projects/1/tasks",
        headers={'Authorization': f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert len(response.json()['data']) == 1

    response = client.delete(
        "/v1/tasks/1",
        headers={'Authorization': f"Bearer {access_token}"}
    )
    assert response.status_code == 200

    response = client.get(
        "/v1/projects/1/tasks",
        headers={'Authorization': f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert len(response.json()['data']) == 0


def test_task_delete_developer_not_authorized(test_db):
    access_token = login_manager(client)
    _create_project(access_token)
    client.post(
        "/v1/tasks/",
        json={"title": "abcde", "description": "Description 1", "project_id": 1, "user_ids": [1]},
        headers={'Authorization': f"Bearer {access_token}"}
    )

    access_token = login_developer(client)
    response = client.delete(
        "/v1/tasks/1",
        headers={'Authorization': f"Bearer {access_token}"}
    )
    assert response.status_code == 403


def test_task_delete_developer_authorzied(test_db):
    access_token = login_manager(client)
    _create_project(access_token)

    access_token = login_developer(client)
    client.post(
        "/v1/tasks/",
        json={"title": "abcde", "description": "Description 1", "project_id": 1, "user_ids": [1]},
        headers={'Authorization': f"Bearer {access_token}"}
    )

    response = client.get(
        "/v1/projects/1/tasks",
        headers={'Authorization': f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert len(response.json()['data']) == 1

    response = client.delete(
        "/v1/tasks/1",
        headers={'Authorization': f"Bearer {access_token}"}
    )
    assert response.status_code == 200

    response = client.get(
        "/v1/projects/1/tasks",
        headers={'Authorization': f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert len(response.json()['data']) == 0


def _create_project(access_token):
    client.post(
        "/v1/projects/",
        json={"title": "abcde", "description": "Description 1"},
        headers={'Authorization': f"Bearer {access_token}"}
    )
