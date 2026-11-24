# 03 · RAG Primer

You know basic ML; this fills in the LLM/RAG layer. (~60 min read, plus running `scripts/04_toy_rag.py`.)

## 1. The problem RAG solves

A plain LLM:
- **Doesn't know** recent facts (the KEV catalog changed this week; the 10-K came out last month).
- **Hallucinates**: fluently invents CVE numbers, costs and quotes.
- **Can't cite** where an answer came from.
- Can't see **private/long documents** that won't fit in its context window.

**Retrieval-Augmented Generation (RAG)**: at question time, *retrieve* relevant passages from your own corpus and put them in the prompt, so the model *generates from evidence*.

```
question ─► [retriever] ─► top-k passages ─► prompt = instructions + passages + question ─► LLM ─► answer + citations
                ▲
          vector index built offline from your documents
```

## 2. The two phases

### Offline: indexing
1. **Load** raw documents (JSON, HTML, PDF).
2. **Clean / parse**: strip boilerplate, keep structure (sections, tables).
3. **Chunk**: split into passages (e.g. 200–500 tokens) with overlap; attach **metadata**.
4. **Embed**: turn each chunk into a vector with an embedding model.
5. **Store** vectors + text + metadata in a vector store.

### Online: answering
1. **(Optional) rewrite the query** (expand abbreviations, resolve "that company" from chat history).
2. **Retrieve** top-k chunks (vector similarity, keyword, or both), optionally **filter by metadata**.
3. **Rerank** with a stronger (slower) model to put the best chunks first.
4. **Build the prompt** with instructions + context + question.
5. **Generate** the answer with citations.
6. **Post-check**: verify quotes and citations exist in the retrieved text.

## 3. Key concepts

### Embeddings & similarity
An embedding model maps text to a vector so that *semantically similar* texts are close (typically measured by **cosine similarity**). "extortion malware" ≈ "ransomware", which keyword search would miss. Common open-source choices (Week 3): `sentence-transformers` models such as `all-MiniLM-L6-v2` or `bge-*` families.

### Sparse vs dense vs hybrid retrieval
| | Sparse (BM25 / TF-IDF) | Dense (embeddings) | Hybrid |
|---|---|---|---|
| Matches | exact words | meaning | both |
| Strong at | IDs & rare terms: `CVE-2023-34362`, ticker names | paraphrases, concepts | most real-world cases |
| Weak at | synonyms | exact identifiers, numbers | needs fusion tuning |

> Security text is full of **exact identifiers**, so pure dense retrieval is risky for us. Expect hybrid in Week 3.

### Chunking
Chunking is the most underrated lever. Trade-offs:
- **Too small:** lose context ("it" without its subject).
- **Too large:** dilute relevance; waste context window; cost.
- **Structure-aware** chunking (by 10-K item/paragraph, one chunk per CVE record) usually beats fixed-size splitting.
- **Overlap** reduces the chance of cutting a key sentence in half.
- **Metadata** (ticker, form, item, date, source URL) enables filtering and citation.

### Reranking
A **cross-encoder** reads (query, chunk) *together* and scores relevance: slower but more accurate than embedding similarity. Typical: retrieve 30–50 cheaply, rerank to the best 5–8.

### Prompting for grounded answers
Instruct the model to: answer **only** from context, **cite** chunk IDs, **say "I don't know"** if the context is insufficient, and **quote** numbers exactly. Then *test* that it obeys (Week 5), because instructions alone don't guarantee behavior.

### Context window and "lost in the middle"
Models use information at the start and end of long contexts better than the middle. More chunks ≠ better answers. Fewer, better chunks win.

## 4. Where RAG fails (and how we'll catch it)

| Failure | Symptom | Where it originates | How the harness catches it |
|---|---|---|---|
| **Retrieval miss** | Right document never retrieved | chunking, embeddings, filters | retrieval recall@k on golden set |
| **Wrong-context retrieval** | Plausible but wrong filing/year | missing date metadata | answer-vs-gold checks, date-sensitive cases |
| **Hallucination** | Claims not in context | model ignores instructions | faithfulness/groundedness scoring |
| **Bad citation** | Cites source that doesn't support claim | prompt/generation | citation verification |
| **Numeric error** | $45M becomes $54M | generation | exact-match numeric checks |
| **Overconfidence** | Answers when corpus has no evidence | no abstention | "unanswerable" test cases |
| **Injection** | Document text hijacks the model | untrusted context | adversarial suite |
| **Stale data** | Uses last month's KEV | no refresh | freshness tests |

## 5. Tooling landscape (you'll choose in Week 3)

- **Vector stores:** FAISS (library), Chroma (simple, local), Qdrant/Weaviate/pgvector (server-grade).
- **Frameworks:** LangChain, LlamaIndex, Haystack. *Useful, but we'll first build the core pieces by hand so you understand what the framework hides.*
- **Embeddings:** open-source (`sentence-transformers`) or API-based.
- **LLMs:** the mentor will confirm the provider; design so the model is swappable.

## 6. Try it: the toy RAG

```bash
python week-1/scripts/04_toy_rag.py "What was the market reaction to the ransomware incident?"
```

Read the code (it's short). Map each function to a step above. Then do **Exercise 5** in [`../exercises.md`](../exercises.md), which asks you to break it on purpose.

## Check your understanding

1. Why does hybrid retrieval matter more for CVE data than for generic web text?
2. Name three metadata fields you'd attach to each 10-K chunk and one query each enables.
3. What's the difference between a retrieval failure and a generation failure, and why must we measure them separately?

*(Answers in the [self-check quiz](self_check_quiz.md).)*
