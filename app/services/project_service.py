from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.project import Project
from app.models.subtitle_file import SubtitleFile
from app.models.user import User
from app.schemas.project import ProjectCreate


def create_project(
    db: Session,
    project_data: ProjectCreate,
    user: User,
) -> Project:
    project = Project(
        user_id=user.id,
        name=project_data.name,
        original_file_name=None,
        source_language=project_data.source_language,
        target_language=project_data.target_language,
        status="pending",
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def get_user_projects(db: Session, user_id: UUID) -> list[Project]:
    return (
        db.query(Project)
        .filter(Project.user_id == user_id)
        .order_by(Project.created_at.desc())
        .all()
    )


def get_project_by_id(db: Session, project_id: UUID, user_id: UUID) -> Project:
    project = (
        db.query(Project)
        .filter(Project.id == project_id, Project.user_id == user_id)
        .first()
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


def update_project_after_upload(
    db: Session,
    project_id: UUID,
    original_file_name: str,
    subtitle_file: SubtitleFile,
) -> Project:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project.original_file_name = original_file_name
    project.status = "processing"
    db.commit()
    db.refresh(project)
    return project