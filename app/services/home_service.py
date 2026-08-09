from sqlalchemy.orm import Session

from app.models.home_banner import HomeBanner
from app.models.movie import Movie
from app.models.content_creator import ContentCreator
from app.models.short import Short
from app.models.live_video import LiveVideo

# Section limits
BANNER_LIMIT = 5
POPULAR_MOVIES_LIMIT = 10
CREATORS_LIMIT = 10
SHORTS_LIMIT = 10
LIVE_VIDEOS_LIMIT = 10


def get_home_banners(db: Session, limit: int = BANNER_LIMIT) -> list[HomeBanner]:
    return (
        db.query(HomeBanner)
        .filter(HomeBanner.is_active == True)  # noqa: E712
        .order_by(HomeBanner.sort_order.asc())
        .limit(limit)
        .all()
    )


def get_popular_movies(db: Session, limit: int = POPULAR_MOVIES_LIMIT) -> list[Movie]:
    return (
        db.query(Movie)
        .filter(Movie.is_popular == True)  # noqa: E712
        .order_by(Movie.sort_order.asc())
        .limit(limit)
        .all()
    )


def get_content_creators(db: Session, limit: int = CREATORS_LIMIT) -> list[ContentCreator]:
    return (
        db.query(ContentCreator)
        .order_by(ContentCreator.created_at.asc())
        .limit(limit)
        .all()
    )


def get_shorts(db: Session, limit: int = SHORTS_LIMIT) -> list[Short]:
    return (
        db.query(Short)
        .filter(Short.is_published == True)  # noqa: E712
        .order_by(Short.sort_order.asc())
        .limit(limit)
        .all()
    )


def get_live_videos(db: Session, limit: int = LIVE_VIDEOS_LIMIT) -> list[LiveVideo]:
    return (
        db.query(LiveVideo)
        .filter(LiveVideo.is_live == True)  # noqa: E712
        .order_by(LiveVideo.sort_order.asc())
        .limit(limit)
        .all()
    )


def get_home_data(db: Session):
    """Aggregate all Home screen data into a single dict."""
    return {
        "banners": get_home_banners(db),
        "popular_movies": get_popular_movies(db),
        "creators": get_content_creators(db),
        "shorts": get_shorts(db),
        "live_videos": get_live_videos(db),
    }