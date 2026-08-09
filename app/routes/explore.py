from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.ratelimit import limiter
from app.core.response import success_response
from app.models.user import User
from app.services.auth_service import get_current_user
from app.services.explore_service import get_explore_data

router = APIRouter(tags=["Explore"])


def get_optional_user(
    request: Request,
    db: Session = Depends(get_db),
) -> User | None:
    """Return the current user if authenticated, otherwise None."""
    try:
        return get_current_user(request, db)
    except Exception:
        return None


@router.get("/explore")
@limiter.limit("30/minute")
def explore(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_user),
):
    data = get_explore_data(db, current_user)
    return success_response(message="Explore data fetched successfully", data=data)