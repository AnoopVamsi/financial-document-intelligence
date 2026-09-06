from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from src.guardrails import validate_question
from src.hybrid_search import hybrid_search
from src.rag import generate_grounded_answer


class RAGState(TypedDict):
    question: str
    retrieved_chunks: list[dict]
    answer: str
    blocked: bool


def retrieve_node(state: RAGState) -> dict:
    """Find relevant financial-document evidence."""

    chunks = hybrid_search(state["question"])

    return {"retrieved_chunks": chunks}


def guardrail_node(state: RAGState) -> dict:
    """Validate the question before sending it to the model."""

    is_allowed, message = validate_question(state["question"])

    if not is_allowed:
        return {
            "blocked": True,
            "answer": message,
        }

    return {"blocked": False}


def route_after_guardrails(state: RAGState) -> str:
    """Choose whether to stop or generate a grounded answer."""

    if state["blocked"]:
        return "stop"

    return "generate"


def generate_node(state: RAGState) -> dict:
    """Generate an answer only from retrieved document evidence."""

    answer = generate_grounded_answer(
        state["question"],
        state["retrieved_chunks"],
    )

    return {"answer": answer}


def build_workflow():
    """Create the LangGraph RAG workflow."""

    workflow = StateGraph(RAGState)

    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("guardrails", guardrail_node)
    workflow.add_node("generate", generate_node)

    workflow.add_edge(START, "retrieve")
    workflow.add_edge("retrieve", "guardrails")

    workflow.add_conditional_edges(
        "guardrails",
        route_after_guardrails,
        {
            "stop": END,
            "generate": "generate",
        },
    )

    workflow.add_edge("generate", END)

    return workflow.compile()


rag_workflow = build_workflow()


def run_rag_workflow(question: str) -> dict:
    """Run the full LangGraph workflow for one question."""

    return rag_workflow.invoke(
        {
            "question": question,
            "retrieved_chunks": [],
            "answer": "",
            "blocked": False,
        }
    )