from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session


from app.database import get_db

from app.auth.schemas.role import (
    RoleCreate,
    RoleResponse
)

from app.auth.services import role



router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)





@router.post(
    "/",
    response_model=RoleResponse
)
def create_role(
    role_data: RoleCreate,
    db: Session = Depends(get_db)
):

    try:

        return role.create_role(
            db,
            role_data
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )





@router.get(
    "/",
    response_model=list[RoleResponse]
)
def get_roles(
    db: Session = Depends(get_db)
):

    return role.get_roles(
        db
    )





@router.get(
    "/{role_id}",
    response_model=RoleResponse
)
def get_role(
    role_id: UUID,
    db: Session = Depends(get_db)
):

    role = role.get_role_by_id(
        db,
        role_id
    )


    if not role:

        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )


    return role





@router.delete(
    "/{role_id}"
)
def delete_role(
    role_id: UUID,
    db: Session = Depends(get_db)
):

    role = role.delete_role(
        db,
        role_id
    )


    if not role:

        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )


    return {
        "message": "Role deleted successfully"
    }