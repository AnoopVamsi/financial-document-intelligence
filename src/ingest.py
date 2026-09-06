from pathlib import Path
import fitz  # PyMuPDF

from src.config import RAW_DATA_DIR


def extract_pdf_pages(pdf_path: Path) -> list[dict]:
    """Extract readable text and page metadata from one PDF file."""

    document = fitz.open(pdf_path)
    pages = []

    for page_number, page in enumerate(document, start=1):
        text = page.get_text("text").strip()

        if text:
            pages.append(
                {
                    "document_name": pdf_path.name,
                    "page_number": page_number,
                    "text": text,
                }
            )

    document.close()
    return pages


def ingest_all_pdfs() -> list[dict]:
    """Read all PDF files from data/raw and return page-level records."""

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    all_pages = []

    for pdf_path in RAW_DATA_DIR.glob("*.pdf"):
        pages = extract_pdf_pages(pdf_path)
        all_pages.extend(pages)

        print(f"Processed {pdf_path.name}: {len(pages)} pages with text")

    return all_pages


if __name__ == "__main__":
    records = ingest_all_pdfs()
    print(f"\nTotal extracted pages: {len(records)}")