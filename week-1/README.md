# Week 1: Foundations & Orientation

**Goal of the week:** by Sunday, every team member can explain *what Canary is, why it is hard, and what data it runs on*, has a working environment, has touched every data source with real code, and has run (and broken) a toy RAG pipeline.

No building of the "real" system yet. This week is about **understanding the problem well enough that Weeks 2–6 go fast**.

---

## Learning objectives

By the end of Week 1 you can:

1. Explain what a **CVE**, **CVSS score**, **CWE**, **CISA KEV** entry, and **ransomware campaign** are, and how they relate.
2. Explain what **10-K Item 1A / Item 1C** and **8-K Item 1.05** are and why they matter for a risk assistant.
3. Describe the **RAG pipeline** end to end (ingest → chunk → embed → retrieve → generate → cite) and name where each stage can fail.
4. Explain why LLM apps need **evaluation harnesses** and name at least four **adversarial attacks** (prompt injection, data poisoning, …).
5. Pull data from **CISA KEV, NVD and SEC EDGAR** with Python.
6. Use the team's **Git/GitHub workflow** (branch → PR → review).

## Suggested time budget: ~8–10 hours

| Block | Time | What to do |
|---|---|---|
| Setup | 1 h | [Environment setup](resources/05_environment_setup.md) – venv, install, `.env`, first PR |
| Domain | 2 h | [Project map](resources/00_project_map.md), [Cyber primer](resources/01_cyber_domain_primer.md), [Finance & filings primer](resources/02_finance_and_filings_primer.md) |
| AI | 2 h | [RAG primer](resources/03_rag_primer.md), [Evaluation & adversarial primer](resources/04_evaluation_and_adversarial_primer.md) |
| Hands-on | 2–3 h | Run the four [scripts](scripts/) and complete the [exercises](exercises.md) |
| Wrap-up | 1 h | [Self-check quiz](resources/self_check_quiz.md), write your [submission](submissions/README.md), prep questions for the sync |

## Recommended order

1. Read the root [`README.md`](../README.md).
2. Do the [environment setup](resources/05_environment_setup.md) *first*, so a broken install doesn't surprise you on Saturday night.
3. Read [`00_project_map.md`](resources/00_project_map.md) to see the whole system and where each week fits.
4. Alternate reading and coding: after each primer, run the matching script.

   | Primer | Script that goes with it |
   |---|---|
   | 01 Cyber domain | [`01_explore_cisa_kev.py`](scripts/01_explore_cisa_kev.py), [`02_explore_nvd.py`](scripts/02_explore_nvd.py) |
   | 02 Finance & filings | [`03_explore_edgar.py`](scripts/03_explore_edgar.py) |
   | 03 RAG | [`04_toy_rag.py`](scripts/04_toy_rag.py) |
   | 04 Evaluation & adversarial | Exercise 6 in [`exercises.md`](exercises.md) |

5. Do the [exercises](exercises.md), then the [quiz](resources/self_check_quiz.md).
6. Open a PR adding your folder under [`submissions/`](submissions/README.md).

## Folder map

```
week-1/
├── README.md                          <- this file
├── exercises.md                       <- hands-on tasks (core + stretch)
├── resources/
│   ├── 00_project_map.md              <- architecture, weekly plan, how pieces connect
│   ├── 01_cyber_domain_primer.md      <- CVE, CVSS, CWE, KEV, EPSS, ransomware
│   ├── 02_finance_and_filings_primer.md <- 10-K, 8-K, SEC cyber rules, event studies
│   ├── 03_rag_primer.md               <- RAG concepts and failure modes
│   ├── 04_evaluation_and_adversarial_primer.md <- metrics, test sets, OWASP LLM Top 10
│   ├── 05_environment_setup.md        <- Python env, secrets, Git workflow
│   ├── 06_data_sources_cheatsheet.md  <- endpoints, fields, rate limits, gotchas
│   ├── reading_list.md                <- papers, docs, optional deep dives
│   ├── glossary.md                    <- every acronym in one place
│   ├── self_check_quiz.md             <- 15 questions (answers at the bottom)
│   └── mentor_notes.md                <- for the mentor: session plan & rubric
├── scripts/                           <- runnable starter code (tested)
└── submissions/                       <- your deliverables go here
```

## Deliverables (due at the end of the week)

Open **one pull request** that adds `week-1/submissions/<your-github-username>/` containing:

- [ ] `notes.md`: filled-in [template](submissions/_template.md) (domain summary in your own words, RAG diagram, questions)
- [ ] `exercises/`: your code/outputs for the exercises (no data files, no keys!)
- [ ] `question_bank.md`: **10 realistic questions** you'd want Canary to answer, each tagged with the data source(s) needed and a note on how you'd verify the answer. *These seed our Week 5 golden test set.*

## Definition of done

- [ ] `python week-1/scripts/04_toy_rag.py` runs on your machine
- [ ] You can sketch the architecture on a whiteboard from memory
- [ ] You scored ≥ 12/15 on the self-check quiz (or know why you missed the rest)
- [ ] Your PR is open and has at least one teammate review

## Where to get unstuck

1. Re-read the relevant primer, then the [glossary](resources/glossary.md).
2. Search the error message; check the [data-source cheatsheet](resources/06_data_sources_cheatsheet.md) for rate limit/403 gotchas.
3. Ask in the team channel *with* the command you ran and the full error text.
4. Bring the question to the weekly sync. No question is too basic, since half this domain is new to everyone.

## Looking ahead: Week 2

We turn today's exploration scripts into **robust ingestion pipelines** (pagination, caching, retries, schema validation) and decide on **chunking strategies** for 10-K risk factors. Skim [`../week-2/README.md`](../week-2/README.md) to see what's coming.
