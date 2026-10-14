"""
What does GET /exploratory-analytics/jobs/skills-by-location return?

The API documentation lists the endpoint with the query parameters limit
(default 100, "number of (location_code, skill) pairs to include"), source,
occupation_id, location_code, skill_id, from_date and to_date, and shows the
response only as a list of generic objects. Before anything is built on it this
probe prints the raw response for one source and one month:

  A. the default call (limit=100): status, seconds, number of rows, the fields
     of the first row, and the first 10 rows as returned;
  B. limit=1000: does the row count grow (so 100 was a cap) or stay (so there
     are fewer pairs), and is there a maximum for `limit`;
  C. the same month with location_code set (default GR): rows for one country;
  D. a different month (default one month later), to see that the date filters
     change the result.

It also reports, for each call, the numeric fields found in the rows and whether
the rows are sorted by the first of them, descending (a sign that `limit` keeps
the most frequent pairs).

Usage, from the repo root:
    python -m diagnostics.41_skills_by_location_probe
    python -m diagnostics.41_skills_by_location_probe --source lesjeudis.com --month 2024-10 --location-code FR

Outputs: docs/skills_by_location_probe.md and the raw responses in
data/raw/skills_by_location_probe.json. Four requests. The default month,
kariera.gr March 2025, is one in which kariera.gr postings carry skill tags
(Report Section 9.7, item 11). A month with no tags should return nothing, which
is also worth knowing: use --month 2026-03 to check.
"""

import argparse
import calendar
import json
import time
from datetime import date
from pathlib import Path

REPORT_PATH = Path("docs/skills_by_location_probe.md")
RAW_PATH = Path("data/raw/skills_by_location_probe.json")
ENDPOINT = "/exploratory-analytics/jobs/skills-by-location"


def month_bounds(ym):
    y, m = (int(x) for x in ym.split("-"))
    return date(y, m, 1).isoformat(), date(y, m, calendar.monthrange(y, m)[1]).isoformat()


def next_month(ym):
    y, m = (int(x) for x in ym.split("-"))
    m += 1
    if m == 13:
        y, m = y + 1, 1
    return f"{y}-{m:02d}"


def call(client, params):
    from skillab_client import BASE_URL
    params = {k: v for k, v in params.items() if v not in (None, "")}
    t0 = time.time()
    r = client.session.get(f"{BASE_URL}{ENDPOINT}", params=params, timeout=600)
    dt = time.time() - t0
    try:
        body = r.json()
    except Exception:
        body = r.text[:500]
    return r.status_code, body, dt


def numeric_fields(row):
    return [k for k, v in row.items() if isinstance(v, (int, float)) and not isinstance(v, bool)]


def describe(label, params, status, body, dt):
    L = [f"## {label}", "", f"Parameters: `{json.dumps({k: v for k, v in params.items() if v not in (None, '')})}`", "",
         f"HTTP {status}, {dt:.0f} s.", ""]
    if status != 200:
        L += ["Response (first 500 characters):", "", f"    {str(body)[:500]}", ""]
        return L
    if not isinstance(body, list):
        L += [f"Response is a {type(body).__name__}, not a list. First 800 characters:", "",
              f"    {json.dumps(body)[:800]}", ""]
        return L
    L.append(f"Rows: **{len(body):,}**.")
    if body and isinstance(body[0], dict):
        first = body[0]
        L.append(f"Fields of the first row: `{list(first.keys())}`.")
        nums = numeric_fields(first)
        L.append(f"Numeric fields: `{nums}`.")
        if nums:
            vals = [r.get(nums[0]) for r in body if isinstance(r.get(nums[0]), (int, float))]
            desc = all(a >= b for a, b in zip(vals, vals[1:]))
            L.append(f"Sorted by `{nums[0]}` descending: **{'yes' if desc else 'no'}** "
                     f"(first {vals[0]:,}, last {vals[-1]:,}); sum of `{nums[0]}` over the rows: {sum(vals):,}.")
        for key in ("location_code", "location", "country"):
            if key in first:
                codes = sorted({str(r.get(key)) for r in body})
                L.append(f"Distinct `{key}` values: {len(codes)} ({', '.join(codes[:15])}{' ...' if len(codes) > 15 else ''}).")
                break
    L += ["", "First 10 rows as returned:", "", "```json", json.dumps(body[:10], indent=1, ensure_ascii=False), "```", ""]
    return L


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="kariera.gr")
    ap.add_argument("--month", default="2025-03")
    ap.add_argument("--location-code", default="GR")
    args = ap.parse_args()

    from skillab_client import SkillabClient
    client = SkillabClient()
    lo, hi = month_bounds(args.month)
    lo2, hi2 = month_bounds(next_month(args.month))

    calls = [
        ("A. Default limit", {"limit": 100, "source": args.source, "from_date": lo, "to_date": hi}),
        ("B. limit=1000", {"limit": 1000, "source": args.source, "from_date": lo, "to_date": hi}),
        (f"C. One country ({args.location_code})", {"limit": 100, "source": args.source,
                                                    "location_code": args.location_code, "from_date": lo, "to_date": hi}),
        (f"D. The next month ({next_month(args.month)})", {"limit": 100, "source": args.source,
                                                           "from_date": lo2, "to_date": hi2}),
    ]
    L = [f"# skills-by-location probe: {args.source}, {args.month}", ""]
    raw = {}
    for label, params in calls:
        try:
            status, body, dt = call(client, params)
        except Exception as exc:
            status, body, dt = "FAILED", str(exc), 0.0
        print(f"{label}: HTTP {status}, {dt:.0f} s, rows {len(body) if isinstance(body, list) else '-'}")
        raw[label] = {"params": params, "status": status, "seconds": dt, "body": body}
        L += describe(label, params, status, body, dt)

    L += ["Reading: compare the row counts of A and B (a cap or not), check whether the numeric field counts postings "
          "or skill mentions by comparing it with a known monthly total for the source (Report Section 9.3), and whether "
          "C and D differ from A. A month without tags should return an empty list."]
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(L), encoding="utf-8")
    RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
    RAW_PATH.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8")
    print(f"\nWritten: {REPORT_PATH} and {RAW_PATH}")


if __name__ == "__main__":
    main()
