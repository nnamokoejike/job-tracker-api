from fastapi.testclient import TestClient
import uuid
from app.main import app

client = TestClient(app)

test_email = f"pytest_user_{uuid.uuid4()}@example.com"
test_password = "password123"


def test_register_user():
    response = client.post(
        "/auth/register",
        json={
            "email": test_email,
            "password": test_password
        }
    )

    assert response.status_code == 201


def test_duplicate_registration():
    response = client.post(
        "/auth/register",
        json={
            "email": test_email,
            "password": test_password
        }
    )

    assert response.status_code == 400



def test_login_success(client, test_user_data):
    client.post(
        "/auth/register",
        json=test_user_data
    )

    response = client.post(
        "/auth/login",
        data={
            "username": test_user_data["email"],
            "password": test_user_data["password"]
        }
    )

    assert response.status_code == 200

    response_data = response.json()

    assert "access_token" in response_data
    assert response_data["token_type"] == "bearer"


def test_login_invalid_password(client, test_user_data):
    client.post(
        "/auth/register",
        json=test_user_data
    )

    response = client.post(
        "/auth/login",
        data={
            "username": test_user_data["email"],
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401


def test_get_current_user(client, auth_headers):
    response = client.get(
        "/auth/me",
        headers=auth_headers
    )

    assert response.status_code == 200

    response_data = response.json()

    assert "email" in response_data
    assert "hashed_password" not in response_data


def test_get_current_user_without_token(client):
    response = client.get("/auth/me")

    assert response.status_code == 401


def test_fixture_login(client, test_user_data):
    response = client.post(
        "/auth/register",
        json=test_user_data
    )

    assert response.status_code == 201