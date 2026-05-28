import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Project(Base):
    __tablename__ = "project"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False, index=True)

    video_name = Column(String, nullable=False)
    source_language = Column(String, nullable=False)
    target_language = Column(String, nullable=False)

    status = Column(String, default="pending")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())