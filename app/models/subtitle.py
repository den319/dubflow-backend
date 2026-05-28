import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Subtitle(Base):
    __tablename__ = "subtitle"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    project_id = Column(UUID(as_uuid=True), ForeignKey("project.id"), nullable=False)

    original_subtitle_file = Column(String, nullable=False)
    translated_subtitle_file = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())