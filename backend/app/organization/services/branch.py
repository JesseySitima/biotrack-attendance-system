from sqlalchemy.orm import Session

from uuid import UUID

from app.organization.models.branch import Branch
from app.organization.schemas import BranchCreate



def create_branch(
    db: Session,
    branch_data: BranchCreate
):

    branch = Branch(
        name=branch_data.name,
        code=branch_data.code,
        address=branch_data.address
    )

    db.add(branch)
    db.commit()
    db.refresh(branch)

    return branch



def get_branches(
    db: Session
):

    return (
        db.query(Branch)
        .filter(
            Branch.is_active == True
        )
        .all()
    )



def get_branch(
    db: Session,
    branch_id: UUID
):

    return (
        db.query(Branch)
        .filter(
            Branch.id == branch_id
        )
        .first()
    )



def update_branch(
    db: Session,
    branch: Branch,
    branch_data: BranchCreate
):

    branch.name = branch_data.name
    branch.code = branch_data.code
    branch.address = branch_data.address

    db.commit()
    db.refresh(branch)

    return branch



def deactivate_branch(
    db: Session,
    branch: Branch
):

    branch.is_active = False

    db.commit()