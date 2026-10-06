"""
Follow-up to 03_date_coverage_check.py / Section 9 of the Week 2 report.
That check confirmed "data exists 2019 onward" as one lumped range per
source, which is NOT the same claim as "the brief's specific pre-shock
baseline window (2019-2020) has sufficient coverage." A source could pass
the first while having, say, 50 postings in 2019-2020 and the other
99% of its "2019+" total concentrated in 2023-2025.

This probes the 2019-01-01..2020-12-31 window specifically, per source,
using the same proven page_size=100 pattern (via count_postings) as the
rest of this project's reliable queries. Resumable, same as
03_date_coverage_check.py, in case of partial failures.
"""

import json
from pathlib import Path

from skillab_client import SkillabClient

BASELINE_RANGE = ("2019-01-01", "2020-12-31")

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
OUT_PATH = OUTPUT_DIR / "baseline_2019_2020_check.json"


def load_existing_results():
    if OUT_PATH.exists():
        with open(OUT_PATH, encoding="utf-8") as f:
            return json.load(f)
    return []


def save_results(results):
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


def save_result_for_source(results, source, new_entry):
    """Replace any existing entry for this source (so a retried, now-
    successful probe overwrites a previous failed one) rather than
    appending a duplicate."""
    results = [r for r in results if r["source"] != source]
    results.append(new_entry)
    save_results(results)
    return results


def probe(client, source):
    try:
        count = client.count_postings(source, min_upload_date=BASELINE_RANGE[0], max_upload_date=BASELINE_RANGE[1])
        return count, None
    except Exception as exc:
        return None, str(exc)


def main():
    client = SkillabClient()
    results = load_existing_results()
    # Only treat a source as "done" if it SUCCEEDED (error is None). A
    # previously failed probe is retried, not skipped -- fixes a bug where
    # the first version of this script treated a failed attempt as
    # permanently resolved, so re-running it never actually retried
    # anything that had errored out.
    succeeded_sources = {r["source"] for r in results if r.get("error") is None}

    if succeeded_sources:
        print(f"Resuming: skipping sources that already SUCCEEDED: {sorted(succeeded_sources)}\n")

    sources_to_retry = [s for s in JOB_SOURCES if s not in succeeded_sources]
    if any(r["source"] in sources_to_retry and r.get("error") for r in results):
        previously_failed = sorted({r["source"] for r in results if r.get("error") and r["source"] in sources_to_retry})
        print(f"Retrying sources that previously failed: {previously_failed}\n")

    for source in sources_to_retry:
        print(f"Checking '{source}', 2019-2020 specifically...")
        count, error = probe(client, source)
        if error:
            print(f"  -> FAILED: {error}")
        else:
            print(f"  -> {count} postings in 2019-2020")
        new_entry = {
            "source": source,
            "window": "2019-01-01 to 2020-12-31",
            "count": count,
            "error": error,
        }
        results = save_result_for_source(results, source, new_entry)

    print(f"\nResults saved to {OUT_PATH}\n")
    print("=== Summary: postings specifically in 2019-2020 ===")
    for r in sorted(results, key=lambda x: (x["count"] is None, -(x["count"] or 0))):
        if r["error"]:
            print(f"  {r['source']:<20} UNRESOLVED ({r['error']})")
        else:
            flag = "  <-- very thin (<100)" if r["count"] < 100 else ""
            print(f"  {r['source']:<20} {r['count']:>10,} postings{flag}")


if __name__ == "__main__":
    main()
