from sqlalchemy.orm import Session

from app.organization.models.work_schedule import WorkSchedule


def seed_default_work_schedule(
    db: Session
):

    if db.query(WorkSchedule).count() > 0:
        return

    db.add_all([
        WorkSchedule(weekday=0, is_working_day=True),
        WorkSchedule(weekday=1, is_working_day=True),
        WorkSchedule(weekday=2, is_working_day=True),
        WorkSchedule(weekday=3, is_working_day=True),
        WorkSchedule(weekday=4, is_working_day=True),
        WorkSchedule(weekday=5, is_working_day=False),
        WorkSchedule(weekday=6, is_working_day=False),
    ])

    db.commit()