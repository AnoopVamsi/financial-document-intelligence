from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"


def load_embedding_model() -> SentenceTransformer:
    """Load a free local model that converts text into embeddings."""
    return SentenceTransformer(MODEL_NAME)


def create_embeddings(chunk_records: list[dict]) -> list[dict]:
    """Add an embedding vector to every text chunk."""

    if not chunk_records:
        return []

    model = load_embedding_model()
    texts = [chunk["text"] for chunk in chunk_records]

    vectors = model.encode(texts, show_progress_bar=True)

    for chunk, vector in zip(chunk_records, vectors):
        chunk["embedding"] = vector.tolist()

    return chunk_records