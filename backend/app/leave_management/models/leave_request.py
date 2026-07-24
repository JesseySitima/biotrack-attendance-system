from sqlalchemy import (
    String,
    Date,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import (
    mapped_column,
    relationship
)

from datetime import datetime

from app.models.base import Base
from app.models.mixins import UUIDMixin, AuditMixin

class LeaveRequest(
    Base,
    UUIDMixin,
    AuditMixin
):

    __tablename__ = "leave_requests"


    employee_id = mapped_column(
        ForeignKey("employees.id"),
        nullable=False
    )


    leave_type_id = mapped_column(
        ForeignKey("leave_types.id"),
        nullable=False
    )


    start_date = mapped_column(
        Date,
        nullable=False
    )


    end_date = mapped_column(
        Date,
        nullable=False
    )


    reason = mapped_column(
        String,
        nullable=True
    )


    status = mapped_column(
        String,
        nullable=False,
        default="PENDING"
    )


    approved_by = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )


    approved_at = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
        # Relationships

    employee = relationship(
        "Employee"
    )


    leave_type = relationship(
        "LeaveType"
    )


    approver = relationship(
        "User",
        foreign_keys=[approved_by]
    )