# Week 5: The Test Harness

> **Status: outline.** Detailed resources will be added after Week 4. The harness design starts in Week 1 (the question bank) and is refined every week.

## Goal
Build a **rigorous, automated harness** that measures Canary's **factual accuracy** and its **resilience to adversarial attack**, with a regression gate we can run in CI.

## Planned topics
- **Golden dataset**: curated from the Week 1 question banks; question types, gold sources, splits, versioning
- **Retrieval metrics** (Recall@k, MRR, nDCG) and **generation metrics** (correctness, faithfulness, citation accuracy, numeric exactness, abstention quality)
- **LLM-as-judge** with rubrics, bias checks and calibration against human labels
- **Adversarial suite**: direct & indirect prompt injection, poisoned documents, jailbreaks, prompt/secret leakage, tool abuse, over-refusal (OWASP Top 10 for LLM Apps)
- Metrics: **attack success rate**, robustness delta, confidence intervals
- Tooling comparison: RAGAS, DeepEval, promptfoo, garak vs. custom checks
- A **CI gate** (e.g. GitHub Actions) that fails when scores regress

## Expected deliverables
- `harness/` package: datasets, runners, scorers, reports
- `harness/adversarial/` attack library with documented mitigations
- A report comparing system versions (baseline RAG → agent → hardened agent)

## Prerequisite
The agent from [Week 4](../week-4/README.md) and the question banks from [Week 1](../week-1/submissions/README.md).
