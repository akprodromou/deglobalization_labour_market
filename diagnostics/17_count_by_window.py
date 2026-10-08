"""
Posting counts per CLOSED calendar window (year or month) for one source.

Why this exists: the open-ended probes in script 16 (min=<year>-01-01,
max=today) time out for OJA, the largest source, even for 2025+. A closed
window for OJA (2019-01-01..2020-12-31) did succeed earlier (407,545), so
for OJA we count narrower closed windows directly instead of subtracting
open-ended counts.

Usage, from the repo root:
    python -m diagnostics.17_count_by_window
    python -m diagnostics.17_count_by_window --source OJA --years 2019 2020 2021 2022 2023 2024 2025
    python -m diagnostics.17_count_by_window --granularity month --years 2020 2021

Only successful counts are saved (data/raw/window_counts.json), so a re-run
retries just the windows that failed. Each window is a separate probe, so a
timeout on one does not block the others.
"""

import argparse
import calendar
import json
from datetime import date
from pathlib import Path

from skillab_client import SkillabClient

OUT_PATH = Path("data/raw/window_counts.json")
DEFAULT_YEARS = [2019, 2020, 2021, 2022, 2023, 2024, 2025]


def build_windows(years, granularity, today=None):
    """[(label, start, end)] closed windows; windows after `today` are dropped
    and the window containing `today` ends at `today`."""
    today = today or date.today()
    windows = []
    for y in sorted(set(years)):
        if granularity == "year":
            spans = [(f"{y}", date(y, 1, 1), date(y, 12, 31))]
        else:
            spans = [
                (f"{y}-{m:02d}", date(y, m, 1), date(y, m, calendar.monthrange(y, m)[1]))
                for m in range(1, 13)
            ]
        for label, start, end in spans:
            if start > today:
                continue
            windows.append((label, start.isoformat(), min(end, today).isoformat()))
    return windows


def load_all():
    if not OUT_PATH.exists():
        return {}
    with open(OUT_PATH, encoding="utf-8") as f:
        return json.load(f)


def save_all(data):
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="OJA")
    parser.add_argument("--years", nargs="+", type=int, default=DEFAULT_YEARS)
    parser.add_argument("--granularity", choices=["year", "month"], default="year")
    args = parser.parse_args()

    windows = build_windows(args.years, args.granularity)
    data = load_all()
    source_counts = data.setdefault(args.source, {})
    client = SkillabClient()

    for label, start, end in windows:
        key = f"{start}..{end}"
        if key in source_counts:
            continue
        try:
            count = client.count_postings(args.source, min_upload_date=start, max_upload_date=end)
        except Exception as exc:
            print(f"  {label} ({key}): FAILED ({exc})")
            continue
        source_counts[key] = count
        save_all(data)
        print(f"  {label} ({key}): {count:,}")

    print(f"\n=== {args.source}: postings per {args.granularity} (closed windows) ===")
    total, missing = 0, 0
    for label, start, end in windows:
        count = source_counts.get(f"{start}..{end}")
        if count is None:
            missing += 1
            print(f"  {label:<8} ?")
        else:
            total += count
            print(f"  {label:<8} {count:>12,}")
    print(f"  {'sum':<8} {total:>12,}" + (f"   ({missing} window(s) unresolved; sum is a lower bound)" if missing else ""))
    print("\n'?' = probe failed; re-run to retry only the failed windows.")


if __name__ == "__main__":
    main()
