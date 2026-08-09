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

### 4. Create/Update Content (Admin)
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

### 5. Upload Subtitle
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

Rate limit exceeded → `429`:
```json
{ "message": "Rate limit exceeded", "success": false, "data": null }
```

---

## Running Tests

```bash
./venv/bin/python -m pytest app/tests/ -v
```

**34 tests** covering: auth (14), home (9), content CRUD (11).

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