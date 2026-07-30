from sqlalchemy.orm import Session

from app.organization.models.work_schedule import WorkSchedule


def get_work_schedule(
    db: Session
) -> dict[int, bool]:

    schedule = (
        db.query(WorkSchedule)
        .all()
    )

    return {
        day.weekday: day.is_working_day
        for day in schedule
    }