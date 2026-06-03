

from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.sql import func

from app.models.base import Base, UUIDMixin


class TranslationCache(Base, UUIDMixin):
    __tablename__ = "translation_cache"

    source_text = Column(
        Text,
        nullable=False,
        index=True,
    )

    source_language = Column(
        String,
        nullable=False,
    )

    target_language = Column(
        String,
        nullable=False,
    )

    translated_text = Column(
        Text,
        nullable=False,
    )

    provider_name = Column(
        String,
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )