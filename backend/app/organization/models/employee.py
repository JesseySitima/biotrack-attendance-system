from sqlalchemy import (
    String,
    ForeignKey
)

from sqlalchemy.orm import (
    mapped_column,
    relationship
)

from app.models.base import Base
from app.models.mixins import UUIDMixin, AuditMixin


class Employee(
    Base,
    UUIDMixin,
    AuditMixin
):

    __tablename__ = "employees"


    employee_number = mapped_column(
        String,
        unique=True,
        nullable=False
    )


    first_name = mapped_column(
        String,
        nullable=False
    )


    last_name = mapped_column(
        String,
        nullable=False
    )


    phone = mapped_column(
        String,
        nullable=True
    )


    email = mapped_column(
        String,
        nullable=True
    )


    user_id = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        unique=True
    )


    branch_id = mapped_column(
        ForeignKey("branches.id"),
        nullable=False
    )


    department_id = mapped_column(
        ForeignKey("departments.id"),
        nullable=False
    )


    position_id = mapped_column(
        ForeignKey("positions.id"),
        nullable=False
    )
    
    manager_id = mapped_column(
    ForeignKey("employees.id"),
    nullable=True
)


    # Relationships

    user = relationship(
        "User",
        back_populates="employee",
        foreign_keys=[user_id]
    )


    branch = relationship(
        "Branch",
        back_populates="employees"
    )


    department = relationship(
        "Department",
        back_populates="employees"
    )


    position = relationship(
        "Position",
        back_populates="employees"
    )
    
    manager = relationship(
    "Employee",
    remote_side="Employee.id",
    back_populates="team_members"
)


    team_members = relationship(
        "Employee",
        back_populates="manager"
    )