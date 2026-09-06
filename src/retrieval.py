from src.embeddings import load_embedding_model
from src.vector_store import get_collection


def retrieve_relevant_chunks(question: str, top_k: int = 5) -> list[dict]:
    """Find the most relevant financial-document chunks for a question."""

    model = load_embedding_model()
    question_embedding = model.encode(question).tolist()

    collection = get_collection()

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    retrieved_chunks = []

    for document, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        retrieved_chunks.append(
            {
                "text": document,
                "document_name": metadata["document_name"],
                "page_number": metadata["page_number"],
                "chunk_number": metadata["chunk_number"],
                "distance": round(distance, 4),
            }
        )

    return retrieved_chunks


if __name__ == "__main__":
    test_question = "What are the major risk factors mentioned in the annual report?"

    results = retrieve_relevant_chunks(test_question)

    print(f"\nQuestion: {test_question}\n")

    for index, result in enumerate(results, start=1):
        print(
            f"{index}. {result['document_name']} | "
            f"Page {result['page_number']} | "
            f"Chunk {result['chunk_number']}"
        )
        print(result["text"][:400])
        print("-" * 60)