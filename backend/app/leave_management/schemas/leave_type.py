from uuid import UUID

from pydantic import BaseModel


class LeaveTypeCreate(BaseModel):

    name: str
    description: str | None = None
    default_days: int
    is_paid: bool = True


class LeaveTypeUpdate(BaseModel):

    name: str | None = None
    description: str | None = None
    default_days: int | None = None
    is_paid: bool | None = None


class LeaveTypeResponse(BaseModel):

    id: UUID
    name: str
    description: str | None = None
    default_days: int
    is_paid: bool
    is_active: bool

    class Config:
        from_attributes = True