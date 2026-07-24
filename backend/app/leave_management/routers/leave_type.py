from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session


from app.database import get_db


from app.leave_management.schemas import (
    LeaveTypeCreate,
    LeaveTypeUpdate,
    LeaveTypeResponse
)


from app.leave_management.services import (
    create_leave_type,
    get_leave_types,
    get_leave_type,
    update_leave_type,
    delete_leave_type
)



router = APIRouter(
    prefix="/leave-types",
    tags=["Leave Types"]
)



@router.post(
    "",
    response_model=LeaveTypeResponse
)
def add_leave_type(
    leave_type: LeaveTypeCreate,
    db: Session = Depends(get_db)
):

    return create_leave_type(
        db,
        leave_type
    )



@router.get(
    "",
    response_model=list[LeaveTypeResponse]
)
def list_leave_types(
    db: Session = Depends(get_db)
):

    return get_leave_types(db)



@router.get(
    "/{leave_type_id}",
    response_model=LeaveTypeResponse
)
def retrieve_leave_type(
    leave_type_id: UUID,
    db: Session = Depends(get_db)
):

    leave_type = get_leave_type(
        db,
        leave_type_id
    )


    if not leave_type:
        raise HTTPException(
            status_code=404,
            detail="Leave type not found"
        )


    return leave_type



@router.put(
    "/{leave_type_id}",
    response_model=LeaveTypeResponse
)
def edit_leave_type(
    leave_type_id: UUID,
    leave_type: LeaveTypeUpdate,
    db: Session = Depends(get_db)
):

    updated_leave_type = update_leave_type(
        db,
        leave_type_id,
        leave_type
    )


    if not updated_leave_type:
        raise HTTPException(
            status_code=404,
            detail="Leave type not found"
        )


    return updated_leave_type



@router.delete(
    "/{leave_type_id}"
)
def remove_leave_type(
    leave_type_id: UUID,
    db: Session = Depends(get_db)
):

    leave_type = delete_leave_type(
        db,
        leave_type_id
    )


    if not leave_type:
        raise HTTPException(
            status_code=404,
            detail="Leave type not found"
        )


    return {
        "message": "Leave type deleted successfully"
    }