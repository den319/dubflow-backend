from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.subtitle_file import SubtitleFile
from app.models.subtitle_entry import SubtitleEntry
from app.models.user import User

from app.services.storage_service import save_subtitle_file
from app.utils.subtitle_parser import parse_srt_file
from app.services.translation.translation_service import (
    translate_subtitle_entries,
)


def upload_subtitle_service(
    db: Session,
    user: User,
    source_language,
    target_language,
    file,
):
    # Save physical file
    saved_file = save_subtitle_file(file)

    # Auto-create project from the uploaded file
    project_name = file.filename.replace(".srt", "") if file.filename else "Untitled Project"
    project = Project(
        user_id=user.id,
        name=project_name,
        original_file_name=file.filename,
        source_language=source_language,
        target_language=target_language,
        status="processing",
    )
    db.add(project)
    db.flush()

    # Parse subtitles
    parsed_entries = parse_srt_file(
        saved_file["file_path"]
    )

    # Create subtitle file record linked to the project
    subtitle_file = SubtitleFile(
        project_id=project.id,
        file_type=saved_file["extension"],
        source_language=source_language,
        target_language=target_language,
        original_file_path=saved_file["file_path"],
        total_entries=len(parsed_entries),
        translated_entries=0,
        status="uploaded",
    )

    db.add(subtitle_file)
    db.flush()

    subtitle_entries = []

    # Create subtitle entries
    for entry in parsed_entries:
        subtitle_entry = SubtitleEntry(
            subtitle_file_id=subtitle_file.id,
            sequence_number=entry["sequence_number"],
            start_time=entry["start_time"],
            end_time=entry["end_time"],
            original_text=entry["original_text"],
            translation_status="pending",
        )

        subtitle_entries.append(subtitle_entry)

    db.add_all(subtitle_entries)

    db.commit()

    translation_result = translate_subtitle_entries(
        db=db,
        subtitle_file_id=subtitle_file.id,
        source_language=source_language,
        target_language=target_language,
    )

    return {
        "subtitle_file": subtitle_file,
        "translated_file_path": translation_result["translated_file_path"],
    }