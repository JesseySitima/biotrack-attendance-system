from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session


from app.database import get_db


from app.organization.schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse
)

from app.organization.schemas.employee_account import (
    EmployeeAccountCreate
)

from app.organization.services import (
    create_employee,
    get_employees,
    get_employee,
    update_employee,
    delete_employee
)

from app.organization.services.employee_account import (
    assign_employee_account
)





router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)



@router.post(
    "",
    response_model=EmployeeResponse
)
def add_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):

    return create_employee(
        db,
        employee
    )



@router.get(
    "",
    response_model=list[EmployeeResponse]
)
def list_employees(
    db: Session = Depends(get_db)
):

    return get_employees(db)



@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse
)
def retrieve_employee(
    employee_id: UUID,
    db: Session = Depends(get_db)
):

    employee = get_employee(
        db,
        employee_id
    )


    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )


    return employee



@router.put(
    "/{employee_id}",
    response_model=EmployeeResponse
)
def edit_employee(
    employee_id: UUID,
    employee: EmployeeUpdate,
    db: Session = Depends(get_db)
):

    updated_employee = update_employee(
        db,
        employee_id,
        employee
    )


    if not updated_employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )


    return updated_employee



@router.delete(
    "/{employee_id}"
)
def remove_employee(
    employee_id: UUID,
    db: Session = Depends(get_db)
):

    employee = delete_employee(
        db,
        employee_id
    )


    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )


    return {
        "message": "Employee deleted successfully"
    }
    
@router.post(
    "/{employee_id}/assign-account"
)
def create_employee_account(
    employee_id: UUID,
    account_data: EmployeeAccountCreate,
    db: Session = Depends(get_db)
):

    return assign_employee_account(
        db,
        employee_id,
        account_data
    )