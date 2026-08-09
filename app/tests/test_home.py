import pytest


def test_home_returns_200(authenticated_client):
    """Test that GET /home returns 200."""
    response = authenticated_client.get("/home")
    assert response.status_code == 200


def test_home_returns_authenticated_user(authenticated_client):
    """Test that authenticated user information is returned correctly."""
    response = authenticated_client.get("/home")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["user"]["username"] == "testuser"
    assert data["data"]["user"]["id"] is not None


def test_home_requires_auth(client):
    """Test that /home requires authentication."""
    response = client.get("/home")
    assert response.status_code == 401
    data = response.json()
    assert data["success"] is False
    assert "Not authenticated" in data["message"]


def test_home_returns_banners(authenticated_client, db):
    """Test that banners are returned."""
    from app.seeds.home_seed import seed_home_data
    seed_home_data(db)

    response = authenticated_client.get("/home")
    assert response.status_code == 200
    data = response.json()
    banners = data["data"]["banners"]
    assert isinstance(banners, list)
    assert len(banners) > 0
    assert "title" in banners[0]
    assert "image_url" in banners[0]


def test_home_returns_popular_movies(authenticated_client, db):
    """Test that popular movies are returned."""
    from app.seeds.home_seed import seed_home_data
    seed_home_data(db)

    response = authenticated_client.get("/home")
    assert response.status_code == 200
    data = response.json()
    movies = data["data"]["popular_movies"]
    assert isinstance(movies, list)
    assert len(movies) > 0
    assert "title" in movies[0]
    assert "poster_url" in movies[0]
    assert "rating" in movies[0]


def test_home_returns_creators(authenticated_client, db):
    """Test that creators are returned."""
    from app.seeds.home_seed import seed_home_data
    seed_home_data(db)

    response = authenticated_client.get("/home")
    assert response.status_code == 200
    data = response.json()
    creators = data["data"]["creators"]
    assert isinstance(creators, list)
    assert len(creators) > 0
    assert "name" in creators[0]
    assert "username" in creators[0]
    assert "is_verified" in creators[0]


def test_home_returns_shorts(authenticated_client, db):
    """Test that shorts are returned."""
    from app.seeds.home_seed import seed_home_data
    seed_home_data(db)

    response = authenticated_client.get("/home")
    assert response.status_code == 200
    data = response.json()
    shorts = data["data"]["shorts"]
    assert isinstance(shorts, list)
    assert len(shorts) > 0
    short = shorts[0]
    assert "title" in short
    assert "thumbnail_url" in short
    assert "creator" in short
    assert "views_count" in short
    assert "name" in short["creator"]


def test_home_returns_live_videos(authenticated_client, db):
    """Test that live videos are returned."""
    from app.seeds.home_seed import seed_home_data
    seed_home_data(db)

    response = authenticated_client.get("/home")
    assert response.status_code == 200
    data = response.json()
    live_videos = data["data"]["live_videos"]
    assert isinstance(live_videos, list)
    assert len(live_videos) > 0
    live = live_videos[0]
    assert "title" in live
    assert "thumbnail_url" in live
    assert "creator" in live
    assert "viewer_count" in live
    assert "is_live" in live


def test_home_empty_sections_do_not_fail(authenticated_client, db):
    """Test that empty sections return [] instead of erroring."""
    # No home data seeded - all sections should be empty
    response = authenticated_client.get("/home")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["banners"] == []
    assert data["data"]["popular_movies"] == []
    assert data["data"]["creators"] == []
    assert data["data"]["shorts"] == []
    assert data["data"]["live_videos"] == []