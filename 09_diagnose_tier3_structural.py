"""
Second follow-up on Tier 3's 0% result. 07 and 08 confirmed the field
names are correct and that, WITHIN the current 7,222-profile sample, no
bucket clears MIN_BUCKET_SIZE=20. But that doesn't yet tell us whether
this is (a) a sample-size artifact that would resolve with more data,
(b) a structural ceiling caused by overly fine-grained sector categories,
or (c) concentrated in specific sources the way occupation_uris and NUTS
turned out to be. This checks all three before accepting MIN_BUCKET_SIZE
as the right call.
"""

import json
from collections import Counter
from pathlib import Path

PROFILES_PATH = Path("data/raw/profiles_sample.jsonl")


def load_profiles(path: Path) -> list:
    profiles = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                profiles.append(json.loads(line))
    return profiles


def main():
    profiles = load_profiles(PROFILES_PATH)
    print(f"{len(profiles)} profiles loaded.\n")

    print("=== 'sectors' non-empty completeness, by source ===")
    by_source_total = Counter()
    by_source_with_sectors = Counter()
    for p in profiles:
        source = p.get("source", "UNKNOWN")
        by_source_total[source] += 1
        if p.get("sectors"):
            by_source_with_sectors[source] += 1
    for source, total in sorted(by_source_total.items(), key=lambda x: -x[1]):
        with_sectors = by_source_with_sectors.get(source, 0)
        print(f"  {source:<20} {with_sectors:>5}/{total:<5} ({with_sectors/total:.1%})")

    all_sector_values = Counter()
    for p in profiles:
        for sector in (p.get("sectors") or []):
            all_sector_values[sector] += 1
    print(f"\n=== Distinct sector values across ALL 7,222 profiles: {len(all_sector_values)} ===")
    print("Top 15 by frequency:")
    for sector, count in all_sector_values.most_common(15):
        print(f"  {count:>4}  {sector!r}")

    print("\n=== Raw 'sectors' field value, 5 examples (profiles that have it) ===")
    shown = 0
    for p in profiles:
        if p.get("sectors"):
            print(f"  id={p.get('id')}: {p['sectors']!r}")
            shown += 1
        if shown >= 5:
            break

    print("\n=== 'highest_degree' value distribution (including empty/null) ===")
    degree_counts = Counter(p.get("highest_degree") for p in profiles)
    for value, count in degree_counts.most_common(15):
        print(f"  {value!r}: {count}")

    print("\n=== 'degree' (separate field) value distribution, top 15 ===")
    degree_field_counts = Counter(p.get("degree") for p in profiles)
    for value, count in degree_field_counts.most_common(15):
        print(f"  {value!r}: {count}")

    biggest_bucket_in_sample = max(all_sector_values.values()) if all_sector_values else 0
    if biggest_bucket_in_sample:
        scale_factor_needed = 20 / biggest_bucket_in_sample
        projected_sample_size_needed = int(len(profiles) * scale_factor_needed)
        print(f"\n=== Scale check ===")
        print(f"Biggest single sector bucket in this sample (any degree, raw count): "
              f"{biggest_bucket_in_sample}")
        print(f"At this same rate, a sample of roughly {projected_sample_size_needed:,} profiles "
              f"would be needed for just the single most common sector to reach 20 -- "
              f"and that's before requiring those profiles to ALSO be Tier 1 (have skills), "
              f"which the real data shows holds for only a minority of sector-bearing profiles.")


if __name__ == "__main__":
    main()