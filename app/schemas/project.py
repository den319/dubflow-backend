from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class ProjectCreate(BaseModel):
    name: str
    source_language: str
    target_language: str


class ProjectResponse(BaseModel):
    id: UUID
    name: str
    original_file_name: str | None = None
    source_language: str
    target_language: str
    status: str
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True