from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database import get_db

from app.organization.services.employee_account import (
    assign_employee_account
)

from app.organization.schemas.employee_account import (
    EmployeeAccountCreate
)


router = APIRouter(
    prefix="/employees",
    tags=["Employee Accounts"]
)


@router.post("/{employee_id}/account")
def create_employee_account(
    employee_id,
    account: EmployeeAccountCreate,
    db: Session = Depends(get_db)
):

    return assign_employee_account(
        db,
        employee_id,
        account
    )