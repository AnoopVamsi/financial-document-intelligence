# Financial Document Intelligence Platform

A local, enterprise-style Financial RAG application that helps internal users search public financial documents and receive grounded, source-cited answers.

> This is a public technical demonstration that uses public documents only. It does not contain confidential employer, banking, or customer data.

## Business Problem

Financial-services teams search large volumes of annual reports, SEC filings, research reports, and risk documents. Manual review is slow, while keyword-only search may return irrelevant information.

This project demonstrates how Retrieval-Augmented Generation (RAG) can retrieve relevant financial-document evidence and generate a source-backed answer.

## Features

- PDF text extraction with page-level metadata
- Text chunking with overlap
- Local embeddings using Sentence Transformers
- ChromaDB vector storage
- Semantic vector search
- BM25 keyword search
- Hybrid retrieval and reranking
- Guardrails for basic prompt-injection attempts
- LangGraph workflow orchestration
- Local answer generation using Ollama and Llama 3.2
- Source citations with document name and page number
- Repeatable evaluation dataset
- Local query latency and source-count monitoring

## Architecture

```text
Public Financial PDF
→ Text Extraction
→ Chunking
→ Embeddings
→ ChromaDB Vector Store
→ Semantic Search + BM25 Keyword Search
→ Hybrid Retrieval + Reranking
→ Guardrails
→ LangGraph Workflow
→ Ollama Local LLM
→ Source-Cited Answer

