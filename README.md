# Dubflow Backend

FastAPI backend for Dubflow — a subtitle translation + streaming content platform. Provides authentication, project management, subtitle translation, Home screen data, and content CRUD APIs.

## Tech Stack

| Technology | Purpose |
|-----------|---------|
| **FastAPI** | Web framework — auto-generates OpenAPI docs at `/docs` |
| **PostgreSQL** | Database (Neon) |
| **SQLAlchemy** | ORM |
| **Alembic** | Database migrations |
| **Argon2** | Password hashing |
| **JWT (python-jose)** | Token-based authentication |
| **Pydantic** | Data validation |
| **Uvicorn** | ASGI server |
| **SlowAPI** | Rate limiting |

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create `.env`:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/dubflow_db
SECRET_KEY=your-super-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENVIRONMENT=development
```

Run:
```bash
alembic upgrade head
./start.sh          # or: uvicorn app.main:app --reload
```

Server runs at **http://localhost:8000** — interactive docs at **/docs**.

---

## Universal Response Format

**Every JSON API response follows this structure:**

```json
{
  "message": "Human-readable message",
  "success": true,
  "data": { }
}
```

- `message` — string, describes what happened
- `success` — boolean, `true` for success, `false` for errors
- `data` — the actual payload (object, array, or `null`)

**Error responses** (e.g. 401, 404, 400) also use this format:
```json
{
  "message": "Not authenticated",
  "success": false,
  "data": null
}
```

> **Note:** The subtitle upload endpoint (`/subtitles/upload-subtitle`) returns a **file download**, not JSON.

---

## Authentication

All auth endpoints are prefixed with `/auth`.

| Method | Endpoint | Description | Auth | Rate Limit |
|--------|----------|-------------|:---:|:---:|
| POST | `/auth/register` | Register a new user | ❌ | 5/min |
| POST | `/auth/login` | Login, get JWT token | ❌ | 10/min |
| GET | `/auth/me` | Get current user | ✅ | — |
| POST | `/auth/logout` | Clear auth cookie | ❌ | — |

### Register

```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "myuser",
  "password": "securepassword"
}
```

**Response** `200 OK`:
```json
{
  "message": "User registered successfully",
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "username": "myuser",
    "avatar_url": null
  }
}
```

**Error** `400` (duplicate email):
```json
{ "message": "Email already registered", "success": false, "data": null }
```

### Login

```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response** `200 OK`:
```json
{
  "message": "Login successful",
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer"
  }
}
```

The JWT is also set as an HttpOnly cookie (`access_token`) automatically.

### Get Current User

```http
GET /auth/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

**Response** `200 OK`:
```json
{
  "message": "User fetched successfully",
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "username": "myuser",
    "avatar_url": null
  }
}
```

### Logout

```http
POST /auth/logout
```

**Response** `200 OK`:
```json
{ "message": "Logged out successfully", "success": true, "data": null }
```

---

## Home Screen API

Returns all data needed to render the Flutter Home screen in **one request**.

| Method | Endpoint | Description | Auth | Rate Limit |
|--------|----------|-------------|:---:|:---:|
| GET | `/home` | All home data (user, banners, movies, creators, shorts, live videos) | ✅ | 30/min |

```http
GET /home
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

