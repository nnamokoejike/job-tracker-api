# Job Tracker API

![Tests](https://github.com/nnamokoejike/job-tracker-api/actions/workflows/tests.yml/badge.svg)

A production-style backend application for tracking job applications built with FastAPI and PostgreSQL.

## Features

* User Registration and Authentication
* JWT-Based Authorization
* Job Application CRUD Operations
* Status Tracking
* Search by Company
* Filter by Status
* Pagination
* Sorting
* Analytics Dashboard
* Application Logging
* Automated Testing with Pytest

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and receive JWT token |
| GET | `/auth/me` | Get current authenticated user |

### Job Applications

| Method | Endpoint | Description |
|---|---|---|
| POST | `/job-applications/` | Create job application |
| GET | `/job-applications/` | Get all applications with filtering, search, pagination and sorting |
| GET | `/job-applications/{id}` | Get one application |
| PATCH | `/job-applications/{id}` | Update application |
| DELETE | `/job-applications/{id}` | Delete application |
| GET | `/job-applications/stats/summary` | Get analytics summary |

## Tech Stack

* FastAPI
* PostgreSQL
* SQLAlchemy
* Alembic
* Pydantic
* Pytest
* JWT Authentication

## Project Structure

```text
app/
├── api/
├── core/
├── db/
├── models/
├── schemas/
├── services/

tests/
├── conftest.py
├── test_auth.py
├── test_job_applications.py
```

## Running the Project

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

## Running Tests

```bash
pytest
```

Current Test Coverage:

* Authentication Tests
* Authorization Tests
* CRUD Tests
* Search Tests
* Filtering Tests
* Pagination Tests
* Analytics Tests

Total: 18 Automated Tests

## Logging

Application logs are written to:

```text
logs/app.log
```

Logged Events:

* Application Startup
* User Registration
* Successful Login
* Failed Login Attempts
* Job Application Creation
* Job Application Updates
* Job Application Deletion

```
```
