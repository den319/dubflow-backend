from sqlalchemy import Column, String, Text, Boolean, DateTime
from sqlalchemy.sql import func

from app.models.base import Base, UUIDMixin


class ContentCreator(Base, UUIDMixin):
    __tablename__ = "content_creators"

    name = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    avatar_url = Column(String, nullable=True)
    bio = Column(Text, nullable=True)

    is_verified = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())