**Response** `200 OK`:
```json
{
  "message": "Home data fetched successfully",
  "success": true,
  "data": {
    "user": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "username": "myuser",
      "avatar_url": null
    },
    "banners": [
      {
        "id": "uuid",
        "title": "Trending Now",
        "subtitle": "Watch what everyone is talking about",
        "image_url": "https://placehold.co/1600x600?text=Trending+Now",
        "content_type": "movie",
        "content_id": null
      }
    ],
    "popular_movies": [
      {
        "id": "uuid",
        "title": "Oppenheimer",
        "poster_url": "https://placehold.co/400x600?text=Oppenheimer",
        "banner_url": "https://placehold.co/1600x600?text=Oppenheimer",
        "source_language": "en",
        "content_type": "movie",
        "is_popular": true,
        "is_featured": true,
        "rating": 8.5,
        "release_year": 2023
      }
    ],
    "creators": [
      {
        "id": "uuid",
        "name": "Aadi",
        "username": "aadi",
        "avatar_url": "https://placehold.co/200x200?text=Aadi",
        "is_verified": true
      }
    ],
    "shorts": [
      {
        "id": "uuid",
        "title": "Oppenheimer Best Scene",
        "thumbnail_url": "https://placehold.co/400x700?text=Oppenheimer+Short",
        "creator": {
          "id": "uuid",
          "name": "Aadi",
          "username": "aadi",
          "avatar_url": "https://placehold.co/200x200?text=Aadi"
        },
        "language": "en",
        "views_count": 12000
      }
    ],
    "live_videos": [
      {
        "id": "uuid",
        "title": "Behind the Scenes of Action!",
        "thumbnail_url": "https://placehold.co/1200x675?text=Live+Action",
        "creator": {
          "id": "uuid",
          "name": "Robert",
          "username": "robert",
          "avatar_url": "https://placehold.co/200x200?text=Robert"
        },
        "language": "en",
        "viewer_count": 4100,
        "is_live": true
      }
    ]
  }
}
```

**Section limits:** banners: 5, popular movies: 10, creators: 10, shorts: 10, live videos: 10.

---

## Explore API

Returns all data needed to render the Flutter **Explore screen** in **one request**. Explore queries reusable domain tables (Content, Category, CreatorProfile, UserFollow, PlaybackHistory) rather than UI-specific tables.

| Method | Endpoint | Description | Auth | Rate Limit |
|--------|----------|-------------|:---:|:---:|
| GET | `/explore` | All explore sections (featured, categories, content, trending_now, top_artists, recently_played) | Optional | 30/min |

> **Auth is optional.** Without a token, `following` and `recently_played` return `[]`. With a token, they reflect the current user's follows & playback history.

```http
GET /explore
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

**Response** `200 OK`:
```json
{
  "message": "Explore data fetched successfully",
  "success": true,
  "data": {
    "featured": [
      {
        "id": "uuid",
        "title": "Learn Python in 10 Minutes",
        "description": "A quick Python tutorial for beginners.",
        "content_type": "video",
        "thumbnail_url": "https://placehold.co/400x700?text=Python+Tutorial",
        "banner_url": "https://placehold.co/1600x600?text=Learning",
        "creator": {
          "id": "uuid",
          "username": "sara",
          "display_name": "Sara",
          "avatar_url": "https://placehold.co/200x200?text=Sara",
          "is_verified": true
        },
        "view_count": 45000,
        "like_count": 5200,
        "duration_seconds": 600,
        "created_at": "2026-08-09T19:58:24.903733+05:30"
      }
    ],
    "categories": [
      { "id": "uuid", "name": "Trend", "slug": "trend", "icon_url": "https://..." },
      { "id": "uuid", "name": "Music", "slug": "music", "icon_url": "https://..." },
      { "id": "uuid", "name": "Gaming", "slug": "gaming", "icon_url": "https://..." },
      { "id": "uuid", "name": "Learning", "slug": "learning", "icon_url": "https://..." }
    ],
    "content": {
      "recent": [ /* ContentResponse[] */ ],
      "following": [ /* ContentResponse[] — empty if not authenticated */ ],
      "trendy": [ /* ContentResponse[] */ ],
      "learning": [ /* ContentResponse[] */ ]
    },
    "trending_now": [ /* ContentResponse[] */ ],
    "top_artists": [
      {
        "id": "uuid",
        "username": "sara",
        "display_name": "Sara",
        "avatar_url": "https://placehold.co/200x200?text=Sara",
        "is_verified": true,
        "follower_count": 21000
      }
    ],
    "recently_played": [ /* ContentResponse[] — empty if not authenticated */ ]
  }
}
```

**Section limits (configurable):** featured: 5, recent: 10, following: 10, trendy: 10, learning: 10, trending_now: 10, top_artists: 10, recently_played: 10.

> Each `featured`/`content`/`trending_now`/`recently_played` item uses the **ContentResponse** shape above (id, title, description, content_type, thumbnail_url, banner_url, creator, view_count, like_count, duration_seconds, created_at). No passwords or sensitive user fields are ever returned.

---

## Explore CRUD APIs

All explore CRUD endpoints are prefixed with `/explore`. **All require authentication** (Bearer token or cookie). Rate limit: 30/min each.

These endpoints let a frontend admin/manage content, categories, creators, follows, and playback history.

### Categories

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/explore/categories` | Create a category |
| PUT | `/explore/categories/{id}` | Update a category |

