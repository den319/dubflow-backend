from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base, UUIDMixin


class User(Base, UUIDMixin):
    __tablename__ = "users"


    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    is_active = Column(Boolean, default=True)

    avatar_url = Column(String, nullable=True)

    follows = relationship(
        "UserFollow",
        foreign_keys="UserFollow.follower_id",
        backref="follower",
    )
    followers = relationship(
        "UserFollow",
        foreign_keys="UserFollow.following_id",
        backref="followed",
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
