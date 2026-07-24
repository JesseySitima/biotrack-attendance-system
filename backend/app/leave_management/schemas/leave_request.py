from uuid import UUID
from datetime import date, datetime

from pydantic import BaseModel


class LeaveRequestCreate(BaseModel):

    leave_type_id: UUID
    start_date: date
    end_date: date
    reason: str | None = None



class LeaveRequestResponse(BaseModel):

    id: UUID

    employee_id: UUID
    leave_type_id: UUID

    start_date: date
    end_date: date

    reason: str | None = None

    status: str

    approved_by: UUID | None = None
    approved_at: datetime | None = None

    is_active: bool


    class Config:
        from_attributes = True
        
class LeaveRequestApproval(BaseModel):

    status: str