**Create Category:**
```http
POST /explore/categories
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json

{
  "name": "Animation",
  "slug": "animation",
  "description": "Animated content",
  "icon_url": "https://placehold.co/100x100?text=Animation"
}
```

**Response** `200 OK`:
```json
{
  "message": "Category created successfully",
  "success": true,
  "data": {
    "id": "uuid",
    "name": "Animation",
    "slug": "animation",
    "description": "Animated content",
    "icon_url": "https://placehold.co/100x100?text=Animation"
  }
}
```

**Update Category** (only send fields to change):
```http
PUT /explore/categories/{category_id}
Content-Type: application/json

{ "name": "Animation & Cartoons", "description": "Updated description" }
```

### Creator Profiles

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/explore/creators` | Create a creator profile (links a `users` row) |
| PUT | `/explore/creators/{id}` | Update a creator profile |

**Create Creator Profile:**
```http
POST /explore/creators
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json

{
  "user_id": "uuid-of-existing-user",
  "display_name": "Aadi",
  "bio": "Movie reviewer and reactor.",
  "avatar_url": "https://placehold.co/200x200?text=Aadi",
  "is_verified": true,
  "follower_count": 12500
}
```

**Response** `200 OK`:
```json
{
  "message": "Creator profile created successfully",
  "success": true,
  "data": {
    "id": "uuid",
    "user_id": "uuid-of-user",
    "display_name": "Aadi",
    "bio": "Movie reviewer and reactor.",
    "avatar_url": "https://placehold.co/200x200?text=Aadi",
    "is_verified": true,
    "follower_count": 12500
  }
}
```

**Update Creator Profile:**
```http
PUT /explore/creators/{profile_id}
Content-Type: application/json

{ "display_name": "Aadi Official", "is_verified": true }
```

### Content

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/explore/content` | Create a content item |
| PUT | `/explore/content/{id}` | Update a content item |

**Create Content:**
```http
POST /explore/content
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json

{
  "creator_id": "uuid-of-creator-profile",
  "title": "My New Video",
  "description": "A test video",
  "content_type": "video",
  "thumbnail_url": "https://placehold.co/400x700?text=New",
  "banner_url": "https://placehold.co/1600x600?text=New",
  "status": "published",
  "visibility": "public",
  "duration_seconds": 120,
  "view_count": 0,
  "like_count": 0,
  "is_featured": false
}
```

> **content_type** values: `movie` | `short` | `video` | `live`
> **status** values: `draft` | `published` | `archived`
> **visibility** values: `public` | `private` | `unlisted`

**Response** `200 OK`:
```json
{
  "message": "Content created successfully",
  "success": true,
  "data": {
    "id": "uuid",
    "creator_id": "uuid-of-creator-profile",
    "title": "My New Video",
    "description": "A test video",
    "content_type": "video",
    "thumbnail_url": "https://placehold.co/400x700?text=New",
    "banner_url": "https://placehold.co/1600x600?text=New",
    "status": "published",
    "visibility": "public",
    "duration_seconds": 120,
    "view_count": 0,
    "like_count": 0,
    "is_featured": false
  }
}
```

**Update Content:**
```http
PUT /explore/content/{content_id}
Content-Type: application/json

{ "title": "New Title", "view_count": 100, "like_count": 20 }
```

