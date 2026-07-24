from fastapi import FastAPI
from sqlalchemy import text

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
    leave_request
)


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)


app.include_router(auth.router)

app.include_router(
    role.router
)
app.include_router(
    branch.router
)
app.include_router(
    department.router
)
app.include_router(
    position.router
)
app.include_router(
    employee.router
)
app.include_router(
    leave_type.router
)
app.include_router(
    leave_request.router
)


@app.get("/")
def root():
    return {
        "message": "BioTrack API is running"
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


@app.get("/database-health")
def database_health():

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "database": "connected"
        }

    except Exception as error:

        return {
            "database": "failed",
            "error": str(error)
        }