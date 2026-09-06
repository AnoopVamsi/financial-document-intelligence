import json
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOGS_DIR = PROJECT_ROOT / "logs"
METRICS_FILE = LOGS_DIR / "query_metrics.jsonl"


def start_timer() -> float:
    """Start timing one RAG request."""
    return time.perf_counter()


def log_query_metrics(
    question: str,
    elapsed_seconds: float,
    source_count: int,
    blocked: bool,
) -> None:
    """Save lightweight local monitoring metrics."""

    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    record = {
        "question": question,
        "latency_seconds": round(elapsed_seconds, 2),
        "source_count": source_count,
        "blocked": blocked,
    }

    with METRICS_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record) + "\n")