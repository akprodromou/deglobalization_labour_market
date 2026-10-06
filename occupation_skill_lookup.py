"""
Tier 2 of the fallback chain (brief Section 4, Table 3): for profiles with
no direct `skills`, but a populated `occupation_uris` field, look up the
default skill set for that occupation via the official ESCO
occupation-skill relations table.

Source file: occupationSkillRelations_en.csv, downloaded directly from
esco.ec.europa.eu/en/use-esco/download (the official ESCO occupation
pillar export). Columns confirmed from the real file:
    occupationUri, occupationLabel, relationType, skillType, skillUri, skillLabel
relationType is "essential" or "optional". skillType is "skill/competence",
"knowledge", or blank -- not used by this lookup, but kept available on
the loaded records in case a later analysis wants to split by it.

IMPORTANT, confirmed empirically against real Skillab profile data: a
profile's `occupation_uris` field is NOT a clean list of ESCO occupation
URIs. It mixes together an ESCO occupation URI AND an ISCO classification
URI in the same list, e.g.:

    [
      "http://data.europa.eu/esco/occupation/<uuid>",
      "http://data.europa.eu/esco/isco/C1323"
    ]

Only the first kind matches rows in occupationSkillRelations_en.csv (which
is keyed on ESCO occupation URIs, not ISCO codes), so
extract_esco_occupation_uri() filters the list down to just that one
before doing any lookup.

Also confirmed: `occupation_uris` is effectively Revelio-exclusive (94.0%
completeness on Revelio profiles, 0.0% on every other of the 29 profile
sources, checked near-exhaustively across ~30,000 non-Revelio profiles).
So in practice this tier is only ever reachable for Revelio-sourced
profiles -- see occupation_text_matcher.py for a Tier 2 enhancement that
extends reach to other sources via the free-text `occupation` field.
"""

import csv
from pathlib import Path

ESCO_OCCUPATION_URI_PREFIX = "http://data.europa.eu/esco/occupation/"


class OccupationSkillLookup:
    def __init__(self):
        # occupation_uri -> [skill_uris]
        self.essential = {}
        self.optional = {}
        self.occupation_labels = {}  # occupation_uri -> label, handy for debugging/reporting

    def load(self, csv_path: str):
        path = Path(csv_path)
        if not path.exists():
            raise FileNotFoundError(
                f"ESCO occupation-skill relations file not found: {csv_path}. "
                "Download it from esco.ec.europa.eu/en/use-esco/download."
            )

        n_rows = 0
        with open(path, encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                n_rows += 1
                occ_uri = row["occupationUri"]
                skill_uri = row["skillUri"]
                relation = row["relationType"]

                self.occupation_labels.setdefault(occ_uri, row["occupationLabel"])

                if relation == "essential":
                    self.essential.setdefault(occ_uri, []).append(skill_uri)
                elif relation == "optional":
                    self.optional.setdefault(occ_uri, []).append(skill_uri)
                # any other relationType value is unexpected; silently
                # skipped rather than crashing, since this is a lookup
                # table, not something we want to be brittle on.

        return {
            "rows_loaded": n_rows,
            "unique_occupations": len(self.occupation_labels),
        }

    def skills_for_occupation(self, occupation_uri: str, include_optional: bool = True) -> list:
        """Essential skills first, optional skills appended after (deduplicated),
        for a single ESCO occupation URI. Empty list if the URI isn't in the table."""
        skills = list(self.essential.get(occupation_uri, []))
        if include_optional:
            seen = set(skills)
            for skill_uri in self.optional.get(occupation_uri, []):
                if skill_uri not in seen:
                    skills.append(skill_uri)
                    seen.add(skill_uri)
        return skills


def extract_esco_occupation_uri(occupation_uris: list) -> str:
    """
    A profile's occupation_uris list mixes an ESCO occupation URI together
    with an ISCO classification URI. Returns the first URI that matches
    the ESCO occupation URI pattern, or None if there isn't one.
    """
    if not occupation_uris:
        return None
    for uri in occupation_uris:
        if isinstance(uri, str) and uri.startswith(ESCO_OCCUPATION_URI_PREFIX):
            return uri
    return None


def tier2_lookup_skills_for_profile(profile: dict, lookup: OccupationSkillLookup) -> dict:
    """
    Given a profile dict (expects an `occupation_uris` key) and a loaded
    OccupationSkillLookup, returns:
        {"skills": [...], "occupation_uri": str or None, "occupation_label": str or None}
    `skills` is [] if no ESCO occupation URI could be extracted, or if that
    URI isn't present in the ESCO table (shouldn't normally happen, since
    the table covers the full occupation pillar, but handled gracefully).
    """
    occupation_uris = profile.get("occupation_uris") or []
    esco_uri = extract_esco_occupation_uri(occupation_uris)
    if esco_uri is None:
        return {"skills": [], "occupation_uri": None, "occupation_label": None}

    skills = lookup.skills_for_occupation(esco_uri)
    return {
        "skills": skills,
        "occupation_uri": esco_uri,
        "occupation_label": lookup.occupation_labels.get(esco_uri),
    }


if __name__ == "__main__":
    import sys

    csv_path = sys.argv[1] if len(sys.argv) > 1 else "occupationSkillRelations_en.csv"

    lookup = OccupationSkillLookup()
    stats = lookup.load(csv_path)
    print(f"Loaded {stats['rows_loaded']} rows, {stats['unique_occupations']} unique occupations.")
    assert stats["unique_occupations"] > 0, "No occupations loaded -- check the CSV path/format."

    mixed_uris = [
        "http://data.europa.eu/esco/isco/C1323",
        "http://data.europa.eu/esco/occupation/00030d09-2b3a-4efd-87cc-c4ea39d27c34",
    ]
    extracted = extract_esco_occupation_uri(mixed_uris)
    print(f"\nSmoke test 1 -- extract from mixed ESCO+ISCO list: {extracted}")
    assert extracted == "http://data.europa.eu/esco/occupation/00030d09-2b3a-4efd-87cc-c4ea39d27c34"

    isco_only = ["http://data.europa.eu/esco/isco/C1323"]
    assert extract_esco_occupation_uri(isco_only) is None
    print("Smoke test 2 -- ISCO-only list correctly returns None")

    assert extract_esco_occupation_uri([]) is None
    assert extract_esco_occupation_uri(None) is None
    print("Smoke test 3 -- empty/None input correctly returns None")

    test_uri = "http://data.europa.eu/esco/occupation/00030d09-2b3a-4efd-87cc-c4ea39d27c34"
    skills = lookup.skills_for_occupation(test_uri)
    print(f"\nSmoke test 4 -- skills for '{lookup.occupation_labels.get(test_uri)}': "
          f"{len(skills)} skills found")
    assert len(skills) > 0, f"Expected skills for {test_uri}, got none -- check the CSV."

    synthetic_profile = {
        "source": "revelio",
        "skills": [],
        "occupation_uris": mixed_uris,
    }
    result = tier2_lookup_skills_for_profile(synthetic_profile, lookup)
    print(f"\nSmoke test 5 -- tier2_lookup_skills_for_profile: "
          f"{len(result['skills'])} skills, occupation='{result['occupation_label']}'")
    assert len(result["skills"]) > 0
    assert result["occupation_uri"] == test_uri

    no_occ_profile = {"source": "linkedin", "skills": [], "occupation_uris": []}
    result = tier2_lookup_skills_for_profile(no_occ_profile, lookup)
    assert result["skills"] == [] and result["occupation_uri"] is None
    print("Smoke test 6 -- profile with no occupation_uris correctly returns empty result")

    print("\nAll smoke-test assertions passed.")