### Content ↔ Category Association

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/explore/content-categories` | Attach a category to a content item |

```http
POST /explore/content-categories
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json

{
  "content_id": "uuid-of-content",
  "category_id": "uuid-of-category"
}
```

**Response** `200 OK`:
```json
{
  "message": "Content category association created successfully",
  "success": true,
  "data": {
    "content_id": "uuid-of-content",
    "category_id": "uuid-of-category"
  }
}
```

> **Error** `400` (duplicate): `{ "message": "Content already in this category", "success": false, "data": null }`

### Follows

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/explore/follows` | Follow a user |
| PUT | `/explore/follows/{id}` | Update a follow relationship |

**Create Follow:**
```http
POST /explore/follows
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json

{
  "follower_id": "uuid-of-current-user",
  "following_id": "uuid-of-user-to-follow"
}
```

**Response** `200 OK`:
```json
{
  "message": "Follow relationship created successfully",
  "success": true,
  "data": {
    "id": "uuid",
    "follower_id": "uuid-of-current-user",
    "following_id": "uuid-of-user-to-follow"
  }
}
```

> **Error** `400` (self-follow): `{ "message": "Cannot follow yourself", "success": false, "data": null }`
> **Error** `400` (duplicate): `{ "message": "Already following this user", "success": false, "data": null }`

### Playback History

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/explore/playback-history` | Record/update playback (upsert — no duplicate rows) |
| PUT | `/explore/playback-history/{id}` | Update a playback record |

**Record Playback:**
```http
POST /explore/playback-history
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json

{
  "user_id": "uuid-of-user",
  "content_id": "uuid-of-content",
  "progress_seconds": 45,
  "completed": false
}
```

**Response** `200 OK`:
```json
{
  "message": "Playback history created successfully",
  "success": true,
  "data": {
    "id": "uuid",
    "user_id": "uuid-of-user",
    "content_id": "uuid-of-content",
    "progress_seconds": 45,
    "completed": false
  }
}
```

> **Upsert behavior:** calling POST again with the same `user_id` + `content_id` updates the existing record instead of creating a duplicate — perfect for "recently played" tracking.

---

## Content CRUD APIs

All content endpoints are prefixed with `/content`. **All require authentication** (Bearer token or cookie). Rate limit: 30/min each.

### Home Banners

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/content/banners` | Create a banner |
| PUT | `/content/banners/{id}` | Update a banner |

**Create Banner:**
```http
POST /content/banners
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json

{
  "title": "Trending Now",
  "subtitle": "Watch what everyone is talking about",
  "image_url": "https://placehold.co/1600x600?text=Trending+Now",
  "content_type": "movie",
  "content_id": null,
  "is_active": true,
  "sort_order": 1
}
```

**Response** `200 OK`:
```json
{
  "message": "Banner created successfully",
  "success": true,
  "data": {
    "id": "uuid",
    "title": "Trending Now",
    "subtitle": "Watch what everyone is talking about",
    "image_url": "https://placehold.co/1600x600?text=Trending+Now",
    "content_type": "movie",
    "content_id": null,
    "is_active": true,
    "sort_order": 1
  }
}
```

**Update Banner** (only send fields you want to change):
```http
PUT /content/banners/{banner_id}
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json

{ "title": "New Title", "sort_order": 2 }
```

**Error** `404`:
```json
{ "message": "Banner not found", "success": false, "data": null }
```

### Movies

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/content/movies` | Create a movie |
| PUT | `/content/movies/{id}` | Update a movie |

**Create Movie:**
```http
POST /content/movies
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json

