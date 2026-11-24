# 01 · Cybersecurity Domain Primer

You don't need to become a security engineer. You need enough vocabulary to read our data, write good test questions, and notice when the model says something nonsensical. (~45 min read.)

## 1. Vulnerabilities: CVE, CWE, CVSS

**Vulnerability**: a flaw in software or hardware that an attacker can abuse.

**CVE (Common Vulnerabilities and Exposures)**: a unique public ID for one specific vulnerability, formatted `CVE-<year>-<number>`, e.g. `CVE-2021-44228` (Log4Shell). IDs are assigned by *CNAs* (CVE Numbering Authorities: vendors, CERTs, MITRE). A CVE record is short: ID, description, references.

**NVD (National Vulnerability Database)**: run by NIST. It *enriches* CVEs with severity scores, weakness types and affected-product lists. Our primary source for "what is this CVE?".

**CWE (Common Weakness Enumeration)**: the *category* of the underlying mistake, e.g. `CWE-89` SQL injection, `CWE-502` deserialization of untrusted data. Many CVEs share one CWE.

**CPE (Common Platform Enumeration)**: standardized names for affected products/versions, e.g. `cpe:2.3:a:apache:log4j:2.14.1`. Useful for mapping CVEs to the technology a company runs.

**CVSS (Common Vulnerability Scoring System)**: a 0.0–10.0 *severity* score based on how the flaw can be exploited and its impact.

| Score | Severity |
|---|---|
| 0.0 | None |
| 0.1 – 3.9 | Low |
| 4.0 – 6.9 | Medium |
| 7.0 – 8.9 | High |
| 9.0 – 10.0 | Critical |

> ⚠️ **CVSS measures how bad a bug *could* be, not whether anyone is exploiting it.** A "10.0" nobody exploits may matter less than a "7.5" used by ransomware gangs daily. That's why we also need KEV and EPSS.

NVD may publish several CVSS versions (v2, v3.0, v3.1, v4.0) per CVE. Pipelines must pick one deliberately (our `02_explore_nvd.py` prefers the newest).

## 2. Is it actually being exploited? KEV and EPSS

**CISA KEV (Known Exploited Vulnerabilities) catalog**: CISA's list of CVEs with *evidence of active exploitation*. US federal agencies must patch them by a due date. Useful fields: `cveID`, `vendorProject`, `product`, `dateAdded`, `dueDate`, `shortDescription`, **`knownRansomwareCampaignUse`** (`Known`/`Unknown`).

**EPSS (Exploit Prediction Scoring System)**: a model from FIRST that estimates the *probability* a CVE will be exploited in the next 30 days. Optional enrichment for later weeks.

| Signal | Question it answers | Nature |
|---|---|---|
| CVSS | How bad could it be? | Theoretical severity |
| EPSS | How likely is exploitation soon? | Predicted probability |
| KEV | Is it being exploited *now*? | Observed fact |

## 3. Attacks and incidents

- **Ransomware**: malware that encrypts a victim's systems and demands payment. **Double extortion** adds *data theft*: pay or we leak your data. Operators are often organized "ransomware-as-a-service" groups (e.g. LockBit, ALPHV/BlackCat, Cl0p, Conti).
- **Data breach**: unauthorized access to or exposure of data. May or may not involve ransomware.
- **Supply-chain attack**: compromising a vendor/software so that its customers are hit (SolarWinds 2020; MOVEit 2023). One CVE → hundreds of victim companies, so company-level impact depends on *which vendors they use*.
- **Zero-day**: a vulnerability exploited before a patch exists.
- **Initial access**: how attackers first get in: unpatched internet-facing systems, stolen credentials, phishing. KEV entries are mostly in the first category.
- **Incident response (IR)**: the process of detecting, containing, eradicating and recovering from an incident.
- **MITRE ATT&CK**: a catalog of attacker tactics and techniques. We won't use it deeply but you'll see it cited.

## 4. How incidents hurt companies (this is the "impact" in our project)

| Impact type | Examples |
|---|---|
| **Operational** | Systems offline, production halted, delayed shipments, canceled procedures |
| **Direct financial** | Ransom paid, forensic & legal fees, remediation, notification costs, regulatory fines |
| **Revenue** | Lost sales during downtime, customer churn |
| **Market** | Stock price drop (often temporary), higher cost of capital |
| **Legal/regulatory** | Class actions, SEC/FTC/state AG actions, GDPR fines |
| **Insurance offsets** | Cyber insurance may recover part of the cost (often disclosed later) |

Companies describe these effects in **8-K** and **10-K** filings. See [`02_finance_and_filings_primer.md`](02_finance_and_filings_primer.md).

## 5. Well-known case studies (to anchor intuition)

Skim two or three; the public details are easy to look up, and we will use some for test questions. *Always verify figures against a primary source (the company's 8-K/10-K) before relying on them. Numbers quoted in blog posts are often wrong or outdated.*

| Case | Why it's instructive |
|---|---|
| **Log4Shell** (CVE-2021-44228, Dec 2021) | One library flaw, millions of systems; CVSS 10.0; in KEV |
| **Colonial Pipeline** (May 2021) | Ransomware causing *operational* shutdown of critical infrastructure |
| **MOVEit Transfer** (CVE-2023-34362, 2023) | Mass exploitation of a file-transfer product by the Cl0p group; many downstream victims |
| **MGM Resorts** (Sept 2023) | Social-engineering-led intrusion; quantified impact in SEC filings |
| **Change Healthcare** (Feb 2024) | Ransomware at a healthcare payments hub; cascading impact on providers and its parent company's disclosures |

## 6. What this means for Canary

- A good question links **three layers**: a *vulnerability* (CVE/KEV) → a *company exposure* (10-K/8-K) → a *financial effect* (market data, disclosed costs).
- The hard part: **CVE ↔ company links are rarely explicit.** Filings often don't name the CVE. Honest answers must say "the filing does not state this".
- KEV's `knownRansomwareCampaignUse` is a key structured filter we can expose as a tool.

## Check your understanding

1. Why can a CVSS 9.8 vulnerability be *lower priority* than a CVSS 7.5 one?
2. Which dataset tells us a CVE is exploited in the wild? Which tells us its CWE?
3. Why does one MOVEit-style CVE produce many separate company disclosures?

*(Answers are in the [self-check quiz](self_check_quiz.md).)*
