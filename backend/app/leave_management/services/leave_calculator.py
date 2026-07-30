from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.leave_management.models import PublicHoliday


def calculate_leave_days(
    db: Session,
    start_date: date,
    end_date: date
) -> int:

    holidays = {
        holiday.holiday_date
        for holiday in (
            db.query(PublicHoliday)
            .filter(
                PublicHoliday.holiday_date >= start_date,
                PublicHoliday.holiday_date <= end_date
            )
            .all()
        )
    }

    days = 0
    current = start_date

    while current <= end_date:

        # Monday=0 ... Sunday=6
        if current.weekday() < 5 and current not in holidays:
            days += 1

        current += timedelta(days=1)

    return days