from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.content import Content
from app.models.category import Category
from app.models.content_category import ContentCategory
from app.models.creator_profile import CreatorProfile
from app.models.user_follow import UserFollow
from app.models.playback_history import PlaybackHistory
from app.models.user import User


# Section limits (configurable)
FEATURED_LIMIT = 5
RECENT_LIMIT = 10
FOLLOWING_LIMIT = 10
TRENDING_LIMIT = 10
LEARNING_LIMIT = 10
TRENDING_NOW_LIMIT = 10
TOP_ARTISTS_LIMIT = 10
RECENTLY_PLAYED_LIMIT = 10


def _serialize_content(content: Content) -> dict:
    """Convert a Content ORM object into the API response dict."""
    creator = content.creator
    user = creator.user if creator else None

    return {
        "id": content.id,
        "title": content.title,
        "description": content.description,
        "content_type": content.content_type,
        "thumbnail_url": content.thumbnail_url,
        "banner_url": content.banner_url,
        "creator": {
            "id": creator.id if creator else None,
            "username": user.username if user else None,
            "display_name": creator.display_name if creator else None,
            "avatar_url": creator.avatar_url if creator else None,
            "is_verified": creator.is_verified if creator else False,
        },
        "view_count": content.view_count,
        "like_count": content.like_count,
        "duration_seconds": content.duration_seconds,
        "created_at": content.created_at,
    }


def _serialize_artist(profile: CreatorProfile) -> dict:
    """Convert a CreatorProfile ORM object into the top-artist response dict."""
    user = profile.user
    return {
        "id": profile.id,
        "username": user.username if user else None,
        "display_name": profile.display_name,
        "avatar_url": profile.avatar_url,
        "is_verified": profile.is_verified,
        "follower_count": profile.follower_count,
    }


def get_featured_content(db: Session, limit: int = FEATURED_LIMIT) -> list[dict]:
    """Return featured content items."""
    items = (
        db.query(Content)
        .filter(
            Content.is_featured == True,  # noqa: E712
            Content.status == "published",
            Content.visibility == "public",
        )
        .order_by(Content.view_count.desc())
        .limit(limit)
        .all()
    )
    return [_serialize_content(c) for c in items]


def get_recent_content(db: Session, limit: int = RECENT_LIMIT) -> list[dict]:
    """Return most recently created content."""
    items = (
        db.query(Content)
        .filter(
            Content.status == "published",
            Content.visibility == "public",
        )
        .order_by(Content.created_at.desc())
        .limit(limit)
        .all()
    )
    return [_serialize_content(c) for c in items]


def get_following_content(
    db: Session, user_id, limit: int = FOLLOWING_LIMIT
) -> list[dict]:
    """Return content created by users the current user follows."""
    if user_id is None:
        return []

    # Find users followed by the current user
    followed_user_ids = (
        db.query(UserFollow.following_id)
        .filter(UserFollow.follower_id == user_id)
        .all()
    )
    followed_user_ids = [row[0] for row in followed_user_ids]

    if not followed_user_ids:
        return []

    # Find creator profiles for those users
    creator_ids = (
        db.query(CreatorProfile.id)
        .filter(CreatorProfile.user_id.in_(followed_user_ids))
        .all()
    )
    creator_ids = [row[0] for row in creator_ids]

    if not creator_ids:
        return []

    items = (
        db.query(Content)
        .filter(
            Content.creator_id.in_(creator_ids),
            Content.status == "published",
            Content.visibility == "public",
        )
        .order_by(Content.created_at.desc())
        .limit(limit)
        .all()
    )
    return [_serialize_content(c) for c in items]


def get_trending_content(db: Session, limit: int = TRENDING_LIMIT) -> list[dict]:
    """Return trending content ordered by view_count then created_at."""
    items = (
        db.query(Content)
        .filter(
            Content.status == "published",
            Content.visibility == "public",
        )
        .order_by(Content.view_count.desc(), Content.created_at.desc())
        .limit(limit)
        .all()
    )
    return [_serialize_content(c) for c in items]


def get_learning_content(db: Session, limit: int = LEARNING_LIMIT) -> list[dict]:
    """Return content in the 'learning' category."""
    items = (
        db.query(Content)
        .join(ContentCategory, ContentCategory.content_id == Content.id)
        .join(Category, Category.id == ContentCategory.category_id)
        .filter(
            Category.slug == "learning",
            Content.status == "published",
            Content.visibility == "public",
        )
        .order_by(Content.view_count.desc())
        .limit(limit)
        .all()
    )
    return [_serialize_content(c) for c in items]


def get_top_artists(db: Session, limit: int = TOP_ARTISTS_LIMIT) -> list[dict]:
    """Return top artists ranked by follower_count."""
    profiles = (
        db.query(CreatorProfile)
        .order_by(CreatorProfile.follower_count.desc())
        .limit(limit)
        .all()
    )
    return [_serialize_artist(p) for p in profiles]


def get_recently_played(
    db: Session, user_id, limit: int = RECENTLY_PLAYED_LIMIT
) -> list[dict]:
    """Return content the user recently played, ordered by last_played_at."""
    if user_id is None:
        return []

    history = (
        db.query(PlaybackHistory)
        .filter(PlaybackHistory.user_id == user_id)
        .order_by(PlaybackHistory.last_played_at.desc())
        .limit(limit)
        .all()
    )
    return [_serialize_content(h.content) for h in history if h.content]


def get_categories(db: Session) -> list[dict]:
    """Return all categories."""
    categories = db.query(Category).order_by(Category.name.asc()).all()
    return [
        {
            "id": c.id,
            "name": c.name,
            "slug": c.slug,
            "icon_url": c.icon_url,
        }
        for c in categories
    ]


def search_content(
    db: Session, query: str, limit: int = 20, offset: int = 0
) -> list[dict]:
    """Search content by title or description."""
    if not query:
        return []

    search_term = f"%{query}%"
    items = (
        db.query(Content)
        .filter(
            or_(Content.title.ilike(search_term), Content.description.ilike(search_term)),
            Content.status == "published",
            Content.visibility == "public",
        )
        .order_by(Content.view_count.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return [_serialize_content(c) for c in items]


def get_explore_data(db: Session, current_user: User | None = None) -> dict:
    """Assemble the complete Explore response."""
    user_id = current_user.id if current_user else None

    return {
        "featured": get_featured_content(db),
        "categories": get_categories(db),
        "content": {
            "recent": get_recent_content(db),
            "following": get_following_content(db, user_id),
            "trendy": get_trending_content(db),
            "learning": get_learning_content(db),
        },
        "trending_now": get_trending_content(db, TRENDING_NOW_LIMIT),
        "top_artists": get_top_artists(db),
        "recently_played": get_recently_played(db, user_id),
    }