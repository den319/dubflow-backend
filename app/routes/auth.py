from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.config import settings
from app.core.ratelimit import limiter
from app.core.response import success_response
from app.core.security import create_access_token
from app.schemas.user import UserCreate, LoginRequest
from app.services.auth_service import (
    create_user,
    authenticate_user,
    get_current_user,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
@limiter.limit("5/minute")
def register(
    request: Request,
    user: UserCreate,
    db: Session = Depends(get_db),
):
    db_user = create_user(db, user)
    return success_response(
        message="User registered successfully",
        data={
            "id": str(db_user.id),
            "email": db_user.email,
            "username": db_user.username,
            "avatar_url": db_user.avatar_url,
        },
    )


@router.post("/login")
@limiter.limit("10/minute")
def login(
    request: Request,
    payload: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, payload.email, payload.password)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    access_token = create_access_token(
        data={"sub": user.email}
    )

    is_production = settings.ENVIRONMENT == "production"

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=is_production,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

    return success_response(
        message="Login successful",
        data={
            "access_token": access_token,
            "token_type": "bearer",
        },
    )


@router.get("/me")
def me(current_user=Depends(get_current_user)):
    return success_response(
        message="User fetched successfully",
        data={
            "id": str(current_user.id),
            "email": current_user.email,
            "username": current_user.username,
            "avatar_url": current_user.avatar_url,
        },
    )


@router.post("/logout")
def logout(response: Response):
    is_production = settings.ENVIRONMENT == "production"

    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=is_production,
        samesite="lax",
    )

    return success_response(message="Logged out successfully")