from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.auth.schemas.role import RoleResponse


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role_id: UUID

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):

    id: UUID
    username: str
    email: EmailStr
    role: RoleResponse
    is_active: bool


    class Config:
        from_attributes = True