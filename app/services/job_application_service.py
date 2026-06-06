from sqlalchemy.orm import Session
from app.core.logging_config import logger
from app.models.job_application import JobApplication
from app.models.user import User
from app.schemas.job_application import (
    JobApplicationCreate,
    JobApplicationUpdate
)


def create_job_application(
    db: Session,
    job_data: JobApplicationCreate,
    current_user: User
):
    new_application = JobApplication(
        user_id=current_user.id,
        company_name=job_data.company_name,
        position=job_data.position,
        location=job_data.location,
        salary=job_data.salary,
        job_link=job_data.job_link,
        notes=job_data.notes
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    logger.info(
        f"Job application created: "
        f"{new_application.company_name} - "
        f"{new_application.position} "
        f"by user {current_user.email}"
    )

    return new_application


def get_job_applications(
    db: Session,
    current_user: User,
    status: str | None = None,
    company: str | None = None,
    page: int = 1,
    size: int = 10,
    sort_by: str = "created_at",
    sort_order: str = "desc"
):
    query = (
        db.query(JobApplication)
        .filter(
            JobApplication.user_id == current_user.id
        )
    )

    if status:
        query = query.filter(
            JobApplication.status == status
        )

    if company:
        query = query.filter(
            JobApplication.company_name.ilike(f"%{company}%")
        )

    allowed_sort_fields = {
        "company_name": JobApplication.company_name,
        "position": JobApplication.position,
        "location": JobApplication.location,
        "salary": JobApplication.salary,
        "status": JobApplication.status,
        "date_applied": JobApplication.date_applied,
        "created_at": JobApplication.created_at
    }

    sort_column = allowed_sort_fields.get(
        sort_by,
        JobApplication.created_at
    )

    if sort_order == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    total = query.count()

    applications = (
        query
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )

    return {
        "items": applications,
        "page": page,
        "size": size,
        "total": total
    }


def get_job_application_by_id(
    db: Session,
    application_id: str,
    current_user: User
):
    return (
        db.query(JobApplication)
        .filter(
            JobApplication.id == application_id,
            JobApplication.user_id == current_user.id
        )
        .first()
    )


def update_job_application(
    db: Session,
    application_id: str,
    update_data: JobApplicationUpdate,
    current_user: User
):
    application = (
        db.query(JobApplication)
        .filter(
            JobApplication.id == application_id,
            JobApplication.user_id == current_user.id
        )
        .first()
    )

    if application is None:
        return None

    update_dict = update_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_dict.items():
        setattr(application, field, value)

    db.commit()
    db.refresh(application)

    logger.info(
        f"Job application updated: "
        f"{application.company_name} - "
        f"{application.position} "
        f"by user {current_user.email}"
    )

    return application


def delete_job_application(
    db: Session,
    application_id: str,
    current_user: User
):
    application = (
        db.query(JobApplication)
        .filter(
            JobApplication.id == application_id,
            JobApplication.user_id == current_user.id
        )
        .first()
    )

    if application is None:
        return None

    logger.info(
        f"Job application deleted: "
        f"{application.company_name} - "
        f"{application.position} "
        f"by user {current_user.email}"
    )

    db.delete(application)
    db.commit()

    return application


def get_application_stats(
    db: Session,
    current_user: User
):
    applications = (
        db.query(JobApplication)
        .filter(
            JobApplication.user_id == current_user.id
        )
        .all()
    )

    total = len(applications)

    stats = {
        "total_applications": total,
        "applied": 0,
        "interview": 0,
        "assessment": 0,
        "offer": 0,
        "rejected": 0,
        "withdrawn": 0,
        "interview_rate": 0,
        "offer_rate": 0,
        "rejection_rate": 0
    }

    for application in applications:
        if application.status in stats:
            stats[application.status] += 1

    if total > 0:
        stats["interview_rate"] = round(
            (stats["interview"] / total) * 100,
            2
        )

        stats["offer_rate"] = round(
            (stats["offer"] / total) * 100,
            2
        )

        stats["rejection_rate"] = round(
            (stats["rejected"] / total) * 100,
            2
        )

    return stats