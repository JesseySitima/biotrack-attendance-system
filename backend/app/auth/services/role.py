from uuid import UUID

from sqlalchemy.orm import Session

from app.auth.models.role import Role

from app.auth.schemas.role import RoleCreate



def create_role(
    db: Session,
    role_data: RoleCreate
):

    existing_role = db.query(Role).filter(
        Role.name == role_data.name
    ).first()


    if existing_role:
        raise ValueError(
            "Role already exists"
        )


    role = Role(
        name=role_data.name,
        description=role_data.description
    )


    db.add(role)
    db.commit()
    db.refresh(role)


    return role





def get_roles(
    db: Session
):

    return db.query(Role).all()





def get_role_by_id(
    db: Session,
    role_id: UUID
):

    return db.query(Role).filter(
        Role.id == role_id
    ).first()





def delete_role(
    db: Session,
    role_id: UUID
):

    role = db.query(Role).filter(
        Role.id == role_id
    ).first()


    if not role:
        return None


    db.delete(role)
    db.commit()


    return role