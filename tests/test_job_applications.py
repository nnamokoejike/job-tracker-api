import uuid
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

test_email = f"job_user_{uuid.uuid4()}@example.com"
test_password = "password123"


def create_test_user():
    client.post(
        "/auth/register",
        json={
            "email": test_email,
            "password": test_password
        }
    )


def get_auth_token():
    create_test_user()

    response = client.post(
        "/auth/login",
        data={
            "username": test_email,
            "password": test_password
        }
    )

    return response.json()["access_token"]


def test_create_job_application(client, auth_headers):
    response = client.post(
        "/job-applications/",
        json={
            "company_name": "BMW",
            "position": "Backend Developer",
            "location": "Munich",
            "salary": 65000,
            "job_link": "https://bmw.com/jobs/123",
            "notes": "Applied via LinkedIn"
        },
        headers=auth_headers
    )

    assert response.status_code == 201

    response_data = response.json()

    assert response_data["company_name"] == "BMW"
    assert response_data["position"] == "Backend Developer"


def test_get_job_applications(client, auth_headers):
    response = client.get(
        "/job-applications/",
        headers=auth_headers
    )

    assert response.status_code == 200

    response_data = response.json()

    assert "items" in response_data
    assert "page" in response_data
    assert "size" in response_data
    assert "total" in response_data


def test_get_single_job_application(client, auth_headers):
    create_response = client.post(
        "/job-applications/",
        json={
            "company_name": "SAP",
            "position": "Python Developer",
            "location": "Berlin",
            "salary": 70000,
            "job_link": "https://sap.com/jobs/123",
            "notes": "Test application"
        },
        headers=auth_headers
    )

    application_id = create_response.json()["id"]

    response = client.get(
        f"/job-applications/{application_id}",
        headers=auth_headers
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["id"] == application_id
    assert response_data["company_name"] == "SAP"
    assert response_data["position"] == "Python Developer"


def test_update_job_application(client, auth_headers):
    create_response = client.post(
        "/job-applications/",
        json={
            "company_name": "Microsoft",
            "position": "Backend Engineer",
            "location": "Berlin",
            "salary": 85000,
            "job_link": "https://microsoft.com/jobs/123",
            "notes": "Original application"
        },
        headers=auth_headers
    )

    application_id = create_response.json()["id"]

    update_response = client.patch(
        f"/job-applications/{application_id}",
        json={
            "status": "interview"
        },
        headers=auth_headers
    )

    assert update_response.status_code == 200

    response_data = update_response.json()

    assert response_data["id"] == application_id
    assert response_data["status"] == "interview"

def test_delete_job_application(client, auth_headers):
    create_response = client.post(
        "/job-applications/",
        json={
            "company_name": "Amazon",
            "position": "Software Engineer",
            "location": "Munich",
            "salary": 90000,
            "job_link": "https://amazon.jobs/123",
            "notes": "Delete test"
        },
        headers=auth_headers
    )

    application_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/job-applications/{application_id}",
        headers=auth_headers
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        f"/job-applications/{application_id}",
        headers=auth_headers
    )

    assert get_response.status_code == 404


def test_filter_job_applications_by_status(client, auth_headers):
    client.post(
        "/job-applications/",
        json={
            "company_name": "BMW",
            "position": "Backend Developer",
            "location": "Munich",
            "salary": 70000,
            "job_link": "https://bmw.com/jobs/1",
            "notes": "Filter test",
            "status": "interview"
        },
        headers=auth_headers
    )

    response = client.get(
        "/job-applications/?status=interview",
        headers=auth_headers
    )

    assert response.status_code == 200

    response_data = response.json()

    assert "items" in response_data

    for application in response_data["items"]:
        assert application["status"] == "interview"


def test_search_job_applications_by_company(client, auth_headers):
    client.post(
        "/job-applications/",
        json={
            "company_name": "BMW",
            "position": "Python Developer",
            "location": "Munich",
            "salary": 75000,
            "job_link": "https://bmw.com/jobs/2",
            "notes": "Company search test"
        },
        headers=auth_headers
    )

    response = client.get(
        "/job-applications/?company=BMW",
        headers=auth_headers
    )

    assert response.status_code == 200

    response_data = response.json()

    assert "items" in response_data

    for application in response_data["items"]:
        assert "BMW" in application["company_name"]


def test_job_applications_pagination(client, auth_headers):
    response = client.get(
        "/job-applications/?page=1&size=5",
        headers=auth_headers
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["page"] == 1
    assert response_data["size"] == 5

    assert "items" in response_data
    assert "total" in response_data

    assert len(response_data["items"]) <= 5


def test_job_applications_analytics(client, auth_headers):
    response = client.get(
        "/job-applications/stats/summary",
        headers=auth_headers
    )

    assert response.status_code == 200

    response_data = response.json()

    assert "total_applications" in response_data
    assert "applied" in response_data
    assert "interview" in response_data
    assert "assessment" in response_data
    assert "offer" in response_data
    assert "rejected" in response_data
    assert "withdrawn" in response_data

    assert "interview_rate" in response_data
    assert "offer_rate" in response_data
    assert "rejection_rate" in response_data