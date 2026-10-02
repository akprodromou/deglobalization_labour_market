"""
Definitive check: is occupation_uris genuinely Revelio-only, or did the
Week 2 completeness audit's 250-record-per-source sample just miss rare
non-empty values in other sources?

For every NON-revelio profile source, this pulls as much of the source's
full population as practical (capped at MAX_RECORDS_PER_SOURCE, since
STACK-Stack Overflow alone has ~105,000 records -- not worth a full pull
for this specific question) and checks occupation_uris completeness
directly, rather than inferring from a small sample.

Revelio itself already has strong evidence (94.0% from n=250, and this
field is the reason Revelio needs special per-country handling in the
first place) -- not re-checked exhaustively here, since the open question
is specifically about the OTHER sources.
"""

import json
from pathlib import Path

from skillab_client import SkillabClient

MAX_RECORDS_PER_SOURCE = 2000  # cap, so the one huge source doesn't dominate runtime

PROFILE_SOURCES_EXCL_REVELIO = [
    "linkedin",
    "stack-biology", "STACK-Biology",
    "stack-chemistry", "STACK-Chemistry",
    "stack-earthscience", "STACK-Earth Science",
    "STACK-Electrical Engineering", "stack-electronics",
    "stack-interpersonal", "STACK-Interpersonal Skills",
    "stack-law", "STACK-Law",
    "stack-linguistics", "STACK-Linguistics",
    "stack-literature", "STACK-Literature",
    "stack-math", "STACK-Mathematics",
    "stack-philosophy", "STACK-Philosophy",
    "stack-physics", "STACK-Physics",
    "stack-politics", "STACK-Politics",
    "stack-sports", "STACK-Sports",
    "stack-stackoverflow", "STACK-Stack Overflow",
]

OUTPUT_DIR = Path("data/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = OUTPUT_DIR / "occupation_uris_full_check.json"


def is_non_empty(value):
    if value is None:
        return False
    if isinstance(value, (str, list, dict)) and len(value) == 0:
        return False
    return True


def check_source(client, source):
    print(f"Checking source='{source}' (up to {MAX_RECORDS_PER_SOURCE} records)...")
    total_seen = 0
    non_empty_count = 0
    examples = []

    try:
        for record in client.iter_profiles(source=source):
            total_seen += 1
            if is_non_empty(record.get("occupation_uris")):
                non_empty_count += 1
                if len(examples) < 2:
                    examples.append({
                        "id": record.get("id"),
                        "occupation_uris": record.get("occupation_uris"),
                    })
            if total_seen >= MAX_RECORDS_PER_SOURCE:
                break
    except Exception as exc:
        print(f"  -> FAILED after {total_seen} records: {exc}")
        return {
            "source": source, "total_checked": total_seen,
            "non_empty_count": non_empty_count, "error": str(exc),
            "examples": examples,
        }

    pct = round(100 * non_empty_count / total_seen, 2) if total_seen else None
    print(f"  -> checked {total_seen} records, {non_empty_count} with non-empty "
          f"occupation_uris ({pct}%)")
    return {
        "source": source, "total_checked": total_seen,
        "non_empty_count": non_empty_count, "error": None,
        "examples": examples,
    }


def main():
    client = SkillabClient()
    results = []

    for source in PROFILE_SOURCES_EXCL_REVELIO:
        result = check_source(client, source)
        results.append(result)
        with open(OUT_PATH, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\nSaved to {OUT_PATH}\n")
    print("=== Summary ===")
    any_found = False
    for r in results:
        if r["non_empty_count"] > 0:
            any_found = True
            print(f"  {r['source']}: {r['non_empty_count']}/{r['total_checked']} non-empty -- "
                  f"NOT Revelio-exclusive!")
    if not any_found:
        total_checked = sum(r["total_checked"] for r in results)
        print(f"  Confirmed: 0 non-empty occupation_uris found across "
              f"{total_checked} checked records spanning all {len(PROFILE_SOURCES_EXCL_REVELIO)} "
              f"non-Revelio sources. occupation_uris is Revelio-exclusive.")


if __name__ == "__main__":
    main()
