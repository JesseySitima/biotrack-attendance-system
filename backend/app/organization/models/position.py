from sqlalchemy import (
    ForeignKey,
    String
)

from sqlalchemy.orm import (
    mapped_column,
    relationship
)

from app.models.base import Base
from app.models.mixins import UUIDMixin, AuditMixin


class Position(
    Base,
    UUIDMixin,
    AuditMixin
):

    __tablename__ = "positions"


    name = mapped_column(
        String,
        nullable=False
    )


    description = mapped_column(
        String,
        nullable=True
    )


    department_id = mapped_column(
        ForeignKey("departments.id"),
        nullable=False
    )


    department = relationship(
    "Department",
    back_populates="positions"
    )
    
    employees = relationship(
    "Employee",
    back_populates="position"
    )