{
  "title": "Oppenheimer",
  "description": "The story of J. Robert Oppenheimer.",
  "poster_url": "https://placehold.co/400x600?text=Oppenheimer",
  "banner_url": "https://placehold.co/1600x600?text=Oppenheimer",
  "source_language": "en",
  "content_type": "movie",
  "is_popular": true,
  "is_featured": true,
  "rating": 8.5,
  "release_year": 2023,
  "sort_order": 1
}
```

**Response** `200 OK`:
```json
{
  "message": "Movie created successfully",
  "success": true,
  "data": {
    "id": "uuid",
    "title": "Oppenheimer",
    "description": "The story of J. Robert Oppenheimer.",
    "poster_url": "https://placehold.co/400x600?text=Oppenheimer",
    "banner_url": "https://placehold.co/1600x600?text=Oppenheimer",
    "source_language": "en",
    "content_type": "movie",
    "is_popular": true,
    "is_featured": true,
    "rating": 8.5,
    "release_year": 2023,
    "sort_order": 1
  }
}
```

**Update Movie:**
```http
PUT /content/movies/{movie_id}
Content-Type: application/json

{ "title": "New Title", "rating": 9.0 }
```

### Content Creators

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/content/creators` | Create a creator |
| PUT | `/content/creators/{id}` | Update a creator |

**Create Creator:**
```http
POST /content/creators
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json

{
  "name": "Aadi",
  "username": "aadi",
  "avatar_url": "https://placehold.co/200x200?text=Aadi",
  "bio": "Movie reviewer and reactor.",
  "is_verified": true
}
```

**Response** `200 OK`:
```json
{
  "message": "Creator created successfully",
  "success": true,
  "data": {
    "id": "uuid",
    "name": "Aadi",
    "username": "aadi",
    "avatar_url": "https://placehold.co/200x200?text=Aadi",
    "bio": "Movie reviewer and reactor.",
    "is_verified": true
  }
}
```

### Shorts

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/content/shorts` | Create a short |
| PUT | `/content/shorts/{id}` | Update a short |

**Create Short:**
```http
POST /content/shorts
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json

{
  "title": "Oppenheimer Best Scene",
  "description": "The most intense scene.",
  "thumbnail_url": "https://placehold.co/400x700?text=Short",
  "creator_id": "uuid-of-creator",
  "language": "en",
  "views_count": 12000,
  "is_published": true,
  "sort_order": 1
}
```

**Response** `200 OK`:
```json
{
  "message": "Short created successfully",
  "success": true,
  "data": {
    "id": "uuid",
    "title": "Oppenheimer Best Scene",
    "description": "The most intense scene.",
    "thumbnail_url": "https://placehold.co/400x700?text=Short",
    "creator_id": "uuid-of-creator",
    "language": "en",
    "views_count": 12000,
    "is_published": true,
    "sort_order": 1
  }
}
```

### Live Videos

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/content/live-videos` | Create a live video |
| PUT | `/content/live-videos/{id}` | Update a live video |

**Create Live Video:**
```http
POST /content/live-videos
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json

{
  "title": "Behind the Scenes of Action!",
  "description": "Live set tour.",
  "thumbnail_url": "https://placehold.co/1200x675?text=Live",
  "creator_id": "uuid-of-creator",
  "language": "en",
  "viewer_count": 4100,
  "is_live": true,
  "started_at": "2026-08-09T12:00:00Z",
  "sort_order": 1
}
```

**Response** `200 OK`:
```json
{
  "message": "Live video created successfully",
  "success": true,
  "data": {
    "id": "uuid",
    "title": "Behind the Scenes of Action!",
    "description": "Live set tour.",
    "thumbnail_url": "https://placehold.co/1200x675?text=Live",
    "creator_id": "uuid-of-creator",
    "language": "en",
    "viewer_count": 4100,
    "is_live": true,
    "started_at": "2026-08-09T12:00:00Z",
    "sort_order": 1
  }
}
```

---

## Projects

All project endpoints are prefixed with `/projects`. **All require authentication.**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/projects` | Create a project |
| GET | `/projects` | List current user's projects |
| GET | `/projects/{id}` | Get a single project |

> **Note:** Uploading a subtitle file auto-creates a project. These endpoints are for manual management.

**Create Project:**
```http
POST /projects
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json

