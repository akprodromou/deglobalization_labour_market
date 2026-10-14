"""
Re-fetch the sampled pages of script 33 WITH the description text, so that
exposure groups can be classified on title and description, not on the title alone.

Why: the API keyword filter turned out not to behave like a text search (script
37: 'manager', 'consultant' and 'nurse' return 0 in a month of about 7,000
postings, while 'hotel' returns 1,748 and 'driver' 525; matching is
case-insensitive and whole-token, and and/or combine correctly, but what is indexed
is unclear). Counting on the stored titles (script 35) is too thin: titles are short
and cut to 90 characters. This script fetches the same evenly spaced pages as
script 33 and stores, per posting, the compact fields of script 33 plus the first
2,000 characters of the description (key "x"). Everything stays in
data/raw/stability_pages_text.json (local, not for the repo).

Usage, from the repo root (credentials in .env or env vars):
    python -m diagnostics.38_fetch_text_pages --case oil-gr
    python -m diagnostics.38_fetch_text_pages --case all --pages 6

Same cases, grid and request cost as script 33 (20-70 s per page; one case is
roughly 20-30 minutes). Resumable: finished pages are kept; re-run after failures.
Then:  python -m diagnostics.35_exposure_keyword_counts --pages-file data/raw/stability_pages_text.json
"""

import argparse
import importlib
import math
from pathlib import Path

OUT = Path("data/raw/stability_pages_text.json")
DESC_CHARS = 2000


def main():
    m33 = importlib.import_module("diagnostics.33_composition_stability_check")
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", choices=list(m33.CASES) + ["all"], default="all")
    ap.add_argument("--pages", type=int, default=6, help="evenly spaced pages per month (default 6)")
    args = ap.parse_args()

    from skillab_client import SkillabClient
    client = SkillabClient()
    counts = m33.load(m33.COUNTS_PATH)
    store = m33.load(OUT)
    for case in (list(m33.CASES) if args.case == "all" else [args.case]):
        source, months, _after, _ev = m33.CASES[case]
        print(f"=== {case} ===")
        for ym in months:
            n = m33.month_count(client, source, ym, counts)
            if not n:
                print(f"  {source} {ym}: no postings")
                continue
            n_pages = math.ceil(n / m33.PAGE_SIZE)
            for pg in m33.grid_pages(n_pages, args.pages):
                key = f"{source}|{ym}|{pg}"
                if key in store:
                    continue
                try:
                    items, _ = m33.fetch_page(client, source, ym, pg)
                except Exception as exc:
                    print(f"  {source} {ym} page {pg}/{n_pages}: FAILED ({exc})")
                    continue
                recs = []
                for p in items:
                    r = m33.compact(p)
                    r["x"] = str(p.get("description") or "")[:DESC_CHARS]
                    recs.append(r)
                store[key] = recs
                m33.save(OUT, store)
                print(f"  {source} {ym} page {pg}/{n_pages}: {len(items)} postings")


if __name__ == "__main__":
    main()
