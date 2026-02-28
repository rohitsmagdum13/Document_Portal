"""
app.py
-------
FastAPI backend for the Document Portal.
"""

from fastapi import FastAPI

# Create the FastAPI application
app = FastAPI(title="Document Portal", version="0.1.0")


@app.get("/")
def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "Document Portal is running"}


# Run with:  uvicorn app:app --reload
