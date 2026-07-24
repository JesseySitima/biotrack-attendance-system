from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.auth.models.user import User


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials"
    )


    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[
                settings.ALGORITHM
            ]
        )


        user_id = payload.get(
            "user_id"
        )


        if user_id is None:
            raise credentials_exception


    except JWTError:
        raise credentials_exception


    user = (
        db.query(User)
        .filter(
            User.id == user_id
        )
        .first()
    )


    if user is None:
        raise credentials_exception


    if user.employee is None:
        raise HTTPException(
            status_code=400,
            detail="User is not linked to an employee"
        )


    return user