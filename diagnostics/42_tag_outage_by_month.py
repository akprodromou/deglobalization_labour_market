"""
When do the skill tags stop? Population-level, per source and month.

Script 34 measured tag fill on samples. Script 41 showed that
GET /exploratory-analytics/jobs/skills-by-location returns, from the whole
population and within seconds, the most frequent (country, skill) pairs of a
source and date window, with `Freq` apparently the number of postings that carry
the skill (March 2025, kariera.gr: 'communication' 396 of about 2,884 postings
= 13.7%; April 2025: 198 of 1,458 = 13.6%).

For each source and month this script makes two calls:
  1. limit=1: the single most frequent (country, skill) pair, its count and name;
  2. limit=1 with a fixed skill_id (default: ESCO 'communication'): how many
     postings carry that one skill, which is comparable from month to month.
It divides both by the month's posting total (the closed-window counts of Report
Section 9.9, built into TOTALS below; a month missing from TOTALS has no ratio).
A month where the tags stop shows an empty result, or a count near 0, while the
posting total stays high.

Caveats: the ratio is a proxy for tag fill, not tag fill itself, because a posting
can be tagged without carrying 'communication'; and `Freq` counting postings is an
inference from script 41, not documented. The cut-off month is read from where
the fixed-skill count falls to 0 with a large posting total.

Usage, from the repo root:
    python -m diagnostics.42_tag_outage_by_month
    python -m diagnostics.42_tag_outage_by_month --sources kariera.gr --range 2025-09 2026-04

Output: docs/tag_outage_by_month.md; raw results are cached in
data/raw/tag_outage_by_month.json, so an interrupted run resumes. About
(sources x months x 2) calls of 1-10 s: 5 sources over 27 months is roughly
270 calls, 10-30 minutes.
"""

import argparse
import json
import time
from pathlib import Path

REPORT_PATH = Path("docs/tag_outage_by_month.md")
CACHE_PATH = Path("data/raw/tag_outage_by_month.json")
ENDPOINT = "/exploratory-analytics/jobs/skills-by-location"
COMMUNICATION = "http://data.europa.eu/esco/skill/15d76317-c71a-4fa2-aadc-2ecc34e627b7"
DEFAULT_SOURCES = ["kariera.gr", "lesjeudis.com", "jobbland.se", "jobs.de", "kariera.fr"]

# Posting totals per month, from Section 9.9 of the report (closed-window counts), starting August 2024.
TOTALS_FROM = (2024, 8)
TOTALS = {
    "kariera.gr": [2738, 5629, 5480, 5593, 4866, 7065, 3174, 2884, 1458, 4219, 4678, 4097, 3510, 1703, 61, 37,
                   3308, 7112, 6542, 6953, 6659, 0],
    "lesjeudis.com": [5660, 6649, 4935, 3986, 3511, 4191, 1548, 450, 581, 2336, 3887, 800, 3383, 3279, 1476, 738,
                      386, 250, 6561, 768, 0],
    "jobbland.se": [4184, 10034, 48018, 50097, 47151, 53139, 23017, 10959, 4139, 6210, 132, 460, 3066, 3968, 1520,
                    3618, 28639, 48511, 55457, 62392, 47721, 53794, 46127, 31166, 40875, 595, 0],
    "jobs.de": [3427, 5632, 8175, 6417, 4029, 1690, 2572, 1691, 597],
    "kariera.fr": [3000, 27099, 32892, 7043, 4941, 6054, 4916, 523, 0],
}


def month_list(start, end):
    y, m = (int(x) for x in start.split("-"))
    ey, em = (int(x) for x in end.split("-"))
    while (y, m) <= (ey, em):
        yield f"{y}-{m:02d}"
        m += 1
        if m == 13:
            y, m = y + 1, 1


def month_bounds(ym):
    import calendar
    from datetime import date
    y, m = (int(x) for x in ym.split("-"))
    return date(y, m, 1).isoformat(), date(y, m, calendar.monthrange(y, m)[1]).isoformat()


def total_for(source, ym):
    series = TOTALS.get(source)
    if not series:
        return None
    y, m = (int(x) for x in ym.split("-"))
    idx = (y - TOTALS_FROM[0]) * 12 + (m - TOTALS_FROM[1])
    return series[idx] if 0 <= idx < len(series) else None


