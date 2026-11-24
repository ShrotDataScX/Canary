"""Week 1 - Script 2: Look up CVEs in the NVD (National Vulnerability Database) API.

NVD holds the full description, CVSS severity score, weaknesses (CWE) and affected
products (CPE) for every CVE. KEV tells us *which* CVEs matter; NVD tells us *what*
they are.

Run:
    python week-1/scripts/02_explore_nvd.py                  # defaults to Log4Shell
    python week-1/scripts/02_explore_nvd.py CVE-2023-34362   # MOVEit Transfer

Notes:
  * No API key is needed, but unauthenticated calls are rate limited
    (about 5 requests per rolling 30 seconds). Be polite: cache results, add sleeps.
  * Request a free key at https://nvd.nist.gov/developers/request-an-api-key
    and export it as NVD_API_KEY to get a higher limit.
"""

import os
import sys

import requests

NVD_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"


def fetch_cve(cve_id: str) -> dict:
    headers = {}
    if os.getenv("NVD_API_KEY"):
        headers["apiKey"] = os.environ["NVD_API_KEY"]
    resp = requests.get(NVD_URL, params={"cveId": cve_id}, headers=headers, timeout=60)
    resp.raise_for_status()
    vulns = resp.json().get("vulnerabilities", [])
    if not vulns:
        raise SystemExit(f"{cve_id} not found in NVD")
    return vulns[0]["cve"]


def english_description(cve: dict) -> str:
    for d in cve.get("descriptions", []):
        if d.get("lang") == "en":
            return d["value"]
    return ""


def best_cvss(cve: dict) -> tuple[str, float | None, str | None]:
    """Return (version, base score, severity), preferring the newest CVSS version."""
    metrics = cve.get("metrics", {})
    for key in ("cvssMetricV40", "cvssMetricV31", "cvssMetricV30", "cvssMetricV2"):
        if key in metrics and metrics[key]:
            data = metrics[key][0]["cvssData"]
            severity = data.get("baseSeverity") or metrics[key][0].get("baseSeverity")
            return key.replace("cvssMetric", ""), data.get("baseScore"), severity
    return "n/a", None, None


def main() -> None:
    cve_id = sys.argv[1] if len(sys.argv) > 1 else "CVE-2021-44228"
    cve = fetch_cve(cve_id)

    version, score, severity = best_cvss(cve)
    weaknesses = [
        d["value"]
        for w in cve.get("weaknesses", [])
        for d in w.get("description", [])
    ]

    print(f"CVE:         {cve['id']}")
    print(f"Published:   {cve.get('published')}")
    print(f"CVSS:        {score} ({severity}) [{version}]")
    print(f"Weaknesses:  {', '.join(weaknesses) or 'n/a'}")
    print(f"In CISA KEV: {'cisaExploitAdd' in cve}")
    print(f"\nDescription:\n{english_description(cve)}")
    print(f"\nReferences: {len(cve.get('references', []))} links, e.g.")
    for ref in cve.get("references", [])[:3]:
        print(f"  - {ref['url']}")

    print("\nThink about it: which fields would you embed for retrieval? "
          "Which would you keep as structured metadata for filtering?")


if __name__ == "__main__":
    main()
