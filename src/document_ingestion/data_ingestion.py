"""Simple document ingestion helpers – save, read and list PDFs per session."""

import os
import uuid
from pathlib import Path

import fitz

from exception.custom_exception import DocumentPortalException
from logger.custom_logger import CustomLogger


class DocumentHandler:
    """Session-scoped PDF manager with structured logging.

    Creates: <base_dir>/<session_id>/*.pdf
    """

    def __init__(self, base_dir: str = "data/document_analyzer", session_id: str | None = None):
        self.base_dir = Path(os.getcwd()) / base_dir
        self.session_id = session_id or uuid.uuid4().hex[:12]
        self.session_path = self.base_dir / self.session_id
        self.session_path.mkdir(parents=True, exist_ok=True)
        self.log = CustomLogger().get_logger(__file__)
        self.log.info("Session initialised", session_path=str(self.session_path), session_id=self.session_id)

    # ── Save PDF ──────────────────────────────────────────────────────
    def save_pdf(self, uploaded_file) -> str:
        """Save an uploaded/file-like PDF to the session directory."""
        try:
            filename = os.path.basename(uploaded_file.name)
            if not filename.lower().endswith(".pdf"):
                raise ValueError("Invalid file type. Only PDFs are allowed.")
            save_path = os.path.join(self.session_path, filename)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.read() if hasattr(uploaded_file, "read") else uploaded_file.getbuffer())
            self.log.info("PDF saved successfully", file=filename, save_path=save_path, session_id=self.session_id)
            return save_path
        except Exception as e:
            self.log.error("Failed to save PDF", error=str(e), session_id=self.session_id)
            raise DocumentPortalException(f"Failed to save PDF: {e}", e) from e

    # ── Read PDF ──────────────────────────────────────────────────────
    def read_pdf(self, pdf_path: str) -> str:
        """Extract all text from a PDF, page by page."""
        try:
            with fitz.open(pdf_path) as doc:
                chunks = [f"\n--- Page {i + 1} ---\n{doc.load_page(i).get_text()}" for i in range(doc.page_count)]  # type: ignore
            text = "\n".join(chunks)
            self.log.info("PDF read successfully", pdf_path=pdf_path, session_id=self.session_id, pages=len(chunks))
            return text
        except Exception as e:
            self.log.error("Failed to read PDF", error=str(e), pdf_path=pdf_path, session_id=self.session_id)
            raise DocumentPortalException(f"Could not process PDF: {pdf_path}", e) from e

    # ── List PDFs ─────────────────────────────────────────────────────
    def list_pdfs(self) -> list[str]:
        """Return sorted names of all PDFs in the session folder."""
        pdfs = sorted(f.name for f in self.session_path.iterdir() if f.is_file() and f.suffix.lower() == ".pdf")
        self.log.info("Listed PDFs in session", count=len(pdfs), session_id=self.session_id)
        return pdfs

    # ── Helpers ───────────────────────────────────────────────────────
    def get_pdf_path(self, file_name: str) -> Path:
        """Return absolute path for a PDF name (does not check existence)."""
        if not file_name.lower().endswith(".pdf"):
            file_name += ".pdf"
        return self.session_path / file_name

    def __repr__(self) -> str:
        return f"DocumentHandler(base_dir='{self.base_dir}', session_id='{self.session_id}')"


# ══════════════════════════════════════════════════════════════════════ #
#  CLI test – run with: python -m src.document_ingestion.data_ingestion #
# ══════════════════════════════════════════════════════════════════════ #
if __name__ == "__main__":
    from datetime import datetime, timezone

    LINE = "═" * 60
    THIN = "─" * 60
    source_dir = Path(os.getcwd()) / "data" / "document_analyzer"
    pdf_files = sorted(f for f in source_dir.iterdir() if f.is_file() and f.suffix.lower() == ".pdf")

    print(f"\n{LINE}")
    print("  DOCUMENT HANDLER — INGESTION TEST")
    print(f"{LINE}")
    print(f"  Source directory : {source_dir}")
    print(f"  PDFs found       : {len(pdf_files)}")
    print(LINE)

    if not pdf_files:
        print("  ⚠  No PDFs found. Nothing to ingest.")
    else:
        for pdf_path in pdf_files:
            date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            safe_name = pdf_path.stem.replace(" ", "_")
            session_id = f"{date_str}_{safe_name}"

            handler = DocumentHandler(session_id=session_id)

            with open(pdf_path, "rb") as fh:
                saved_path = handler.save_pdf(fh)

            text = handler.read_pdf(saved_path)
            page_count = text.count("--- Page")

            print(f"\n  {THIN}")
            print(f"  FILE        : {pdf_path.name}")
            print(f"  SESSION ID  : {handler.session_id}")
            print(f"  SESSION DIR : {handler.session_path}")
            print(f"  SAVED TO    : {saved_path}")
            print(f"  PAGES       : {page_count}")
            print(f"  TEXT PREVIEW : {text[:200].strip()}...")
            print(f"  PDFs IN DIR : {handler.list_pdfs()}")
            print(f"  {THIN}")

    print(f"\n{LINE}")
    print("  DONE")
    print(f"{LINE}\n")