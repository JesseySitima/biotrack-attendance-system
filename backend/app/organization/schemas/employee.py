from uuid import UUID

from pydantic import (
    BaseModel,
    EmailStr,
    Field
)

from app.organization.schemas.branch import BranchResponse
from app.organization.schemas.department import DepartmentResponse
from app.organization.schemas.position import PositionResponse

class EmployeeCreate(BaseModel):

    first_name: str = Field(
        min_length=2,
        max_length=50
    )

    last_name: str = Field(
        min_length=2,
        max_length=50
    )

    phone: str | None = Field(
        default=None,
        max_length=20
    )

    email: EmailStr | None = None

    branch_id: UUID

    department_id: UUID

    position_id: UUID
    
    manager_id: UUID | None = None


class EmployeeUpdate(BaseModel):

    employee_number: str = Field(
            min_length=3,
            max_length=20
        )
    
    first_name: str = Field(
            min_length=2,
            max_length=50
        )
    
    last_name: str = Field(
            min_length=2,
            max_length=50
        )
    
    phone: str | None = Field(
            default=None,
            max_length=20
        )
    
    email: EmailStr | None = None
    
    manager_id: UUID | None = None


class ManagerResponse(BaseModel):

    id: UUID

    employee_number: str

    first_name: str

    last_name: str


    class Config:
        from_attributes = True


class EmployeeResponse(BaseModel):

    id: UUID

    employee_number: str

    first_name: str

    last_name: str

    phone: str | None

    email: str | None

    user_id: UUID | None

    branch: BranchResponse

    department: DepartmentResponse

    position: PositionResponse
    
    manager: ManagerResponse | None = None


    class Config:
        from_attributes = True