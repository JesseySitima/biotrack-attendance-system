from uuid import UUID

from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.leave_management.services.leave_balance import (
    get_employee_leave_balances
)

from app.leave_management.schemas.leave_balance import (
    LeaveBalanceResponse
)


router = APIRouter(
    prefix="/leave-balances",
    tags=["Leave Balances"]
)


@router.get(
    "/employee/{employee_id}",
    response_model=list[LeaveBalanceResponse]
)
def get_employee_balances(
    employee_id: UUID,
    db: Session = Depends(get_db)
):

    return get_employee_leave_balances(
        db,
        employee_id
    )