"""Basic document analysis utilities."""


def analyze_document(text: str) -> dict:
    """Return simple analysis stats for input text."""
    words = text.split()
    return {
        "word_count": len(words),
        "char_count": len(text),
    }
