from sqlalchemy import String, ForeignKey

from sqlalchemy.orm import mapped_column, relationship

from app.models.base import Base
from app.models.mixins import UUIDMixin, AuditMixin


class User(Base, UUIDMixin, AuditMixin):

    __tablename__ = "users"


    username = mapped_column(
        String,
        unique=True,
        nullable=False
    )


    email = mapped_column(
        String,
        unique=True,
        nullable=False
    )


    password_hash = mapped_column(
        String,
        nullable=False
    )


    role_id = mapped_column(
        ForeignKey("roles.id"),
        nullable=True
    )


    # Relationships

    role = relationship(
    "Role",
    back_populates="users",
    foreign_keys=[role_id]
    )


    employee = relationship(
        "Employee",
        back_populates="user",
        uselist=False,
        foreign_keys="Employee.user_id"
    )