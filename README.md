# Dubflow Backend

A FastAPI backend for subtitle translation with authentication, project management, and automatic translation. Users can upload `.srt` subtitle files, which are automatically parsed, translated, and returned as a translated file — all in a single API call.

## Tech Stack

| Technology | Purpose |
|-----------|---------|
| **FastAPI** | Web framework — automatically generates OpenAPI docs at `/docs` |
| **PostgreSQL** | Database — production-grade relational database (Neon) |
| **SQLAlchemy** | ORM — maps Python classes to database tables |
| **Alembic** | Database migrations — tracks schema changes |
| **Argon2** | Password hashing — securely stores user passwords |
| **JWT (python-jose)** | Token-based authentication — stateless auth via signed tokens |
| **Pydantic** | Data validation — ensures request/response data integrity |
| **Uvicorn** | ASGI server — runs the FastAPI application |
| **SlowAPI** | Rate limiting — protects auth endpoints from brute force |

## Project Structure

```
dubflow-backend/
├── alembic/                        # Database migration files
│   ├── versions/                   # Migration scripts
│   ├── env.py                      # Alembic environment config
│   └── script.py.mako
├── app/
│   ├── core/                       # Core setup
│   │   ├── config.py               # App config from .env
│   │   ├── database.py             # DB connection, session
│   │   ├── ratelimit.py            # Rate limiter instance
│   │   └── security.py             # Password hashing + JWT creation
│   ├── models/                     # SQLAlchemy ORM models
│   │   ├── base.py                 # DeclarativeBase + UUIDMixin
│   │   ├── user.py                 # User model
│   │   ├── project.py              # Project model
│   │   ├── subtitle_file.py        # Subtitle file model
│   │   ├── subtitle_entry.py       # Individual subtitle entry model
│   │   ├── subscription.py         # Subscription model
│   │   └── translation_cache.py    # Translation cache model
│   ├── routes/                     # API endpoints
│   │   ├── auth.py                 # Auth (register, login, me, logout)
│   │   ├── health.py               # Health check
│   │   ├── project.py              # Project CRUD
│   │   └── subtitle.py             # Subtitle upload + translate
│   ├── schemas/                    # Pydantic request/response models
│   │   ├── user.py                 # UserCreate, UserResponse, LoginRequest
│   │   └── project.py              # ProjectCreate, ProjectResponse
│   ├── services/                   # Business logic layer
│   │   ├── auth_service.py         # Auth logic + get_current_user dependency
│   │   ├── project_service.py      # Project CRUD logic
│   │   ├── subtitle_service.py     # Upload + parse + translate flow
│   │   ├── storage_service.py      # File storage
│   │   ├── generators/             # Subtitle file generators
│   │   │   └── srt_generator.py    # SRT file generation
│   │   └── translation/            # Translation services
│   │       ├── translation_service.py
│   │       └── providers/
│   │           ├── google_translate.py
│   │           └── libre_translate.py
│   ├── utils/
│   │   └── subtitle_parser.py      # SRT file parser
│   ├── tests/                      # Unit tests
│   │   ├── conftest.py             # Test fixtures
│   │   ├── test_health.py
│   │   └── test_auth.py
│   └── main.py                     # FastAPI app entry point
├── .env                            # Environment variables (gitignored)
├── alembic.ini                     # Alembic config
├── requirements.txt                # Python dependencies
├── start.sh                        # Quick start script (runs migrations + server)
└── README.md
```

## Prerequisites

- Python 3.10+
- PostgreSQL (or a Neon database URL)
- `venv` (Python virtual environment)

## Setup

### 1. Clone and Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/dubflow_db
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENVIRONMENT=development
```

> **Note:** The `SECRET_KEY` is used to sign JWT tokens. Generate a strong one for production (`openssl rand -hex 32`). Set `ENVIRONMENT=production` on your deployed server to enable secure cookies (HTTPS-only).

### 4. Create the Database

```bash
createdb dubflow_db
```

### 5. Run Database Migrations

```bash
alembic upgrade head
```

### 6. Start the Server

```bash
# Using the script (auto-runs migrations)
./start.sh

