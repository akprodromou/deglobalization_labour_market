# Data schema: Skillab tracker profiles and postings

Generated on 2026-10-08 by `diagnostics/19_generate_schema_doc.py` from
`data/raw/profiles_sample.jsonl` (7,222 profiles) and
`data/raw/postings_sample.jsonl` (6,723 postings). The inventory tables are computed from the
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
  `{"items": [...], "count": N}`.
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


## 3. Postings (job schema)

6,723 postings, 16 sources.

| Field | Observed types | Non-empty | Literal 'empty' | Note |
|---|---|---|---|---|
| `description` | str, null | 92.6% |  | Free text. |
| `experience_level` | null, str | 48.7% |  |  |
| `id` | int | 100.0% |  |  |
| `location` | str, null | 98.7% |  | Free text. |
| `location_code` | str, null | 93.0% |  | Country code in the Eurostat convention (`EL` for Greece, `UK` for the United Kingdom). |
| `nuts1` | null, str | 13.1% |  | String of the form 'NUTS level N label'. nuts1/2/3 are populated only for the EURES family. |
| `nuts2` | null, str | 12.5% |  | See nuts1. |
| `nuts3` | null, str | 12.0% |  | See nuts1. |
| `occupations` | list[str], list | 85.6% |  | Occupation list. |
| `organization` | null, str | 13.9% |  |  |
| `sectors` | list[str], list | 71.2% |  | Sector list; partly populated. |
| `skills` | list[str], list | 80.5% |  | Skill list. Completeness varies strongly by source (e.g. `eures` low, `eures-escox` near complete). |
| `source` | str | 100.0% |  | Job source (16 sources). OJA is the only source with a 2019-2020 baseline. |
| `source_id` | str | 100.0% |  |  |
| `title` | str | 93.0% |  |  |
| `type` | str, null | 88.3% |  |  |
| `upload_date` | str | 100.0% |  | See 'Date semantics' below: its meaning differs by source family. |

### Completeness of key fields by source (postings)

| Source | n | `skills` | `occupations` | `sectors` | `description` | `location` | `location_code` | `nuts1` |
|---|---|---|---|---|---|---|---|---|
| jobbland | 468 | 79.9% | 80.6% | 73.3% | 100.0% | 100.0% | 100.0% | 0.0% |
| jobmedic | 468 | 80.8% | 93.8% | 90.2% | 100.0% | 100.0% | 100.0% | 0.0% |
| jobmedic.co.uk | 468 | 80.8% | 93.8% | 90.2% | 100.0% | 100.0% | 100.0% | 0.0% |
| jobscentral | 468 | 96.2% | 94.9% | 90.2% | 100.0% | 100.0% | 0.0% | 0.0% |
| jobs.de | 468 | 94.0% | 97.9% | 91.7% | 100.0% | 100.0% | 100.0% | 0.0% |
| kariera.fr | 468 | 93.6% | 96.4% | 84.8% | 100.0% | 100.0% | 100.0% | 0.0% |
| kariera.gr | 468 | 90.6% | 90.0% | 82.9% | 100.0% | 100.0% | 100.0% | 0.0% |
| lesjeudis | 468 | 98.1% | 96.8% | 93.2% | 100.0% | 100.0% | 100.0% | 0.0% |
| lesjeudis.com | 468 | 98.1% | 96.8% | 93.2% | 100.0% | 100.0% | 100.0% | 0.0% |
| jobbland.se | 468 | 79.9% | 80.6% | 73.3% | 100.0% | 100.0% | 100.0% | 0.0% |
| eures | 468 | 39.1% | 80.8% | 60.5% | 96.8% | 88.9% | 100.0% | 92.9% |
| eures-escox | 468 | 100.0% | 100.0% | 73.3% | 97.2% | 92.5% | 100.0% | 95.1% |
| OJA | 468 | 100.0% | 100.0% | 0.0% | 0.0% | 100.0% | 100.0% | 0.0% |
| jobbguru | 319 | 18.8% | 20.4% | 18.8% | 100.0% | 100.0% | 100.0% | 0.0% |
| jobbguru.se | 319 | 18.8% | 20.4% | 18.8% | 100.0% | 100.0% | 100.0% | 0.0% |
| brightminds | 1 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 0.0% | 0.0% |

## 4. Profiles (profile schema)

7,222 profiles, 30 sources.

