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
from app.models.user import User

from app.services.subtitle_service import (
    upload_subtitle_service,
)
from app.services.auth_service import get_current_user
from fastapi.responses import FileResponse

router = APIRouter(
    prefix="/subtitles",
    tags=["Subtitles"],
)


@router.post("/upload-subtitle")
def upload_subtitle(
    source_language: str = Form(...),
    target_language: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not file.filename.endswith(".srt"):
        raise HTTPException(
            status_code=400,
            detail="Only .srt files are allowed",
        )

    print(current_user)

    result = upload_subtitle_service(
        db=db,
        user=current_user,
        source_language=source_language,
        target_language=target_language,
        file=file,
    )

    translated_file_path = result["translated_file_path"]

    return FileResponse(
        path=translated_file_path,
        media_type="application/octet-stream",
        filename="translated.srt",
    )
