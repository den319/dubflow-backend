import pytest


def test_create_banner(authenticated_client):
    """Test creating a home banner."""
    response = authenticated_client.post(
        "/content/banners",
        json={
            "title": "Test Banner",
            "subtitle": "Test subtitle",
            "image_url": "https://placehold.co/1600x600?text=Test",
            "content_type": "movie",
            "is_active": True,
            "sort_order": 1,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Banner created successfully"
    assert data["data"]["title"] == "Test Banner"
    assert "id" in data["data"]


def test_update_banner(authenticated_client, db):
    """Test updating a home banner."""
    from app.models.home_banner import HomeBanner
    banner = HomeBanner(
        title="Old Title",
        image_url="https://placehold.co/1600x600?text=Old",
        is_active=True,
        sort_order=1,
    )
    db.add(banner)
    db.commit()
    db.refresh(banner)

    response = authenticated_client.put(
        f"/content/banners/{banner.id}",
        json={"title": "New Title"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Banner updated successfully"
    assert data["data"]["title"] == "New Title"


def test_create_movie(authenticated_client):
    """Test creating a movie."""
    response = authenticated_client.post(
        "/content/movies",
        json={
            "title": "Test Movie",
            "description": "A test movie",
            "poster_url": "https://placehold.co/400x600?text=Test",
            "source_language": "en",
            "content_type": "movie",
            "is_popular": True,
            "rating": 7.5,
            "release_year": 2024,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Movie created successfully"
    assert data["data"]["title"] == "Test Movie"
    assert data["data"]["rating"] == 7.5


def test_update_movie(authenticated_client, db):
    """Test updating a movie."""
    from app.models.movie import Movie
    movie = Movie(
        title="Old Movie",
        source_language="en",
        content_type="movie",
        is_popular=False,
        is_featured=False,
        sort_order=0,
    )
    db.add(movie)
    db.commit()
    db.refresh(movie)

    response = authenticated_client.put(
        f"/content/movies/{movie.id}",
        json={"title": "New Movie", "is_popular": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Movie updated successfully"
    assert data["data"]["title"] == "New Movie"
    assert data["data"]["is_popular"] is True


def test_create_creator(authenticated_client):
    """Test creating a content creator."""
    response = authenticated_client.post(
        "/content/creators",
        json={
            "name": "Test Creator",
            "username": "testcreator",
            "avatar_url": "https://placehold.co/200x200?text=Test",
            "bio": "A test creator",
            "is_verified": True,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Creator created successfully"
    assert data["data"]["name"] == "Test Creator"
    assert data["data"]["username"] == "testcreator"


def test_update_creator(authenticated_client, db):
    """Test updating a content creator."""
    from app.models.content_creator import ContentCreator
    creator = ContentCreator(
        name="Old Creator",
        username="oldcreator",
        is_verified=False,
    )
    db.add(creator)
    db.commit()
    db.refresh(creator)

    response = authenticated_client.put(
        f"/content/creators/{creator.id}",
        json={"name": "New Creator", "is_verified": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Creator updated successfully"
    assert data["data"]["name"] == "New Creator"
    assert data["data"]["is_verified"] is True


def test_create_short(authenticated_client, db):
    """Test creating a short."""
    from app.models.content_creator import ContentCreator
    creator = ContentCreator(
        name="Short Creator",
        username="shortcreator",
        is_verified=False,
    )
    db.add(creator)
    db.commit()
    db.refresh(creator)

    response = authenticated_client.post(
        "/content/shorts",
        json={
            "title": "Test Short",
            "thumbnail_url": "https://placehold.co/400x700?text=Short",
            "creator_id": str(creator.id),
            "language": "en",
            "views_count": 100,
            "is_published": True,
            "sort_order": 1,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Short created successfully"
    assert data["data"]["title"] == "Test Short"
    assert data["data"]["views_count"] == 100


def test_update_short(authenticated_client, db):
    """Test updating a short."""
    from app.models.content_creator import ContentCreator
    from app.models.short import Short
    creator = ContentCreator(
        name="Short Creator 2",
        username="shortcreator2",
        is_verified=False,
    )
    db.add(creator)
    db.commit()
    db.refresh(creator)

    short = Short(
        title="Old Short",
        creator_id=creator.id,
        language="en",
        views_count=0,
        is_published=True,
        sort_order=0,
    )
    db.add(short)
    db.commit()
    db.refresh(short)

    response = authenticated_client.put(
        f"/content/shorts/{short.id}",
        json={"title": "New Short", "views_count": 500},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Short updated successfully"
    assert data["data"]["title"] == "New Short"
    assert data["data"]["views_count"] == 500


def test_create_live_video(authenticated_client, db):
    """Test creating a live video."""
    from app.models.content_creator import ContentCreator
    creator = ContentCreator(
        name="Live Creator",
        username="livecreator",
        is_verified=False,
    )
    db.add(creator)
    db.commit()
    db.refresh(creator)

    response = authenticated_client.post(
        "/content/live-videos",
        json={
            "title": "Test Live",
            "thumbnail_url": "https://placehold.co/1200x675?text=Live",
            "creator_id": str(creator.id),
            "language": "en",
            "viewer_count": 50,
            "is_live": True,
            "sort_order": 1,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Live video created successfully"
    assert data["data"]["title"] == "Test Live"
    assert data["data"]["viewer_count"] == 50


def test_update_live_video(authenticated_client, db):
    """Test updating a live video."""
    from app.models.content_creator import ContentCreator
    from app.models.live_video import LiveVideo
    creator = ContentCreator(
        name="Live Creator 2",
        username="livecreator2",
        is_verified=False,
    )
    db.add(creator)
    db.commit()
    db.refresh(creator)

    live_video = LiveVideo(
        title="Old Live",
        creator_id=creator.id,
        language="en",
        viewer_count=0,
        is_live=True,
        sort_order=0,
    )
    db.add(live_video)
    db.commit()
    db.refresh(live_video)

    response = authenticated_client.put(
        f"/content/live-videos/{live_video.id}",
        json={"title": "New Live", "viewer_count": 1000},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Live video updated successfully"
    assert data["data"]["title"] == "New Live"
    assert data["data"]["viewer_count"] == 1000


def test_update_nonexistent_banner(authenticated_client):
    """Test updating a non-existent banner returns 404."""
    from uuid import uuid4
    response = authenticated_client.put(
        f"/content/banners/{uuid4()}",
        json={"title": "New Title"},
    )
    assert response.status_code == 404
    data = response.json()
    assert data["success"] is False
    assert "Banner not found" in data["message"]