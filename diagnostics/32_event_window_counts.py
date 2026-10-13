"""
Monthly posting counts around two candidate events, per source.

Events:
  * US "Liberation Day" tariffs, 2 Apr 2025  -> months 2025-01 .. 2025-08
  * Iran war / oil shock, 28 Feb 2026        -> months 2025-11 .. 2026-05

For each source and month this records the number of dated postings (closed
calendar window, the same probe as script 17). The point is to see, before we
commit to an event design, (a) whether each source has data on both sides of the
event and (b) whether the monthly volume jumps for collection reasons right at
the event date.

Usage, from the repo root (credentials in .env or env vars):
    python -m diagnostics.32_event_window_counts
    python -m diagnostics.32_event_window_counts --sources lesjeudis.com kariera.gr
    python -m diagnostics.32_event_window_counts --event tariffs
    python -m diagnostics.32_event_window_counts --sources kariera.gr jobbland.se lesjeudis.com --range 2024-08 2026-10

Resumable: successful counts are kept in data/raw/event_window_counts.json, so a
re-run retries only failed windows (the server drops some requests; just re-run).
Output: docs/event_window_counts.md
"""

import argparse
import calendar
import json
from datetime import date
from pathlib import Path

from skillab_client import SkillabClient

OUT_PATH = Path("data/raw/event_window_counts.json")
REPORT_PATH = Path("docs/event_window_counts.md")

DEFAULT_SOURCES = ["lesjeudis.com", "lesjeudis", "kariera.gr", "kariera.fr",
                   "jobs.de", "jobbland.se", "jobbland", "eures"]

EVENTS = {
    "tariffs": ("US tariffs, 2 Apr 2025", date(2025, 4, 2), (2025, 1), (2025, 8)),
    "oil": ("Iran war / oil shock, 28 Feb 2026", date(2026, 2, 28), (2025, 11), (2026, 5)),
}


def months(start, end):
    y, m = start
    while (y, m) <= end:
        yield y, m
        m += 1
        if m == 13:
            y, m = y + 1, 1


def load():
    return json.loads(OUT_PATH.read_text(encoding="utf-8")) if OUT_PATH.exists() else {}


def save(data):
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sources", nargs="+", default=DEFAULT_SOURCES)
    ap.add_argument("--event", choices=list(EVENTS) + ["both"], default="both")
    ap.add_argument("--range", nargs=2, metavar=("START", "END"),
                    help="instead of the two events: every month from START to END (YYYY-MM)")
    args = ap.parse_args()

    if args.range:
        a = tuple(int(x) for x in args.range[0].split("-"))
        b = tuple(int(x) for x in args.range[1].split("-"))
        EVENTS["range"] = (f"Monthly counts {args.range[0]} to {args.range[1]}", None, a, b)
        chosen = ["range"]
    else:
        chosen = list(EVENTS) if args.event == "both" else [args.event]
    wanted = sorted({ym for e in chosen for ym in months(EVENTS[e][2], EVENTS[e][3])})
    data = load()
    client = SkillabClient()
    today = date.today()

    for src in args.sources:
        store = data.setdefault(src, {})
        for y, m in wanted:
            start = date(y, m, 1)
            if start > today:
                continue
            key = f"{y}-{m:02d}"
            if key in store:
                continue
            end = min(date(y, m, calendar.monthrange(y, m)[1]), today)
            try:
                store[key] = client.count_postings(src, start.isoformat(), end.isoformat())
            except Exception as exc:
                print(f"  {src} {key}: FAILED ({exc})")
                continue
            save(data)
            print(f"  {src} {key}: {store[key]:,}")

    lines = ["# Monthly posting counts around candidate events", "",
             "Dated postings per closed calendar month. `?` = probe failed, re-run to retry. "
             "Counts reflect collection as well as the labour market; read them as coverage, not demand.", ""]
    for e in chosen:
        label, when, a, b = EVENTS[e]
        cols = list(months(a, b))
        lines += [f"## {label}", "",
                  "| source | " + " | ".join(f"{y}-{m:02d}" for y, m in cols) + " |",
                  "|---|" + "---:|" * len(cols)]
        for src in args.sources:
            row = []
            for y, m in cols:
                v = data.get(src, {}).get(f"{y}-{m:02d}")
                row.append("?" if v is None else f"{v:,}")
            lines.append(f"| {src} | " + " | ".join(row) + " |")
        lines.append("")
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print(f"\nWritten: {REPORT_PATH}")


if __name__ == "__main__":
    main()
