"""
Generates docs/schema.md: the field inventory for profiles and postings.

The field lists, observed types and completeness tables are computed from the
working samples (data/raw/profiles_sample.jsonl and postings_sample.jsonl), so
they cannot drift from the data. The notes and quirks are written by hand
below and reflect the findings in docs/week2_data_quality_report.md.

"Non-empty" means: not null, not an empty string/list/dict, and not the
literal string 'empty' (which the API uses for missing values in some fields;
those are counted separately).

Usage, from the repo root:
    python -m diagnostics.19_generate_schema_doc
"""

import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

PROFILES_PATH = Path("data/raw/profiles_sample.jsonl")
POSTINGS_PATH = Path("data/raw/postings_sample.jsonl")
OUT_PATH = Path("docs/schema.md")

PROFILE_KEY_FIELDS = ["skills", "occupation_uris", "sectors", "content", "startdate", "highest_degree"]
POSTING_KEY_FIELDS = ["skills", "occupations", "sectors", "description", "location", "location_code", "nuts1"]

PROFILE_NOTES = {
    "skills": "Skill list. The basis of Tier 1. Overall completeness hides a large source effect (see the by-source table).",
    "occupation_uris": "List mixing an ESCO occupation URI with an ISCO URI (`http://data.europa.eu/esco/isco/C...`). Use `extract_esco_occupation_uri`. Effectively Revelio-only.",
    "sectors": "Sector list at fine (NACE-class) granularity. Effectively Revelio-only.",
    "content": "The real free-text field for profiles.",
    "description": "Effectively unused for profiles.",
    "startdate": "Only one date per profile. Mostly missing outside Revelio.",
    "highest_degree": "Uses the literal string 'empty' for missing values.",
    "degree": "Uses the literal string 'empty' for missing values.",
    "location": "Free text.",
    "source": "29 sources with inconsistent naming; see `source_normalization.py`.",
}

POSTING_NOTES = {
    "skills": "Skill list. Completeness varies strongly by source (e.g. `eures` low, `eures-escox` near complete).",
    "occupations": "Occupation list.",
    "sectors": "Sector list; partly populated.",
    "description": "Free text.",
    "location": "Free text.",
    "location_code": "Country code in the Eurostat convention (`EL` for Greece, `UK` for the United Kingdom).",
    "nuts1": "String of the form 'NUTS level N label'. nuts1/2/3 are populated only for the EURES family.",
    "nuts2": "See nuts1.",
    "nuts3": "See nuts1.",
    "upload_date": "See 'Date semantics' below: its meaning differs by source family.",
    "source": "Job source (16 sources). OJA is the only source with a 2019-2020 baseline.",
}

HEADER = """# Data schema: Skillab tracker profiles and postings

Generated on {today} by `diagnostics/19_generate_schema_doc.py` from
`data/raw/profiles_sample.jsonl` ({n_prof:,} profiles) and
`data/raw/postings_sample.jsonl` ({n_post:,} postings). The inventory tables are computed from the
samples; the notes were written from the findings in `docs/week2_data_quality_report.md`.
Completeness percentages describe the sample, which was drawn at roughly equal size per source.

## 1. Access

- Base URL `https://skillab-tracker.csd.auth.gr/api`. Log in with `POST /login` (JSON body with username and
  password); the response is a bare token string, sent afterwards as `Authorization: Bearer <token>`.
  Credentials are taken from the environment variables `SKILLAB_USERNAME` and `SKILLAB_PASSWORD` and are never
  stored in the repository.
- Profiles: `POST /profiles`. Postings ("jobs"): `POST /jobs`. Source lists: `GET /profiles/sources`,
  `GET /jobs/sources`.
- Filters go in a form-urlencoded body; `page` and `page_size` are query parameters; the response is
  `{{"items": [...], "count": N}}`.
- Reliability: `page_size=100` is reliable; `page_size=1` count probes are not. Open-ended date ranges
  (`min_upload_date=YYYY-01-01`, `max_upload_date=today`) are usually reliable for small sources, closed windows
  work for large sources such as OJA, and requests with an empty result often time out repeatedly. A timeout
  is therefore never treated as evidence of an empty result without a positive confirmation.
- The dataset is live and grows; every count is a snapshot taken on a given day.

## 2. Date semantics (`upload_date` on postings)

- **Scraped job boards:** the posting date on the source board (confirmed by the project author).
- **OJA:** the Eurostat Web Intelligence Hub defines the underlying date as the first detection of the posting for a
  source, replaced by the publication date where the advertisement states one. Whether Skillab's `upload_date`
  maps to it is unverified. OJA contains data from January 2019 to March 2025, with a 51-fold step in
  January 2024 (see report Section 9.4).
- **EURES family (`eures`, `eures-escox`):** behaves like an import date. All 2026 postings fall in January and
  February 2026 and none are dated later. Not usable for time series.
- Profiles carry almost no usable dates (`startdate`), so time-series work relies on postings.

"""

