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

However, Revelio is simultaneously the *strongest* source on two other fields that are weak everywhere else: `occupation_uris` (94.0%, vs. 0.0% elsewhere) and `startdate` (42.0%, vs. ~0% elsewhere). This indicates Revelio is a structurally different kind of source — closer to a formal employment record than a free-text profile — and its weaknesses and strengths are complementary to, not simply worse than, the other sources. This supports the thesis's existing design choice of a multi-tier fallback chain: different sources carry genuinely different kinds of signal, and no single tier or source can be relied upon alone.

## 7. Finding 4: Source Naming Is Inconsistent and Needs Normalisation

Both the profile and posting source lists contain what appear to be duplicate or near-duplicate sources under inconsistent casing or naming:

- Profiles: e.g. `stack-math` vs. `STACK-Mathematics`, `stack-law` vs. `STACK-Law` (14 such pairs across the 29 profile sources).
- Postings: e.g. `jobbguru` vs. `jobbguru.se`, `jobmedic` vs. `jobmedic.co.uk`, `lesjeudis` vs. `lesjeudis.com`.

Some of these (e.g. the `.se`/`.co.uk`/`.fr` suffixed postings sources) plausibly represent genuine country-specific variants of the same underlying job board rather than true duplicates, and should be treated as such rather than merged. The STACK profile sources are more likely genuine duplicates introduced at the ingestion stage, since the paired completeness figures (e.g. `stack-math` 60.4% vs. `STACK-Mathematics` 96.8% skills completeness) differ enough to suggest they are not simply case variants of an identical dataset, but may instead reflect two separate scrapes or processing passes of the same topic area. This should be resolved with a source-normalisation step before `source` is treated as a clean categorical variable in any analysis (e.g. the DGI's labour-market sub-index), and is flagged here rather than resolved silently.

## 8. Caveat: Posting Date Ranges in This Sample Are Not Yet Reliable Evidence of True Source Coverage

An initial check of `upload_date` ranges by source suggested that most sources' data only begins in 2023–2024, with the exception of `OJA`, which appeared to span only five days in 2019. This is very likely a sampling artefact, not a true reflection of source coverage, for two reasons:

1. For the three chunked sources (`eures`, `eures-escox`, `OJA`), the fetch script stops pulling from a given date-range chunk as soon as it has enough records to meet its target, so the apparent date range reflects wherever in the chunk the API happened to return records from first, not the chunk's true span.
2. For all other sources, only the first ~468 records returned by the API (in whatever default order it uses, not necessarily chronological) were sampled, so the observed date range reflects an arbitrary slice, not the source's actual temporal coverage.

**This caveat means the "which sources reach back to 2019" check in the current notebook should not be relied upon as-is.** A dedicated check — querying each source's true `min_upload_date`/`max_upload_date` directly via the API's date filters, without relying on an incidentally-ordered sample — is needed before any claim about temporal coverage is made in the thesis. This is proposed as the next concrete task (Section 9).

## 9. Recommended Next Steps

1. **Dedicated date-coverage check.** For each posting source, issue two lightweight queries (`page_size=1`, sorted or filtered toward the earliest and latest plausible dates) to establish genuine `min`/`max` upload dates, rather than inferring coverage from this sample.
2. **Source normalisation.** Decide, source by source, which apparent duplicates (STACK sources) should be merged and which (country-suffixed job boards) should be kept distinct, before `source` is used as a categorical variable elsewhere in the thesis.
3. **Occupation-URI augmentation plan.** Since `occupation_uris` is only usable for Revelio, decide whether Tier 2 of the fallback chain should be modified to map the free-text `occupation` field to an ESCO URI for other sources, and scope this as its own task if so.
4. **NUTS/geocoding decision.** Decide between restricting regional analysis to EURES-family sources (simpler, but narrows the regional sample considerably) or building a geocoding fallback for the free-text `location` field (broader coverage, but a non-trivial additional pipeline step).
