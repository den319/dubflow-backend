from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.models.base import Base, UUIDMixin


class PlaybackHistory(Base, UUIDMixin):
    __tablename__ = "playback_history"
    __table_args__ = (
        UniqueConstraint("user_id", "content_id", name="uq_user_content_playback"),
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    content_id = Column(
        UUID(as_uuid=True),
        ForeignKey("contents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    progress_seconds = Column(Integer, nullable=False, default=0)
    completed = Column(Boolean, nullable=False, default=False)

    last_played_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    content = relationship("Content", back_populates="playback_history")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())