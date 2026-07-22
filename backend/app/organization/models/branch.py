from sqlalchemy import String

from sqlalchemy.orm import (
    mapped_column,
    relationship
)

from app.models.base import Base
from app.models.mixins import UUIDMixin, AuditMixin


class Branch(
    Base,
    UUIDMixin,
    AuditMixin
):

    __tablename__ = "branches"


    name = mapped_column(
        String,
        nullable=False
    )


    code = mapped_column(
        String,
        unique=True,
        nullable=False
    )


    address = mapped_column(
        String,
        nullable=True
    )
    
    employees = relationship(
    "Employee",
    back_populates="branch"
    )