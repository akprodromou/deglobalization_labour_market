"""
Builds a manually-reviewable CSV to measure the real precision of
occupation_text_matcher.py, rather than judging it from a handful of
hand-picked examples.

Pulls real `occupation` free-text strings from profiles_sample.jsonl
(across all sources, including both matched and unmatched cases, so you
can see both wrong matches AND missed matches), runs the matcher on each,
and writes a CSV with a blank "correct?" column for you to fill in by
hand (y/n) while looking at each row.

PREREQUISITE: requires data/raw/profiles_sample.jsonl to exist. If you
don't have it on this machine (it's .gitignore'd, since it contains real
personal data), run 01_fetch_sample.py first.
"""

import csv
import json
import random
from pathlib import Path

from occupation_text_matcher import OccupationTextMatcher

PROFILES_PATH = Path("data/raw/profiles_sample.jsonl")
OUTPUT_PATH = Path("data/raw/occupation_matcher_validation_sample.csv")
SAMPLE_SIZE = 100
RANDOM_SEED = 42  # fixed, so the sample is reproducible if you need to re-run this


def load_profiles_with_occupation_text():
    if not PROFILES_PATH.exists():
        raise FileNotFoundError(
            f"{PROFILES_PATH} not found. Run 01_fetch_sample.py first to generate it "
            "(it's .gitignore'd since it contains real personal data, so it won't "
            "already be present after a fresh git clone)."
        )
    profiles = []
    with open(PROFILES_PATH, encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            occ_text = record.get("occupation")
            if occ_text and occ_text.strip():
                profiles.append(record)
    return profiles


def main():
    profiles = load_profiles_with_occupation_text()
    print(f"Found {len(profiles)} profiles with non-empty 'occupation' text "
          f"(out of whatever total is in {PROFILES_PATH}).")

    random.seed(RANDOM_SEED)
    sample = random.sample(profiles, min(SAMPLE_SIZE, len(profiles)))
    print(f"Sampling {len(sample)} for review.")

    matcher = OccupationTextMatcher()

    rows = []
    for profile in sample:
        occ_text = profile["occupation"]
        result = matcher.match(occ_text)
        rows.append({
            "source": profile.get("source", ""),
            "occupation_text": occ_text,
            "matched_label": result["label"] if result else "",
            "matched_uri": result["uri"] if result else "",
            "method": result["method"] if result else "no_match",
            "confidence": result["confidence"] if result else "",
            "correct_y_n": "",  # fill in by hand: y / n / unsure
            "notes": "",  # optional free-text notes while reviewing
        })

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    matched = sum(1 for r in rows if r["method"] != "no_match")
    exact = sum(1 for r in rows if r["method"] == "exact")
    fuzzy = sum(1 for r in rows if r["method"] == "fuzzy")
    print(f"\nSaved {len(rows)} rows to {OUTPUT_PATH}")
    print(f"  {matched}/{len(rows)} got a match ({exact} exact, {fuzzy} fuzzy), "
          f"{len(rows) - matched} no match")
    print(f"\nOpen the CSV in Excel, fill in 'correct_y_n' for each row by reading "
          f"'occupation_text' against 'matched_label', then let me know the results.")


if __name__ == "__main__":
    main()
