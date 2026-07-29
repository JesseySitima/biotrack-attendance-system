from uuid import UUID

from pydantic import BaseModel


class LeaveTypeSimpleResponse(BaseModel):

    id: UUID

    name: str

    class Config:
        from_attributes = True



class LeaveBalanceResponse(BaseModel):

    id: UUID

    leave_type: LeaveTypeSimpleResponse

    allocated_days: int

    used_days: int

    remaining_days: int


    class Config:
        from_attributes = True