"""
Two cheap checks for any 2019-2020 data outside OJA.

Part A (API): do any sources hold postings with NO upload_date? A date-windowed
query (ours, and the trend endpoint) cannot see them. For each non-OJA source it
prints the count with no date filter and the count with a 1900-2100 window; the
difference is the number of postings without an upload_date.

Part B (local, no API calls): profiles have a `startdate` (the start of the
person's role). From data/raw/profiles_sample.jsonl it shows how many profiles
have one, from which years, by source, and how many fall in 2019-2020. A sample
of ~7,000 profiles says whether the field is worth pursuing; it does not give
population counts (ProfileFilter has no date filter, so a population count means
paging through profiles).

Usage, from the repo root (credentials in env vars for Part A):
    python -m diagnostics.29_alternative_baseline_checks
    python -m diagnostics.29_alternative_baseline_checks --skip-api
    python -m diagnostics.29_alternative_baseline_checks --sources eures kariera.gr
"""

import argparse
import json
import re
import time
from collections import Counter, defaultdict
from pathlib import Path

PROFILES_PATH = Path("data/raw/profiles_sample.jsonl")
SOURCES = ["eures", "eures-escox", "kariera.gr", "kariera.fr", "jobbland.se", "jobbland", "jobs.de",
           "lesjeudis.com", "lesjeudis", "jobmedic.co.uk", "jobmedic", "jobscentral",
           "jobbguru.se", "jobbguru", "brightminds"]


def count(client, source, lo=None, hi=None, attempts=3):
    from skillab_client import BASE_URL, JOBS_ENDPOINT
    form = {"sources": [source]}
    if lo:
        form["min_upload_date"] = lo
    if hi:
        form["max_upload_date"] = hi
    last = None
    for i in range(1, attempts + 1):
        try:
            r = client.session.post(f"{BASE_URL}{JOBS_ENDPOINT}", params={"page": 1, "page_size": 100},
                                    data=form, timeout=120)
            r.raise_for_status()
            return r.json().get("count", 0)
        except Exception as exc:
            last = exc
            time.sleep(5 * i)
    raise last


def part_a(sources):
    from skillab_client import SkillabClient
    client = SkillabClient()
    print("PART A: postings with no upload_date (no date filter minus 1900-2100 window)\n")
    print(f"{'source':<16}{'no date filter':>16}{'1900-2100':>14}{'no upload_date':>16}")
    for s in sources:
        try:
            a = count(client, s)
        except Exception as exc:
            print(f"{s:<16}  all-time count FAILED ({exc})")
            continue
        try:
            b = count(client, s, "1900-01-01", "2100-12-31")
        except Exception as exc:
            print(f"{s:<16}{a:>16,}  windowed count FAILED ({exc})")
            continue
        print(f"{s:<16}{a:>16,}{b:>14,}{a - b:>16,}")
    print("\nA positive last column means postings that no date-windowed query can reach.")


def part_b():
    print("\nPART B: profile `startdate` in the local sample\n")
    if not PROFILES_PATH.exists():
        print(f"  {PROFILES_PATH} not found")
        return
    by_source = defaultdict(lambda: {"n": 0, "with": 0, "years": Counter(), "ctry_1920": Counter()})
    with open(PROFILES_PATH, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            p = json.loads(line)
            d = by_source[p.get("source")]
            d["n"] += 1
            m = re.match(r"^(\d{4})", str(p.get("startdate") or ""))
            if m:
                d["with"] += 1
                d["years"][m.group(1)] += 1
                if m.group(1) in ("2019", "2020"):
                    d["ctry_1920"][p.get("country") or p.get("user_country") or "?"] += 1
    total_with, total_1920 = 0, 0
    for s, d in sorted(by_source.items(), key=lambda kv: -kv[1]["n"]):
        yrs = d["years"]
        n1920 = yrs["2019"] + yrs["2020"]
        total_with += d["with"]
        total_1920 += n1920
        top = ", ".join(f"{y}: {c}" for y, c in sorted(yrs.items())[:12]) or "none"
        print(f"  {s}: {d['n']:,} profiles, {d['with']:,} with startdate ({100 * d['with'] / d['n']:.1f}%); "
              f"2019-2020: {n1920}")
        print(f"      years: {top}")
        if d["ctry_1920"]:
            print(f"      2019-2020 by country: {dict(d['ctry_1920'].most_common(5))}")
    print(f"\n  Total with startdate: {total_with:,}; of which 2019-2020: {total_1920:,}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-api", action="store_true")
    parser.add_argument("--sources", nargs="+", default=SOURCES)
    args = parser.parse_args()
    part_b()
    if not args.skip_api:
        print()
        part_a(args.sources)


if __name__ == "__main__":
    main()
