from src.config import CHUNK_OVERLAP, CHUNK_SIZE


def split_text(text: str) -> list[str]:
    """Split text into overlapping character-based chunks."""

    chunks = []
    start = 0

    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


def create_chunks(page_records: list[dict]) -> list[dict]:
    """Create searchable chunks while preserving source metadata."""

    chunk_records = []

    for page in page_records:
        text_chunks = split_text(page["text"])

        for chunk_number, chunk_text in enumerate(text_chunks, start=1):
            chunk_records.append(
                {
                    "document_name": page["document_name"],
                    "page_number": page["page_number"],
                    "chunk_number": chunk_number,
                    "text": chunk_text,
                }
            )

    return chunk_records