import os
import pysrt
from app.core.config import settings




def generate_translated_srt(
    subtitle_entries,
    output_filename: str,
):
    os.makedirs(settings.OUTPUT_DIR, exist_ok=True)

    subtitles = pysrt.SubRipFile()

    for entry in subtitle_entries:
        subtitle = pysrt.SubRipItem(
            index=entry.sequence_number,
            start=pysrt.SubRipTime.from_string(entry.start_time),
            end=pysrt.SubRipTime.from_string(entry.end_time),
            text=entry.translated_text or entry.original_text,
        )

        subtitles.append(subtitle)

    output_path = os.path.join(
        settings.OUTPUT_DIR,
        output_filename,
    )

    subtitles.save(
        output_path,
        encoding="utf-8",
    )

    return output_path