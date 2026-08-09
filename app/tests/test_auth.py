import pytest
from fastapi.testclient import TestClient


def test_register_user(client):
    """Test user registration."""
    response = client.post(
        "/auth/register",
        json={
            "email": "test_register@example.com",
            "username": "testuser",
            "password": "password123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "User registered successfully"
    assert data["data"]["email"] == "test_register@example.com"
    assert data["data"]["username"] == "testuser"
    assert "id" in data["data"]


def test_register_duplicate_email(client):
    """Test that registering with same email fails."""
    # First registration
    client.post(
        "/auth/register",
        json={
            "email": "test_duplicate@example.com",
            "username": "testuser",
            "password": "password123",
        },
    )
    # Second registration with same email
    response = client.post(
        "/auth/register",
        json={
            "email": "test_duplicate@example.com",
            "username": "anotheruser",
            "password": "password456",
        },
    )
    # Should fail (400: email already registered)
    assert response.status_code in [400, 422, 500]
    data = response.json()
    assert data["success"] is False


def test_login_success(client):
    """Test successful login."""
    # Register first
    client.post(
        "/auth/register",
        json={
            "email": "test_login@example.com",
            "username": "loginuser",
            "password": "password123",
        },
    )
    # Login
    response = client.post(
        "/auth/login",
        json={"email": "test_login@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Login successful"
    assert data["data"]["token_type"] == "bearer"
    assert "access_token" in data["data"]
    # Check that cookie was set
    assert "access_token" in response.cookies


def test_login_wrong_password(client):
    """Test login with wrong password."""
    # Register first
    client.post(
        "/auth/register",
        json={
            "email": "test_wrongpw@example.com",
            "username": "testuser",
            "password": "password123",
        },
    )
    # Login with wrong password
    response = client.post(
        "/auth/login",
        json={"email": "test_wrongpw@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    data = response.json()
    assert data["success"] is False
    assert "Invalid credentials" in data["message"]


def test_login_nonexistent_user(client):
    """Test login with non-existent email."""
    response = client.post(
        "/auth/login",
        json={"email": "notexist@example.com", "password": "password123"},
    )
    assert response.status_code == 401
    data = response.json()
    assert data["success"] is False


def test_get_current_user(authenticated_client):
    """Test getting current user profile."""
    response = authenticated_client.get("/auth/me")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["email"] == "test_user@example.com"
    assert data["data"]["username"] == "testuser"


def test_get_current_user_without_login(client):
    """Test getting current user without authentication."""
    response = client.get("/auth/me")
    assert response.status_code == 401
    data = response.json()
    assert data["success"] is False
    assert "Not authenticated" in data["message"]


def test_logout(authenticated_client):
    """Test logout clears cookie."""
    # Verify we're logged in
    me_response = authenticated_client.get("/auth/me")
    assert me_response.status_code == 200
    
    # Logout
    logout_response = authenticated_client.post("/auth/logout")
    assert logout_response.status_code == 200
    data = logout_response.json()
    assert data["success"] is True
    assert data["message"] == "Logged out successfully"
    
    # Verify cookie is cleared
    assert "access_token" not in logout_response.cookies
    
    # Now /me should fail
    me_after_logout = authenticated_client.get("/auth/me")
    assert me_after_logout.status_code == 401


def test_login_sets_httponly_cookie(client):
    """Test that login sets HttpOnly cookie for security."""
    # Register first
    client.post(
        "/auth/register",
        json={
            "email": "test_cookie@example.com",
            "username": "testuser",
            "password": "password123",
        },
    )
    # Login
    response = client.post(
        "/auth/login",
        json={"email": "test_cookie@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    
    # Check cookie attributes
    cookies = response.cookies
    assert "access_token" in cookies
    
    # Verify httponly flag is set (can't access via JavaScript)
    set_cookie_header = response.headers.get("set-cookie", "")
    assert "httponly" in set_cookie_header.lower()


def test_register_invalid_email(client):
    """Test registration with invalid email format."""
    response = client.post(
        "/auth/register",
        json={
            "email": "invalid-email",  # Missing @ and domain
            "username": "testuser",
            "password": "password123",
        },
    )
    assert response.status_code == 422  # Validation error
    data = response.json()
    assert "detail" in data  # Pydantic validation error


def test_register_missing_password(client):
    """Test registration without password."""
    response = client.post(
        "/auth/register",
        json={
            "email": "test_missing@example.com",
            "username": "testuser",
            # Missing password
        },
    )
    assert response.status_code == 422  # Validation error


def test_password_is_hashed(client, db):
    """Test that passwords are stored as hashes, not plain text."""
    from app.models.user import User
    
    # Register user
    client.post(
        "/auth/register",
        json={
            "email": "test_hash@example.com",
            "username": "testuser",
            "password": "password123",
        },
    )
    
    # Query user directly from database
    user = db.query(User).filter(User.email == "test_hash@example.com").first()
    assert user is not None
    # Password should be hashed (Argon2 hashes start with $argon2id$)
    assert user.hashed_password.startswith("$argon2id$")
    assert user.hashed_password != "password123"