"""
Does the working sample's tag fill depend on the posting month?

Section 13.6 reports kariera.gr tag fill of 90% (occupations), 91% (skills) and
83% (sectors) in the working sample, against 58%, 57% and 52% in the pages
of Section 9.7 that cover the whole life of the board. The likely reason is
that the working sample's kariera.gr postings are all dated 2024, before the tags
stop. This script tests that on the sample itself: for one source it groups the
sampled postings by month of `upload_date` and shows the share with occupations,
skills and sectors filled.

Offline: reads data/raw/postings_sample.jsonl, no network, no credentials.

Run (from the project root, venv active):
    python -m diagnostics.48_sample_tag_fill_by_month
    python -m diagnostics.48_sample_tag_fill_by_month --source jobbland --field skills

Output: docs/sample_tag_fill_by_month_<source>.md
"""

import argparse
import json
from collections import defaultdict
from pathlib import Path

POSTINGS_PATH = Path("data/raw/postings_sample.jsonl")
FIELDS = ["occupations", "skills", "sectors"]


def missing(value) -> bool:
    if value is None:
        return True
    if isinstance(value, str) and value.strip().lower() in ("", "empty"):
        return True
    if isinstance(value, (list, dict)) and not value:
        return True
    return False


def month_of(value) -> str:
    if isinstance(value, str) and len(value) >= 7 and value[4] == "-":
        return value[:7]
    return "(no date)"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--path", default=str(POSTINGS_PATH))
    ap.add_argument("--source", default="kariera.gr")
    ap.add_argument("--field", default=None,
                    help="report only this field (default: occupations, skills, sectors)")
    args = ap.parse_args()

    rows = []
    with open(args.path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                p = json.loads(line)
                if p.get("source") == args.source:
                    rows.append(p)
    print(f"{args.source}: {len(rows)} postings in the sample")
    if not rows:
        print("No postings for this source; check the spelling of --source.")
        return

    fields = [args.field] if args.field else FIELDS
    by_month = defaultdict(list)
    for p in rows:
        by_month[month_of(p.get("upload_date"))].append(p)

    out = [f"# Tag fill by month in the working sample: {args.source}\n",
           f"Postings: {len(rows)}. Share of postings with the field filled, "
           "by month of `upload_date`.\n",
           "| Month | Postings | " + " | ".join(f"`{x}`" for x in fields) + " |",
           "|---|---:|" + "|".join("---:" for _ in fields) + "|"]
    for m in sorted(by_month):
        g = by_month[m]
        cells = [f"{sum(1 for p in g if not missing(p.get(x))) / len(g):.0%}"
                 for x in fields]
        out.append(f"| {m} | {len(g)} | " + " | ".join(cells) + " |")
    tot = [f"{sum(1 for p in rows if not missing(p.get(x))) / len(rows):.0%}"
           for x in fields]
    out.append(f"| **All** | {len(rows)} | " + " | ".join(tot) + " |")
    out.append("")
    out.append("Reading: if every sampled month lies before the tags stop "
               "(kariera.gr: December 2025), a high overall fill rate here and a "
               "lower rate in Section 9.7 are consistent with a change over "
               "time, not a contradiction.")

    path = Path(f"docs/sample_tag_fill_by_month_{args.source}.md")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("\n".join(out))
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
