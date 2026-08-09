from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.ratelimit import limiter
from app.core.response import success_response
from app.schemas.project import ProjectCreate
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


@router.post("")
@limiter.limit("30/minute")
def create_project_endpoint(
    request: Request,
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = create_project(db=db, project_data=project_data, user=current_user)
    return success_response(
        message="Project created successfully",
        data={
            "id": str(project.id),
            "name": project.name,
            "original_file_name": project.original_file_name,
            "source_language": project.source_language,
            "target_language": project.target_language,
            "status": project.status,
            "created_at": project.created_at.isoformat() if project.created_at else None,
            "updated_at": project.updated_at.isoformat() if project.updated_at else None,
        },
    )


@router.get("")
def list_projects(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    projects = get_user_projects(db=db, user_id=current_user.id)
    return success_response(
        message="Projects fetched successfully",
        data=[
            {
                "id": str(p.id),
                "name": p.name,
                "original_file_name": p.original_file_name,
                "source_language": p.source_language,
                "target_language": p.target_language,
                "status": p.status,
                "created_at": p.created_at.isoformat() if p.created_at else None,
                "updated_at": p.updated_at.isoformat() if p.updated_at else None,
            }
            for p in projects
        ],
    )


@router.get("/{project_id}")
def get_project(
    request: Request,
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from uuid import UUID
    project = get_project_by_id(db=db, project_id=UUID(project_id), user_id=current_user.id)
    return success_response(
        message="Project fetched successfully",
        data={
            "id": str(project.id),
            "name": project.name,
            "original_file_name": project.original_file_name,
            "source_language": project.source_language,
            "target_language": project.target_language,
            "status": project.status,
            "created_at": project.created_at.isoformat() if project.created_at else None,
            "updated_at": project.updated_at.isoformat() if project.updated_at else None,
        },
    )