import pytest


def test_create_category(authenticated_client):
    """Test creating a category."""
    response = authenticated_client.post(
        "/explore/categories",
        json={
            "name": "Animation",
            "slug": "animation",
            "description": "Animated content",
            "icon_url": "https://placehold.co/100x100?text=Animation",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["name"] == "Animation"
    assert data["data"]["slug"] == "animation"


def test_update_category(authenticated_client, db):
    """Test updating a category."""
    from app.models.category import Category
    cat = Category(name="Music", slug="music")
    db.add(cat)
    db.commit()

    response = authenticated_client.put(
        f"/explore/categories/{cat.id}",
        json={"name": "Music Videos", "description": "Updated description"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["name"] == "Music Videos"


def test_create_creator_profile(authenticated_client):
    """Test creating a creator profile."""
    # First create a user
    resp = authenticated_client.post(
        "/auth/register",
        json={
            "email": "test_creator_crud@example.com",
            "username": "testcreatorcrud",
            "password": "test123",
        },
    )
    assert resp.status_code == 200
    user_id = resp.json()["data"]["id"]

    response = authenticated_client.post(
        "/explore/creators",
        json={
            "user_id": user_id,
            "display_name": "Test Creator",
            "bio": "Test bio",
            "avatar_url": "https://placehold.co/200x200?text=TC",
            "is_verified": True,
            "follower_count": 100,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["display_name"] == "Test Creator"


def test_update_creator_profile(authenticated_client, db):
    """Test updating a creator profile."""
    from app.models.user import User
    from app.models.creator_profile import CreatorProfile

    user = db.query(User).filter(User.username == "testuser").first()
    profile = CreatorProfile(
        user_id=user.id,
        display_name="Old Name",
        follower_count=100,
    )
    db.add(profile)
    db.commit()

    response = authenticated_client.put(
        f"/explore/creators/{profile.id}",
        json={"display_name": "New Name", "follower_count": 250},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["display_name"] == "New Name"


def test_create_content(authenticated_client, db):
    """Test creating content."""
    # Create a creator profile for the test user
    from app.models.user import User
    from app.models.creator_profile import CreatorProfile

    user = db.query(User).filter(User.username == "testuser").first()
    profile = CreatorProfile(
        user_id=user.id,
        display_name="Test Creator",
        follower_count=0,
    )
    db.add(profile)
    db.commit()

    response = authenticated_client.post(
        "/explore/content",
        json={
            "creator_id": str(profile.id),
            "title": "My New Video",
            "description": "A test video",
            "content_type": "video",
            "thumbnail_url": "https://placehold.co/400x700?text=New",
            "status": "published",
            "visibility": "public",
            "duration_seconds": 120,
            "view_count": 0,
            "like_count": 0,
            "is_featured": False,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["title"] == "My New Video"
    assert data["data"]["creator_id"] == str(profile.id)


def test_update_content(authenticated_client, db):
    """Test updating content."""
    from app.models.user import User
    from app.models.creator_profile import CreatorProfile
    from app.models.content import Content

    user = db.query(User).filter(User.username == "testuser").first()
    profile = CreatorProfile(
        user_id=user.id,
        display_name="Test Creator",
        follower_count=0,
    )
    db.add(profile)
    db.commit()

    content = Content(
        creator_id=profile.id,
        title="Old Title",
        content_type="video",
        status="published",
        visibility="public",
        view_count=10,
        like_count=1,
        is_featured=False,
    )
    db.add(content)
    db.commit()

    response = authenticated_client.put(
        f"/explore/content/{content.id}",
        json={"title": "New Title", "view_count": 100, "like_count": 20},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["title"] == "New Title"
    assert data["data"]["view_count"] == 100


def test_create_content_category(authenticated_client, db):
    """Test creating a content-category association."""
    from app.models.user import User
    from app.models.creator_profile import CreatorProfile
    from app.models.content import Content
    from app.models.category import Category

    user = db.query(User).filter(User.username == "testuser").first()
    profile = CreatorProfile(
        user_id=user.id,
        display_name="Test Creator",
        follower_count=0,
    )
    db.add(profile)
    db.commit()

    content = Content(
        creator_id=profile.id,
        title="Categorized Content",
        content_type="video",
        status="published",
        visibility="public",
        is_featured=False,
    )
    cat = Category(name="Music", slug="music")
    db.add_all([content, cat])
    db.commit()

    response = authenticated_client.post(
        "/explore/content-categories",
        json={
            "content_id": str(content.id),
            "category_id": str(cat.id),
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["content_id"] == str(content.id)
    assert data["data"]["category_id"] == str(cat.id)


def test_create_user_follow(authenticated_client, db):
    """Test creating a follow relationship."""
    from app.models.user import User
    other = User(
        email="test_crud_follow@example.com",
        username="testcrudfollow",
        hashed_password="hashed",
    )
    db.add(other)
    db.commit()

    user = db.query(User).filter(User.username == "testuser").first()

    response = authenticated_client.post(
        "/explore/follows",
        json={
            "follower_id": str(user.id),
            "following_id": str(other.id),
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["follower_id"] == str(user.id)


def test_follow_self_rejected(authenticated_client):
    """Test that following yourself is rejected."""
    # Get current user
    user_id = None
    response = authenticated_client.get("/auth/me")
    if response.status_code == 200:
        user_id = response.json()["data"]["id"]

    if user_id:
        resp = authenticated_client.post(
            "/explore/follows",
            json={"follower_id": user_id, "following_id": user_id},
        )
        assert resp.status_code == 400
        assert "Cannot follow yourself" in resp.json()["message"]


def test_create_playback_history(authenticated_client, db):
    """Test creating playback history."""
    from app.models.user import User
    from app.models.creator_profile import CreatorProfile
    from app.models.content import Content

    user = db.query(User).filter(User.username == "testuser").first()
    profile = CreatorProfile(
        user_id=user.id,
        display_name="Test Creator",
        follower_count=0,
    )
    db.add(profile)
    db.commit()

    content = Content(
        creator_id=profile.id,
        title="Played Content",
        content_type="video",
        status="published",
        visibility="public",
        is_featured=False,
    )
    db.add(content)
    db.commit()

    response = authenticated_client.post(
        "/explore/playback-history",
        json={
            "user_id": str(user.id),
            "content_id": str(content.id),
            "progress_seconds": 45,
            "completed": False,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["progress_seconds"] == 45
    assert data["data"]["completed"] is False


def test_playback_history_upsert(authenticated_client, db):
    """Test that creating playback history again updates the existing record."""
    from app.models.user import User
    from app.models.creator_profile import CreatorProfile
    from app.models.content import Content
    from app.models.playback_history import PlaybackHistory

    user = db.query(User).filter(User.username == "testuser").first()
    profile = CreatorProfile(
        user_id=user.id,
        display_name="Test Creator",
        follower_count=0,
    )
    db.add(profile)
    db.commit()

    content = Content(
        creator_id=profile.id,
        title="Played Twice",
        content_type="video",
        status="published",
        visibility="public",
        is_featured=False,
    )
    db.add(content)
    db.commit()

    # Create first time
    resp1 = authenticated_client.post(
        "/explore/playback-history",
        json={
            "user_id": str(user.id),
            "content_id": str(content.id),
            "progress_seconds": 10,
            "completed": False,
        },
    )
    assert resp1.status_code == 200
    first_id = resp1.json()["data"]["id"]

    # Create second time — should update existing, not duplicate
    resp2 = authenticated_client.post(
        "/explore/playback-history",
        json={
            "user_id": str(user.id),
            "content_id": str(content.id),
            "progress_seconds": 90,
            "completed": True,
        },
    )
    assert resp2.status_code == 200
    assert resp2.json()["data"]["id"] == first_id
    assert resp2.json()["data"]["progress_seconds"] == 90
    assert resp2.json()["data"]["completed"] is True

    # Only one record should exist
    count = db.query(PlaybackHistory).filter(
        PlaybackHistory.user_id == user.id,
        PlaybackHistory.content_id == content.id,
    ).count()
    assert count == 1


def test_crud_requires_auth(client):
    """Test that CRUD endpoints require authentication."""
    response = client.post("/explore/categories", json={"name": "X", "slug": "x"})
    assert response.status_code == 401
    data = response.json()
    assert data["success"] is False
    assert "Not authenticated" in data["message"]