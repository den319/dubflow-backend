
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.models.base import Base, UUIDMixin


class Project(Base, UUIDMixin):
    __tablename__ = "projects"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    original_file_name = Column(String, nullable=False)
    source_language = Column(String, nullable=False)
    target_language = Column(String, nullable=False)

    status = Column(String, nullable=False, default="pending")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())