# Or directly
uvicorn app.main:app --reload
```

The server will be available at **http://localhost:8000**

## API Documentation

FastAPI generates interactive API docs automatically:

| URL | Description |
|-----|-------------|
| `/docs` | Swagger UI — test endpoints from the browser |
| `/redoc` | ReDoc — alternative docs UI |
| `/openapi.json` | OpenAPI spec (JSON) |

## API Endpoints

### Health

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|:---:|
| GET | `/` | Welcome message | ❌ |
| GET | `/health` | Health check → `{"status": "ok"}` | ❌ |

### Authentication

All auth endpoints are prefixed with `/auth`.

| Method | Endpoint | Description | Auth Required | Rate Limit |
|--------|----------|-------------|:---:|:---:|
| POST | `/auth/register` | Register a new user | ❌ | 5/min |
| POST | `/auth/login` | Login and get JWT token | ❌ | 10/min |
| GET | `/auth/me` | Get current authenticated user | ✅ | — |
| POST | `/auth/logout` | Clear auth cookie | ❌ | — |

---

#### Register

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
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "username": "myuser"
}
```

**Error** `400 Bad Request` (duplicate email):
```json
{
    "detail": "Email already registered"
}
```

---

#### Login

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
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer"
}
```

The JWT token is also set as an HttpOnly cookie (`access_token`) with:
- `HttpOnly` — JavaScript cannot read it (XSS protection)
- `SameSite=lax` — CSRF protection
- `Max-Age` — based on `ACCESS_TOKEN_EXPIRE_MINUTES`
- `Secure` — only in production (when `ENVIRONMENT=production`)

---

#### Get Current User

```http
GET /auth/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

Or via cookie:

```http
GET /auth/me
Cookie: access_token=eyJhbGciOiJIUzI1NiIs...
```

**Response** `200 OK`:
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "username": "myuser"
}
```

**Error** `401 Unauthorized`:
```json
{
    "detail": "Not authenticated"
}
```

---

#### Logout

```http
POST /auth/logout
```

**Response** `200 OK` (clears the `access_token` cookie):
```json
{
    "message": "Logged out successfully"
}
```

---

### Projects

All project endpoints are prefixed with `/projects`. **All require authentication.**

| Method | Endpoint | Description | Rate Limit |
|--------|----------|-------------|:---:|
| POST | `/projects` | Create a new project | 30/min |
| GET | `/projects` | List all projects for current user | — |
| GET | `/projects/{project_id}` | Get a single project by ID | — |

> **Note:** When you upload a subtitle file via `/subtitles/upload-subtitle`, a project is **automatically created** for you. You only need these endpoints if you want to create projects manually or list existing ones.

---

#### Create Project

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

**Response** `201 Created`:
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "My Video Project",
    "original_file_name": null,
    "source_language": "en",
    "target_language": "es",
    "status": "pending",
    "created_at": "2026-07-15T12:00:00Z",
    "updated_at": null
}
```

---

#### List Projects

```http
GET /projects
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

**Response** `200 OK`:
```json
[
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "My Video Project",
        "original_file_name": "demo-srt-file.srt",
        "source_language": "en",
        "target_language": "es",
        "status": "completed",
        "created_at": "2026-07-15T12:00:00Z",
        "updated_at": "2026-07-15T12:05:00Z"
    }
]
```

---

#### Get Project by ID

```http
GET /projects/550e8400-e29b-41d4-a716-446655440000
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

**Response** `200 OK`:
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "My Video Project",
    "original_file_name": "demo-srt-file.srt",
    "source_language": "en",
    "target_language": "es",
    "status": "completed",
    "created_at": "2026-07-15T12:00:00Z",
    "updated_at": "2026-07-15T12:05:00Z"
}
```

**Error** `404 Not Found`:
```json
{
    "detail": "Project not found"
}
```

---

### Subtitles

All subtitle endpoints are prefixed with `/subtitles`. **All require authentication.**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/subtitles/upload-subtitle` | Upload SRT file → auto-create project → translate → download |

---

#### Upload and Translate Subtitle

This is the **main endpoint** of the application. It accepts an SRT file, automatically creates a project, parses the subtitles, translates them, and returns the translated file — all in a single request.

```http
POST /subtitles/upload-subtitle
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: multipart/form-data

source_language: en
target_language: es
file: @demo-srt-file.srt
```

**Form Fields:**

