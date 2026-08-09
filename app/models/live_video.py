from sqlalchemy import Column, String, ForeignKey, Integer, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.models.base import Base, UUIDMixin


class LiveVideo(Base, UUIDMixin):
    __tablename__ = "live_videos"

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    thumbnail_url = Column(String, nullable=True)

    creator_id = Column(
        UUID(as_uuid=True),
        ForeignKey("content_creators.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    language = Column(String, nullable=False, default="en")

    viewer_count = Column(Integer, nullable=False, default=0)

    is_live = Column(Boolean, nullable=False, default=True)

    started_at = Column(DateTime(timezone=True), nullable=True)

    sort_order = Column(Integer, nullable=False, default=0)

    creator = relationship("ContentCreator", backref="live_videos")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())