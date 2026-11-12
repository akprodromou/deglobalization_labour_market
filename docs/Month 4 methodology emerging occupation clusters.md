# Month 4 methodology: emerging occupation clusters

Nov 10, 2026 · @anton

Month 4 clusters job titles, and titles plus skills, to find emerging occupations in the three boards, then measures their volume and regional concentration. This page records the method and the decisions taken so far; it is a working draft.

## Status and decisions

Month 3 is finished and the supervisor approved moving to Month 4. The brief: embed job titles (multilingual-e5), cluster them (HDBSCAN, with UMAP for validation and a k-means ablation), check the clusters against seven named occupations, then build quarterly volume series, regional HHI and an Occupation Emergence Rate per cluster.

**Deliverables.** A validated set of 6 to 10 emerging occupation clusters (they need not be the seven named), quarterly volume series, HHI per cluster and region, and the emergence-rate series.

**Named occupations to look for:** trade compliance officer, supply chain resilience analyst, semiconductor process engineer, battery cell technician, critical materials specialist, export control specialist, reshoring program manager. We report which are found and do not force them.

**Decisions taken in Month 4**

- Baseline is within sample: AccelerateEU (22 April 2026) for jobbland.se, InvestAI (11 February 2025) for lesjeudis.com, none for jobs.de.
- Weighted shares only; the boards are never merged.
- Postings are mapped to NUTS-2; vague locations are dropped from HHI and their share is reported.
- All postings are clustered first. The flagged share and channel mix come afterwards from the Month 3 tags.
- Emergence threshold is 100 postings per quarter per board, plus a share-based version. Quarters rather than a full year suffice.
- Only inputs A (title) and D (title plus skills) are run; B and C are not.
- Titles alone do not define the work, so a skills lens is needed. Duties come late in postings, so truncated views are not enough.

## Pipeline

The pipeline runs per board (jobbland.se 53,959 postings, lesjeudis.com 18,625, jobs.de 12,243). Embedding, UMAP and HDBSCAN run on Colab (T4); shares, NUTS-2 mapping and HHI run on the Mac.

1. **Title cleaning** (script 90). Strips employer names, locations, gender markers such as (m/w/d) and trailing reference codes (for example IRC207099 or 2024-112135), and removes frequent trailing segments found by counting suffixes (25 or more occurrences). Segments starting with a digit are never dropped. Changed titles: jobs.de 11,814; lesjeudis 14,535 (78.0%); jobbland 24,625 (46.8%).
2. **Embedding.** Each cleaned title gets the prefix "query: " and goes through multilingual-e5-large (1024 dimensions, L2-normalised). A posting without a title uses the first 150 characters of its description.
3. **Input A** is the title embedding alone.
4. **Input D** concatenates three blocks, each L2-normalised and weighted, then renormalised: the title embedding (weight 1), an ESCO skills block (tf-idf over ESCO skills extracted from the full text, reduced to 100 dimensions with TruncatedSVD, weight 0.5) and a pruned Lightcast block (tf-idf, 20 dimensions, weight 0.3). Postings with no skills get zeros in those blocks, so they are clustered on the title only. The weights are untested defaults; v1 used 1.0 and 0.5.
5. **Clustering.** UMAP to 10 dimensions (cosine, min\_dist 0, n\_neighbors 30), then HDBSCAN (min\_cluster\_size 40, min\_samples 10, eom). Three seeds. A k-means run with the same k is the ablation.
6. **Skills source.** ESCO skills come from script 69b: sentence-embedding matching (all-MiniLM-L6-v2, similarity at least 0.6) over windows of up to 3,000 characters, so duties that appear late in a posting are covered. Lightcast terms come from script 91 and lexicon/lightcast\_block\_terms.csv (629 rows, 135 selected, 16 pruned).

## Results so far

**Cluster counts.** jobs.de gave 79 clusters on A and 109 on D; lesjeudis gave 141 on A and 122 on D. Between 31% and 40% of postings end as noise. Noise is HDBSCAN label -1: a posting that is not in a dense region of at least 40 similar postings. Rare emerging occupations may sit in noise, so the noise share is reported with every result.

