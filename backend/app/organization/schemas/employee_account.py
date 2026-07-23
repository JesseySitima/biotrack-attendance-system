from uuid import UUID

from pydantic import BaseModel, EmailStr


class EmployeeAccountCreate(BaseModel):

    username: str
    email: EmailStr
    password: str
    role_id: UUID