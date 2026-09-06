import ollama

MODEL_NAME = "llama3.2:3b"


def build_context(retrieved_chunks: list[dict]) -> str:
    """Combine retrieved source chunks into context for the local LLM."""

    context_parts = []

    for chunk in retrieved_chunks:
        source = (
            f"Source: {chunk['document_name']}, "
            f"page {chunk['page_number']}"
        )

        context_parts.append(f"{source}\n{chunk['text']}")

    return "\n\n---\n\n".join(context_parts)


def generate_grounded_answer(question: str, retrieved_chunks: list[dict]) -> str:
    """Answer only from retrieved financial-document evidence."""

    if not retrieved_chunks:
        return "I could not find relevant information in the indexed documents."

    context = build_context(retrieved_chunks)

    prompt = f"""
You are a financial document research assistant.

Answer the user's question using ONLY the provided document context.
Do not use outside knowledge.
If the context does not contain enough evidence, say:
"I could not find enough evidence in the indexed documents."

Question:
{question}

Document context:
{context}
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response["message"]["content"]