# Architecture

## End-to-End Workflow

```text
Public Financial PDF
→ Text Extraction
→ Chunking
→ Local Embeddings
→ ChromaDB Vector Store
→ Semantic Search + BM25 Keyword Search
→ Hybrid Retrieval + Reranking
→ Guardrails
→ LangGraph Workflow
→ Ollama Local LLM
→ Source-Cited Answer