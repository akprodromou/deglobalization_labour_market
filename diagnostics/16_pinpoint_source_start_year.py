"""
15_derive_2019_2020_by_subtraction.py found that 7 sources have IDENTICAL
counts for '2019 onward' and 'post-2021 onward' -- strong evidence their
real data starts somewhere at or after 2021-01-01, not 2019 as the
original coverage check's "2019 onward: Yes" label implied (that label
was technically true but misleading for the brief's specific 2019-2020
baseline-window purpose).

This pins down the actual start year for every source using the SAME
reliable open-ended query pattern (min_upload_date=X-01-01, max=today),
by checking each year boundary 2019-2023 individually. Once two
consecutive years give the same count, that's the floor -- no need to
probe further back.
"""

import json
from datetime import date
from pathlib import Path

from skillab_client import SkillabClient

TODAY = date.today().isoformat()
# 3 checkpoints rather than 5: enough to triangulate roughly when data
# starts without doubling the number of API calls. OJA, jobbland, and
# jobbland.se are excluded -- 15_derive_2019_2020_by_subtraction.py
# already confirmed they have real 2019-2020 data, so there's nothing to
# pinpoint for them.
CANDIDATE_YEARS = [2019, 2021, 2023]

ALL_JOB_SOURCES = [
    "brightminds", "eures", "eures-escox",
    "jobbguru", "jobbguru.se",
    "jobmedic", "jobmedic.co.uk",
    "jobscentral", "jobs.de",
    "kariera.fr", "kariera.gr",
    "lesjeudis", "lesjeudis.com",
]

OUT_PATH = Path("data/raw/source_start_year.json")


def load_existing():
    if OUT_PATH.exists():
        with open(OUT_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save(results):
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


def probe_from_year(client, source, year):
    try:
        count = client.count_postings(source, min_upload_date=f"{year}-01-01", max_upload_date=TODAY)
        return count, None
    except Exception as exc:
        return None, str(exc)


def main():
    client = SkillabClient()
    results = load_existing()

    for source in ALL_JOB_SOURCES:
        if source in results and results[source].get("resolved"):
            print(f"Skipping '{source}' (already resolved: starts {results[source]['earliest_year_with_data']}).")
            continue

        print(f"\n=== {source} ===")
        year_counts = {}
        for year in CANDIDATE_YEARS:
            count, error = probe_from_year(client, source, year)
            if error:
                print(f"  {year}-01-01 onward: FAILED ({error})")
                year_counts[year] = None
            else:
                print(f"  {year}-01-01 onward: {count:,}")
                year_counts[year] = count

        # Determine the earliest year where the count differs from the
        # NEXT year checked (i.e. where real data starts accumulating).
        resolved_counts = {y: c for y, c in year_counts.items() if c is not None}
        earliest_year_with_data = None
        sorted_years = sorted(resolved_counts.keys())
        for i, year in enumerate(sorted_years):
            if i == 0:
                continue
            prev_year = sorted_years[i - 1]
            if resolved_counts[year] != resolved_counts[prev_year]:
                earliest_year_with_data = prev_year
                break
        if earliest_year_with_data is None and sorted_years:
            # No plateau found within the probed years -- data may start
            # before the earliest year checked (2019) or we simply
            # couldn't tell from this range.
            if len(sorted_years) >= 2 and resolved_counts[sorted_years[0]] > 0:
                earliest_year_with_data = f"<={sorted_years[0]}"

        results[source] = {
            "year_counts": year_counts,
            "earliest_year_with_data": earliest_year_with_data,
            "resolved": len(resolved_counts) == len(CANDIDATE_YEARS),
        }
        save(results)

    print("\n=== Summary: earliest year each source has real data ===")
    for source, r in results.items():
        print(f"  {source:<20} earliest year with data: {r['earliest_year_with_data']}")


if __name__ == "__main__":
    main()
