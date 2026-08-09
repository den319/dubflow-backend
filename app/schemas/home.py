from uuid import UUID
from pydantic import BaseModel


# --- Sub-schemas ---

class HomeUser(BaseModel):
    id: UUID
    username: str
    avatar_url: str | None = None

    class Config:
        from_attributes = True


class HomeBannerResponse(BaseModel):
    id: UUID
    title: str
    subtitle: str | None = None
    image_url: str
    content_type: str | None = None
    content_id: UUID | None = None

    class Config:
        from_attributes = True


class MovieResponse(BaseModel):
    id: UUID
    title: str
    poster_url: str | None = None
    banner_url: str | None = None
    source_language: str
    content_type: str

    is_popular: bool
    is_featured: bool
    rating: float | None = None
    release_year: int | None = None

    class Config:
        from_attributes = True


class CreatorResponse(BaseModel):
    id: UUID
    name: str
    username: str
    avatar_url: str | None = None
    is_verified: bool

    class Config:
        from_attributes = True


class ShortCreatorResponse(BaseModel):
    id: UUID
    name: str
    username: str
    avatar_url: str | None = None

    class Config:
        from_attributes = True


class ShortResponse(BaseModel):
    id: UUID
    title: str
    thumbnail_url: str | None = None
    creator: ShortCreatorResponse
    language: str
    views_count: int

    class Config:
        from_attributes = True


class LiveVideoCreatorResponse(BaseModel):
    id: UUID
    name: str
    username: str
    avatar_url: str | None = None

    class Config:
        from_attributes = True


class LiveVideoResponse(BaseModel):
    id: UUID
    title: str
    thumbnail_url: str | None = None
    creator: LiveVideoCreatorResponse
    language: str
    viewer_count: int
    is_live: bool

    class Config:
        from_attributes = True


# --- Home response ---

class HomeResponse(BaseModel):
    user: HomeUser
    banners: list[HomeBannerResponse]
    popular_movies: list[MovieResponse]
    creators: list[CreatorResponse]
    shorts: list[ShortResponse]
    live_videos: list[LiveVideoResponse]