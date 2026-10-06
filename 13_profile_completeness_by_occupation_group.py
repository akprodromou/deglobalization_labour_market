"""
Brief's Week 2 deliverable: "Profile completeness report (by source and
occupation group)." We've done by-source thoroughly (Week 2 report,
Section 4 and others). By-occupation-group has not been done.

There is no direct 'occupation_group' field on profiles. But
occupation_uris frequently contains BOTH an ESCO occupation URI and an
ISCO classification URI in the same list (confirmed earlier, e.g.
["http://data.europa.eu/esco/occupation/<uuid>",
 "http://data.europa.eu/esco/isco/C1323"]).
The ISCO URI's code (after the 'C') follows the standard ISCO-08
structure: the FIRST digit is the "major group" (1-digit, 10 categories,
e.g. 1=Managers, 2=Professionals, 3=Technicians and associate
professionals, ...). This script extracts that major group where
available and reports skills completeness stratified by it.

IMPORTANT CAVEAT, stated upfront rather than glossed over: this is only
derivable for profiles that have an ISCO URI in occupation_uris, which
-- per Finding 1 of the Week 2 report -- is almost exclusively a Revelio
phenomenon. So this breakdown's coverage is inherently limited to roughly
the same ~3% of the sample as Tier 2's occupation_uris path, NOT the full
sample. It answers "does skills completeness vary by occupation group
WITHIN the subset where we can tell," not "by occupation group overall."
"""

import json
import re
from collections import Counter
from pathlib import Path

PROFILES_PATH = Path("data/raw/profiles_sample.jsonl")

ISCO_URI_PATTERN = re.compile(r"http://data\.europa\.eu/esco/isco/C(\d+)")

ISCO_MAJOR_GROUPS = {
    "1": "Managers",
    "2": "Professionals",
    "3": "Technicians and associate professionals",
    "4": "Clerical support workers",
    "5": "Service and sales workers",
    "6": "Skilled agricultural, forestry and fishery workers",
    "7": "Craft and related trades workers",
    "8": "Plant and machine operators, and assemblers",
    "9": "Elementary occupations",
    "0": "Armed forces occupations",
}


def load_profiles(path: Path) -> list:
    profiles = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                profiles.append(json.loads(line))
    return profiles


def extract_isco_major_group(occupation_uris) -> str:
    """Returns the 1-digit ISCO major group code, or None if no ISCO URI
    is present in the list."""
    if not occupation_uris:
        return None
    for uri in occupation_uris:
        if not isinstance(uri, str):
            continue
        match = ISCO_URI_PATTERN.search(uri)
        if match:
            code = match.group(1)
            return code[0]  # first digit = major group
    return None


def main():
    profiles = load_profiles(PROFILES_PATH)
    print(f"{len(profiles)} profiles loaded.\n")

    tagged = []
    for p in profiles:
        major_group = extract_isco_major_group(p.get("occupation_uris"))
        tagged.append((p, major_group))

    n_with_group = sum(1 for _, g in tagged if g is not None)
    print(f"Profiles with a derivable ISCO major group: {n_with_group}/{len(profiles)} "
          f"({n_with_group/len(profiles):.1%}) -- this is the coverage ceiling for this "
          f"breakdown, not the full sample.\n")

    # Confirm the coverage really is concentrated in Revelio, as expected.
    by_source = Counter()
    for p, g in tagged:
        if g is not None:
            by_source[p.get("source", "UNKNOWN")] += 1
    print("Source breakdown of profiles with a derivable ISCO major group:")
    for source, count in by_source.most_common():
        print(f"  {source}: {count}")

    # Skills completeness stratified by major group, within the derivable subset.
    print("\n=== Skills completeness by ISCO major group (within derivable subset only) ===")
    group_total = Counter()
    group_with_skills = Counter()
    for p, g in tagged:
        if g is None:
            continue
        group_total[g] += 1
        if p.get("skills"):
            group_with_skills[g] += 1

    for code, total in sorted(group_total.items()):
        label = ISCO_MAJOR_GROUPS.get(code, f"Unknown code {code}")
        with_skills = group_with_skills.get(code, 0)
        print(f"  [{code}] {label:<55} {with_skills:>3}/{total:<3} skills-complete ({with_skills/total:.1%})")


if __name__ == "__main__":
    main()
