from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, ForeignKey, DateTime, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.models.base import Base, UUIDMixin


class SubtitleFile(Base, UUIDMixin):
    __tablename__ = "subtitle_files"

    project_id = Column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    file_type = Column(
        String,
        nullable=False,
        default="srt",
    )

    source_language = Column(
        String,
        nullable=False,
    )

    target_language = Column(
        String,
        nullable=False,
    )

    original_file_path = Column(
        String,
        nullable=False,
    )

    translated_file_path = Column(
        String,
        nullable=True,
    )

    total_entries = Column(
        Integer,
        nullable=False,
        default=0,
    )

    translated_entries = Column(
        Integer,
        nullable=False,
        default=0,
    )

    status = Column(
        String,
        nullable=False,
        default="uploaded",
    )

    entries = relationship(
        "SubtitleEntry",
        back_populates="subtitle_file",
        cascade="all, delete-orphan",
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )