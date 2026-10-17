# Month 2: Data Coverage and Completeness Report

## 1. Scope

This report summarises the results of the Week 1–2 data collection and completeness audit against the Skillab tracker API, covering profiles and job postings across all available sources. It documents the sample collected, the completeness of the fields the thesis depends on, and several structural data-quality issues that affect how the Tier 1–4 skill-fallback chain and the regional (NUTS-based) analysis should be designed in Chapter 2. Section 9.8 records the study-period decision that followed from the date-coverage findings (case study from 2024 to date) and gives draft thesis text for it.

## 2. Sample Collected

- **7,222 profiles** across 29 of 29 available sources.
- **6,723 postings** across 16 of 16 available sources.
- No sources were excluded. Four sources (`revelio`, `eures`, `eures-escox`, `OJA`) required additional handling — either chunking by country (`revelio`) or by upload date (`eures`, `eures-escox`, `OJA`) — because bare, unfiltered requests to these sources were found to time out intermittently. This appears to be a server-side reliability issue tied to very large underlying tables rather than anything specific to this thesis's query pattern, and was reported to the supervising team.

## 3. Aggregate Completeness

| Record type | Field | Completeness |
|---|---|---|
| Profiles | `skills` | 62.7% |
| Profiles | `occupation_uris` | 3.3% |
| Profiles | `content` | 95.9% |
| Profiles | `description` | 0.2% |
| Profiles | `location` | 100.0% |
| Profiles | `startdate` | 1.5% |
| Postings | `skills` | 80.4% |
| Postings | `occupations` | 83.0% |
| Postings | `description` | 92.8% |
| Postings | `location` | 99.3% |
| Postings | `nuts1`/`nuts2`/`nuts3` | ~13% |
| Postings | `upload_date` | 100.0% |

Two immediate conclusions from the aggregate alone: profiles carry almost no usable date information (`startdate` 1.5%), so any time-series work must rely on postings; and `description` is not a usable field for profiles (`content` is the real free-text field, at 95.9%). However, the aggregate numbers substantially understate how concentrated several of these fields are in specific sources — this is the more important finding of this report, detailed below.

## 4. Finding 1: `occupation_uris` Is Effectively a Revelio-Only Field

The aggregate 3.3% completeness for `occupation_uris` is not evenly distributed thinness — it is close to a binary split by source:

| Source | `occupation_uris` completeness |
|---|---|
| revelio | 94.0% |
| every other profile source (all STACK sources, linkedin) | 0.0% |

**Implication for the Tier 2 fallback (occupation URI → default skill set):** this fallback tier will only ever be reachable for Revelio-sourced profiles, which make up roughly 3.5% of the current sample. For every other source, a profile without direct skills (Tier 1) cannot fall through to Tier 2 via this field, because the field is simply absent at the source level, not missing at random. If broader Tier 2 coverage is needed, the free-text `occupation` field (which is populated far more broadly, as seen in manual inspection of sample records) would need to be mapped to an ESCO occupation URI as a pre-processing step, rather than relying on `occupation_uris` being present.

## 5. Finding 2: Regional (NUTS) Detail Is EURES-Only, but Country Is Available for Most Postings

As with `occupation_uris`, the aggregate ~13% NUTS completeness for postings hides a near-total split:

| Source | `nuts1` | `nuts2` | `nuts3` |
|---|---|---|---|
| eures | 96.2% | 95.3% | 95.1% |
| eures-escox | 92.9% | 89.1% | 87.2% |
| every other posting source (13 sources) | 0.0% | 0.0% | 0.0% |

**Implication for regional and Greece-panel analysis:** structured, ready-to-use regional analysis (NUTS1–3) is currently only possible on EURES-sourced postings. Every other source has `location` populated as free text (99–100%) but no structured regional breakdown at all. Two options follow from this:
1. Restrict NUTS-based regional analysis to the EURES subset, and state this explicitly as a scope limitation, or
2. Build a geocoding step that derives NUTS codes from the free-text `location` field for the remaining sources. This is a non-trivial addition to the pipeline and should be scoped as its own task rather than assumed to be a quick fix, given it would need to cover inconsistent free-text formats across many different job boards.

It is also worth noting that `eures` and `eures-escox` appear to be the same underlying feed processed two different ways: `eures` has only 37.8% `skills` completeness, while `eures-escox` has 100%. The "-escox" naming strongly suggests the latter has been processed through the ESCOX extraction tool (Kavargyris et al., 2025, cited in Chapter 1), which would explain the near-complete skills extraction alongside slightly lower NUTS completeness (87–93% vs. 95–96%).

**Country-level location is available more widely than NUTS.** The posting schema includes `location_code`, described as a country code ("e.g. GR, DE, FR"). It follows the Eurostat convention (`EL` for Greece, `UK` for the United Kingdom, not `GR`/`GB`) and is populated for about 93% of sampled postings. This softens the conclusion above: country-level analysis does not depend on geocoding, only regional (NUTS) analysis does. Two cautions: the sample was drawn at roughly 468 postings per source by design, so sample counts per country reflect that design and not the true distribution (true country shares need count queries filtered by `location_code`); and some sources (`brightminds` and probably `jobscentral`) show codes outside Europe. The schema also lists `nuts1`, `nuts2` and `nuts3` as "NUTS level N label" strings; the actual values have not yet been inspected.

## 6. Finding 3: Revelio's Field Profile Is a Genuine Trade-off, Not Simply "Worse" Data

Revelio was flagged in the thesis brief as a source to check for disproportionately sparse skills. This is confirmed:

- Revelio `skills` completeness: **12.4%**, against a mean of 64.1% and median of 62.8% across all other profile sources — the single lowest of any source by a wide margin.

However, Revelio is simultaneously the *strongest* source on three other fields that are weak everywhere else: `occupation_uris` (94.0%, vs. 0.0% elsewhere), `startdate` (42.0%, vs. ~0% elsewhere), and — confirmed during the Week 3 fallback-chain build, below — `sectors` (91.6%, vs. 1.2% on LinkedIn and 0.0% on every STACK source). This indicates Revelio is a structurally different kind of source — closer to a formal employment record than a free-text profile — and its weaknesses and strengths are complementary to, not simply worse than, the other sources. This supports the thesis's existing design choice of a multi-tier fallback chain: different sources carry genuinely different kinds of signal, and no single tier or source can be relied upon alone.

This trade-off has a direct, non-obvious consequence for Tier 3 of the fallback chain (sector + highest-degree prior): see Section 10 below. The field Tier 3 needs to build its prior (`sectors`) and the field it needs to validate against (`skills`) are concentrated in the same single source, and within that source they are close to mutually exclusive (91.6% vs. 12.4% completeness) — so the overlap population Tier 3 can actually learn from is far smaller than either field's completeness would suggest on its own.

### 6.1 Greek profiles: the Greece-panel check required by the brief

Profiles carry no country code, so Greek profiles were identified from the free-text `location` (`diagnostics/46_greek_profiles_check.py`, output `docs/greek_profiles_check.md`; a profile is Greek when its location names Greece or a Greek city, accents ignored). The working sample holds **99 Greek profiles of 7,222 (1.4%)**. All 99 location strings contain "Greece" (58 are the bare country, 20 "Athens, Greece", 8 "Athens, Greece and London, UK", the rest other Greek towns). None comes from Revelio: 95 come from 27 STACK sources and 4 from `linkedin`, at most 9 per source. The shares describe a sample of at most 250 profiles per source and are not a Greek share of the population.

| Field | Greek (n=99) | Non-Greek, same sources (n=6,373) |
|---|---|---|
| `skills` | 64.6% (55%-73%) | 66.1% |
| `occupation_uris` | 0.0% | 0.0% |
| `sectors` | 0.0% | 0.0% (3 of 6,373) |
| `content` | 100.0% | 98.4% |
| `startdate` | 0.0% | 0.0% |

Result. Greek profiles are not sparser than comparable profiles: the skills share is 64.6% against 66.1% in the same sources, and the Greek interval contains the comparison value. The fallback tiers split as 64.6% Tier 1 and 35.4% neither Tier 1 nor Tier 2, against 66.1% and 33.9% for the same sources. The result is a weak basis for a Greece panel for three reasons. First, the Greek profiles come from question-and-answer forums (STACK) and four LinkedIn records, so they describe forum users and not Greek workers. Second, they have no `occupation_uris`, no `sectors` and no `startdate`, so Tier 2 and Tier 3 are unreachable and no profile can be placed in time or in an occupation. Third, there are only 99 of them. The Greece panel therefore rests on postings (`kariera.gr`, 87,766 postings with a Greek location code in the population, Section 9.11), not on profiles. The Greek postings have their own limits: tags stop in December 2025 and the source ends in April 2026 (9.7 item 11, 9.3).

## 7. Finding 4: Source Naming Is Inconsistent and Needs Normalisation

Both the profile and posting source lists contain what appear to be duplicate or near-duplicate sources under inconsistent casing or naming:

- Profiles: e.g. `stack-math` vs. `STACK-Mathematics`, `stack-law` vs. `STACK-Law` (14 such pairs across the 29 profile sources).
- Postings: e.g. `jobbguru` vs. `jobbguru.se`, `jobmedic` vs. `jobmedic.co.uk`, `lesjeudis` vs. `lesjeudis.com`.

