"""Week 1 - Script 1: Explore the CISA Known Exploited Vulnerabilities (KEV) catalog.

KEV is a list of CVEs that CISA has confirmed are being exploited in the wild.
It is one of the highest-signal security datasets that is free and requires no key.

Run:
    python week-1/scripts/01_explore_cisa_kev.py

What to look for:
  * How many entries are there? How fast is it growing per year?
  * Which vendors/products show up the most?
  * What does `knownRansomwareCampaignUse` tell us? (Hint: it links CVEs to ransomware.)
"""

from pathlib import Path

import pandas as pd
import requests

KEV_URL = (
    "https://www.cisa.gov/sites/default/files/feeds/"
    "known_exploited_vulnerabilities.json"
)
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
OUT_PATH = DATA_DIR / "kev.csv"


def fetch_kev() -> pd.DataFrame:
    resp = requests.get(KEV_URL, timeout=60)
    resp.raise_for_status()
    payload = resp.json()
    print(f"Catalog version: {payload.get('catalogVersion')}  "
          f"released: {payload.get('dateReleased')}")
    df = pd.DataFrame(payload["vulnerabilities"])
    df["dateAdded"] = pd.to_datetime(df["dateAdded"])
    return df


def main() -> None:
    df = fetch_kev()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)

    print(f"\nTotal KEV entries: {len(df)}")
    print(f"Columns: {list(df.columns)}\n")

    print("== Entries added per year ==")
    print(df.groupby(df["dateAdded"].dt.year).size().to_string())

    print("\n== Top 10 vendors ==")
    print(df["vendorProject"].value_counts().head(10).to_string())

    print("\n== Ransomware usage flag ==")
    print(df["knownRansomwareCampaignUse"].value_counts().to_string())

    ransomware = df[df["knownRansomwareCampaignUse"] == "Known"]
    print("\n== Sample CVEs used by ransomware campaigns ==")
    cols = ["cveID", "vendorProject", "product", "dateAdded"]
    print(ransomware[cols].head(10).to_string(index=False))

    print(f"\nSaved a local copy to {OUT_PATH} (git-ignored; do not commit data).")


if __name__ == "__main__":
    main()
