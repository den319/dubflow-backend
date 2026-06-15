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