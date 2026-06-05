from uuid import UUID

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.services.translation.translation_service import (
    translate_subtitle_entries,
)

router = APIRouter(
    prefix="/translations",
    tags=["Translations"],
)


@router.post("/{subtitle_file_id}")
def translate_subtitles(
    subtitle_file_id: UUID,
    source_language: str,
    target_language: str,
    db: Session = Depends(get_db),
):
    result = translate_subtitle_entries(
        db=db,
        subtitle_file_id=subtitle_file_id,
        source_language=source_language,
        target_language=target_language,
    )

    return result