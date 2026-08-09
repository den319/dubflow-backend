from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


# --- HomeBanner ---

class HomeBannerCreate(BaseModel):
    title: str
    subtitle: str | None = None
    image_url: str
    content_type: str | None = None
    content_id: UUID | None = None
    is_active: bool = True
    sort_order: int = 0


class HomeBannerUpdate(BaseModel):
    title: str | None = None
    subtitle: str | None = None
    image_url: str | None = None
    content_type: str | None = None
    content_id: UUID | None = None
    is_active: bool | None = None
    sort_order: int | None = None


# --- Movie ---

class MovieCreate(BaseModel):
    title: str
    description: str | None = None
    poster_url: str | None = None
    banner_url: str | None = None
    source_language: str = "en"
    content_type: str = "movie"
    is_popular: bool = False
    is_featured: bool = False
    rating: float | None = None
    release_year: int | None = None
    sort_order: int = 0


class MovieUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    poster_url: str | None = None
    banner_url: str | None = None
    source_language: str | None = None
    content_type: str | None = None
    is_popular: bool | None = None
    is_featured: bool | None = None
    rating: float | None = None
    release_year: int | None = None
    sort_order: int | None = None


# --- ContentCreator ---

class ContentCreatorCreate(BaseModel):
    name: str
    username: str
    avatar_url: str | None = None
    bio: str | None = None
    is_verified: bool = False


class ContentCreatorUpdate(BaseModel):
    name: str | None = None
    username: str | None = None
    avatar_url: str | None = None
    bio: str | None = None
    is_verified: bool | None = None


# --- Short ---

class ShortCreate(BaseModel):
    title: str
    description: str | None = None
    thumbnail_url: str | None = None
    creator_id: UUID
    language: str = "en"
    views_count: int = 0
    is_published: bool = True
    sort_order: int = 0


class ShortUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    thumbnail_url: str | None = None
    creator_id: UUID | None = None
    language: str | None = None
    views_count: int | None = None
    is_published: bool | None = None
    sort_order: int | None = None


# --- LiveVideo ---

class LiveVideoCreate(BaseModel):
    title: str
    description: str | None = None
    thumbnail_url: str | None = None
    creator_id: UUID
    language: str = "en"
    viewer_count: int = 0
    is_live: bool = True
    started_at: datetime | None = None
    sort_order: int = 0


class LiveVideoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    thumbnail_url: str | None = None
    creator_id: UUID | None = None
    language: str | None = None
    viewer_count: int | None = None
    is_live: bool | None = None
    started_at: datetime | None = None
    sort_order: int | None = None