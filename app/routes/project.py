from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.ratelimit import limiter
from app.schemas.project import ProjectCreate, ProjectResponse
from app.services.project_service import (
    create_project,
    get_user_projects,
    get_project_by_id,
)
from app.services.auth_service import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@router.post("", response_model=ProjectResponse, status_code=201)
@limiter.limit("30/minute")
def create_project_endpoint(
    request: Request,
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_project(db=db, project_data=project_data, user=current_user)


@router.get("", response_model=list[ProjectResponse])
def list_projects(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_projects(db=db, user_id=current_user.id)


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    request: Request,
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from uuid import UUID
    return get_project_by_id(db=db, project_id=UUID(project_id), user_id=current_user.id)
