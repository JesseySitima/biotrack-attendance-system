from uuid import UUID

from sqlalchemy.orm import Session

from app.leave_management.models.public_holiday import PublicHoliday
from app.leave_management.schemas.public_holiday import (
    PublicHolidayCreate
)


def create_public_holiday(
    db: Session,
    holiday_data: PublicHolidayCreate
):

    existing = (
        db.query(PublicHoliday)
        .filter(
            PublicHoliday.holiday_date == holiday_data.holiday_date
        )
        .first()
    )

    if existing:
        raise ValueError(
            "A public holiday already exists for this date."
        )

    holiday = PublicHoliday(
        name=holiday_data.name,
        holiday_date=holiday_data.holiday_date
    )

    db.add(holiday)

    db.commit()

    db.refresh(holiday)

    return holiday


def get_public_holidays(
    db: Session
):

    return (
        db.query(PublicHoliday)
        .order_by(PublicHoliday.holiday_date)
        .all()
    )


def get_public_holiday(
    db: Session,
    holiday_id: UUID
):

    return (
        db.query(PublicHoliday)
        .filter(
            PublicHoliday.id == holiday_id
        )
        .first()
    )


def delete_public_holiday(
    db: Session,
    holiday_id: UUID
):

    holiday = get_public_holiday(
        db,
        holiday_id
    )

    if holiday is None:
        return None

    db.delete(holiday)

    db.commit()

    return holiday