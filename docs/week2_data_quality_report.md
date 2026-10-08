# Month 2, Week 2: Data Coverage and Completeness Report

## 1. Scope

This report summarises the results of the Week 1–2 data collection and completeness audit against the Skillab tracker API, covering profiles and job postings across all available sources. It documents the sample collected, the completeness of the fields the thesis depends on, and several structural data-quality issues that affect how the Tier 1–4 skill-fallback chain and the regional (NUTS-based) analysis should be designed in Chapter 2.

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

## 9. Date Coverage and the Pre-Shock Baseline

This section replaces an earlier version that concluded "15 of 16 posting sources confirm coverage from 2019 onward". That statement was true but misleading for the thesis: "has data from 2019 onward" is not the same as "has data in the brief's 2019–2020 baseline window". Most sources pass the first test and fail the second.

### 9.1 Method and its limits

Coverage was measured with the API's `min_upload_date` / `max_upload_date` filters, using the `count` returned with a `page_size=100` request (a `page_size=1` count-only query proved unreliable and was dropped). Two query shapes were used:

- **Open-ended** (`min = <year>-01-01`, `max = today`) at the checkpoints 2019, 2021, 2023, 2024, 2025 and 2026. The count never rises as the checkpoint year rises, so identical counts at consecutive checkpoints mean no postings fall between them. For example, a source with the same count at 2019, 2021 and 2023 has every posting dated 2023 or later. Counts for an interval are obtained by subtraction.
- **Closed windows** (calendar year, then calendar month) for `OJA`, whose open-ended probes all timed out.

Two caveats apply throughout. First, the dataset is live and keeps growing, so counts taken on different days are snapshots, and subtraction across snapshots is a derivation, not a measurement (for example, `eures` grew from 362,902 to 401,511 between two measurement dates). Second, **a timeout is not informative.** Closed windows with no matching postings are slow (the empty months of 2025 each needed one to three retries or failed outright), but large windows also time out (2024-10 and 2024-12 failed three times and later returned 53,906 and 48,950). Persistently failing closed windows have so far usually turned out to be empty (`jobs.de` and `kariera.fr` for 2026, `jobbland` for 2025 onward, OJA from April 2025, and the 2019–2020 windows of several boards), but this is a hint and not proof, so every such window is confirmed by a positive measurement of its complement (a successful count for the neighbouring window that equals the known total) before being reported as zero.

### 9.2 What `upload_date` means

For the scraped job boards, `upload_date` is the posting date on the source board (confirmed by the project author; the API schema says only "Date when the job was uploaded"). For `OJA` the position is less clean. The Eurostat Web Intelligence Hub (WIH) metadata report (23 July 2026) defines the corresponding source variable `first_active_date` as the date the posting is first detected for a source, replaced by the publication date where the advertisement states one. If Skillab's `upload_date` derives from that field, OJA dates are a mixture of publication and first-detection dates. This mapping is **not verified**. The EURES family is a different case: it is an aggregator portal, not a scraped board, so the confirmation does not obviously apply. A secondary description of the EURES portal (not Skillab documentation, and not independently verified) says its date filter ("publication date") records when a vacancy notice was transmitted, imported or published onto the EURES database, which keeps notices only while they are current. The monthly counts for `eures-escox` do not fit a steady flow of postings or a stock of survivors rising towards the present. All 828,524 postings dated 2026 fall in two months: 130,336 in January and 698,188 in February (the two sum exactly to the 2026-onward total, so March–July are zero by subtraction, and August–October were measured at zero). Nothing is dated after February 2026, and a single month holds more than ten times the whole of 2025 (62,512). `eures` shows the same pattern: 99,040 postings in January and 260,801 in February 2026, which sum exactly to its 2026-onward total (359,841), so nothing is dated after February 2026. This looks like a bulk load, so for the EURES family `upload_date` behaves like an import date and does not measure when employers posted the vacancy. The EURES family is therefore **not usable for time-series analysis**. Whether the 2025 counts (41,090 for `eures`, 62,512 for `eures-escox`) are also clustered into a few import months could not be established: all twelve monthly probes for `eures-escox` 2025 timed out on every attempt. This does not change the conclusion above. The question for the Skillab team is in Section 11.

### 9.3 Posting sources other than OJA: one-year snapshots, late ramp-ups, almost no baseline

