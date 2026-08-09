from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.ratelimit import limiter
from app.core.response import success_response
from app.models.user import User
from app.services.auth_service import get_current_user
from app.services.home_service import get_home_data
from app.schemas.home import (
    HomeBannerResponse,
    MovieResponse,
    CreatorResponse,
    ShortResponse,
    ShortCreatorResponse,
    LiveVideoResponse,
    LiveVideoCreatorResponse,
)

router = APIRouter(tags=["Home"])


@router.get("/home")
@limiter.limit("30/minute")
def get_home(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data = get_home_data(db)

    payload = {
        "user": {
            "id": str(current_user.id),
            "username": current_user.username,
            "avatar_url": current_user.avatar_url,
        },
        "banners": [
            HomeBannerResponse.model_validate(b).model_dump() for b in data["banners"]
        ],
        "popular_movies": [
            MovieResponse.model_validate(m).model_dump() for m in data["popular_movies"]
        ],
        "creators": [
            CreatorResponse.model_validate(c).model_dump() for c in data["creators"]
        ],
        "shorts": [
            ShortResponse(
                id=s.id,
                title=s.title,
                thumbnail_url=s.thumbnail_url,
                creator=ShortCreatorResponse(
                    id=s.creator.id,
                    name=s.creator.name,
                    username=s.creator.username,
                    avatar_url=s.creator.avatar_url,
                ),
                language=s.language,
                views_count=s.views_count,
            ).model_dump()
            for s in data["shorts"]
        ],
        "live_videos": [
            LiveVideoResponse(
                id=v.id,
                title=v.title,
                thumbnail_url=v.thumbnail_url,
                creator=LiveVideoCreatorResponse(
                    id=v.creator.id,
                    name=v.creator.name,
                    username=v.creator.username,
                    avatar_url=v.creator.avatar_url,
                ),
                language=v.language,
                viewer_count=v.viewer_count,
                is_live=v.is_live,
            ).model_dump()
            for v in data["live_videos"]
        ],
    }

    return success_response(message="Home data fetched successfully", data=payload)