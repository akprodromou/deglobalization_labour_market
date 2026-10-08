"""
We've never actually type-checked the real postings schema the way
07/09_diagnose_tier3_*.py did for profiles -- the Week 2 report's postings
completeness numbers came from the completeness-audit notebook, which
checked specific named fields (skills, occupations, description, location,
nuts1/2/3, upload_date) without confirming the FULL field list or whether
country/sector fields exist at all for postings.

The brief's Week 2 deliverable asks for "postings by year, country,
sector" -- we have by-year (Section 9). This checks whether 'country'
and 'sector'-equivalent fields even exist on postings records, and if so,
reports completeness and a breakdown by each.
"""

import json
from collections import Counter
from pathlib import Path

POSTINGS_PATH = Path("data/raw/postings_sample.jsonl")


def load_postings(path: Path) -> list:
    postings = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                postings.append(json.loads(line))
    return postings


def main():
    postings = load_postings(POSTINGS_PATH)
    print(f"{len(postings)} postings loaded.\n")

    # 1. Full field list and types, same approach as the profile diagnostics.
    field_types = {}
    for p in postings:
        for key, value in p.items():
            field_types.setdefault(key, set()).add(type(value).__name__)

    print("=== All field names on postings, with types seen ===")
    for key, types_seen in sorted(field_types.items()):
        print(f"  {key:<20} types: {sorted(types_seen)}")

    # 2. Specifically look for anything resembling 'country' or 'sector'.
    print("\n=== Candidate country/sector fields ===")
    candidates = [k for k in field_types if "countr" in k.lower() or "sector" in k.lower() or "nuts" in k.lower()]
    for key in candidates:
        non_empty = sum(1 for p in postings if p.get(key))
        print(f"  '{key}': non-empty in {non_empty}/{len(postings)} ({non_empty/len(postings):.1%})")

    # 3. If a country-like field exists, show its value distribution and
    #    completeness by source.
    country_field = next((k for k in field_types if k.lower() in ("country", "country_code", "countrycode")), None)
    if country_field:
        print(f"\n=== Using '{country_field}' as the country field ===")
        country_counts = Counter(p.get(country_field) for p in postings if p.get(country_field))
        print("Top 15 values:")
        for value, count in country_counts.most_common(15):
            print(f"  {value!r}: {count}")

        print(f"\nCompleteness of '{country_field}' by source:")
        by_source_total = Counter()
        by_source_with_field = Counter()
        for p in postings:
            source = p.get("source", "UNKNOWN")
            by_source_total[source] += 1
            if p.get(country_field):
                by_source_with_field[source] += 1
        for source, total in sorted(by_source_total.items(), key=lambda x: -x[1]):
            with_field = by_source_with_field.get(source, 0)
            print(f"  {source:<20} {with_field:>5}/{total:<5} ({with_field/total:.1%})")
    else:
        print("\nNo direct 'country'/'country_code' field found on postings.")

    # 4. Same for a sector-like field.
    sector_field = next((k for k in field_types if "sector" in k.lower()), None)
    if sector_field:
        print(f"\n=== Using '{sector_field}' as the sector field ===")
        non_empty = sum(1 for p in postings if p.get(sector_field))
        print(f"Completeness: {non_empty}/{len(postings)} ({non_empty/len(postings):.1%})")
    else:
        print("\nNo direct 'sector' field found on postings.")

    # 5. Raw examples, so the real shape is visible directly.
    print("\n=== 3 raw example postings (full JSON, truncated to 2000 chars) ===")
    for i, p in enumerate(postings[:3]):
        print(f"\n--- posting {i} (source={p.get('source')}) ---")
        print(json.dumps(p, indent=2, ensure_ascii=False)[:2000])


if __name__ == "__main__":
    main()
