from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.models.base import Base, UUIDMixin


class Content(Base, UUIDMixin):
    __tablename__ = "contents"

    creator_id = Column(
        UUID(as_uuid=True),
        ForeignKey("creator_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    content_type = Column(String, nullable=False, default="video")  # movie | short | video | live

    thumbnail_url = Column(String, nullable=True)
    banner_url = Column(String, nullable=True)

    status = Column(String, nullable=False, default="published")  # draft | published | archived
    visibility = Column(String, nullable=False, default="public")  # public | private | unlisted

    duration_seconds = Column(Integer, nullable=False, default=0)

    view_count = Column(Integer, nullable=False, default=0)
    like_count = Column(Integer, nullable=False, default=0)

    is_featured = Column(Boolean, nullable=False, default=False)

    creator = relationship("CreatorProfile", back_populates="content")

    categories = relationship(
        "Category",
        secondary="content_categories",
        back_populates="contents",
    )

    playback_history = relationship("PlaybackHistory", back_populates="content")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())