from sqlalchemy import String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
import uuid

from app.db.base import Base


class JobApplication(Base):
    __tablename__ = "job_applications"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    user_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("users.id"),
        nullable=False
    )

    company_name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    position: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    location: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    salary: Mapped[float | None] = mapped_column(
        Numeric,
        nullable=True
    )

    job_link: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    notes: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String,
        default="applied",
        nullable=False
    )

    date_applied: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    user = relationship("User")