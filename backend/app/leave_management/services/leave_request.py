from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.leave_management.models.leave_request import LeaveRequest

from app.leave_management.schemas.leave_request import (
    LeaveRequestCreate
)

from app.leave_management.services.leave_balance import (
    get_employee_leave_balance,
    consume_leave_balance,
    has_sufficient_balance
)

from app.leave_management.constants import (
    LEAVE_PENDING,
    LEAVE_APPROVED,
    LEAVE_REJECTED
)

from app.organization.models.employee import Employee

from app.utils.permissions import (
    is_hr_or_admin,
    is_manager_of_employee
)

from app.auth.models.user import User


def calculate_leave_days(
    start_date,
    end_date
):

    return (
        end_date - start_date
    ).days + 1
    
    

def create_leave_request(
    db: Session,
    employee_id: UUID,
    leave_request_data: LeaveRequestCreate
):

    if leave_request_data.end_date < leave_request_data.start_date:
        raise ValueError(
            "End date cannot be before start date"
        )


    requested_days = calculate_leave_days(
        leave_request_data.start_date,
        leave_request_data.end_date
    )


    leave_balance = get_employee_leave_balance(
        db,
        employee_id,
        leave_request_data.leave_type_id
    )


    if not leave_balance:
        raise ValueError(
            "Leave balance not found"
        )


    remaining_days = (
        leave_balance.allocated_days -
        leave_balance.used_days
    )


    if requested_days > remaining_days:
        raise ValueError(
            "Insufficient leave balance"
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
    
def get_manager_leave_requests(
    db: Session,
    manager_employee_id: UUID
):

    return (
        db.query(LeaveRequest)
        .join(
            Employee,
            LeaveRequest.employee_id == Employee.id
        )
        .filter(
            Employee.manager_id == manager_employee_id
        )
        .all()
    )
    

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

    if leave_request.status != LEAVE_PENDING:
        raise ValueError(
            "Leave request has already been processed"
        )

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
    
    days = (
        leave_request.end_date -
        leave_request.start_date
    ).days + 1


    if status == LEAVE_APPROVED:

        has_balance = has_sufficient_balance(
            db=db,
            employee_id=leave_request.employee_id,
            leave_type_id=leave_request.leave_type_id,
            requested_days=days
        )


        if not has_balance:
            raise ValueError(
                "Insufficient leave balance"
            )


        balance = consume_leave_balance(
            db=db,
            employee_id=leave_request.employee_id,
            leave_type_id=leave_request.leave_type_id,
            days=days
        )


        if not balance:
            raise ValueError(
                "Leave balance not found"
            )

    leave_request.status = status
    leave_request.approved_by = current_user.id
    leave_request.approved_at = datetime.now(timezone.utc)

    try:
        db.commit()
        db.refresh(leave_request)

    except Exception:
        db.rollback()
        raise


    return leave_request