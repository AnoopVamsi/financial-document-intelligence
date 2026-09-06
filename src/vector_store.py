import chromadb

COLLECTION_NAME = "financial_documents"


def get_collection():
    """Create or open the local financial-document vector collection."""

    client = chromadb.PersistentClient(path="chroma_db")

    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"description": "Public financial document chunks"},
    )


def store_chunks(embedded_chunks: list[dict]) -> int:
    """Store embedded document chunks and their source metadata."""

    if not embedded_chunks:
        return 0

    collection = get_collection()

    collection.upsert(
        ids=[
            f"{chunk['document_name']}-page-{chunk['page_number']}-chunk-{chunk['chunk_number']}"
            for chunk in embedded_chunks
        ],
        documents=[chunk["text"] for chunk in embedded_chunks],
        embeddings=[chunk["embedding"] for chunk in embedded_chunks],
        metadatas=[
            {
                "document_name": chunk["document_name"],
                "page_number": chunk["page_number"],
                "chunk_number": chunk["chunk_number"],
            }
            for chunk in embedded_chunks
        ],
    )

    return len(embedded_chunks)