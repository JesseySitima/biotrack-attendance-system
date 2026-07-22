from uuid import UUID

from pydantic import BaseModel



class PositionCreate(BaseModel):

    name: str
    description: str | None = None
    department_id: UUID



class PositionUpdate(BaseModel):

    name: str | None = None
    description: str | None = None
    department_id: UUID | None = None



class PositionResponse(BaseModel):

    id: UUID
    name: str
    description: str | None
    department_id: UUID


    class Config:
        from_attributes = True