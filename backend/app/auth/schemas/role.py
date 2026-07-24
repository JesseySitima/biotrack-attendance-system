from uuid import UUID

from pydantic import BaseModel


class RoleCreate(BaseModel):

    name: str
    description: str | None = None



class RoleResponse(BaseModel):

    id: UUID
    name: str
    description: str | None = None


    class Config:
        from_attributes = True