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

## 4. Finding 1: `occupation_uris` Is Confirmed Revelio-Exclusive

The initial Week 2 completeness-by-source audit (based on a 250-record sample per source) suggested `occupation_uris` was a near-binary split by source:

| Source | `occupation_uris` completeness |
|---|---|
| revelio | 94.0% |
| every other profile source (all STACK sources, linkedin) | 0.0% |

This was re-checked against a much larger population to rule out a sampling artefact: for 23 of the 29 non-Revelio profile sources, **every single record** was checked (not a sample); for the remaining 6 larger sources, up to 2,000 records each were checked. Across **30,389 checked records spanning all 29 non-Revelio sources, zero had a non-empty `occupation_uris` field.** `occupation_uris` is confirmed Revelio-exclusive, not a sampling artefact.

**Implication for the Tier 2 fallback (occupation URI → default skill set):** this fallback tier is only reachable for Revelio-sourced profiles, roughly 3.5% of the current sample. For every other source, a profile without direct skills (Tier 1) cannot fall through to Tier 2 via this field, because the field is structurally absent at the source level, not missing at random. Broader Tier 2 coverage requires mapping the free-text `occupation` field (populated far more broadly) to an ESCO occupation URI as a pre-processing step, rather than relying on `occupation_uris` being present.

**Tier 2 lookup mechanism (built, Month 2 Week 3):** the Tracker API itself does not expose an occupation→skill relation (confirmed by inspecting `IscoOccupationSchema`, which has no skills field, and the `Utility` endpoints, which only expand within the occupation hierarchy itself — see Appendix). Tier 2 is instead implemented as a local lookup against the European Commission's own official ESCO occupation-skill relations file (`occupationSkillRelations_en.csv`, downloaded directly from esco.ec.europa.eu), confirmed to contain 126,051 relation rows across all 3,039 ESCO occupations, split into "essential" (67,600) and "optional" (58,451) relations. This lookup is entirely local and offline once the file is downloaded, so it is unaffected by the Tracker API's reliability issues.

## 5. Finding 2: NUTS Coverage Is Concentrated in the EURES Family of Sources

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

## 6. Finding 3: Revelio's Field Profile Is a Genuine Trade-off, Not Simply "Worse" Data

Revelio was flagged in the thesis brief as a source to check for disproportionately sparse skills. This is confirmed:

- Revelio `skills` completeness: **12.4%**, against a mean of 64.1% and median of 62.8% across all other profile sources — the single lowest of any source by a wide margin.

However, Revelio is simultaneously the *strongest* source on two other fields that are weak everywhere else: `occupation_uris` (94.0%, vs. 0.0% elsewhere) and `startdate` (42.0%, vs. ~0% elsewhere). This indicates Revelio is a structurally different kind of source — closer to a formal employment record than a free-text profile — and its weaknesses and strengths are complementary to, not simply worse than, the other sources. This supports the thesis's existing design choice of a multi-tier fallback chain: different sources carry genuinely different kinds of signal, and no single tier or source can be relied upon alone.

## 7. Finding 4: Source Naming Is Inconsistent and Needs Normalisation

Both the profile and posting source lists contain what appear to be duplicate or near-duplicate sources under inconsistent casing or naming:

- Profiles: e.g. `stack-math` vs. `STACK-Mathematics`, `stack-law` vs. `STACK-Law` (14 such pairs across the 29 profile sources).
- Postings: e.g. `jobbguru` vs. `jobbguru.se`, `jobmedic` vs. `jobmedic.co.uk`, `lesjeudis` vs. `lesjeudis.com`.

