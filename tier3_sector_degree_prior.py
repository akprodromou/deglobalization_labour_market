"""
Tier 3 of the fallback chain (brief Section 4): for profiles with no
skills AND no occupation_uris, use sector tags and highest degree as a
"weak prior" -- explicitly lower-confidence than Tier 2's ESCO-grounded
imputation, per the brief's own confidence label ("Weak: sector and
education proxy").

The brief specifies the INPUTS (sectors, highest_degree) but not the
mechanism, since there is no official sector-to-skills table the way
ESCO provides an occupation-to-skills one. This builds an EMPIRICAL prior
instead: for each (sector, highest_degree) combination, find the skills
most commonly self-reported by TIER 1 profiles (real, non-empty skills
only -- never Tier 2/3 profiles, to avoid building an inference on top of
another inference).

Two bucket granularities, coarser used as a fallback:
  1. (sector, highest_degree) -- most specific
  2. (sector,) alone -- used when the specific (sector, degree) bucket is
     too small to trust (MIN_BUCKET_SIZE)
A profile's `sectors` field is a list (profiles can belong to more than
one sector); matches across all of a profile's sectors are combined.
"""

from collections import Counter

MIN_BUCKET_SIZE = 20  # minimum Tier-1 profiles in a bucket before trusting it
TOP_N_SKILLS = 10      # how many skills to return per bucket


class SectorDegreePrior:
    def __init__(self):
        self.sector_degree_buckets = {}  # (sector, degree) -> Counter(skill_uri)
        self.sector_only_buckets = {}    # sector -> Counter(skill_uri)
        self.sector_degree_counts = {}   # (sector, degree) -> n profiles
        self.sector_only_counts = {}     # sector -> n profiles

    def fit(self, tier1_profiles: list):
        """
        tier1_profiles: profiles already confirmed to have a real,
        non-empty `skills` list (Tier 1 only -- do not pass Tier 2/3
        profiles here).
        """
        for profile in tier1_profiles:
            skills = profile.get("skills") or []
            if not skills:
                continue
            sectors = profile.get("sectors") or []
            degree = profile.get("highest_degree") or None

            for sector in sectors:
                self.sector_only_buckets.setdefault(sector, Counter()).update(skills)
                self.sector_only_counts[sector] = self.sector_only_counts.get(sector, 0) + 1

                if degree:
                    key = (sector, degree)
                    self.sector_degree_buckets.setdefault(key, Counter()).update(skills)
                    self.sector_degree_counts[key] = self.sector_degree_counts.get(key, 0) + 1

        return self

    def get_default_skills(self, sectors: list, highest_degree: str = None,
                            top_n: int = TOP_N_SKILLS) -> dict:
        """
        Returns {"skills": [...], "bucket_type": "sector_degree" | "sector_only" | "mixed" | None,
        "bucket_size": int, "sectors_used": [...]}

        Tries the more specific (sector, degree) bucket first for each of
        the profile's sectors; falls back to sector-only if that specific
        bucket is too small or degree is missing; skips a sector entirely
        if even the sector-only bucket is too small.
        """
        if not sectors:
            return {"skills": [], "bucket_type": None, "bucket_size": 0, "sectors_used": []}

        combined = Counter()
        bucket_types_used = set()
        sectors_used = []
        total_bucket_size = 0

        for sector in sectors:
            key = (sector, highest_degree) if highest_degree else None
            if key and self.sector_degree_counts.get(key, 0) >= MIN_BUCKET_SIZE:
                combined.update(self.sector_degree_buckets[key])
                bucket_types_used.add("sector_degree")
                total_bucket_size += self.sector_degree_counts[key]
                sectors_used.append(sector)
            elif self.sector_only_counts.get(sector, 0) >= MIN_BUCKET_SIZE:
                combined.update(self.sector_only_buckets[sector])
                bucket_types_used.add("sector_only")
                total_bucket_size += self.sector_only_counts[sector]
                sectors_used.append(sector)
            # else: this sector has too little Tier-1 data to trust; skipped

        if not combined:
            return {"skills": [], "bucket_type": None, "bucket_size": 0, "sectors_used": []}

        bucket_type = "sector_degree" if "sector_degree" in bucket_types_used else "sector_only"
        if "sector_degree" in bucket_types_used and "sector_only" in bucket_types_used:
            bucket_type = "mixed"

        top_skills = [skill for skill, _ in combined.most_common(top_n)]
        return {
            "skills": top_skills, "bucket_type": bucket_type,
            "bucket_size": total_bucket_size, "sectors_used": sectors_used,
        }


if __name__ == "__main__":
    # Quick smoke test with synthetic data, so this can be sanity-checked
    # without needing a live API pull.
    synthetic_tier1_profiles = []
    for i in range(25):
        synthetic_tier1_profiles.append({
            "sectors": ["ICT"],
            "highest_degree": "bachelor",
            "skills": ["python", "sql", "communication"],
        })
    for i in range(25):
        synthetic_tier1_profiles.append({
            "sectors": ["ICT"],
            "highest_degree": "master",
            "skills": ["python", "machine_learning", "leadership"],
        })
    # Retail: split across two degree values (15 each) so that each
    # specific (sector, degree) bucket is BELOW MIN_BUCKET_SIZE, but the
    # sector-only aggregate (30) is above it -- this is the case that
    # should trigger the sector-only fallback.
    for i in range(15):
        synthetic_tier1_profiles.append({
            "sectors": ["Retail"],
            "highest_degree": "bachelor",
            "skills": ["customer_service", "sales"],
        })
    for i in range(15):
        synthetic_tier1_profiles.append({
            "sectors": ["Retail"],
            "highest_degree": "master",
            "skills": ["customer_service", "team_management"],
        })

    prior = SectorDegreePrior().fit(synthetic_tier1_profiles)

    print("Case 1: ICT + bachelor (specific bucket has 25 profiles, >= MIN_BUCKET_SIZE)")
    result = prior.get_default_skills(["ICT"], "bachelor")
    print(" ", result)
    assert result["bucket_type"] == "sector_degree"
    assert result["bucket_size"] == 25
    assert "python" in result["skills"]

    print("Case 2: Retail + bachelor (specific bucket only has 15 profiles, below MIN_BUCKET_SIZE, falls back to sector-only)")
    result = prior.get_default_skills(["Retail"], "bachelor")
    print(" ", result)
    assert result["bucket_type"] == "sector_only"
    assert result["bucket_size"] == 30

    print("Case 3: unknown sector (no data at all)")
    result = prior.get_default_skills(["Unknown Sector"], "bachelor")
    print(" ", result)
    assert result["bucket_type"] is None
    assert result["skills"] == []

    print("Case 4: multiple sectors combined (ICT + Retail)")
    result = prior.get_default_skills(["ICT", "Retail"], "bachelor")
    print(" ", result)
    assert result["bucket_type"] == "mixed"

    print("\nAll smoke-test assertions passed.")