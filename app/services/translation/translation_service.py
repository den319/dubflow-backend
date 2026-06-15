import uuid

from sqlalchemy.orm import Session

from app.models.subtitle_entry import SubtitleEntry
from app.models.subtitle_file import SubtitleFile

from app.services.translation.providers.google_translate import (
    translate_multiple_texts,
)

from app.services.generators.srt_generator import (
    generate_translated_srt,
)


def translate_subtitle_entries(
    db: Session,
    subtitle_file_id,
    source_language: str,
    target_language: str,
):
    entries = (
        db.query(SubtitleEntry)
        .filter(
            SubtitleEntry.subtitle_file_id == subtitle_file_id
        )
        .order_by(SubtitleEntry.sequence_number)
        .all()
    )

    if not entries:
        return {
            "translated_entries": 0,
            "translated_file_path": None,
        }

    # Collect all original texts for batch translation
    original_texts = [entry.original_text for entry in entries]

    # Translate all texts in a single API call
    translated_texts = translate_multiple_texts(
        texts=original_texts,
        source_language=source_language,
        target_language=target_language,
    )

    # Assign translated texts back to entries
    for entry, translated_text in zip(entries, translated_texts):
        entry.translated_text = translated_text
        entry.translation_status = "completed"

    db.commit()

    # Generate translated SRT
    output_filename = f"{uuid.uuid4()}.srt"

    translated_file_path = generate_translated_srt(
        subtitle_entries=entries,
        output_filename=output_filename,
    )

    # Update subtitle_file record
    subtitle_file = (
        db.query(SubtitleFile)
        .filter(SubtitleFile.id == subtitle_file_id)
        .first()
    )

    subtitle_file.translated_file_path = translated_file_path
    subtitle_file.status = "translated"

    db.commit()

    return {
        "translated_entries": len(entries),
        "translated_file_path": translated_file_path,
    }