import requests
from app.core.config import settings


def translate_text(
    text: str,
    source_language: str,
    target_language: str,
):
    payload = {
        "q": text,
        "source": source_language,
        "target": target_language,
        "format": "text",
    }
    
    response = requests.post(
        settings.LIBRETRANSLATE_URL,
        json=payload,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    return data["translatedText"]