{
  "name": "My Video Project",
  "source_language": "en",
  "target_language": "es"
}
```

**Response** `200 OK`:
```json
{
  "message": "Project created successfully",
  "success": true,
  "data": {
    "id": "uuid",
    "name": "My Video Project",
    "original_file_name": null,
    "source_language": "en",
    "target_language": "es",
    "status": "pending",
    "created_at": "2026-08-09T12:00:00Z",
    "updated_at": null
  }
}
```

**List Projects:**
```http
GET /projects
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

**Response** `200 OK`:
```json
{
  "message": "Projects fetched successfully",
  "success": true,
  "data": [
    {
      "id": "uuid",
      "name": "My Video Project",
      "original_file_name": "demo.srt",
      "source_language": "en",
      "target_language": "es",
      "status": "completed",
      "created_at": "2026-08-09T12:00:00Z",
      "updated_at": "2026-08-09T12:05:00Z"
    }
  ]
}
```

---

## Subtitles

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/subtitles/upload-subtitle` | Upload SRT → auto-create project → translate → download |

**Upload & Translate:**
```http
POST /subtitles/upload-subtitle
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: multipart/form-data

source_language: en
target_language: es
file: @demo-srt-file.srt
```

**Response:** Translated `.srt` file download (`application/octet-stream`).

**Error** `400`:
```json
{ "message": "Only .srt files are allowed", "success": false, "data": null }
```

---

## Frontend Integration Flow

### 1. Register
```dart
final response = await http.post(
  Uri.parse('$baseUrl/auth/register'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({
    'email': email,
    'username': username,
    'password': password,
  }),
);
final data = jsonDecode(response.body);
// data["success"] == true → registration successful
// data["data"]["id"] → user id
```

### 2. Login
```dart
final response = await http.post(
  Uri.parse('$baseUrl/auth/login'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({'email': email, 'password': password}),
);
final data = jsonDecode(response.body);
// data["success"] == true → login successful
// data["data"]["access_token"] → store this token
// Send it as: Authorization: Bearer <token>
```

### 3. Fetch Home Screen
```dart
final response = await http.get(
  Uri.parse('$baseUrl/home'),
  headers: {'Authorization': 'Bearer $token'},
);
final data = jsonDecode(response.body);
// data["data"]["user"] → welcome header
// data["data"]["banners"] → carousel
// data["data"]["popular_movies"] → movie rows
// data["data"]["creators"] → follow creators row
// data["data"]["shorts"] → shorts section
// data["data"]["live_videos"] → live section
```

### 4. Fetch Explore Screen
```dart
// Auth is optional. For a logged-in user (so following & recently_played populate):
final response = await http.get(
  Uri.parse('$baseUrl/explore'),
  headers: {'Authorization': 'Bearer $token'},
);
final data = jsonDecode(response.body)["data"];

// data["featured"] → hero carousel (ContentResponse[])
// data["categories"] → filter chip row (CategoryResponse[])
//   - each: { id, name, slug, icon_url }
// data["content"]["recent"] → recent section (ContentResponse[])
// data["content"]["following"] → following section (ContentResponse[])
// data["content"]["trendy"] → trendy section (ContentResponse[])
// data["content"]["learning"] → learning section (ContentResponse[])
// data["trending_now"] → trending now row (ContentResponse[])
// data["top_artists"] → top artists row (TopArtistResponse[])
//   - each: { id, username, display_name, avatar_url, is_verified, follower_count }
// data["recently_played"] → recently played (ContentResponse[])

// Every ContentResponse item looks like:
// {
//   "id": "...",
//   "title": "...",
//   "description": "...",
//   "content_type": "video",        // movie | short | video | live
//   "thumbnail_url": "...",
//   "banner_url": "...",
//   "creator": {
//     "id": "...",
//     "username": "...",
//     "display_name": "...",
//     "avatar_url": "...",
//     "is_verified": true
//   },
//   "view_count": 45000,
//   "like_count": 5200,
//   "duration_seconds": 600,
//   "created_at": "2026-08-09T19:58:24.903733+05:30"
// }
```

### 5. Explore CRUD (Admin / User Actions)
```dart
// Create a category
final resp = await http.post(
  Uri.parse('$baseUrl/explore/categories'),
  headers: {'Content-Type': 'application/json', 'Authorization': 'Bearer $token'},
  body: jsonEncode({
    'name': 'Animation',
    'slug': 'animation',
    'description': 'Animated content',
    'icon_url': 'https://placehold.co/100x100?text=Animation',
  }),
);

// Create a content item (points to a creator profile)
final resp = await http.post(
  Uri.parse('$baseUrl/explore/content'),
  headers: {'Content-Type': 'application/json', 'Authorization': 'Bearer $token'},
  body: jsonEncode({
    'creator_id': creatorProfileId,
    'title': 'My New Video',
    'content_type': 'video',
    'thumbnail_url': 'https://...',
    'status': 'published',
    'visibility': 'public',
    'duration_seconds': 120,
    'is_featured': false,
  }),
);

// Update content (only send fields to change)
final resp = await http.put(
  Uri.parse('$baseUrl/explore/content/$contentId'),
  headers: {'Content-Type': 'application/json', 'Authorization': 'Bearer $token'},
  body: jsonEncode({'title': 'New Title', 'view_count': 100}),
);

// Follow a user (e.g. from creator profile page)
final resp = await http.post(
  Uri.parse('$baseUrl/explore/follows'),
  headers: {'Content-Type': 'application/json', 'Authorization': 'Bearer $token'},
  body: jsonEncode({
    'follower_id': currentUserId,
    'following_id': creatorUserId,
  }),
);

// Record playback progress (upserts — no duplicate rows)
final resp = await http.post(
  Uri.parse('$baseUrl/explore/playback-history'),
  headers: {'Content-Type': 'application/json', 'Authorization': 'Bearer $token'},
  body: jsonEncode({
    'user_id': currentUserId,
    'content_id': contentId,
    'progress_seconds': 45,
    'completed': false,
  }),
);
```

### 6. Create/Update Content (Admin)
```dart
// Create a movie
final response = await http.post(
  Uri.parse('$baseUrl/content/movies'),
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer $token',
  },
  body: jsonEncode({
    'title': 'Oppenheimer',
    'source_language': 'en',
    'content_type': 'movie',
    'is_popular': true,
    'rating': 8.5,
    'release_year': 2023,
  }),
);

// Update a movie
final response = await http.put(
  Uri.parse('$baseUrl/content/movies/$movieId'),
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer $token',
  },
  body: jsonEncode({'title': 'New Title', 'rating': 9.0}),
);
```

### 7. Upload Subtitle
```dart
final request = http.MultipartRequest(
  'POST',
  Uri.parse('$baseUrl/subtitles/upload-subtitle'),
);
request.headers['Authorization'] = 'Bearer $token';
request.fields['source_language'] = 'en';
request.fields['target_language'] = 'es';
request.files.add(await http.MultipartFile.fromPath('file', srtFilePath));
final response = await request.send();
// Returns translated .srt file as download
```

---

## Rate Limiting

| Endpoint | Limit |
|----------|-------|
| `POST /auth/register` | 5/min per IP |
| `POST /auth/login` | 10/min per IP |
| `POST /projects` | 30/min per IP |
| `GET /home` | 30/min per IP |
| All `/content/*` | 30/min per IP |
| `GET /explore` | 30/min per IP |
| All `/explore/*` CRUD | 30/min per IP |

Rate limit exceeded → `429`:
```json
{ "message": "Rate limit exceeded", "success": false, "data": null }
```

---

## Running Tests

```bash
./venv/bin/python -m pytest app/tests/ -v
```

**59 tests** covering: auth (14), home (9), content CRUD (11), explore read (13), explore CRUD (12).

---

## Common Commands

```bash
# Run server
./venv/bin/uvicorn app.main:app --reload

# Run tests
./venv/bin/python -m pytest app/tests/ -v

# Create migration
./venv/bin/alembic revision --autogenerate -m "description"

# Apply migrations
./venv/bin/alembic upgrade head

# Seed data
./venv/bin/python -m app.seeds.seed