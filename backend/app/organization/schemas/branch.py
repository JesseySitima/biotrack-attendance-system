from uuid import UUID

from pydantic import BaseModel


class BranchCreate(BaseModel):

    name: str
    code: str
    address: str | None = None



class BranchResponse(BaseModel):

    id: UUID
    name: str
    code: str
    address: str | None

    class Config:
        from_attributes = True