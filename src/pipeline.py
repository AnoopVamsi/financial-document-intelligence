from src.chunking import create_chunks
from src.embeddings import create_embeddings
from src.ingest import ingest_all_pdfs
from src.vector_store import store_chunks


def run_ingestion_pipeline() -> list[dict]:
    """Extract, chunk, embed, and store public financial documents."""

    page_records = ingest_all_pdfs()
    chunk_records = create_chunks(page_records)
    embedded_chunks = create_embeddings(chunk_records)
    stored_count = store_chunks(embedded_chunks)

    print(f"\nTotal extracted pages: {len(page_records)}")
    print(f"Total searchable chunks: {len(chunk_records)}")
    print(f"Total embedding vectors created: {len(embedded_chunks)}")
    print(f"Total vectors stored in ChromaDB: {stored_count}")

    return embedded_chunks


if __name__ == "__main__":
    run_ingestion_pipeline()