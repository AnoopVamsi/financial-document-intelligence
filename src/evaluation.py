import json
from pathlib import Path

from src.hybrid_search import hybrid_search
from src.rag import generate_grounded_answer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_ROOT / "tests" / "evaluation_dataset.json"
RESULTS_PATH = PROJECT_ROOT / "tests" / "evaluation_results.json"


def run_evaluation() -> list[dict]:
    """Run the RAG pipeline against the repeatable test dataset."""

    with DATASET_PATH.open("r", encoding="utf-8") as file:
        test_cases = json.load(file)

    results = []

    for index, test_case in enumerate(test_cases, start=1):
        question = test_case["question"]

        print(f"\nRunning test {index}: {question}")

        retrieved_chunks = hybrid_search(question)
        answer = generate_grounded_answer(question, retrieved_chunks)

        results.append(
            {
                "question": question,
                "expected_topic": test_case["expected_topic"],
                "answer": answer,
                "sources": [
                    {
                        "document_name": chunk["document_name"],
                        "page_number": chunk["page_number"],
                        "rerank_score": chunk["rerank_score"],
                    }
                    for chunk in retrieved_chunks
                ],
            }
        )

    with RESULTS_PATH.open("w", encoding="utf-8") as file:
        json.dump(results, file, indent=2)

    return results


if __name__ == "__main__":
    run_evaluation()
    print(f"\nEvaluation results saved to: {RESULTS_PATH}")