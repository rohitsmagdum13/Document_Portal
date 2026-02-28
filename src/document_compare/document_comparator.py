"""Simple document comparison utilities."""


def compare_documents(text_a: str, text_b: str) -> dict:
    """Compare two documents by basic size metrics."""
    return {
        "doc_a_chars": len(text_a),
        "doc_b_chars": len(text_b),
        "same_length": len(text_a) == len(text_b),
    }
