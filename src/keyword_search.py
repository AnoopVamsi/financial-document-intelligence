import re

from rank_bm25 import BM25Okapi

from src.vector_store import get_collection


def tokenize(text: str) -> list[str]:
    """Convert text into simple lowercase search tokens."""
    return re.findall(r"\b\w+\b", text.lower())


def keyword_search(question: str, top_k: int = 5) -> list[dict]:
    """Search document chunks using BM25 keyword ranking."""

    collection = get_collection()

    data = collection.get(
        include=["documents", "metadatas"],
    )

    documents = data["documents"]
    metadatas = data["metadatas"]
    ids = data["ids"]

    if not documents:
        return []

    tokenized_documents = [tokenize(document) for document in documents]
    bm25 = BM25Okapi(tokenized_documents)

    scores = bm25.get_scores(tokenize(question))
    ranked_indexes = sorted(
        range(len(scores)),
        key=lambda index: scores[index],
        reverse=True,
    )[:top_k]

    results = []

    for index in ranked_indexes:
        metadata = metadatas[index]

        results.append(
            {
                "id": ids[index],
                "text": documents[index],
                "document_name": metadata["document_name"],
                "page_number": metadata["page_number"],
                "chunk_number": metadata["chunk_number"],
                "keyword_score": round(float(scores[index]), 4),
            }
        )

    return results