from uuid import UUID

from sqlalchemy.orm import Session

from app.leave_management.models.leave_balance import LeaveBalance
from app.leave_management.models.leave_type import LeaveType



def initialize_employee_leave_balances(
    db: Session,
    employee_id: UUID
):

    leave_types = (
       db.query(LeaveType)
        .filter(
            LeaveType.is_active == True
        )
        .all()
    )


    balances = []

    for leave_type in leave_types:

        balance = LeaveBalance(
            employee_id=employee_id,
            leave_type_id=leave_type.id,
            allocated_days=leave_type.default_days,
            used_days=0
        )

        balances.append(balance)


    db.add_all(balances)

    db.flush()

    return balances



def get_employee_leave_balances(
    db: Session,
    employee_id: UUID
):

    return (
        db.query(LeaveBalance)
        .filter(
            LeaveBalance.employee_id == employee_id
        )
        .all()
    )



def get_employee_leave_balance(
    db: Session,
    employee_id: UUID,
    leave_type_id: UUID
):

    return (
        db.query(LeaveBalance)
        .filter(
            LeaveBalance.employee_id == employee_id,
            LeaveBalance.leave_type_id == leave_type_id
        )
        .first()
    )
    
def consume_leave_balance(
    db: Session,
    employee_id: UUID,
    leave_type_id: UUID,
    days: int
):

    balance = get_employee_leave_balance(
        db,
        employee_id,
        leave_type_id
    )


    if not balance:
        return None


    balance.used_days += days


    db.flush()


    return balance

def restore_leave_balance(
    db: Session,
    employee_id,
    leave_type_id,
    days: float
):
    balance = get_employee_leave_balance(
        db=db,
        employee_id=employee_id,
        leave_type_id=leave_type_id
    )

    if not balance:
        return None

    balance.used_days -= days

    if balance.used_days < 0:
        balance.used_days = 0.0

    db.commit()
    db.refresh(balance)

    return balance

def has_sufficient_balance(
    db: Session,
    employee_id: UUID,
    leave_type_id: UUID,
    requested_days: int
):

    balance = get_employee_leave_balance(
        db,
        employee_id,
        leave_type_id
    )


    if not balance:
        return False


    remaining_days = (
        balance.allocated_days -
        balance.used_days
    )


    return remaining_days >= requested_days