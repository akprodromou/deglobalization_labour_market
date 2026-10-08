"""
Inspect the OJA stratified sample page by page.

Why: in the first run of script 21 every sampled page contained a single ISCO
major group (2019-06 all group 3; 2024-01 and 2024-02 all group 2), and
organization/description were empty. That suggests the API returns results in an
order tied to occupation, so a page of 100 consecutive results is not a random
draw. This prints, for every sampled page, what is in it, so we can see the
ordering and the real format of `occupations`.

Usage, from the repo root:
    python -m diagnostics.22_inspect_oja_sample
Read-only: uses data/raw/oja_stratified_sample.jsonl, makes no API calls.
"""

import json
import re
from collections import Counter
from pathlib import Path

SAMPLE_PATH = Path("data/raw/oja_stratified_sample.jsonl")
ISCO = re.compile(r"isco/C(\d+)")


def isco_codes(p):
    out = []
    for entry in p.get("occupations") or []:
        text = entry if isinstance(entry, str) else json.dumps(entry, ensure_ascii=False)
        out.extend(ISCO.findall(text))
    return out


def main():
    pages = {}
    with open(SAMPLE_PATH, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                row = json.loads(line)
                pages.setdefault((row["_window"], row["_page"]), []).append(row["posting"])

    for (window, page), items in sorted(pages.items()):
        first_codes = Counter(c[0][0] if c else None for c in (isco_codes(p) for p in items))
        four = Counter(c[0][:4] if c else None for c in (isco_codes(p) for p in items))
        n_occ = Counter(len(p.get("occupations") or []) for p in items)
        ids = [p.get("id") for p in items]
        dates = Counter(str(p.get("upload_date"))[:10] for p in items)
        print(f"\n=== {window} page {page}: {len(items)} postings ===")
        print(f"  id first/last: {ids[0]} .. {ids[-1]}")
        print(f"  upload_date: {dict(dates.most_common(4))}")
        print(f"  ISCO major group of first code: {dict(first_codes)}")
        print(f"  ISCO 4-digit (first code), top 5: {dict(four.most_common(5))}")
        print(f"  occupations per posting: {dict(n_occ)}")
        print(f"  titles: {[str(p.get('title'))[:40] for p in items[:3]]}")
        print(f"  description type/len of first: {type(items[0].get('description')).__name__}, "
              f"{len(str(items[0].get('description') or ''))}")
        print(f"  organization of first: {items[0].get('organization')!r}")

    first = next(iter(pages.values()))[0]
    print("\n=== One raw posting (occupations/skills truncated) ===")
    shown = dict(first)
    shown["skills"] = (shown.get("skills") or [])[:3]
    shown["occupations"] = (shown.get("occupations") or [])[:4]
    print(json.dumps(shown, indent=2, ensure_ascii=False)[:3000])


if __name__ == "__main__":
    main()
