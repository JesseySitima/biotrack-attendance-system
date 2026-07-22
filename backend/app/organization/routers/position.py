from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database import get_db


from app.organization.schemas.position import (
    PositionCreate,
    PositionUpdate,
    PositionResponse
)


from app.organization.services.position import (
    create_position,
    get_positions,
    get_position,
    update_position,
    delete_position
)


router = APIRouter(
    prefix="/positions",
    tags=["Positions"]
)



@router.post(
    "",
    response_model=PositionResponse
)
def add_position(
    position: PositionCreate,
    db: Session = Depends(get_db)
):

    return create_position(
        db,
        position
    )



@router.get(
    "",
    response_model=list[PositionResponse]
)
def list_positions(
    db: Session = Depends(get_db)
):

    return get_positions(db)



@router.get(
    "/{position_id}",
    response_model=PositionResponse
)
def get_single_position(
    position_id: UUID,
    db: Session = Depends(get_db)
):

    position = get_position(
        db,
        position_id
    )


    if not position:
        raise HTTPException(
            status_code=404,
            detail="Position not found"
        )


    return position



@router.put(
    "/{position_id}",
    response_model=PositionResponse
)
def edit_position(
    position_id: UUID,
    position: PositionUpdate,
    db: Session = Depends(get_db)
):

    updated_position = update_position(
        db,
        position_id,
        position
    )


    if not updated_position:
        raise HTTPException(
            status_code=404,
            detail="Position not found"
        )


    return updated_position



@router.delete(
    "/{position_id}"
)
def remove_position(
    position_id: UUID,
    db: Session = Depends(get_db)
):

    deleted_position = delete_position(
        db,
        position_id
    )


    if not deleted_position:
        raise HTTPException(
            status_code=404,
            detail="Position not found"
        )


    return {
        "message": "Position deleted successfully"
    }