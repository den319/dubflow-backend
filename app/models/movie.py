from sqlalchemy import Column, String, Float, Integer, Text, Boolean, DateTime
from sqlalchemy.sql import func

from app.models.base import Base, UUIDMixin


class Movie(Base, UUIDMixin):
    __tablename__ = "movies"

    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    poster_url = Column(String, nullable=True)
    banner_url = Column(String, nullable=True)

    source_language = Column(String, nullable=False, default="en")

    content_type = Column(String, nullable=False, default="movie")

    is_popular = Column(Boolean, nullable=False, default=False)
    is_featured = Column(Boolean, nullable=False, default=False)

    rating = Column(Float, nullable=True)
    release_year = Column(Integer, nullable=True)

    sort_order = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())