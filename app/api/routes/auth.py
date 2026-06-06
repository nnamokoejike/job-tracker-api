from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import get_current_user
from app.models.user import User

from app.schemas.login import LoginRequest
from app.schemas.token import Token
from app.core.security import verify_password, create_access_token
from app.core.logging_config import logger

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import get_user_by_email, create_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = get_user_by_email(db, user_data.email)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    new_user = create_user(db, user_data)

    return new_user

@router.post(
    "/login",
    response_model=Token
)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = get_user_by_email(db, form_data.username)

    if not user:
        logger.warning(
            f"Failed login attempt: {form_data.username}"
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    password_valid = verify_password(
        form_data.password,
        user.hashed_password
    )

    if not password_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = create_access_token(
        data={"sub": user.email}
    )
    logger.info(f"User logged in: {user.email}")

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user