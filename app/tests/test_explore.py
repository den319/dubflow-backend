import pytest


def test_explore_returns_200(authenticated_client):
    """Test that GET /explore returns 200."""
    response = authenticated_client.get("/explore")
    assert response.status_code == 200


def test_explore_returns_universal_format(authenticated_client):
    """Test that /explore returns the universal response format."""
    response = authenticated_client.get("/explore")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "message" in data
    assert "data" in data


def test_explore_returns_all_sections(authenticated_client, db):
    """Test that /explore returns all expected sections."""
    from app.seeds.explore_seed import seed_explore_data
    seed_explore_data(db)

    response = authenticated_client.get("/explore")
    assert response.status_code == 200
    data = response.json()["data"]

    assert "featured" in data
    assert "categories" in data
    assert "content" in data
    assert "trending_now" in data
    assert "top_artists" in data
    assert "recently_played" in data

    # Content sections
    assert "recent" in data["content"]
    assert "following" in data["content"]
    assert "trendy" in data["content"]
    assert "learning" in data["content"]


def test_explore_returns_categories(authenticated_client, db):
    """Test that categories are returned."""
    from app.seeds.explore_seed import seed_explore_data
    seed_explore_data(db)

    response = authenticated_client.get("/explore")
    assert response.status_code == 200
    categories = response.json()["data"]["categories"]
    assert isinstance(categories, list)
    assert len(categories) >= 4

    slugs = {c["slug"] for c in categories}
    assert "trend" in slugs
    assert "music" in slugs
    assert "gaming" in slugs
    assert "learning" in slugs


def test_explore_returns_featured(authenticated_client, db):
    """Test that featured content is returned."""
    from app.seeds.explore_seed import seed_explore_data
    seed_explore_data(db)

    response = authenticated_client.get("/explore")
    assert response.status_code == 200
    featured = response.json()["data"]["featured"]
    assert isinstance(featured, list)
    assert len(featured) > 0
    assert "title" in featured[0]
    assert "creator" in featured[0]
    assert "view_count" in featured[0]


def test_explore_returns_trending(authenticated_client, db):
    """Test that trending content is returned."""
    from app.seeds.explore_seed import seed_explore_data
    seed_explore_data(db)

    response = authenticated_client.get("/explore")
    assert response.status_code == 200
    trending = response.json()["data"]["trending_now"]
    assert isinstance(trending, list)
    assert len(trending) > 0


def test_explore_returns_top_artists(authenticated_client, db):
    """Test that top artists are returned."""
    from app.seeds.explore_seed import seed_explore_data
    seed_explore_data(db)

    response = authenticated_client.get("/explore")
    assert response.status_code == 200
    artists = response.json()["data"]["top_artists"]
    assert isinstance(artists, list)
    assert len(artists) > 0
    artist = artists[0]
    assert "display_name" in artist
    assert "follower_count" in artist
    assert "is_verified" in artist
    # Should not expose sensitive fields
    assert "hashed_password" not in artist


def test_explore_returns_learning_content(authenticated_client, db):
    """Test that learning content is returned."""
    from app.seeds.explore_seed import seed_explore_data
    seed_explore_data(db)

    response = authenticated_client.get("/explore")
    assert response.status_code == 200
    learning = response.json()["data"]["content"]["learning"]
    assert isinstance(learning, list)
    assert len(learning) > 0


def test_explore_returns_following_content(authenticated_client, db):
    """Test that following content is returned for authenticated user."""
    from app.seeds.explore_seed import seed_explore_data
    seed_explore_data(db)

    response = authenticated_client.get("/explore")
    assert response.status_code == 200
    following = response.json()["data"]["content"]["following"]
    assert isinstance(following, list)
    assert len(following) > 0


def test_explore_returns_recently_played(authenticated_client, db):
    """Test that recently played content is returned."""
    from app.seeds.explore_seed import seed_explore_data
    seed_explore_data(db)

    response = authenticated_client.get("/explore")
    assert response.status_code == 200
    recently_played = response.json()["data"]["recently_played"]
    assert isinstance(recently_played, list)
    assert len(recently_played) > 0


def test_explore_without_auth_returns_200(client):
    """Test that /explore works without authentication."""
    response = client.get("/explore")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    # Following and recently played should be empty without auth
    assert data["data"]["content"]["following"] == []
    assert data["data"]["recently_played"] == []


def test_explore_empty_sections_do_not_fail(authenticated_client):
    """Test that empty sections return [] instead of erroring."""
    response = authenticated_client.get("/explore")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["featured"] == []
    assert data["categories"] == []
    assert data["content"]["recent"] == []
    assert data["content"]["following"] == []
    assert data["content"]["trendy"] == []
    assert data["content"]["learning"] == []
    assert data["trending_now"] == []
    assert data["top_artists"] == []
    assert data["recently_played"] == []


def test_explore_content_has_creator_info(authenticated_client, db):
    """Test that content items include creator info."""
    from app.seeds.explore_seed import seed_explore_data
    seed_explore_data(db)

    response = authenticated_client.get("/explore")
    assert response.status_code == 200
    featured = response.json()["data"]["featured"]
    assert len(featured) > 0
    creator = featured[0]["creator"]
    assert "id" in creator
    assert "username" in creator
    assert "display_name" in creator
    assert "is_verified" in creator
    # No sensitive fields
    assert "hashed_password" not in creator