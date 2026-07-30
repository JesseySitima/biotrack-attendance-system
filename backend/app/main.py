from fastapi import FastAPI
from sqlalchemy import text

from app.database import SessionLocal
from contextlib import asynccontextmanager

from app.config import settings
from app.database import engine

from app.auth.routers import auth
from app.auth.routers import role
from app.organization.routers import branch
from app.organization.routers import department
from app.organization.routers import position
from app.organization.routers import employee
from app.leave_management.routers import (
    leave_type,
    leave_request,
    leave_balance,
    public_holiday,
)
from app.organization.services.work_schedule_seed import (
    seed_default_work_schedule,
)


@asynccontextmanager
async def lifespan(app: FastAPI):

    db = SessionLocal()

    try:
        seed_default_work_schedule(db)

    finally:
        db.close()

    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan
)


app.include_router(auth.router)

app.include_router(role.router)
# organization
app.include_router(branch.router)
app.include_router(department.router)
app.include_router(position.router)
app.include_router(employee.router)
# Leave Management
app.include_router(leave_type.router)
app.include_router(leave_request.router)
app.include_router(leave_balance.router)
app.include_router(public_holiday.router)


@app.get("/")
def root():
    return {"message": "BioTrack API is running"}


@app.get("/health")
def health_check():

    return {"status": "healthy"}


@app.get("/database-health")
def database_health():

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {"database": "connected"}

    except Exception as error:

        return {"database": "failed", "error": str(error)}
