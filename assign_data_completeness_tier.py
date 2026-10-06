"""
Month 2, Week 3: the integrated Tier 1-4 fallback chain (brief Section 4,
Table 3), combined into a single function that tags every profile with a
`data_completeness` label -- the exact field name the brief specifies.

Tier definitions (brief's Table 3):
  Tier 1 "Full":     skills array populated directly -> use as-is.
  Tier 2 "Inferred":  skills empty, but an ESCO occupation can be
                      resolved (via occupation_uris directly -- Revelio --
                      or via free-text `occupation` exact-match -- other
                      sources, see occupation_text_matcher.py) -> look up
                      essential+optional skills for that occupation in the
                      ESCO table (occupation_skill_lookup.py).
  Tier 3 "Weak":      no skills, no resolvable occupation -> fall back to
                      an empirical sector+highest_degree prior, built only
                      from real Tier 1 profiles, never from inferred ones
                      (tier3_sector_degree_prior.py).
  Tier 4 "Sparse":    none of the above -> excluded from skill-based
                      analyses; retained for geographic/demographic
                      analysis only (brief's Week 4 policy).

This module exposes one function, `assign_data_completeness_tier(profile,
...)`, meant to be applied to every profile in the working sample, plus a
`run_full_pipeline(...)` helper that does the two-pass process this chain
actually requires:
  Pass 1: scan all profiles, fit the Tier 3 SectorDegreePrior using only
          the ones that are genuinely Tier 1 (real skills).
  Pass 2: assign a tier to every profile (including the Tier 1 ones,
          trivially), using the fitted Tier 3 prior as the final fallback.
Tier 3 cannot be computed in a single pass, because its prior must be
built from the OTHER profiles' confirmed Tier-1 data before it can be
applied to any profile needing a fallback.
"""

from occupation_skill_lookup import OccupationSkillLookup, tier2_lookup_skills_for_profile
from occupation_text_matcher import OccupationTextMatcher
from tier3_sector_degree_prior import SectorDegreePrior


def _is_tier1(profile: dict) -> bool:
    return bool(profile.get("skills"))


def assign_data_completeness_tier(
    profile: dict,
    occ_lookup: OccupationSkillLookup,
    text_matcher: OccupationTextMatcher,
    sector_prior: SectorDegreePrior,
) -> dict:
    """
    Returns a dict to be merged onto the profile record:
        {
          "data_completeness": "Full" | "Inferred" | "Weak" | "Sparse",
          "tier": 1 | 2 | 3 | 4,
          "skills_used": [...],
          "tier_detail": {...},
        }
    """
    if _is_tier1(profile):
        return {
            "data_completeness": "Full",
            "tier": 1,
            "skills_used": profile["skills"],
            "tier_detail": {"mechanism": "direct"},
        }

    tier2_result = tier2_lookup_skills_for_profile(profile, occ_lookup)
    if tier2_result["skills"]:
        return {
            "data_completeness": "Inferred",
            "tier": 2,
            "skills_used": tier2_result["skills"],
            "tier_detail": {
                "mechanism": "occupation_uris",
                "occupation_uri": tier2_result["occupation_uri"],
                "occupation_label": tier2_result["occupation_label"],
            },
        }

    occupation_text = profile.get("occupation")
    if occupation_text:
        match = text_matcher.match(occupation_text)
        if match["occupation_uri"]:
            skills = occ_lookup.skills_for_occupation(match["occupation_uri"])
            if skills:
                return {
                    "data_completeness": "Inferred",
                    "tier": 2,
                    "skills_used": skills,
                    "tier_detail": {
                        "mechanism": f"occupation_text_{match['method']}",
                        "occupation_uri": match["occupation_uri"],
                        "occupation_text": occupation_text,
                        "confidence": match["confidence"],
                    },
                }

    sectors = profile.get("sectors") or []
    highest_degree = profile.get("highest_degree")
    tier3_result = sector_prior.get_default_skills(sectors, highest_degree)
    if tier3_result["skills"]:
        return {
            "data_completeness": "Weak",
            "tier": 3,
            "skills_used": tier3_result["skills"],
            "tier_detail": {
                "mechanism": "sector_degree_prior",
                "bucket_type": tier3_result["bucket_type"],
                "bucket_size": tier3_result["bucket_size"],
                "sectors_used": tier3_result["sectors_used"],
            },
        }

    return {
        "data_completeness": "Sparse",
        "tier": 4,
        "skills_used": [],
        "tier_detail": {"mechanism": None},
    }


