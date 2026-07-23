from sqlalchemy import String

from sqlalchemy.orm import (
    mapped_column,
    relationship
)

from app.models.base import Base
from app.models.mixins import UUIDMixin, AuditMixin


class Role(
    Base,
    UUIDMixin,
    AuditMixin
):

    __tablename__ = "roles"


    name = mapped_column(
        String,
        unique=True,
        nullable=False
    )


    description = mapped_column(
        String,
        nullable=True
    )


    users = relationship(
    "User",
    back_populates="role",
    foreign_keys="User.role_id"
)