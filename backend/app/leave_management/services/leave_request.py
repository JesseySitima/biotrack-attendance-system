from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.leave_management.models.leave_request import LeaveRequest

from app.leave_management.schemas.leave_request import (
    LeaveRequestCreate
)

from app.leave_management.constants import (
    LEAVE_PENDING,
    LEAVE_APPROVED,
    LEAVE_REJECTED
)

from app.utils.permissions import (
    is_hr_or_admin,
    is_manager_of_employee
)

from app.auth.models.user import User


def create_leave_request(
    db: Session,
    employee_id: UUID,
    leave_request_data: LeaveRequestCreate
):
    if leave_request_data.end_date < leave_request_data.start_date:
        raise ValueError(
            "End date cannot be before start date"
        )

    leave_request = LeaveRequest(
        employee_id=employee_id,
        leave_type_id=leave_request_data.leave_type_id,
        start_date=leave_request_data.start_date,
        end_date=leave_request_data.end_date,
        reason=leave_request_data.reason,
        status=LEAVE_PENDING
    )


    db.add(leave_request)

    db.commit()

    db.refresh(leave_request)


    return leave_request

def get_leave_requests(
    db: Session
):

    return (
        db.query(LeaveRequest)
        .all()
    )



def get_leave_request(
    db: Session,
    leave_request_id: UUID
):

    return (
        db.query(LeaveRequest)
        .filter(
            LeaveRequest.id == leave_request_id
        )
        .first()
    )



def get_employee_leave_requests(
    db: Session,
    employee_id: UUID
):

    return (
        db.query(LeaveRequest)
        .filter(
            LeaveRequest.employee_id == employee_id
        )
        .all()
    )
    
def approve_leave_request(
    db: Session,
    leave_request_id: UUID,
    approved_by: UUID
):

    leave_request = (
        db.query(LeaveRequest)
        .filter(
            LeaveRequest.id == leave_request_id
        )
        .first()
    )


    if not leave_request:
        return None


    leave_request.status = LEAVE_APPROVED
    leave_request.approved_by = approved_by
    leave_request.approved_at = datetime.utcnow()


    db.commit()

    db.refresh(leave_request)


    return leave_request

def reject_leave_request(
    db: Session,
    leave_request_id: UUID
):

    leave_request = (
        db.query(LeaveRequest)
        .filter(
            LeaveRequest.id == leave_request_id
        )
        .first()
    )


    if not leave_request:
        return None


    leave_request.status = LEAVE_REJECTED


    db.commit()

    db.refresh(leave_request)


    return leave_request

def approve_leave_request(
    db: Session,
    leave_request_id: UUID,
    current_user: User,
    status: str
):

    leave_request = (
        db.query(LeaveRequest)
        .filter(
            LeaveRequest.id == leave_request_id
        )
        .first()
    )


    if not leave_request:
        return None


    can_approve = (
        is_hr_or_admin(current_user)
        or
        is_manager_of_employee(
            current_user,
            leave_request
        )
    )

    if not can_approve:
        return False


    leave_request.status = status
    leave_request.approved_by = current_user.id
    leave_request.approved_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(leave_request)

    return leave_request