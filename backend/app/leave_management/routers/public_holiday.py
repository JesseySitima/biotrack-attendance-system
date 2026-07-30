from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.auth.models.user import User

from app.utils.dependencies import get_current_user
from app.utils.permissions import is_hr_or_admin

from app.leave_management.schemas.public_holiday import (
    PublicHolidayCreate,
    PublicHolidayResponse
)

from app.leave_management.services import (
    create_public_holiday,
    get_public_holidays,
    delete_public_holiday
)


router = APIRouter(
    prefix="/public-holidays",
    tags=["Public Holidays"]
)


@router.get(
    "",
    response_model=list[PublicHolidayResponse]
)
def all_public_holidays(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return get_public_holidays(db)


@router.post(
    "",
    response_model=PublicHolidayResponse
)
def create_holiday(
    holiday: PublicHolidayCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if not is_hr_or_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only HR/Admin can manage public holidays."
        )

    try:
        return create_public_holiday(
            db,
            holiday
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete(
    "/{holiday_id}",
    response_model=PublicHolidayResponse
)
def remove_holiday(
    holiday_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if not is_hr_or_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only HR/Admin can manage public holidays."
        )

    holiday = delete_public_holiday(
        db,
        holiday_id
    )

    if holiday is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Public holiday not found."
        )

    return holiday