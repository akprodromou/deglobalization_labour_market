"""
Quick follow-up to 12_diagnose_postings_schema.py: 'location_code' showed
up as a field but wasn't substring-matched by the country/sector filter
(its name doesn't contain "countr"), and all 3 raw examples printed had
it as null. Before concluding postings have no country-level field at
all, check its real completeness and whether it holds country codes.
"""

import json
from collections import Counter
from pathlib import Path

POSTINGS_PATH = Path("data/raw/postings_sample.jsonl")


def main():
    postings = []
    with open(POSTINGS_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                postings.append(json.loads(line))

    print(f"{len(postings)} postings loaded.\n")

    non_empty = sum(1 for p in postings if p.get("location_code"))
    print(f"'location_code' non-empty in {non_empty}/{len(postings)} ({non_empty/len(postings):.1%})")

    if non_empty:
        value_counts = Counter(p.get("location_code") for p in postings if p.get("location_code"))
        print(f"\nDistinct values: {len(value_counts)}")
        print("Top 20:")
        for value, count in value_counts.most_common(20):
            print(f"  {value!r}: {count}")

        print("\nCompleteness by source:")
        by_source_total = Counter()
        by_source_with_field = Counter()
        for p in postings:
            source = p.get("source", "UNKNOWN")
            by_source_total[source] += 1
            if p.get("location_code"):
                by_source_with_field[source] += 1
        for source, total in sorted(by_source_total.items(), key=lambda x: -x[1]):
            with_field = by_source_with_field.get(source, 0)
            print(f"  {source:<20} {with_field:>5}/{total:<5} ({with_field/total:.1%})")
    else:
        print("\n'location_code' is empty across the entire sample -- confirmed no usable "
              "country-level structured field exists on postings beyond free-text 'location' "
              "and the NUTS fields (EURES-family only, per Week 2 report Finding 2).")


if __name__ == "__main__":
    main()
