from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Query
)

from sqlalchemy.orm import Session


from app.database import get_db


from app.auth.models.user import User


from app.utils.dependencies import get_current_user

from app.utils.permissions import (
    is_hr_or_admin
)

from app.leave_management.schemas.leave_request import (
    LeaveRequestCreate,
    LeaveRequestResponse
)


from app.leave_management.services import (
    create_leave_request,
    approve_leave_request,
    get_employee_leave_requests,
    get_manager_leave_requests,
    get_leave_requests
)

from app.leave_management.constants import (
    LEAVE_APPROVED,
    LEAVE_REJECTED
)



router = APIRouter(
    prefix="/leave-requests",
    tags=["Leave Requests"]
)

@router.get(
    "/my",
    response_model=list[LeaveRequestResponse]
)
def my_leave_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    employee = current_user.employee


    if employee is None:
        raise HTTPException(
            status_code=400,
            detail="User is not linked to an employee"
        )


    return get_employee_leave_requests(
        db,
        employee.id
    )

@router.get(
    "/team",
    response_model=list[LeaveRequestResponse]
)
def team_leave_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    employee = current_user.employee

    if employee is None:
        raise HTTPException(
            status_code=400,
            detail="User is not linked to an employee"
        )

    return get_manager_leave_requests(
        db,
        employee.id
    ) 
 
 
    
@router.get(
    "",
    response_model=list[LeaveRequestResponse]
)
def all_leave_requests(
    status_filter: str | None = Query(
        default=None,
        alias="status"
    ),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if not is_hr_or_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to view all leave requests"
        )


    return get_leave_requests(
        db,
        status_filter
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


    try:
        return create_leave_request(
            db,
            employee.id,
            leave_request
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
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

@router.put(
    "/{leave_request_id}/reject",
    response_model=LeaveRequestResponse
)
def reject_leave(
    leave_request_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    leave_request = approve_leave_request(
        db=db,
        leave_request_id=leave_request_id,
        current_user=current_user,
        status=LEAVE_REJECTED
    )


    if leave_request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Leave request not found"
        )


    if leave_request is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to reject this leave request"
        )


    return leave_request