def run_full_pipeline(profiles: list, esco_csv_path: str) -> list:
    """
    Two-pass application of the fallback chain to a full list of profile
    dicts. Returns a new list of profiles, each with the four
    `assign_data_completeness_tier` keys merged in.
    """
    occ_lookup = OccupationSkillLookup()
    occ_lookup.load(esco_csv_path)
    text_matcher = OccupationTextMatcher(occ_lookup.occupation_labels)

    tier1_profiles = [p for p in profiles if _is_tier1(p)]
    sector_prior = SectorDegreePrior().fit(tier1_profiles)

    tagged_profiles = []
    for profile in profiles:
        tier_info = assign_data_completeness_tier(profile, occ_lookup, text_matcher, sector_prior)
        tagged_profiles.append({**profile, **tier_info})

    return tagged_profiles


def summarize_tier_distribution(tagged_profiles: list) -> dict:
    """Fraction of profiles at each tier -- the brief's explicit Week 3 requirement."""
    n = len(tagged_profiles)
    counts = {"Full": 0, "Inferred": 0, "Weak": 0, "Sparse": 0}
    for p in tagged_profiles:
        counts[p["data_completeness"]] += 1
    return {
        label: {"count": c, "fraction": round(c / n, 4) if n else 0.0}
        for label, c in counts.items()
    }


if __name__ == "__main__":
    import sys

    esco_csv_path = sys.argv[1] if len(sys.argv) > 1 else "occupationSkillRelations_en.csv"

    synthetic_profiles = [
        {"source": "linkedin", "skills": ["python", "sql"], "occupation_uris": [], "sectors": ["ICT"], "highest_degree": "bachelor"},
        {"source": "linkedin", "skills": ["negotiation"], "occupation_uris": [], "sectors": ["Retail"], "highest_degree": "bachelor"},
        *[
            {"source": "linkedin", "skills": ["python", "communication"], "occupation_uris": [], "sectors": ["ICT"], "highest_degree": "bachelor"}
            for _ in range(20)
        ],
        {
            "source": "revelio", "skills": [], "sectors": ["Culture"], "highest_degree": "master",
            "occupation_uris": [
                "http://data.europa.eu/esco/isco/C1323",
                "http://data.europa.eu/esco/occupation/00030d09-2b3a-4efd-87cc-c4ea39d27c34",
            ],
        },
        {
            "source": "jobs.de", "skills": [], "occupation_uris": [], "occupation": "Technical Director",
            "sectors": ["Culture"], "highest_degree": "master",
        },
        {"source": "stack-math", "skills": [], "occupation_uris": [], "sectors": ["ICT"], "highest_degree": "bachelor"},
        {"source": "unknown_source", "skills": [], "occupation_uris": [], "sectors": [], "highest_degree": None},
    ]

    tagged = run_full_pipeline(synthetic_profiles, esco_csv_path)

    print("Per-profile results:")
    for p in tagged:
        print(f"  source={p['source']:<16} -> data_completeness={p['data_completeness']:<9} "
              f"tier={p['tier']}  mechanism={p['tier_detail'].get('mechanism')}  "
              f"n_skills={len(p['skills_used'])}")

    dist = summarize_tier_distribution(tagged)
    print("\nTier distribution:")
    for label, stats in dist.items():
        print(f"  {label:<9}: {stats['count']} profiles ({stats['fraction']:.1%})")

    assert tagged[0]["tier"] == 1 and tagged[0]["data_completeness"] == "Full"
    revelio_row = next(p for p in tagged if p["source"] == "revelio")
    assert revelio_row["tier"] == 2 and revelio_row["tier_detail"]["mechanism"] == "occupation_uris"
    textmatch_row = next(p for p in tagged if p["source"] == "jobs.de")
    assert textmatch_row["tier"] == 2 and textmatch_row["tier_detail"]["mechanism"].startswith("occupation_text")
    tier3_row = next(p for p in tagged if p["source"] == "stack-math")
    assert tier3_row["tier"] == 3, f"Expected Tier 3, got tier={tier3_row['tier']} ({tier3_row['tier_detail']})"
    tier4_row = next(p for p in tagged if p["source"] == "unknown_source")
    assert tier4_row["tier"] == 4 and tier4_row["skills_used"] == []

    print("\nAll smoke-test assertions passed (all four tiers and both Tier-2 paths fired as expected).")