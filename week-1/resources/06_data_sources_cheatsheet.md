# 06 · Data Sources Cheatsheet

Quick reference for the four data sources. Verified working on the date the scripts were written; APIs change, so check the official docs if something breaks.

---

## 1. CISA KEV

| | |
|---|---|
| **What** | CVEs with confirmed active exploitation |
| **Feed (JSON)** | `https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json` |
| **Human page** | <https://www.cisa.gov/known-exploited-vulnerabilities-catalog> |
| **Auth / limits** | None. Single file, a few MB. Cache it; refresh daily |
| **Top-level keys** | `title`, `catalogVersion`, `dateReleased`, `count`, `vulnerabilities[]` |

Per-vulnerability fields: `cveID`, `vendorProject`, `product`, `vulnerabilityName`, `dateAdded`, `shortDescription`, `requiredAction`, `dueDate`, `knownRansomwareCampaignUse`, `notes`, `cwes`.

Gotchas: `knownRansomwareCampaignUse` is the *string* `"Known"`/`"Unknown"`, not a boolean. Entries can be updated over time. Catalog is small (~1.8k rows), so we can fully re-ingest.

---

## 2. NVD (CVE API 2.0)

| | |
|---|---|
| **Base URL** | `https://services.nvd.nist.gov/rest/json/cves/2.0` |
| **Docs** | <https://nvd.nist.gov/developers/vulnerabilities> |
| **Single CVE** | `?cveId=CVE-2021-44228` |
| **Pagination** | `resultsPerPage` (max 2000) + `startIndex`; response has `totalResults` |
| **Date filters** | `lastModStartDate` / `lastModEndDate` (ISO-8601; ranges are limited, currently 120 days) |
| **Auth / limits** | Works without a key at ~5 requests per rolling 30 s; with a free key ~50 per 30 s (header `apiKey`). Add a short sleep between calls |

Response shape: `vulnerabilities[].cve` with `id`, `published`, `lastModified`, `descriptions[]` (pick `lang == "en"`), `metrics` (`cvssMetricV31`, `cvssMetricV40`, …), `weaknesses[]` (CWE IDs), `configurations[]` (CPE match rules), `references[]`, and KEV fields (`cisaExploitAdd`, `cisaActionDue`…) when applicable.

Gotchas: metrics may be **missing** for recent/unanalyzed CVEs; multiple CVSS versions coexist; descriptions are multilingual; NVD enrichment sometimes lags CVE publication. Don't fetch all ~250k+ CVEs by default: start from the KEV list.

---

## 3. SEC EDGAR

| | |
|---|---|
| **Ticker → CIK** | `https://www.sec.gov/files/company_tickers.json` |
| **Filing index per company** | `https://data.sec.gov/submissions/CIK##########.json` (CIK zero-padded to 10 digits) |
| **Filing document** | `https://www.sec.gov/Archives/edgar/data/<cik>/<accession-no-dashes>/<primaryDocument>` |
| **Structured financials** | `https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json` (XBRL numbers, stretch goal) |
| **Docs** | <https://www.sec.gov/search-filings/edgar-application-programming-interfaces> |
| **Full-text search (web UI)** | <https://efts.sec.gov/LatestSearch/> via <https://www.sec.gov/edgar/search/> (use for manual exploration) |
| **Auth / limits** | **No key, but a descriptive `User-Agent` with your name+email is mandatory.** Max **10 requests/second**; exceeding it can get your IP blocked |

Submissions JSON: `filings.recent` is a *columnar* dict (`form`, `filingDate`, `accessionNumber`, `primaryDocument`, `items`, …) → `pd.DataFrame(data["filings"]["recent"])`. Older filings are listed in `filings.files[]` as extra JSON files.

Gotchas: filings are large HTML (often inline-XBRL); tables flatten badly; amendments exist (`10-K/A`, `8-K/A`); tickers get reused/changed (prefer CIK as the key); `items` is a comma-separated string, with the cyber item being `1.05`.

---

## 4. Market data

| | |
|---|---|
| **Library** | `yfinance` (`pip install yfinance`), an unofficial Yahoo Finance wrapper |
| **Use** | `yf.download("AAPL", start="2023-01-01", end="2024-01-01")` → OHLCV DataFrame; benchmark with `^GSPC` (S&P 500) or a sector ETF |
| **Limits** | Unofficial; can break or rate-limit. Fine for learning; consider a licensed source for production |

Use **adjusted close** for returns, align trading days with the benchmark, and remember filings often happen *after* market close (use the next trading day as the reaction day).

---

## 5. Example fields to decide on in Week 2

| Source | Free-text to embed | Structured metadata to keep |
|---|---|---|
| KEV | `vulnerabilityName` + `shortDescription` | `cveID`, vendor, product, `dateAdded`, ransomware flag, CWE |
| NVD | English description | CVSS score/severity/version, CWE, published/modified dates, CPEs |
| 10-K | Item 1A / 1C paragraphs | CIK, ticker, fiscal year, filing date, item, accession, URL |
| 8-K | Item text (esp. 1.05) | CIK, ticker, filing date, items, accession, URL |
| Market | (none, a numeric tool, not embedded) | ticker, date, adjusted close |
