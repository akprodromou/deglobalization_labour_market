"""
Does the API's own keyword filter give us exact population counts?

Script 35 can only count keywords in the 600 postings per month that script 33
sampled, and only in the title. The documented JobFilter also has `keywords` and
`keywords_logic` (Section "iter_postings" of skillab_client.py). If the server
searches title and description and returns the matching `count`, every exposed
group can be counted on the whole population, per month, with no sampling.

This probe finds out how the filter behaves before anything is built on it:
  1. which `keywords_logic` values are accepted ("and", "or", upper case ...);
  2. whether a keyword is matched in the title, the description, or both, and
     whether it is case-insensitive and matches word stems;
  3. how the count compares with the share found in the sample (script 35);
  4. how long a count request takes.

For each probe the script prints the count, the time, and for the first 100
returned postings how many contain the keyword in the title and in the
description (case-insensitive substring). A filter that matches the description
will show many postings with the word only in the description.

Usage, from the repo root:
    python -m diagnostics.36_keyword_filter_probe
    python -m diagnostics.36_keyword_filter_probe --source jobs.de --month 2024-10

Output: docs/keyword_filter_probe.md. Each probe is one request (20-70 s); the
default set is about 14 requests. Failed probes are reported, not retried.
"""

import argparse
import calendar
import time
from datetime import date
from pathlib import Path

REPORT_PATH = Path("docs/keyword_filter_probe.md")

# (label, keywords, keywords_logic or None)
PROBES = [
    ("no keyword (month total)", None, None),
    ("energy", ["energy"], None),
    ("nurse", ["nurse"], None),
    ("driver", ["driver"], None),
    ("hotel", ["hotel"], None),
    ("energy, logic=or with nurse", ["energy", "nurse"], "or"),
    ("energy, logic=and with nurse", ["energy", "nurse"], "and"),
    ("energy, logic=OR with nurse", ["energy", "nurse"], "OR"),
    ("ENERGY (upper case)", ["ENERGY"], None),
    ("energ (stem)", ["energ"], None),
]


def post(client, source, lo, hi, kws, logic):
    from skillab_client import BASE_URL, JOBS_ENDPOINT
    form = {"sources": [source], "min_upload_date": lo, "max_upload_date": hi}
    if kws:
        form["keywords"] = kws
    if logic:
        form["keywords_logic"] = logic
    t0 = time.time()
    r = client.session.post(f"{BASE_URL}{JOBS_ENDPOINT}", params={"page": 1, "page_size": 100}, data=form, timeout=240)
    dt = time.time() - t0
    if r.status_code != 200:
        return None, [], dt, f"HTTP {r.status_code}: {r.text[:120]}"
    j = r.json()
    return j.get("count"), j.get("items", []), dt, ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="kariera.gr")
    ap.add_argument("--month", default="2026-03")
    args = ap.parse_args()

    from skillab_client import SkillabClient
    y, m = (int(x) for x in args.month.split("-"))
    lo, hi = date(y, m, 1).isoformat(), date(y, m, calendar.monthrange(y, m)[1]).isoformat()
    client = SkillabClient()

    L = [f"# Keyword filter probe: {args.source}, {args.month}", "",
         "| probe | keywords | logic | count | seconds | first 100: keyword in title | in description | in description only | note |",
         "|---|---|---|---:|---:|---:|---:|---:|---|"]
    for label, kws, logic in PROBES:
        try:
            count, items, dt, note = post(client, args.source, lo, hi, kws, logic)
        except Exception as exc:
            count, items, dt, note = None, [], 0.0, f"FAILED: {exc}"
        in_t = in_d = only_d = "-"
        if kws and items:
            words = [k.lower() for k in kws]
            tt = [any(w in str(p.get("title") or "").lower() for w in words) for p in items]
            dd = [any(w in str(p.get("description") or "").lower() for w in words) for p in items]
            in_t, in_d = sum(tt), sum(dd)
            only_d = sum(1 for a, b in zip(tt, dd) if b and not a)
        L.append(f"| {label} | {kws or '-'} | {logic or '-'} | {'-' if count is None else f'{count:,}'} | {dt:.0f} | "
                 f"{in_t} | {in_d} | {only_d} | {note} |")
        print(L[-1])
    L += ["", "Reading: a count that falls when `and` is used and rises when `or` is used means the logic parameter "
          "works as named; a large 'in description only' column means the filter searches the description; "
          "identical counts for 'energy', 'ENERGY' and the other cases show case-insensitivity or its absence; "
          "'energ' matching more than 'energy' shows stem matching."]
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(L), encoding="utf-8")
    print(f"\nWritten: {REPORT_PATH}")


if __name__ == "__main__":
    main()
