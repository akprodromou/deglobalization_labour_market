"""
Per-source posting counts by time interval, derived from open-ended
count queries (min_upload_date=<year>-01-01, max_upload_date=today) -- the
query shape that has been reliable on this API, unlike closed historical
windows.

count(Y onward) never increases as Y increases, so the number of postings
in the interval [Y_i, Y_{i+1}) is count(Y_i) - count(Y_{i+1}). If the counts
for consecutive checkpoints are IDENTICAL, there are no postings between
those checkpoints; e.g. count(2019) == count(2021) == count(2023) means every
posting is dated 2023 or later.

Usage, from the repo root:
    python -m diagnostics.16_pinpoint_source_start_year
    python -m diagnostics.16_pinpoint_source_start_year --sources OJA --years 2019 2020 2021 2022 2023 2024 2025

Only successful counts are saved, so re-running retries just the probes that
failed or were never made.
"""

import argparse
import json
from datetime import date
from pathlib import Path

from skillab_client import SkillabClient

TODAY = date.today().isoformat()
DEFAULT_YEARS = [2019, 2021, 2023]
DEFAULT_SOURCES = [
    "brightminds", "eures", "eures-escox",
    "jobbguru", "jobbguru.se",
    "jobmedic", "jobmedic.co.uk",
    "jobscentral", "jobs.de",
    "kariera.fr", "kariera.gr",
    "lesjeudis", "lesjeudis.com",
]
OUT_PATH = Path("data/raw/source_start_year.json")


def load_counts():
    """{source: {year(int): count}} -- successful probes only."""
    if not OUT_PATH.exists():
        return {}
    with open(OUT_PATH, encoding="utf-8") as f:
        raw = json.load(f)
    counts = {}
    for source, entry in raw.items():
        year_counts = entry.get("year_counts", {})
        counts[source] = {int(y): c for y, c in year_counts.items() if c is not None}
    return counts


def save_counts(counts):
    raw = {
        source: {"year_counts": {str(y): c for y, c in sorted(year_map.items())}}
        for source, year_map in counts.items()
    }
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(raw, f, indent=2, ensure_ascii=False)


def probe_from_year(client, source, year):
    try:
        count = client.count_postings(source, min_upload_date=f"{year}-01-01", max_upload_date=TODAY)
        return count, None
    except Exception as exc:
        return None, str(exc)


def interval_counts(year_map, years):
    """[(label, count_or_None)] for [y_i, y_{i+1}) plus the open last interval."""
    ys = sorted(years)
    out = []
    for i, y in enumerate(ys):
        this_count = year_map.get(y)
        if i + 1 < len(ys):
            next_count = year_map.get(ys[i + 1])
            label = f"{y}-{ys[i + 1] - 1}"
            value = None if this_count is None or next_count is None else this_count - next_count
        else:
            label = f"{y}+"
            value = this_count
        out.append((label, value))
    return out


def format_value(value):
    if value is None:
        return "?"
    if value < 0:
        return f"{value:,} (!)"  # dataset grew between two queries
    return f"{value:,}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", nargs="+", default=DEFAULT_SOURCES)
    parser.add_argument("--years", nargs="+", type=int, default=DEFAULT_YEARS)
    args = parser.parse_args()
    years = sorted(set(args.years))

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    client = SkillabClient()
    counts = load_counts()

    for source in args.sources:
        year_map = counts.setdefault(source, {})
        missing = [y for y in years if y not in year_map]
        if not missing:
            print(f"{source}: all requested checkpoints already measured.")
            continue
        print(f"\n=== {source} ===")
        for year in missing:
            count, error = probe_from_year(client, source, year)
            if error:
                print(f"  {year}-01-01 onward: FAILED ({error})")
            else:
                print(f"  {year}-01-01 onward: {count:,}")
                year_map[year] = count
                save_counts(counts)

    print(f"\n=== Postings per interval (first checkpoint: {years[0]}; earlier postings are not counted) ===")
    for source in args.sources:
        year_map = counts.get(source, {})
        parts = [f"{label}: {format_value(value)}" for label, value in interval_counts(year_map, years)]
        total = year_map.get(years[0])
        total_text = f"{total:,}" if total is not None else "?"
        print(f"  {source:<16} since {years[0]}: {total_text:>10}  |  " + "  ".join(parts))
    print("\n'?' = a needed probe failed or is missing; re-run to retry. '(!)' = negative interval "
          "(the live dataset grew between two queries).")


if __name__ == "__main__":
    main()
