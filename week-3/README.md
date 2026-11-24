# Week 3: The RAG Pipeline

> **Status: outline.** Detailed resources will be added after Week 2.

## Goal
Build a **retrieval-augmented generation baseline** over the Week 2 corpus that answers questions with **verifiable citations**.

## Planned topics
- **Embeddings** (`sentence-transformers`) and the vector store (FAISS / Chroma): index build and persistence
- **Hybrid retrieval**: BM25 + dense, fusion (e.g. Reciprocal Rank Fusion), **metadata filtering** (ticker, date, form/item)
- **Reranking** with a cross-encoder
- **Grounded generation**: prompt design, citation format, abstention ("I don't know")
- Retrieval metrics on a small dev set: **Recall@k, MRR**
- Build-by-hand first, *then* compare with a framework (LangChain / LlamaIndex)

## Expected deliverables
- `src/canary/rag/` pipeline with a CLI (`python -m canary.ask "…"`)
- Baseline results: retrieval metrics + a qualitative error analysis of ≥ 20 failures
- Swappable LLM interface (no vendor lock-in)

## Prerequisite
A clean corpus and metadata schema from [Week 2](../week-2/README.md).
