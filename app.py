import streamlit as st

from src.rag import generate_grounded_answer
from src.retrieval import retrieve_relevant_chunks

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
    st.write("✓ Local Ollama answer generation")
    st.write("✓ Source citations")
    st.write("○ Hybrid search and guardrails — next")

st.subheader("Ask a question about the indexed financial documents")

question = st.chat_input(
    "Example: What are the major risk factors in this annual report?"
)

if question:
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Retrieving sources and generating a grounded answer..."):
            results = retrieve_relevant_chunks(question)

            if results:
                answer = generate_grounded_answer(question, results)
            else:
                answer = "I could not find relevant information in the indexed documents."

        st.markdown(answer)

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
                        f"Semantic distance: {result['distance']}"
                    )

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Documents Indexed", "1")

with col2:
    st.metric("Vector Chunks", "975")

with col3:
    st.metric("RAG Mode", "Local Ollama + ChromaDB")

st.caption(
    "This project uses public financial documents only. "
    "Do not upload confidential banking or customer data."
)