Some of these (e.g. the `.se`/`.co.uk`/`.fr` suffixed postings sources) plausibly represent genuine country-specific variants of the same underlying job board rather than true duplicates, and should be treated as such rather than merged. The STACK profile sources are more likely genuine duplicates introduced at the ingestion stage, since the paired completeness figures (e.g. `stack-math` 60.4% vs. `STACK-Mathematics` 96.8% skills completeness) differ enough to suggest they are not simply case variants of an identical dataset, but may instead reflect two separate scrapes or processing passes of the same topic area. This should be resolved with a source-normalisation step before `source` is treated as a clean categorical variable in any analysis (e.g. the DGI's labour-market sub-index), and is flagged here rather than resolved silently.

## 8. Dedicated Date-Coverage Check: Confirmed Results

An initial completeness-notebook check of `upload_date` ranges by source was found to be unreliable: it reflected wherever in an arbitrarily-ordered or date-chunked sample the fetch happened to land, not each source's true coverage (e.g. it initially suggested `OJA` spanned only five days in 2019, which turned out to be a sampling artefact). A dedicated check was built to resolve this properly, querying each source directly via the API's `min_upload_date`/`max_upload_date` filters rather than inferring coverage from an incidentally-ordered sample.

**Method note:** the first version of this dedicated check used a lightweight, `page_size=1` "count-only" query, on the reasoning that fewer returned records would mean a lighter request. This was empirically wrong: these lightweight queries failed unreliably and unpredictably — including, on one run, failing twice on a date range (`eures-escox`, 2023) that had been independently confirmed via a different method to contain 417 real records. The working pattern, consistent with every successful data-pull across this project, turned out to be the full `page_size=100` paginated request shape. Once the check was rebuilt around that pattern, and narrowed from checking all 12 individual years to two wide-range probes per source (2019-onward, and 2010–2018), it completed cleanly in about 22 minutes.

**Results:**

| Source | Confirmed data 2019+ | Confirmed data pre-2019 |
|---|---|---|
| brightminds | Yes (1 posting, 2024 only) | No |
| eures | Yes (401,511) | Unresolved |
| eures-escox | Yes (891,613) | Unresolved (failed 3 attempts across 2 sessions) |
| jobbguru / jobbguru.se | Yes (319 each) | No |
| jobbland | Yes (68,092) | Yes (3) |
| jobbland.se | Yes (694,823) | Unresolved |
| jobmedic / jobmedic.co.uk | Yes (1,010 / 1,448) | No |
| jobscentral | Yes (6,284) | No |
| jobs.de | Yes (34,230) | No |
| kariera.fr / kariera.gr | Yes (86,468 / 87,766) | No |
| lesjeudis / lesjeudis.com | Yes (18,404 / 55,375) | No |
| OJA | Yes (2,924,235) | **Yes (123,200)** |

**Conclusion: 15 of 16 posting sources confirm coverage from 2019 onward.** `brightminds` is the only source confirmed *not* to reach 2019 (it has a single posting, dated 2024). Whether `eures-escox` has any data before 2019 remains genuinely unresolved — the recent-range probe succeeded (891,613 postings confirmed from 2019 onward), but the pre-2019 probe failed consistently across three independent attempts on two separate days. Given this specific probe has never once succeeded despite the source's own recent-range data being large and reliably retrievable, this is reported as an open limitation rather than assumed to mean "no pre-2019 data" either way.

Two further findings worth noting:
- **`OJA` is the deepest historical source found**, with 123,200 confirmed pre-2019 postings — the opposite of the original (artefact-driven) impression that it was a narrow, recent-only source.
- **`eures`'s total count (401,511) differs from an earlier count of this source (362,902) taken on an earlier date.** This is not an error; it reflects that the underlying dataset is live and continues to grow. Any exact counts reported in this thesis should be understood as a snapshot taken on a specific date, not a fixed figure.

## 9. Recommended Next Steps

1. **~~Dedicated date-coverage check~~ — complete (Section 8).** `eures-escox`'s pre-2019 coverage remains genuinely unresolved after three attempts and is reported as a limitation rather than pursued further.
2. **~~Source normalisation~~ — decided (Month 2, Week 3).** STACK pairs kept distinct (completeness differs meaningfully between pairs, suggesting two ingestion passes rather than true duplicates) but flagged as likely over-counting independent coverage. Job-board country-suffixed sources kept fully distinct, with a derived `source_country` field. See `source_normalization.py`.
3. **~~Occupation-URI augmentation (Tier 2)~~ — built (Month 2, Week 3).** Implemented as a local lookup against the official ESCO occupation-skill relations file, not an API-dependent mechanism. See `occupation_skill_lookup.py`. Remaining work: a text-classification step to map the free-text `occupation` field to an ESCO occupation URI, so Tier 2 can fire for sources other than Revelio -- this is now the main open task for extending Tier 2 coverage.
4. **NUTS/geocoding decision.** Decide between restricting regional analysis to EURES-family sources (simpler, but narrows the regional sample considerably) or building a geocoding fallback for the free-text `location` field (broader coverage, but a non-trivial additional pipeline step).