**Update:** the suffixed postings sources are not independent country variants. A duplicate check on the working sample (`diagnostics/20_check_duplicate_postings.py`, Section 13.4) found that the same postings appear under both names in four pairs: `jobbguru`/`jobbguru.se`, `jobbland`/`jobbland.se`, `lesjeudis`/`lesjeudis.com` and `jobmedic`/`jobmedic.co.uk`. These must be merged, not kept as separate sources. The STACK profile sources are also likely duplicates introduced at the ingestion stage, since the paired completeness figures (e.g. `stack-math` 60.4% vs. `STACK-Mathematics` 96.8% skills completeness) differ enough to suggest they are not simply case variants of an identical dataset, but may instead reflect two separate scrapes or processing passes of the same topic area. This should be resolved with a source-normalisation step before `source` is treated as a clean categorical variable in any analysis (e.g. the DGI's labour-market sub-index), and is flagged here rather than resolved silently.

## 8. Finding 5: No Multi-Role Career History Is Available for Any Profile

The brief's Week 2 activities explicitly call for confirming "career history depth (multiple roles per profile, with dates) needed for transition analysis." This was checked directly and the answer is negative: **the Skillab tracker API does not provide multi-role career history for profiles, structurally or otherwise.**

Three independent checks confirm this:

1. **Type-checked across all 27 fields on all 7,222 sample profiles**, the only list-typed fields are `skills`, `occupation_uris`, and `sectors` — none of which is a role/position history. The three role-adjacent fields (`company`, `occupation`, `startdate`) are strictly scalar; no profile in the sample carries more than one value under any of them.
2. Those three fields are themselves very sparse: `company` 2.9%, `occupation` 6.9%, `startdate` 1.5%.
3. **Confirmed against the live API schema directly** (Swagger docs, `ProfileSchema`), not just inferred from the sample: the schema's 27 fields match exactly what the sample shows, and the only profile-related endpoints in the entire API are `POST /api/profiles`, `GET /api/profiles/sources`, `GET /api/descriptive-analytics/profiles`, `GET /api/exploratory-analytics/profiles/skills-by-location`, and `GET /api/clustering-analytics/profiles`. None exposes positions, experience, or work history in any form.

As a secondary check, the free-text `content` bio field was scanned for multiple distinct years mentioned (a rough proxy for prose-narrated career history, since there's no structured field for it): only 4.3% of profiles with content mention two or more distinct years at all, which is an upper bound on how many profiles *might* narrate a transition in prose — not a confirmed count, and would require dedicated NLP extraction to verify even that.

**Implication:** any thesis analysis that depends on tracking an individual's role-to-role transitions over time cannot be built from this API's profile data as currently exposed. This is a scope-level finding that should be raised with the supervising team directly, rather than something resolvable through better querying or additional fallback logic — the data simply isn't there. Depending on how central multi-role transition tracking is to the thesis's planned analysis, this may require either restructuring that part of the analysis to rely on postings-level signals (e.g. aggregate occupation/skill shifts across the corpus over time, rather than individual career trajectories) or seeking a supplementary data source.

**Role start dates (`startdate`) exist only in Revelio.** In a sample of 250 profiles per profile source (`diagnostics/29`, Part B), `startdate` was filled for 105 of 250 Revelio profiles (42%) and for none of the LinkedIn and STACK profiles. Revelio start years run back to the 1970s; 6 of the 105 fall in 2019–2020, all in Germany. A role start date marks when the person's current role began, so it could give a hiring-by-date series for people still in that role, with survivorship bias (people who left are absent). `ProfileFilter` has no date field, so a population-level count would require paging through the Revelio profiles; the size of that source and the year distribution of start dates have not been measured.

## 9. Date Coverage and the Pre-Shock Baseline

This section replaces an earlier version that concluded "15 of 16 posting sources confirm coverage from 2019 onward". That statement was true but misleading for the thesis: "has data from 2019 onward" is not the same as "has data in the brief's 2019–2020 baseline window". Most sources pass the first test and fail the second.

### 9.1 Method and its limits

Coverage was measured with the API's `min_upload_date` / `max_upload_date` filters, using the `count` returned with a `page_size=100` request (a `page_size=1` count-only query proved unreliable and was dropped). Two query shapes were used:

- **Open-ended** (`min = <year>-01-01`, `max = today`) at the checkpoints 2019, 2021, 2023, 2024, 2025 and 2026. The count never rises as the checkpoint year rises, so identical counts at consecutive checkpoints mean no postings fall between them. For example, a source with the same count at 2019, 2021 and 2023 has every posting dated 2023 or later. Counts for an interval are obtained by subtraction.
- **Closed windows** (calendar year, then calendar month) for `OJA`, whose open-ended probes all timed out.

Two caveats apply throughout. First, the dataset is live and keeps growing, so counts taken on different days are snapshots, and subtraction across snapshots is a derivation, not a measurement (for example, `eures` grew from 362,902 to 401,511 between two measurement dates). Second, **a timeout is not informative.** Closed windows with no matching postings are slow (the empty months of 2025 each needed one to three retries or failed outright), but large windows also time out (2024-10 and 2024-12 failed three times and later returned 53,906 and 48,950). Persistently failing closed windows have so far usually turned out to be empty (`jobs.de` and `kariera.fr` for 2026, `jobbland` for 2025 onward, OJA from April 2025, and the 2019–2020 windows of several boards), but this is a hint and not proof, so every such window is confirmed by a positive measurement of its complement (a successful count for the neighbouring window that equals the known total) before being reported as zero.

### 9.2 What `upload_date` means

For the scraped job boards, `upload_date` was first understood to be the posting date on the source board (stated by the project author; the API schema says only "Date when the job was uploaded"). The supervisor's later reply (Section 11, item 10) is that `upload_date` does not necessarily correspond to the original posting date and that its meaning depends on the source; for the EURES family it is the insertion date. The "posting date" reading should therefore not be relied on. For `OJA` the position is less clean. The Eurostat Web Intelligence Hub (WIH) metadata report (23 July 2026) defines the corresponding source variable `first_active_date` as the date the posting is first detected for a source, replaced by the publication date where the advertisement states one. If Skillab's `upload_date` derives from that field, OJA dates are a mixture of publication and first-detection dates. This mapping is **not verified**. The EURES family is a different case: it is an aggregator portal, not a scraped board, so the confirmation does not obviously apply. A secondary description of the EURES portal (not Skillab documentation, and not independently verified) says its date filter ("publication date") records when a vacancy notice was transmitted, imported or published onto the EURES database, which keeps notices only while they are current. The monthly counts for `eures-escox` do not fit a steady flow of postings or a stock of survivors rising towards the present. All 828,524 postings dated 2026 fall in two months: 130,336 in January and 698,188 in February (the two sum exactly to the 2026-onward total, so March–July are zero by subtraction, and August–October were measured at zero). Nothing is dated after February 2026, and a single month holds more than ten times the whole of 2025 (62,512). `eures` shows the same pattern: 99,040 postings in January and 260,801 in February 2026, which sum exactly to its 2026-onward total (359,841), so nothing is dated after February 2026. This looks like a bulk load, so for the EURES family `upload_date` behaves like an import date and does not measure when employers posted the vacancy. The EURES family is therefore **not usable for time-series analysis**. Whether the 2025 counts (41,090 for `eures`, 62,512 for `eures-escox`) are also clustered into a few import months could not be established: all twelve monthly probes for `eures-escox` 2025 timed out on every attempt. This does not change the conclusion above. The question for the Skillab team is in Section 11.

### 9.3 Posting sources other than OJA: one-year snapshots, late ramp-ups, almost no baseline

Postings by period, derived from open-ended counts (identical counts at consecutive checkpoints mean an empty interval). The pre-2024 columns combine counts taken on different days, so small differences between snapshots are possible.

| Source | 2019–2020 | 2021–2023 | 2024 | 2025 | 2026 to date | No `upload_date` |
|---|---|---|---|---|---|---|
| brightminds | 0 | 0 | 1 | 0 | 0 | 0 |
| jobbguru, jobbguru.se | 0 | 0 | 319 each | 0 | 0 | 0 |
| jobmedic / jobmedic.co.uk | 0 | 0 | 1,010 / 1,448 | 0 | 0 | 0 |
| jobscentral | 0 | 0 | 6,284 | 0 | 0 | 0 |
| lesjeudis | 0 | 0 | 18,404 | 0 | 0 | 0 |
| lesjeudis.com | 0 | 0 | 24,741 | 23,055 | 7,579 | 0 |
| kariera.gr | 0 | 0 | 24,306 | 36,194 | 27,266 | 0 |
| kariera.fr | 0 | 0 | 74,975 | 11,493 | 0 (derived) | 0 |
| jobs.de | 0 | 0 | 27,680 | 6,550 | 0 (derived) | 0 |
| eures | 0 | 444 | 136 | 41,090 | 359,841 | **158,689** |
| eures-escox | 0 | 426 | 151 | 62,512 | 828,524 | **647,773** |
| jobbland.se | 90 | about 1,550 | 167,678 | 138,867 | 386,638 | 0 |
| jobbland | 9 | about 1,114 | 66,969 | 0 | 0 (derived) | 0 |

The last column is the all-time count (no date filter) minus the count inside a 1900–2100 date window (`diagnostics/29`, Part A; see Section 9.6, item 8). The period columns count only postings that have an `upload_date`. For the EURES family the two together give the full source: `eures` 401,511 dated + 158,689 undated = 560,200, and `eures-escox` 891,613 + 647,773 = 1,539,386, i.e. 2,099,586 postings in the two sources. Without the last column the table shows only 62% of them.

(The 417 `eures-escox` postings for 2023 match an independent check made earlier in the project. Pre-2019 coverage of `eures-escox` and `jobbland.se` remains unresolved.)

What this shows:

- **Six boards are essentially one-year snapshots of 2024** (`brightminds`, `jobbguru`/`.se`, `jobmedic`/`.co.uk`, `jobscentral`, `lesjeudis`, and `jobbland`, which also has about 1,100 postings in 2021–2023 and nothing after 2024), with nothing or almost nothing before or after. They support cross-sectional analysis of 2024 only.
- **No source other than OJA has a usable 2019–2020 baseline.** The only non-zero values are 9 and 90 postings for `jobbland` and `jobbland.se`.
- **Data after March 2025 exists only outside OJA**, in `eures`, `eures-escox` (cross-sectional use only, see below), `jobbland.se`, `kariera.gr` and `lesjeudis.com`, plus `jobs.de` and `kariera.fr` for 2025 only (6,550 and 11,493 postings, measured directly with closed 2025 windows, which also show that neither source has anything dated 2026). These are different sources, with a different mix from the baseline.
- **The EURES family is almost entirely 2025–2026 and highly clustered.** Only about 0.14% of `eures` postings and 0.06% of `eures-escox` postings predate 2025. For `eures-escox`, 2026 consists of 130,336 postings in January and 698,188 in February and nothing afterwards (see 9.2). The dates describe import events and not posting activity, so this family can support cross-sectional analysis (composition, skills) but not any trend over time.
- **Where the monthly series begin.** For `kariera.gr`, `lesjeudis.com`, `jobs.de` and `kariera.fr` the all-time total of postings with a location code, taken from the server's location endpoint (`diagnostics/43`), equals the sum of the monthly counts of Section 9.9 exactly (87,766; 55,375; 34,230; 86,468), so nothing with a location code lies outside August 2024 and the last month counted. Direct counts for January and February 2024 (and March for three of the four) also gave 0 (`diagnostics/40`). `jobbland.se` begins earlier and as a ramp: 191, 246, 292, 410, 2,116, 2,879 and 2,060 postings in January to July 2024 (8,194 together; with August to December 2024, 159,484, they give the 167,678 of the table), against 4,184 in August and 48,018 in October. Its all-time total of 694,838 is the 2024 to 2026 columns of the table (693,183) plus 1,655 dated before 2024 (90 and about 1,550 in the first two columns). The ramp reflects growing collection, not labour demand.

### 9.4 OJA: the only baseline source, with a structural break

`OJA` is the only source with substantial data in 2019–2020, and also has 123,200 postings before 2019. Yearly counts (closed windows):

| Year | Postings | Average per month |
|---|---|---|
| 2019 | 213,934 | 17,828 |
| 2020 | 193,611 | 16,134 |
| 2021 | 172,182 | 14,348 |
| 2022 | 119,632 | 9,969 |
| 2023 | 103,263 | 8,605 |
| 2024 | 2,098,325 | 174,860 |
| 2025 | 23,288 | 1,941 |
| **2019–2025** | **2,924,235** | |

(The 2019 + 2020 total of 407,545 matches the independent direct 2019–2020 probe, and the sum of the yearly counts matches the earlier 2019-onward total of 2,924,235.)

Monthly counts around the break (2023 months sum to 103,263 and 2024 months to 2,098,325, matching the yearly totals):

| Month | 2023 | 2024 | 2025 |
|---|---|---|---|
| Jan | 14,600 | 276,271 | 9,439 |
| Feb | 11,362 | 236,890 | 7,499 |
| Mar | 11,652 | 208,162 | 6,350 |
| Apr | 10,162 | 243,099 | 0 |
| May | 6,847 | 221,152 | 0 |
| Jun | 7,275 | 203,323 | 0 |
| Jul | 5,680 | 222,488 | 0 |
| Aug | 5,604 | 149,292 | 0 |
| Sep | 9,473 | 176,584 | 0 |
| Oct | 7,685 | 53,906 | 0 |
| Nov | 7,532 | 58,208 | 0 (derived)² |
| Dec | 5,391 | 48,950 | 0 (derived)² |

² The November and December 2025 probes timed out; the three non-empty months of 2025 sum exactly to the 2025 yearly total, so the remaining months must be zero.

Three features matter for the design:

1. **OJA data ends in March 2025.** April–October 2025 are measured as zero, with no gradual tail. An independent thesis using the same API reports that its extraction also stopped at March 2025 (citation to be added). The usable OJA window is **January 2019 to March 2025**.
2. **A 51-fold step occurs on 1 January 2024.** December 2023 has 5,391 postings and January 2024 has 276,271. After January the monthly count decays to about 50,000 by Q4 2024 and 6,000–9,000 in Q1 2025. This is not labour-market behaviour. The step is a change in occupation coverage: 95% of January 2024 postings belong to 11 ISCO codes that have no postings in December 2023, and ten of them exist only in 2024 (Sections 9.4c and 9.4d). Why those occupations enter the data in January 2024 is not known (question (g) in Section 11).
3. **The 2019–2023 decline** (about 17,800 to 8,600 postings a month) is smaller but also unexplained, and may likewise reflect changes in source mix. The WIH report states that OJA draws on over 400 sources, some unstable, and recommends restricting time-series work to stable sources. Skillab exposes only `source = "OJA"`, so source-level stability cannot currently be checked.

### 9.4a What OJA records contain, and how results are ordered

Inspection of 17 result pages (100 postings each) drawn from five months of OJA (June 2019, December 2023, January, February and December 2024; `diagnostics/21` and `22`) shows:

- **OJA records carry no text.** In every sampled posting `title` is an empty string, and `description` and `organization` are null; `sectors` is an empty list (consistent with 0/468 in the working sample). What an OJA record does carry is one ISCO-08 4-digit occupation (as an ESCO URI, always exactly one), a list of ESCO skill URIs, `experience_level`, `location`/`location_code` and `upload_date`. OJA postings therefore cannot be used with text methods (TF-IDF, embeddings, LLM classification of descriptions). Any task- or skill-based measure on the baseline period has to be built from the ESCO skill URIs and ISCO codes.
- **Results are ordered by `id`, and ids are laid out in blocks by occupation.** Each sampled page contained one ISCO 4-digit code (or two, at a block boundary): for example 3141 for ids 2,873,601–2,878,439 in June 2019 (at least 45 consecutive pages, a large share of that month), 2511/2512/2513 for ids 196,370–796,440 in January and February 2024, and 2431 for ids around 2.43–2.48 million in the same months. A page is therefore not a random draw, and a random-page sample reflects the blocks it lands on, not the month's composition.
- **The January 2024 step coincides with a change of block** (see 9.4b for the grid result). All January and February 2024 pages at low ids (60, 508, 863 of 2,763; 112, 1129, 1512 of 2,369) were ISCO 251x (software and applications professionals), with 100 postings per page on a single upload date. Whether the 51-fold increase is a bulk ingest of ICT-occupation postings cannot be settled from five pages per window; the systematic page grid (`diagnostics/24`) and country counts (`diagnostics/23`) are designed to test it.
- **Missing country codes.** 40% of the sampled January and February 2024 postings had no `location_code`, against none in June 2019, December 2023 and December 2024.
- **The OJA content in Skillab may not be the full Eurostat OJA.** Only about a dozen distinct ISCO codes appeared in 17 pages, with long runs of single codes. If Skillab holds OJA for a restricted set of occupations, OJA is not a representative baseline of the labour market. This is unconfirmed and is a question for Skillab.

### 9.4b Systematic page grid: December 2023 versus January 2024

Because results are ordered by `id` and ids come in occupation blocks, 24 evenly spaced pages through a month (`diagnostics/24`) give a systematic sample of the blocks. Each grid page is one point; a block shorter than about 4% of the month can be missed.

| | December 2023 (5,391 postings) | January 2024 (276,271 postings) |
|---|---|---|
| Dominant ISCO 4-digit codes (share of grid pages' postings) | 8131 chemical products plant operators 42%; 3141 life science technicians 23%; 2113 chemists 13%; 2133 environmental protection professionals 10%; 7124 insulation workers 5%; 3116 chemical engineering technicians 4%; 8114 mineral products machine operators about 4% | 2511 systems analysts 32%; 2512 software developers 27%; 2431 advertising and marketing professionals 17%; 2513, 2330 (secondary education teachers), 3312 (credit and loans officers), 1211 (finance managers) and 2133 about 4% each |
| ISCO major groups | 8: 45%, 3: 27%, 2: 23%, 7: 5% | 2: 92%, 1: 4%, 3: 4% |
| Id range | 2.98 M to 4.41 M | 196,170 to 442,308 (first 16 of 24 grid pages), then 2.13 M to 3.85 M |
| Pages with no `location_code` at all | 0 of 24 | 7 of 24 (all in the id range 2.13–2.72 M: 2330, 2431, 3312, 1211) |
| Non-empty `title` / `description` | 0 / 0 of 2,400 | 0 / 0 of 2,400 |

What this shows:

1. **The January 2024 step is mostly a block of ICT postings that is absent in December 2023.** Sixteen of the 24 January grid pages (the first 65% of the month, ids 196,170–442,308) are ISCO 2511/2512 postings, (population counts in 9.4c: ISCO 251x holds 186,694 of the 276,271 postings, 67.6%). None of the 24 December grid pages was an ICT code. These January pages carry `location_code` (FR, DE, SE, NL, ES, PT).
2. **The rest of January is also a different mix and still larger than all of December.** The other 89,577 postings (32.4%) are mostly marketing (2431), finance (1211, 3312, 2413) and education (2330) codes, many without a country code. That alone is about 17 times the whole of December 2023.
3. **Each month consists of a handful of occupation blocks, and the set of blocks differs between months.** December 2023 is dominated by chemical, laboratory and environmental occupations; June 2019 by 3141 and 2145 (chemical engineers); January 2024 by ICT, marketing, finance and education. Some codes recur (3141 in June 2019 and December 2023; 2133 in December 2023 and January 2024; 2431 and 1211 through 2024), so a within-occupation panel is possible for a small number of codes.
4. **Consequence.** OJA monthly totals are not a labour-market series. Their level and their 2019–2023 decline, like the January 2024 step, depend on which occupation batches the data holds for a month. This must be settled (`diagnostics/25`: counts per ISCO code and window) before OJA is used as the baseline, and it is a question for Skillab whether OJA is the full Eurostat OJA or a set of occupation-specific extracts.

### 9.4c Population counts per ISCO code: December 2023 versus January 2024

Filtered count queries (`diagnostics/25`, occupation filter by ESCO ISCO URI) over the whole of each month:

| ISCO | Occupation | Dec 2023 | Jan 2024 |
|---|---|---|---|
| 3141 | Life science technicians | 1,184 | 1,783 |
| 3116 | Chemical engineering technicians | 125 | 234 |
| 2113 | Chemists | 721 | 931 |
| 2133 | Environmental protection professionals | 632 | 835 |
| 8131 | Chemical products plant and machine operators | 2,286 | 3,462 |
| 8114 | Cement, stone and other mineral products machine operators | 166 | 271 |
| 7124 | Insulation workers | 267 | 417 |
| **Subtotal, 7 codes present in both months** | | **5,381** | **7,933** |
| 2145 | Chemical engineers | 0 | 787 |
| 2511 / 2512 / 2513 / 2514 / 2519 | Software and systems (ISCO 251x) | 0 | 82,859 / 82,064 / 12,813 / 5,361 / 3,597 |
| 2431 | Advertising and marketing professionals | 0 | 45,971 |
| 1211 | Finance managers | 0 | 15,802 |
| 2330 | Secondary education teachers | 0 | 8,159 |
| 3312 / 2413 | Credit and loans officers; financial investment advisers | 0 | 2,950 / 2,258 |
| **Subtotal, 11 codes absent in December** | | **0** | **262,621** |
| Other codes | | 10 | 5,717 |
| **Window total** | | **5,391** | **276,271** |

- **Eighteen codes account for 99.8% of December 2023 and 97.9% of January 2024.** A month of OJA in Skillab consists of very few occupations.
- **The seven codes present in both months grow by 47%** (5,381 to 7,933), within the range of ordinary month-to-month movement in the 2023 monthly series (5,391 to 14,600). They show no step.
- **The 51-fold step is entirely the entry of 11 new codes**, which make up 95.1% of January 2024 (262,621 of 276,271).
- **Reading.** OJA in Skillab looks like an extract restricted to a set of occupations, and that set changes over time. Raw monthly OJA totals therefore measure which occupations are covered, not labour demand. Whether this is by design, and which occupations are covered when, is a question for Skillab (question (g)). A baseline can only be built within occupations that are present throughout, and the next step is a code-by-year (and, for the key codes, code-by-month) count from 2019 to March 2025.

### 9.4d Population counts per ISCO code, 2019 to March 2025

Same method as 9.4c, one window per calendar year (`diagnostics/25`; 2025 = January to March, the only months with data):

| ISCO | Occupation | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 (Jan–Mar) |
|---|---|---|---|---|---|---|---|---|
| 3141 | Life science technicians | 96,054 | 84,132 | 68,402 | 27,692 | 25,929 | 11,538 | 4,413 |
| 8131 | Chemical products plant and machine operators | 49,062 | 41,846 | 42,607 | 38,480 | 29,442 | 22,261 | 9,501 |
| 2113 | Chemists | 18,354 | 17,095 | 16,897 | 15,743 | 15,246 | 6,540 | 2,195 |
| 2133 | Environmental protection professionals | 17,491 | 15,342 | 14,406 | 12,492 | 11,687 | 6,784 | 1,772 |
| 2145 | Chemical engineers | 16,729 | 16,618 | 12,699 | 10,955 | 6,245 | 7,901 | 2,733 |
| 3116 | Chemical engineering technicians | 5,948 | 6,516 | 5,752 | 4,869 | 4,601 | 2,233 | 827 |
| 8114 | Cement, stone and other mineral products machine operators | 4,725 | 5,869 | 5,813 | 3,282 | 3,452 | 1,904 | 899 |
| 7124 | Insulation workers | 4,090 | 4,457 | 4,475 | 5,452 | 6,021 | 1,313 | 819 |
| **Eight core codes** | | **212,453** | **191,875** | **171,051** | **118,965** | **102,623** | **60,474** | **23,159** |
| 2511 / 2512 / 2513 / 2514 / 2519 (software and systems) | | 0 | 0 | 0 | 0 | 0 | 1,256,589 | 0 |
| 2431 marketing; 1211 finance managers; 2330 secondary teachers; 3312 credit officers; 2413 investment advisers | | 0 | 0 | 0 | 0 | 0 | 720,735 | 0 |
| Other codes | | 1,481 | 1,736 | 1,131 | 667 | 640 | 60,527 | 129 |
| **Window total** | | **213,934** | **193,611** | **172,182** | **119,632** | **103,263** | **2,098,325** | **23,288** |

What this shows:

1. **OJA in Skillab is an extract restricted to eight ISCO codes, all in chemical and process industries, laboratory work and the environment.** They account for 99.1% to 99.5% of postings in every year from 2019 to 2023 and in January–March 2025 (other codes: 0.5% to 0.9%). It is not a cross-section of the labour market, and the baseline of 407,545 postings for 2019–2020 consists of these eight occupations (3141 alone is 44% of it).
2. **Ten further codes (ICT, marketing, finance, education) exist only in 2024**, where they make up 94.2% of postings (1,977,324 of 2,098,325). They are zero in 2023 and in January–March 2025. The 2024 total therefore cannot be compared with any other year, and it is the sole cause of the structural break described in 9.4.
3. **The eight core codes form a continuous series from January 2019 to March 2025**, and this is the only OJA content that does. It falls from 212,453 (2019) to 102,623 (2023) and 60,474 (2024). The fall is very uneven: ISCO 3141 drops by 73% between 2019 and 2023, while 7124 rises by 47%. Whether these movements are labour demand or changes in the underlying sources (the WIH report warns that OJA's >400 sources are not all stable) cannot be told from Skillab.
4. **Consequence for the design.** The occupations that can be followed over the whole period are a narrow slice of the economy. They are not representative of European labour demand, and OJA carries no text (9.4a), so language-based indicators cannot be built from OJA postings. Possible uses are a within-occupation panel of the eight core codes (counts or shares by country and month, with skills as the content variable), or a reframing of the thesis's measurement around what Skillab holds. This is a decision for the supervisor and is the main open issue for Month 2.

### 9.5 Consequences for the research design

**Update, 13 October 2026:** the supervisor has decided that the case study covers 2024 to date (Section 9.8). The bullets below record the options that were considered while a 2019–2020 baseline was still being sought; those that rely on OJA or on a 2019–2020 baseline no longer apply, the others (shares instead of counts, no pooling of sources, event-study within sources) carry over.

- **No source spans the whole period.** The baseline (2019–2020) exists only in OJA, which ends in March 2025. Everything after March 2025 comes from other sources that have almost nothing before 2024 or 2025. Pooling them would confound any change in deglobalisation language with a change in source and country mix.
- **Raw counts are driven by ingestion** and cannot measure labour demand, in OJA (the January 2024 step) or in the EURES family (the 2026 ramp-up). Analyses should use **shares and rates within each period**, with composition (country via `location_code`, occupation group, sector) checked.
- **The brief's validation windows are covered unevenly.** The 2022 energy-crisis and 2023 Chips Act windows fall inside the 2019–2023 OJA regime. The 2025 tariff window can be examined only (a) in OJA for January–March 2025, which precedes the main April measures, and (b) in within-source series for `eures-escox`, `jobbland.se` and `kariera.gr`, analysed separately and never pooled with OJA without calibration.
- **Bridging is possible only where sources overlap**: OJA against `kariera.gr`, `lesjeudis.com`, `jobbland.se`, `jobs.de` and `kariera.fr` during 2024, and against the EURES family and the same boards in January–March 2025. A calibration on country and occupation shares in those months is the natural design, but it needs the composition analysis first.
- **The supervisor advises excluding OJA** (Section 11, item 10). Without it, the pre-shock window available in Skillab starts in August 2024. The 2025 tariff period can then be studied as an event-study within sources: `kariera.gr` (Greece, August 2024 to April 2026), `lesjeudis.com` (France, August 2024 to March 2026) and `jobbland.se` (Sweden, 2024 to 2026), each with eight months before April 2025 and, for the first two, a year or more after. Monthly volumes in all of these sources move by an order of magnitude for collection reasons (Section 9.6, point 6), so only within-source shares can be used, never counts. The 2022 and 2023 validation windows cannot be tested outside OJA. This reframing needs the supervisor's agreement.
- **OJA's occupation coverage changes over time and is narrow** (Sections 9.4c and 9.4d), so the monthly total must not be used as a series. Only eight ISCO codes (chemical and process industries, laboratory, environment) run from 2019 to March 2025; ten others exist only in 2024.
- **Provisional recommendation (to be agreed with the supervisor):** restrict any OJA series to the eight core codes. The earlier plan (2019–2023 OJA as the primary series, 2024 to March 2025 as a second regime, post-March 2025 sources as a separate supplementary analysis) no longer holds for OJA as a whole, because the 2024 regime is a different set of occupations. The post-March 2025 supplementary analysis is unaffected. All of this must be reconciled with the brief's timeline (monthly data to 2026).
- Profiles carry almost no usable dates (`startdate` 1.5%), so all time-series work rests on postings.

### 9.6 Independent check with the API's trend endpoint

`GET /api/trend-analytics/jobs/skills-by-location` (listed in the API documentation as "job counts per month by location code") returns one row per source, country and month, aggregated on the server (`diagnostics/26`, `27`). It was used to test whether our POST `/jobs` counts, and therefore the empty years in the non-OJA sources, are a querying error.

| Source | Our filtered counts | Trend endpoint | Agreement |
|---|---|---|---|
| OJA 2018–2023, 2025 | 123,200; 213,934; 193,611; 172,182; 119,632; 103,263; 23,288 | identical for every year | exact |
| OJA 2024 | 2,098,325 | 1,422,236 | trend lower by 676,089 (32.2%), the postings without `location_code` (see below) |
| eures 2021–23 / 2024 / 2025 / 2026 | 444 / 136 / 41,090 / 359,841 | 444 / 136 / 41,087 / 359,831 | exact, except 3 and 10 postings |
| eures-escox 2021–23 / 2024 / 2025 / 2026 | 426 / 151 / 62,512 / 828,524 | 426 / 150 / 62,503 / 828,486 | exact, except 1, 9 and 38 postings |
| kariera.gr 2024 / 2025 / 2026 | 24,306 / 36,194 / 27,266 | identical | exact |
| jobbland.se 2019–20 / 2021–23 / 2024 / 2025 | 90 / ~1,550 / 167,678 / 138,867 | 90 / 1,550 / 167,678 / 138,867 | exact |
| jobbland 2019–20 / 2021–23 / 2024 | 9 / ~1,114 / 66,969 | 9 / 1,114 / 66,969 | exact |
| jobs.de, kariera.fr, lesjeudis.com, lesjeudis, jobmedic.co.uk, jobmedic, jobbguru.se, jobbguru | as in 9.3 | identical | exact |
| jobscentral (6,284 in 2024), brightminds (1) | present | no rows at all | these sources have no `location_code`, and the endpoint omits postings without one |

What this establishes:

1. **Our counts are right.** For 13 of the 16 sources, and for OJA in every year but 2024, the two methods agree exactly or to within a few dozen postings, so the near-empty years before 2024 in the non-OJA sources are in the data, not a result of how we query.
2. **The trend endpoint omits postings without a `location_code`.** This explains the jobscentral and brightminds rows, the few missing EURES postings, and the 2024 OJA gap of 32.2%, which matches the 29% of January 2024 grid pages that had no country code (Section 9.4b).
3. **The scraped boards all begin in August 2024.** `kariera.gr`, `jobs.de`, `kariera.fr`, `lesjeudis(.com)`, `jobmedic(.co.uk)` and `jobbguru(.se)` each have their first month in August 2024. Their last months differ: `jobbguru` September 2024, `lesjeudis` and `jobmedic` and `jobbland` November–December 2024, `kariera.fr` March 2025, `jobs.de` April 2025, `lesjeudis.com` March 2026 and `kariera.gr` April 2026.
4. **Sparse earlier postings exist in a few sources.** `jobbland.se` has a handful of postings from 2017 on (59 in 2019, 31 in 2020, 70 in 2021, 249 in 2022, 1,231 in 2023) and the EURES family from November 2021 (about 10 per year until 2023), too few to form a series.
5. **Date errors.** `jobbland.se` has 7 postings dated 2027 and apparently 2 more dated after today in 2026 (its trend total for 2026 is 2 higher than our count up to today), so `upload_date` is not reliable for every record.

6. **Monthly volumes are driven by collection, not by the labour market, in every source.** From `docs/coverage_population.md`, Section 4:
   - `jobbland.se` effectively starts in May 2024 (2,116; only 191–410 a month before), peaks at 48,018–53,139 a month from October 2024 to January 2025, falls to 23,017 (February 2025), 10,959 (March), 4,139 (April) and 132 (June 2025), then climbs again to 28,639 (December 2025) and 40,000–62,000 a month in 2026. Its last month, September 2026, holds only 595 (incomplete). Any pre/post comparison around April 2025 would be dominated by this swing.
   - `kariera.gr` falls to 61 and 37 postings in October and November 2025 and recovers to 3,308 in December.
   - `lesjeudis.com` goes from 4,191 (January 2025) to 450 (March 2025), back to 3,887 (June 2025) and 250 (January 2026).
   - The EURES family is about 100 postings a month until August 2025, then grows steeply: 937 (September 2025), 1,523, 15,811, 21,926, 99,039 (January 2026) and 260,792 (February 2026) for `eures`; `eures-escox` follows the same pattern at 2.7 times the size in February 2026. It stops after February 2026.
7. **Country totals double-count duplicate pairs.** Swedish postings in 2024 (235,285) are `jobbland.se` 167,678 + `jobbland` 66,969 + `jobbguru` and `jobbguru.se` 319 each, and the French and British figures are inflated in the same way. Section 13.4 describes the merge used in the sample; the population-level overlap of the pairs is still unconfirmed.

8. **Postings with no `upload_date` exist in the EURES family and are invisible to every date-windowed query.** Comparing the count with no date filter to the count in a 1900–2100 window (`diagnostics/29`, Part A):

   | Source | All-time count | With an `upload_date` | No `upload_date` |
   |---|---|---|---|
   | eures | 560,200 | 401,511 | 158,689 (28%) |
   | eures-escox | 1,539,386 | 891,613 | 647,773 (42%) |

   For the other 13 non-OJA sources the two counts are identical, so no postings are hidden. All yearly and monthly EURES-family figures in this report (Sections 9.3 and 9.6, `docs/coverage_population.md`) therefore describe only the dated 72% and 58%. 806,462 postings in the EURES family have no date at all; `diagnostics/30` sampled 40 evenly spaced pages of each source's unfiltered result set (`docs/undated_postings_grid.md`). Findings: (i) the undated postings are not an archive of older records. They lie in the same id range (about 6.25M to 8.35M) as the dated postings, whose dates are almost all 2025–2026 (a few 2023–2024 on the first pages), and the sampled undated postings are live-looking vacancies (for example a 2026 summer-substitute post). Their text mentions 2026 far more often than any other year (113 of 156 year mentions in eures, 148 of 218 in eures-escox); mentions of 2019 or 2020 are a handful (eures: 4 for 2020; eures-escox: 5 and 4) and occur at about the same rate in dated postings, i.e. incidental references such as years of experience. (ii) Missing dates are a feed property: many pages are 100% undated and come from a single country (DE, FR, NL, AT, ES), while other pages of the same countries are fully dated, so whole ingestion batches arrive without `upload_date`. This is consistent with the supervisor's remark that empty fields follow the source data structure. (iii) Share in the sample: 31% (eures) and 51% (eures-escox) of grid postings; the population figures above (28%, 42%) are the authoritative ones, the grid is for locating them. Conclusion: the undated EURES postings are not a source of 2019–2020 data. Consequence for 2026 analysis: dated-only counts under-represent FR, NL, ES and AT feeds, so country composition computed from dated postings alone is biased. This conclusion rests on sampled text and id position, not on a known publication date. `diagnostics/31` (`docs/field_audit.md`; 35 pages, 3,500 `eures` postings, of which 31% undated; `eures-escox` sampled separately, see Section 9.7) adds three points. (a) The API returns no field beyond the documented JobSchema, and `upload_date` is its only date, so no collection or insertion date can be recovered for the undated postings through the API; whether the database holds one that the API does not expose is a question for the tracker's maintainers. (b) Undated records are thinner than dated ones: non-empty `skills` 13% versus 60%, `location` 55% versus 97%, `organization` 77% versus 96%, `description` 91% versus 98%, `type` 93% versus 100%, which fits a different feed format. (c) Test of the id as a clock: predicting a dated posting's `upload_date` from the nearest dated posting on a different page gives a median absolute error of 10 days (75th percentile 26, 90th 69, maximum 293), with 45% of predictions within 7 days and 78% within 31 days; 14 of 31 neighbouring page pairs run backwards (dates do not rise strictly with id). Id-based dating would therefore be coarse, at best usable for quarterly placement and always labelled as imputed. It would also be extrapolation in the newest ids, where the sampled pages 4762, 4948, 5322 and 5509 are 96–100% undated. In any case it could only place these postings in 2025–2026.

Population-level coverage tables by source, year, country and month are in `docs/coverage_population.md` (generated by `diagnostics/27`). They cover postings with a country code only.

### 9.7 Fields returned by every source, and how complete they are

`diagnostics/31` (`docs/field_audit.md`) fetched evenly spaced pages of each source (5 pages, about 500 postings, per board; `jobbguru`/`jobbguru.se` 3 pages, `brightminds` its single posting; `eures` 35 pages, 3,500 postings) and recorded every key in the raw JSON, including keys that are always null. `eures-escox` (200 postings, 8 pages of 25 rows) was fetched in a separate run because the server dropped every request of 100 rows for that source. Findings:

1. **No field is missing from our schema.** Every source returns exactly the documented JobSchema keys: no undocumented key appears anywhere, and no documented key is absent. `upload_date` is the only date.
2. **What differs is how often the fields are filled.** Share of sampled postings with a non-empty value (dated postings only for `eures` and `eures-escox`; "0%" means no non-empty value in the sample):

| Source | Sampled | description | exp. level | type | location | location_code | nuts1 | occupations | sectors | skills | organization |
|---|---|---|---|---|---|---|---|---|---|---|---|
| kariera.gr | 500 | 100% | 99% | 100% | 100% | 100% | 11% | 58% | 52% | 57% | 0% |
| kariera.fr | 500 | 98% | 2% | 100% | 100% | 100% | 0% | 88% | 74% | 92% | 0% |
| jobs.de | 500 | 100% | 2% | 100% | 100% | 100% | 0% | 83% | 77% | 80% | 0% |
| lesjeudis | 500 | 100% | 100% | 100% | 100% | 100% | 0% | 98% | 96% | 99% | 0% |
| lesjeudis.com | 500 | 100% | 44% | 100% | 100% | 100% | 3% | 96% | 93% | 99% | 0% |
| jobbguru | 219 | 100% | 100% | 100% | 100% | 100% | 0% | 19% | 18% | 16% | 0% |
| jobbguru.se | 219 | 100% | 1% | 100% | 100% | 100% | 0% | 19% | 18% | 16% | 0% |
| jobmedic | 500 | 100% | 100% | 100% | 100% | 100% | 0% | 95% | 90% | 81% | 0% |
| jobmedic.co.uk | 500 | 100% | 100% | 100% | 100% | 100% | 0% | 95% | 91% | 77% | 0% |
| jobbland | 500 | 100% | 100% | 100% | 100% | 100% | 0% | 92% | 86% | 93% | 0% |
| jobbland.se | 500 | 100% | 0% | 0% | 100% | 100% | 40% | 39% | 38% | 38% | 0% |
| jobscentral | 500 | 100% | 100% | 100% | 100% | 0% | 0% | 94% | 89% | 96% | 0% |
| brightminds | 1 | 100% | 100% | 100% | 100% | 0% | 0% | 100% | 100% | 100% | 0% |
| eures | 3,500 | 98% | 0% | 100% | 97% | 100% | 93% | 86% | 71% | 60% | 96% |
| eures-escox | 200 | 100% | 0% | 100% | 76% | 100% | 84% | 42% | 40% | 100% | 86% |

3. **Full text is available for every non-OJA source** (`description` 98–100%), which the lexicon work in Month 3 needs and which OJA lacks.
4. **`organization` is empty in every scraped board (0%)** and filled only in `eures` (96% of dated postings). Employer-level analysis is therefore possible only with `eures`.
5. **`location_code` is empty in `jobscentral` and `brightminds`**, which is why the trend endpoint returns no rows for them. `nuts1`–`nuts3` are mostly empty outside `eures` (0–11%, `jobbland.se` 40%).
6. **`experience_level` and `type` depend on the source.** `jobbland.se` has neither; `experience_level` is nearly empty in `kariera.fr` (2%), `jobs.de` (2%) and `eures` (0%); `lesjeudis.com` has 44%.
7. **Occupation, skill and sector tags are patchy.** `kariera.gr` carries ESCO occupations for 58% of postings, skills for 57% and sectors for 52%; `jobbguru`/`jobbguru.se` only 16–19%; `jobbland.se` 38–39%. Any occupation-based analysis on these sources has to cope with unlabelled postings.
8. **`jobbguru` and `jobbguru.se` look like the same postings** (same sampled dates and the same fill rates), but `experience_level` is 100% in one and 1% in the other, so they are not exact copies.
9. **`eures-escox` returns the same keys as `eures`, with a different fill pattern.** `skills` is 100% for dated and undated postings alike (against 60% and 13% in `eures`). For occupations and sectors the order is reversed: undated postings are better tagged than dated ones (`occupations` 98% versus 42%, `sectors` 89% versus 40%). `organization` is 86% (dated) and 66% (undated), `nuts1` 84% and 75%, `location` 76% and 51%. The sample is small (92 dated, 108 undated), so these figures are good to roughly ten percentage points; 54% of the sampled postings were undated against 42% in the population. In this sample the id predicts the date of a dated posting with a median error of 14 days (75th percentile 54, 90th 89, maximum 119; 1 of 5 neighbouring page pairs backwards), the same coarse picture as for `eures`.
10. **Access note.** For `eures-escox`, requests of 100 rows (also with a one-day date window) were dropped with "Remote end closed connection without response", while requests of 1, 5 and 25 rows succeeded; each took 65 to 71 seconds, and two of the eight 25-row pages needed a retry after a 504. The cause is not known; the pattern suggests a per-request cost of about a minute plus a time limit in front of the server. Large pulls from this source should use small pages and expect about a minute per request.

11. **Occupation, sector and skill tags stop in December 2025 in `kariera.gr` and in October 2025 in `jobbland.se`; `lesjeudis.com` keeps them into March 2026** (`diagnostics/33`, `diagnostics/34`, `docs/stability_check.md`, `docs/tag_fill_by_month.md`). In `kariera.gr`, a date-filtered middle page per month shows occupations in 85–99%, sectors in 78–96% and skills in 84–100% of postings from August 2024 to November 2025, then 0% in all three for each month from December 2025 to April 2026 (100 postings sampled per month). The unfiltered result set agrees: pages with ids up to 5,288,150 (upload dates to 1 July 2025) are tagged (occupations 88–98%, sectors 80–89%, skills 92–100%), pages from id 5,355,774 on (2026 dates) are at 0%. So the 58%, 52% and 57% quoted in the table above for `kariera.gr` average a tagged period and an untagged one. In `jobbland.se` the 600 postings sampled in each month from January to May 2026 carry no occupation, sector or skill tag either (the 38–39% found earlier presumably came from earlier postings). `lesjeudis.com` is tagged in 2024 (94–99%). A population-level check (`diagnostics/41`, `42`; `docs/tag_outage_by_month.md`) with the server's skills-by-location endpoint (`GET /exploratory-analytics/jobs/skills-by-location`, which returns the most frequent skills per country from the whole population within seconds; that `Freq` counts postings is an inference from the stable shares below, not documented) gives, for the share of postings carrying the ESCO skill "communication": in `kariera.gr` 10.6% to 13.7% a month from August 2024 to September 2025 (October and November 2025 have only 61 and 37 postings), 0.4% in December 2025 (12 of 3,308), 0.0% in January and February 2026 (3 and 1 postings) and 0 from March 2026; in `jobbland.se` 5.2% to 9.3% from August 2024 to September 2025 (June 2025, 132 postings, shows 0), 0 of 1,520 postings in October 2025 and at most 19 postings with that skill in any month of 2026 (19 of 55,457 in February), so the tags stop there in October 2025, not in 2026; in `lesjeudis.com` 5.4% to 7.6% in 2024 and 2025, 3.4% and 2.0% in December 2025 and January 2026 (386 and 250 postings), 4.4% in February and 5.2% in March 2026, so it stays tagged (the tags continue, but thinner: the share of postings carrying the single most frequent skill falls from 10.9-17.1% before December 2025 to 5.6-8.3% from December 2025 to March 2026, which may mean that fewer skills pass the similarity threshold, a hypothesis that nothing here tests, so tag-based comparisons that cross December 2025 are unsafe in this source as well); `jobs.de` (2.2% to 5.0%) and `kariera.fr` (1.5% to 3.4%) are tagged in every month they cover. The outage is therefore specific to `kariera.gr` and `jobbland.se` and is not a general stop of the tagging. The cause is not known and should be put to the Skillab team (Section 11 item 10 (i) and (j)). The results of `diagnostics/34` also show `upload_date` ranges inside single 100-row pages of 2026 (for example 1 February to 7 April 2026), so for the newest ids the id order no longer follows the date order.

Limits: five pages per source (200 postings for `eures-escox`) describe fill rates roughly, to within a few to ten percentage points, not exactly; only the first element of list fields was inspected, and value distributions (for example the categories of `type`) were not tabulated.

### 9.8 Study period decision: 2024 to date

**Decision (supervisor, 13 October 2026).** No source other than OJA holds data for 2019, 2020 or earlier, and OJA is not to be used. The case study therefore covers **2024 to date**, and the thesis report must state the data-availability findings and that the study period follows from them.

**Evidence behind the decision** (details in the sections cited):

1. All 16 posting sources and all counts were checked with three independent methods: filtered counts (9.3), the server-side trend endpoint (9.6, agreement exact or within a few dozen postings for 13 of 16 sources) and a complete source list (16 sources, `kariera.group` and other guessed names return nothing). The empty years are in the data, not a querying error.
2. The only non-OJA postings dated 2019–2020 are 90 (`jobbland.se`) and 9 (`jobbland`). Before 2024 the other sources hold about 1,550 (`jobbland.se`), about 1,114 (`jobbland`) and about 1,160 across `eures` and `eures-escox` (580 and 577).
3. OJA has the only sizeable 2019–2023 data (407,545 postings in 2019–2020, 395,077 in 2021–2023, plus 123,200 earlier), but its records carry no title, description or organization, its occupation coverage changes (ten occupation codes exist only in 2024 and cause the January 2024 step), and it ends in March 2025 (9.4a–9.4d).
4. The scraped boards start in August 2024 (`kariera.gr`, `jobs.de`, `kariera.fr`, `lesjeudis`, `lesjeudis.com`, `jobmedic`, `jobmedic.co.uk`, `jobbguru`, `jobbguru.se`; `jobbland.se` effectively in May 2024). Most stop within months: `jobbguru` September 2024, `lesjeudis`, `jobmedic` and `jobbland` November–December 2024, `kariera.fr` March 2025, `jobs.de` April 2025. Only `lesjeudis.com` (to March 2026), `kariera.gr` (to April 2026) and `jobbland.se` (to September 2026, last month incomplete) run on. `jobscentral` and `brightminds` are one-year snapshots of 2024 (9.3, 9.6).
5. The EURES family has about 100 postings a month until August 2025, then rises steeply and appears to have been loaded in bulk: 99,039 (January 2026) and 260,792 (February 2026) for `eures`, nothing dated later. Its `upload_date` is an insertion date (supervisor, 11 item 10). 806,462 of its 2,099,586 postings have no `upload_date` at all and fall outside every date-based count (9.6 item 8).
6. Monthly volumes in every source follow data collection, not the labour market (9.6 item 6). Counts cannot be compared over time. Shares and composition within a source are less exposed to this, but not immune: if collection changes which postings are captured (as in OJA, where new occupation codes appeared in January 2024), shares shift too. Section 9.8 below reports the first stability checks; the volume jumps themselves (for example `jobbland.se`, 53,139 in January 2025 and 132 in June 2025) have not been tested.

**What this means for the study (to be reflected in the thesis).**

- January to April 2024 is effectively uncovered outside OJA, so the usable window starts in August 2024 for most sources.
- The reference period before the April 2025 tariff measures is about eight months long (August 2024 to March 2025) and exists only in `kariera.gr` (Greece), `lesjeudis.com` (France), `jobbland.se` (Sweden), and, ending earlier, `kariera.fr`, `jobs.de` and `jobbland`. Country coverage differs by source and the sources cannot be pooled without a calibration.
- The 2022 energy-crisis and 2023 Chips Act validation windows from the brief cannot be tested.
- Analyses should use shares and composition within a source and country, never raw counts, and only after a stability check: compare the composition (occupation group, sector) of high-volume and low-volume months within the same source. Where composition moves with volume, the source cannot support a trend in shares either. The undated EURES postings should be treated as a separate cross-sectional group.

**Stability check around the testable events (`diagnostics/33`, `diagnostics/34`; 14 October 2026).** From each calendar month, six evenly spaced pages (600 postings) were compared before and after the event with the Jensen-Shannon divergence (0 identical, 1 disjoint), against the largest divergence between adjacent months on the same side ("drift") and a permutation null. Results (`docs/stability_check.md`):

| Case | Variables that could be tested | Result |
|---|---|---|
| EU tariffs on Chinese EVs, `kariera.gr` (Sep-Dec 2024) | occupation, sector, experience level, type, tags, description length | Occupation (0.039 against drift 0.055), sector (0.036 against 0.058), experience level and description length are within normal drift. The share of postings with an occupation tag rises from 88-90% to 94% and the "no occupation" share falls from 11.3% to 6.3%, so tag-based shares move partly through tag coverage (flagged "beyond drift" for the tag-present variables and for `type`, at divergences of 0.003-0.019). **Title words: 0.190 against drift 0.104, beyond drift.** |
| EU tariffs on Chinese EVs, `lesjeudis.com` (Aug 2024-Jan 2025) | same | Within normal drift for occupation (0.028 against 0.084), sector, type, tags and description length; experience level 0.013 against 0.012, marginally beyond. **Title words: 0.186 against drift 0.105, beyond drift.** |
| EU tariffs on Chinese EVs, `jobs.de` (Aug 2024-Jan 2025) | same | The mix is volatile: adjacent-month divergences are 0.204 (occupation), 0.184 (sector) and 0.205 (title words), so most readings are "within drift" only because the drift is large. **Title words 0.424 against 0.205: beyond drift.** The share of first sector "postal activities under universal service obligation" falls from 11.6% to 1.3%, "removal services" appears (0% to 2.1%), the "no occupation" share rises from 5.4% to 13.6% and occupation-tag coverage falls from 96% to 85% over the six months. |
| Iran war and oil shock, `kariera.gr` (Jan-Apr 2026) | experience level, type, description length only | Occupation, sector and skill tags are empty in every sampled posting (9.7 item 11), so those variables cannot be tested. The three variables that vary are within normal drift, and so are the title words (0.063 against drift 0.123). |
| Iran war and oil shock, `jobbland.se` (Jan-May 2026) | description length only | Everything else is empty or constant (no tags, no experience level, no type); description length is within normal drift, and so are the title words (0.021 against drift 0.052). |

Reading: (i) month-to-month drift is large compared with a random split (for example 0.055 against 0.016 for the occupation mix in `kariera.gr`), so composition changes from month to month even when volume is steady; an event effect smaller than that drift cannot be told apart from it. (ii) For the 2024 event the two screens disagree. The tag-based variables are within normal drift in Greece and France, but the title-word distribution moves clearly more than the month-to-month drift in both (0.190 against 0.104 in Greece; 0.186 against 0.105 in France; the null 95th percentile is 0.029 and 0.018). Between September-October and November-December 2024 the vocabulary of the postings changed, and the sector shares show where (in Greece restaurant activities and hotels rise from 0.9% to 3.2% and from 0.7% to 2.8%; in France hotels fall from 2.1% to 0.4%). Collection and seasonality cannot be separated here, because the boards start in August 2024 and there is no earlier year. Overall shares of postings are therefore not safe to compare across this event. (iii) For the 2026 event no structured field is available in either source, but the title-word distribution is within normal drift in both (Greece 0.063 against 0.123; Sweden 0.021 against 0.052), so a text-based measure passes this screen. This is a weaker test than a tag-based one (titles are short, 300 words were compared, and 'drift' is only two to three adjacent pairs). (iv) The boards start in August 2024, so no seasonal control exists for any event except by comparison with the same months of the following year (March-April 2025 against March-April 2026 in `kariera.gr`, whose 2026 tags are missing). (v) Design consequence (the author's proposal, not part of the brief): instead of the share of event-relevant postings among all postings, compare an exposed group of postings (defined by the Month 3 lexicon, for example automotive and battery vocabulary) with a control group of postings in unexposed fields, from the same source and the same months, before and after the event. A shift in the overall mix, from season or collection, moves both groups and largely cancels. This needs a lexicon-defined exposed group large enough per window; its size has not been measured. (vi) A reading of "within normal drift" is only as strict as the drift is small. In `jobs.de` adjacent months already differ by 0.2, and in `kariera.gr` the title words differ by about 0.10 to 0.12 between adjacent months, so a composition change of that size would pass the screen unnoticed. A pass means no evidence of an unusual shift, not evidence of stability; this applies to the oil-shock result as well. Script 33 now marks such readings as weak when the drift exceeds 0.10 (a rule of thumb, not a tested threshold).

**Draft thesis text (Data and limitations).**

> *Data availability and study period.* The research design originally assumed a pre-shock reference window of 2019–2020 and monthly data up to 2026. An audit of all sixteen job-posting sources in the Skillab Tracker showed that this window cannot be built from the sources that may be used. Only one source, the Eurostat Online Job Advertisement (OJA) collection, holds postings from 2019–2020 (407,545) and earlier (123,200). Its records contain no title, description or employer, its occupation coverage changes during the series (ten occupation codes appear only in 2024, producing a break in January 2024), and it ends in March 2025; following the advice of the project supervisor it is not used. Every other source starts later. The scraped job boards begin in August 2024, and the EURES sources hold about 1,160 postings before 2025, then rise sharply in 2025 and early 2026. Their dates, moreover, are not publication dates: for the EURES sources `upload_date` is the insertion date, and 806,462 of their 2,099,586 postings carry no date at all. Monthly posting volumes in each source follow data collection and not labour demand, so counts are not comparable over time, and within-source shares and composition can be compared only where they prove stable when collection volume changes. The case study therefore covers the period from 2024 to date, with a reference period before the April 2025 tariff measures of about eight months, available for Greece, France and Sweden. Occupation, sector and skill tags are missing in the 2026 postings of the boards that cover the most recent events, so analyses of those events rely on the title and description text. Results are interpreted within, not across, sources, and this limitation is the reason the study does not test the earlier validation episodes (the 2022 energy crisis and the 2023 Chips Act).

### 9.9 Candidate events from 2024 onwards and what the data can support

Events supplied on 13 October 2026 (dates and descriptions as supplied; the 2026 items were not independently verified), plus two events added at the author's initiative: the US "Liberation Day" tariffs of 2 April 2025 (announced 2 April; an additional 20% on EU imports, 10% baseline from 5 April) and the oil-price shock after the US-Israeli strikes on Iran of 28 February 2026 (Brent $71.32 at the 27 February close, peak $138 on 7 April, conditional ceasefire on 8 April; prices from press reports). The test applied is whether a source has stable monthly volume on both sides of the event. Volume in the scraped boards follows collection runs more than the labour market, and a volume break at the event date cannot be told apart from the event. Monthly counts come from `diagnostics/32` (`docs/event_window_counts.md`).

Dated postings per calendar month:

| Month | `kariera.gr` (GR) | `lesjeudis.com` (FR) | `jobbland.se` (SE) | `jobs.de` (DE) | `kariera.fr` (FR) |
|---|---:|---:|---:|---:|---:|
| 2024-08 | 2,738 | 5,660 | 4,184 | 3,427 | 3,000 |
| 2024-09 | 5,629 | 6,649 | 10,034 | 5,632 | 27,099 |
| 2024-10 | 5,480 | 4,935 | 48,018 | 8,175 | 32,892 |
| 2024-11 | 5,593 | 3,986 | 50,097 | 6,417 | 7,043 |
| 2024-12 | 4,866 | 3,511 | 47,151 | 4,029 | 4,941 |
| 2025-01 | 7,065 | 4,191 | 53,139 | 1,690 | 6,054 |
| 2025-02 | 3,174 | 1,548 | 23,017 | 2,572 | 4,916 |
| 2025-03 | 2,884 | 450 | 10,959 | 1,691 | 523 |
| 2025-04 | 1,458 | 581 | 4,139 | 597 | 0 |
| 2025-05 | 4,219 | 2,336 | 6,210 | 0 | 0 |
| 2025-06 | 4,678 | 3,887 | 132 | 0 | 0 |
| 2025-07 | 4,097 | 800 | 460 | 0 | 0 |
| 2025-08 | 3,510 | 3,383 | 3,066 | 0 | 0 |
| 2025-09 | 1,703 | 3,279 | 3,968 | 0 | 0 |
| 2025-10 | 61 | 1,476 | 1,520 | 0 | 0 |
| 2025-11 | 37 | 738 | 3,618 | 0 | 0 |
| 2025-12 | 3,308 | 386 | 28,639 | 0 | 0 |
| 2026-01 | 7,112 | 250 | 48,511 | 0 | 0 |
| 2026-02 | 6,542 | 6,561 | 55,457 | 0 | 0 |
| 2026-03 | 6,953 | 768 | 62,392 | 0 | 0 |
| 2026-04 | 6,659 | 0 | 47,721 | 0 | 0 |
| 2026-05 | 0 | 0 | 53,794 | 0 | 0 |
| 2026-06 | 0 | 0 | 46,127 | 0 | 0 |
| 2026-07 | 0 | 0 | 31,166 | 0 | 0 |
| 2026-08 | 0 | 0 | 40,875 | 0 | 0 |
| 2026-09 | 0 | 0 | 595 | 0 | 0 |
| 2026-10 | 0 | 0 | 0 | 0 | 0 |

`kariera.gr` is stable at 5,000 to 5,600 a month from September to December 2024 and at 6,500 to 7,100 from January to April 2026, with a collection gap in between (61 and 37 postings in October and November 2025) and a 2:1 swing in early 2025. `jobbland.se` runs in two regimes: about 48,000 to 62,000 a month from October 2024 to January 2025 and from January to June 2026, and 130 to 10,000 in between; it then falls to 31,166 (July), 40,875 (August) and 595 (September 2026). `lesjeudis.com` declines through late 2024, is erratic in 2025 and has a one-month spike in February 2026 (6,561). `kariera.fr` (France, 74,975 postings in 2024) shows a collection break exactly at the first EV event: 27,099 and 32,892 in September and October 2024, then 7,043 in November, so it cannot serve that event. `jobs.de` (Germany) rises from 3,427 (August) to 8,175 (October 2024) and falls to 6,417, 4,029 and 1,690 (November to January), a trend through the event rather than a break; its composition is unstable (9.8). Both stop in April and March 2025. The EURES family (about 100 a month until August 2025, then a bulk load of 99,040 in January and 260,801 in February 2026, nothing dated later; insertion dates) does not offer a stable window around any event below.

| Event | Date | What the data show | Assessment |
|---|---|---|---|
| EU Critical Raw Materials Act in force | 23 May 2024 | The four other boards have nothing before August 2024. `jobbland.se` has 191, 246, 292 and 410 postings in January to April and 2,116 in May 2024 | Chosen as a primary event (author, 16 October 2026) but at risk: the only pre-period is `jobbland.se` (about 1,100 postings in January to April 2024) and its volume rises fivefold in the event month (collection ramp, 9.3); testable only if the sector windows prove large enough, to be measured first in Month 3 |
| EU tariffs on Chinese electric vehicles | 30 Oct 2024 | `kariera.gr` is stable from September to December 2024 (4,866 to 5,629 a month). `lesjeudis.com` has about three pre-months (August to October) and a downward trend (6,649 to 3,511). `jobbland.se` changes regime in October 2024 (10,034 to 48,018), so it has no pre-period. | **Not testable as an overall-share comparison in any of the three countries; an exposed-versus-control contrast is possible only if the exposed group proves large enough (not yet measured)** (9.8). Greece has no car industry, so it is a weak test of this event; Germany (`jobs.de`, the most exposed country) has a window, but its composition is unstable (title words 0.424 against drift 0.205; one sector falls from 11.6% to 1.3% of postings); France (`lesjeudis.com`) looks like an IT board (consultancy and programming dominate its sector tags). Pre-period about two months (France three, with a trend); occupation and sector shares are within normal drift, but the title vocabulary shifts beyond drift between September-October and November-December 2024 and no seasonal control exists |
| US "Liberation Day" tariffs | 2 Apr 2025 | `kariera.gr` falls from 7,065 (January) to 3,174 and 2,884, hits 1,458 in April, then recovers to 4,219 to 4,678. `lesjeudis.com` runs 450, 581, 2,336, 3,887, 800. `jobbland.se` falls from 53,139 to 132. `kariera.fr` and `jobs.de` end in March and April. | **Doubtful**: volume moves by a factor of two or more within the window in every source; at most Greece, with April excluded and a stability check |
| China rare-earth export controls | 9 Oct and 8 Nov 2025 | `kariera.gr` 61 and 37 postings; `jobbland.se` 1,520 and 3,618; `lesjeudis.com` 1,476 and 738. All sources are in a collection trough. | Not testable |
| EU CBAM definitive phase | 1 Jan 2026 | `kariera.gr` outage in October and November, 3,308 in December; `jobbland.se` ramps from 3,618 to 28,639 to 48,511; `lesjeudis.com` declines to 250; the EURES bulk load starts in January. Every source is in transition at the event date. | Not testable (revised from "feasible" in the first version of this section) |
| Iran war and oil-price shock | 28 Feb 2026 | `kariera.gr`: 7,112, 6,542 before and 6,953, 6,659 after (April is its last month). `jobbland.se`: 48,511 and 55,457 before, 62,392, 47,721, 53,794 and 46,127 after (March to June), then 31,166 and 40,875 in July and August. `lesjeudis.com`: 6,561 in February, 768 in March and 0 afterwards. | **Testable in Greece and Sweden on text only**; two months before, two (Greece) or four to six (Sweden) after; the peak of 7 April is inside both. Occupation, sector and skill tags are missing in both sources in the event period (`kariera.gr` from December 2025, `jobbland.se` from October 2025; 9.7 item 11), so the measure must come from titles and descriptions; the title-word composition is within normal drift across the event in both (9.8) |
| NATO Ankara summit, defence spending | 7 Jul 2026 | `jobbland.se` only: 46,127 in June, then 31,166 in July and 40,875 in August, 11% and 32% below June's 46,127, the lowest month of March to June, then 595 in September | Doubtful: Sweden only, two post-months, and the drop cannot be told apart from a change in collection |
| EU 21st sanctions package on Russia | 23 Jul 2026 | As above; the NATO date is 16 days earlier, so the two cannot be separated | Doubtful, as above; at most one combined July 2026 episode in Sweden |
| EU public procurement proposal, European preference | 9 Sep 2026 | `jobbland.se` September 2026 holds 595 (partial month) and October 0 | Not testable |
| EU Steel and Metals Action Plan | 19 Mar 2025 | `kariera.gr`: 3,174, 2,884 before (Feb, Mar) and 1,458, 4,219 after; `lesjeudis.com`: 1,548, 450 then 581, 2,336; `jobbland.se` ramps down from 53,139 to 10,959 and 4,139; `jobs.de` ends in April | Doubtful: the event sits in the same collection decline as the US tariffs; three to six pre-months exist in Greece and France only; usable as a same-sector (metals, manufacturing) skills comparison with pooled windows, not as a share comparison |
| EU customs-duties and tariff-quota regulation for certain US imports (with the EU-US deal, 27 Jul 2025) | proposed 28 Aug 2025, adopted Jun 2026 | `kariera.gr`: 4,097 (Jul) and 3,510 (Aug), 1,703 (Sep) then the October-November outage; `lesjeudis.com`: 800 (Jul) then 3,383; `jobbland.se`: 460 (Jul), 3,066, 3,968 | Doubtful: volume swings by 4 to 8 times around the dates in two sources, and the June 2026 adoption has no post-window in Greece or France; treated as one event (supervisor, 13 Oct) |
| EU 19th sanctions package on Russia | 23 Oct 2025 | `kariera.gr` 61 and 37 postings in Oct-Nov (outage), 3,308 in Dec; `jobbland.se` 1,520, 3,618, 28,639; `lesjeudis.com` 1,476, 738 | Not testable in Oct-Nov 2025: every source is in a trough or ramp; a window of December 2025 onwards has no pre-period |
| EU AccelerateEU strategy | 22 Apr 2026 | `kariera.gr` 6,953 (Mar), 6,659 (Apr) then 0; `jobbland.se` 62,392, 47,721 before, 53,794, 46,127 after; `lesjeudis.com` ends in March | Testable in Sweden on text only (two to four pre-months from January 2026, four post-months to August); no tags after October 2025, so a validated text classifier is needed (supervisor answer (a)) |
| EU trade restrictions on Russia | 15 Mar 2022 | No source has data before 2024 | Outside the data window; context only |


**Primary events chosen by the author (16 October 2026).** The EU Critical Raw Materials Act (23 May 2024, critical materials), the Steel and Metals Action Plan (19 Mar 2025, reshoring) and AccelerateEU (22 Apr 2026, energy security). The criterion is policy relevance to a channel, with the same-sector skills and description comparison as the main test (supervisor, 16 October). Limits that the table above documents and the analysis has to carry: the Act has a pre-period only in `jobbland.se` (191, 246, 292 and 410 postings in January to April 2024 against 2,116 in May, a collection ramp), so its pre-window rests on about 1,100 postings before any sector split and a sector-level result may not be estimable; the Action Plan lies in a collection decline in every source; AccelerateEU is Sweden-only and tag-free, so it needs the validated text classifier. Defence, trade compliance and the sanctions and US-tariff events are not primary; the thesis can therefore say little about those channels. The first step of Month 3 is to measure the number of postings per sector-month for each primary event and to drop or downgrade an event whose sector windows are too small.

**Tags (decision, 17 October 2026).** The Tracker's skill, occupation and sector tags are used as supplied inside the tagged period, which covers the Critical Raw Materials Act and the Steel and Metals Action Plan (both windows fall before the outage). No tag production is planned. AccelerateEU lies entirely in the untagged period (from October 2025 in `jobbland.se`, from December 2025 in `kariera.gr`), so it uses one text-based measure applied identically before and after, with sectors from the validated classifier. Running ESCOX locally is deferred; it may be done later for AccelerateEU only, if ESCO skill identifiers are needed for comparison with the other events. No comparison crosses the outage boundary.

Notes: (i) The Iran war and oil-price shock (Greece, Sweden, text-based measures) is the best-supported event; the EU tariffs on Chinese electric vehicles (Greece, France) can be used only with an exposed-versus-control design (9.8). The US tariffs of April 2025 stay in as a doubtful, Greece-only case. The remaining events have no usable window, because the event falls in a collection gap or ramp, or because no source has data after it. (ii) Stable volume is a necessary condition only. A source can have a constant monthly count and a changing composition of postings (a different scraped category or country mix), so any comparison must use shares within a source and country, pooled windows (for example eight weeks before and after) with confidence intervals, and the stability check of Section 9.8, which has not been run. (iii) Results from one source per country are results for that board's postings, not for the national labour market. (iv) The sectors named by the events (automotive and batteries, energy-intensive manufacturing, energy and fuels, transport and chemicals as oil-price-exposed sectors) should drive the Month 3 lexicon and the sector filters. (v) Open questions for the supervisor: whether the scrapers still run, since `kariera.gr` and `lesjeudis.com` have no postings after April and March 2026 and `jobbland.se` falls to 595 in September 2026; whether the April 2025 tariffs and the Iran war can be added to the official event list; why `kariera.gr` and `jobbland.se` lose their tags while `lesjeudis.com` keeps them (9.7 item 11).

### 9.10 Exposure groups from keywords: what the pilot shows and what it does not

Event studies need a group of postings that an event plausibly touches and a control group that it does not. Three attempts to build such groups with the tools available are recorded here (`diagnostics/35`, `36`, `37`, `38`; pilot work, no results are claimed).

1. **API keyword filter (`keywords`, `keywords_logic`).** In `kariera.gr`, March 2026 (6,953 postings), counts return in 0 to 4 seconds. The filter is case-insensitive (`hotel`, `Hotel`, `HOTEL`: 1,748 each), matches whole tokens (`hotels` and `hote`: 0) and combines correctly (`hotel` or `driver` 2,210 = 1,748 + 525 − 63 for `and`); `keywords_logic` accepts only `and` and `or` in lower case. It searches the title for some words (postings found by `saleswomen` and `scientist`, which do not occur in their descriptions) but not as a text search of title and description: `manager`, `consultant`, `nurse` and `assistants` return 0 in a month of about 7,000 postings, and `energy` returns 0 although `energ` returns 12. What is indexed differs by source (item 5), so these counts cannot serve as population counts.
2. **Titles only** (600 sampled postings per month, titles cut to 90 characters). The matched titles are mostly sensible, but the groups are small and describe the type of job, not the industry of the employer: the "automotive" group in `kariera.gr` is car rental and fleet driving, in `jobs.de` it is Kfz workshops and car dealers; the "energy" group in `kariera.gr` is energy-supplier call-centre and sales work.
3. **Title plus the first 400 characters of the description** (`diagnostics/38` then `35`; oil-shock cases only). This adds many false positives: matched postings include "CUSTOMER SERVICE OFFICER", "Accounting Clerk" and "MEDICAL VISITORS" in the Greek manufacturing and transport groups, and "Warehouse worker for a pharmacy's e-pharmacy" and a shop assistant in the Swedish energy group (probably phrases such as "full of energy" or an employer's profile). Keyword matching on running text cannot tell what the job is from what the advertisement mentions.

4. **Wildcards and the other documented filters** (`diagnostics/39`, `40`, `44`). A first probe in `kariera.gr`, March 2026, gave `nurs*` 58 postings and `energ*` 12 (the same as `energ` without an asterisk), but `software*`, `engineer*`, `manager*` and the query of the ESCOPlus 2.0 paper (Section 9.11) 0, as the plain words also did. The supervisor's hypothesis was that the asterisk stands for characters that follow in the same word. A designed test with words of known positive count (`diagnostics/44`) does not support it. In `kariera.gr`, `hotel` and `hotel*` both return 1,748 postings, but `hote*` returns 0 (a wildcard for following characters would return the 1,748), and so do `hotels` and `hotels*`, although the word "hotels" occurs in the text of the postings found by `hotel`. In `jobbland.se`, June 2024, `software` returns 269, `softwares` and `softwares*` 1 each, `softwar*` 25, `softwa*` 0 and `soft*` 43 (`software*` timed out after 105 seconds). Some truncated forms return hits (`nurs*` 58, with nursing, nurse and nurses in the postings, while `nurse`, `nurses`, `nurse*` and `nur*` return 0; `hot*` 64; `energ*` 12), others none (`engineer*`, `enginee*`, `engine*`, `engi*` in a month of about 7,000 postings), and a leading asterisk (`*oftware`, `*otel`, `*urse`) returns 0. No single rule fits these counts on their own; the experiment in item 5 explains most of them (a stemmed index in `kariera.gr` and an asterisk that is ignored), but not `energ*` (12) in `kariera.gr` and `softwar*` (25) and `soft*` (43) in `jobbland.se`. In `jobbland.se` the plain keyword `software` does return hits (7 of 191 postings in January 2024, 209 of 2,116 in May, 269 of 2,879 in June, about 10% from May to July 2024), so the filter works where the word occurs. The API documentation describes `keywords` only as "keywords that must be included", without field or language. The same filter also takes `organization_names` (exact names), `sectors`, `skill_ids` and `occupation_ids`, each with its own and/or logic. The last three depend on the tags (9.7 item 11), and `organization` is empty in every scraped board (9.7 item 4), so exposure groups by employer are possible only in `eures`, which has no stable window (9.9).

5. **Ground-truth experiment on the keyword filter** (`diagnostics/45`; two samples of 100 postings, results in `docs/keyword_index_experiment_*.md`). The documented `ids` filter is combined with `keywords`, so the server states which of the 100 postings match, and this is compared with the text we hold. *`jobbland.se`, June 2024 (first 100 of 2,879 postings).* The filter matches whole words in the title or anywhere in the description, not only at its start (words found only late in the description, such as `good`, `also` and `position`, are found). A word is a whitespace-delimited token with punctuation removed at its ends; an apostrophe splits it (`role's` is found by `role`), but a slash or full stop between letters does not (`extras/actors` and `commercial.there` are not found by `extras` and `commercial`; for `extras` the filter misses 31 of 48 postings). This rule reproduces the server's answer exactly for 22 of 24 sampled words, with one extra posting each for `recording` and `role`. There is no stemming (`commerci` returns 0; `commercial` 26 and `commercials` 7 postings, separately) and no stop-word removal (`where`, `which`, `only`, `here` are found). *`kariera.gr`, March 2026 (first 100 of 6,953 postings).* Common words return 0 although they occur in the sample (`engineer` 0 of 26 postings, `manager` 0 of 17, `business` 0 of 62, `years` 0 of 59, `people` 0 of 41, `from` 0 of 55), while their stems return the postings (`engin` 43, `manag` 63, `busi` 62, `year` 81, `benefit` 57, `consult` 23, `futur` 59, `peopl` 44, `build` 46, `energi` 20, `softwar` 26). `store` finds 33 postings, of which only 23 contain that exact word, and `stores` finds 0 although 31 postings contain it. This is what an index of stemmed words queried with unstemmed words would give, and it explains `nurs*` (58) of the first probe, since `nurs` is the stem of nurse, nurses and nursing. English function words (`from`, `over`) are not found, as if stop words had been removed. A local English stemmer (Snowball) applied to the words of our text reproduces the server's answer exactly (F1 1.00) for 7 of the 11 stem queries (`engin`, `busi`, `year`, `consult`, `futur`, `build`, `softwar`) and for `store`, `lead`, `analyst`, `drive` and `equal`, and it predicts the 0 results for the plain words above; for `manag`, `peopl`, `energi` and `benefit` the server returns 1, 3, 1 and 6 postings more than the stemmer predicts. The server also splits hyphenated words (`senior-lead` is found by `senior`); the remaining differences were not examined. *Asterisk.* In both sources `X*` returns the same postings as `X` when X is a word (`wanted*`, `recording*`, `commercial*`, `store*`, `senior*`, `hotel*`), every truncated form returns 0 (`wante*`, `comm*`, `engi*`, `stor*`, `senio*`), and `want*` does not find postings with "wanted". The asterisk is therefore ignored and is not a wildcard; the hypothesis that it stands for following characters is not supported. *Open.* `other` finds 8 of about 60 postings that contain it in `kariera.gr`. `energ*`, `softwar*` and `soft*` (item 4) are not explained; the `jobbland.se` sample consists mostly of English-language casting advertisements, and Swedish-language postings may be indexed differently, which was not tested. The behaviour resembles a full-text index with a different language configuration for each source, which is an inference and not documented. *Consequence.* Counts from the `keywords` filter depend on the source (stemming, stop words) and on punctuation, so they are neither comparable across sources nor population counts. Word matching for exposure groups should be done on downloaded text with one tokenizer and one stemmer for all sources (the Month 3 lexicon); the filter can be used to pre-select postings if the source's own behaviour is taken into account.

What the pilot does show, and what is robust to the false positives: (i) In `kariera.gr`, hotel, resort and restaurant roles (many for a tour operator) are 22% to 38% of the sampled postings from January to April 2026 (26.7%, 38.2%, 27.0%, 22.3%); pooled, 32.4% before and 24.7% after 28 February. This is consistent with seasonal recruiting for the summer, and it dominates any share computed on that source. (ii) The health and education control group is about 1% of Greek postings (1.3% before, 0.5% after), so it cannot be a control in Greece. (iii) In `jobbland.se` the health and education group rises from 17.5% (January) to 24.8% (May 2026) while the other groups are roughly flat; many of these are municipal summer-substitute posts, so this is also a seasonal drift. Overall shares are therefore not comparable across the event without a seasonal reference, and none exists for 2026 beyond the same months of 2025 (for `kariera.gr` March to April 2025: 2,884 and 1,458 postings, tags present).

Consequence: exposure has to be defined by a classifier that has been validated against hand-labelled postings (for example classification of titles and opening text into industries by a language model, checked on a labelled sample), or by the structured tags, which are missing in the 2026 postings of the two boards that cover the most recent events (Section 9.7 item 11). Either choice is a methodological step that goes beyond the data audit and should be agreed with the supervisor.

### 9.11 Other API endpoints, country codes and the ESCOPlus 2.0 paper

Endpoints of the analytics families, as documented and as probed (`diagnostics/41`, `43`; none of the results below is a claim about a mechanism the documentation does not give):

| Endpoint | Returns | Date filter | Use here |
|---|---|---|---|
| `GET /trend-analytics/jobs/skills-by-location` | job counts per source, country and month (despite the name); optional `occupation_id` | yes | Population counts per month (9.6). Monthly counts of one ESCO occupation are possible but tag-dependent and not yet used |
| `GET /exploratory-analytics/jobs/skills-by-location` | most frequent (country, skill) pairs; fields `location_code`, `Var1` (ESCO skill URI), `label`, `Freq`; sorted by `Freq`, `limit` keeps the top N (100 and 1,000 both honoured, 1 to 11 seconds) | yes | Tag-outage check (9.7 item 11); monthly skill shares in tagged months |
| `GET /descriptive-analytics/jobs/locations` | postings per location code (fields `Var1`, `Freq`) | no | Country table below |
| `GET /clustering-analytics/jobs` | skill clusters from co-occurrence (`limit`, `k`, `source`) | no | Not used: method undocumented, no date filter, built on the tags |
| `POST /jobs` filters | `keywords`, `ids`, `skill_ids`, `occupation_ids`, `organization_names`, `sectors`, `location_code`, `sources`, `min_upload_date`, `max_upload_date` | yes | 9.10 |

Country codes follow EU practice: Greece is `EL` and the United Kingdom `UK`, so a filter on `GR` or `GB` returns nothing. Postings with a location code, all months (`diagnostics/43`): 5,519,045 in 32 codes, led by DE 1,362,950, FR 1,064,855, SE 893,400, NL 469,833, UK 376,926, BE 336,967, AT 268,201, IT 146,039, PL 102,572 and EL 91,670. By source: `OJA` 2,371,346; `eures` 560,175 (DE 53%); `eures-escox` 1,539,252 (DE 26%, FR 24%, NL 18%, BE 16%); `jobbland.se` 694,838 (all SE); `jobbland` 68,095 (SE); `kariera.gr` 87,766 (EL); `kariera.fr` 86,468 (FR); `lesjeudis.com` 55,375 and `lesjeudis` 18,404 (FR); `jobs.de` 34,230 (DE); `jobmedic.co.uk` 1,448 and `jobmedic` 1,010 (UK); `jobbguru` and `jobbguru.se` 319 each (SE); `brightminds` and `jobscentral` 0 (no location code). Two consequences: Greece is `kariera.gr` (87,766 of the 91,670 Greek postings, 96%; at most 3,904 elsewhere, part of them in `OJA`), and Sweden is mostly `jobbland.se` (78% of Swedish postings). The country counts per source are exact for the whole population and settle Section 11 item 8.

The ESCOPlus 2.0 paper (Kavargyris, Mittas and Angelis, developed in SKILLAB) describes a pipeline that extracts ESCO skills and occupations from the title and description of each posting with the ESCOX tool (translation of non-English text, cosine similarity against ESCO with a threshold of 0.5, on average 5.14 occupations per posting), validated on 200 postings annotated by one author (TF-IDF F1 0.749, no inter-rater agreement). Its corpus is 54,000 software postings from January 2024 to December 2025 from `kariera.gr`, LesJeudis, Jobs.de, karieragroup and Jobbland. For this study: (i) it explains what the tags probably are (that the Tracker's tags on these boards are ESCOX output is my inference, not stated in the paper), and that occupation tags are multi-valued; (ii) its date range does not match ours for four of the boards (August 2024, Section 9.3), and only `jobbland.se` reaches back to January 2024; (iii) its skill intensity, the share of postings of occupation j that mention skill s (Spada et al.), is a candidate building block for the Month 3 index, which depends on the tags and is not yet decided; (iv) its quantile thresholds with a sensitivity analysis are a model for the thresholds used in the stability check (9.8). The lexicon, pruning and web tool, and all its results (eight software occupations), do not bear on the events.

## 10. Tier 1–4 Fallback Chain — Results

The fallback chain (brief Section 4, Table 3) was implemented as a single integrated function (`assign_data_completeness_tier.py`) combining:
- **Tier 1 "Full":** direct `skills`.
- **Tier 2 "Inferred":** ESCO occupation lookup (`occupation_skill_lookup.py`, using the official `occupationSkillRelations_en.csv`, 126,051 rows / 3,039 occupations), reachable either via `occupation_uris` directly (Revelio) or via an exact-substring match of the free-text `occupation` field against ESCO occupation labels (`occupation_text_matcher.py`, validated at 100% precision on a 12-case hand-labelled sample; a TF-IDF fuzzy-matching fallback was also built and validated, found to perform worse than chance — 30% precision — and is disabled by default).
- **Tier 3 "Weak":** an empirical sector + highest-degree prior (`tier3_sector_degree_prior.py`), built only from genuine Tier-1 profiles, bucketed by `(sector, highest_degree)` with a `(sector,)`-only fallback, requiring at least 20 Tier-1 profiles in a bucket before trusting it.
- **Tier 4 "Sparse":** excluded from skill-based analyses; retained for geographic/demographic analysis only.

The brief names the four `data_completeness` labels "full text / skills only / occupation only / sparse" (Section 2 activity list) and "Full / Inferred / Weak / Sparse" (Section 4, Table 3). The pipeline uses the second set, which describes the confidence of the skill information; the correspondence is Full = skills present (Tier 1), Inferred = skills inferred from the occupation (Tier 2, "occupation only"), Weak = sector and degree prior (Tier 3) and Sparse = none of these (Tier 4). The first set, which describes which fields exist, has no separate label because "full text" is a property of the `content` field (95.9% filled) and not a tier.

Applied to the full 7,222-profile working sample:

| Tier | Label | Count | % of sample |
|---|---|---|---|
| 1 | Full | 4,526 | 62.7% |
| 2 | Inferred | 224 | 3.1% |
| 3 | Weak | 0 | 0.0% |
| 4 | Sparse | 2,472 | 34.2% |

(Tier 1's 62.7% matches the aggregate `skills` completeness in Section 3 exactly, confirming the two independent measurements agree. Of Tier 2's 224 profiles, 197 resolved via `occupation_uris` and 27 via the free-text exact-match enhancement.)

**Tier 2 validation (`diagnostics/49_validate_tier2.py`, `docs/tier2_validation.md`, 17 October 2026).** Tier 2 has two links, checked separately.

*The skill sets.* Of the Revelio profiles, 31 have both an ESCO occupation URI and self-reported skills (89 skills in all, every one matched to an ESCO skill; the ESCO table holds all 31 occupations). For each, the ESCO default set of the occupation (essential and optional skills, on average 57) was compared with the profile's own skills, and with the default set of a random other occupation from the same pool (fixed seed).

| Measure | Own occupation | Random other occupation | Difference (95% bootstrap interval) |
|---|---:|---:|---|
| Recall, essential and optional (mean) | 8.9% | 1.5% | +7.5% (-0.0% to +17.5%) |
| Recall, essential only (mean) | 1.1% | 0.0% | |
| Precision (mean) | 0.3% | 0.1% | +0.2% (-0.1% to +0.5%) |
| Recall (median) | 0.0% | 0.0% | |

The own occupation has the higher recall in 5 of 31 profiles (16%); in the other 26 the two are equal (mostly both zero). The result is that **the sample does not show that the inferred skill sets resemble what people in these occupations report**: the mean is higher than for a random occupation, but the interval reaches zero, the median is zero and the gain comes from a handful of profiles. The test is weak in both directions: the profiles list about three skills each (89 in 31 profiles), so recall can only take a few values; 31 is a small number; and profiles that report skills are not the profiles that Tier 2 serves. The ESCO default sets are long and generic (57 skills), and the precision of 0.3% shows that a profile reports almost none of them. Consequence for the design: Tier 2 skills are a conservative imputation without demonstrated accuracy, so results stay separate for Tier 1 and Tier 2 as the brief requires, Tier 2 does not enter any main result, and Tier 2 profiles are used only as a sensitivity check. The event analysis rests on postings (Section 9.9) and does not use Tier 2.

*The free-text link.* Hand labels (one rater, the author) on 100 profile occupation texts: the exact-substring match used in Tier 2 returned a match for 13 texts (13%) and was correct in 12 of the 12 labelled (100%; Wilson 95% interval 76% to 100%; one row was left unlabelled); the fuzzy TF-IDF fallback matched 20 texts and was correct in 6 (30%; 15% to 52%) and is disabled; 67 texts had no match. Tier 2 through free text therefore reaches few profiles but with a high labelled precision, and the labelled sample is small.

**Tier 3 finding: structurally near-unreachable at this sample size, not a bug.** Tier 3 produced zero assignments. Investigation (not merely accepted at face value) found:
- `sectors` is itself concentrated almost entirely in Revelio (91.6% completeness) vs. 1.2% on LinkedIn and 0.0% on every STACK source — the same concentration pattern as `occupation_uris` (Finding 1) and now folded into Finding 3.
- Because Revelio's `skills` completeness is only 12.4% (Finding 3), the population with **both** `sectors` and genuine Tier-1 `skills` — the only data `tier3_sector_degree_prior.py` can learn from — is just 31 profiles sample-wide, spread across 48 distinct (fine-grained NACE-class-level) sector categories. The single largest resulting bucket held 3 profiles, far short of the `MIN_BUCKET_SIZE = 20` threshold.
- This is not a sampling artefact fixable by pulling more data at the current rate: scaling the Tier-1-and-sectors overlap population from 31 to the ~208 needed for the largest bucket to clear 20 would require on the order of 48,000+ total profiles, proportionally representative of Revelio — far beyond the brief's Week 1 target (5,000–10,000) and dependent on the one source already flagged (Week 1–2) as the slowest and least reliable to pull from in bulk.
- `MIN_BUCKET_SIZE = 20` was kept as-is rather than lowered to force Tier 3 to produce output: building an "empirical" prior from 3–6 data points would defeat the purpose of guarding against low-confidence inference that motivated the threshold in the first place.

**Conclusion:** the fallback chain functions in practice as Tier 1 → Tier 2 → Tier 4 on this sample, with Tier 3 implemented and validated (synthetic smoke tests covering all four tiers and both Tier 2 paths pass against the real ESCO table) but essentially unused given current field concentration. This should be stated plainly as a scope limitation in the methods section, alongside Finding 3's broader point that Revelio trades skill-text depth for structured fields.

## 11. Recommended Next Steps

1. **Date-coverage check and baseline - largely complete (Section 9).** Baseline window covered by `OJA` only, and only for eight ISCO codes (Section 9.4d); usable OJA range January 2019 to March 2025; post-March 2025 data exists only in other sources. The 2025/2026 split for `jobs.de`, `kariera.fr` and `jobbland` is resolved by direct closed-window counts (Section 9.3).
2. **OJA regime decision (open).** Run a composition and duplicate check (country, occupation group, sector, duplicate rate) on samples from December 2023 and January 2024 to identify the cause of the 51-fold step, and on 2019 against 2023 to check the earlier decline. Decide whether 2024 to March 2025 can be pooled with 2019-2023. The existing working sample cannot be used for this: its OJA part is entirely 2019 (Section 13.1), so a new, time-stratified OJA sample is needed.
3. **~~Tier 1-4 fallback chain~~ - complete (Section 10).** Tier 3's near-total absence is documented as a structural finding.
4. **Source normalisation.** Merge the four duplicate postings pairs (Section 13.4; `python -m diagnostics.18_postings_breakdowns --merge-aliases` gives merged tables). Still to decide: the STACK profile sources, and whether the larger member of each postings pair is a superset of the smaller at population level (the sample cannot show this). Deduplicate by content, because `id` is not shared across aliases.
5. **~~Occupation-URI augmentation~~ - addressed in Section 10** (27 additional profiles resolved by free-text exact match beyond the 197 from `occupation_uris`).
6. **Geography decision.** Country-level analysis can use `location_code` (about 93% coverage). Regional (NUTS) analysis remains limited to EURES-family postings unless a geocoding step is built from free-text `location`; decide whether regional analysis is needed for the Greece panel.
7. **Career history - checked, negative (Section 8).** Raise with the supervisor: restructure the transition analysis around postings-level aggregate signals, or find a supplementary source.
8. **Breakdown tables - done for the working sample (Section 13).** Population-level country counts by source are now available (Section 9.11, `diagnostics/43`).
9. **Schema documentation - done** (`docs/schema.md`, regenerated by `python -m diagnostics.19_generate_schema_doc`).
10. **Questions for the Skillab team or supervisor.** (a) Is `upload_date` the source board's posting date for scraped boards, and what is it for OJA (publication date or first-detection date)? (b) Does the API expose the underlying OJA source or its stability flag? (c) Are OJA postings de-duplicated across skills and locations? (d) What explains the January 2024 step and the end of data in March 2025? (e) Is `upload_date` for the EURES family an import or publication date on EURES and not the employer's posting date, given that 84% of `eures-escox`'s 2026 postings fall in February 2026 and nothing is dated after that? (f) What coverage is planned after March 2025, since the brief assumes monthly data to 2026? (g) Why do OJA postings have an empty title and no description or organization, and is OJA in Skillab restricted to certain occupations or is it the full Eurostat OJA? (h) Is the `keywords` index built with a different language configuration for each source (stemmed words and stop words in `kariera.gr`, whole words in `jobbland.se`), and how are Swedish-language postings indexed? Our experiments point to this (Section 9.10 item 5); a confirmation would settle it. (i) Why are occupation, sector and skill tags absent from the postings of `kariera.gr` from December 2025 and of `jobbland.se` from October 2025, while `lesjeudis.com` is still tagged in March 2026 (Section 9.7 item 11)? (j) Are the tags produced by ESCOX, and will they be produced for the missing months? (k) The ESCOPlus 2.0 paper reports a corpus of January 2024 to December 2025 from `kariera.gr`, LesJeudis, Jobs.de, karieragroup and Jobbland; in the Tracker four of these boards start in August 2024 and `jobbland.se` in January 2024 (Section 9.3). Which date and which sources did the paper use? (l) How does the `clustering-analytics` endpoint compute its clusters (Section 9.11)? The asterisk question was answered by experiment: a trailing asterisk is ignored (Section 9.10 item 5).

    **Supervisor's answers (October 2026).** (a) `upload_date` does not necessarily correspond to the original posting date; its meaning depends on the source. (b) Do not use Eurostat's OJA source in the analysis. (c) Use the other available sources. (d) The January 2024 change and the March 2025 interruption are due to the data retrieval sources. (e) For the EURES family it is the insertion date. (f) To cover up to 2026, use the remaining sources in the Tracker instead of OJA, after checking their time coverage. (g) The empty fields likely relate to the structure of the data received from that source. The supervisor's overall recommendation is to avoid OJA and rely on the other sources, which hold millions of records and data for 2026.

    **Consequence and open question.** The time-coverage check the supervisor asks for has been done (Sections 9.3 and 9.6): no other source holds data for 2019–2020, the scraped boards begin in August 2024, and the EURES family is concentrated in 2025–2026. With OJA excluded the thesis has no 2019–2020 pre-shock baseline in Skillab. The question to put back was which source the supervisor expects to cover the baseline, or whether the reference period should change.

    **Supervisor's decision (13 October 2026).** Since no other data source exists for 2019, 2020 and earlier, the case study is done from 2024 to date, and the report must state the data-availability findings and that the limitation led to focusing on 2024 onwards. Recorded in Section 9.8.

    **Supervisor's answers to the second set of questions (16 October 2026).** (a) A text-based sector classifier, validated on a hand-labelled sample, is acceptable for 2026 postings. (b) The main test is a same-sector comparison of skills and descriptions; overall sector shares are secondary. (c) The choice of primary events is the author's. (d) The scrapers are running, but the data are loaded in bulk, so volumes follow loads and the coverage end dates may move; analyses must state the data-cut date. (e) The stop of tags in `kariera.gr` and `jobbland.se` is not explained by Skillab. (f) Tags are not produced by ESCOX; a mapping script was promised. (g) The ESCOPlus 2.0 corpus is 54,000 software engineering postings across the EU, 2024 to 2025. (h) The keyword index has no per-source language setting; a collection script was promised. The two scripts then arrived and were read (below). Question (h) above is still open: the experiments of 9.10 show a stemmed index with stop words in `kariera.gr` and an exact-word index in `jobbland.se`, and the collection script has to be read to see whether the difference comes from the text that is stored (for example a processing step on one source) rather than from the index. The meaning of `upload_date` on the scraped boards was answered later the same day (below).

    **The two scripts (read 16 October 2026).** `collection.py` is a client of the same `POST /jobs` endpoint used here: it logs in, posts eight software-engineering phrases as `keywords` with an empty `sources` list, pages through the results with `page` only, fetches the label of each skill and occupation id one request at a time, and saves the postings with `mapped_skills` and `mapped_occupations`. It sets no language option and nothing about the index, so it does not explain the stemming difference between `kariera.gr` and `jobbland.se`; that has to come from how the index is built on the server, and the question to Skillab narrows to that. It also means the ESCOPlus corpus was selected by this keyword filter across all sources, whose matching differs by source (9.10 item 5); whether that affected its recall by source is not known. `mapping.py` does not produce the Tracker's tags either: it reads the skill and occupation ids already present on each posting and adds `non_esco_skills`, the ten most similar entries of an English lexicon (`escoplus_lexicon_not_in_esco.csv`, not supplied) by TF-IDF cosine similarity of word and bigram vectors, threshold 0.15, with the TF-IDF fitted on the batch itself and English stop words. Consequences for this study: the tags' origin remains unexplained; the script handles English text only, so Greek, Swedish and French postings would need translation or a language-specific method; and because the TF-IDF weights depend on the batch, scores are not comparable between runs. It is a reference for the idea of text-based skill extraction, not code to reuse.

    **Skillab team's reply to the three questions (16 October 2026, afternoon).** (a) All sources use one common retrieval mechanism; keywords are searched in the title and description, and a posting is returned if any of the given words or phrases is found. This does not account for the per-source difference measured in 9.10 item 5 (in `kariera.gr` the plain word `engineer` returns no posting of the 100 tested and the stem `engin` returns 43), which is therefore unexplained and stays a documented property of the filter; the analysis does not use the server filter for counting (word matching is done locally with one tokenizer and one stemmer). (b) The team did not say why the tags stop. It advises running the ESCOX skill extractor locally (public repository `esco-skill-extractor`, not yet read or run here) with a similarity threshold below the 0.5 set in the Tracker, and trying several thresholds if no skills are detected. Two consequences: the Tracker does use ESCOX with threshold 0.5, which differs from the earlier answer that the tags are not produced by ESCOX; and the tag outage may mean that no skill passed the 0.5 threshold for the affected postings (a hypothesis, not tested). Any locally extracted skills must be produced with one threshold for all months, tagged and untagged, so that months before and after an event are measured in the same way; Tracker tags at 0.5 must not be mixed with local tags at a lower threshold. (c) `upload_date` on the scraped boards is the date on which the posting was published on the portal. This answers the open question in Section 9.3 in favour of the posting date. It does not remove a selection effect: if each collection run captures the postings still online at the time, months just before a source's first run contain only postings that stayed online, which would explain the ramps (for `jobbland.se` 191, 246, 292 and 410 postings in January to April 2024, 2,116 in May) and the troughs in the gaps between runs. This is an inference from the monthly counts and should be checked by comparing posting dates with first-seen dates if the latter can be obtained. If it holds, the pre-period of the Critical Raw Materials Act holds a survivor-selected set of postings and is not comparable with the post-period. The tool's own defaults are 0.6 for skills and 0.55 for occupations, so the Tracker's 0.5 is a deployment setting; it returns skill and occupation URIs and no sectors, so sector tags are not covered by it and the validated text classifier is needed in any case.
11. **~~Week 4 deliverable~~ - complete** (`week4_data_quality_policy.md`).

## 12. Month 2 Deliverables Status (against the brief)

| Brief requirement | Status |
|---|---|
| Connect to the API; pull postings and profiles | Done (7,222 profiles, 6,723 postings, all sources) |
| Audit field completeness | Done (Sections 3-8); occupation-group tabulation pending |
| Baseline window (2019-2020) and coverage | Done (Section 9); outcome: no usable 2019-2020 baseline outside OJA, which is not to be used. Study period changed to 2024 to date by the supervisor (Section 9.8); reference period before April 2025 about eight months (August 2024 to March 2025) |
| Four-tier fallback chain, tested on 5,000+ profiles | Done (Section 10; applied to 7,222). Tier 2 lookup validated (Section 10): the inferred skill sets are not shown to match own skills (31 profiles); the free-text link has 12 of 12 labelled exact matches |
| Career-history depth | Done: negative (Section 8) |
| Greece panel reliability (Greek profiles sparse?) | Done (Section 6.1): not sparser than comparable profiles, but only 99 forum-based profiles with no occupation, sector or date; the Greece panel rests on postings |
| Data coverage report (by year, country, sector) | Done at population level for postings with a country code (field completeness by country and sector: Section 13.6): by source, year, country and month in `docs/coverage_population.md` (Section 9.6); sector is not available from the aggregate endpoint, so the sector table remains the working-sample one (Section 13.3) |
| Profile completeness report (source, occupation group) | Done (Sections 3-8 and 13.5); the occupation-group view covers only 3.3% of profiles (Revelio) |
| Eurostat labour force statistics (baseline validation, listed as a resource) | Not used: it was to validate a 2019-2020 baseline, which does not exist in Skillab outside OJA, and the study period is 2024 to date (Section 9.8). Country-level validation of the 2024-onwards series is a Month 3 option |
| Schema documentation | Done: `docs/schema.md`, generated from the samples by `19_generate_schema_doc.py` |

## 13. Breakdowns of the Working Sample

Source: `docs/postings_breakdowns.md` (script 18) and `diagnostics/13_profile_completeness_by_occupation_group.py`. All counts describe the 6,723-posting and 7,222-profile working samples.

### 13.1 The sample is not time-representative

| Source | Where the sample falls in time |
|---|---|
| OJA | 468 of 468 dated 2019 |
| eures-escox | 468 of 468 dated 2026 |
| eures | 100 in 2023, 100 in 2024, 100 in 2025, 168 in 2026 |
| every other source | at least 96% dated 2024 |

Consequences: any completeness figure quoted for OJA describes 2019 postings only, and for `eures-escox` 2026 postings only; the aggregate figures in Section 3 mix periods and sources. Composition comparisons across periods (for example December 2023 against January 2024) need a new, time-stratified sample.

### 13.2 Country

`location_code` is populated for 6,254 of 6,723 postings (93.0%) on the raw sample and for 4,535 of 5,004 (90.6%) after the four duplicate source pairs are merged (Section 13.4); the code is missing for all of `jobscentral` and `brightminds`. There are 19 distinct codes. Shares of postings with a code:

| Code | Raw sample | Merged sample |
|---|---|---|
| DE | 17.4% | 24.1% |
| FR | 22.7% | 21.0% |
| SE | 25.2% | 17.4% |
| UK | 15.3% | 10.8% |
| EL | 7.5% | 10.3% |
| CZ | 4.4% | 6.0% |
| AT | 4.2% | 5.8% |
| BG | 1.4% | 2.0% |
| 11 other codes | each 0.5% or less | each 0.7% or less |

Country is almost a function of source. Eleven of the 16 sources carry a single country code, two (`jobscentral`, `brightminds`) carry none, and only three are multi-country: OJA (15 codes, in a 2019-only sample), `eures` (11) and `eures-escox` (5). Greece (EL, 468 postings, 10.3% of the merged sample) comes only from `kariera.gr`; the OJA and EURES samples contain no Greek postings. These shares therefore reflect which boards were sampled and cannot be read as the country distribution of the labour market. A Greece-specific analysis from OJA is not supported by this sample and would need filtered count queries on `location_code` to check.

### 13.3 Sector

`sectors` is populated for 4,785 of 6,723 postings (71.2%) on the raw sample and 3,528 of 5,004 (70.5%) on the merged sample, by the definition used in the script (not null, not empty, not the literal `'empty'`); Section 3 reported 69.1% from the audit notebook, probably under a slightly different definition. Points that matter:

- **OJA has no sector information in the sample** (0 of 468, all 2019 postings). The baseline source cannot support sector analysis through `sectors`. Sector would have to be derived from occupations or descriptions.
- Completeness elsewhere ranges from 18.8% (`jobbguru`, `jobbguru.se`) and 60.5% (`eures`) to 73-93% for the other boards.
- There are 539 distinct sector labels at mixed NACE levels (a section-level label such as "MANUFACTURING" sits beside class-level labels). The labels need harmonising to one level before use. On the merged sample the most frequent are business and other management consultancy (26.8% of postings with sectors), activities of head offices (20.2%), engineering activities and technical consultancy (14.4%) and hospital activities (14.1%). Sector shares largely reflect which specialised boards were sampled (for example the medical board `jobmedic` drives the hospital and nursing labels), so they say little about the labour market as a whole.

### 13.4 Duplicate sources: confirmed

Four pairs showed identical sample sizes, year splits and sector counts. `diagnostics/20_check_duplicate_postings.py` confirms that they hold largely the same postings under two names:

| Pair | Shared by title/organisation/location/date | Shared by description |
|---|---|---|
| jobbguru / jobbguru.se | 318 (99.7%) | 301 (94.4%) |
| jobbland / jobbland.se | 451 (96.4%) | 434 (92.7%) |
| lesjeudis / lesjeudis.com | 436 (93.2%) | 309 (66.0%) |
| jobmedic / jobmedic.co.uk | not matched (see below) | 418 (89.3%) |

(Percentages are of the smaller sample. For `jobmedic` the content key did not match, presumably because titles, organisations or locations are formatted differently, but the descriptions do.) Several points follow:

- **`id` is not shared across the aliases** (no id appears in two sources), so duplicates can be found only by content or description.
- **The overlap measured here is in the sample; the population relation is unconfirmed.** The population sizes of the pairs differ (for example 693,183 and 66,969 postings from 2024 for `jobbland.se` and `jobbland`), so one member may be a superset of the other. Both samples were probably the first 468 records in the same order, which would explain the near-complete overlap.
- **Merging result.** `python -m diagnostics.18_postings_breakdowns --merge-aliases` dropped 319 (`jobbguru.se`), 468 (`jobbland.se`), 468 (`jobmedic.co.uk`) and 464 (`lesjeudis.com`) alias postings as already present in the shorter-named source, and kept 4 (`lesjeudis.com`, dated 2025-2026, which `lesjeudis` does not contain). The sample falls from 6,723 to 5,004 postings. Within the sample the aliases are therefore essentially complete copies.
- **Country shares were inflated.** The SE share fell from 25.2% to 17.4% and the UK share from 15.3% to 10.8%, while DE became the largest (24.1%). Section 13.2 shows both versions.
- **Which member should be canonical?** The alias with the larger population is probably a superset (`jobbland.se`, `lesjeudis.com`, `jobmedic.co.uk`; `jobbguru` and `jobbguru.se` have the same size). The four extra `lesjeudis.com` postings fit this. If so, future pulls should use the larger member. The two small pairs (`jobmedic`, `jobbguru`, about 1,000-1,500 postings each) could be fetched in full to confirm the subset relation.
- **A smaller overlap exists between different boards:** `kariera.fr` shares 9 postings by content (1.9% of its sample) with `lesjeudis` and with `lesjeudis.com`.
- **Repeats inside one source.** By title/organisation/location/date, 0.3-5.6% of each source's sample is repeated (highest `lesjeudis` and `lesjeudis.com`, 5.6%). Description-only repeats are far higher (up to 33% for `lesjeudis`, 25% for `jobs.de`), but many of these are probably the same advertisement text for different locations or jobs, so they are not removed automatically. A deduplication rule (drop exact title/organisation/location/date repeats) must be fixed before any share is computed.

### 13.5 Profiles by occupation group

An ISCO major group can be derived for only 235 of 7,222 profiles (3.3%), all from Revelio. Of these, 31 (13.2%) have skills. By group: managers 10 of 66 (15.2%), professionals 17 of 107 (15.9%), technicians 2 of 30 (6.7%), service and sales 2 of 18 (11.1%), clerical 0 of 4, craft trades 0 of 5, plant and machine operators 0 of 3 and elementary 0 of 2; there are none in groups 0 and 6. Cells below 30 are too small to compare. The view mainly restates Revelio's low skills rate (12.4%) and says little about occupation effects.

### 13.6 Field completeness by country and by sector

`diagnostics/47_completeness_by_country_sector.py` (output `docs/completeness_by_country_sector.md`) gives the completeness of each field within a country and within a sector, which the brief's Step 2 asks for. It uses the working sample without the four alias sources (5,000 of 6,723 postings; countries with fewer than 30 postings are not comparable). All figures describe a sample that is almost entirely 2024 for the scraped boards, 2019 for OJA and 2026 for `eures-escox` (13.1), and not the population.

**By country.** Completeness follows the source, because country is almost a function of source (DE: `jobs.de`, `eures-escox`, `eures`, OJA; FR: `kariera.fr`, `lesjeudis`; SE: `jobbland`, `jobbguru`; UK: `jobmedic`; EL: `kariera.gr` only).

| Country (postings) | title / description | occupations | skills | sectors | Other |
|---|---|---|---|---|---|
| DE (989) | 88% | 99% | 96% | 79% | `experience_level` 5%; `nuts1` 40% |
| FR (952) | 99% | 97% | 96% | 88% | `organization` 0%; `experience_level` 50% |
| SE (788) | 100% | 56% | 55% | 51% | `organization` 0% |
| UK (489) | 96% | 94% | 82% | 86% | `organization` 0% |
| **EL (468)** | **100%** | **90%** | **91%** | **83%** | `experience_level` 91%; `organization` 0% |
| BG (268) | 99% | 1% | 32% | 0% | `nuts1` 99% (EURES) |
| AT (265) | 2% | 100% | 100% | 2% | OJA: no text |
| CZ (227) | 99% / 93% | 100% | 68% | 52% | `experience_level` 0% |
| no code (469) | 100% | 95% | 96% | 90% | `jobscentral` |

Greece is among the best-filled countries, which settles the brief's concern about Greek data for postings. The comparison with Section 9.7 needs care: that table, based on pages spread over the whole life of each board, gives `kariera.gr` 58% occupations, 57% skills and 52% sectors, while the working sample gives 90%, 91% and 83%. The reason is the sample date (9.7 item 11, `docs/tag_fill_by_month.md`): `kariera.gr` tag fill is 78% to 100% in every month from August 2024 to November 2025 and 0% from December 2025; the working sample for `kariera.gr` is dated 2024 and so lies wholly in the tagged period, while the 9.7 pages also include the untagged months and average the two. Sweden is the weakest of the large countries (about 55% for occupations, skills and sectors), driven by `jobbguru` (sector completeness 18.8%, 13.3). `organization` is empty for all the scraped boards, which is the reason for deduplicating by content (Section 11, item 4).

**By sector.** For the 25 most frequent sector labels, `title`, `description` and `occupations` are 100% filled and `skills` is 77% to 100%. The lowest `skills` are in health care: residential nursing care 77%, diagnostic imaging and medical laboratories 77%, nursing and midwifery 79%, hospitals 85%. `experience_level` varies from 10% (patient transportation by ambulance) and 42% (electronic components) to 96% (security activities). The 1,617 postings with no sector (32% of the used sample) are less complete: `title` and `description` 71%, `occupations` 53%, `skills` 63%. Two consequences for the design: sector shares and sector-specific comparisons rest on the 68% of postings that carry a sector and that are better filled than the rest, so a sector comparison describes the labelled postings and not all postings; and a text classifier cannot label the 29% of the unlabelled postings that have no title or description (mostly OJA), which the validation sample must account for.

