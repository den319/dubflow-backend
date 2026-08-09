from uuid import UUID
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.ratelimit import limiter
from app.core.response import success_response
from app.models.user import User
from app.services.auth_service import get_current_user
from app.services.content_service import (
    create_home_banner,
    update_home_banner,
    create_movie,
    update_movie,
    create_content_creator,
    update_content_creator,
    create_short,
    update_short,
    create_live_video,
    update_live_video,
)
from app.schemas.content import (
    HomeBannerCreate,
    HomeBannerUpdate,
    MovieCreate,
    MovieUpdate,
    ContentCreatorCreate,
    ContentCreatorUpdate,
    ShortCreate,
    ShortUpdate,
    LiveVideoCreate,
    LiveVideoUpdate,
)

router = APIRouter(prefix="/content", tags=["Content"])


# --- HomeBanner ---

@router.post("/banners")
@limiter.limit("30/minute")
def create_banner(
    request: Request,
    data: HomeBannerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    banner = create_home_banner(db, data)
    return success_response(
        message="Banner created successfully",
        data={
            "id": str(banner.id),
            "title": banner.title,
            "subtitle": banner.subtitle,
            "image_url": banner.image_url,
            "content_type": banner.content_type,
            "content_id": str(banner.content_id) if banner.content_id else None,
            "is_active": banner.is_active,
            "sort_order": banner.sort_order,
        },
    )


@router.put("/banners/{banner_id}")
@limiter.limit("30/minute")
def update_banner(
    request: Request,
    banner_id: str,
    data: HomeBannerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    banner = update_home_banner(db, UUID(banner_id), data)
    return success_response(
        message="Banner updated successfully",
        data={
            "id": str(banner.id),
            "title": banner.title,
            "subtitle": banner.subtitle,
            "image_url": banner.image_url,
            "content_type": banner.content_type,
            "content_id": str(banner.content_id) if banner.content_id else None,
            "is_active": banner.is_active,
            "sort_order": banner.sort_order,
        },
    )


# --- Movie ---

@router.post("/movies")
@limiter.limit("30/minute")
def create_movie_endpoint(
    request: Request,
    data: MovieCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    movie = create_movie(db, data)
    return success_response(
        message="Movie created successfully",
        data={
            "id": str(movie.id),
            "title": movie.title,
            "description": movie.description,
            "poster_url": movie.poster_url,
            "banner_url": movie.banner_url,
            "source_language": movie.source_language,
            "content_type": movie.content_type,
            "is_popular": movie.is_popular,
            "is_featured": movie.is_featured,
            "rating": movie.rating,
            "release_year": movie.release_year,
            "sort_order": movie.sort_order,
        },
    )


@router.put("/movies/{movie_id}")
@limiter.limit("30/minute")
def update_movie_endpoint(
    request: Request,
    movie_id: str,
    data: MovieUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    movie = update_movie(db, UUID(movie_id), data)
    return success_response(
        message="Movie updated successfully",
        data={
            "id": str(movie.id),
            "title": movie.title,
            "description": movie.description,
            "poster_url": movie.poster_url,
            "banner_url": movie.banner_url,
            "source_language": movie.source_language,
            "content_type": movie.content_type,
            "is_popular": movie.is_popular,
            "is_featured": movie.is_featured,
            "rating": movie.rating,
            "release_year": movie.release_year,
            "sort_order": movie.sort_order,
        },
    )


# --- ContentCreator ---

@router.post("/creators")
@limiter.limit("30/minute")
def create_creator_endpoint(
    request: Request,
    data: ContentCreatorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    creator = create_content_creator(db, data)
    return success_response(
        message="Creator created successfully",
        data={
            "id": str(creator.id),
            "name": creator.name,
            "username": creator.username,
            "avatar_url": creator.avatar_url,
            "bio": creator.bio,
            "is_verified": creator.is_verified,
        },
    )


@router.put("/creators/{creator_id}")
@limiter.limit("30/minute")
def update_creator_endpoint(
    request: Request,
    creator_id: str,
    data: ContentCreatorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    creator = update_content_creator(db, UUID(creator_id), data)
    return success_response(
        message="Creator updated successfully",
        data={
            "id": str(creator.id),
            "name": creator.name,
            "username": creator.username,
            "avatar_url": creator.avatar_url,
            "bio": creator.bio,
            "is_verified": creator.is_verified,
        },
    )


# --- Short ---

@router.post("/shorts")
@limiter.limit("30/minute")
def create_short_endpoint(
    request: Request,
    data: ShortCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    short = create_short(db, data)
    return success_response(
        message="Short created successfully",
        data={
            "id": str(short.id),
            "title": short.title,
            "description": short.description,
            "thumbnail_url": short.thumbnail_url,
            "creator_id": str(short.creator_id),
            "language": short.language,
            "views_count": short.views_count,
            "is_published": short.is_published,
            "sort_order": short.sort_order,
        },
    )


@router.put("/shorts/{short_id}")
@limiter.limit("30/minute")
def update_short_endpoint(
    request: Request,
    short_id: str,
    data: ShortUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    short = update_short(db, UUID(short_id), data)
    return success_response(
        message="Short updated successfully",
        data={
            "id": str(short.id),
            "title": short.title,
            "description": short.description,
            "thumbnail_url": short.thumbnail_url,
            "creator_id": str(short.creator_id),
            "language": short.language,
            "views_count": short.views_count,
            "is_published": short.is_published,
            "sort_order": short.sort_order,
        },
    )


# --- LiveVideo ---

@router.post("/live-videos")
@limiter.limit("30/minute")
def create_live_video_endpoint(
    request: Request,
    data: LiveVideoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    live_video = create_live_video(db, data)
    return success_response(
        message="Live video created successfully",
        data={
            "id": str(live_video.id),
            "title": live_video.title,
            "description": live_video.description,
            "thumbnail_url": live_video.thumbnail_url,
            "creator_id": str(live_video.creator_id),
            "language": live_video.language,
            "viewer_count": live_video.viewer_count,
            "is_live": live_video.is_live,
            "started_at": live_video.started_at.isoformat() if live_video.started_at else None,
            "sort_order": live_video.sort_order,
        },
    )


@router.put("/live-videos/{live_video_id}")
@limiter.limit("30/minute")
def update_live_video_endpoint(
    request: Request,
    live_video_id: str,
    data: LiveVideoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    live_video = update_live_video(db, UUID(live_video_id), data)
    return success_response(
        message="Live video updated successfully",
        data={
            "id": str(live_video.id),
            "title": live_video.title,
            "description": live_video.description,
            "thumbnail_url": live_video.thumbnail_url,
            "creator_id": str(live_video.creator_id),
            "language": live_video.language,
            "viewer_count": live_video.viewer_count,
            "is_live": live_video.is_live,
            "started_at": live_video.started_at.isoformat() if live_video.started_at else None,
            "sort_order": live_video.sort_order,
        },
    )