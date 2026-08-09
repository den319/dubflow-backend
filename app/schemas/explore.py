from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


# --- Sub-schemas ---

class CreatorResponse(BaseModel):
    id: UUID
    username: str
    display_name: str
    avatar_url: str | None = None
    is_verified: bool

    class Config:
        from_attributes = True


class CategoryResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    icon_url: str | None = None

    class Config:
        from_attributes = True


class ContentResponse(BaseModel):
    id: UUID
    title: str
    description: str | None = None
    content_type: str
    thumbnail_url: str | None = None
    banner_url: str | None = None
    creator: CreatorResponse
    view_count: int
    like_count: int
    duration_seconds: int
    created_at: datetime

    class Config:
        from_attributes = True


class TopArtistResponse(BaseModel):
    id: UUID
    username: str
    display_name: str
    avatar_url: str | None = None
    is_verified: bool
    follower_count: int

    class Config:
        from_attributes = True


# --- Explore response ---

class ExploreContentSections(BaseModel):
    recent: list[ContentResponse]
    following: list[ContentResponse]
    trendy: list[ContentResponse]
    learning: list[ContentResponse]


class ExploreResponse(BaseModel):
    featured: list[ContentResponse]
    categories: list[CategoryResponse]
    content: ExploreContentSections
    trending_now: list[ContentResponse]
    top_artists: list[TopArtistResponse]
    recently_played: list[ContentResponse]