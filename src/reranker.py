def rerank_results(results: list[dict]) -> list[dict]:
    """Rank hybrid-search results using semantic and keyword signals."""

    if not results:
        return []

    max_keyword_score = max(
        result.get("keyword_score", 0.0)
        for result in results
    )

    for result in results:
        distance = result.get("distance")

        if distance is None:
            semantic_score = 0.0
        else:
            semantic_score = 1 / (1 + distance)

        keyword_score = result.get("keyword_score", 0.0)

        if max_keyword_score > 0:
            normalized_keyword_score = keyword_score / max_keyword_score
        else:
            normalized_keyword_score = 0.0

        result["rerank_score"] = round(
            (0.65 * semantic_score) + (0.35 * normalized_keyword_score),
            4,
        )

    return sorted(
        results,
        key=lambda result: result["rerank_score"],
        reverse=True,
    )