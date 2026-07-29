from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.organization.models.employee import Employee

from app.organization.schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate
)

from app.leave_management.services import (
    initialize_employee_leave_balances
)

def generate_employee_number(
    db: Session
):

    last_employee = (
        db.query(Employee)
        .order_by(
            Employee.created_at.desc()
        )
        .first()
    )


    if not last_employee:
        return "EMP000001"


    last_number = int(
        last_employee.employee_number.replace(
            "EMP",
            ""
        )
    )


    next_number = last_number + 1


    return f"EMP{next_number:06d}"

def create_employee(
    db: Session,
    employee_data: EmployeeCreate
):
    
    employee_number = generate_employee_number(db)
    
    if employee_data.manager_id:

        manager = (
            db.query(Employee)
            .filter(
                Employee.id == employee_data.manager_id
            )
            .first()
        )


        if not manager:
            raise HTTPException(
                status_code=404,
                detail="Manager not found."
            )
        
    

    employee = Employee(
        employee_number=employee_number,
        first_name=employee_data.first_name,
        last_name=employee_data.last_name,
        phone=employee_data.phone,
        email=employee_data.email,
        branch_id=employee_data.branch_id,
        department_id=employee_data.department_id,
        position_id=employee_data.position_id,
        manager_id=employee_data.manager_id,
    )


    db.add(employee)

    db.flush()

    initialize_employee_leave_balances(
        db,
        employee.id
    )

    db.commit()

    db.refresh(employee)

    return employee



def get_employees(
    db: Session
):

    return (
        db.query(Employee)
        .all()
    )



def get_employee(
    db: Session,
    employee_id
):

    return (
        db.query(Employee)
        .filter(
            Employee.id == employee_id
        )
        .first()
    )



def update_employee(
    db: Session,
    employee_id,
    employee_data: EmployeeUpdate
):

    employee = get_employee(
        db,
        employee_id
    )


    if not employee:
        return None


    if employee_data.first_name is not None:
        employee.first_name = employee_data.first_name


    if employee_data.last_name is not None:
        employee.last_name = employee_data.last_name


    if employee_data.phone is not None:
        employee.phone = employee_data.phone


    if employee_data.email is not None:
        employee.email = employee_data.email


    if employee_data.branch_id is not None:
        employee.branch_id = employee_data.branch_id


    if employee_data.department_id is not None:
        employee.department_id = employee_data.department_id


    if employee_data.position_id is not None:
        employee.position_id = employee_data.position_id
        
    if employee_data.manager_id is not None:
        employee.manager_id = employee_data.manager_id


    db.commit()

    db.refresh(employee)

    return employee



def delete_employee(
    db: Session,
    employee_id
):

    employee = get_employee(
        db,
        employee_id
    )


    if not employee:
        return None


    db.delete(employee)

    db.commit()

    return employee