**D v1 withdrawn.** An earlier reading that D beats A on internal metrics (relative validity, stability, k-means agreement) was wrong. Those metrics rewarded clusters formed around a single skill, which are artefacts. After reading the cluster reports, D v1 was withdrawn. One cause is false ESCO matches: sentence-embedding similarity above 0.6 can link generic template sentences to unrelated skills, which is how a skill such as "feed concrete mixer" appeared on IT consultant postings (hypothesis; a diagnostic cell was supplied and its output is pending). Another is the Lightcast term "Supply Chain", which is boilerplate on lesjeudis: 351 of 352 postings in one cluster.

**Coherence filter (v3).** Before building the skill blocks, each skill is kept only if the postings carrying it have similar title embeddings. The embeddings are first centred on the board mean, because e5 scores cluster in a narrow high band (the model card says this is expected, from the 0.01 InfoNCE temperature) and without centring every skill looked equally coherent. Coherence is the norm of the mean of unit vectors, compared with five random sets of the same size; the skill is kept when the lift is at least 0.15. This is my own heuristic, not a published method. It was tested on mock and synthetic data only, and the 0.15 threshold and the 0.5/0.3 weights are untested on real data. A published, citable alternative is document-frequency pruning (max\_df) or taking skills from the description only.

**Named occupations.** The seven named occupations are nearly absent from the A and D outputs. The regex matches for "battery" are unverified. We report which are found without forcing any of them into a cluster.

**Status.** Inputs A for all three boards and D v1 are done. The `--coherence-only` reports are the next step (see open items), then D reruns with tag v2.

**First cluster series on input A (script 93, 12 November).**

- **The count threshold follows the board's size, not the labour market.** jobbland's weighted postings per quarter run 727, 5,389, 16,278, 145,266, 87,115, 10,481, 7,493, 33,777, 166,360, 147,642 and 72,636 (2024-Q1 to 2026-Q3). So 174 clusters "newly cross" 100 postings in 2024-Q4 only because the board is 9 times larger than in 2024-Q3. The cause of the 10-fold drop in 2025-Q2 and Q3 is not known. The share version (0.1% of the quarter) is the metric to use; interval-based crossings (the whole interval C above or below the line) are reported next to it.
- **Volume does not select emerging occupations.** 238 of 256 jobbland clusters, 61 of 141 lesjeudis clusters and 53 of 79 jobs.de clusters pass the threshold. The largest are ordinary occupations: nurses, service technicians, teachers, helpdesk technicians, Java developers. None of the seven named occupations appears among them.
- **Candidates must come from flagged share and change.** On lesjeudis the clusters with the highest flagged shares are defense-flavoured IT roles: cybersecurity engineer (62% flagged), embedded software engineer (60%), systems engineer (45% and 42%), AI engineer (28%), information systems security manager (22%). These are candidates, not validated occupations, and their flags rest mostly on the defense channel, whose precision limits are in the Month 3 report.
- **jobs.de cannot support an emergence series.** Three usable quarters, the last with 76 of 90 days, and flagged shares near zero in every large cluster.
- **Two jobbland clusters are not occupations.** Clusters 171 and 168 (peak shares of 16.1% and 5.4% in 2025-Q4) have empty titles, 99% to 100% unplaced locations and recruiting-ad or church-election text. They passed the template check, so a title-less share is now part of eligibility.
- **Change around an event** now compares equal windows (90 days before and from the event) instead of the whole board.

## Thresholds: 40 and 100

Two different thresholds do two different jobs, and they apply at different moments.

- **40 postings (min\_cluster\_size)** decides whether a cluster exists at all. It counts collected postings over the whole period and is applied inside HDBSCAN.
- **100 postings per quarter** decides whether an existing cluster has emerged. It counts weighted, estimated postings in a quarter (not collected ones) and is applied afterwards, per board. A share-based version is run alongside it.

Example: a cluster of 45 collected postings spread over six quarters exists (45 is at least 40). If its weights scale those up to an estimated 130 postings in the latest quarter, it crosses the emergence line in that quarter. A cluster of 30 collected postings is never formed, so it cannot be counted, even if its weighted size would exceed 100.

The Occupation Emergence Rate is the number of clusters crossing the 100-per-quarter line, per quarter and board.

## Time series, weighted shares and uncertainty

