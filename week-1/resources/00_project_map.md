# 00 · Project Map: The Big Picture

Read this before anything else. It answers: *what are we building, in what order, and why is each piece there?*

## The one-sentence version

> Given a question about a cyber incident, vulnerability or company, Canary **retrieves** the relevant evidence (CVE records, KEV entries, SEC filings, market data), **reasons** over it with an LLM agent, and answers **with citations**. A separate **harness** continuously measures whether those answers are *correct* and *robust to attack*.

## Two products, not one

| | **Canary Agent** | **Canary Harness** |
|---|---|---|
| Purpose | Answer cyber-risk questions grounded in sources | Prove (or disprove) that the agent is accurate and safe |
| Inputs | User question | Test cases: golden Q&A, adversarial prompts, poisoned docs |
| Outputs | Answer + citations | Scores, failure reports, pass/fail gate in CI |
| Built in | Weeks 2–4 | Week 5 (designed from Week 1 onward!) |

**Key idea:** we collect test questions *from day one* (your Week 1 `question_bank.md`). A system you can't measure is a system you can't improve.

## Data flow

```
 CISA KEV ─┐
 NVD ──────┼─► ingest ─► clean ─► chunk + metadata ─► embed ─► vector store
 EDGAR ────┤                                                        │
 Market ───┘                                                        ▼
                                              user question ─► retrieve (+ rerank)
                                                                    │
                          tools (CVE lookup, filings, event study) ─┤
                                                                    ▼
                                                         LLM answer + citations
                                                                    │
                                          harness: golden set · faithfulness · attacks
```

## Why this is genuinely hard (and why it's a good project)

1. **Heterogeneous data.** Structured JSON (KEV/NVD), long messy HTML (10-K), time series (prices). One retriever must serve all of them.
2. **Facts that must be exactly right.** A wrong CVE ID or a wrong dollar figure is worse than no answer. Fluent hallucinations are dangerous in compliance settings.
3. **Time matters.** KEV and NVD change daily; filings are dated; "what was known on date X?" is a real question.
4. **Adversarial setting.** Filings and web content are untrusted text. Attackers can plant instructions inside documents the model retrieves (*indirect prompt injection*).
5. **Production constraints.** Latency, cost, rate limits, reproducibility, monitoring.

## Weekly plan and how the weeks depend on each other

| Week | Output | Needs from before | Feeds into |
|---|---|---|---|
| 1 | Understanding, environment, `question_bank.md` | n/a | Everything |
| 2 | Clean, chunked, metadata-rich corpus | Week 1 data exploration | Week 3 index |
| 3 | RAG baseline that answers with citations | Week 2 corpus | Week 4 agent, Week 5 eval |
| 4 | Agent with tools + guardrails | Week 3 retriever | Week 5 (system under test) |
| 5 | Test harness + adversarial suite + CI gate | Weeks 3–4 + question bank | Week 6 deploy gate |
| 6 | Deployed service + demo | All | n/a |

## Suggested workstreams (for splitting up 7 people)

Not fixed roles; the mentor will assign them in the first sync. Everyone must understand every part.

| Workstream | Focus | Weeks it's busiest |
|---|---|---|
| Security data | KEV + NVD ingestion, CVE enrichment | 2 |
| Filings | EDGAR 10-K/8-K download, section parsing, chunking | 2–3 |
| Market data | Prices, event-study calculation | 2, 4 |
| Retrieval | Embeddings, vector store, hybrid search, rerank | 3 |
| Agent | Tools, prompts, guardrails | 4 |
| Evaluation | Golden set, metrics, LLM-as-judge | 5 |
| Red team + Deployment | Adversarial suite; API, Docker, CI | 5–6 |

## Success criteria for the whole project

- ✅ Answers cite real passages; citations are *verifiable* (the quoted text exists in the source).
- ✅ Measured **factual accuracy** on a held-out golden set, with numbers we can defend.
- ✅ Measured **attack success rate** on an adversarial suite, with a documented mitigation for each class of attack.
- ✅ One command runs the harness; CI blocks a deploy if scores regress.
- ✅ A live deployed demo.
