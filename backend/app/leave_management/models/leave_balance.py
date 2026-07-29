from sqlalchemy import (
    Integer,
    ForeignKey,
    UniqueConstraint
)

from sqlalchemy.orm import (
    mapped_column,
    relationship
)

from app.models.base import Base
from app.models.mixins import UUIDMixin, AuditMixin


class LeaveBalance(
    Base,
    UUIDMixin,
    AuditMixin
):

    __tablename__ = "leave_balances"


    __table_args__ = (
        UniqueConstraint(
            "employee_id",
            "leave_type_id"
        ),
    )


    employee_id = mapped_column(
        ForeignKey("employees.id"),
        nullable=False
    )


    leave_type_id = mapped_column(
        ForeignKey("leave_types.id"),
        nullable=False
    )


    allocated_days = mapped_column(
        Integer,
        nullable=False
    )


    used_days = mapped_column(
        Integer,
        nullable=False,
        default=0
    )


    # Relationships

    employee = relationship(
        "Employee"
    )


    leave_type = relationship(
        "LeaveType"
    )
    
    @property
    def remaining_days(self) -> int:
        return self.allocated_days - self.used_days