**Collection design.** Script 52 does not download every posting. For each calendar day it reads the day's total from the Skillab API, then fetches one random page (about 100 postings; `--per-day`, default 100) of that day. Each record keeps the day total. Requests take 20 to 70 seconds (script 38 docstring), so the sample is probably a cost and speed choice; no line in the scripts states this, so it is my inference.

**Weighted shares.** A posting's weight is the day total divided by the postings taken that day. The share of a unit (a cluster, a tag, a skill) is the sum of the weights of its postings divided by the sum of the day totals. Example: on a day with 1,000 postings of which 100 were taken, each taken posting stands for 10. If 5 of the 100 are in a cluster, the cluster's estimated size that day is 50 and its share is 5%. Without weights, busy days would count the same as quiet days.

**Literature.** This is standard survey-sampling practice: weighting each unit by the inverse of its inclusion probability is the Horvitz-Thompson estimator (Horvitz and Thompson 1952, JASA), and sampling within strata (here days) is covered in Cochran, *Sampling Techniques*, and Lohr, *Sampling: Design and Analysis*. I verified that these references exist; the two textbooks I cite from memory. The scheme assumes the day total is the full population for that day, which holds only if the API count is complete for the day.

**The sample is not the population.** Random sampling within a day is valid only because the day total is known. The weighted population jumps from about 10,000 (September 2024) to about 48,000 (October 2024) on jobbland.se, so early 2024 is not comparable and is flagged. Date coverage from the file names: jobbland.se 2024-01 to 2026-09; lesjeudis.com 2024-08 to 2025-09; jobs.de 2024-08 to 2025-04. Two boards therefore have few quarters.

**Uncertainty.** A bootstrap within each day gives intervals for the shares (Efron 1979; Rao and Wu 1988 for resampling in complex surveys). It treats postings on a page as independent. They are probably not: a page holds adjacent postings in server order and script 52 notes that postings from one day share employers and batches. The within-day bootstrap may therefore understate the variance.

**Is resampling whole days safer?** Not unconditionally; an earlier draft said so too strongly. Resampling days (better, week blocks, because of the weekday cycle) does not rely on independence inside a page, because page clumping shows up in the day-to-day differences, so it is more conservative. But every day is in the sample in a stratified design, so between-day variation is not sampling error in the design-based sense. Day resampling answers a different question (is the change larger than ordinary day-to-day variability, which includes real fluctuation) and may overstate sampling error. Plan: report both intervals, and check employer concentration per page and overdispersion against a binomial. Overdispersion alone cannot separate clumping from real variation.

**Sampling check, first results (script 94, 11 November).** The indicator is the share of postings with any Month 3 flag. Three interval widths are compared per quarter: A redraws postings inside each day, B redraws employers inside each day, C redraws whole ISO weeks.

- **The employer test could not be run.** The employer field is empty on all three boards (jobbland 100%, lesjeudis 100%, jobs.de 99.8% of postings), so B equals A by construction there. On jobbland a proxy was used instead: postings whose first 80 description characters match count as one template. B/A then ranged from 0.96 to 1.33 and was mostly 1.0 to 1.2, so template clumping adds little, with one exception (2025-Q2, 1.33). A proxy catches only template clumping, not employers who write each ad differently. On a few days one template supplies a third of the page (90th percentile 33%).
- **Week-to-week variation is much larger than within-day noise on lesjeudis.** C/A is 2.2 to 2.8 in all five quarters. On jobbland C/A is 0.8 to 1.9 in most quarters, with an outlier of 3.9 in 2025-Q2 (2,010 postings). On jobs.de C/A is 0.7 to 1.2, but the flagged share is only 0.7% to 1.4%.
- **Reading.** The within-day interval alone is too narrow for lesjeudis. The data cannot say whether the cause is clumping or genuine week-to-week change in the flagged share. Week-block intervals also count any trend inside a quarter as noise, so they are conservative for trend detection, and C rests on only 9 to 14 weeks per quarter. Decision for now: report A and C side by side, and use C when judging whether a quarter-to-quarter change is real.

**Sampling check, follow-up on the spikes and gaps (11 November).**

