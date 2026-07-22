from sqlalchemy.orm import Session

from app.organization.models.employee import Employee

from app.organization.schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate
)



def create_employee(
    db: Session,
    employee_data: EmployeeCreate
):

    employee = Employee(
        employee_number=employee_data.employee_number,
        first_name=employee_data.first_name,
        last_name=employee_data.last_name,
        phone=employee_data.phone,
        email=employee_data.email,
        branch_id=employee_data.branch_id,
        department_id=employee_data.department_id,
        position_id=employee_data.position_id
    )


    db.add(employee)

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