"""Quick integration test: document ingestion + analysis."""

from pathlib import Path

from src.document_ingestion.data_ingestion import load_pdfs
from src.document_analyzer.data_analysis import DocumentAnalyzer


DATA_DIR = Path("data/document_analyzer")
MAX_TEST_CHARS = 12000


def main() -> None:
	try:
		print("Starting PDF ingestion...")
		documents = load_pdfs(DATA_DIR)
		print(f"Total page documents loaded: {len(documents)}")

		if not documents:
			print("No documents loaded. Exiting test.")
			return

		print("Starting metadata analysis...")
		analyzer = DocumentAnalyzer()

		# Group loaded pages by source PDF path.
		sources = sorted({str(d.metadata.get("source", "")) for d in documents if d.metadata.get("source")})
		print(f"PDF sources to analyze: {len(sources)}")

		for src in sources:
			src_docs = [d for d in documents if str(d.metadata.get("source", "")) == src]
			text_content = "\n".join(d.page_content for d in src_docs)[:MAX_TEST_CHARS]

			print("\n" + "=" * 60)
			print(f"Source PDF: {src}")
			print(f"Extracted text length for analysis: {len(text_content)} chars")

			analysis_result = analyzer.analyze_document(text_content)

			print("=== METADATA ANALYSIS RESULT ===")
			for key, value in analysis_result.items():
				print(f"{key}: {value}")

	except Exception as e:
		print(f"Test failed: {e}")


if __name__ == "__main__":
	main()