- **jobbland, 14 to 20 April 2025.** 56 of 382 sampled postings are flagged (14.7%), 47 of them energy security. Of the 56, 41 (73%) open with the same sentence of a diversity statement, so they come from one template, probably one employer. The spike behind the wide 2025-Q2 interval is clumping, not a broad rise. The employer is not identified here.
- **lesjeudis has missing days.** Quarters hold 44 to 52 sampled days instead of about 91, and several weeks hold 1 or 2 days. Week-block intervals therefore also mix weekday composition, and the earlier assumption that every day is in the sample holds only for the days collected.
- **lesjeudis, July 2025.** The flagged postings come from many defense employers (Thales, Safran and naval firms among the description openings); the largest template group holds 12%. Late September to early October 2025 has 3.4% flagged (11 of 323), with no group above 9%. The titles give no explanation for the drop; whether those employers stopped posting on the board or the board's mix changed is not known. The lesjeudis flagged-share series is not read as a labour-market trend until this is checked.
- **Template proxy on lesjeudis.** B/A is 1.11 to 1.90 (design effect (B/A) squared, about 1.2 to 3.6), against about 1.0 with the employer field. The proxy is a lower bound: the Thales openings start with a place name that varies, so the 80-character keys split one employer into many groups.
- **Consequence for the method.** Report A and C intervals. Add a template-capped sensitivity: the share recomputed with each template group counted at most a fixed number of times per day. Do not call a one-week jump a trend when one template accounts for most of it.

**Trend method.** For each unit: presence in a posting (not frequency), weighted quarterly share, bootstrap interval, comparison with the baseline as an absolute change and a ratio, a simple slope or before-and-after test, and a read of sample postings. Guards: employer concentration, template text, seasonality, coverage jumps and multiple comparisons.

## Stability of the Skillab database (checks of 12 November)

**Three stages.** The data comes from the Skillab API, not directly from the boards. A posting reaches our sample through three stages: (1) the employer posts it on a board, (2) Skillab ingests it into its database, (3) our script 52 draws one random page of about 100 postings for each calendar day and weights each posting by day total divided by postings taken. Only stage 3 is random and under our control. The weights treat the API's day total as the true population of the day. A weighted share is therefore a valid estimate for what the database holds. It describes the labour market only if stages 1 and 2 are unrelated to the kind of job, and for change over time it is enough that they do not change in a way that depends on the kind of job. The supervisor has told us that the day is the posting's publication date; an ingestion that starts, stops or backfills a source would still change the day totals.

**Coverage regimes.** The weekly weighted population of jobbland (population\_jobbland.csv) is stable in two stretches: 2024-W41 to 2025-W07 and 2025-W50 to 2026-W35, roughly 6,000 to 15,000 postings a week outside holiday weeks. Between them (2025-W08 to 2025-W49) it is mostly under 2,000 a week, with a few spikes up to about 7,000, and before 2024-W19 it is under 700. lesjeudis has no jump of 3 times or more but only 286 of about 415 calendar days sampled, with the gap in 2025-Q1 and Q2. jobs.de has 221 sampled days up to 2025-04-09. A share is compared only inside one stretch of one board.

**Composition-stability test (script 97).** If ingestion changes, the mix of postings should change when the day total jumps. The mix is measured over clusters (script 92), Month 3 channels (six channels and none) and the posting's sector field. The distance is the Jensen-Shannon divergence between two pooled mixes, and both groups are cut at random to the same number of postings before every distance, because the distance grows when a sample is small and groups of unequal size would differ by size alone. The noise floor comes from shuffling whole days between the two groups (a page clumps postings of the same employers, so single postings are never shuffled). Comparisons: (i) low-volume against high-volume days, also inside the same quarter and weekday; (ii) 14 sampled days before against 14 after every jump of the day total of 3 times or more; (iii) the same comparison for stretches with no jump as placebo. 97b prints the cluster-by-cluster difference around one date, and 98 prints sample postings of named clusters.

**Results.**

