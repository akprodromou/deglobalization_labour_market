"""
Tier 2 fallback chain: occupation URI -> default skill set, built from the
OFFICIAL ESCO occupation-skill relations file (occupationSkillRelations_en.csv),
downloaded directly from https://esco.ec.europa.eu/en/use-esco/download.

This is a pure local lookup -- no Tracker API calls involved, so it is
completely unaffected by that API's reliability issues. Confirmed from the
real downloaded file (2026-10-02): 126,051 relation rows, covering 3,039
unique occupations (ESCO's full occupation pillar), split into
"essential" (67,600 rows) and "optional" (58,451 rows) relations, each
further tagged as "skill/competence" or "knowledge" (59 rows have a blank
skillType -- treated as unknown/unspecified, not dropped).

NOTE on profile data shape: a profile's `occupation_uris` field (where
populated -- confirmed non-null only for the "revelio" source, see Week 2
report) is a LIST containing both an ESCO occupation URI AND an ISCO
classification URI together, e.g.:
    ["http://data.europa.eu/esco/occupation/faed05c0-...", "http://data.europa.eu/esco/isco/C1323"]
Only the esco/occupation/ URI matches this relations file; the isco/ one
must be filtered out. extract_esco_occupation_uri() below handles this.
"""

import csv
from collections import defaultdict
from pathlib import Path

DEFAULT_RELATIONS_PATH = Path("occupationSkillRelations_en.csv")


class OccupationSkillLookup:
    def __init__(self, csv_path: Path = DEFAULT_RELATIONS_PATH):
        self.essential = defaultdict(list)  # occupation_uri -> [skill_uri, ...]
        self.optional = defaultdict(list)
        self._load(csv_path)

    def _load(self, csv_path: Path):
        with open(csv_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                occ_uri = row["occupationUri"]
                skill_uri = row["skillUri"]
                if row["relationType"] == "essential":
                    self.essential[occ_uri].append(skill_uri)
                elif row["relationType"] == "optional":
                    self.optional[occ_uri].append(skill_uri)
                # Any other/unexpected relationType value is silently
                # skipped here rather than crashing -- none observed in
                # the confirmed file (only "essential"/"optional" seen),
                # but this keeps the loader robust against a future
                # ESCO version adding a new relation type.

    def get_default_skills(self, occupation_uri: str, include_optional: bool = False) -> list:
        """
        Returns the list of skill URIs associated with an occupation.
        By default, only "essential" skills are returned (the stronger,
        more defining signal). Set include_optional=True to also include
        "optional" skills.
        """
        skills = list(self.essential.get(occupation_uri, []))
        if include_optional:
            skills.extend(self.optional.get(occupation_uri, []))
        return skills

    def has_occupation(self, occupation_uri: str) -> bool:
        return occupation_uri in self.essential or occupation_uri in self.optional


def extract_esco_occupation_uri(occupation_uris_field) -> str | None:
    """
    Given a profile's raw `occupation_uris` field (a list possibly mixing
    ESCO occupation URIs and ISCO classification URIs, or None), return
    just the first ESCO occupation URI found, or None if there isn't one.
    """
    if not occupation_uris_field:
        return None
    for uri in occupation_uris_field:
        if isinstance(uri, str) and "/esco/occupation/" in uri:
            return uri
    return None


def tier2_lookup_skills_for_profile(profile: dict, lookup: OccupationSkillLookup,
                                     include_optional: bool = False) -> list:
    """
    Full Tier 2 step for one profile record: extract its ESCO occupation
    URI (if any) and return the default skill set for that occupation.
    Returns an empty list if the profile has no usable occupation URI, or
    if that occupation isn't found in the relations file.
    """
    occ_uri = extract_esco_occupation_uri(profile.get("occupation_uris"))
    if occ_uri is None:
        return []
    return lookup.get_default_skills(occ_uri, include_optional=include_optional)
