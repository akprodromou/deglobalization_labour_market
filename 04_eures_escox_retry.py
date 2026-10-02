"""
One-off retry: eures-escox was the only source left unresolved on both
probes after the 03_date_coverage_check.py v5 run. This script re-attempts
just those two probes, using the same proven page_size=100 pattern, and
updates the existing results file in place if it succeeds.
"""

import json
from datetime import date
from pathlib import Path

from skillab_client import SkillabClient

SOURCE = "eures-escox"
TODAY = date.today().isoformat()
RECENT_RANGE = ("2019-01-01", TODAY)
HISTORICAL_RANGE = ("2010-01-01", "2018-12-31")

OUT_PATH = Path("data/raw/date_coverage_check.json")


def probe(client, min_date, max_date):
    try:
        count = client.count_postings(SOURCE, min_upload_date=min_date, max_upload_date=max_date)
        return count, None
    except Exception as exc:
        return None, str(exc)


def main():
    client = SkillabClient()

    print(f"Retrying '{SOURCE}', recent (2019-{TODAY[:4]})...")
    recent_count, recent_err = probe(client, *RECENT_RANGE)
    print(f"  -> {'FAILED: ' + recent_err if recent_err else str(recent_count) + ' postings'}")

    print(f"Retrying '{SOURCE}', historical (2010-2018)...")
    hist_count, hist_err = probe(client, *HISTORICAL_RANGE)
    print(f"  -> {'FAILED: ' + hist_err if hist_err else str(hist_count) + ' postings'}")

    new_entry = {
        "source": SOURCE,
        "recent_2019_onward": {
            "count": recent_count, "error": recent_err,
            "confirmed_has_data": recent_count is not None and recent_count > 0,
        },
        "historical_pre_2019": {
            "count": hist_count, "error": hist_err,
            "confirmed_has_data": hist_count is not None and hist_count > 0,
        },
    }

    if OUT_PATH.exists():
        results = json.loads(OUT_PATH.read_text(encoding="utf-8"))
        results = [r for r in results if r["source"] != SOURCE]
        results.append(new_entry)
        OUT_PATH.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nUpdated {OUT_PATH} with the new {SOURCE} result.")
    else:
        print(f"\nNote: {OUT_PATH} not found -- printing result only, nothing saved.")
        print(json.dumps(new_entry, indent=2))


if __name__ == "__main__":
    main()
