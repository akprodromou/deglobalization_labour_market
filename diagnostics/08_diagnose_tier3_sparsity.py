"""
Follow-up to 07_diagnose_tier3_zero.py: field names are confirmed correct
('sectors', 'highest_degree' both exist exactly as the brief names them),
so Tier 3's 0% result is not a naming bug. This checks WHY it's still 0 --
specifically, whether the 232 profiles with a non-empty `sectors` field
are spread too thin across distinct sector values for any
(sector, highest_degree) or (sector,) bucket to ever clear
MIN_BUCKET_SIZE = 20 Tier-1 profiles.

Also checks: of the 232 sector-bearing profiles, how many are themselves
Tier 1 (the only ones that feed SectorDegreePrior.fit())? If very few of
the 232 are Tier 1, the prior has almost nothing to learn from regardless
of how the buckets are sliced.
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

    sector_bearing = [p for p in profiles if p.get("sectors")]
    print(f"Profiles with non-empty 'sectors': {len(sector_bearing)}")

    tier1_sector_bearing = [p for p in sector_bearing if p.get("skills")]
    print(f"Of those, profiles that are ALSO Tier 1 (non-empty 'skills', "
          f"i.e. the only ones SectorDegreePrior.fit() can learn from): "
          f"{len(tier1_sector_bearing)}")

    # Bucket the Tier-1 sector-bearing profiles exactly as
    # SectorDegreePrior.fit() would, and show the resulting bucket sizes.
    sector_degree_counts = Counter()
    sector_only_counts = Counter()
    for p in tier1_sector_bearing:
        degree = p.get("highest_degree")
        for sector in p["sectors"]:
            sector_only_counts[sector] += 1
            if degree:
                sector_degree_counts[(sector, degree)] += 1

    print(f"\nDistinct sectors seen among Tier-1 sector-bearing profiles: {len(sector_only_counts)}")
    print("Sector-only bucket sizes (MIN_BUCKET_SIZE = 20 required to trust a bucket):")
    for sector, count in sector_only_counts.most_common():
        flag = "  <- clears threshold" if count >= 20 else ""
        print(f"  {sector!r}: {count}{flag}")

    print(f"\nDistinct (sector, highest_degree) combinations: {len(sector_degree_counts)}")
    print("Largest (sector, degree) buckets:")
    for key, count in sector_degree_counts.most_common(10):
        flag = "  <- clears threshold" if count >= 20 else ""
        print(f"  {key}: {count}{flag}")

    n_clearing_sector_only = sum(1 for c in sector_only_counts.values() if c >= 20)
    n_clearing_sector_degree = sum(1 for c in sector_degree_counts.values() if c >= 20)
    print(f"\nSector-only buckets clearing MIN_BUCKET_SIZE=20: {n_clearing_sector_only} "
          f"of {len(sector_only_counts)}")
    print(f"(sector, degree) buckets clearing MIN_BUCKET_SIZE=20: {n_clearing_sector_degree} "
          f"of {len(sector_degree_counts)}")

    # How many of the 2,472 Sparse (Tier 4) profiles actually HAD a
    # non-empty sectors field, i.e. could in principle have used Tier 3
    # if the buckets had been large enough?
    sparse_candidates = [
        p for p in profiles
        if not p.get("skills") and not p.get("occupation_uris") and p.get("sectors")
    ]
    print(f"\nProfiles with no skills, no occupation_uris, but a non-empty "
          f"'sectors' field (i.e. reached Tier 3's door): {len(sparse_candidates)}")


if __name__ == "__main__":
    main()