"""
8 sources failed the direct 2019-01-01..2020-12-31 probe consistently
across two full runs (6/6 attempts each): eures, eures-escox, jobbland,
jobs.de, kariera.fr, kariera.gr, lesjeudis, lesjeudis.com.

Rather than retry the same closed-window query shape a third time, this
derives the 2019-2020 count INDIRECTLY using two open-ended queries --
the pattern that has actually been reliable throughout this project
(every "2019 onward" probe in 03_date_coverage_check.py succeeded; it's
specifically BOTH-bounded-in-the-past windows that have been unreliable,
across eures-escox pre-2019 originally and now these 8 for 2019-2020):

    count(2019-2020) = count(2019-01-01 .. today) - count(2021-01-01 .. today)

The first term is already measured and saved in
data/raw/date_coverage_check.json (from 03_date_coverage_check.py). This
script only needs to measure the second term, then computes the
subtraction and clearly labels the result as DERIVED, not directly
measured, since it depends on two separate snapshots potentially taken
seconds apart on a live, growing dataset (the Week 2 report already notes
eures's total count changed between two different measurement dates).
"""

import json
from datetime import date
from pathlib import Path

from skillab_client import SkillabClient

SOURCES_NEEDING_DERIVATION = [
    "eures", "eures-escox", "jobbland", "jobs.de",
    "kariera.fr", "kariera.gr", "lesjeudis", "lesjeudis.com",
]

TODAY = date.today().isoformat()
POST_2021_START = "2021-01-01"

ORIGINAL_RESULTS_PATH = Path("data/raw/date_coverage_check.json")
OUT_PATH = Path("data/raw/baseline_2019_2020_derived.json")


def load_2019_onward_counts_from_file():
    """Pull the already-measured '2019 onward' counts from the original
    03_date_coverage_check.py results file, if it exists on this machine.
    That check was originally run on a different computer (Windows), so
    this file may not be present here -- callers should fall back to a
    fresh probe per-source when a source isn't found in this dict."""
    if not ORIGINAL_RESULTS_PATH.exists():
        print(f"Note: {ORIGINAL_RESULTS_PATH} not found on this machine -- will probe "
              f"'2019 onward' fresh for each source instead of reusing a saved count.\n")
        return {}

    with open(ORIGINAL_RESULTS_PATH, encoding="utf-8") as f:
        original_results = json.load(f)

    counts = {}
    for r in original_results:
        recent = r.get("recent_2019_onward", {})
        counts[r["source"]] = recent.get("count")
    return counts


def probe_2019_onward(client, source):
    try:
        count = client.count_postings(source, min_upload_date="2019-01-01", max_upload_date=TODAY)
        return count, None
    except Exception as exc:
        return None, str(exc)


def probe_post_2021(client, source):
    try:
        count = client.count_postings(source, min_upload_date=POST_2021_START, max_upload_date=TODAY)
        return count, None
    except Exception as exc:
        return None, str(exc)


def load_existing_derived():
    if OUT_PATH.exists():
        with open(OUT_PATH, encoding="utf-8") as f:
            return json.load(f)
    return []


def main():
    counts_2019_onward = load_2019_onward_counts_from_file()
    client = SkillabClient()

    derived_results = load_existing_derived()
    already_done = {r["source"] for r in derived_results if r.get("post_2021_error") is None}

    for source in SOURCES_NEEDING_DERIVATION:
        if source in already_done:
            print(f"Skipping '{source}' (already resolved).")
            continue

        total_2019_onward = counts_2019_onward.get(source)
        if total_2019_onward is None:
            print(f"Checking '{source}', 2019 onward fresh (not found in saved results)...")
            total_2019_onward, onward_error = probe_2019_onward(client, source)
            if onward_error:
                print(f"  -> FAILED: {onward_error} -- cannot derive 2019-2020 for this source without it.")
                entry = {
                    "source": source,
                    "count_2019_onward": None,
                    "count_post_2021": None,
                    "post_2021_error": f"2019-onward probe itself failed: {onward_error}",
                    "derived_2019_2020_count": None,
                }
                derived_results = [r for r in derived_results if r["source"] != source]
                derived_results.append(entry)
                with open(OUT_PATH, "w", encoding="utf-8") as f:
                    json.dump(derived_results, f, indent=2, ensure_ascii=False)
                continue
            print(f"  -> {total_2019_onward:,} postings 2019 onward")

        print(f"Checking '{source}', post-2021 ({POST_2021_START} .. {TODAY})...")
        post_2021_count, error = probe_post_2021(client, source)

        if error:
            print(f"  -> FAILED: {error}")
            entry = {
                "source": source,
                "count_2019_onward": total_2019_onward,
                "count_post_2021": None,
                "post_2021_error": error,
                "derived_2019_2020_count": None,
            }
        else:
            derived_count = total_2019_onward - post_2021_count
            print(f"  -> {post_2021_count:,} postings post-2021. "
                  f"Derived 2019-2020 = {total_2019_onward:,} - {post_2021_count:,} = {derived_count:,}")
            entry = {
                "source": source,
                "count_2019_onward": total_2019_onward,
                "count_post_2021": post_2021_count,
                "post_2021_error": None,
                "derived_2019_2020_count": derived_count,
            }

        derived_results = [r for r in derived_results if r["source"] != source]
        derived_results.append(entry)
        with open(OUT_PATH, "w", encoding="utf-8") as f:
            json.dump(derived_results, f, indent=2, ensure_ascii=False)

    print(f"\nResults saved to {OUT_PATH}\n")
    print("=== Summary: DERIVED 2019-2020 counts (2019-onward minus post-2021) ===")
    for r in sorted(derived_results, key=lambda x: (x["derived_2019_2020_count"] is None,
                                                      -(x["derived_2019_2020_count"] or 0))):
        if r["post_2021_error"]:
            print(f"  {r['source']:<20} UNRESOLVED (post-2021 probe failed: {r['post_2021_error']})")
        else:
            print(f"  {r['source']:<20} {r['derived_2019_2020_count']:>12,} postings (derived)")


if __name__ == "__main__":
    main()
