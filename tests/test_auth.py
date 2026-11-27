from fastapi.testclient import TestClient

from app.models.user import User


def test_register_success(client: TestClient):
    payload = {
        "email": "newuser@example.com",
        "password": "StrongPassword123",
        "full_name": "New User",
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["data"]["email"] == payload["email"]
    assert body["data"]["full_name"] == payload["full_name"]
    assert "hashed_password" not in body["data"]


def test_register_duplicate_email(client: TestClient, customer_user: User):
    payload = {
        "email": customer_user.email,
        "password": "StrongPassword123",
        "full_name": "Duplicate User",
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code in (400, 409)


def test_login_success(client: TestClient, customer_user: User):
    payload = {
        "email": customer_user.email,
        "password": "Customer@123",
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body["data"]
    assert body["data"]["token_type"] == "bearer"


def test_login_wrong_password(client: TestClient, customer_user: User):
    payload = {
        "email": customer_user.email,
        "password": "WrongPassword123",
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 401
