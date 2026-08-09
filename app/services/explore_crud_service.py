from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.category import Category
from app.models.creator_profile import CreatorProfile
from app.models.content import Content
from app.models.content_category import ContentCategory
from app.models.user_follow import UserFollow
from app.models.playback_history import PlaybackHistory
from app.schemas.explore_crud import (
    CategoryCreate,
    CategoryUpdate,
    CreatorProfileCreate,
    CreatorProfileUpdate,
    ContentCreate,
    ContentUpdate,
    ContentCategoryCreate,
    UserFollowCreate,
    UserFollowUpdate,
    PlaybackHistoryCreate,
    PlaybackHistoryUpdate,
)


# --- Category ---

def create_category(db: Session, data: CategoryCreate) -> Category:
    category = Category(**data.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def update_category(db: Session, category_id: UUID, data: CategoryUpdate) -> Category:
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(category, field, value)
    db.commit()
    db.refresh(category)
    return category


# --- CreatorProfile ---

def create_creator_profile(db: Session, data: CreatorProfileCreate) -> CreatorProfile:
    profile = CreatorProfile(**data.model_dump())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def update_creator_profile(db: Session, profile_id: UUID, data: CreatorProfileUpdate) -> CreatorProfile:
    profile = db.query(CreatorProfile).filter(CreatorProfile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Creator profile not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(profile, field, value)
    db.commit()
    db.refresh(profile)
    return profile


# --- Content ---

def create_content(db: Session, data: ContentCreate) -> Content:
    content = Content(**data.model_dump())
    db.add(content)
    db.commit()
    db.refresh(content)
    return content


def update_content(db: Session, content_id: UUID, data: ContentUpdate) -> Content:
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(content, field, value)
    db.commit()
    db.refresh(content)
    return content


# --- ContentCategory ---

def create_content_category(db: Session, data: ContentCategoryCreate) -> ContentCategory:
    # Check for duplicate
    exists = db.query(ContentCategory).filter(
        ContentCategory.content_id == data.content_id,
        ContentCategory.category_id == data.category_id,
    ).first()
    if exists:
        raise HTTPException(status_code=400, detail="Content already in this category")

    cc = ContentCategory(**data.model_dump())
    db.add(cc)
    db.commit()
    db.refresh(cc)
    return cc


# --- UserFollow ---

def create_user_follow(db: Session, data: UserFollowCreate) -> UserFollow:
    if data.follower_id == data.following_id:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")

    exists = db.query(UserFollow).filter(
        UserFollow.follower_id == data.follower_id,
        UserFollow.following_id == data.following_id,
    ).first()
    if exists:
        raise HTTPException(status_code=400, detail="Already following this user")

    follow = UserFollow(**data.model_dump())
    db.add(follow)
    db.commit()
    db.refresh(follow)
    return follow


def update_user_follow(db: Session, follow_id: UUID, data: UserFollowUpdate) -> UserFollow:
    follow = db.query(UserFollow).filter(UserFollow.id == follow_id).first()
    if not follow:
        raise HTTPException(status_code=404, detail="Follow relationship not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(follow, field, value)
    db.commit()
    db.refresh(follow)
    return follow


# --- PlaybackHistory ---

def create_playback_history(db: Session, data: PlaybackHistoryCreate) -> PlaybackHistory:
    # Upsert: if a record exists for this user+content, update it instead of creating duplicate
    existing = db.query(PlaybackHistory).filter(
        PlaybackHistory.user_id == data.user_id,
        PlaybackHistory.content_id == data.content_id,
    ).first()
    if existing:
        existing.progress_seconds = data.progress_seconds
        existing.completed = data.completed
        db.commit()
        db.refresh(existing)
        return existing

    history = PlaybackHistory(**data.model_dump())
    db.add(history)
    db.commit()
    db.refresh(history)
    return history


def update_playback_history(db: Session, history_id: UUID, data: PlaybackHistoryUpdate) -> PlaybackHistory:
    history = db.query(PlaybackHistory).filter(PlaybackHistory.id == history_id).first()
    if not history:
        raise HTTPException(status_code=404, detail="Playback history not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(history, field, value)
    db.commit()
    db.refresh(history)
    return history