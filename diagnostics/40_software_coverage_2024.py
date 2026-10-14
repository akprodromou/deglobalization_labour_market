"""
Are there postings from January to July 2024 in the scraped boards?

The ESCOPlus 2.0 paper (Kavargyris et al.) describes a corpus collected between
January 2024 and December 2025 from kariera.gr, LesJeudis, Jobs.de, karieragroup
and Jobbland. Our closed-window counts (Report Section 9.3) show nothing dated
before August 2024 on these boards. This probe checks the months January 2024 to
September 2024, source by source, with two counts per month:

  1. all postings dated in the month (no keyword), and
  2. postings dated in the month that match the keyword 'software' (and, with
     --keywords, any other keywords), which is the filter the paper used.

If the paper's earlier months exist, they must appear here. If both counts are 0
for January to July, the paper's range refers to something else (for example the
date the corpus was retrieved) and the question goes to the supervisor.

Sources are given by their Tracker names; check `docs/coverage_population.md`
for the exact spellings. 'karieragroup' in the paper is probably kariera.fr, but
that is a guess, so kariera.fr is included and the output says nothing about it.

Usage, from the repo root:
    python -m diagnostics.40_software_coverage_2024
    python -m diagnostics.40_software_coverage_2024 --range 2023-01 2024-12
    python -m diagnostics.40_software_coverage_2024 --keywords software developer

Output: docs/software_coverage_2024.md. Counts without a keyword took about
25 seconds in earlier probes, counts with a keyword 1-4 seconds; the default
(5 sources x 9 months x 2 counts) is 90 requests and takes about 15-20 minutes.
Failed counts are reported as '?', not retried.
"""

import argparse
import calendar
import time
from datetime import date
from pathlib import Path

REPORT_PATH = Path("docs/software_coverage_2024.md")
DEFAULT_SOURCES = ["kariera.gr", "lesjeudis.com", "jobs.de", "kariera.fr", "jobbland.se"]


def months(start, end):
    y, m = (int(x) for x in start.split("-"))
    ey, em = (int(x) for x in end.split("-"))
    while (y, m) <= (ey, em):
        yield y, m
        m += 1
        if m == 13:
            y, m = y + 1, 1


def count(client, source, lo, hi, kws=None):
    from skillab_client import BASE_URL, JOBS_ENDPOINT
    form = {"sources": [source], "min_upload_date": lo, "max_upload_date": hi}
    if kws:
        form["keywords"] = kws
        form["keywords_logic"] = "or"
    for size in (1, 10, 100):  # smallest page the server accepts; only `count` is used
        try:
            r = client.session.post(f"{BASE_URL}{JOBS_ENDPOINT}", params={"page": 1, "page_size": size},
                                    data=form, timeout=240)
        except Exception:
            return None
        if r.status_code == 200:
            return r.json().get("count")
    return None


def fmt(n):
    return "?" if n is None else f"{n:,}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sources", nargs="+", default=DEFAULT_SOURCES)
    ap.add_argument("--range", nargs=2, default=["2024-01", "2024-09"], metavar=("START", "END"))
    ap.add_argument("--keywords", nargs="+", default=["software"])
    args = ap.parse_args()

    from skillab_client import SkillabClient
    client = SkillabClient()
    ms = list(months(*args.range))

    L = [f"# Coverage of {args.range[0]} to {args.range[1]}, all postings and keyword {args.keywords}", "",
         "Each cell is `all / keyword`: postings dated in the month, and those matching the keyword filter "
         "(logic 'or'). '?' means the request failed.", "",
         "| month | " + " | ".join(args.sources) + " |", "|---|" + "---:|" * len(args.sources)]
    rows = {}
    for (y, mo) in ms:
        lo, hi = date(y, mo, 1).isoformat(), date(y, mo, calendar.monthrange(y, mo)[1]).isoformat()
        cells = []
        for s in args.sources:
            t0 = time.time()
            a = count(client, s, lo, hi)
            k = count(client, s, lo, hi, args.keywords)
            cells.append(f"{fmt(a)} / {fmt(k)}")
            print(f"{y}-{mo:02d} {s}: {cells[-1]}  ({time.time() - t0:.0f}s)")
        rows[(y, mo)] = cells
        L.append(f"| {y}-{mo:02d} | " + " | ".join(cells) + " |")
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)  # write as we go: a long run can be stopped
        REPORT_PATH.write_text("\n".join(L), encoding="utf-8")

    L += ["", "Reading: a month with 0 / 0 in a source has no postings dated in it in the Tracker. If January to July "
          "2024 are all 0 / 0 in the boards the paper names, its stated range does not match the `upload_date` we "
          "can query, and the supervisor should be asked which date the paper used."]
    REPORT_PATH.write_text("\n".join(L), encoding="utf-8")
    print(f"\nWritten: {REPORT_PATH}")


if __name__ == "__main__":
    main()
