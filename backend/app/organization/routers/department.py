from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.organization.schemas.department import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse
)

from app.organization.services.department import (
    create_department,
    get_departments,
    get_department,
    update_department,
    delete_department
)


router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)


@router.post(
    "",
    response_model=DepartmentResponse
)
def add_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db)
):

    return create_department(
        db,
        department
    )



@router.get(
    "",
    response_model=list[DepartmentResponse]
)
def list_departments(
    db: Session = Depends(get_db)
):

    return get_departments(db)



@router.get(
    "/{department_id}",
    response_model=DepartmentResponse
)
def get_single_department(
    department_id: UUID,
    db: Session = Depends(get_db)
):

    department = get_department(
        db,
        department_id
    )


    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )


    return department



@router.put(
    "/{department_id}",
    response_model=DepartmentResponse
)
def edit_department(
    department_id: UUID,
    department: DepartmentUpdate,
    db: Session = Depends(get_db)
):

    updated_department = update_department(
        db,
        department_id,
        department
    )


    if not updated_department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )


    return updated_department



@router.delete(
    "/{department_id}"
)
def remove_department(
    department_id: UUID,
    db: Session = Depends(get_db)
):

    deleted_department = delete_department(
        db,
        department_id
    )


    if not deleted_department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )


    return {
        "message": "Department deleted successfully"
    }