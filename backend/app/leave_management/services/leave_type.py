from uuid import UUID

from sqlalchemy.orm import Session

from app.leave_management.models.leave_type import LeaveType

from app.leave_management.schemas.leave_type import (
    LeaveTypeCreate,
    LeaveTypeUpdate
)


def create_leave_type(
    db: Session,
    leave_type_data: LeaveTypeCreate
):

    leave_type = LeaveType(
        name=leave_type_data.name,
        description=leave_type_data.description,
        default_days=leave_type_data.default_days,
        is_paid=leave_type_data.is_paid
    )


    db.add(leave_type)
    db.commit()
    db.refresh(leave_type)

    return leave_type

def get_leave_types(
    db: Session
):

    return (
        db.query(LeaveType)
        .all()
    )



def get_leave_type(
    db: Session,
    leave_type_id: UUID
):

    return (
        db.query(LeaveType)
        .filter(
            LeaveType.id == leave_type_id
        )
        .first()
    )
    
def update_leave_type(
    db: Session,
    leave_type_id: UUID,
    leave_type_data: LeaveTypeUpdate
):

    leave_type = (
        db.query(LeaveType)
        .filter(
            LeaveType.id == leave_type_id
        )
        .first()
    )


    if not leave_type:
        return None


    update_data = leave_type_data.model_dump(
        exclude_unset=True
    )


    for field, value in update_data.items():

        setattr(
            leave_type,
            field,
            value
        )


    db.commit()
    db.refresh(leave_type)

    return leave_type

def delete_leave_type(
    db: Session,
    leave_type_id: UUID
):

    leave_type = (
        db.query(LeaveType)
        .filter(
            LeaveType.id == leave_type_id
        )
        .first()
    )


    if not leave_type:
        return None


    db.delete(leave_type)
    db.commit()

    return leave_type