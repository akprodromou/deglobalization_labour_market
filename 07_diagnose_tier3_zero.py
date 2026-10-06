"""
Diagnostic: Tier 3 (sector + highest_degree empirical prior) came back at
0% on the real 7,222-profile sample, which is suspicious rather than
simply "no data." Before trusting that number, check:

  1. What are the ACTUAL field names on real profile records? (the brief
     specifies `sectors` and `highest_degree`, but like `occupation_uris`
     turning out to need extraction logic, these names were never
     independently verified against a real record)
  2. Of the profiles that ended up Tier 4 (Sparse), how many actually have
     non-empty `sectors` / `highest_degree` under those exact names?
  3. If those fields exist under different names, what are they?

This does not change any pipeline code -- it only inspects the raw JSONL,
so it's safe to run before deciding whether assign_data_completeness_tier.py
needs a field-name fix.
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

    all_keys = Counter()
    for p in profiles:
        all_keys.update(p.keys())
    print("=== All field names seen, with how many profiles have that key at all ===")
    for key, count in sorted(all_keys.items(), key=lambda x: -x[1]):
        print(f"  {key:<25} present in {count}/{len(profiles)} profiles ({count/len(profiles):.1%})")

    print("\n=== Checking the brief's exact field names ===")
    for field in ["sectors", "highest_degree"]:
        present = sum(1 for p in profiles if field in p)
        non_empty = sum(1 for p in profiles if p.get(field))
        print(f"  '{field}': key present in {present}/{len(profiles)}, "
              f"non-empty/truthy in {non_empty}/{len(profiles)} ({non_empty/len(profiles):.1%})")

    print("\n=== Candidate alternate field names (anything containing 'sector' or 'degree'/'education') ===")
    candidates = set()
    for key in all_keys:
        lowered = key.lower()
        if "sector" in lowered or "degree" in lowered or "educat" in lowered or "industr" in lowered:
            candidates.add(key)
    if candidates:
        for key in sorted(candidates):
            print(f"  found candidate field: '{key}' (present in {all_keys[key]} profiles)")
    else:
        print("  none found -- no field name containing 'sector', 'degree', 'educat', or 'industr'.")

    print("\n=== 3 raw example profiles (full JSON) ===")
    for i, p in enumerate(profiles[:3]):
        print(f"\n--- profile {i} (source={p.get('source')}) ---")
        print(json.dumps(p, indent=2, ensure_ascii=False)[:2000])


if __name__ == "__main__":
    main()