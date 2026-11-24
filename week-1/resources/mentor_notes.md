# Mentor Notes (Week 1)

For the mentor. These notes are in the repo for convenience; remove or move them if you prefer mentees not to see the rubric.

## Goals for the week
1. Shared mental model of the whole system (no one should be surprised in Week 3).
2. Working environments and a working Git/PR habit for all 7 people.
3. First look at real data, with the realisation that it's messy.
4. Start the **question bank**, the raw material for Week 5.
5. Gauge skill levels and interests to assign workstreams.

## Before the week starts (≈ 30 min)
- Create a team channel; invite the mentees to the private GitHub repo (**Settings → Collaborators**; keep the repo private).
- Protect `main`: **Settings → Branches → require a pull request + 1 approval**. (Branch protection on *private* repos may need a paid GitHub plan; if unavailable, enforce by convention.)
- Decide the LLM provider/budget for Week 3+ and how keys will be shared (never in the repo).
- Skim the primers, since you'll be asked questions on them.

## Suggested kickoff session (60–75 min)
| Min | Segment |
|---|---|
| 0–10 | Why this project; show a polished end result (demo mock or sketch) |
| 10–25 | Walk through [`00_project_map.md`](00_project_map.md) on a whiteboard |
| 25–40 | Live demo: run KEV, NVD, EDGAR scripts; show a raw 10-K and an 8-K 1.05 |
| 40–55 | Toy RAG live; ask the group to predict what each query retrieves *before* running it |
| 55–65 | Git workflow demo: branch → commit → PR → review |
| 65–75 | Logistics, deliverables, Q&A |

## Suggested end-of-week sync (60 min)
1. 2 min per mentee: *one surprising thing* from the data.
2. Discuss common mistakes seen in PRs.
3. Review the combined question bank: pick the most interesting questions, spot gaps (too many easy lookups? any unanswerable?).
4. Assign **workstreams for Week 2** and preview the Week 2 tasks.

## Discussion questions
- If CVSS isn't about exploitation, what *would* you combine to estimate a company's risk?
- Filings rarely mention CVE IDs. How could we link a vulnerability to a company honestly, and with what confidence?
- What is the cost of a wrong answer here? Who gets hurt by a hallucinated incident report?
- Would you trust an LLM judge to grade our assistant? What would make you trust it more?
- How might an attacker benefit from corrupting an assistant that investors rely on?

## Common pitfalls to watch for
- **Skipping setup** → blocked on Friday. Check in on day 1–2.
- **Committing data/keys** → check PRs for `.csv`, `.env`, notebook outputs.
- **Over-reading filings** → students get lost in 200-page 10-Ks. Point them to Items 1A/1C/7 only.
- **Mixing correlation and causation** in the event study. Make them state limitations.
- **Unverified claims** about incidents copied from blogs. Insist on primary sources.
- **Confidently wrong numbers** about case studies in the primers: the primers intentionally avoid dollar figures; encourage students to find them from filings.
- **EDGAR blocking** the shared network: if many mentees run on the same campus IP at once they can hit the SEC rate limit. Stagger runs; caching helps.

## Rubric
Each deliverable is scored 0–2 (0 = missing/incorrect, 1 = partial, 2 = solid). Total /20.

| Criterion | What "2" looks like |
|---|---|
| Domain understanding (`notes.md` §1) | Own words, accurate, distinguishes severity/exploitation/impact |
| RAG understanding (§2) | Correct pipeline, specific failure modes |
| KEV analysis (Ex 1) | Correct numbers, clear chart, thoughtful interpretation |
| NVD/CVE anatomy (Ex 2) | Accurate table; good embed-vs-metadata reasoning |
| Filings (Ex 3) | Primary sources; notes what the filing *doesn't* say |
| Event study (Ex 4) | Correct method; honest limitations |
| Toy RAG experiments (Ex 5) | All five tests tried; insightful failure analysis; injection location identified |
| Test plan (Ex 6) | Concrete, automatable, aware of metric pitfalls |
| Question bank (Ex 7) | 10 verifiable questions; required mix present |
| Collaboration (PR hygiene, peer review) | Clean PR, no secrets/data, useful review comment |

## Answers/hints for selected exercises
- **Ex 5.1 (synonyms):** "extortion malware attack on a clinic" scores **0.000 for every document** (no shared words), yet the script still returns top-k. Teaching points: lexical search can't see synonyms (motivates embeddings), and a retriever that always returns *something* needs a relevance threshold or the LLM will be fed irrelevant context.
- **Ex 5.2 (out of scope):** the Tesla question retrieves the Acme risk-factor chunk purely because of the word "revenue" (score ~0.24). Good example of a plausible-looking but irrelevant retrieval; the system should abstain.
- **Ex 5.4 (exact IDs):** TF-IDF handles `CVE-2023-34362` and `CVE 2023 34362` identically, because the default tokenizer splits on punctuation into `cve`, `2023`, `34362`. Lexical search is *good* at identifiers; dense embeddings may be worse. Discuss why hybrid search combines both. (Caveat: the Log4Shell chunk also scores ~0.1 just from the shared token `cve`, so matching on identifiers is approximate, not exact.)
- **Ex 5.5 (injection):** the poisoned text lands *inside the context block of the prompt*, with the same authority as legitimate passages: the model can't tell data from instructions. Leads to Week 4 mitigations (delimiting, instruction hierarchy, output verification).
- **Ex 4:** windows: estimation [-130, -11], event [0, +5]. Note filings after market close → reaction day is next trading day. Typical student errors: using close instead of adjusted close, misaligned dates between stock and index.

## Looking ahead (Week 2 prep)
- Decide the storage format for the processed corpus (JSONL vs Parquet) and a metadata schema; draft in the Week 2 README.
- Pre-select a **list of ~30 companies** (mix of sectors and incident histories) so Week 2's ingestion has a bounded scope.
- Think about a shared **corpus snapshot** (private storage), so everyone tests against the same data.
