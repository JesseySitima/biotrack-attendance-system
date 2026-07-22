from sqlalchemy.orm import Session

from app.organization.models.position import Position

from app.organization.schemas.position import (
    PositionCreate,
    PositionUpdate
)



def create_position(
    db: Session,
    position_data: PositionCreate
):

    position = Position(
        name=position_data.name,
        description=position_data.description,
        department_id=position_data.department_id
    )


    db.add(position)
    db.commit()
    db.refresh(position)

    return position



def get_positions(
    db: Session
):

    return db.query(Position).all()



def get_position(
    db: Session,
    position_id
):

    return (
        db.query(Position)
        .filter(
            Position.id == position_id
        )
        .first()
    )



def update_position(
    db: Session,
    position_id,
    position_data: PositionUpdate
):

    position = get_position(
        db,
        position_id
    )


    if not position:
        return None


    if position_data.name is not None:
        position.name = position_data.name


    if position_data.description is not None:
        position.description = position_data.description


    if position_data.department_id is not None:
        position.department_id = position_data.department_id


    db.commit()
    db.refresh(position)

    return position



def delete_position(
    db: Session,
    position_id
):

    position = get_position(
        db,
        position_id
    )


    if not position:
        return None


    db.delete(position)
    db.commit()

    return position