from app.database import SessionLocal

from app.organization.services.work_schedule_seed import (
    seed_default_work_schedule
)


db = SessionLocal()

try:
    seed_default_work_schedule(db)
    print("Work schedule seeded successfully.")
finally:
    db.close()