Postings by period, derived from open-ended counts (identical counts at consecutive checkpoints mean an empty interval). The pre-2024 columns combine counts taken on different days, so small differences between snapshots are possible.

| Source | 2019–2020 | 2021–2023 | 2024 | 2025 | 2026 to date |
|---|---|---|---|---|---|
| brightminds | 0 | 0 | 1 | 0 | 0 |
| jobbguru, jobbguru.se | 0 | 0 | 319 each | 0 | 0 |
| jobmedic / jobmedic.co.uk | 0 | 0 | 1,010 / 1,448 | 0 | 0 |
| jobscentral | 0 | 0 | 6,284 | 0 | 0 |
| lesjeudis | 0 | 0 | 18,404 | 0 | 0 |
| lesjeudis.com | 0 | 0 | 24,741 | 23,055 | 7,579 |
| kariera.gr | 0 | 0 | 24,306 | 36,194 | 27,266 |
| kariera.fr | 0 | 0 | 74,975 | 11,493 | 0 (derived) |
| jobs.de | 0 | 0 | 27,680 | 6,550 | 0 (derived) |
| eures | 0 | 444 | 136 | 41,090 | 359,841 |
| eures-escox | 0 | 426 | 151 | 62,512 | 828,524 |
| jobbland.se | 90 | about 1,550 | 167,678 | 138,867 | 386,638 |
| jobbland | 9 | about 1,114 | 66,969 | 0 | 0 (derived) |

(The 417 `eures-escox` postings for 2023 match an independent check made earlier in the project. Pre-2019 coverage of `eures-escox` and `jobbland.se` remains unresolved.)

What this shows:

- **Six boards are essentially one-year snapshots of 2024** (`brightminds`, `jobbguru`/`.se`, `jobmedic`/`.co.uk`, `jobscentral`, `lesjeudis`, and `jobbland`, which also has about 1,100 postings in 2021–2023 and nothing after 2024), with nothing or almost nothing before or after. They support cross-sectional analysis of 2024 only.
- **No source other than OJA has a usable 2019–2020 baseline.** The only non-zero values are 9 and 90 postings for `jobbland` and `jobbland.se`.
- **Data after March 2025 exists only outside OJA**, in `eures`, `eures-escox` (cross-sectional use only, see below), `jobbland.se`, `kariera.gr` and `lesjeudis.com`, plus `jobs.de` and `kariera.fr` for 2025 only (6,550 and 11,493 postings, measured directly with closed 2025 windows, which also show that neither source has anything dated 2026). These are different sources, with a different mix from the baseline.
- **The EURES family is almost entirely 2025–2026 and highly clustered.** Only about 0.14% of `eures` postings and 0.06% of `eures-escox` postings predate 2025. For `eures-escox`, 2026 consists of 130,336 postings in January and 698,188 in February and nothing afterwards (see 9.2). The dates describe import events and not posting activity, so this family can support cross-sectional analysis (composition, skills) but not any trend over time.

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

- **No source spans the whole period.** The baseline (2019–2020) exists only in OJA, which ends in March 2025. Everything after March 2025 comes from other sources that have almost nothing before 2024 or 2025. Pooling them would confound any change in deglobalisation language with a change in source and country mix.
- **Raw counts are driven by ingestion** and cannot measure labour demand, in OJA (the January 2024 step) or in the EURES family (the 2026 ramp-up). Analyses should use **shares and rates within each period**, with composition (country via `location_code`, occupation group, sector) checked.
- **The brief's validation windows are covered unevenly.** The 2022 energy-crisis and 2023 Chips Act windows fall inside the 2019–2023 OJA regime. The 2025 tariff window can be examined only (a) in OJA for January–March 2025, which precedes the main April measures, and (b) in within-source series for `eures-escox`, `jobbland.se` and `kariera.gr`, analysed separately and never pooled with OJA without calibration.
- **Bridging is possible only where sources overlap**: OJA against `kariera.gr`, `lesjeudis.com`, `jobbland.se`, `jobs.de` and `kariera.fr` during 2024, and against the EURES family and the same boards in January–March 2025. A calibration on country and occupation shares in those months is the natural design, but it needs the composition analysis first.
- **OJA's occupation coverage changes over time and is narrow** (Sections 9.4c and 9.4d), so the monthly total must not be used as a series. Only eight ISCO codes (chemical and process industries, laboratory, environment) run from 2019 to March 2025; ten others exist only in 2024.
- **Provisional recommendation (to be agreed with the supervisor):** restrict any OJA series to the eight core codes. The earlier plan (2019–2023 OJA as the primary series, 2024 to March 2025 as a second regime, post-March 2025 sources as a separate supplementary analysis) no longer holds for OJA as a whole, because the 2024 regime is a different set of occupations. The post-March 2025 supplementary analysis is unaffected. All of this must be reconciled with the brief's timeline (monthly data to 2026).
- Profiles carry almost no usable dates (`startdate` 1.5%), so all time-series work rests on postings.

