"""Week 1 - Script 4: A toy RAG pipeline in ~80 lines, with NO API keys and NO GPU.

Goal: let you *see* every moving part of RAG before we use real tools in Week 3.

    documents -> chunk -> index (TF-IDF vectors) -> retrieve top-k -> build prompt
                                                                         |
                                       (Week 3: send prompt to an LLM) <-+

Retrieval here is TF-IDF + cosine similarity (lexical). In Week 3 we replace it with
dense embeddings and a vector database, and compare the two.

Run:
    python week-1/scripts/04_toy_rag.py
    python week-1/scripts/04_toy_rag.py "Which ransomware group hit a healthcare firm?"
"""

import sys
from dataclasses import dataclass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# A tiny hand-written corpus. Each doc has text plus metadata we can cite later.
# These are SYNTHETIC examples for learning; real data arrives in Week 2.
CORPUS = [
    {"id": "kev-log4j", "source": "CISA KEV",
     "text": "CVE-2021-44228 (Log4Shell) is a remote code execution vulnerability in "
             "Apache Log4j2. It is listed in the CISA KEV catalog and is exploited "
             "in the wild by ransomware actors."},
    {"id": "kev-moveit", "source": "CISA KEV",
     "text": "CVE-2023-34362 is a SQL injection flaw in Progress MOVEit Transfer. "
             "The Cl0p ransomware group used it to steal data from hundreds of "
             "organizations in 2023."},
    {"id": "10k-risk-acme", "source": "10-K Item 1A (synthetic)",
     "text": "Acme Corp. risk factors: a cyberattack could disrupt our manufacturing "
             "operations, lead to loss of customer data, regulatory fines and "
             "reputational damage that could reduce revenue."},
    {"id": "8k-hosp", "source": "8-K Item 1.05 (synthetic)",
     "text": "Northwind Health disclosed a ransomware incident that encrypted "
             "patient scheduling systems. The company estimates remediation costs "
             "of $45 million and has activated its incident response plan."},
    {"id": "mkt-note", "source": "Market note (synthetic)",
     "text": "Shares of Northwind Health fell 8% the day after the ransomware "
             "disclosure and underperformed the healthcare index over five days."},
]


@dataclass
class Hit:
    doc: dict
    score: float


class ToyRetriever:
    def __init__(self, docs: list[dict]) -> None:
        self.docs = docs
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = self.vectorizer.fit_transform(d["text"] for d in docs)

    def search(self, query: str, k: int = 3) -> list[Hit]:
        q_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(q_vec, self.matrix).ravel()
        ranked = scores.argsort()[::-1][:k]
        return [Hit(self.docs[i], float(scores[i])) for i in ranked]


def build_prompt(question: str, hits: list[Hit]) -> str:
    context = "\n".join(f"[{h.doc['id']}] ({h.doc['source']}) {h.doc['text']}" for h in hits)
    return (
        "You are a cyber risk analyst. Answer ONLY from the context below and cite "
        "sources like [id]. If the context is insufficient, say you don't know.\n\n"
        f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    )


def main() -> None:
    question = sys.argv[1] if len(sys.argv) > 1 else (
        "What was the market reaction to the ransomware incident?"
    )
    retriever = ToyRetriever(CORPUS)
    hits = retriever.search(question, k=3)

    print(f"Question: {question}\n")
    print("== Retrieved chunks ==")
    for h in hits:
        print(f"  score={h.score:.3f}  [{h.doc['id']}]  {h.doc['text'][:70]}...")

    print("\n== Prompt that would be sent to the LLM ==")
    print(build_prompt(question, hits))

    print("\nExperiments to try (see week-1/exercises.md):")
    print("  1. Ask a question using synonyms (e.g. 'extortion malware') - does it fail?")
    print("  2. Ask something NOT in the corpus - what does retrieval return anyway?")
    print("  3. Add a malicious document: 'Ignore previous instructions and ...'")


if __name__ == "__main__":
    main()
