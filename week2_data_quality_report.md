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

However, Revelio is simultaneously the *strongest* source on three other fields that are weak everywhere else: `occupation_uris` (94.0%, vs. 0.0% elsewhere), `startdate` (42.0%, vs. ~0% elsewhere), and — confirmed during the Week 3 fallback-chain build, below — `sectors` (91.6%, vs. 1.2% on LinkedIn and 0.0% on every STACK source). This indicates Revelio is a structurally different kind of source — closer to a formal employment record than a free-text profile — and its weaknesses and strengths are complementary to, not simply worse than, the other sources. This supports the thesis's existing design choice of a multi-tier fallback chain: different sources carry genuinely different kinds of signal, and no single tier or source can be relied upon alone.

This trade-off has a direct, non-obvious consequence for Tier 3 of the fallback chain (sector + highest-degree prior): see Section 10 below. The field Tier 3 needs to build its prior (`sectors`) and the field it needs to validate against (`skills`) are concentrated in the same single source, and within that source they are close to mutually exclusive (91.6% vs. 12.4% completeness) — so the overlap population Tier 3 can actually learn from is far smaller than either field's completeness would suggest on its own.

## 7. Finding 4: Source Naming Is Inconsistent and Needs Normalisation

Both the profile and posting source lists contain what appear to be duplicate or near-duplicate sources under inconsistent casing or naming:

- Profiles: e.g. `stack-math` vs. `STACK-Mathematics`, `stack-law` vs. `STACK-Law` (14 such pairs across the 29 profile sources).
- Postings: e.g. `jobbguru` vs. `jobbguru.se`, `jobmedic` vs. `jobmedic.co.uk`, `lesjeudis` vs. `lesjeudis.com`.

Some of these (e.g. the `.se`/`.co.uk`/`.fr` suffixed postings sources) plausibly represent genuine country-specific variants of the same underlying job board rather than true duplicates, and should be treated as such rather than merged. The STACK profile sources are more likely genuine duplicates introduced at the ingestion stage, since the paired completeness figures (e.g. `stack-math` 60.4% vs. `STACK-Mathematics` 96.8% skills completeness) differ enough to suggest they are not simply case variants of an identical dataset, but may instead reflect two separate scrapes or processing passes of the same topic area. This should be resolved with a source-normalisation step before `source` is treated as a clean categorical variable in any analysis (e.g. the DGI's labour-market sub-index), and is flagged here rather than resolved silently.

## 8. Finding 5: No Multi-Role Career History Is Available for Any Profile

The brief's Week 2 activities explicitly call for confirming "career history depth (multiple roles per profile, with dates) needed for transition analysis." This was checked directly and the answer is negative: **the Skillab tracker API does not provide multi-role career history for profiles, structurally or otherwise.**

Three independent checks confirm this:

1. **Type-checked across all 27 fields on all 7,222 sample profiles**, the only list-typed fields are `skills`, `occupation_uris`, and `sectors` — none of which is a role/position history. The three role-adjacent fields (`company`, `occupation`, `startdate`) are strictly scalar; no profile in the sample carries more than one value under any of them.
2. Those three fields are themselves very sparse: `company` 2.9%, `occupation` 6.9%, `startdate` 1.5%.
3. **Confirmed against the live API schema directly** (Swagger docs, `ProfileSchema`), not just inferred from the sample: the schema's 27 fields match exactly what the sample shows, and the only profile-related endpoints in the entire API are `POST /api/profiles`, `GET /api/profiles/sources`, `GET /api/descriptive-analytics/profiles`, `GET /api/exploratory-analytics/profiles/skills-by-location`, and `GET /api/clustering-analytics/profiles`. None exposes positions, experience, or work history in any form.

As a secondary check, the free-text `content` bio field was scanned for multiple distinct years mentioned (a rough proxy for prose-narrated career history, since there's no structured field for it): only 4.3% of profiles with content mention two or more distinct years at all, which is an upper bound on how many profiles *might* narrate a transition in prose — not a confirmed count, and would require dedicated NLP extraction to verify even that.

**Implication:** any thesis analysis that depends on tracking an individual's role-to-role transitions over time cannot be built from this API's profile data as currently exposed. This is a scope-level finding that should be raised with the supervising team directly, rather than something resolvable through better querying or additional fallback logic — the data simply isn't there. Depending on how central multi-role transition tracking is to the thesis's planned analysis, this may require either restructuring that part of the analysis to rely on postings-level signals (e.g. aggregate occupation/skill shifts across the corpus over time, rather than individual career trajectories) or seeking a supplementary data source.

## 9. Dedicated Date-Coverage Check: Confirmed Results

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

1. **~~Dedicated date-coverage check~~ — complete (Section 9).** `eures-escox`'s pre-2019 coverage remains genuinely unresolved after three attempts and is reported as a limitation rather than pursued further. **Open sub-item:** the check confirmed data exists "2019 onward" as a lumped range, not the brief's specific 2019–2020 baseline window in isolation — worth a narrower follow-up check before relying on 2019–2020 specifically as the pre-shock baseline.
2. **~~Tier 1–4 fallback chain~~ — complete (Section 10).** Applied to the full working sample; Tier 3's near-total absence is documented as a structural finding rather than a defect.
3. **Source normalisation.** Decide, source by source, which apparent duplicates (STACK sources) should be merged and which (country-suffixed job boards) should be kept distinct, before `source` is used as a categorical variable elsewhere in the thesis.
4. **Occupation-URI augmentation plan.** ~~Since `occupation_uris` is only usable for Revelio~~ — addressed in Section 10 via the free-text exact-match Tier 2 enhancement (27 additional profiles resolved beyond the 197 from `occupation_uris` directly).
5. **NUTS/geocoding decision.** Decide between restricting regional analysis to EURES-family sources (simpler, but narrows the regional sample considerably) or building a geocoding fallback for the free-text `location` field (broader coverage, but a non-trivial additional pipeline step).
6. **~~Career history depth~~ — checked, result is negative (Section 8).** No multi-role history exists in the API, confirmed against the live schema. Raise with the supervising team: does the thesis's transition analysis need restructuring around postings-level aggregate signals instead of individual career trajectories, or is a supplementary data source needed?
7. **Postings by country/sector, profiles by occupation group.** The brief's Week 2 deliverables ask for postings broken down by country and sector (we have by-year and by-source only) and profile completeness broken down by occupation group (we have by-source only) — not yet built.
8. **Schema documentation.** Write up the real field list, types, and known quirks (mixed ESCO/ISCO URIs in `occupation_uris`, the literal string `'empty'` in `highest_degree`/`degree`, which fields are source-concentrated) as a single reference document — currently this only exists scattered across diagnostic script outputs in this conversation.
9. **Week 4 deliverable.** ~~Write the one-paragraph data-quality policy~~ — complete (`week4_data_quality_policy.md`).
