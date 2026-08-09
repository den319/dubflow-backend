from app.models.home_banner import HomeBanner
from app.models.movie import Movie
from app.models.content_creator import ContentCreator
from app.models.short import Short
from app.models.live_video import LiveVideo


def seed_home_data(db):
    """Seed dummy data for the Home screen."""

    # --- Content Creators ---
    creators = [
        ContentCreator(
            name="Aadi",
            username="aadi",
            avatar_url="https://placehold.co/200x200?text=Aadi",
            bio="Movie reviewer and reactor.",
            is_verified=True,
        ),
        ContentCreator(
            name="Robert",
            username="robert",
            avatar_url="https://placehold.co/200x200?text=Robert",
            bio="Hollywood trailers and breakdowns.",
            is_verified=True,
        ),
        ContentCreator(
            name="Dianna",
            username="dianna",
            avatar_url="https://placehold.co/200x200?text=Dianna",
            bio="K-drama highlights and recaps.",
            is_verified=False,
        ),
    ]
    db.add_all(creators)
    db.commit()

    # --- Banners ---
    banners = [
        HomeBanner(
            title="Trending Now",
            subtitle="Watch what everyone is talking about",
            image_url="https://placehold.co/1600x600?text=Trending+Now",
            content_type="movie",
            content_id=None,
            is_active=True,
            sort_order=1,
        ),
        HomeBanner(
            title="New Releases",
            subtitle="Fresh content added every week",
            image_url="https://placehold.co/1600x600?text=New+Releases",
            content_type=None,
            content_id=None,
            is_active=True,
            sort_order=2,
        ),
        HomeBanner(
            title="Watch in Your Language",
            subtitle="Dubbed and subtitled in your language",
            image_url="https://placehold.co/1600x600?text=Watch+in+Your+Language",
            content_type=None,
            content_id=None,
            is_active=True,
            sort_order=3,
        ),
    ]
    db.add_all(banners)

    # --- Movies ---
    movies = [
        Movie(
            title="Oppenheimer",
            description="The story of J. Robert Oppenheimer and the atomic bomb.",
            poster_url="https://placehold.co/400x600?text=Oppenheimer",
            banner_url="https://placehold.co/1600x600?text=Oppenheimer",
            source_language="en",
            content_type="movie",
            is_popular=True,
            is_featured=True,
            rating=8.5,
            release_year=2023,
            sort_order=1,
        ),
        Movie(
            title="The Witcher",
            description="A monster hunter travels across the continent.",
            poster_url="https://placehold.co/400x600?text=The+Witcher",
            banner_url="https://placehold.co/1600x600?text=The+Witcher",
            source_language="en",
            content_type="series",
            is_popular=True,
            is_featured=True,
            rating=8.1,
            release_year=2019,
            sort_order=2,
        ),
        Movie(
            title="Squid Game",
            description="Hundreds of cash-strapped players accept a strange invitation.",
            poster_url="https://placehold.co/400x600?text=Squid+Game",
            banner_url="https://placehold.co/1600x600?text=Squid+Game",
            source_language="ko",
            content_type="series",
            is_popular=True,
            is_featured=True,
            rating=8.0,
            release_year=2021,
            sort_order=3,
        ),
    ]
    db.add_all(movies)
    db.commit()

    # --- Shorts ---
    shorts = [
        Short(
            title="Oppenheimer Best Scene",
            description="The most intense scene from Oppenheimer.",
            thumbnail_url="https://placehold.co/400x700?text=Oppenheimer+Short",
            creator_id=creators[0].id,
            language="en",
            views_count=12000,
            is_published=True,
            sort_order=1,
        ),
        Short(
            title="The Witcher Monster Fight",
            description="Geralt takes down a griffin.",
            thumbnail_url="https://placehold.co/400x700?text=Witcher+Short",
            creator_id=creators[1].id,
            language="en",
            views_count=8500,
            is_published=True,
            sort_order=2,
        ),
        Short(
            title="Squid Game: Red Light Green Light",
            description="The iconic first game.",
            thumbnail_url="https://placehold.co/400x700?text=Squid+Game+Short",
            creator_id=creators[2].id,
            language="ko",
            views_count=21000,
            is_published=True,
            sort_order=3,
        ),
        Short(
            title="Behind the Scenes: Action Stunts",
            description="How they film the big action sequences.",
            thumbnail_url="https://placehold.co/400x700?text=Action+Shorts",
            creator_id=creators[1].id,
            language="en",
            views_count=5400,
            is_published=True,
            sort_order=4,
        ),
    ]
    db.add_all(shorts)

    # --- Live Videos ---
    live_videos = [
        LiveVideo(
            title="Behind the Scenes of Action!",
            description="Live set tour of the new action movie.",
            thumbnail_url="https://placehold.co/1200x675?text=Live+Action",
            creator_id=creators[1].id,
            language="en",
            viewer_count=4100,
            is_live=True,
            sort_order=1,
        ),
        LiveVideo(
            title="Korean Drama Highlights",
            description="Dianna reacts to the latest K-drama episodes.",
            thumbnail_url="https://placehold.co/1200x675?text=Live+K-Drama",
            creator_id=creators[2].id,
            language="ko",
            viewer_count=3200,
            is_live=True,
            sort_order=2,
        ),
    ]
    db.add_all(live_videos)
    db.commit()

    return {
        "creators": creators,
        "banners": banners,
        "movies": movies,
        "shorts": shorts,
        "live_videos": live_videos,
    }