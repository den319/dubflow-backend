import os
import uuid

from fastapi import UploadFile


UPLOAD_DIR = "uploads/subtitles"


def save_subtitle_file(file: UploadFile):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    extension = file.filename.split(".")[-1]
    filename= file.filename.split(".")[0]

    unique_filename = f"{filename}-{uuid.uuid4()}.{extension}"

    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    return {
        "original_filename": file.filename,
        "stored_filename": unique_filename,
        "file_path": file_path,
        "extension": extension,
    }