QUIRKS = """## 5. Known quirks

1. **Field concentration by source.** `occupation_uris`, `sectors` and `startdate` are essentially Revelio-only for
   profiles; the aggregate completeness numbers understate this (report Findings 1 and 3).
2. **Mixed URIs.** `occupation_uris` holds an ESCO occupation URI and an ISCO URI in the same list.
3. **Literal `'empty'`.** `highest_degree` and `degree` (and possibly other string fields) use the string `'empty'`
   for missing values.
4. **No career history.** A profile is a single-role snapshot; there are no multiple dated roles (confirmed against
   the live schema; report Finding 5).
5. **Regional detail.** `nuts1`-`nuts3` exist only for the EURES family; country is available through `location_code`.
6. **Source naming.** Several profile sources and some postings sources are duplicates or country variants under
   different names; normalise before using `source` as a category (report Finding 4).
7. **Time coverage.** Only OJA reaches the 2019-2020 baseline; other postings sources are mostly 2024-2026 snapshots
   (report Section 9).
8. **Derived field.** The pipeline adds `data_completeness` to profiles (`profiles_tagged.jsonl`): Tier 1 Full
   (skills present), Tier 2 Inferred (ESCO occupation lookup), Tier 3 Weak (sector and degree prior; unused at
   this sample size), Tier 4 Sparse (excluded from skill analyses).
"""


def load(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def is_literal_empty(value):
    return isinstance(value, str) and value.strip().lower() == "empty"


def is_missing(value):
    if value is None or is_literal_empty(value):
        return True
    if isinstance(value, str):
        return value.strip() == ""
    if isinstance(value, (list, dict)):
        return len(value) == 0
    return False


def type_label(value):
    if value is None:
        return "null"
    if isinstance(value, list):
        inner = next((type(x).__name__ for x in value if x is not None), None)
        return f"list[{inner}]" if inner else "list"
    return type(value).__name__


def pct(n, d):
    return f"{n / d:.1%}" if d else "n/a"


def md_table(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    for row in rows:
        out.append("| " + " | ".join(str(c).replace("|", "/") for c in row) + " |")
    return "\n".join(out)


def inventory(records, notes):
    n = len(records)
    fields = sorted({k for r in records for k in r})
    rows = []
    for field in fields:
        types = Counter(type_label(r.get(field)) for r in records if field in r)
        type_text = ", ".join(t for t, _ in types.most_common())
        non_empty = sum(1 for r in records if not is_missing(r.get(field)))
        literal = sum(1 for r in records if is_literal_empty(r.get(field)))
        rows.append([f"`{field}`", type_text, pct(non_empty, n), literal if literal else "", notes.get(field, "")])
    return md_table(["Field", "Observed types", "Non-empty", "Literal 'empty'", "Note"], rows)


def by_source(records, fields):
    groups = defaultdict(list)
    for r in records:
        groups[r.get("source", "UNKNOWN")].append(r)
    rows = []
    for source, recs in sorted(groups.items(), key=lambda x: -len(x[1])):
        rows.append([source, len(recs)] + [pct(sum(1 for r in recs if not is_missing(r.get(f))), len(recs)) for f in fields])
    return md_table(["Source", "n"] + [f"`{f}`" for f in fields], rows)


def main():
    profiles = load(PROFILES_PATH)
    postings = load(POSTINGS_PATH)
    parts = [HEADER.format(today=date.today().isoformat(), n_prof=len(profiles), n_post=len(postings))]

    parts.append("## 3. Postings (job schema)\n")
    parts.append(f"{len(postings):,} postings, {len({r.get('source') for r in postings})} sources.\n")
    parts.append(inventory(postings, POSTING_NOTES) + "\n")
    parts.append("### Completeness of key fields by source (postings)\n")
    parts.append(by_source(postings, POSTING_KEY_FIELDS) + "\n")

    parts.append("## 4. Profiles (profile schema)\n")
    parts.append(f"{len(profiles):,} profiles, {len({r.get('source') for r in profiles})} sources.\n")
    parts.append(inventory(profiles, PROFILE_NOTES) + "\n")
    parts.append("### Completeness of key fields by source (profiles)\n")
    parts.append(by_source(profiles, PROFILE_KEY_FIELDS) + "\n")

    parts.append(QUIRKS)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text("\n".join(parts), encoding="utf-8")
    print(f"Written to {OUT_PATH} ({len(profiles):,} profiles, {len(postings):,} postings).")


if __name__ == "__main__":
    main()
