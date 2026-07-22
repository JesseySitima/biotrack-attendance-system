from sqlalchemy import String

from sqlalchemy.orm import (
    mapped_column,
    relationship
)

from app.models.base import Base
from app.models.mixins import UUIDMixin, AuditMixin


class Department(
    Base,
    UUIDMixin,
    AuditMixin
):

    __tablename__ = "departments"


    name = mapped_column(
        String,
        nullable=False
    )


    code = mapped_column(
        String,
        unique=True,
        nullable=False
    )


    description = mapped_column(
        String,
        nullable=True
    )
    
    positions = relationship(
    "Position",
    back_populates="department"
    )
    
    employees = relationship(
    "Employee",
    back_populates="department"
    )