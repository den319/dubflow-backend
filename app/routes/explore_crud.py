from uuid import UUID
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.ratelimit import limiter
from app.core.response import success_response
from app.models.user import User
from app.services.auth_service import get_current_user
from app.services.explore_crud_service import (
    create_category,
    update_category,
    create_creator_profile,
    update_creator_profile,
    create_content,
    update_content,
    create_content_category,
    create_user_follow,
    update_user_follow,
    create_playback_history,
    update_playback_history,
)
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

router = APIRouter(prefix="/explore", tags=["Explore"])


# --- Category ---

@router.post("/categories")
@limiter.limit("30/minute")
def create_category_endpoint(
    request: Request,
    data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    category = create_category(db, data)
    return success_response(
        message="Category created successfully",
        data={
            "id": str(category.id),
            "name": category.name,
            "slug": category.slug,
            "description": category.description,
            "icon_url": category.icon_url,
        },
    )


@router.put("/categories/{category_id}")
@limiter.limit("30/minute")
def update_category_endpoint(
    request: Request,
    category_id: str,
    data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    category = update_category(db, UUID(category_id), data)
    return success_response(
        message="Category updated successfully",
        data={
            "id": str(category.id),
            "name": category.name,
            "slug": category.slug,
            "description": category.description,
            "icon_url": category.icon_url,
        },
    )


# --- CreatorProfile ---

@router.post("/creators")
@limiter.limit("30/minute")
def create_creator_profile_endpoint(
    request: Request,
    data: CreatorProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = create_creator_profile(db, data)
    return success_response(
        message="Creator profile created successfully",
        data={
            "id": str(profile.id),
            "user_id": str(profile.user_id),
            "display_name": profile.display_name,
            "bio": profile.bio,
            "avatar_url": profile.avatar_url,
            "is_verified": profile.is_verified,
            "follower_count": profile.follower_count,
        },
    )


@router.put("/creators/{profile_id}")
@limiter.limit("30/minute")
def update_creator_profile_endpoint(
    request: Request,
    profile_id: str,
    data: CreatorProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = update_creator_profile(db, UUID(profile_id), data)
    return success_response(
        message="Creator profile updated successfully",
        data={
            "id": str(profile.id),
            "user_id": str(profile.user_id),
            "display_name": profile.display_name,
            "bio": profile.bio,
            "avatar_url": profile.avatar_url,
            "is_verified": profile.is_verified,
            "follower_count": profile.follower_count,
        },
    )


# --- Content ---

@router.post("/content")
@limiter.limit("30/minute")
def create_content_endpoint(
    request: Request,
    data: ContentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    content = create_content(db, data)
    return success_response(
        message="Content created successfully",
        data={
            "id": str(content.id),
            "creator_id": str(content.creator_id),
            "title": content.title,
            "description": content.description,
            "content_type": content.content_type,
            "thumbnail_url": content.thumbnail_url,
            "banner_url": content.banner_url,
            "status": content.status,
            "visibility": content.visibility,
            "duration_seconds": content.duration_seconds,
            "view_count": content.view_count,
            "like_count": content.like_count,
            "is_featured": content.is_featured,
        },
    )


@router.put("/content/{content_id}")
@limiter.limit("30/minute")
def update_content_endpoint(
    request: Request,
    content_id: str,
    data: ContentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    content = update_content(db, UUID(content_id), data)
    return success_response(
        message="Content updated successfully",
        data={
            "id": str(content.id),
            "creator_id": str(content.creator_id),
            "title": content.title,
            "description": content.description,
            "content_type": content.content_type,
            "thumbnail_url": content.thumbnail_url,
            "banner_url": content.banner_url,
            "status": content.status,
            "visibility": content.visibility,
            "duration_seconds": content.duration_seconds,
            "view_count": content.view_count,
            "like_count": content.like_count,
            "is_featured": content.is_featured,
        },
    )


# --- ContentCategory ---

@router.post("/content-categories")
@limiter.limit("30/minute")
def create_content_category_endpoint(
    request: Request,
    data: ContentCategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cc = create_content_category(db, data)
    return success_response(
        message="Content category association created successfully",
        data={
            "content_id": str(cc.content_id),
            "category_id": str(cc.category_id),
        },
    )


# --- UserFollow ---

@router.post("/follows")
@limiter.limit("30/minute")
def create_user_follow_endpoint(
    request: Request,
    data: UserFollowCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    follow = create_user_follow(db, data)
    return success_response(
        message="Follow relationship created successfully",
        data={
            "id": str(follow.id),
            "follower_id": str(follow.follower_id),
            "following_id": str(follow.following_id),
        },
    )


@router.put("/follows/{follow_id}")
@limiter.limit("30/minute")
def update_user_follow_endpoint(
    request: Request,
    follow_id: str,
    data: UserFollowUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    follow = update_user_follow(db, UUID(follow_id), data)
    return success_response(
        message="Follow relationship updated successfully",
        data={
            "id": str(follow.id),
            "follower_id": str(follow.follower_id),
            "following_id": str(follow.following_id),
        },
    )


# --- PlaybackHistory ---

@router.post("/playback-history")
@limiter.limit("30/minute")
def create_playback_history_endpoint(
    request: Request,
    data: PlaybackHistoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    history = create_playback_history(db, data)
    return success_response(
        message="Playback history created successfully",
        data={
            "id": str(history.id),
            "user_id": str(history.user_id),
            "content_id": str(history.content_id),
            "progress_seconds": history.progress_seconds,
            "completed": history.completed,
        },
    )


@router.put("/playback-history/{history_id}")
@limiter.limit("30/minute")
def update_playback_history_endpoint(
    request: Request,
    history_id: str,
    data: PlaybackHistoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    history = update_playback_history(db, UUID(history_id), data)
    return success_response(
        message="Playback history updated successfully",
        data={
            "id": str(history.id),
            "user_id": str(history.user_id),
            "content_id": str(history.content_id),
            "progress_seconds": history.progress_seconds,
            "completed": history.completed,
        },
    )