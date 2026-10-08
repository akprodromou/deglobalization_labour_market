"""
Month 2, Week 2: dedicated posting date-coverage check.

REDESIGNED (v5), based on everything confirmed across this whole project:

1. page_size matters. Every query using the full page_size=100 pagination
   pattern (iter_postings / the big 01_fetch_sample.py runs) has succeeded
   reliably across ALL 16 posting sources. Every query using a lightweight
   page_size=1 count-only probe (the previous version of this script) has
   been unreliable -- including failing TWICE on eures-escox 2023, a date
   range independently CONFIRMED to have 417 real records via the
   page_size=100 pattern on an earlier run. count_postings() in
   skillab_client.py now defaults to page_size=100 to match the one
   pattern that has actually worked.

2. Scope reduced from checking all 12 years individually (192 requests,
   multiple failed multi-hour runs) to just TWO wide-range checks per
   source, which is all the brief actually asks for ("does coverage reach
   2019 onward?"):
     - "recent" = 2019-01-01 .. today  -> confirms data exists in-or-after 2019
     - "historical" = 2010-01-01 .. 2018-12-31 -> confirms data exists before 2019
   16 sources x 2 probes = 32 requests total, not 192.

3. A failed probe is reported as UNRESOLVED, not as evidence of "no data" --
   a repeated-failure-implies-emptiness inference was tried and directly
   DISPROVEN by the eures-escox 2023 contradiction, so this version makes
   no such claim. Each source's own existing client-level retry (3x, with
   backoff) is the only retry; no additional long cooldown loop.

4. Resumable: skips sources already present in the results file.
"""

import json
from datetime import date
from pathlib import Path

from skillab_client import SkillabClient

TODAY = date.today().isoformat()
RECENT_RANGE = ("2019-01-01", TODAY)
HISTORICAL_RANGE = ("2010-01-01", "2018-12-31")

JOB_SOURCES = [
    "brightminds", "eures", "eures-escox",
    "jobbguru", "jobbguru.se",
    "jobbland", "jobbland.se",
    "jobmedic", "jobmedic.co.uk",
    "jobscentral", "jobs.de",
    "kariera.fr", "kariera.gr",
    "lesjeudis", "lesjeudis.com",
    "OJA",
]

OUTPUT_DIR = Path("data/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = OUTPUT_DIR / "date_coverage_check.json"


def load_existing_results():
    if OUT_PATH.exists():
        with open(OUT_PATH, encoding="utf-8") as f:
            return json.load(f)
    return []


def save_results(results):
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


def probe(client, source, min_date, max_date):
    """One probe, page_size=100 (the proven-reliable pattern). Returns
    (count, error) -- error is None on success, count is None on failure."""
    try:
        count = client.count_postings(source, min_upload_date=min_date, max_upload_date=max_date)
        return count, None
    except Exception as exc:
        return None, str(exc)


def process_source(client, source):
    print(f"Checking source='{source}'...")

    recent_count, recent_err = probe(client, source, *RECENT_RANGE)
    if recent_err:
        print(f"  recent (2019-{TODAY[:4]}): FAILED ({recent_err})")
    else:
        print(f"  recent (2019-{TODAY[:4]}): {recent_count} postings")

    hist_count, hist_err = probe(client, source, *HISTORICAL_RANGE)
    if hist_err:
        print(f"  historical (2010-2018): FAILED ({hist_err})")
    else:
        print(f"  historical (2010-2018): {hist_count} postings")

    confirmed_since_2019 = (recent_count is not None) and (recent_count > 0)
    confirmed_before_2019 = (hist_count is not None) and (hist_count > 0)

    result = {
        "source": source,
        "recent_2019_onward": {
            "count": recent_count, "error": recent_err, "confirmed_has_data": confirmed_since_2019,
        },
        "historical_pre_2019": {
            "count": hist_count, "error": hist_err, "confirmed_has_data": confirmed_before_2019,
        },
    }
    print(f"  -> confirmed data 2019+: {confirmed_since_2019}"
          f"{' (UNRESOLVED -- probe failed)' if recent_err else ''}; "
          f"confirmed data pre-2019: {confirmed_before_2019}"
          f"{' (UNRESOLVED -- probe failed)' if hist_err else ''}")
    return result


def main():
    client = SkillabClient()
    results = load_existing_results()
    done_sources = {r["source"] for r in results}

    if done_sources:
        print(f"Resuming: skipping already-processed sources: {sorted(done_sources)}\n")

    for source in JOB_SOURCES:
        if source in done_sources:
            continue
        result = process_source(client, source)
        results.append(result)
        save_results(results)

    print(f"\nFinal results saved to {OUT_PATH}\n")
    print("=== Summary ===")
    for r in results:
        since = r["recent_2019_onward"]
        hist = r["historical_pre_2019"]
        since_label = "YES" if since["confirmed_has_data"] else ("UNRESOLVED" if since["error"] else "NO")
        hist_label = "YES" if hist["confirmed_has_data"] else ("UNRESOLVED" if hist["error"] else "NO")
        print(f"  {r['source']}: data 2019+ = {since_label}, data pre-2019 = {hist_label}")


if __name__ == "__main__":
    main()
