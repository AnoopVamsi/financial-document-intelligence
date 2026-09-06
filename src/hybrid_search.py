from src.keyword_search import keyword_search
from src.retrieval import retrieve_relevant_chunks


def hybrid_search(question: str, top_k: int = 5) -> list[dict]:
    """Combine semantic and BM25 keyword search results."""

    semantic_results = retrieve_relevant_chunks(question, top_k=top_k)
    keyword_results = keyword_search(question, top_k=top_k)

    combined = {}

    for result in semantic_results:
        key = (
            result["document_name"],
            result["page_number"],
            result["chunk_number"],
        )

        combined[key] = {
            **result,
            "semantic_match": True,
            "keyword_match": False,
            "keyword_score": 0.0,
        }

    for result in keyword_results:
        key = (
            result["document_name"],
            result["page_number"],
            result["chunk_number"],
        )

        if key in combined:
            combined[key]["keyword_match"] = True
            combined[key]["keyword_score"] = result["keyword_score"]
        else:
            combined[key] = {
                **result,
                "distance": None,
                "semantic_match": False,
                "keyword_match": True,
            }

    ranked_results = sorted(
        combined.values(),
        key=lambda item: (
            item["semantic_match"] and item["keyword_match"],
            item["semantic_match"],
            item["keyword_score"],
        ),
        reverse=True,
    )

    return ranked_results[:top_k]


if __name__ == "__main__":
    test_question = "What supply chain risks are mentioned?"

    results = hybrid_search(test_question)

    print(f"\nQuestion: {test_question}\n")

    for index, result in enumerate(results, start=1):
        print(
            f"{index}. {result['document_name']} | "
            f"Page {result['page_number']} | "
            f"Semantic: {result['semantic_match']} | "
            f"Keyword: {result['keyword_match']}"
        )