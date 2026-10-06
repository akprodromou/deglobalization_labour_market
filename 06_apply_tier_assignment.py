"""
Month 2, Week 3: apply the integrated Tier 1-4 fallback chain
(assign_data_completeness_tier.py) to the real working profile sample,
tag every profile with `data_completeness`, and report the tier
distribution -- the brief's explicit Week 3 deliverable.

Reads:
    data/raw/profiles_sample.jsonl        (one JSON object per line)
    data/raw/occupationSkillRelations_en.csv

Writes:
    data/raw/profiles_tagged.jsonl        (every profile + the 4 new tier fields)
    (both already excluded from git via .gitignore's data/raw/*.jsonl rule)

Prints the tier distribution to the console, which is the number to paste
into the Week 4 data-quality policy paragraph.
"""

import json
from pathlib import Path

from assign_data_completeness_tier import run_full_pipeline, summarize_tier_distribution

PROFILES_PATH = Path("data/raw/profiles_sample.jsonl")
ESCO_CSV_PATH = Path("data/raw/occupationSkillRelations_en.csv")
OUTPUT_PATH = Path("data/raw/profiles_tagged.jsonl")


def load_profiles(path: Path) -> list:
    profiles = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                profiles.append(json.loads(line))
    return profiles


def save_tagged_profiles(tagged_profiles: list, path: Path):
    with open(path, "w", encoding="utf-8") as f:
        for profile in tagged_profiles:
            f.write(json.dumps(profile, ensure_ascii=False) + "\n")


def main():
    if not PROFILES_PATH.exists():
        raise FileNotFoundError(f"{PROFILES_PATH} not found -- run 01_fetch_sample.py first.")
    if not ESCO_CSV_PATH.exists():
        raise FileNotFoundError(f"{ESCO_CSV_PATH} not found.")

    print(f"Loading profiles from {PROFILES_PATH}...")
    profiles = load_profiles(PROFILES_PATH)
    print(f"  {len(profiles)} profiles loaded.")

    print(f"\nRunning the Tier 1-4 fallback chain (ESCO table: {ESCO_CSV_PATH})...")
    tagged_profiles = run_full_pipeline(profiles, str(ESCO_CSV_PATH))

    save_tagged_profiles(tagged_profiles, OUTPUT_PATH)
    print(f"\nTagged profiles saved to {OUTPUT_PATH}")

    dist = summarize_tier_distribution(tagged_profiles)
    print("\n=== Tier distribution (Week 3 deliverable) ===")
    for label, stats in dist.items():
        print(f"  {label:<9}: {stats['count']:>6} profiles ({stats['fraction']:.1%})")

    tier2_by_mechanism = {}
    for p in tagged_profiles:
        if p["tier"] == 2:
            mech = p["tier_detail"]["mechanism"]
            tier2_by_mechanism[mech] = tier2_by_mechanism.get(mech, 0) + 1
    if tier2_by_mechanism:
        print("\nTier 2 breakdown by mechanism:")
        for mech, count in sorted(tier2_by_mechanism.items(), key=lambda x: -x[1]):
            print(f"  {mech}: {count}")


if __name__ == "__main__":
    main()