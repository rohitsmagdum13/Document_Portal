"""Simple document ingestion helpers."""


def ingest_document(file_name: str) -> dict:
    """Return minimal ingestion response for a file."""
    return {
        "status": "ingested",
        "file_name": file_name,
    }
