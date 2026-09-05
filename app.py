import streamlit as st

st.set_page_config(
    page_title="Financial Document Intelligence",
    page_icon="🏦",
    layout="wide",
)

st.title("🏦 Financial Document Intelligence")
st.caption("Enterprise-style financial document search and RAG platform")

with st.sidebar:
    st.header("Platform Features")
    st.write("✓ Document ingestion")
    st.write("✓ OCR and text extraction")
    st.write("✓ Hybrid search")
    st.write("✓ Source-cited answers")
    st.write("✓ Guardrails and evaluation")

st.subheader("Ask a question about financial documents")

question = st.chat_input(
    "Example: What are the major risk factors in this annual report?"
)

if question:
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        st.info(
            "The RAG pipeline is being built. "
            "Soon, this answer will be generated from retrieved financial-document sources."
        )

st.divider()

st.subheader("Project Status")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Documents Indexed", "0")

with col2:
    st.metric("Vector Chunks", "0")

with col3:
    st.metric("Retrieval Mode", "Coming soon")

st.caption(
    "This project uses public financial documents only. "
    "Do not upload confidential banking or customer data."
)