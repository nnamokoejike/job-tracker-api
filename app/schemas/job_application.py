from pydantic import BaseModel
from datetime import datetime
from app.enums import ApplicationStatus


class JobApplicationCreate(BaseModel):
    company_name: str
    position: str
    location: str | None = None
    salary: float | None = None
    job_link: str | None = None
    notes: str | None = None


class JobApplicationUpdate(BaseModel):
    company_name: str | None = None
    position: str | None = None
    location: str | None = None
    salary: float | None = None
    job_link: str | None = None
    notes: str | None = None
    status: ApplicationStatus | None = None


class JobApplicationResponse(BaseModel):
    id: str
    company_name: str
    position: str
    location: str | None
    salary: float | None
    job_link: str | None
    notes: str | None
    status: ApplicationStatus
    date_applied: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PaginatedJobApplicationResponse(BaseModel):
    items: list[JobApplicationResponse]
    page: int
    size: int
    total: int