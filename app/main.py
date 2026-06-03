from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.routes import health, auth, subtitle

app = FastAPI(title=settings.APP_NAME)

# CORS middleware — required for cookies to work with frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Frontend URLs
    allow_credentials=True,  # Required for cookies
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(subtitle.router)


@app.on_event("startup")
def on_startup():
    """Create database tables on startup."""
    try:
        Base.metadata.create_all(bind=engine)
        print("✓ Database tables created successfully")
    except Exception as e:
        print(f"⚠ Database connection failed: {e}")
        print("  The server will still start, but DB features won't work.")


@app.get("/")
def root():
    return {"message": f"Welcome to {settings.APP_NAME}"}