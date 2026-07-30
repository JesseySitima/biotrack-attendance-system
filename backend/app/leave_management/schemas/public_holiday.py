from uuid import UUID
from datetime import date

from pydantic import BaseModel


class PublicHolidayCreate(BaseModel):

    name: str
    holiday_date: date


class PublicHolidayResponse(BaseModel):

    id: UUID
    name: str
    holiday_date: date

    class Config:
        from_attributes = True