import uuid
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.db.base import Base
from app.db.session import engine


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def test_user_data():
    return {
        "email": f"test_user_{uuid.uuid4()}@example.com",
        "password": "password123"
    }


@pytest.fixture
def auth_token(client, test_user_data):
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

    return response.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token):
    return {
        "Authorization": f"Bearer {auth_token}"
    }


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)