from sqlalchemy import (
    String,
    Integer,
    Boolean
)

from app.models.base import Base
from app.models.mixins import UUIDMixin, AuditMixin

from sqlalchemy.orm import mapped_column


class LeaveType(
    Base,
    UUIDMixin,
    AuditMixin
):

    __tablename__ = "leave_types"


    name = mapped_column(
        String,
        unique=True,
        nullable=False
    )


    description = mapped_column(
        String,
        nullable=True
    )


    default_days = mapped_column(
        Integer,
        nullable=False
    )


    is_paid = mapped_column(
        Boolean,
        default=True
    )