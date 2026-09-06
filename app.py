import streamlit as st

from src.monitoring import log_query_metrics, start_timer
from src.workflow import run_rag_workflow

st.set_page_config(
    page_title="Financial Document Intelligence",
    page_icon="🏦",
    layout="wide",
)

st.title("🏦 Financial Document Intelligence")
st.caption("Enterprise-style financial document search and RAG platform")

with st.sidebar:
    st.header("Platform Features")
    st.write("✓ PDF ingestion and chunking")
    st.write("✓ Local embeddings")
    st.write("✓ ChromaDB semantic search")
    st.write("✓ BM25 keyword search")
    st.write("✓ Hybrid retrieval and reranking")
    st.write("✓ Guardrails")
    st.write("✓ LangGraph workflow")
    st.write("✓ Local Ollama answer generation")
    st.write("✓ Source citations")
    st.write("✓ Local monitoring")

st.subheader("Ask a question about the indexed financial documents")

question = st.chat_input(
    "Example: What are the major risk factors in this annual report?"
)

if question:
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        request_start = start_timer()

        with st.spinner("Running the LangGraph financial RAG workflow..."):
            workflow_result = run_rag_workflow(question)

        elapsed_seconds = start_timer() - request_start

        log_query_metrics(
            question=question,
            elapsed_seconds=elapsed_seconds,
            source_count=len(workflow_result["retrieved_chunks"]),
            blocked=workflow_result["blocked"],
        )

        st.markdown(workflow_result["answer"])

        results = workflow_result["retrieved_chunks"]

        if results:
            st.subheader("Sources used")

            for index, result in enumerate(results, start=1):
                with st.expander(
                    f"{index}. {result['document_name']} — "
                    f"Page {result['page_number']}"
                ):
                    st.write(result["text"])
                    st.caption(
                        f"Chunk {result['chunk_number']} | "
                        f"Rerank score: {result.get('rerank_score', 'N/A')}"
                    )

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Documents Indexed", "1")

with col2:
    st.metric("Vector Chunks", "975")

with col3:
    st.metric("Workflow", "LangGraph RAG")

st.caption(
    "This project uses public financial documents only. "
    "Do not upload confidential banking or customer data."
)