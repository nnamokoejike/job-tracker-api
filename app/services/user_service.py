from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password
from app.core.logging_config import logger

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user_data: UserCreate):
    hashed_password = hash_password(user_data.password)

    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logger.info(f"New user registered: {new_user.email}")

    return new_user