# 02 · Finance & SEC Filings Primer

No finance background required. (~45 min read.)

## 1. Why filings?

US public companies must tell investors about material risks and events, in standardized documents filed on **SEC EDGAR** (free, public). When a cyber incident hits, these filings are the **authoritative record** of what the company says happened and what it cost.

## 2. The filings we care about

### 10-K: annual report
A long (100–300 page) document. Parts relevant to us:

| Item | Name | Why we care |
|---|---|---|
| **1** | Business | What the company does (helps infer exposure/dependencies) |
| **1A** | **Risk Factors** | The company's *own* list of risks, including cyber risk. Core retrieval content |
| **1C** | **Cybersecurity** | New (FY ending on/after Dec 15, 2023): describes cyber risk management, strategy and **board/management governance** |
| **7** | MD&A (Management's Discussion & Analysis) | Where costs and operational effects of incidents are often explained |
| **8** | Financial Statements & notes | Hard numbers: expenses, insurance recoveries, contingencies |

### 8-K: current report (unscheduled events)
Short, filed within days of a significant event.

| 8-K Item | Meaning |
|---|---|
| **1.05** | **Material Cybersecurity Incidents**: the dedicated cyber item |
| 8.01 | Other Events: used for incidents not (yet) deemed material, or voluntary updates |
| 7.01 | Regulation FD disclosure |
| 2.02 | Results of operations (earnings), sometimes mentions incident costs |
| 9.01 | Exhibits (e.g. press releases) |

### 10-Q: quarterly report
Same structure idea as a 10-K, quarterly. Often where incident costs show up in follow-up quarters (stretch scope).

## 3. The SEC cybersecurity disclosure rule (2023)

Adopted July 2023 (Release No. 33-11216), in force from December 2023:

1. **8-K Item 1.05**: disclose a *material* cybersecurity incident within **four business days of determining it is material** (describe nature, scope, timing and the material impact or reasonably likely impact). Missing details may be filed later via an **8-K/A** amendment.
2. **10-K Item 1C** (Reg S-K Item 106): annual disclosure of risk-management processes and governance.
3. A national-security/public-safety delay is possible if the US Attorney General determines disclosure would pose a substantial risk.

Consequences for our data:
- **Before Dec 2023**, there is no Item 1.05. Incidents appear under other items or only in news. Older cases must be handled differently.
- **"Material" is a judgment call.** Many companies file under 8.01 instead of 1.05; this has been a topic of SEC staff guidance. Don't assume "no 1.05" means "no incident".
- **Initial 8-Ks are often vague**; the true financial impact comes later in 10-Q/10-K. A good assistant tracks a *timeline* across filings.

## 4. Anatomy of EDGAR identifiers

- **CIK**: the company's permanent ID (e.g. Apple = 320193). Tickers can change; CIKs don't.
- **Accession number**: unique filing ID, e.g. `0000320193-26-000026`.
- **Primary document**: the main HTML file inside a filing.
- 8-K filings carry an **`items`** field in the submissions API (e.g. `1.05,9.01`): perfect for filtering to cyber disclosures.

Gotchas: huge HTML with inline XBRL tags, tables that break text extraction, repeated boilerplate across years, and amendments (`10-K/A`, `8-K/A`). We handle these in Week 2.

## 5. Reading a 10-K risk factor like an analyst (try this!)

Open a recent 10-K for a company you know, jump to **Item 1A**, and search for "cyber". Ask:

- Is the language **specific** ("we experienced an incident in 2023 that…") or **boilerplate** ("we may be subject to cyberattacks")?
- Does it mention **third-party vendors**, **ransomware**, **operational disruption**, **insurance**?
- Compare with last year's filing: what changed? *("Risk factor drift" is a classic analytic and a great Canary query.)*

## 6. Market data and the event study

A common way to measure an event's *financial* impact: the **event study**.

1. Pick the **event date** (e.g. the day before/of an 8-K filing). Beware: the filing may come after the market already reacted to news.
2. Estimate the stock's **expected return** with a benchmark, e.g. the **market model**: `R_stock = α + β · R_market + ε`, fit on a window *before* the event (e.g. 120 trading days, ending ~10 days prior).
3. **Abnormal return (AR)** = actual return − expected return.
4. **Cumulative abnormal return (CAR)** = sum of AR over an event window (e.g. [-1, +1] or [0, +5] days).
5. Test whether CAR differs from zero (t-test across the estimation-window residual std).

Notes: single-company event studies are **noisy**; one result is an anecdote, not proof. Our assistant must state *what it computed and over which window*, and avoid claiming causation.

Data: `yfinance` (free, unofficial wrapper, fine for learning; not guaranteed for production).

## 7. What this means for Canary

- **Chunk by filing section**, with metadata `{ticker, cik, form, item, filing_date, accession}`, so retrieval can filter ("only 8-K Item 1.05 after 2023-12-18").
- **Dates are first-class.** Many bugs will be "retrieved the 2022 filing for a question about 2024".
- **Quote, don't paraphrase numbers.** Costs (`$45 million`) must be copied exactly; harness checks this.
- **Say what the filing doesn't say.** Absence of evidence is a valid, valuable answer.

## Check your understanding

1. What's the difference between Item 1A and Item 1C?
2. A company files an 8-K under Item 8.01 about a ransomware incident. Is that evidence it's not material? Why/why not?
3. Why is "CAR over [0, +5]" for one incident weak evidence on its own?

*(Answers in the [self-check quiz](self_check_quiz.md).)*
