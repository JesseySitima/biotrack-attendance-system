from datetime import date

from sqlalchemy import (
    String,
    Date
)

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.models.base import Base
from app.models.mixins import UUIDMixin


class PublicHoliday(
    Base,
    UUIDMixin
):
    __tablename__ = "public_holidays"

    name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    holiday_date: Mapped[date] = mapped_column(
        Date,
        unique=True,
        nullable=False
    )