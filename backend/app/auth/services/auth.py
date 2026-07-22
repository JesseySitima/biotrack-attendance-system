from sqlalchemy.orm import Session

from app.auth.models.user import User
from app.auth.schemas.user import UserCreate

from app.utils.security import (
    hash_password,
    verify_password
)


def create_user(
    db: Session,
    user_data: UserCreate
):

    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hash_password(
            user_data.password
        )
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(
    db: Session,
    email: str,
    password: str
):

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not user:
        return None


    if not verify_password(
        password,
        user.password_hash
    ):
        return None


    return user