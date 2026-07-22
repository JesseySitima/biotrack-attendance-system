from sqlalchemy import String

from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.models.mixins import UUIDMixin, AuditMixin


class User(
    Base,
    UUIDMixin,
    AuditMixin
):

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


    role = mapped_column(
        String,
        default="employee"
    )
    
    employee = relationship(
    "Employee",
    back_populates="user",
    uselist=False,
    foreign_keys="Employee.user_id"
)