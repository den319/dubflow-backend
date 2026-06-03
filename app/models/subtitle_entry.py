

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Text,
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import Index

from app.models.base import Base, UUIDMixin


class SubtitleEntry(Base, UUIDMixin):
    __tablename__ = "subtitle_entries"

    __table_args__ = (
        Index(
            "idx_subtitle_translation_status",
            "subtitle_file_id",
            "translation_status",
        ),
    )

    subtitle_file_id = Column(
        UUID(as_uuid=True),
        ForeignKey("subtitle_files.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    sequence_number = Column(
        Integer,
        nullable=False,
    )

    start_time = Column(
        String,
        nullable=False,
    )

    end_time = Column(
        String,
        nullable=False,
    )

    original_text = Column(
        Text,
        nullable=False,
    )

    translated_text = Column(
        Text,
        nullable=True,
    )

    translation_status = Column(
        String,
        nullable=False,
        default="pending",
    )

    subtitle_file = relationship(
        "SubtitleFile",
        back_populates="entries",
    )

    error_message = Column(
        Text,
        nullable=True,
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
