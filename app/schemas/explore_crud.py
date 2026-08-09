from uuid import UUID
from pydantic import BaseModel


# --- Category ---

class CategoryCreate(BaseModel):
    name: str
    slug: str
    description: str | None = None
    icon_url: str | None = None


class CategoryUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    description: str | None = None
    icon_url: str | None = None


# --- CreatorProfile ---

class CreatorProfileCreate(BaseModel):
    user_id: UUID
    display_name: str
    bio: str | None = None
    avatar_url: str | None = None
    is_verified: bool = False
    follower_count: int = 0


class CreatorProfileUpdate(BaseModel):
    display_name: str | None = None
    bio: str | None = None
    avatar_url: str | None = None
    is_verified: bool | None = None
    follower_count: int | None = None


# --- Content ---

class ContentCreate(BaseModel):
    creator_id: UUID
    title: str
    description: str | None = None
    content_type: str = "video"  # movie | short | video | live
    thumbnail_url: str | None = None
    banner_url: str | None = None
    status: str = "published"  # draft | published | archived
    visibility: str = "public"  # public | private | unlisted
    duration_seconds: int = 0
    view_count: int = 0
    like_count: int = 0
    is_featured: bool = False


class ContentUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    content_type: str | None = None
    thumbnail_url: str | None = None
    banner_url: str | None = None
    status: str | None = None
    visibility: str | None = None
    duration_seconds: int | None = None
    view_count: int | None = None
    like_count: int | None = None
    is_featured: bool | None = None


# --- ContentCategory ---

class ContentCategoryCreate(BaseModel):
    content_id: UUID
    category_id: UUID


# --- UserFollow ---

class UserFollowCreate(BaseModel):
    follower_id: UUID
    following_id: UUID


class UserFollowUpdate(BaseModel):
    follower_id: UUID | None = None
    following_id: UUID | None = None


# --- PlaybackHistory ---

class PlaybackHistoryCreate(BaseModel):
    user_id: UUID
    content_id: UUID
    progress_seconds: int = 0
    completed: bool = False


class PlaybackHistoryUpdate(BaseModel):
    progress_seconds: int | None = None
    completed: bool | None = None