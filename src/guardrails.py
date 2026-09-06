PROMPT_INJECTION_PATTERNS = [
    "ignore previous instructions",
    "ignore all instructions",
    "reveal your system prompt",
    "show your hidden prompt",
    "act as a different assistant",
    "do not use the document context",
]


def validate_question(question: str) -> tuple[bool, str]:
    """Check whether a user question contains a basic prompt-injection attempt."""

    normalized_question = question.lower()

    for pattern in PROMPT_INJECTION_PATTERNS:
        if pattern in normalized_question:
            return (
                False,
                "I cannot process requests that attempt to override "
                "the document-search instructions.",
            )

    return True, ""


def has_sufficient_evidence(retrieved_chunks: list[dict]) -> bool:
    """Require retrieved evidence before generating an answer."""

    return len(retrieved_chunks) > 0