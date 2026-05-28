import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db, engine, SessionLocal
from app.core.config import settings

# Use the same PostgreSQL database as development (for testing in dev phase)
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Reuse existing engine from database.py
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Use the existing development database for testing."""
    # Create all tables (they should already exist from startup)
    Base.metadata.create_all(bind=engine)
    
    # Create a new session
    db = TestingSessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        # Clean up test data after each test
        from app.models.user import User
        from app.models.project import Project
        from app.models.subtitle import Subtitle
        from app.models.subscription import Subscription
        
        # Delete test data (users with test_ prefix email)
        # Order matters due to foreign key constraints
        try:
            # Delete subscriptions for test users
            db.query(Subscription).filter(
                Subscription.user_id.in_(
                    db.query(User.id).filter(User.email.like("test_%"))
                )
            ).delete(synchronize_session=False)
            
            # Delete subtitles for test projects
            db.query(Subtitle).filter(
                Subtitle.project_id.in_(
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
    client.post(
        "/auth/register",
        json={
            "email": "test_user@example.com",
            "username": "testuser",
            "password": "test123",
        },
    )
    # Login to get cookie
    client.post(
        "/auth/login",
        data={"email": "test_user@example.com", "password": "test123"},
    )
    yield client