| Field | Observed types | Non-empty | Literal 'empty' | Note |
|---|---|---|---|---|
| `city` | null, str | 2.6% | 60 |  |
| `company` | null, str | 2.9% |  |  |
| `content` | str, null | 95.9% |  | The real free-text field for profiles. |
| `country` | null, str | 3.5% |  |  |
| `degree` | null, str | 1.0% | 53 | Uses the literal string 'empty' for missing values. |
| `description` | null, str | 0.2% |  | Effectively unused for profiles. |
| `ethnicity_predicted` | null, str | 3.5% |  |  |
| `full_name` | str | 100.0% |  |  |
| `highest_degree` | null, str | 1.3% | 159 | Uses the literal string 'empty' for missing values. |
| `id` | int | 100.0% |  |  |
| `location` | str | 100.0% |  | Free text. |
| `occupation` | null, str | 6.9% |  |  |
| `occupation_uris` | null, list[str], list | 3.3% |  | List mixing an ESCO occupation URI with an ISCO URI (`http://data.europa.eu/esco/isco/C...`). Use `extract_esco_occupation_uri`. Effectively Revelio-only. |
| `region` | null, str | 3.5% |  |  |
| `sectors` | list, list[str] | 3.2% |  | Sector list at fine (NACE-class) granularity. Effectively Revelio-only. |
| `sex_predicted` | null, str | 3.4% | 5 |  |
| `skills` | list[str], list | 62.7% |  | Skill list. The basis of Tier 1. Overall completeness hides a large source effect (see the by-source table). |
| `source` | str | 100.0% |  | 29 sources with inconsistent naming; see `source_normalization.py`. |
| `source_id` | str | 100.0% |  |  |
| `startdate` | null, str | 1.5% |  | Only one date per profile. Mostly missing outside Revelio. |
| `ultimate_parent_school_name` | null, str | 1.7% |  |  |
| `university_country` | null, str | 1.7% |  |  |
| `university_location` | null, str | 0.3% |  |  |
| `university_name` | null, str | 1.7% |  |  |
| `university_raw` | null, str | 1.7% |  |  |
| `url` | str, null | 55.4% |  |  |
| `user_country` | null, str | 3.5% |  |  |
| `user_location` | null, str | 3.5% |  |  |

### Completeness of key fields by source (profiles)

| Source | n | `skills` | `occupation_uris` | `sectors` | `content` | `startdate` | `highest_degree` |
|---|---|---|---|---|---|---|---|
| linkedin | 250 | 44.0% | 0.0% | 1.2% | 60.0% | 0.0% | 0.0% |
| stack-biology | 250 | 85.2% | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% |
| STACK-Biology | 250 | 84.0% | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% |
| stack-chemistry | 250 | 72.0% | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% |
| STACK-Chemistry | 250 | 60.8% | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% |
| STACK-Earth Science | 250 | 35.6% | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% |
| STACK-Electrical Engineering | 250 | 88.4% | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% |
| stack-electronics | 250 | 57.2% | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% |
| stack-interpersonal | 250 | 62.8% | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% |
| STACK-Interpersonal Skills | 250 | 32.0% | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% |
| stack-law | 250 | 73.2% | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% |
| STACK-Law | 250 | 54.4% | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% |
| stack-linguistics | 250 | 73.2% | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% |
| STACK-Linguistics | 250 | 45.6% | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% |
| STACK-Literature | 250 | 20.8% | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% |
| stack-math | 250 | 60.4% | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% |
| STACK-Mathematics | 250 | 96.8% | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% |
| stack-philosophy | 250 | 68.8% | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% |
| STACK-Philosophy | 250 | 52.4% | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% |
| stack-physics | 250 | 83.2% | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% |
| STACK-Physics | 250 | 95.2% | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% |
| stack-politics | 250 | 67.6% | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% |
| STACK-Politics | 250 | 38.4% | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% |
| STACK-Sports | 250 | 31.2% | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% |
| stack-stackoverflow | 250 | 99.2% | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% |
| STACK-Stack Overflow | 250 | 100.0% | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% |
| revelio | 250 | 12.4% | 94.0% | 91.6% | 21.6% | 42.0% | 36.4% |
| stack-earthscience | 204 | 74.5% | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% |
| stack-sports | 145 | 57.2% | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% |
| stack-literature | 123 | 43.9% | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% |

## 5. Known quirks

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
