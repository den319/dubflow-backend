import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db, engine, SessionLocal
from app.core.config import settings
from app.core.ratelimit import limiter

# Use the same PostgreSQL database as development (for testing in dev phase)
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Reuse existing engine from database.py
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Use the existing development database for testing."""
    # Reset rate limiter between tests
    limiter.reset()
    # Create all tables (they should already exist from startup)
    Base.metadata.create_all(bind=engine)
    
    # Create a new session
    db = TestingSessionLocal()

    # Clean up test data before test starts (avoids duplicate issues)
    from app.models.user import User
    from app.models.project import Project
    from app.models.subtitle_entry import SubtitleEntry
    from app.models.subtitle_file import SubtitleFile
    from app.models.subscription import Subscription
    from app.models.home_banner import HomeBanner
    from app.models.movie import Movie
    from app.models.content_creator import ContentCreator
    from app.models.short import Short
    from app.models.live_video import LiveVideo
    from app.models.playback_history import PlaybackHistory
    from app.models.content_category import ContentCategory
    from app.models.content import Content
    from app.models.category import Category
    from app.models.creator_profile import CreatorProfile
    from app.models.user_follow import UserFollow

    # Delete test data (users with test_ prefix email)
    # Order matters due to foreign key constraints
    try:
        # Delete playback history for test users
        db.query(PlaybackHistory).filter(
            PlaybackHistory.user_id.in_(
                db.query(User.id).filter(User.email.like("test_%"))
            )
        ).delete(synchronize_session=False)

        # Delete follows for test users
        db.query(UserFollow).filter(
            UserFollow.follower_id.in_(
                db.query(User.id).filter(User.email.like("test_%"))
            )
        ).delete(synchronize_session=False)
        db.query(UserFollow).filter(
            UserFollow.following_id.in_(
                db.query(User.id).filter(User.email.like("test_%"))
            )
        ).delete(synchronize_session=False)

        # Delete content-category relationships
        db.query(ContentCategory).delete(synchronize_session=False)

        # Delete content
        db.query(Content).delete(synchronize_session=False)

        # Delete categories
        db.query(Category).delete(synchronize_session=False)

        # Delete creator profiles
        db.query(CreatorProfile).delete(synchronize_session=False)

        # Delete live videos and shorts (depend on content_creators)
        db.query(LiveVideo).delete(synchronize_session=False)
        db.query(Short).delete(synchronize_session=False)
        # Delete content creators
        db.query(ContentCreator).delete(synchronize_session=False)
        db.query(Movie).delete(synchronize_session=False)
        db.query(HomeBanner).delete(synchronize_session=False)

        # Delete subscriptions for test users
        db.query(Subscription).filter(
            Subscription.user_id.in_(
                db.query(User.id).filter(User.email.like("test_%"))
            )
        ).delete(synchronize_session=False)
        
        # Delete subtitle entries for test projects
        db.query(SubtitleEntry).filter(
            SubtitleEntry.subtitle_file_id.in_(
                db.query(SubtitleFile.id).filter(SubtitleFile.project_id.in_(
                    db.query(Project.id).filter(Project.user_id.in_(
                        db.query(User.id).filter(User.email.like("test_%"))
                    ))
                ))
            )
        ).delete(synchronize_session=False)
        
        # Delete subtitle files for test projects
        db.query(SubtitleFile).filter(
            SubtitleFile.project_id.in_(
                db.query(Project.id).filter(Project.user_id.in_(
                    db.query(User.id).filter(User.email.like("test_%"))
                ))
            )
        ).delete(synchronize_session=False)
        
        # Delete projects for test users
        db.query(Project).filter(
            Project.user_id.in_(
                db.query(User.id).filter(User.email.like("test_%"))
            )
        ).delete(synchronize_session=False)
        
        # Delete test users
        db.query(User).filter(User.email.like("test_%")).delete(synchronize_session=False)
        
        db.commit()
    except Exception as e:
        # Rollback on cleanup error
        db.rollback()
        print(f"Cleanup error: {e}")
    
    try:
        yield db
    finally:
        # Clean up test data after each test (before closing session)
        from app.models.user import User
        from app.models.project import Project
        from app.models.subtitle_entry import SubtitleEntry
        from app.models.subtitle_file import SubtitleFile
        from app.models.subscription import Subscription
        from app.models.home_banner import HomeBanner
        from app.models.movie import Movie
        from app.models.content_creator import ContentCreator
        from app.models.short import Short
        from app.models.live_video import LiveVideo
        from app.models.playback_history import PlaybackHistory
        from app.models.content_category import ContentCategory
        from app.models.content import Content
        from app.models.category import Category
        from app.models.creator_profile import CreatorProfile
        from app.models.user_follow import UserFollow

        try:
            # Delete playback history for test users
            db.query(PlaybackHistory).filter(
                PlaybackHistory.user_id.in_(
                    db.query(User.id).filter(User.email.like("test_%"))
                )
            ).delete(synchronize_session=False)

            # Delete follows for test users
            db.query(UserFollow).filter(
                UserFollow.follower_id.in_(
                    db.query(User.id).filter(User.email.like("test_%"))
                )
            ).delete(synchronize_session=False)
            db.query(UserFollow).filter(
                UserFollow.following_id.in_(
                    db.query(User.id).filter(User.email.like("test_%"))
                )
            ).delete(synchronize_session=False)

            # Delete content-category relationships
            db.query(ContentCategory).delete(synchronize_session=False)

            # Delete content
            db.query(Content).delete(synchronize_session=False)

            # Delete categories
            db.query(Category).delete(synchronize_session=False)

            # Delete creator profiles
            db.query(CreatorProfile).delete(synchronize_session=False)

            # Delete live videos and shorts (depend on content_creators)
            db.query(LiveVideo).delete(synchronize_session=False)
            db.query(Short).delete(synchronize_session=False)
            # Delete content creators
            db.query(ContentCreator).delete(synchronize_session=False)
            db.query(Movie).delete(synchronize_session=False)
            db.query(HomeBanner).delete(synchronize_session=False)

            # Delete subscriptions for test users
            db.query(Subscription).filter(
                Subscription.user_id.in_(
                    db.query(User.id).filter(User.email.like("test_%"))
                )
            ).delete(synchronize_session=False)
            
            # Delete subtitle entries for test projects
            db.query(SubtitleEntry).filter(
                SubtitleEntry.subtitle_file_id.in_(
                    db.query(SubtitleFile.id).filter(SubtitleFile.project_id.in_(
                        db.query(Project.id).filter(Project.user_id.in_(
                            db.query(User.id).filter(User.email.like("test_%"))
                        ))
                    ))
                )
            ).delete(synchronize_session=False)
            
            # Delete subtitle files for test projects
            db.query(SubtitleFile).filter(
                SubtitleFile.project_id.in_(
                    db.query(Project.id).filter(Project.user_id.in_(
                        db.query(User.id).filter(User.email.like("test_%"))
                    ))
                )
            ).delete(synchronize_session=False)
            
            # Delete projects for test users
            db.query(Project).filter(
                Project.user_id.in_(
                    db.query(User.id).filter(User.email.like("test_%"))
                )
            ).delete(synchronize_session=False)
            
            # Delete test users
            db.query(User).filter(User.email.like("test_%")).delete(synchronize_session=False)
            
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Cleanup error: {e}")

        db.close()


@pytest.fixture(scope="function")
def client(db):
    """Create a test client with database dependency overridden."""
    def override_get_db():
        try:
            yield db
        finally:
            pass  # Don't close here, fixture handles it
    
    # Override the database dependency
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up overrides after test
    app.dependency_overrides.clear()


@pytest.fixture
def authenticated_client(client):
    """Create a client that is already logged in."""
    # Register a test user
    resp = client.post(
        "/auth/register",
        json={
            "email": "test_user@example.com",
            "username": "testuser",
            "password": "test123",
        },
    )
    assert resp.status_code == 200, f"Register failed: {resp.text}"
    # Login to get cookie (LoginRequest expects JSON body)
    resp = client.post(
        "/auth/login",
        json={"email": "test_user@example.com", "password": "test123"},
    )
    assert resp.status_code == 200, f"Login failed: {resp.text}"
    yield client