from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.home_banner import HomeBanner
from app.models.movie import Movie
from app.models.content_creator import ContentCreator
from app.models.short import Short
from app.models.live_video import LiveVideo
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


# --- HomeBanner ---

def create_home_banner(db: Session, data: HomeBannerCreate) -> HomeBanner:
    banner = HomeBanner(**data.model_dump())
    db.add(banner)
    db.commit()
    db.refresh(banner)
    return banner


def update_home_banner(db: Session, banner_id: UUID, data: HomeBannerUpdate) -> HomeBanner:
    banner = db.query(HomeBanner).filter(HomeBanner.id == banner_id).first()
    if not banner:
        raise HTTPException(status_code=404, detail="Banner not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(banner, field, value)
    db.commit()
    db.refresh(banner)
    return banner


# --- Movie ---

def create_movie(db: Session, data: MovieCreate) -> Movie:
    movie = Movie(**data.model_dump())
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie


def update_movie(db: Session, movie_id: UUID, data: MovieUpdate) -> Movie:
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(movie, field, value)
    db.commit()
    db.refresh(movie)
    return movie


# --- ContentCreator ---

def create_content_creator(db: Session, data: ContentCreatorCreate) -> ContentCreator:
    creator = ContentCreator(**data.model_dump())
    db.add(creator)
    db.commit()
    db.refresh(creator)
    return creator


def update_content_creator(db: Session, creator_id: UUID, data: ContentCreatorUpdate) -> ContentCreator:
    creator = db.query(ContentCreator).filter(ContentCreator.id == creator_id).first()
    if not creator:
        raise HTTPException(status_code=404, detail="Creator not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(creator, field, value)
    db.commit()
    db.refresh(creator)
    return creator


# --- Short ---

def create_short(db: Session, data: ShortCreate) -> Short:
    short = Short(**data.model_dump())
    db.add(short)
    db.commit()
    db.refresh(short)
    return short


def update_short(db: Session, short_id: UUID, data: ShortUpdate) -> Short:
    short = db.query(Short).filter(Short.id == short_id).first()
    if not short:
        raise HTTPException(status_code=404, detail="Short not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(short, field, value)
    db.commit()
    db.refresh(short)
    return short


# --- LiveVideo ---

def create_live_video(db: Session, data: LiveVideoCreate) -> LiveVideo:
    live_video = LiveVideo(**data.model_dump())
    db.add(live_video)
    db.commit()
    db.refresh(live_video)
    return live_video


def update_live_video(db: Session, live_video_id: UUID, data: LiveVideoUpdate) -> LiveVideo:
    live_video = db.query(LiveVideo).filter(LiveVideo.id == live_video_id).first()
    if not live_video:
        raise HTTPException(status_code=404, detail="Live video not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(live_video, field, value)
    db.commit()
    db.refresh(live_video)
    return live_video