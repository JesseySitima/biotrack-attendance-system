from sqlalchemy.orm import Session
from uuid import UUID
from app.organization.models.department import Department
from app.organization.schemas.department import (
    DepartmentCreate,
    DepartmentUpdate
)



def create_department(
    db: Session,
    department_data: DepartmentCreate
):

    department = Department(
        name=department_data.name,
        code=department_data.code,
        description=department_data.description
    )

    db.add(department)
    db.commit()
    db.refresh(department)

    return department



def get_departments(
    db: Session
):

    return db.query(Department).all()



def get_department(
    db: Session,
    department_id
):

    return (
        db.query(Department)
        .filter(
            Department.id == department_id
        )
        .first()
    )


def update_department(
    db: Session,
    department_id: UUID,
    department_data: DepartmentUpdate
):

    department = get_department(
        db,
        department_id
    )

    if not department:
        return None


    if department_data.name is not None:
        department.name = department_data.name


    if department_data.code is not None:
        department.code = department_data.code


    if department_data.description is not None:
        department.description = department_data.description


    db.commit()
    db.refresh(department)

    return department



def delete_department(
    db: Session,
    department_id: UUID
):

    department = get_department(
        db,
        department_id
    )

    if not department:
        return None


    db.delete(department)
    db.commit()

    return department