- jobbland, low against high volume: before controlling for weekday the cluster mix differs (excess 0.106); inside the same quarter and weekday it hardly does (distance 0.016 against 0.011 expected by chance, excess 0.005, p=0.008) and the channel mix does not differ at all (excess 0.000, p=0.10). Weekdays against weekends explain most of the earlier difference. The sector mix still differs (excess 0.028), which fits the change of the sector field below.
- jobbland, jumps: the clearly significant cluster shifts are at 2024-12-23 (the Christmas dip, +0.032), and at 2025-12-09, 2025-12-23 and 2026-01-06 (+0.18, +0.04, +0.04). The last three are produced by two clusters (171 and 168) that exist only because title-less postings are embedded from their opening text (see below); they vanish when title-less postings are left out. Other jumps are borderline and moved between runs, so they are not reported as findings.
- jobbland, sector field: filled for 82 to 91% of postings until 2025-Q2, 52% in 2025-Q3 and 0% from 2025-Q4. The sector mix shifts strongly at the 2025-07-16 and 2025-09-17 jumps (excess +0.33 and +0.29). We do not use the field, so this matters only as a sign that Skillab's output for this board changed in 2025.
- lesjeudis: day totals stable (mean 126 to 251 a day by quarter), no jump to test, sector field filled for 94 to 97%, no difference in channel mix between low and high days and a very small one in cluster mix (excess 0.004 inside quarters).
- jobs.de: two jumps (2024-12-25, 2025-02-05), neither significant (p=0.09, 0.08); no difference between low and high days. Only 221 sampled days, so the test has little power.

**What we can claim.** Within what the database holds, the kinds of job do not depend on how many ads came in. This is consistent with ingestion being unrelated to occupation. It is not a proof that ingestion is random. A bias that never changes (an employer or sector the database never ingests) cannot show up in a comparison of mixes. The test compares the whole mix, so it has little power for small clusters, and emerging occupations are small. lesjeudis and jobs.de give weak evidence because there are few jumps to test. The thesis states the result in these terms and the checks as a limitation.

**The title-less block (jobbland).** No posting taken before 2025-12-09 lacks a title. In the 14 days from 2025-12-09, 61% of postings taken have none. By month the share is 44% in December 2025 (54% weighted) and 13% in January 2026 (10% weighted), and 0% in every other month; 1,389 of 53,959 postings in all. Samples of clusters 171 and 168 show that these postings are ordinary jobs: cluster 171 holds varied occupations (GIS engineer, software tester, team leader, compliance specialist, quality technician, a head of department), and cluster 168 holds introductions of municipalities and regions. The two clusters exist because the first 150 characters of a description are mostly employer boilerplate or a recruiter's opening line, not a description of the job. So the shift of the cluster mix at 2025-12-09 is an artefact of how title-less postings are embedded, not a change in the occupations. What changed is that the postings arrive without a title. The channel flags are not affected: the Month 3 tagger reads title and description, so title-less postings were tagged from the description. Title-less postings are therefore kept in the channel analysis. For occupation clusters, the title lens is not valid for them, and a way to give them an occupation is needed (Open items).

**Consequences for the design.** Event analyses are done inside one board and one stable stretch. For jobbland the AccelerateEU (2026-04-22) window runs from 2026-02-01, after the title-less block, with 80 days on each side and monthly periods; it contains no title-less posting, so it does not wait for the title question. The jobbland data before 2025-12-09 form a separate regime. For lesjeudis, the InvestAI baseline (2025-02-11) falls in a thin stretch of sampled days and its coverage per window is checked first. jobs.de has no event baseline. The sector field is not used.

## HHI across NUTS-2 regions

For each cluster and quarter, the Herfindahl-Hirschman Index measures how concentrated the cluster's postings are across regions:

```latex
HHI = \sum_r s_r^2
```

where s\_r is region r's weighted share of the cluster's postings. It runs from 1/R (spread evenly over R regions) to 1 (all in one region). Example: three regions with shares 0.5, 0.3 and 0.2 give 0.25 + 0.09 + 0.04 = 0.38.

- Postings are mapped to NUTS-2 regions of the 2021 classification (Eurostat GISCO polygons): Sweden 8 and Germany 38 regions were all found; for France the polygon file holds 27 regions and 22 received postings. The 22 are the older pre-2016 regions, not the 13 current ones. The 5 without postings are presumably overseas (not checked). The regional mapping uses the posting's own nuts2 field where it exists (jobbland only, 36% of postings), then Swedish counties, then place names learned from those postings, then a GeoNames lookup with the polygons (script 96).
- Postings with a vague location (for example a country name only) are dropped from the HHI and their share is reported next to it, so the reader sees how much was left out.
- HHI is not comparable across countries without normalisation, because the number of regions differs, and it is noisy for small clusters.

