from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

def test_register():
    response = client.post(
        "/v1/auth/register",
        json={"full_name": "Behrooz Payoon", "username": "behrooz", "password": "123", "role": 'manager'},
    )
    assert response.status_code == 200


def test_login():
    response = client.post(
        "/v1/auth/register",
        json={"full_name": "Behrooz Payoon", "username": "behrooz", "password": "123", "role": 'manager'},
    )
    assert response.status_code == 200

    response = client.post(
        "/v1/auth/login",
        json={"username": "behrooz", "password": "123"},
    )
    assert response.status_code == 200
