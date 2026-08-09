from app.models.user import User
from app.models.creator_profile import CreatorProfile
from app.models.category import Category
from app.models.content import Content
from app.models.content_category import ContentCategory
from app.models.user_follow import UserFollow
from app.models.playback_history import PlaybackHistory
from app.core.security import hash_password


def seed_explore_data(db):
    """Seed dummy data for the Explore screen. Idempotent — safe to run multiple times."""

    # --- Users (creators) ---
    user_defs = [
        {
            "email": "creator1@example.com",
            "username": "aadi",
            "avatar_url": "https://placehold.co/200x200?text=Aadi",
        },
        {
            "email": "creator2@example.com",
            "username": "robert",
            "avatar_url": "https://placehold.co/200x200?text=Robert",
        },
        {
            "email": "creator3@example.com",
            "username": "dianna",
            "avatar_url": "https://placehold.co/200x200?text=Dianna",
        },
        {
            "email": "creator4@example.com",
            "username": "mike",
            "avatar_url": "https://placehold.co/200x200?text=Mike",
        },
        {
            "email": "creator5@example.com",
            "username": "sara",
            "avatar_url": "https://placehold.co/200x200?text=Sara",
        },
    ]

    users = []
    for ud in user_defs:
        u = db.query(User).filter(User.email == ud["email"]).first()
        if not u:
            u = User(
                email=ud["email"],
                username=ud["username"],
                hashed_password=hash_password("password123"),
                avatar_url=ud["avatar_url"],
            )
            db.add(u)
        users.append(u)
    db.commit()

    # --- Creator Profiles ---
    profiles = []
    profile_defs = [
        {
            "user_id": users[0].id,
            "display_name": "Aadi",
            "bio": "Movie reviewer and reactor.",
            "avatar_url": "https://placehold.co/200x200?text=Aadi",
            "is_verified": True,
            "follower_count": 12500,
        },
        {
            "user_id": users[1].id,
            "display_name": "Robert",
            "bio": "Hollywood trailers and breakdowns.",
            "avatar_url": "https://placehold.co/200x200?text=Robert",
            "is_verified": True,
            "follower_count": 9800,
        },
        {
            "user_id": users[2].id,
            "display_name": "Dianna",
            "bio": "K-drama highlights and recaps.",
            "avatar_url": "https://placehold.co/200x200?text=Dianna",
            "is_verified": False,
            "follower_count": 7200,
        },
        {
            "user_id": users[3].id,
            "display_name": "Mike",
            "bio": "Gaming streams and walkthroughs.",
            "avatar_url": "https://placehold.co/200x200?text=Mike",
            "is_verified": True,
            "follower_count": 15400,
        },
        {
            "user_id": users[4].id,
            "display_name": "Sara",
            "bio": "Educational content and tutorials.",
            "avatar_url": "https://placehold.co/200x200?text=Sara",
            "is_verified": True,
            "follower_count": 21000,
        },
    ]

    for pd in profile_defs:
        p = db.query(CreatorProfile).filter(CreatorProfile.user_id == pd["user_id"]).first()
        if not p:
            p = CreatorProfile(**pd)
            db.add(p)
        profiles.append(p)
    db.commit()

    # --- Categories ---
    category_defs = [
        {
            "name": "Trend",
            "slug": "trend",
            "description": "What's hot right now",
            "icon_url": "https://placehold.co/100x100?text=Trend",
        },
        {
            "name": "Music",
            "slug": "music",
            "description": "Music videos and performances",
            "icon_url": "https://placehold.co/100x100?text=Music",
        },
        {
            "name": "Gaming",
            "slug": "gaming",
            "description": "Gameplay, streams, and walkthroughs",
            "icon_url": "https://placehold.co/100x100?text=Gaming",
        },
        {
            "name": "Learning",
            "slug": "learning",
            "description": "Educational and tutorial content",
            "icon_url": "https://placehold.co/100x100?text=Learning",
        },
    ]

    categories = []
    for cd in category_defs:
        c = db.query(Category).filter(Category.slug == cd["slug"]).first()
        if not c:
            c = Category(**cd)
            db.add(c)
        categories.append(c)
    db.commit()

    # --- Content ---
    content_defs = [
        {
            "creator_id": profiles[0].id,
            "title": "Oppenheimer Best Scene",
            "description": "The most intense scene from Oppenheimer.",
            "content_type": "short",
            "thumbnail_url": "https://placehold.co/400x700?text=Oppenheimer+Short",
            "banner_url": "https://placehold.co/1600x600?text=Oppenheimer",
            "status": "published",
            "visibility": "public",
            "duration_seconds": 120,
            "view_count": 12000,
            "like_count": 1500,
            "is_featured": True,
        },
        {
            "creator_id": profiles[1].id,
            "title": "The Witcher Monster Fight",
            "description": "Geralt takes down a griffin.",
            "content_type": "short",
            "thumbnail_url": "https://placehold.co/400x700?text=Witcher+Short",
            "banner_url": "https://placehold.co/1600x600?text=The+Witcher",
            "status": "published",
            "visibility": "public",
            "duration_seconds": 95,
            "view_count": 8500,
            "like_count": 900,
            "is_featured": True,
        },
        {
            "creator_id": profiles[2].id,
            "title": "Squid Game: Red Light Green Light",
            "description": "The iconic first game.",
            "content_type": "short",
            "thumbnail_url": "https://placehold.co/400x700?text=Squid+Game+Short",
            "banner_url": "https://placehold.co/1600x600?text=Squid+Game",
            "status": "published",
            "visibility": "public",
            "duration_seconds": 180,
            "view_count": 21000,
            "like_count": 3200,
            "is_featured": True,
        },
        {
            "creator_id": profiles[3].id,
            "title": "Top 10 Gaming Moments 2024",
            "description": "The best gaming moments of the year.",
            "content_type": "video",
            "thumbnail_url": "https://placehold.co/400x700?text=Gaming+Moments",
            "banner_url": "https://placehold.co/1600x600?text=Gaming",
            "status": "published",
            "visibility": "public",
            "duration_seconds": 600,
            "view_count": 32000,
            "like_count": 4100,
            "is_featured": True,
        },
        {
            "creator_id": profiles[4].id,
            "title": "Learn Python in 10 Minutes",
            "description": "A quick Python tutorial for beginners.",
            "content_type": "video",
            "thumbnail_url": "https://placehold.co/400x700?text=Python+Tutorial",
            "banner_url": "https://placehold.co/1600x600?text=Learning",
            "status": "published",
            "visibility": "public",
            "duration_seconds": 600,
            "view_count": 45000,
            "like_count": 5200,
            "is_featured": True,
        },
        {
            "creator_id": profiles[0].id,
            "title": "Movie Review: Dune Part 2",
            "description": "My full review of Dune Part 2.",
            "content_type": "video",
            "thumbnail_url": "https://placehold.co/400x700?text=Dune+Review",
            "banner_url": "https://placehold.co/1600x600?text=Dune",
            "status": "published",
            "visibility": "public",
            "duration_seconds": 900,
            "view_count": 15000,
            "like_count": 1800,
            "is_featured": False,
        },
        {
            "creator_id": profiles[1].id,
            "title": "Behind the Scenes: Action Stunts",
            "description": "How they film the big action sequences.",
            "content_type": "video",
            "thumbnail_url": "https://placehold.co/400x700?text=Action+Shorts",
            "banner_url": "https://placehold.co/1600x600?text=Action",
            "status": "published",
            "visibility": "public",
            "duration_seconds": 450,
            "view_count": 5400,
            "like_count": 600,
            "is_featured": False,
        },
        {
            "creator_id": profiles[2].id,
            "title": "K-Drama Highlights: Episode 5",
            "description": "The best moments from episode 5.",
            "content_type": "short",
            "thumbnail_url": "https://placehold.co/400x700?text=K-Drama+Highlights",
            "banner_url": "https://placehold.co/1600x600?text=K-Drama",
            "status": "published",
            "visibility": "public",
            "duration_seconds": 150,
            "view_count": 9800,
            "like_count": 1100,
            "is_featured": False,
        },
        {
            "creator_id": profiles[3].id,
            "title": "Minecraft Speedrun World Record",
            "description": "Watch me break the world record.",
            "content_type": "video",
            "thumbnail_url": "https://placehold.co/400x700?text=Minecraft+Speedrun",
            "banner_url": "https://placehold.co/1600x600?text=Minecraft",
            "status": "published",
            "visibility": "public",
            "duration_seconds": 1200,
            "view_count": 28000,
            "like_count": 3600,
            "is_featured": False,
        },
        {
            "creator_id": profiles[4].id,
            "title": "Machine Learning Basics",
            "description": "Understand ML concepts in simple terms.",
            "content_type": "video",
            "thumbnail_url": "https://placehold.co/400x700?text=ML+Basics",
            "banner_url": "https://placehold.co/1600x600?text=Machine+Learning",
            "status": "published",
            "visibility": "public",
            "duration_seconds": 750,
            "view_count": 19000,
            "like_count": 2400,
            "is_featured": False,
        },
        {
            "creator_id": profiles[0].id,
            "title": "Top 10 Movie Trailers This Week",
            "description": "The most anticipated trailers.",
            "content_type": "video",
            "thumbnail_url": "https://placehold.co/400x700?text=Trailers",
            "banner_url": "https://placehold.co/1600x600?text=Trailers",
            "status": "published",
            "visibility": "public",
            "duration_seconds": 300,
            "view_count": 11000,
            "like_count": 1300,
            "is_featured": False,
        },
        {
            "creator_id": profiles[1].id,
            "title": "Live: Movie Premiere Reaction",
            "description": "Reacting live to the premiere.",
            "content_type": "live",
            "thumbnail_url": "https://placehold.co/400x700?text=Live+Premiere",
            "banner_url": "https://placehold.co/1600x600?text=Live",
            "status": "published",
            "visibility": "public",
            "duration_seconds": 3600,
            "view_count": 7500,
            "like_count": 800,
            "is_featured": False,
        },
        {
            "creator_id": profiles[2].id,
            "title": "K-Pop Music Video Reaction",
            "description": "Reacting to the latest K-Pop MV.",
            "content_type": "short",
            "thumbnail_url": "https://placehold.co/400x700?text=K-Pop+Reaction",
            "banner_url": "https://placehold.co/1600x600?text=K-Pop",
            "status": "published",
            "visibility": "public",
            "duration_seconds": 90,
            "view_count": 17000,
            "like_count": 2100,
            "is_featured": False,
        },
        {
            "creator_id": profiles[3].id,
            "title": "Fortnite Battle Royale Highlights",
            "description": "My best Fortnite moments.",
            "content_type": "short",
            "thumbnail_url": "https://placehold.co/400x700?text=Fortnite",
            "banner_url": "https://placehold.co/1600x600?text=Fortnite",
            "status": "published",
            "visibility": "public",
            "duration_seconds": 60,
            "view_count": 13000,
            "like_count": 1500,
            "is_featured": False,
        },
        {
            "creator_id": profiles[4].id,
            "title": "Web Development Crash Course",
            "description": "Learn HTML, CSS, and JS fast.",
            "content_type": "video",
            "thumbnail_url": "https://placehold.co/400x700?text=Web+Dev",
            "banner_url": "https://placehold.co/1600x600?text=Web+Development",
            "status": "published",
            "visibility": "public",
            "duration_seconds": 1800,
            "view_count": 25000,
            "like_count": 3000,
            "is_featured": False,
        },
        {
            "creator_id": profiles[0].id,
            "title": "Live: Movie Awards Reaction",
            "description": "Reacting live to the awards show.",
            "content_type": "live",
            "thumbnail_url": "https://placehold.co/400x700?text=Live+Awards",
            "banner_url": "https://placehold.co/1600x600?text=Awards",
            "status": "published",
            "visibility": "public",
            "duration_seconds": 5400,
            "view_count": 6200,
            "like_count": 700,
            "is_featured": False,
        },
    ]

    contents = []
    for cd in content_defs:
        c = db.query(Content).filter(
            Content.title == cd["title"],
            Content.creator_id == cd["creator_id"],
        ).first()
        if not c:
            c = Content(**cd)
            db.add(c)
        contents.append(c)
    db.commit()

    # --- Content-Category relationships ---
    # Trend: 0, 2, 3, 4, 5, 8, 9, 10, 14
    # Music: 12
    # Gaming: 3, 8, 13
    # Learning: 4, 9, 14
    cc_pairs = [
        (0, 0), (2, 0), (3, 0), (3, 2), (4, 0), (4, 3),
        (5, 0), (8, 0), (8, 2), (9, 0), (9, 3), (10, 0),
        (12, 1), (13, 2), (14, 0), (14, 3),
    ]
    for ci, cat_i in cc_pairs:
        exists = db.query(ContentCategory).filter(
            ContentCategory.content_id == contents[ci].id,
            ContentCategory.category_id == categories[cat_i].id,
        ).first()
        if not exists:
            db.add(ContentCategory(
                content_id=contents[ci].id,
                category_id=categories[cat_i].id,
            ))
    db.commit()

    # --- Follows (test user follows creators) ---
    test_user = db.query(User).filter(User.email == "test_user@example.com").first()

    follows = []
    if test_user:
        follow_pairs = [
            (test_user.id, users[0].id),
            (test_user.id, users[2].id),
            (test_user.id, users[4].id),
        ]
        for fid, tid in follow_pairs:
            exists = db.query(UserFollow).filter(
                UserFollow.follower_id == fid,
                UserFollow.following_id == tid,
            ).first()
            if not exists:
                f = UserFollow(follower_id=fid, following_id=tid)
                db.add(f)
                follows.append(f)
    else:
        follow_pairs = [
            (users[0].id, users[1].id),
            (users[0].id, users[4].id),
            (users[1].id, users[3].id),
            (users[2].id, users[0].id),
            (users[3].id, users[4].id),
            (users[4].id, users[1].id),
        ]
        for fid, tid in follow_pairs:
            exists = db.query(UserFollow).filter(
                UserFollow.follower_id == fid,
                UserFollow.following_id == tid,
            ).first()
            if not exists:
                f = UserFollow(follower_id=fid, following_id=tid)
                db.add(f)
                follows.append(f)
    db.commit()

    # --- Playback history (test user) ---
    playback = []
    if test_user:
        playback_defs = [
            (test_user.id, contents[0].id, 60, False),
            (test_user.id, contents[4].id, 600, True),
            (test_user.id, contents[8].id, 300, False),
        ]
        for uid, cid, progress, completed in playback_defs:
            exists = db.query(PlaybackHistory).filter(
                PlaybackHistory.user_id == uid,
                PlaybackHistory.content_id == cid,
            ).first()
            if not exists:
                ph = PlaybackHistory(
                    user_id=uid,
                    content_id=cid,
                    progress_seconds=progress,
                    completed=completed,
                )
                db.add(ph)
                playback.append(ph)
    db.commit()

    return {
        "users": users,
        "profiles": profiles,
        "categories": categories,
        "contents": contents,
        "follows": follows,
        "playback": playback,
    }