| Field | Type | Required | Description |
|-------|------|:--------:|-------------|
| `source_language` | string | ✅ | Source language code (e.g., `en`, `es`, `hi`) |
| `target_language` | string | ✅ | Target language code (e.g., `es`, `hi`, `fr`) |
| `file` | file | ✅ | The `.srt` subtitle file to upload |

**Response:** The translated `.srt` file is returned as a file download (`application/octet-stream`).

**Error** `400 Bad Request`:
```json
{
    "detail": "Only .srt files are allowed"
}
```

**Error** `401 Unauthorized`:
```json
{
    "detail": "Not authenticated"
}
```

---

## Authentication Flow

### Two Ways to Authenticate

The API supports two authentication methods:

1. **Cookie-based (browser/web apps):** After login, the JWT is stored in an HttpOnly cookie. The browser automatically sends it with every request.

2. **Bearer Token (API clients like Postman, mobile apps):** After login, copy the `access_token` from the response and include it in the `Authorization` header.

```
                    REGISTER                    LOGIN
                    ─────────                   ─────
Client                      Server     Client                    Server
  │                           │         │                         │
  │ POST /auth/register      │         │ POST /auth/login        │
  │ {email, username, pw}    │         │ {email, password}       │
  │─────────────────────────>│         │────────────────────────>│
  │                           │         │                         │
  │                   1. Hash password │                 1. Find user
  │                   2. Save to DB    │                 2. Verify password
  │                   3. Return user   │                 3. Create JWT
  │                           │         │                 4. Set HttpOnly cookie
  │ {id, email, username}    │         │                         │
  │<─────────────────────────│         │ ← Set-Cookie: access_token=...
  │                           │         │ {message, access_token, token_type}
  │                           │         │<────────────────────────│


              AUTHENTICATED REQUEST (Cookie — Browser)
              ────────────────────────────────────────
Client                          Server
  │                               │
  │ GET /auth/me                  │
  │ Cookie: access_token=eyJ...   │
  │──────────────────────────────>│
  │                               │
  │                   1. Read token from cookie
  │                   2. Decode & verify JWT signature
  │                   3. Check expiration
  │                   4. Extract email from "sub" claim
  │                   5. Look up user in DB
  │                               │
  │ {id, email, username}         │
  │<──────────────────────────────│


              AUTHENTICATED REQUEST (Bearer Token — API Client)
              ─────────────────────────────────────────────────
Client                          Server
  │                               │
  │ POST /subtitles/upload-subtitle
  │ Authorization: Bearer eyJ...  │
  │──────────────────────────────>│
  │                               │
  │                   1. Read token from Authorization header
  │                   2. Decode & verify JWT signature
  │                   3. Check expiration
  │                   4. Extract email from "sub" claim
  │                   5. Look up user in DB
  │                               │
  │ Translated .srt file          │
  │<──────────────────────────────│
```

---

## Complete Integration Flow (Frontend)

Here's the typical flow for a frontend application:

```
1. User registers
   POST /auth/register → { id, email, username }

2. User logs in
   POST /auth/login → { access_token, token_type }
   → Store the access_token in localStorage/sessionStorage
   → (Cookie is also set automatically for browser requests)

3. User uploads a subtitle file
   POST /subtitles/upload-subtitle
   Authorization: Bearer <access_token>
   Form: source_language=en, target_language=es, file=subtitles.srt
   → Returns translated .srt file as download

4. (Optional) User views their projects
   GET /projects
   Authorization: Bearer <access_token>
   → Returns list of all projects with their status
```

---

## Rate Limiting

The API uses **SlowAPI** for rate limiting to prevent abuse:

| Endpoint | Limit |
|----------|-------|
| `POST /auth/register` | 5 requests per minute per IP |
| `POST /auth/login` | 10 requests per minute per IP |
| `POST /projects` | 30 requests per minute per IP |

When a rate limit is exceeded, the API returns:

```json
{
    "detail": "Rate limit exceeded"
}
```

Status code: `429 Too Many Requests`

---

## Database Models

### User (`users` table)
| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID (PK) | Auto-generated, unique |
| email | String | Unique, indexed, NOT NULL |
| username | String | Unique, indexed, NOT NULL |
| hashed_password | String | NOT NULL |
| is_active | Boolean | Default: true |
| created_at | DateTime (tz) | Auto-set |
| updated_at | DateTime (tz) | Auto-updated |

