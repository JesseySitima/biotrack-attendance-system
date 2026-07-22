from uuid import UUID

from pydantic import BaseModel



class EmployeeCreate(BaseModel):

    employee_number: str

    first_name: str

    last_name: str

    phone: str | None = None

    email: str | None = None

    branch_id: UUID

    department_id: UUID

    position_id: UUID



class EmployeeUpdate(BaseModel):

    first_name: str | None = None

    last_name: str | None = None

    phone: str | None = None

    email: str | None = None

    branch_id: UUID | None = None

    department_id: UUID | None = None

    position_id: UUID | None = None



class EmployeeResponse(BaseModel):

    id: UUID

    employee_number: str

    first_name: str

    last_name: str

    phone: str | None

    email: str | None

    user_id: UUID | None

    branch_id: UUID

    department_id: UUID

    position_id: UUID


    class Config:
        from_attributes = True