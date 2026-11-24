# Reading List

Split into **Must read** (do this week) and **Optional** (deeper dives; many will matter in later weeks). Links point to official or canonical sources; if one has moved, search the title.

## Must read (≈ 2–3 hours total)

### Security data
- **CISA KEV catalog** (browse, don't read in full): <https://www.cisa.gov/known-exploited-vulnerabilities-catalog>
- **NVD: Vulnerability Metrics (CVSS explained)**: <https://nvd.nist.gov/vuln-metrics/cvss>
- **FIRST: What is EPSS?**: <https://www.first.org/epss/>

### Filings and regulation
- **SEC press release & fact sheet on the 2023 cyber disclosure rules**: search "SEC Adopts Rules on Cybersecurity Risk Management, Strategy, Governance, and Incident Disclosure" at <https://www.sec.gov/newsroom>
- **SEC: How to read a 10-K** (investor.gov): <https://www.investor.gov/introduction-investing/getting-started/researching-investments/how-read-10-k10-q>
- **SEC EDGAR API documentation**: <https://www.sec.gov/search-filings/edgar-application-programming-interfaces>

### RAG and LLM apps
- **"Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"** (Lewis et al., 2020), the original RAG paper. Read abstract, intro, Figure 1: <https://arxiv.org/abs/2005.11401>
- **Pinecone or LlamaIndex "What is RAG?" guides**: any beginner explainer; compare two.
- **Sentence-BERT** (Reimers & Gurevych, 2019), how sentence embeddings work. Abstract + intro: <https://arxiv.org/abs/1908.10084>

### Evaluation and security
- **OWASP Top 10 for LLM Applications**: <https://owasp.org/www-project-top-10-for-large-language-model-applications/> (read all ten summaries)
- **RAGAS: Automated Evaluation of RAG** (Es et al., 2023). Abstract + metrics section: <https://arxiv.org/abs/2309.15217>

## Optional deep dives

### RAG
- **"Lost in the Middle"** (Liu et al., 2023), why long contexts hurt: <https://arxiv.org/abs/2307.03172>
- **BEIR benchmark** (Thakur et al., 2021), why BM25 is a strong baseline: <https://arxiv.org/abs/2104.08663>
- **Reciprocal Rank Fusion** (Cormack et al., 2009), simple hybrid-search fusion (search the title).

### Adversarial / safety
- **"Not what you've signed up for"** (Greshake et al., 2023), indirect prompt injection in LLM-integrated apps: <https://arxiv.org/abs/2302.12173>
- **"Universal and Transferable Adversarial Attacks on Aligned Language Models"** (Zou et al., 2023): <https://arxiv.org/abs/2307.15043>
- **PoisonedRAG** (Zou et al., 2024), knowledge-corruption attacks on RAG: search the title on arXiv.
- **garak**, an LLM vulnerability scanner: <https://github.com/NVIDIA/garak>
- **promptfoo**, test-driven LLM evaluation: <https://github.com/promptfoo/promptfoo>

### Finance / event studies
- **MacKinlay, "Event Studies in Economics and Finance"** (1997): the classic reference; search the title.
- Browse the **Item 1C** section of two large companies' latest 10-Ks and compare how they describe governance.

### Cyber background
- **MITRE ATT&CK**: <https://attack.mitre.org/>
- **Verizon Data Breach Investigations Report (DBIR)**: annual; good for how breaches typically start.
- Public post-incident write-ups for Colonial Pipeline, MOVEit, MGM Resorts, Change Healthcare (always cross-check against company filings).

## How to read a paper (if it's new to you)
1. Abstract → conclusion → figures. Decide if it's worth the rest.
2. Write down in two sentences: *What problem? What's the key idea?*
3. Note one thing that applies to Canary. That note goes in your `notes.md`.
