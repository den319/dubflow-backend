import pysrt


def parse_srt_file(file_path: str):
    subtitles = pysrt.open(file_path)

    parsed_entries = []

    for subtitle in subtitles:
        print("subtitle: ", subtitle)
        
        parsed_entries.append(
            {
                "sequence_number": subtitle.index,
                "start_time": str(subtitle.start),
                "end_time": str(subtitle.end),
                "original_text": subtitle.text,
            }
        )

    return parsed_entries