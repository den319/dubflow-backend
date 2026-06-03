from app.models.subtitle_entry import SubtitleEntry


def seed_subtitle_entries(db, subtitle_files):
    entries = [
        SubtitleEntry(
            subtitle_file_id=subtitle_files[0].id,
            sequence_number=1,
            start_time="00:00:01,000",
            end_time="00:00:03,000",
            original_text="Hello Professor",
            translated_text="नमस्ते प्रोफेसर",
            translation_status="completed",
        ),
        SubtitleEntry(
            subtitle_file_id=subtitle_files[0].id,
            sequence_number=2,
            start_time="00:00:04,000",
            end_time="00:00:06,000",
            original_text="How are you?",
            translated_text="आप कैसे हैं?",
            translation_status="completed",
        ),
    ]

    db.add_all(entries)
    db.commit()

    return entries