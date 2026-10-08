"""
Month 2 brief, Week 2 activities: "Confirm career history depth (multiple
roles per profile, with dates) needed for transition analysis."

This was not checked yet. The field list already extracted from real
profiles (07_diagnose_tier3_zero.py) showed only SINGULAR role-related
fields -- company, occupation, startdate -- not a plural array like
positions/experience/work_history/roles. This script confirms that
directly, rather than assuming the brief's "multiple roles per profile"
expectation matches the real schema:

  1. Re-derives the full field list and flags anything that looks like it
     could hold multiple roles (a list/array-typed field other than the
     already-known skills/occupation_uris/sectors).
  2. Reports completeness of the three known single-role fields
     (company, occupation, startdate).
  3. Checks whether any profile has more than one of anything
     role-related (defensive check, in case a single profile occasionally
     carries a list under one of these keys despite the schema looking
     scalar on average).
  4. As a rough, non-NLP proxy: scans the free-text `content` field for
     multiple distinct 4-digit years (2000-2026), since a profile
     describing multiple past roles would typically mention more than one
     date range in prose, even without a structured field for it.
"""

import json
import re
from collections import Counter
from pathlib import Path

PROFILES_PATH = Path("data/raw/profiles_sample.jsonl")
YEAR_PATTERN = re.compile(r"\b(19[5-9]\d|20[0-2]\d)\b")


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

    # 1. Field-level type check: for every key, is the value ever a list
    #    (other than the known skills/occupation_uris/sectors fields)?
    print("=== Field value types seen (flagging any list-typed field) ===")
    field_types = {}
    for p in profiles:
        for key, value in p.items():
            types_seen = field_types.setdefault(key, set())
            types_seen.add(type(value).__name__)

    known_list_fields = {"skills", "occupation_uris", "sectors"}
    for key, types_seen in sorted(field_types.items()):
        flag = ""
        if "list" in types_seen and key not in known_list_fields:
            flag = "  <-- LIST-TYPED, not a known multi-value field, could hold multiple roles"
        print(f"  {key:<30} types seen: {sorted(types_seen)}{flag}")

    # 2. Completeness of the known single-role fields.
    print("\n=== Completeness of known role-related fields ===")
    for field in ["company", "occupation", "startdate"]:
        non_empty = sum(1 for p in profiles if p.get(field))
        print(f"  '{field}': non-empty in {non_empty}/{len(profiles)} ({non_empty/len(profiles):.1%})")

    # 3. Does any profile carry more than one value under a role-related
    #    field (defensive, in case of an inconsistent schema)?
    print("\n=== Checking for any profile with multiple values under company/occupation/startdate ===")
    multi_value_found = 0
    for p in profiles:
        for field in ["company", "occupation", "startdate"]:
            value = p.get(field)
            if isinstance(value, list) and len(value) > 1:
                multi_value_found += 1
                print(f"  id={p.get('id')}: '{field}' = {value}")
    if multi_value_found == 0:
        print("  None found -- every profile has at most a single scalar value "
              "for company/occupation/startdate, never a list of several.")

    # 4. Rough proxy: how many distinct years are mentioned in free-text
    #    `content`, as a signal of whether the bio text itself narrates
    #    a multi-role history even without a structured field for it.
    print("\n=== Distinct years mentioned in 'content' free text (rough proxy only) ===")
    year_count_distribution = Counter()
    profiles_with_content = [p for p in profiles if p.get("content")]
    for p in profiles_with_content:
        years_found = set(YEAR_PATTERN.findall(p["content"]))
        year_count_distribution[len(years_found)] += 1

    total_with_content = len(profiles_with_content)
    for n_years, count in sorted(year_count_distribution.items()):
        print(f"  {n_years} distinct year(s) mentioned: {count} profiles "
              f"({count/total_with_content:.1%} of {total_with_content} profiles with content)")

    multi_year_profiles = sum(c for n, c in year_count_distribution.items() if n >= 2)
    print(f"\n  Profiles mentioning 2+ distinct years in free text: {multi_year_profiles} "
          f"({multi_year_profiles/total_with_content:.1%} of profiles with content) "
          f"-- a rough upper bound on how many profiles MIGHT narrate multiple roles "
          f"in prose, not a confirmed count (would need actual NLP extraction to verify).")


if __name__ == "__main__":
    main()
