from app.models.subtitle_file import SubtitleFile


def seed_subtitle_files(db, projects):
    subtitle_files = [
        SubtitleFile(
            project_id=projects[0].id,
            file_type="srt",
            source_language="en",
            target_language="hi",
            original_file_path="uploads/subtitles/moneyheist.srt",
            translated_file_path=None,
            status="uploaded",
        ),
        SubtitleFile(
            project_id=projects[1].id,
            file_type="srt",
            source_language="en",
            target_language="es",
            original_file_path="uploads/subtitles/narcos.srt",
            translated_file_path="uploads/subtitles/narcos_es.srt",
            status="translated",
        ),
    ]

    db.add_all(subtitle_files)
    db.commit()

    return subtitle_files