"""
Does the API keyword filter support wildcards (an asterisk) and multi-word
phrases, as the ESCOPlus 2.0 query suggests?

Kavargyris et al. retrieved their 54,000 software postings with the query
"software engineer*" OR "software" OR "software development" OR "software test*"
OR "software automat*" (Section 4 of the paper). Scripts 36 and 37 found that
the filter is case-insensitive and whole-token, that 'manager' returns 0 in
kariera.gr March 2026, and that the stem 'energ' returned 12 where 'energy'
returned 0. This probe tests whether a trailing asterisk changes anything.

  A. Exact word against the same word with an asterisk: software / software*,
     engineer / engineer*, manager / manager*, nurse / nurs*, energy / energ*.
  B. The paper's full query, as 'or' keywords, with and without asterisks.
  C. For each probe, among the first 100 returned postings: how many contain the
     keyword stem in the title and how many in the description (case-insensitive
     substring), and how many contain a longer word starting with the stem
     (a hit that only a prefix match could produce).

A count that rises when the asterisk is added means the asterisk is read as a
wildcard. Identical counts mean it is ignored or stripped. A count of 0 with the
asterisk means it is treated as part of the token.

Usage, from the repo root:
    python -m diagnostics.39_keyword_wildcard_probe
    python -m diagnostics.39_keyword_wildcard_probe --source lesjeudis.com --month 2024-10

Output: docs/keyword_wildcard_probe.md. About 14 requests of a few seconds each.
The default month, kariera.gr March 2026, is the one used in scripts 36 and 37,
so the results can be compared with them.
"""

import argparse
import calendar
import re
import time
from datetime import date
from pathlib import Path

REPORT_PATH = Path("docs/keyword_wildcard_probe.md")

PAPER_PLAIN = ["software engineer", "software", "software development", "software test", "software automat"]
PAPER_STAR = ["software engineer*", "software", "software development", "software test*", "software automat*"]

# (label, keywords, logic)
PROBES = [
    ("software", ["software"], None),
    ("software*", ["software*"], None),
    ("engineer", ["engineer"], None),
    ("engineer*", ["engineer*"], None),
    ("manager", ["manager"], None),
    ("manager*", ["manager*"], None),
    ("nurse", ["nurse"], None),
    ("nurs*", ["nurs*"], None),
    ("energy", ["energy"], None),
    ("energ*", ["energ*"], None),
    ("software engineer (phrase)", ["software engineer"], None),
    ("software engineer* (phrase)", ["software engineer*"], None),
    ("paper query without asterisks, or", PAPER_PLAIN, "or"),
    ("paper query with asterisks, or", PAPER_STAR, "or"),
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


def stems(kws):
    """Lower-case stems: asterisk removed, one stem per keyword."""
    return [k.lower().rstrip("*").strip() for k in kws if k.strip("* ")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="kariera.gr")
    ap.add_argument("--month", default="2026-03")
    args = ap.parse_args()

    from skillab_client import SkillabClient
    y, m = (int(x) for x in args.month.split("-"))
    lo, hi = date(y, m, 1).isoformat(), date(y, m, calendar.monthrange(y, m)[1]).isoformat()
    client = SkillabClient()

    L = [f"# Keyword wildcard probe: {args.source}, {args.month}", "",
         "| probe | keywords | logic | count | seconds | first 100: stem in title | stem in description | "
         "longer word starting with stem | note |",
         "|---|---|---|---:|---:|---:|---:|---:|---|"]
    for label, kws, logic in PROBES:
        try:
            count, items, dt, note = post(client, args.source, lo, hi, kws, logic)
        except Exception as exc:
            count, items, dt, note = None, [], 0.0, f"FAILED: {exc}"
        in_t = in_d = longer = "-"
        if items:
            st = stems(kws)
            title = [str(p.get("title") or "").lower() for p in items]
            desc = [str(p.get("description") or "").lower() for p in items]
            in_t = sum(1 for t in title if any(s in t for s in st))
            in_d = sum(1 for d in desc if any(s in d for s in st))
            pats = [re.compile(r"\b" + re.escape(s) + r"[^\W\d_]+", re.I) for s in st]
            longer = sum(1 for t, d in zip(title, desc) if any(p.search(t) or p.search(d) for p in pats))
        L.append(f"| {label} | {kws} | {logic or '-'} | {'-' if count is None else f'{count:,}'} | {dt:.0f} | "
                 f"{in_t} | {in_d} | {longer} | {note} |")
        print(L[-1])

    L += ["", "Reading: compare each word with its asterisk version. A higher count with the asterisk, together with "
          "hits in the last column (words such as 'softwares' or 'engineering' that only a prefix match can return), "
          "means the asterisk is a wildcard. The same count means it is ignored. Zero means it is part of the token. "
          "The two last rows show whether the paper's query works as written."]
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(L), encoding="utf-8")
    print(f"\nWritten: {REPORT_PATH}")


if __name__ == "__main__":
    main()