def call(client, params):
    from skillab_client import BASE_URL
    try:
        r = client.session.get(f"{BASE_URL}{ENDPOINT}", params=params, timeout=600)
    except Exception as exc:
        return None, f"FAILED: {exc}"
    if r.status_code != 200:
        return None, f"HTTP {r.status_code}: {r.text[:100]}"
    try:
        body = r.json()
    except Exception:
        return None, "not JSON"
    return body, ""


def pct(n, tot):
    return "-" if n is None or not tot else f"{100 * n / tot:.1f}%"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sources", nargs="+", default=DEFAULT_SOURCES)
    ap.add_argument("--range", nargs=2, default=["2024-08", "2026-10"], metavar=("START", "END"))
    ap.add_argument("--skill-id", default=COMMUNICATION)
    args = ap.parse_args()

    from skillab_client import SkillabClient
    client = SkillabClient()
    cache = json.loads(CACHE_PATH.read_text(encoding="utf-8")) if CACHE_PATH.exists() else {}
    months = list(month_list(*args.range))

    for s in args.sources:
        for ym in months:
            key = f"{s}|{ym}|{args.skill_id}"
            if key in cache and cache[key].get("ok"):
                continue
            lo, hi = month_bounds(ym)
            t0 = time.time()
            top, e1 = call(client, {"limit": 1, "source": s, "from_date": lo, "to_date": hi})
            fixed, e2 = call(client, {"limit": 1, "source": s, "from_date": lo, "to_date": hi,
                                      "skill_id": args.skill_id})
            ok = top is not None and fixed is not None
            cache[key] = {
                "ok": ok, "err": e1 or e2,
                "top_label": top[0].get("label") if top else None,
                "top_freq": top[0].get("Freq") if top else None,
                "top_code": top[0].get("location_code") if top else None,
                "fixed_freq": (sum(r.get("Freq", 0) for r in fixed) if fixed is not None else None),
            }
            print(f"{s} {ym}: top {cache[key]['top_label']} {cache[key]['top_freq']}, fixed {cache[key]['fixed_freq']} "
                  f"({time.time() - t0:.0f}s) {cache[key]['err']}")
            CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
            CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")

    L = ["# Skill tags by source and month (population level)", "",
         f"Fixed skill: `{args.skill_id}`. 'Postings' are the closed-window counts of Report Section 9.9. "
         "'Top skill' is the most frequent (country, skill) pair of the month. Shares are Freq divided by postings; "
         "'-' means no posting total is available or the request failed.", ""]
    for s in args.sources:
        L += [f"## {s}", "", "| month | postings | top skill (country) | top Freq | top share | fixed-skill Freq | fixed share |",
              "|---|---:|---|---:|---:|---:|---:|"]
        last_tagged = None
        for ym in months:
            c = cache.get(f"{s}|{ym}|{args.skill_id}")
            tot = total_for(s, ym)
            if not c or not c.get("ok"):
                L.append(f"| {ym} | {tot if tot is not None else '-'} | request failed | - | - | - | - |")
                continue
            tf, ff = c["top_freq"], c["fixed_freq"]
            if ff:
                last_tagged = ym
            tot_txt = "-" if tot is None else f"{tot:,}"
            label = c["top_label"] or "(none)"
            if c["top_code"]:
                label += " (" + str(c["top_code"]) + ")"
            tf_txt = "-" if tf is None else str(tf)
            ff_txt = "-" if ff is None else str(ff)
            L.append(f"| {ym} | {tot_txt} | {label} | {tf_txt} | {pct(tf, tot)} | {ff_txt} | {pct(ff, tot)} |")
        L += ["", f"Last month with a non-zero fixed-skill count in this range: **{last_tagged or 'none'}**.", ""]
    L += ["Reading: a month with a large posting total and 0 or '(none)' has no skill tags. A share that moves slowly "
          "from month to month is a stable tag rate. A share that falls sharply while the total stays high means "
          "tagging thinned out before it stopped. The shares for months with a very small total (a few dozen "
          "postings) are not reliable."]
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(L), encoding="utf-8")
    print(f"\nWritten: {REPORT_PATH}")


if __name__ == "__main__":
    main()
