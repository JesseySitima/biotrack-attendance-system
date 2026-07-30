from sqlalchemy import Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class WorkSchedule(Base):
    __tablename__ = "work_schedule"

    weekday: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    is_working_day: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )