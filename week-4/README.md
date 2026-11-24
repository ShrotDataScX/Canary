# Week 4: The Agent

> **Status: outline.** Detailed resources will be added after Week 3.

## Goal
Upgrade the RAG baseline into an **agent** that can plan, call **tools**, and combine evidence across vulnerabilities, filings and market data, safely.

## Planned topics
- **Tool use / function calling**: `lookup_cve`, `search_kev`, `find_filings`, `compute_event_study`, `compare_risk_factors`
- Multi-step reasoning for multi-hop questions (CVE → vendor → company → market impact)
- **Guardrails**: untrusted-content handling, instruction hierarchy, least-privilege tools, output validation, citation verification
- Conversation memory and query rewriting
- Cost, latency and failure handling (timeouts, retries, tool errors)
- Structured outputs (JSON schemas) for downstream use

## Expected deliverables
- `src/canary/agent/` with documented tools and an end-to-end demo
- A written **threat model** for the agent (inputs, trust boundaries, tools, abuse cases), which feeds Week 5
- Traces of ≥ 10 multi-hop questions with analysis of where reasoning broke

## Prerequisite
A working retriever and answer pipeline from [Week 3](../week-3/README.md).
