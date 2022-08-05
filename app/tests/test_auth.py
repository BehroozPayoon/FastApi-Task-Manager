from fastapi.testclient import TestClient

from app.main import app
from .base import override_get_db, test_db
from app.api.deps import get_db


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_register_invalid_username(test_db):
    response = client.post(
        "/v1/auth/register",
        json={"full_name": "Behrooz Payoon", "username": "beh", "password": "1As@11", "role": 'manager'},
    )
    assert response.status_code == 400


def test_registe_invalid_password(test_db):
    response = client.post(
        "/v1/auth/register",
        json={"full_name": "Behrooz Payoon", "username": "behrooz", "password": "123", "role": 'manager'},
    )
    assert response.status_code == 400


def test_register_invalid_role(test_db):
    response = client.post(
        "/v1/auth/register",
        json={"full_name": "Behrooz Payoon", "username": "behrooz", "password": "1As@11", "role": 'managers'},
    )
    assert response.status_code == 400


def test_register_successful(test_db):
    response = client.post(
        "/v1/auth/register",
        json={"full_name": "Behrooz Payoon", "username": "behrooz", "password": "1As@11", "role": 'manager'},
    )
    assert response.status_code == 200


def test_register_taken_username(test_db):
    response = client.post(
        "/v1/auth/register",
        json={"full_name": "Behrooz Payoon", "username": "behrooz", "password": "1As@11", "role": 'manager'},
    )
    assert response.status_code == 200

    response = client.post(
        "/v1/auth/register",
        json={"full_name": "Behrooz Payoon", "username": "behrooz", "password": "1As@11", "role": 'manager'},
    )
    assert response.status_code == 400


def test_login_invalid_username(test_db):
    response = client.post(
        "/v1/auth/login",
        json={"username": "beh", "password": "1As@11"},
    )
    assert response.status_code == 400


def test_login_invalid_password(test_db):
    response = client.post(
        "/v1/auth/login",
        json={"username": "behrooz", "password": "123"},
    )
    assert response.status_code == 400


def test_login_user_not_found(test_db):
    response = client.post(
        "/v1/auth/login",
        json={"username": "behrooz", "password": "1As@11"},
    )
    assert response.status_code == 404


def test_login_successful(test_db):
    response = _register()
    assert response.status_code == 200

    response = client.post(
        "/v1/auth/login",
        json={"username": "behrooz", "password": "1As@11"},
    )
    assert response.status_code == 200


def _register():
    response = client.post(
        "/v1/auth/register",
        json={"full_name": "Behrooz Payoon", "username": "behrooz", "password": "1As@11", "role": 'manager'},
    )
    return response