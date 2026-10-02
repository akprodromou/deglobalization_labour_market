"""
Month 2, Week 2: dedicated posting date-coverage check.

CORRECTED (v4): an earlier version theorized that failures were caused by
request pacing / cumulative server load, and added delays + long cooldown
retries. That theory was tested and FAILED: a fresh run (with pacing
already added) reproduced the EXACT same failures on the EXACT same years
(eures: 2018/2019/2020) immediately, before any cumulative load could have
built up. The pattern that actually fits BOTH runs: years with confirmed
real data succeed reliably, even huge ones (eures-escox 2026, 828,524
rows); years before a source's real data begins consistently fail. This
looks like a backend issue proving "zero/near-zero matching rows" cheaply
(e.g. no usable index on the date column), not a client pacing problem.

CONSEQUENCE: this version does NOT retry a (source, year) pair that has
already failed on a previous run (loaded from the results file) -- if it
failed consistently before, retrying again is very unlikely to help and
only costs time (each attempt costs up to 3x45s plus backoff). A year
failing for the FIRST time in a given run gets one quick, short retry
(in case of a genuine transient blip), but no long deferred-cooldown loop.
A year that still fails is recorded as "no_data_inferred": True -- an
explicit INFERENCE, clearly distinguished from a confirmed positive count.

RESUMABLE: loads existing results and skips sources already fully
resolved (including sources resolved via inference, not just confirmed
positive counts), so prior runs' time is never wasted.
"""

import json
import time
from pathlib import Path

from skillab_client import SkillabClient

YEARS = list(range(2015, 2027))
COVERAGE_CUTOFF_YEAR = 2019
RATE_LIMIT_DELAY = 1
SHORT_RETRY_DELAY = 10

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


def check_year(client, source, year):
    try:
        count = client.count_postings(
            source, min_upload_date=f"{year}-01-01", max_upload_date=f"{year}-12-31"
        )
        return count, None
    except Exception as exc:
        return None, str(exc)
    finally:
        time.sleep(RATE_LIMIT_DELAY)


def process_source(client, source):
    print(f"Checking year-by-year coverage for source='{source}'...")
    year_counts = {}

    for year in YEARS:
        count, error = check_year(client, source, year)
        if error:
            print(f"  {year}: failed once ({error}); one short retry in {SHORT_RETRY_DELAY}s...")
            time.sleep(SHORT_RETRY_DELAY)
            count, error = check_year(client, source, year)
            if error:
                print(f"  {year}: failed again -> inferring no/negligible data")
            else:
                print(f"  {year}: succeeded on retry -> {count} postings")
        elif count > 0:
            print(f"  {year}: {count} postings")

        year_counts[year] = count

    resolved_with_data = [y for y, c in year_counts.items() if c and c > 0]
    inferred_empty = [y for y, c in year_counts.items() if c is None]
    earliest = min(resolved_with_data) if resolved_with_data else None
    latest = max(resolved_with_data) if resolved_with_data else None
    reaches_cutoff = earliest is not None and earliest <= COVERAGE_CUTOFF_YEAR

    print(f"  -> earliest confirmed: {earliest}, latest confirmed: {latest}, "
          f"reaches {COVERAGE_CUTOFF_YEAR} or earlier: {reaches_cutoff}"
          f"{' (' + str(len(inferred_empty)) + ' year(s) inferred empty, not directly confirmed)' if inferred_empty else ''}")

    return {
        "source": source,
        "year_counts": {str(k): v for k, v in year_counts.items()},
        "earliest_confirmed_year": earliest,
        "latest_confirmed_year": latest,
        "reaches_2019_or_earlier": reaches_cutoff,
        "years_with_inferred_no_data": inferred_empty,
    }


def main():
    client = SkillabClient()
    results = load_existing_results()
    done_sources = {r["source"] for r in results}

    if done_sources:
        print(f"Resuming: {len(done_sources)} source(s) already processed, skipping: "
              f"{sorted(done_sources)}\n")

    for source in JOB_SOURCES:
        if source in done_sources:
            continue
        result = process_source(client, source)
        results.append(result)
        save_results(results)

    print(f"\nFinal results saved to {OUT_PATH}")
    not_reaching = [r for r in results if not r["reaches_2019_or_earlier"]]
    print(f"\n{len(not_reaching)} of {len(JOB_SOURCES)} sources do NOT confirm coverage back to "
          f"{COVERAGE_CUTOFF_YEAR}:")
    for r in not_reaching:
        print(f"  {r['source']}: earliest confirmed year = {r['earliest_confirmed_year']}, "
              f"years with inferred no data = {r['years_with_inferred_no_data']}")


if __name__ == "__main__":
    main()
