"""Week 1 - Script 3: Explore SEC EDGAR filings for a public company.

We will use EDGAR's free JSON API to find a company's recent 10-K (annual report) and
8-K (current report) filings. Since Dec 2023, public companies must disclose material
cyber incidents in an 8-K (Item 1.05) within 4 business days, and describe cyber risk
management in the 10-K (Item 1C).

Run:
    export SEC_USER_AGENT="Your Name your.email@example.com"
    python week-1/scripts/03_explore_edgar.py AAPL
    python week-1/scripts/03_explore_edgar.py MSFT

IMPORTANT: The SEC *requires* a descriptive User-Agent that includes contact info, and
limits you to 10 requests/second. Requests without a User-Agent get blocked (HTTP 403).
Use your own real name/email locally; never commit it to the repo.
"""

import os
import sys

import pandas as pd
import requests

TICKER_MAP_URL = "https://www.sec.gov/files/company_tickers.json"
SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik:010d}.json"


def headers() -> dict:
    ua = os.getenv("SEC_USER_AGENT")
    if not ua:
        raise SystemExit(
            "Set SEC_USER_AGENT first, e.g.\n"
            '  export SEC_USER_AGENT="Jane Doe jane@example.com"   (PowerShell: '
            '$env:SEC_USER_AGENT="Jane Doe jane@example.com")'
        )
    return {"User-Agent": ua}


def ticker_to_cik(ticker: str) -> int:
    resp = requests.get(TICKER_MAP_URL, headers=headers(), timeout=60)
    resp.raise_for_status()
    for entry in resp.json().values():
        if entry["ticker"].upper() == ticker.upper():
            return int(entry["cik_str"])
    raise SystemExit(f"Ticker {ticker} not found")


def recent_filings(cik: int) -> tuple[str, pd.DataFrame]:
    resp = requests.get(SUBMISSIONS_URL.format(cik=cik), headers=headers(), timeout=60)
    resp.raise_for_status()
    data = resp.json()
    df = pd.DataFrame(data["filings"]["recent"])
    return data["name"], df


def filing_url(cik: int, accession: str, primary_doc: str) -> str:
    return (
        f"https://www.sec.gov/Archives/edgar/data/{cik}/"
        f"{accession.replace('-', '')}/{primary_doc}"
    )


def main() -> None:
    ticker = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    cik = ticker_to_cik(ticker)
    name, df = recent_filings(cik)
    print(f"{name} (ticker={ticker.upper()}, CIK={cik})\n")

    for form in ("10-K", "8-K"):
        subset = df[df["form"] == form].head(3)
        print(f"== Latest {form} filings ==")
        for _, row in subset.iterrows():
            url = filing_url(cik, row["accessionNumber"], row["primaryDocument"])
            # 8-K filings carry an `items` field, e.g. "1.05,9.01"
            items = f"  items={row['items']}" if row.get("items") else ""
            print(f"  {row['filingDate']}  {row['accessionNumber']}{items}\n    {url}")
        print()

    cyber = df[(df["form"] == "8-K") & df["items"].fillna("").str.contains("1.05")]
    print(f"8-Ks with Item 1.05 (material cybersecurity incident) in the recent "
          f"window: {len(cyber)}")
    print("\nTask: open one 10-K link in your browser and find Item 1A (Risk Factors). "
          "How would you split that text into chunks for retrieval?")


if __name__ == "__main__":
    main()
