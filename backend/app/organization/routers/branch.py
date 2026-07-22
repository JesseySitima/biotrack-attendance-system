from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from uuid import UUID

from app.database import get_db

from app.organization.schemas import (
    BranchCreate,
    BranchResponse
)

from app.organization.services import (
    create_branch,
    get_branches,
    get_branch,
    update_branch,
    deactivate_branch
)


router = APIRouter(
    prefix="/branches",
    tags=["Branches"]
)


@router.post(
    "",
    response_model=BranchResponse
)
def add_branch(
    branch: BranchCreate,
    db: Session = Depends(get_db)
):

    return create_branch(
        db,
        branch
    )



@router.get(
    "",
    response_model=list[BranchResponse]
)
def list_branches(
    db: Session = Depends(get_db)
):

    return get_branches(db)



@router.get(
    "/{branch_id}",
    response_model=BranchResponse
)
def retrieve_branch(
    branch_id: UUID,
    db: Session = Depends(get_db)
):

    branch = get_branch(
        db,
        branch_id
    )

    if not branch:
        raise HTTPException(
            status_code=404,
            detail="Branch not found"
        )

    return branch



@router.put(
    "/{branch_id}",
    response_model=BranchResponse
)
def edit_branch(
    branch_id: UUID,
    branch_data: BranchCreate,
    db: Session = Depends(get_db)
):

    branch = get_branch(
        db,
        branch_id
    )

    if not branch:
        raise HTTPException(
            status_code=404,
            detail="Branch not found"
        )

    return update_branch(
        db,
        branch,
        branch_data
    )



@router.delete(
    "/{branch_id}"
)
def remove_branch(
    branch_id: UUID,
    db: Session = Depends(get_db)
):

    branch = get_branch(
        db,
        branch_id
    )

    if not branch:
        raise HTTPException(
            status_code=404,
            detail="Branch not found"
        )

    deactivate_branch(
        db,
        branch
    )

    return {
        "message": "Branch deactivated"
    }