"""Load PDFs from a directory into LangChain Documents."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import hashlib
import re
import shutil
import uuid

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

from exception.custom_exception import DocumentPortalException
from logger.custom_logger import CustomLogger


log = CustomLogger().get_logger(__file__)


def _safe_name(name: str) -> str:
    """Make a filesystem-safe, lowercase name fragment."""
    clean = re.sub(r"[^a-zA-Z0-9_-]+", "_", name).strip("_")
    return clean.lower() or "document"


def create_pdf_session_id(pdf_path: Path) -> str:
    """Create session id per PDF.

    Pattern (industry-style):
    YYYYMMDDTHHMMSSZ__<file_stem>__<8hex>
    """
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    stem = _safe_name(pdf_path.stem)
    uid = uuid.uuid4().hex[:8]
    return f"{ts}__{stem}__{uid}"


def _file_sha256(path: Path) -> str:
    """Return SHA-256 hash for a file."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def create_session_artifacts(data_dir: str | Path, pdf_path: Path) -> tuple[str, Path, Path, bool]:
    """Create or reuse one session file for a source PDF.

    Returns
    -------
    tuple[str, Path, Path, bool]
        session_id, session_dir, session_file, reused_existing
    """
    root = Path(data_dir)
    if not root.is_absolute():
        root = Path.cwd() / root

    sessions_root = root / "sessions"
    sessions_root.mkdir(parents=True, exist_ok=True)

    src_hash = _file_sha256(pdf_path)

    # Reuse previously-versioned file if same name + same content hash.
    for existing in sessions_root.glob(f"*/{pdf_path.name}"):
        try:
            if _file_sha256(existing) == src_hash:
                return existing.parent.name, existing.parent, existing, True
        except Exception:
            continue

    session_id = create_pdf_session_id(pdf_path)
    session_dir = sessions_root / session_id
    session_dir.mkdir(parents=True, exist_ok=True)

    copied_file = session_dir / pdf_path.name
    shutil.copy2(pdf_path, copied_file)

    return session_id, session_dir, copied_file, False


def get_pdf_files(data_dir: str | Path = "data/document_analyzer") -> list[Path]:
    """Return all PDF paths from a directory (recursive)."""
    try:
        root = Path(data_dir)

        # Use absolute path for stable logging and loading.
        if not root.is_absolute():
            root = Path.cwd() / root

        # Validate input directory.
        if not root.exists() or not root.is_dir():
            raise FileNotFoundError(f"Directory not found: {root}")

        # Ignore archived version files under data_dir/sessions.
        pdfs = sorted(p for p in root.rglob("*.pdf") if "sessions" not in p.relative_to(root).parts)
        log.info("Discovered PDF files", directory=str(root), count=len(pdfs))
        return pdfs
    except Exception as e:
        log.error("Failed to discover PDF files", directory=str(data_dir), error=str(e))
        raise DocumentPortalException(f"Failed to get PDF files from: {data_dir}", e) from e


def enrich_metadata(doc: Document, data_dir: str | Path = "data/document_analyzer", session_id: str | None = None, session_file: str | None = None, session_dir: str | None = None) -> Document:
    """Add structured metadata fields to one document."""
    src = Path(str(doc.metadata.get("source", "")))
    base = Path(data_dir)

    if not base.is_absolute():
        base = Path.cwd() / base

    # Convert loader page index (0-based) to human-friendly 1-based.
    page = doc.metadata.get("page")
    pg_no = (int(page) + 1) if isinstance(page, int) else None

    # Build relative path if source is inside base dir.
    try:
        rel = str(src.relative_to(base)) if src else ""
    except Exception:
        rel = src.name if src else ""

    doc.metadata.update({"file_name": src.name, "file_stem": src.stem, "file_extension": src.suffix.lower(), "absolute_path": str(src), "relative_path": rel, "page_number": pg_no, "loaded_at_utc": datetime.now(timezone.utc).isoformat(), "session_id": session_id, "session_dir": session_dir, "session_file": session_file})
    return doc


def load_pdfs(data_dir: str | Path = "data/document_analyzer") -> list[Document]:
    """Load PDFs and create one session folder per PDF file."""
    try:
        root = Path(data_dir)
        if not root.is_absolute():
            root = Path.cwd() / root

        # Reuse file discovery for validation + logging.
        pdfs = get_pdf_files(root)
        if not pdfs:
            log.info("No PDF files found", directory=str(root))
            return []

        all_docs: list[Document] = []

        for pdf in pdfs:
            sid, sdir, sfile, reused = create_session_artifacts(root, pdf)

            log.info("Loading PDF", source_pdf=str(pdf), session_id=sid, session_dir=str(sdir), session_file=str(sfile), reused_session_file=reused)

            loader = PyPDFLoader(str(pdf))
            docs = loader.load()

            docs = [enrich_metadata(doc, root, session_id=sid, session_dir=str(sdir), session_file=str(sfile)) for doc in docs]
            all_docs.extend(docs)

            log.info("PDF processed", source_pdf=str(pdf), pages=len(docs), session_id=sid)

        log.info("PDF loading completed", directory=str(root), files=len(pdfs), documents=len(all_docs))
        return all_docs
    except Exception as e:
        log.error("Failed to load PDFs", directory=str(data_dir), error=str(e))
        raise DocumentPortalException(f"Failed to load PDFs from: {data_dir}", e) from e


# if __name__ == "__main__":
#     target_dir = "data/document_analyzer"
#     print("\n" + "=" * 60)
#     print("DOCUMENT INGESTION TEST")
#     print("=" * 60)
#     print(f"Directory: {target_dir}")

#     try:
#         documents = load_pdfs(target_dir)
#         print(f"Documents loaded: {len(documents)}")

#         if documents:
#             first = documents[0]
#             print("-" * 60)
#             print("First document metadata:")
#             print(first.metadata)
#             print("-" * 60)
#             preview = first.page_content[:250].replace("\n", " ").strip()
#             print(f"Preview: {preview}...")
#             print(f"Session ID  : {first.metadata.get('session_id')}")
#             print(f"Session Dir : {first.metadata.get('session_dir')}")
#             print(f"Session File: {first.metadata.get('session_file')}")

#         print("=" * 60)
#         print("TEST COMPLETED")
#         print("=" * 60 + "\n")
#     except Exception as ex:
#         print(f"Test failed: {ex}")

