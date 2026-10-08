"""
Month 2, Week 1, Step 1: authenticate and retrieve a sample of 5,000-10,000
profiles and postings across all available sources.

CONFIRMED: unfiltered queries against /api/profiles and /api/jobs can
hang/time out on very large tables. Filtered queries (by "sources", at
minimum) work correctly. This script ALWAYS filters by a real source.

FOUR SOURCES NEED SPECIAL HANDLING:
  - "revelio" (profiles): BARE CALLS HAVE NEVER SUCCEEDED (always 500 or
    timeout, across multiple days). Only country_codes-chunked calls have
    ever worked (DE, FR, IT on different attempts, though not all three
    every time). This script ALWAYS chunks revelio by country -- never
    attempts it bare.
  - "eures", "eures-escox", "OJA" (postings): bare calls succeeded on one
    day, failed on another -- no confirmed need for a filter, but chunking
    by upload date should reduce the per-request result size and may
    improve reliability. This script tries these three chunked by date
    range FIRST, as the primary strategy, not as a last resort.

For both groups, any chunk that still fails is retried ONCE in a deferred
pass after a 60s cooldown, once the rest of the run is done -- giving a
real time gap rather than an immediate retry.

Real profile/job sources confirmed via GET /api/profiles/sources and
GET /api/jobs/sources -- note inconsistent casing across likely
duplicate/near-duplicate sources (e.g. "stack-math" vs "STACK-Mathematics",
"jobbguru" vs "jobbguru.se"): a data-cleaning issue for the Week 2 audit.
"""

import json
import time
from collections import Counter
from pathlib import Path

from skillab_client import SkillabClient

TARGET_TOTAL = 7500  # anywhere in the 5,000-10,000 range specified in the brief
COOLDOWN_SECONDS = 60

PROFILE_SOURCES = [
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

JOB_SOURCES = [
    "brightminds",
    "jobbguru", "jobbguru.se",
    "jobbland", "jobbland.se",
    "jobmedic", "jobmedic.co.uk",
    "jobscentral", "jobs.de",
    "kariera.fr", "kariera.gr",
    "lesjeudis", "lesjeudis.com",
]

CHUNKED_JOB_SOURCES = ["eures", "eures-escox", "OJA"]

REVELIO_CHUNKS = [{"country_codes": [c]} for c in
                  ["DE", "FR", "GB", "IT", "ES", "NL", "GR", "SE", "BE"]]

DATE_CHUNKS = [
    {"min_upload_date": "2019-01-01", "max_upload_date": "2021-12-31"},
    {"min_upload_date": "2022-01-01", "max_upload_date": "2023-12-31"},
    {"min_upload_date": "2024-01-01", "max_upload_date": "2024-12-31"},
    {"min_upload_date": "2025-01-01", "max_upload_date": "2025-12-31"},
    {"min_upload_date": "2026-01-01", "max_upload_date": "2026-12-31"},
]

OUTPUT_DIR = Path("data/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def try_fetch(iterator_fn, target, **filter_kwargs):
    records = []
    try:
        for record in iterator_fn(**filter_kwargs):
            records.append(record)
            if len(records) >= target:
                break
        return records, True
    except Exception as exc:
        label = ", ".join(f"{k}={v}" for k, v in filter_kwargs.items())
        print(f"     [{label}] failed: {exc}")
        return records, False


def fetch_chunked_with_retry(iterator_fn, base_kwargs, chunks, target):
    records = []
    failed_chunks = []

    for chunk_kwargs in chunks:
        if len(records) >= target:
            break
        kwargs = {**base_kwargs, **chunk_kwargs}
        chunk, ok = try_fetch(iterator_fn, target - len(records), **kwargs)
        records.extend(chunk)
        if not ok:
            failed_chunks.append(chunk_kwargs)
        elif chunk:
            print(f"     {chunk_kwargs} -> {len(chunk)} records")

    if failed_chunks and len(records) < target:
        print(f"  {len(failed_chunks)} chunk(s) failed: {failed_chunks}. "
              f"Waiting {COOLDOWN_SECONDS}s before retry...")
        time.sleep(COOLDOWN_SECONDS)
        for chunk_kwargs in failed_chunks:
            if len(records) >= target:
                break
            kwargs = {**base_kwargs, **chunk_kwargs}
            chunk, ok = try_fetch(iterator_fn, target - len(records), **kwargs)
            records.extend(chunk)
            if ok:
                print(f"     {chunk_kwargs} SUCCEEDED on retry: {len(chunk)} records")

    return records


def fetch_plain_sources(record_type, iterator_fn, sources, per_source_target):
    all_records = []
    failed_sources = []

    print(f"--- {record_type}: plain sources ---")
    for source in sources:
        print(f"Fetching {record_type} from source='{source}' (target: {per_source_target})...")
        records, ok = try_fetch(iterator_fn, per_source_target, source=source)
        all_records.extend(records)
        if ok:
            print(f"  -> got {len(records)} records from {source}")
        else:
            failed_sources.append(source)

    if failed_sources:
        print(f"\n{len(failed_sources)} source(s) failed: {failed_sources}. "
              f"Waiting {COOLDOWN_SECONDS}s before retry...")
        time.sleep(COOLDOWN_SECONDS)
        for source in failed_sources:
            print(f"Retrying {record_type} from source='{source}'...")
            records, ok = try_fetch(iterator_fn, per_source_target, source=source)
            all_records.extend(records)
            if ok:
                print(f"  -> SUCCEEDED on retry: {len(records)} records from {source}")

    return all_records


def main():
    client = SkillabClient()

    n_profile_slots = len(PROFILE_SOURCES) + 1
    per_profile_target = max(1, TARGET_TOTAL // n_profile_slots)

    profile_records = fetch_plain_sources(
        "profiles", client.iter_profiles, PROFILE_SOURCES, per_profile_target
    )

    print("--- profiles: revelio (always chunked by country, never bare) ---")
    revelio_records = fetch_chunked_with_retry(
        client.iter_profiles, {"source": "revelio"}, REVELIO_CHUNKS, per_profile_target
    )
    print(f"  -> got {len(revelio_records)} records from revelio total")
    profile_records.extend(revelio_records)

    out_path = OUTPUT_DIR / "profiles_sample.jsonl"
    with open(out_path, "w", encoding="utf-8") as f:
        for record in profile_records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"\nSaved {len(profile_records)} profiles to {out_path}")
    print(f"  Source breakdown: {dict(Counter(r.get('source', 'MISSING') for r in profile_records))}")

    n_job_slots = len(JOB_SOURCES) + len(CHUNKED_JOB_SOURCES)
    per_job_target = max(1, TARGET_TOTAL // n_job_slots)

    posting_records = fetch_plain_sources(
        "postings", client.iter_postings, JOB_SOURCES, per_job_target
    )

    print("--- postings: eures / eures-escox / OJA (chunked by date range) ---")
    for problem_source in CHUNKED_JOB_SOURCES:
        print(f"Fetching postings from source='{problem_source}' (chunked by date)...")
        chunk_records = fetch_chunked_with_retry(
            client.iter_postings, {"source": problem_source}, DATE_CHUNKS, per_job_target
        )
        print(f"  -> got {len(chunk_records)} records from {problem_source}")
        posting_records.extend(chunk_records)

    out_path = OUTPUT_DIR / "postings_sample.jsonl"
    with open(out_path, "w", encoding="utf-8") as f:
        for record in posting_records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"\nSaved {len(posting_records)} postings to {out_path}")
    print(f"  Source breakdown: {dict(Counter(r.get('source', 'MISSING') for r in posting_records))}")


if __name__ == "__main__":
    main()