## 10. Week 3: Tier 1–4 Fallback Chain — Results

The fallback chain (brief Section 4, Table 3) was implemented as a single integrated function (`assign_data_completeness_tier.py`) combining:
- **Tier 1 "Full":** direct `skills`.
- **Tier 2 "Inferred":** ESCO occupation lookup (`occupation_skill_lookup.py`, using the official `occupationSkillRelations_en.csv`, 126,051 rows / 3,039 occupations), reachable either via `occupation_uris` directly (Revelio) or via an exact-substring match of the free-text `occupation` field against ESCO occupation labels (`occupation_text_matcher.py`, validated at 100% precision on a 12-case hand-labelled sample; a TF-IDF fuzzy-matching fallback was also built and validated, found to perform worse than chance — 30% precision — and is disabled by default).
- **Tier 3 "Weak":** an empirical sector + highest-degree prior (`tier3_sector_degree_prior.py`), built only from genuine Tier-1 profiles, bucketed by `(sector, highest_degree)` with a `(sector,)`-only fallback, requiring at least 20 Tier-1 profiles in a bucket before trusting it.
- **Tier 4 "Sparse":** excluded from skill-based analyses; retained for geographic/demographic analysis only.

Applied to the full 7,222-profile working sample:

| Tier | Label | Count | % of sample |
|---|---|---|---|
| 1 | Full | 4,526 | 62.7% |
| 2 | Inferred | 224 | 3.1% |
| 3 | Weak | 0 | 0.0% |
| 4 | Sparse | 2,472 | 34.2% |

(Tier 1's 62.7% matches the aggregate `skills` completeness in Section 3 exactly, confirming the two independent measurements agree. Of Tier 2's 224 profiles, 197 resolved via `occupation_uris` and 27 via the free-text exact-match enhancement.)

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
8. **Breakdown tables - done for the working sample (Section 13).** Population-level country counts (for example Greek postings in OJA) still need filtered count queries.
9. **Schema documentation - done** (`docs/schema.md`, regenerated by `python -m diagnostics.19_generate_schema_doc`).
10. **Questions for the Skillab team or supervisor.** (a) Is `upload_date` the source board's posting date for scraped boards, and what is it for OJA (publication date or first-detection date)? (b) Does the API expose the underlying OJA source or its stability flag? (c) Are OJA postings de-duplicated across skills and locations? (d) What explains the January 2024 step and the end of data in March 2025? (e) Is `upload_date` for the EURES family an import or publication date on EURES and not the employer's posting date, given that 84% of `eures-escox`'s 2026 postings fall in February 2026 and nothing is dated after that? (f) What coverage is planned after March 2025, since the brief assumes monthly data to 2026? (g) Why do OJA postings have an empty title and no description or organization, and is OJA in Skillab restricted to certain occupations or is it the full Eurostat OJA?
11. **~~Week 4 deliverable~~ - complete** (`week4_data_quality_policy.md`).

## 12. Month 2 Deliverables Status (against the brief)

| Brief requirement | Status |
|---|---|
| Connect to the API; pull postings and profiles | Done (7,222 profiles, 6,723 postings, all sources) |
| Audit field completeness | Done (Sections 3-8); occupation-group tabulation pending |
| Baseline window (2019-2020) and coverage | Done (Section 9): OJA only, restricted to eight ISCO codes; 2024 adds ten codes that exist only that year; OJA ends March 2025; later data only from other sources |
| Four-tier fallback chain, tested on 5,000+ profiles | Done (Section 10; applied to 7,222) |
| Career-history depth | Done: negative (Section 8) |
| Data coverage report (by year, country, sector) | Done for the working sample (Section 13); sample is not time-representative, so population-level counts remain open |
| Profile completeness report (source, occupation group) | Done (Sections 3-8 and 13.5); the occupation-group view covers only 3.3% of profiles (Revelio) |
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