### Project (`projects` table)
| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID (PK) | Auto-generated, unique |
| user_id | UUID (FK → users.id) | NOT NULL, indexed, CASCADE delete |
| name | String | NOT NULL |
| original_file_name | String | Nullable |
| source_language | String | NOT NULL |
| target_language | String | NOT NULL |
| status | String | Default: "pending" |
| created_at | DateTime (tz) | Auto-set |
| updated_at | DateTime (tz) | Auto-updated |

### SubtitleFile (`subtitle_files` table)
| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID (PK) | Auto-generated, unique |
| project_id | UUID (FK → projects.id) | NOT NULL, indexed, CASCADE delete |
| file_type | String | NOT NULL |
| source_language | String | NOT NULL |
| target_language | String | NOT NULL |
| original_file_path | String | NOT NULL |
| translated_file_path | String | Nullable |
| total_entries | Integer | NOT NULL |
| translated_entries | Integer | NOT NULL |
| status | String | NOT NULL |
| created_at | DateTime (tz) | Auto-set |
| updated_at | DateTime (tz) | Auto-updated |

### SubtitleEntry (`subtitle_entries` table)
| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID (PK) | Auto-generated, unique |
| subtitle_file_id | UUID (FK → subtitle_files.id) | NOT NULL, indexed, CASCADE delete |
| sequence_number | Integer | NOT NULL |
| start_time | String | NOT NULL |
| end_time | String | NOT NULL |
| original_text | Text | NOT NULL |
| translated_text | Text | Nullable |
| translation_status | String | NOT NULL |
| error_message | Text | Nullable |
| created_at | DateTime (tz) | Auto-set |
| updated_at | DateTime (tz) | Auto-updated |

### Subscription (`subscriptions` table)
| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID (PK) | Auto-generated, unique |
| user_id | UUID (FK → users.id) | NOT NULL, indexed, CASCADE delete |
| plan_type | String | NOT NULL |
| payment_provider | String | Nullable |
| provider_customer_id | String | Nullable |
| provider_subscription_id | String | Nullable |
| status | String | NOT NULL |
| created_at | DateTime (tz) | Auto-set |
| updated_at | DateTime (tz) | Auto-updated |

### TranslationCache (`translation_cache` table)
| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID (PK) | Auto-generated, unique |
| source_text | Text | NOT NULL, indexed |
| source_language | String | NOT NULL |
| target_language | String | NOT NULL |
| translated_text | Text | NOT NULL |
| provider_name | String | Nullable |
| created_at | DateTime (tz) | Auto-set |

---

## Security

- **Passwords** are hashed using **Argon2** (via `passlib`) — the most secure password hashing algorithm available
- **JWT tokens** are signed with HMAC-SHA256 using a secret key
- **Cookies** are `HttpOnly` (inaccessible to JavaScript) — mitigates XSS attacks
- **SameSite=lax** — provides CSRF protection
- **Secure flag** — enabled only in production (`ENVIRONMENT=production`)
- **CORS** is configured to allow specific frontend origins
- **Rate limiting** — protects auth endpoints from brute-force attacks
- **Bearer token support** — allows API clients to authenticate without cookies

---

## Running Tests

Tests use the **same PostgreSQL database** as development (with cleanup after each test).

```bash
# Run all tests
pytest app/tests/ -v

# Run only auth tests
pytest app/tests/test_auth.py -v

# Run with short traceback
pytest app/tests/ -v --tb=short
```

### What Gets Tested

#### Auth Tests (`test_auth.py`)
- ✅ Register a new user
- ✅ Register with duplicate email (should fail)
- ✅ Login with correct credentials (sets cookie)
- ✅ Login with wrong password (should fail 401)
- ✅ Login with non-existent user (should fail 401)
- ✅ Get current user when authenticated
- ✅ Get current user without auth (should fail 401)
- ✅ Logout (clears cookie)
- ✅ Login sets HttpOnly cookie
- ✅ Register with invalid email (validation error 422)
- ✅ Register with missing password (validation error 422)
- ✅ Password is stored as hash, not plain text

---

## Common Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Run development server
uvicorn app.main:app --reload

# Run tests
pytest app/tests/ -v

# Create migration after model changes
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Check migration status
alembic current

# Run seed data
python3 -m app.seeds.seed