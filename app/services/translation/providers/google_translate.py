from deep_translator import GoogleTranslator


def translate_text(
    text: str,
    source_language: str,
    target_language: str,
) -> str:
    translated = GoogleTranslator(
        source=source_language,
        target=target_language,
    ).translate(text)

    return translated


def translate_multiple_texts(
    texts: list[str],
    source_language: str,
    target_language: str,
) -> list[str]:
    """Translate a list of texts in a single API call (batch translation)."""
    if not texts:
        return []

    translated = GoogleTranslator(
        source=source_language,
        target=target_language,
    ).translate_batch(texts)

    return translated