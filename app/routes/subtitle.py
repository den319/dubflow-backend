from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    Form,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.services.subtitle_service import (
    upload_subtitle_service,
)

router = APIRouter(
    prefix="/subtitles",
    tags=["Subtitles"],
)


@router.post("/upload")
def upload_subtitle(
    project_id: UUID = Form(...),
    source_language: str = Form(...),
    target_language: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # Validate extension
    if not file.filename.endswith(".srt"):
        raise HTTPException(
            status_code=400,
            detail="Only .srt files are allowed",
        )

    subtitle_file = upload_subtitle_service(
        db=db,
        project_id=project_id,
        source_language=source_language,
        target_language=target_language,
        file=file,
    )

    return {
        "message": "Subtitle uploaded successfully",
        "subtitle_file_id": subtitle_file.id,
        "total_entries": subtitle_file.total_entries,
    }