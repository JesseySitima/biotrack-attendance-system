from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session


from app.database import get_db


from app.auth.models.user import User


from app.utils.dependencies import get_current_user


from app.leave_management.schemas.leave_request import (
    LeaveRequestCreate,
    LeaveRequestResponse
)


from app.leave_management.services import (
    create_leave_request,
    approve_leave_request
)

from app.leave_management.constants import (
    LEAVE_APPROVED
)



router = APIRouter(
    prefix="/leave-requests",
    tags=["Leave Requests"]
)

@router.post(
    "",
    response_model=LeaveRequestResponse
)
def request_leave(
    leave_request: LeaveRequestCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    employee = current_user.employee


    if employee is None:
        raise HTTPException(
            status_code=400,
            detail="User is not linked to an employee"
        )


    return create_leave_request(
        db,
        employee.id,
        leave_request
    )
    
@router.put(
    "/{leave_request_id}/approve",
    response_model=LeaveRequestResponse
)
def approve_leave(
    leave_request_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    leave_request = approve_leave_request(
        db=db,
        leave_request_id=leave_request_id,
        current_user=current_user,
        status=LEAVE_APPROVED
    )


    if leave_request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Leave request not found"
        )


    if leave_request is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to approve this leave request"
        )


    return leave_request