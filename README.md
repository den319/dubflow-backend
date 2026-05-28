# Dubflow Backend

A FastAPI backend for subtitle translation with authentication, project management, and subscription handling.

## Tech Stack

| Technology | Purpose |
|-----------|---------|
| **FastAPI** | Web framework — automatically generates OpenAPI docs |
| **PostgreSQL** | Database — production-grade relational database |
| **SQLAlchemy** | ORM — maps Python classes to database tables |
| **Alembic** | Database migrations — tracks schema changes |
| **bcrypt** | Password hashing — securely stores user passwords |
| **JWT (python-jose)** | Token-based authentication — stateless auth via signed tokens |
| **Pydantic** | Data validation — ensures request/response data integrity |
| **Uvicorn** | ASGI server — runs the FastAPI application |

## Project Structure

```
dubflow-backend/
├── alembic/                    # Database migration files
│   ├── versions/
│   │   └── d9327dc876a2_initial_migration.py
│   ├── env.py
│   └── script.py.mako
├── app/
│   ├── core/                   # Core setup
│   │   ├── config.py           # App config from .env
│   │   ├── database.py         # DB connection, session, Base
│   │   └── security.py         # Password hashing + JWT creation
│   ├── models/                 # SQLAlchemy ORM models
│   │   ├── user.py             # User model (UUID primary key)
│   │   ├── project.py          # Project model
│   │   ├── subtitle.py         # Subtitle model
│   │   └── subscription.py     # Subscription model
│   ├── routes/                 # API endpoints
│   │   ├── auth.py             # Auth endpoints (register, login, me, logout)
│   │   └── health.py           # Health check
│   ├── schemas/                # Pydantic request/response models
│   │   └── user.py             # UserCreate, UserResponse, LoginRequest
│   ├── services/               # Business logic layer
│   │   └── auth_service.py     # Auth logic + get_current_user dependency
│   ├── tests/                  # Unit tests
│   │   ├── conftest.py         # Test fixtures (DB, client)
│   │   ├── test_health.py      # Health endpoint tests
│   │   └── test_auth.py        # Auth endpoint tests
│   └── main.py                 # FastAPI app entry point
├── .env                        # Environment variables (gitignored)
├── alembic.ini                 # Alembic config
├── requirements.txt            # Python dependencies
├── start.sh                    # Quick start script
└── README.md
```

## Prerequisites

- Python 3.10+
- PostgreSQL
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
```

> **Note:** The `SECRET_KEY` is used to sign JWT tokens. Generate a strong one for production (`openssl rand -hex 32`).

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
# Using the script
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

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/health` | Health check → `{"status": "ok"}` |

### Authentication

All auth endpoints are prefixed with `/auth`.

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
    "id": "uuid-string",
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

#### Login
```http
POST /auth/login
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "securepassword"
}
```

**Response** `200 OK` (sets `access_token` as HttpOnly cookie):
```json
{
    "message": "Login successful"
}
```

The JWT token is stored in an HttpOnly cookie (`access_token`) with:
- `HttpOnly` — JavaScript cannot read it (XSS protection)
- `SameSite=lax` — CSRF protection
- `Max-Age` — based on `ACCESS_TOKEN_EXPIRE_MINUTES`

#### Get Current User
```http
GET /auth/me
Cookie: access_token=<token>
```

**Response** `200 OK`:
```json
{
    "id": "uuid-string",
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

## Authentication Flow

```
                  REGISTER                    LOGIN
                  ─────────                   ─────
Client                    Server     Client                    Server
  │                         │         │                         │
  │ POST /auth/register    │         │ POST /auth/login        │
  │ {email, username, pw}  │         │ {email, password}       │
  │───────────────────────>│         │────────────────────────>│
  │                         │         │                         │
  │                 1. Hash password │                 1. Find user
  │                 2. Save to DB    │                 2. Verify password
  │                 3. Return user   │                 3. Create JWT
  │                         │         │                 4. Set HttpOnly cookie
  │ {id, email, username}  │         │                         │
  │<───────────────────────│         │ ← Set-Cookie: access_token=...
  │                         │         │ {message: "Login successful"}
  │                         │         │<────────────────────────│


                   AUTHENTICATED REQUEST
                   ─────────────────────
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
  │ {id, email, username}         │  ← Returns user or 401
  │<──────────────────────────────│
```

## Running Tests

Tests use the **same PostgreSQL database** as development (with cleanup after each test).

```bash
# Run all tests
pytest app/tests/ -v

# Run only auth tests
pytest app/tests/test_auth.py -v

# Run with coverage
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

## Database Models

### User (`user` table)
| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID (PK) | Auto-generated |
| email | String | Unique, indexed, NOT NULL |
| username | String | Unique, indexed, NOT NULL |
| hashed_password | String | NOT NULL |
| is_active | Boolean | Default: true |
| created_at | DateTime | Auto-set |
| updated_at | DateTime | Auto-updated |

### Project (`projects` table)
| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer (PK) | Auto-increment |
| user_id | Integer (FK → users.id) | NOT NULL |
| video_name | String | NOT NULL |
| source_language | String | NOT NULL |
| target_language | String | NOT NULL |
| status | String | Default: "pending" |
| created_at | DateTime | Auto-set |
| updated_at | DateTime | Auto-updated |

### Subtitle (`subtitles` table)
| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer (PK) | Auto-increment |
| project_id | Integer (FK → projects.id) | NOT NULL |
| original_subtitle_file | String | NOT NULL |
| translated_subtitle_file | String | Nullable |
| created_at | DateTime | Auto-set |
| updated_at | DateTime | Auto-updated |

### Subscription (`subscriptions` table)
| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer (PK) | Auto-increment |
| user_id | Integer (FK → users.id) | NOT NULL |
| plan_type | String | NOT NULL |
| stripe_customer_id | String | Nullable |
| status | String | Default: "active" |
| created_at | DateTime | Auto-set |
| updated_at | DateTime | Auto-updated |

## Security

- **Passwords** are hashed using **bcrypt** (via `passlib`) — never stored in plain text
- **JWT tokens** are signed with HMAC-SHA256 using a secret key
- **Cookies** are `HttpOnly` (inaccessible to JavaScript) — mitigates XSS attacks
- **SameSite=lax** — provides CSRF protection
- **CORS** is configured to allow specific frontend origins

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