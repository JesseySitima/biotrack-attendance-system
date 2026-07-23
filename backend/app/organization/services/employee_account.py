from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.organization.models.employee import Employee
from app.auth.models.user import User

from app.organization.schemas.employee_account import (
    EmployeeAccountCreate
)

from app.utils.security import hash_password



def assign_employee_account(
    db: Session,
    employee_id,
    account_data: EmployeeAccountCreate
):

    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )


    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found."
        )


    if employee.user_id:
        raise HTTPException(
            status_code=400,
            detail="Employee already has an account."
        )


    user = User(
        username=account_data.username,
        email=account_data.email,
        password_hash=hash_password(
            account_data.password
        ),
        role_id=account_data.role_id
    )


    db.add(user)

    db.flush()


    employee.user_id = user.id


    db.commit()

    db.refresh(employee)


    return employee