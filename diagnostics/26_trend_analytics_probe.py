"""
Independent check of our counts using the API's own aggregation endpoint.

Why: all our coverage numbers come from POST /jobs filtered counts. The API docs
also list GET /api/trend-analytics/jobs/skills-by-location, described as "job
counts per month by location code" with optional ?source=, ?from_date=,
?to_date=, ?location_code=, ?occupation_id= and ?limit= (default 100 rows). It
aggregates on the server, so it needs no pagination and can show a source's whole
time profile in one call. If its monthly numbers agree with ours, our querying is
right and the empty years are real. If they disagree, our queries are wrong.

Reference values from our own queries, for comparison:
  OJA 2024-01 total            276,271      OJA 2019 total       213,934
  eures 2026-01 / 2026-02       99,040 / 260,801
  eures-escox 2026-01 / 02     130,336 / 698,188
  jobbland.se 2019-2020             90 postings in total

Usage, from the repo root (credentials in env vars):
    python -m diagnostics.26_trend_analytics_probe
    python -m diagnostics.26_trend_analytics_probe --sources OJA eures kariera.gr --limit 20000
    python -m diagnostics.26_trend_analytics_probe --sources OJA --from-date 2024-01-01 --to-date 2024-01-31

The response shape is not documented, so the script saves each raw response to
data/raw/trend_<source>.json, prints the first rows, and tries to sum a month
field and a count field into per-year totals. If it cannot recognise the shape it
says so, and the printed sample is what to paste back.
"""

import argparse
import json
import re
import time
from collections import Counter, defaultdict
from pathlib import Path

from skillab_client import BASE_URL, SkillabClient

ENDPOINT = "/trend-analytics/jobs/skills-by-location"
MONTH = re.compile(r"^(\d{4})-(\d{2})")
COUNT_NAMES = ("freq", "count", "job_count", "jobs", "jobs_count", "n", "total", "value")
# the 16 job sources found earlier; used if GET /jobs/sources times out
KNOWN_SOURCES = ["OJA", "eures", "eures-escox", "kariera.gr", "jobbland.se", "jobbland", "jobs.de",
                 "kariera.fr", "lesjeudis.com", "lesjeudis", "jobmedic.co.uk", "jobmedic",
                 "jobscentral", "jobbguru.se", "jobbguru", "brightminds"]
ATTEMPTS = 3


def fetch(client, source, limit, from_date, to_date):
    params = {"source": source, "limit": limit}
    if from_date:
        params["from_date"] = from_date
    if to_date:
        params["to_date"] = to_date
    last = None
    for attempt in range(1, ATTEMPTS + 1):
        try:
            return client.session.get(f"{BASE_URL}{ENDPOINT}", params=params, timeout=180)
        except Exception as exc:
            last = exc
            print(f"  attempt {attempt}/{ATTEMPTS} failed: {exc}")
            time.sleep(5 * attempt)
    raise last


def rows_of(payload):
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("items", "data", "results", "rows"):
            if isinstance(payload.get(key), list):
                return payload[key]
    return None


def parse_month(value):
    """'2024-01...' or '01/2024' -> '2024-01', else None."""
    if not isinstance(value, str):
        return None
    m = MONTH.match(value)
    if m:
        return f"{m.group(1)}-{m.group(2)}"
    m = re.match(r"^(\d{2})/(\d{4})$", value.strip())
    if m:
        return f"{m.group(2)}-{m.group(1)}"
    return None


def find_month_and_count(row):
    month = next((parse_month(v) for v in row.values() if parse_month(v)), None)
    lowered = {k.lower(): v for k, v in row.items()}
    count = next((lowered[k] for k in COUNT_NAMES
                  if isinstance(lowered.get(k), (int, float)) and not isinstance(lowered.get(k), bool)), None)
    if count is None:
        ints = [v for v in row.values() if isinstance(v, (int, float)) and not isinstance(v, bool)]
        count = ints[0] if len(ints) == 1 else None
    return month, count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", nargs="+", default=None, help="default: all job sources")
    parser.add_argument("--limit", type=int, default=20000)
    parser.add_argument("--from-date")
    parser.add_argument("--to-date")
    args = parser.parse_args()

    client = SkillabClient()
    sources = args.sources
    if not sources:
        try:
            sources = client.get_job_sources()
        except Exception as exc:
            print(f"Could not list sources ({exc}); using the 16 known ones.")
            sources = KNOWN_SOURCES
    Path("data/raw").mkdir(parents=True, exist_ok=True)

    for source in sources:
        print(f"\n=== {source} ===")
        try:
            r = fetch(client, source, args.limit, args.from_date, args.to_date)
        except Exception as exc:
            print(f"  request failed: {exc}")
            continue
        print(f"  HTTP {r.status_code}")
        if r.status_code != 200:
            print(f"  body: {r.text[:300]}")
            continue
        payload = r.json()
        safe = re.sub(r"[^A-Za-z0-9_.-]", "_", source)
        Path(f"data/raw/trend_{safe}.json").write_text(json.dumps(payload), encoding="utf-8")
        rows = rows_of(payload)
        if rows is None:
            print(f"  unrecognised top level ({type(payload).__name__}); first 400 chars: {str(payload)[:400]}")
            continue
        print(f"  rows returned: {len(rows):,}" + ("  (equals --limit: raise it)" if len(rows) >= args.limit else ""))
        for row in rows[:2]:
            print(f"  sample row: {json.dumps(row, ensure_ascii=False)[:300]}")
        by_year, by_month, unmatched = Counter(), defaultdict(int), 0
        for row in rows:
            if not isinstance(row, dict):
                unmatched += 1
                continue
            month, count = find_month_and_count(row)
            if month is None or count is None:
                unmatched += 1
                continue
            by_year[month[:4]] += count
            by_month[month[:7]] += count
        if by_year:
            print("  per-year totals: " + ", ".join(f"{y}: {c:,}" for y, c in sorted(by_year.items())))
            first, last = min(by_month), max(by_month)
            print(f"  first month with data: {first}; last: {last}; months with data: {len(by_month)}")
        if unmatched:
            print(f"  rows not recognised (no month/count found): {unmatched:,}")
        if not by_year:
            print("  shape not recognised; paste the sample rows above")


if __name__ == "__main__":
    main()