**Mapping results (script 96, 11 November).** Shares are of the raw sampled items, duplicates not removed.

| Board | Placed in a NUTS-2 region | Vague or outside, dropped | Unmatched | Regions found |
| --- | --- | --- | --- | --- |
| jobbland.se | 75.7% | 23.5% vague, 0.5% outside | 0.4% | 8 of 8 |
| lesjeudis.com | 99.8% | under 0.1% | 0.2% | 22 mainland regions |
| jobs.de | 98.7% | 0.8% outside, under 0.1% vague | 0.5% | 38 of 38 |

- **jobbland.se.** Only postings whose location names a county carry their own region (36.1%); the county table agrees with that field in all 20,767 postings checked. Towns written without a county are placed from the same town seen with a county (38.8%). The gazetteer route agreed with the own field in only 20 of 51 postings, so it is switched off for Sweden. The 23.5% dropped are bare country names and Nordic-area names; whether this share changes over time or by cluster has not been checked.
- **lesjeudis.com and jobs.de.** Placement relies on the GeoNames gazetteer and the NUTS 2021 polygons. 45.6% of lesjeudis postings and 29.0% of jobs.de postings sit in place names that exist in more than one region; the largest place is taken. I read the 40 busiest such names for each board and found no wrong choice, which is my own reading, not an independent check.
- **Two errors found and fixed.** A shared manual file dropped 665 Berlin postings as outside Germany; manual rows now name their country. Bracket qualifiers such as (Oder) are kept when the qualified name exists, and otherwise an ambiguous bare name is left unmatched instead of guessed.
- **Concentration.** Île-de-France holds 46.4% of placed lesjeudis postings, so HHI is only comparable within a board.

## Why skill dictionaries, not TF-IDF alone

TF-IDF has no time dimension, so it cannot say which terms are growing. It also surfaces words that are not skills, and it does not map Swedish, French and German terms to one concept. ESCO and Lightcast supply a filtered, multilingual vocabulary of skills, so the same skill is counted the same way across languages. Their importance in a posting is still measured by us, by presence per posting and the trend method above. Lightcast API access is needed for the Lightcast skill list (Tracker skills are never mixed with local skills).

**Caveat: ESCO false positives.** The extractor matches sentences to skills at similarity 0.6 or above, and generic or template sentences can match unrelated skills. This can distort the Month 3 skills-per-channel tables. The check has not been run: the diagnostic cell output is pending, and the effect on those tables is untested.

## Open items

1. Run `--coherence-only` for the three boards, read `docs/skill_coherence_<board>.md`, choose the threshold, then rerun D with tag v2.
2. Sensitivity check of the ESCO weight (0.25, 0.5, 1.0) with ARI between runs.
3. Diagnostic for false ESCO matches; if confirmed, remove boilerplate sentences before extraction and check the Month 3 skills-per-channel tables.
4. Fix the rule for selecting 6 to 10 clusters: eligible clusters (share crossing, template and title-less filters), flagged share and its change around the event, and manual reading of the postings (script 98).
5. Verify the named-occupation regex matches (battery in particular).
6. Look at the weekly flagged share for jobbland 2025-Q2 and for lesjeudis to see whether spikes or a few weeks drive the wide week-block intervals.
7. Give title-less postings an occupation for the clusters. The opening 150 characters are mostly boilerplate, so they cannot be used. Proposal: infer a title from the description with the Qwen 7B model on Colab (about 1,400 postings) and validate it on titled postings with the title hidden (agreement with the true title); cluster with the inferred titles and report results with and without them. Decision pending.
8. Read the candidate clusters with script 98 and `--only-flagged` (jobbland 237, 16, 138, 15, 234, 69; lesjeudis 34, 125, 139, 88, 71, 121, 117, 126, 115) to check flag false positives before choosing the 6 to 10.
9. Run script 93 for jobbland from 2026-02-01, monthly, 80-day windows around AccelerateEU. For lesjeudis, check the sampled days per window around InvestAI first (population\_lesjeudis.csv).
10. Time-based check of the late-September 2025 collapse of the lesjeudis flagged share (script 97 compares mix with volume, not with time).
11. Ask Skillab, through the supervisor, how ingestion works and whether sources or fields changed between 2024 and 2026 (sector field in 2025, title-less postings in December 2025).
