from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.api.dependencies import get_current_user
from app.schemas.job_application import (
    JobApplicationCreate,
    JobApplicationUpdate,
    JobApplicationResponse,
    PaginatedJobApplicationResponse
)
from app.services.job_application_service import (
    create_job_application,
    get_job_applications,
    get_job_application_by_id,
    update_job_application,
    delete_job_application,
    get_application_stats
)

router = APIRouter(
    prefix="/job-applications",
    tags=["Job Applications"]
)


@router.post(
    "/",
    response_model=JobApplicationResponse,
    status_code=status.HTTP_201_CREATED
)
def create_application(
    job_data: JobApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_job_application(
        db=db,
        job_data=job_data,
        current_user=current_user
    )


@router.get(
    "/",
    response_model=PaginatedJobApplicationResponse
)
def list_applications(
    status: str | None = None,
    company: str | None = None,
    page: int = 1,
    size: int = 10,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_job_applications(
        db=db,
        current_user=current_user,
        status=status,
        company=company,
        page=page,
        size=size,
        sort_by=sort_by,
        sort_order=sort_order
    )


@router.get("/stats/summary")
def application_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_application_stats(
        db=db,
        current_user=current_user
    )


@router.get(
    "/{application_id}",
    response_model=JobApplicationResponse
)
def get_application(
    application_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    application = get_job_application_by_id(
        db=db,
        application_id=application_id,
        current_user=current_user
    )

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )

    return application


@router.patch(
    "/{application_id}",
    response_model=JobApplicationResponse
)
def update_application(
    application_id: str,
    update_data: JobApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    application = update_job_application(
        db=db,
        application_id=application_id,
        update_data=update_data,
        current_user=current_user
    )

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )

    return application


@router.delete(
    "/{application_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_application(
    application_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    application = delete_job_application(
        db=db,
        application_id=application_id,
        current_user=current_user
    )

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )

    return None