# Month 3 methodology: deglobalization lexicon and posting classifier

Oct 28, 2026 · @anton

## Purpose and deliverables

Month 3 builds a lexicon of deglobalization terms, uses it to find relevant postings, has an LLM tag each by channel and intensity, and measures the result on 300 hand-annotated postings. This document fixes the order of work and the assumptions behind it, so the thesis can state them.

The brief asks for four deliverables:

- A final lexicon of 300 to 500 terms, grown from 30 to 50 seed terms with TF-IDF (uni-, bi- and tri-grams) and multilingual-e5 embedding similarity. The supervisor accepted a lexicon of 150 terms instead (27 October 2026).
- A tagged posting dataset: channel and intensity (low, medium, high) for each flagged posting.
- A classifier evaluation report: precision, recall and F1 on 300 annotated postings.
- A prompt template library for the LLM classification.

The method follows the brief's methodological reference, Kavargyris et al. (2025), Algorithms 18(9), 554: an LLM tags the postings, a human-annotated sample validates it, and several models are compared on that sample.

## Status and decisions, 28 October 2026

The tagger is Claude Haiku 4.5 with prompt v8, chosen because it matches the agreed definitions and scores the same as its predecessors within noise. All results below are round-1 development results; the round-2 test is being annotated.

**Decisions since 20 October**

- **Lexicon:** 150 terms, English only, six channels; accepted by the supervisor on 27 October 2026 in place of 300 to 500.
- **Channel definitions:** strategic-sector view, accepted by the supervisor (27 October). Total-defence and security-check boilerplate is removed before matching.
- **Reshoring** (author, 28 October): firms moving production back from abroad. A posting cannot show the earlier offshoring, so the sectors are fixed in advance: space, aerospace, semiconductors and electronic components, and battery production. Wind and solar equipment manufacturing is energy security, never reshoring.
- **Trade compliance** (author, 28 October): routine customs and shipping paperwork, "exports" in a company description and a skill listed as "a plus" are none. Customs-authority staff count only when the duties involve declarations, origin, sanctions or export control.
- **Intensity** (author, 28 October): stays at three levels as defined, not collapsed; channel is the main measure.
- **Models:** Qwen 2.5 7B (Ollama) and Claude Haiku 4.5 (API). Mistral 7B was not run, and a Sonnet run was cancelled to limit cost.
- **Prompt versions:** v6 (customs-authority rule, strategic sectors), v7 (stricter on reshoring, trade compliance and intensity), v8 (reshoring and energy security boundary, 28 October). The annotation guide carries the same wording as the prompt.

**Evaluation design**

Round 1 has 472 annotated postings: 322 lexicon-flagged postings drawn in strata by Qwen's predicted channel, and 150 postings without a lexicon term to measure what the lexicon misses. Its labels were made under the v6 guide and were used to develop the prompts, so its scores are optimistic. Round 2 is a fresh sample of 300 flagged postings, drawn from Haiku v7's strata with every round-1 posting left out, and annotated under the v8 guide. Round 1 used up nearly all rare-channel postings, so round 2 holds only 9 reshoring, 3 trade compliance and no critical materials postings: it tests defense, energy security and the overall relevant-or-not decision, not the rare channels.

**Round-1 results** (F1 per channel; intensity as quadratic-weighted kappa)

| Run | Macro-F1 | Any vs none | Reshoring | Defense | Critical materials | Energy security | Trade compliance | Intensity kappa |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen 2.5 7B, v6 | 0.57 | 0.84 | 0.52 | 0.87 | 0.82 | 0.82 | 0.36 | 0.55 |
| Qwen 2.5 7B, v7 | 0.53 | 0.82 | 0.43 | 0.85 | 0.72 | 0.73 | 0.45 | 0.61 |
| Haiku 4.5, v6 | 0.65 | 0.89 | 0.81 | 0.92 | 0.90 | 0.84 | 0.43 | 0.64 |
| Haiku 4.5, v7 | 0.66 | 0.88 | 0.84 | 0.92 | 0.89 | 0.79 | 0.53 | 0.58 |
| Haiku 4.5, v8 | 0.64 | 0.88 | 0.80 | 0.90 | 0.82 | 0.82 | 0.51 | 0.58 |

Haiku is clearly ahead of Qwen. Among the Haiku prompts the differences are inside the intervals and inside the run-to-run noise (21 of 622 postings changed channel between v7 and v8, against 3% between two runs of the same prompt).

**How to read it**

- Defense, energy security and critical materials are usable. Energy security loses mostly low-intensity sales, recruiting and admin roles at solar and battery firms (17 of 20 missed), which the guide rates low and the model rates none.
- Reshoring is precise (0.93 under v8) with lower recall.
- Trade compliance stays weak: precision about 0.35, recall about 0.89. The model reads "responsible for customs procedures" as compliance work; the guide does not. Report it as a candidate flag.
- Diversification has one annotated posting and cannot be evaluated.
- Intensity is exploratory. The annotator agreed with himself on channel for 43 of 50 postings (86%, Cohen's kappa 0.76), but on intensity only weighted kappa 0.11 (15 postings), below the model-annotator kappa of 0.58.
- Lexicon precision is 0.62; 2% of postings without a lexicon term were judged relevant (interval 0.00 to 0.04).

**Limits to state**

**Round-2 results** (Haiku v8, weighted F1 with 95% bootstrap intervals; 28 October)

| Labels used | Defense | Energy security | Any channel vs none | Intensity (weighted kappa) |
| --- | --- | --- | --- | --- |
| All 300 rows | 0.86 (0.81 to 0.91) | 0.64 (0.50 to 0.79) | 0.84 (0.79 to 0.88) | 0.39 |
| Human rows only (1 to 59) | 0.85 (0.72 to 0.95) | 0.71 (0.41 to 0.99) | 0.84 (0.72 to 0.93) | 0.18 |

Rows 1 to 59 were annotated by the author; rows 60 to 300 were labelled by Claude under the v8 guide, at the author's request, and are marked in the `source` column of the completed sheet. Labeller and tagger belong to the same model family, so the 241 Claude rows are a consistency check, not independent validation, and the thesis must report them as such. The 59 human rows alone are too few for narrow intervals.

Defense is stable across both label sets. Energy security has lower recall (about 0.60): the misses are mostly low-intensity sales, recruiting and administrative roles. Lexicon precision is 0.59 on all rows and 0.66 on the human rows: about 40% of flagged postings are not about any channel. Reshoring (8 postings), trade compliance (1), critical materials (0) and diversification (0) cannot be assessed on this sample. Intensity stays exploratory: Haiku rates most postings medium where the annotator rated them high.

**Tagger for the full corpus: Qwen 2.5 7B with the v8 prompt** (29 October)

Claude Haiku 4.5 scored higher but costs about $3.50 per 1,000 postings, so the author chose Qwen, which runs free on a Colab GPU. Haiku stays in the thesis as the benchmark and as future work if funding allows. Weighted F1 on the 618 annotated postings both models tagged:

| Measure | Qwen v8 | Haiku v8 |
| --- | --- | --- |
| Round 1, defense | 0.87 | 0.90 |
| Round 1, energy security | 0.76 | 0.82 |
| Round 1, reshoring | 0.44 | 0.80 |
| Round 1, macro-F1 | 0.53 | 0.64 |
| Round 2, defense (all rows) | 0.84 | 0.86 |
| Round 2, energy security (all rows) | 0.68 | 0.64 |
| Round 2, reshoring (all rows) | 0.03 | 0.23 |
| Any channel vs none, rounds 1 and 2 | 0.82 and 0.82 | 0.88 and 0.84 |

Qwen is usable for defense, energy security and the relevant-or-not decision. It misses most reshoring postings in round 2 and over-flags trade compliance (precision about 0.25), so reshoring, trade compliance and critical materials are reported as noisy candidate flags, not as measured quantities. Five of 618 answers on the annotated postings, and 9 of 2,792 in the full run, were invalid and are counted as none.

**Full-corpus result** (merged jobbland.se corpus, January 2024 to September 2026)

The corpus holds 53,959 postings after exact duplicates are removed; 2,792 (5.2%) contain a lexicon term and were tagged. Defense is the largest channel, at about 2 to 3% of all postings from September 2024 on, and energy security is about 0.5%. Change in the weighted share of all postings, 90 days before to 90 days after each event, in percentage points with 95% intervals:

| Channel | Critical Raw Materials Act (23 May 2024) | AccelerateEU (22 April 2026) |
| --- | --- | --- |
| Defense | -0.35 (-1.37 to +0.59) | +0.32 (-0.26 to +0.86) |
| Energy security | -0.29 (-0.99 to +0.23) | +0.04 (-0.21 to +0.29) |
| Reshoring | -0.21 (-0.61 to +0.17) | +0.01 (-0.08 to +0.12) |
| Trade compliance | -0.15 (-0.38 to +0.02) | -0.03 (-0.19 to +0.13) |
| Critical materials | -0.13 (-0.33 to +0.05) | -0.08 (-0.15 to -0.02) |

No change is distinguishable from zero except critical materials around AccelerateEU, which moves from 0.08% to 0.00% of postings. That is a handful of postings tagged by the least validated channel, and one interval in 60 excluding zero is what chance would give, so it is not evidence of an effect. The window before the Critical Raw Materials Act is thin (1,447 postings taken, about 2,100 in the population), which is why those intervals are wide. The result is that this tagger and this sample show no measurable shift in any channel around either event; the intervals on defense (about half a percentage point on a 2% share) would show a change of roughly a quarter or more of the share, and smaller changes cannot be ruled out. December 2025 stands out for defense (6.4%, interval 4.9 to 8.2), outside both event windows, and its postings should be checked for a single employer or campaign before the monthly series is described.

**Skill Surge Index** (script 65; 29 October)

The index is the weighted share of postings in a quarter that contain a skill, divided by the same share in a baseline period. The brief's 2019 baseline does not exist in this corpus, which starts in 2024, so two baselines are reported. The pre-shock baseline, January to April 2024 (before the Critical Raw Materials Act), holds 1,018 postings taken, of which 72 contain a lexicon term. The robustness baseline, September to December 2024, holds 10,359 postings taken and 520 with a term, but falls after the first shock.

Index in 2026Q2, lexicon channels (any posting with at least one term of the channel), with 95% intervals:

| Series | Baseline postings: Jan to Apr 2024 / Sep to Dec 2024 | Index vs Jan to Apr 2024 | Index vs Sep to Dec 2024 |
| --- | --- | --- | --- |
| Any lexicon term | 72 / 520 | 0.67 (0.52 to 0.85) | 0.91 (0.78 to 1.05) |
| Defense | 32 / 340 | 1.03 (0.71 to 1.56) | 0.90 (0.75 to 1.06) |
| Critical materials | 16 / 72 | 0.25 (0.14 to 0.54) | 0.63 (0.38 to 1.01) |
| Energy security | 5 / 69 | 1.41 (0.66 to 5.16) | 1.18 (0.77 to 1.78) |
| Trade compliance | 8 / 44 | 0.69 (0.35 to 1.87) | 1.11 (0.67 to 1.82) |
| Reshoring | 12 / 17 | 0.29 (0.15 to 0.71) | 2.62 (1.25 to 6.29) |

The January to April 2024 baseline is too thin to support most of the series: only defense and the any-term total have more than 16 baseline postings, and the model-tagged series have 14 or fewer in every channel. Its "any term" index below 1 may reflect a change in the corpus, not falling demand: posting volume rose from 190 to 410 a month to over 2,000 from May 2024, and the baseline's flagged share (7.6%) is above the corpus average (5.2%). The composition check (script 33) has not yet been run on these months.

Against the September to December 2024 baseline, defense is flat at about 0.85 to 1.2 from 2025Q1 to 2026Q3 (model-tagged defense 0.88 in 2026Q2), with one exception: 2025Q4 reaches 1.76 for lexicon defense (1.36 to 2.25) and 2.16 for tagged defense (1.63 to 2.84), which is the December 2025 spike. In the first half of 2024 defense stood at 0.55 to 0.61 of the late-2024 level, so the rise happened before the baseline. Critical materials sits below the late-2024 level after 2025Q1 (0.26 to 0.69), led by battery terms, a decline that has not been checked against any outside source. Energy security and trade compliance show no consistent pattern from 2025Q1 on: two of 28 intervals (lexicon energy security in 2025Q1 and 2025Q3, at 1.58 and 1.73) exclude 1, close to what chance produces. Both channels were lower in the first half of 2024, in the quarters before the baseline (lexicon trade compliance 0.22 to 0.40 of the late-2024 level). Reshoring terms stand at 2.6 to 2.9 times the late-2024 level in 2026Q2 and 2026Q3, but the baseline holds 17 postings and the model-tagged series (4 baseline postings, a tagger that misses most reshoring) cannot confirm it, so this is a lead to check by reading the postings, not a finding.

Two cautions apply to every term-level result. Terms that occur together in the same postings move together (for example, the defense terms all dip in 2025Q2), so the term indices are not independent evidence. Quarters that contain baseline days are close to 1.00 by construction and are marked in the report.

- One annotator; round-1 labels precede the final definitions.
- Claude Haiku ran with default sampling, not temperature 0.
- Rare channels have 15 to 20 annotated postings, so their intervals are wide.
- The corpus is an English-language slice of jobbland.se and the lexicon is English only. Job ads have likely been machine-translated to English first.

## Update, 31 October 2026: v9 tagging, lexicon v2 and other job boards

Defense is the only channel with enough validated volume for an event analysis; energy security is indicative only (human-only F1 0.62, interval 0.43 to 0.80), and reshoring, trade compliance and critical materials stay descriptive. The decisions below replace the 28 and 29 October statements where they differ.

- Critical materials follows the EU definition (supervisor-approved): materials on the lists of Regulation (EU) 2024/1252, strategic (Annex I) and critical (Annex II). Platinum-group metals count; gold and silver do not. Steel and general mining (iron ore, base-metal mining) are outside it. The Critical Raw Materials Act (23 May 2024) is therefore reported as descriptive only: the metal terms of the definition are almost empty in the corpus.
- Lexicon v2: 154 terms (158 before 31 October, see the energy-security paragraph below), the original 150 plus seven energy and battery terms and "battery recycling". "Smart grid", "solar cell manufacturing" and "wind turbine manufacturing" were considered and dropped.
- Tagger: Qwen 2.5 7B with prompt v9, plus one rule (script 71). A critical-materials tag is removed unless the posting contains an EU-anchored term (critical raw materials, rare earths, strategic raw materials, battery materials, lithium, raw materials security, critical metals, strategic resource, battery recycling). The prompt alone did not stop the model from labelling LKAB and Boliden postings as critical materials. A mining sector now maps to none. The tags file is tags\_qwen2.5\_7b\_tagging\_v9r.
- Skill Surge Index baseline: September to December 2024. January to April 2024 is too thin (see the 29 October paragraph, which reports both).
- Tracker tags (skills, sectors) stop in autumn 2025 on jobbland.se, so no comparison crosses that boundary. Skills extracted locally with the ESCO skill extractor (one threshold, 0.6, for all months) are never mixed with Tracker skills. The extractor is accepted as a diagnostic; the sector classifier is rejected.
- Scope of sources: any job board that can help, not only jobbland.se.

**Scores of the v9 tags (Qwen 2.5 7B, prompt v9 with the script 71 rule) against v8.** The channels that carry the analysis did not move: defense stays at 0.83 to 0.85 and the relevant-or-not decision at 0.79 to 0.82. Weighted F1, scored on the same annotated postings as before (round 1: 472; round 2: 300 rows):

| Measure | Qwen v8 | Qwen v9 |
| --- | --- | --- |
| Round 1, defense | 0.87 | 0.85 |
| Round 1, energy security | 0.76 | 0.68 |
| Round 1, reshoring | 0.44 | 0.52 |
| Round 1, critical materials | 0.72 | 0.18 |
| Round 1, macro-F1 | 0.53 | 0.44 |
| Round 1, any channel vs none | 0.82 | 0.79 |
| Round 2, defense | 0.84 | 0.83 |
| Round 2, energy security | 0.68 | 0.74 |
| Round 2, reshoring | 0.03 | 0.03 |
| Round 2, macro-F1 | 0.48 | 0.40 |
| Round 2, any channel vs none | 0.82 | 0.82 |
| Intensity, quadratic-weighted kappa (round 1, round 2) |  | 0.60, 0.52 |

Energy security moves in opposite directions in the two rounds, inside wide intervals (round 1: 0.56 to 0.78; round 2: 0.58 to 0.87), so it is noise, not an effect of the prompt. The reshoring samples are 18 and 8 postings. The fall in macro-F1 comes mainly from the critical-materials row and from channels with one or no annotated posting in round 2.

**Critical materials, re-judged.** The 20 annotated critical-materials postings of round 1 were labelled under the old definition, which counted LKAB and Boliden. The re-judgement under the EU definition covers 14 of them: the v9 tags give 2 true positives, 0 false positives, 2 false negatives and 10 true negatives. Five Boliden postings were left unjudged (all tagged none) and one is unclear. The two misses contain only the term "precious metals", which does not by itself make a posting critical-materials. With 14 judged postings the channel is reported as counts, not as an F1. It needs a new human sample under the EU definition before it gets a score.

**Critical materials, new human sample (31 October).** The author labelled 98 postings under the EU definition: all 58 flagged postings with an EU-anchored term and 40 drawn at random from the other 276 postings that carry a critical-materials term of lexicon v2 (334 in all). Twelve are critical materials (10 anchored, 2 other), 6 are unclear. The v9 tags with the term rule mark 11 postings as critical materials, all in the anchored stratum: 6 agree with the author, 5 do not (two none, two reshoring and one energy security by the author's label). Of the author's 12, the tagger finds 6; the 2 in the other stratum (both with battery terms: a control and automation engineer and a process engineer) are both missed. Read as counts: in the anchored stratum precision is 6 of 11 and recall 6 of 10, and the estimate for all 334 postings rests on two postings in the unanchored stratum. Half of the 6 misses are doctoral or postdoctoral positions in battery and geochemistry research, where the channel is a judgement call. The same postings also show the older-label problem: of 14 postings labelled in round 1, 5 now carry a different label (three critical materials became unclear, two none became reshoring).

**Full corpus with the v9 tags (lexicon v2, baseline September to December 2024).** No channel shifts significantly around either event; every interval spans zero. Change in the weighted share of postings, 90 days before to 90 days after, in percentage points:

| Channel | Critical Raw Materials Act (23 May 2024) | AccelerateEU (22 April 2026) |
| --- | --- | --- |
| Defense | -0.41 (-1.34 to +0.51) | +0.40 (-0.21 to +0.98) |
| Energy security | +0.33 (-0.64 to +1.16) | +0.03 (-0.25 to +0.29) |
| Reshoring | -0.12 (-0.61 to +0.33) | +0.04 (-0.02 to +0.11) |
| Trade compliance | -0.16 (-0.35 to +0.00) | -0.03 (-0.18 to +0.13) |
| Critical materials | -0.10 (-0.29 to +0.06) | -0.03 (-0.09 to +0.00) |

Critical materials is essentially zero in every month (0.15% or less) after the EU definition and the term rule, which is the expected result; the channel is too rare for a time series.

**December 2025.** Defense reaches 6.67% of postings in December 2025, against 2.1% to 3.3% in the neighbouring months. The diagnostics cannot attribute it to the European Defence Industry Programme (adopted 8 December 2025): collection restarts around 10 to 18 December 2025, and mid-December is seasonally high. The difference-in-differences against 2024 is +1.04 points (-0.53 to +2.64), not significant; mid-December 2025 against mid-December 2024 is +3.38 points (1.23 to 5.49).

**Skill Surge Index (September to December 2024 = 1.00).** Model-tagged defense is 2.21 (1.64 to 2.94) in 2025Q4, the December effect, and 0.89 to 0.99 in 2026Q1 to Q3. Model-tagged energy security falls to 0.38 (0.24 to 0.57) in 2026Q1 and 0.63 (0.40 to 0.94) in 2026Q3, while the lexicon series for energy security reads 1.56 (0.98 to 2.49) in 2026Q3. The two disagree, which fits the tagger's weak energy-security recall (0.55 in round 1). The model-tagged reshoring and critical-materials series before September 2024 rest on baselines of 6 and 2 postings and are not interpreted. The index tables above that use the January to April 2024 baseline are superseded by this baseline.

**Skills per channel (script 70).** ESCO skills extracted locally from every posting at one threshold (0.6, all months; about 5 to 6 skills per posting, the same volume as the Tracker tags). For each channel the report gives the skills with the highest lift (share of the channel's postings carrying the skill divided by its share in all postings), and the share of that skill's postings that sit in the channel ("specific"). Skills with fewer than 5 postings are not listed.

| Channel (postings taken) | Most specific skills | Reading |
| --- | --- | --- |
| Defense (1,239) | develop defence policies, manage military logistics, military drill, manage troop deployment, unmanned air systems, signals intelligence | 62% to 100% of the postings with these skills are in the channel; a clean profile |
| Energy security (447) | nuclear plant safety precautions, wind turbine maintenance, nuclear energy, wind energy, solar products and energy | 26% to 63% specific; common skills are generic (Swedish, project management) |
| Trade compliance (126) | customs compliance for cargo (80%), international trade (36%), check shipments | the most specific skills match the channel definition |
| Reshoring (63) | battery design (39%), aerospace engineering (25%) | matches the fixed sectors; too few postings for more |
| Critical materials (11) | none reaches 5 postings | no table |

The before and after tables around AccelerateEU rest on 5 to 10 postings per skill (for example defense, "identify digital competence gaps": 5 before, 5 after, shares 0.1% and 2.1%), so they are signals to follow up, not results.

**Other job boards: three events checked, none shows an effect.** Both boards were downloaded with script 52 (day-stratified, full text). The jobs.de event is reported as a finding about the data; the two lesjeudis.com events are monthly comparisons with a control (the AI Act result follows the table).

| Event and board | Data coverage | Finding |
| --- | --- | --- |
| EU definitive tariffs on Chinese electric vehicles, 30 October 2024 (timeline id 29), jobs.de | Daily postings from 16 August 2024 to 17 March 2025; gaps from 18 March 2025 and nothing after April | Not interpretable. The composition screen is weak: postings fall from 8,175 in October 2024 to 1,690 in January 2025, tag fill dips to 71% for sectors in January and February, and one sector (postal activities) goes from 11.6% to 0.6% of the sample. Health and education postings rise from 5.8% to 10.8% (24.7% in March) while vehicle, transport and manufacturing titles fall together. An exploratory count of German electric-vehicle terms inside automotive and manufacturing postings (care excluded) falls from 7.5% to 2.1%, but the cohort itself grows from about 2% to 8% to 10% of postings around 8 November 2024 and the pre-event share rests on 93 postings. Dropped as an event analysis, as agreed. |
| EU InvestAI initiative, 11 February 2025 (timeline id 63, added 31 October 2026), lesjeudis.com | Daily postings from 11 August 2024 to 16 February 2025; then 7 days with postings (7, 16 and 17 March; 5 to 8 April) and none on the other days until 30 April | No effect distinguishable from the trend. Only 13 days follow the event (11 February to 30 April; 954 postings sampled), against 5,912 sampled in November to January. The full-text share of AI and machine-learning terms is 19.5% before and 24.9% after (+5.4 points, 95% interval -1.2 to +11.8; cloud and data centre +9.4, control +5.0). The same rise appears before the event: January to 10 February against November to December is +5.9 points (+1.9 to +9.9). So the post-event step is no larger than the pre-existing trend. An earlier title-only test that counted all of February as after the event was wrong and is withdrawn. After the gap the board's mix changes (control and cloud shares also rise), so March and April alone are not comparable with the months before. Tag fill is 93% to 100% throughout. |

InvestAI is a digital-sovereignty measure (EUR 200 billion of AI investment announced at the Paris AI Action Summit, including EUR 20 billion for AI gigafactories), not a trade-policy measure. The timeline lists it under diversification, the nearest of the six channels, and the author accepted that label on 31 October 2026.

The AI Act obligations for general-purpose AI models (2 August 2025) were tested on lesjeudis.com as a monthly comparison, May and June 2025 against August and September 2025 (July has 8 days with postings and is left out; there are no postings from 29 July to 7 August). The full text of 5,879 sampled postings was searched for AI and machine-learning terms (including the standalone words AI and IA) and, separately, for cloud and data-centre terms; the control is developer and project-role titles. The share of postings with AI terms is 33.3% before and 32.8% after (difference -0.5 points, 95% interval -4.6 to +3.7); cloud and data centre 41.3% to 35.9% (-5.3, -13.0 to +1.0); control 27.0% to 27.2% (+0.3, -3.5 to +3.7). No change is detectable, and the intervals would show a shift of about 4 points or more in the AI share. The AI share is stable at 32% to 34% in every month from May to September 2025, so the restart on 8 August did not move it. The composition check (script 33, May to July against August and September) passes: occupation, sector, experience level, description length and title words are all within normal month-to-month drift, and that drift is low (0.007 to 0.061); tag fill is 96% to 100% in every month. Only posting type shifts beyond drift (0.018 against 0.010), a small change. The result is a clean null on this board. Comparisons that cross the February to April 2025 collection gap are not valid: the AI share jumps from 17% to 24% before the gap to 33% after it, a change of board mix, not of demand.

**Human-only scores of round 2 (31 October 2026).** Scoring only rows labelled by the author removes the circularity of the Claude-labelled rows. On the first 59 human rows the scores equal v8 (defense 0.82, energy security 0.75). On 155 human rows (the 59, plus rows 60 to 150 and five from the critical-materials sheet; v9 tags with the script 71 rule) defense holds and energy security falls:

| Channel | n | Precision | Recall | F1 |
| --- | --: | --: | --: | --: |
| Defense | 55 | 0.75 (0.63 to 0.86) | 0.89 | 0.81 (0.73 to 0.89) |
| Energy security | 21 | 0.47 (0.26 to 0.73) | 0.59 | 0.52 (0.32 to 0.75) |
| Reshoring | 6 | 1.00 | 0.04 | 0.07 |
| Critical materials, trade compliance, diversification | 1 each | not estimable |  |  |
| Any channel vs none |  | 0.73 | 0.83 | 0.78 (0.70 to 0.85) |

Lexicon precision (flagged postings about a channel at all) is 0.62. Intensity agreement where channel agrees: exact 0.60, quadratic-weighted kappa 0.35; the tagger rates 17 of 55 postings the author rated high as low. The macro-F1 of 0.23 is an artifact of channels with one to six postings and is not reported as a result; those channels are reported as counts. Energy security scored 0.74 on the Claude-labelled round 2 rows, so that number was optimistic.

**Energy security: false positives and the lexicon change.** In the human-labelled sample the tagger assigned energy security to 29 postings (unweighted): 17 correct and 12 wrong, all 12 labelled none by the author. Nine of the 12 are Vattenfall Eldistribution and Skanska grid-operation roles matched by "secure electricity", "safe electricity", "stable electricity" and "safe and stable electricity", which describe running the ordinary grid; the others are nuclear decommissioning at Ringhals, "produced in Sweden" in an asset-manager ad, and an electrician matched on "batteries". Four postings the author labelled energy security were missed (nuclear in medical, radiation-measurement and marketing roles, and a solar and battery seller). The four electricity terms were removed from lexicon v2 (158 to 154 terms, change log in lexicon\_v2/CHANGELOG.md). The decision uses the same rows that were scored, so the corrected score will be reported beside the 0.52 and checked on rows 151 to 300. Channel shares and the Skill Surge Index for energy security were computed with the 158-term lexicon and are indicative until the corpus is re-flagged.

**Labelling rules fixed during annotation.** Cyber-sovereignty (for example AI-driven cybersecurity to reduce dependence on the US) is labelled none, or defense where the ad is defense work, with the note cyber-sovereignty; one such posting was first labelled reshoring and corrected. Reshoring means firms moving production back from abroad, in the fixed sectors (space, aerospace, semiconductors and electronic components, battery production). Ads for precious metals are critical materials only when the ad concerns a metal on the EU lists (platinum-group metals yes; gold and silver no). Critical-materials sample (98 postings, stratified by EU-anchored term): anchored stratum precision 6/11 and recall 6/10; two critical-materials postings in the other stratum were missed (battery-term roles). The sample design differs from rounds 1 and 2 and the five rows used in the 155 are counted once; its figures are counts, not population estimates.

**All 300 round-2 rows, and the text the annotator saw (1 November 2026).** The annotation sheets showed the first 1,800 characters of each description; the tagger reads 3,000 plus passages around matched terms further in. For 158 of the 300 rows at least one matched term lies only after character 1,800 (script 74), so the author could have labelled without seeing why the lexicon flagged the posting. Those 158 rows were re-read with the full text and relabelled where the text changed the judgement. Scores of the v9 tags with the 154-term lexicon and the script 71 rule:

| Measure | As first labelled (1,800 characters, 300 rows) | After the full-text check (300 rows) | Rows that were fully visible only (142 rows) |
| --- | --: | --: | --: |
| Defense F1 (precision, recall) | 0.82 (0.76, 0.88) | 0.88 (0.88, 0.87) | 0.84 (0.83, 0.85) |
| Energy security F1 (precision, recall) | 0.66 (0.75, 0.58) | 0.62 (0.75, 0.52) | 0.67 (0.77, 0.59) |
| Any channel vs none, F1 | 0.81 | 0.85 | 0.79 |
| Lexicon precision | 0.61 | 0.71 | 0.60 |
| Intensity, quadratic-weighted kappa | 0.36 | 0.31 | 0.28 |

The figures after the full-text check are the ones to report; the first column shows what the shorter view cost (defense precision 0.76 against 0.88, lexicon precision 0.61 against 0.71). The 142 fully visible rows are not a random subset, so that column is a check and not an estimate. Intervals: defense 0.84 to 0.92 after the check; energy security 0.43 to 0.80 (n = 43), so the channel stays indicative. Reshoring is found almost never (recall 0.01, n = 11); critical materials, trade compliance and diversification have 0 to 2 postings and are counts. The energy-security F1 of 0.52 (155 rows, lexicon of 158 terms) and the 0.62 to 0.66 above are not like for like: the rows differ, and the removal of the four electricity terms also changed the result; the two effects are not separated. Intensity remains weak: the tagger rates many high-intensity postings as low (33 of 110 after the check).

**"Defense" in doctoral contexts (rule applied 1 November 2026).** The bare term "defense" also matches the academic defense of a doctoral thesis ("has documented research work after a defense", "for the position of chief physician, a public defense is also required"), mostly in university and hospital ads and usually late in the text. Among the 155 labelled rows of the earlier sample, 56 were flagged by "defense" alone; of the 26 of those that carry a label, 15 are none. Script 75 now ignores "defense" when every occurrence in a posting is academic (preceded by public, doctoral, thesis, dissertation, PhD or "after a", or followed by "of thesis", or next to a doctoral word and not followed by a sector noun). It affects 27 postings in the whole corpus, all postdoc, doctoral-student, physician and university-administration ads, and all 27 were read and are correct; none had another lexicon term, so all left the flagged set. The effect on the series is therefore negligible. The rule does not explain most of the false flags of the bare term: the other labelled none rows flagged by "defense" alone are not academic and are handled by the tagger, not the lexicon. The scores of the sample do not move because the sample rows stay on the sheet; the flagged-set precision after the rule has not been estimated.

**Round 1 rescored with the final tags (1 November 2026).** Tags: v9 with the script 71 rule, lexicon of 154 terms, PhD-defense rule; 472 postings labelled under annotation guide v6 and lexicon v1. Defense F1 0.85 (0.76 to 0.92; precision 0.79, recall 0.93), reshoring 0.52, critical materials 0.18 (precision 1.00, recall 0.10), trade compliance 0.42 (precision 0.27, recall 0.95, n = 15), any channel vs none 0.78, macro-F1 0.43, intensity kappa 0.61. These match the v9 scores of 31 October except energy security, which falls from 0.68 to 0.61 (precision 0.85, recall 0.47, n = 74). The likely cause is the removal of the four electricity terms: round 1 was labelled under guide v6, which may count grid-operation roles as energy security, while the round-2 labels (current guide) do not. This has not been checked. Three model answers in round 1 are invalid and are scored as wrong. Energy security therefore stays indicative: round 1 gives 0.61 and round 2 (full-text labels) 0.62.

**Limits added by this update**

- The 618 annotated postings were drawn under lexicon v1; the v9 scores reuse them, so they say nothing about the seven terms added in v2.
- Under the v9 tags the critical-materials channel holds 11 postings in the whole corpus (about 100 in the population). It is reported as counts, and its time series is not interpreted.
- Local skill extraction uses one threshold (0.6), chosen to match the volume of the Tracker tags in the probe months. Skill-level results (skills per channel, before and after tables) rest on 5 to 10 postings per skill.
- The jobs.de and lesjeudis.com downloads have collection gaps (lesjeudis.com almost empty after 16 February 2025), and their composition screens show high month-to-month drift in experience level and title words. Shares across these gaps are not comparable.

**Next**

1. Round 2: all 300 rows are human-labelled and scored under lexicon v2 with 154 terms, with and without the full-text check (see the 1 November paragraph); the PhD-defense rule is applied (27 postings)
2. Full corpus tagged with Qwen v9 and the script 71 rule, channel shares computed (script 64); the December 2025 defense spike cannot be attributed to the Defence Industry Programme (see the 31 October update)
3. Sector classifier: rejected by the author; it is not built.
4. ESCOX accepted as a diagnostic; local skills at threshold 0.6 are used for skills per channel and never mixed with Tracker skills. Open: a new human sample for critical materials under the EU definition, the InvestAI framing for the supervisor, and the supervisor wording for the two dropped board events.

## Data and what it supports

Every step uses one corpus: the day-stratified download of jobbland.se postings for January to August 2026 (script 52), 22,638 postings before de-duplication. The skill, occupation and sector tags are empty in 2026, so everything rests on the title and description text.

Exact duplicate descriptions are dropped (5.5% of the sample), and each posting carries a day weight (the day's total postings divided by the postings taken that day) that scales sample counts to the month's population.

The corpus is an English-language slice, not the Swedish labour market. About 98% of the postings are in English, and titles are dominated by municipality, region, nurse, teacher and manager roles. Results describe that slice. The 2024 sources from Months 1 and 2 (other boards and countries) are not used in this step.

## Ordered steps

Sixteen steps, in this order. Steps 1 to 14 are done for the first annotation round; the second round, on a fresh sample, is being annotated (see Status and decisions). The lexicon is frozen at step 7 and the prompt at step 8, before any posting is annotated, because the annotation sample depends on both.

| # | Action | Who or script | Where | Output |
| --- | --- | --- | --- | --- |
| 1 | Download the day-stratified corpus and check that its composition is stable month to month | scripts 52, 51 | laptop (done) | data/raw/corpus\_jobbland.se\_2026-01\_2026-08.jsonl |
| 2 | De-duplicate and attach day weights (automatic in every later script) | corpus\_io.py | any | none: done on load |
| 3 | Review the seed list: 51 terms after the author's revision of 20 October, 13 of them the brief's examples. Keep, cut or add; decide whether to add task-language terms | author | by hand | lexicon/seed\_lexicon.csv |
| 4 | Count how often each seed term occurs and surface TF-IDF n-grams that co-occur with them. Stop point: if fewer than 50 postings contain a seed term, widen the seeds or the corpus before step 5 | script 55 | Colab or laptop | docs/lexicon\_seed\_coverage.md, data/lexicon/candidates\_tfidf.csv |
| 5 | Find phrases close to the seeds with multilingual-e5-base embeddings and FAISS | script 56 | Colab, GPU | data/lexicon/candidates\_embedding.csv |
| 6 | Review both candidate sheets: put 1 under keep and one channel for each term to add | author (hours) | by hand | reviewed sheets |
| 7 | Build the lexicon (150 terms, accepted by the supervisor on 27 October 2026) and freeze it with a date | script 57 | any | lexicon/lexicon.csv, docs/lexicon\_summary.md |
| 8 | Fix the channel and intensity definitions. Pilot: annotate 20 postings that are not in the 300, revise the definitions once, then freeze | author, supervisor | by hand | prompts/tagging\_v1 (or v2), docs/tagging\_annotation\_guide.md |
| 9 | Flag postings with the frozen lexicon and tag them with each model: Qwen 2.5 7B (Ollama, temperature 0) and Claude Haiku 4.5 (API, default sampling); Mistral 7B was not run | script 58 | Colab, GPU | data/tagged/tags\_\<model>\_\<prompt>.jsonl |
| 10 | Second detector for the residual error: tag a random subsample of the unflagged postings with the same model, so the sample can reach relevant postings the lexicon missed | script 58 (extension needed) | Colab, GPU | tags for the unflagged subsample |
| 11 | Draw the 300 postings: strata by predicted channel among flagged postings, plus strata from step 10 | script 59 (extension needed) | any | annotation sheet, hidden key |
| 12 | Annotate blind, text only, in sittings of up to about 100, with the date of each sitting in the first row's note | author (3 to 4 hours) | by hand | filled sheet |
| 13 | After at least three days, annotate 50 of them again | author | by hand | pass-2 sheet |
| 14 | Score each model: precision, recall and F1 per channel with intervals, intensity agreement, lexicon precision, residual error, your consistency | script 60 | any | docs/tagging\_results.md |
| 15 | Choose the model with the best macro-F1 and keep its tags as the tagged dataset | author | by hand | tagged posting dataset |
| 16 | Write up: lexicon completeness paragraph (residual error from step 14), limits, supervisor note | author | by hand | report section |

A parallel track is on hold: the 400-posting sector validation (manufacturing, metals) is annotated, but the sector classifier waits until Month 3 is finished. It does not feed steps 1 to 16.

## Assumptions

Thirteen assumptions underlie the steps. Two are untested (A2 and A7), one is still a draft (A8), and step 4 tests the most consequential one, A2.

| # | Assumption | Status | Checked at |
| --- | --- | --- | --- |
| A1 | The corpus is an English-language slice of jobbland.se, dominated by public-sector and care roles; results describe that slice | Known (98% English) | Profiling, done |
| A2 | Postings describe deglobalization-related work in task and skill terms (customs declarations, export licences, sanctions screening) more than in policy terms (friend-shoring, strategic autonomy, China plus one) | Untested | Step 4 |
| A3 | A posting is tagged only if it contains a lexicon term; what the lexicon misses is the residual error named in the brief's lexicon-completeness limitation | By design | Steps 10 to 14 |
| A4 | De-duplication and day weights make the sample representative of each month; only exact duplicates are removed and the population is treated as distinct texts | Partly checked (no stability flags, Jan to Aug) | Stability check, done |
| A5 | The author's annotation is the reference; there is one annotator, whose consistency is measured by repeating 50 postings | By design | Steps 13, 14 |
| A6 | Annotation and models use the posting text only. Outside knowledge of an employer is not used, and is marked in the note when it was | Rule | Step 12 |
| A7 | LLM answers are repeatable at temperature 0 with a fixed seed, and the model version is pinned (record the Ollama model digest). This was not possible for Claude Haiku: the installed API package rejected the temperature argument, so it ran with default sampling; two runs of the same prompt gave the same channel for 97% of postings | Untested | Re-run a sample at step 9 |
| A8 | The channels come from the author's event timeline. The three intensity levels come from the brief; their definitions are the author's draft | Draft | Step 8 |
| A9 | No pass/fail threshold: models are compared and reported with intervals, as in Kavargyris et al. The 0.80 and 0.70 thresholds in the earlier sector protocol were not in the brief and are dropped | Decided | Step 14 |
| A10 | Strata of the annotation sample are defined by one model's predictions; weights come from the sampling design, so the other models can be scored on the same sample | By design | Step 14 |
| A11 | Embedding similarity only proposes candidate terms; the author decides membership and channel | Rule | Step 6 |
| A12 | The lexicon is English only; the Swedish postings (about 2% of the corpus), and Greek and other languages, are out of scope in this step | Scope | n/a |
| A13 | Everything runs on Google Colab with data on Google Drive; employer text is kept out of git | Decided | All steps |

## What the evaluation measures

Every measure is computed against the author's annotation, on weighted postings, with 95% bootstrap intervals that resample inside each stratum. The population matters for each one, so each row names it.

| Measure | Population | Definition |
| --- | --- | --- |
| Channel precision | Lexicon-flagged postings | Of the postings the model put in a channel, the weighted share the annotator also put there |
| Channel recall | Lexicon-flagged postings | Of the postings the annotator put in a channel, the weighted share the model found |
| F1, macro-F1 | Lexicon-flagged postings | Harmonic mean of precision and recall; macro-F1 averages it over the channels present in the annotation, and is the rule for choosing a model at step 15 |
| Any channel against none | Lexicon-flagged postings | The same measures after merging all channels: does the posting relate to deglobalization at all |
| Lexicon precision | Lexicon-flagged postings | Share the annotator judges relevant (not none): how often a lexicon match is a false match |
| Residual lexicon error | All postings, from the unflagged strata of steps 10 and 11 | Share of relevant postings that contain no lexicon term. This is the error the brief's limitation text says the 300 postings measure; a sample of flagged postings alone cannot show it |
| Pipeline recall | All postings | Lexicon recall combined with classifier recall |
| Intensity agreement | Postings where model and annotator agree on a channel other than none | Exact agreement and quadratic-weighted kappa on low, medium, high |
| Annotator consistency | 50 postings annotated twice | Cohen's kappa for channel, weighted kappa for intensity |

Postings the annotator marks unclear are left out and their share is reported. A posting the model answers with invalid output counts as a wrong prediction.

## Open decisions and differences from the brief

These were the open decisions on 20 October. The section Status and decisions records how each was settled; the table keeps the original options for the record.

| Decision | Options | Recommendation |
| --- | --- | --- |
| Design of the residual-error check (step 10) | (a) Tag every unflagged posting with the LLM: complete, but about 20,000 postings. (b) Tag a random subsample (for example 4,000) of the unflagged postings and sample from its strata: cheaper, weighted back. (c) Annotate a random unflagged sample only: cheapest, but if relevant postings are rare it can only bound their rate | (b), decided after step 4 shows how many postings are flagged |
| Seed list (step 3) | Keep as drafted (policy terms from the brief and the timeline), or add task-language seeds | Decide after the coverage report of step 4 |
| Intensity definitions (step 8) | The draft in the annotation guide: high is the main subject of the role, medium is one of several duties, low is a passing mention | Confirm with the supervisor, then pilot on 20 postings |
| Models (step 9) | Qwen 2.5 7B and Mistral 7B (named in the brief), plus optionally Llama 3 8B, the model the paper used | The two from the brief; add the third only if time allows |

Where this document goes beyond or differs from the brief:

- The brief fixes the three intensity levels but does not define them; the definitions are the author's.
- The categories none and unclear are additions, needed to measure false lexicon matches and undecidable postings.
- The brief evaluates on 300 annotated postings. Here they are drawn in strata and weighted, so that rare channels have enough postings, and they include unflagged postings, so that the lexicon-completeness limitation is measured and not only stated.
- The brief lists spaCy for lemmatization. Matching here uses regular expressions with plural, hyphen and spelling variants instead, which is simpler but less general.
- The sector classifier (manufacturing, metals) is outside the brief and on hold.

## Running on Google Colab

A GPU runtime is needed only for steps 5, 9 and 10; the others run on any runtime. Choose Runtime, Change runtime type, GPU.

- **GPU:** a T4 (16 GB) is enough for the e5 embeddings and for 7B models in 4-bit form through Ollama (about 5 GB). An L4 (24 GB) or A100 (40 GB) tags faster. Colab does not guarantee a given GPU, so availability depends on the plan and on demand. The paper used an A100 with high RAM.
- **RAM:** if steps 4 or 5 stop with a memory error (they count phrases over about 22,000 postings), switch on the High-RAM option.
- **Storage:** Colab's disk is erased when the session ends. Keep the project folder on Google Drive, mount it, and run from it, so every output survives a disconnect. The corpus holds employer text: keep it on Drive, out of git.

Setup cell, run once per session:

```bash
from google.colab import drive
drive.mount('/content/drive')
%cd /content/drive/MyDrive/<project folder>
!pip install -q scikit-learn sentence-transformers faiss-cpu requests
```

Ollama cell, before steps 9 and 10:

```bash
!apt-get -qq install -y zstd
!curl -fsSL https://ollama.com/install.sh | sh
import subprocess; subprocess.Popen(["ollama", "serve"])
!ollama pull qwen2.5:7b
!ollama pull mistral
```

This install recipe is the usual one but has not been run for this project. If it fails, the tagger also has a Claude API backend (the brief allows it).

| Step | Command |
| --- | --- |
| 4 | python -m diagnostics.55\_lexicon\_seed\_coverage\_tfidf |
| 5 | python -m diagnostics.56\_lexicon\_embedding\_expansion |
| 7 | python -m diagnostics.57\_build\_lexicon |
| 9 | python -m diagnostics.58\_tag\_postings --backend ollama --model qwen2.5:7b (then --model mistral) |
| 11 | python -m diagnostics.59\_make\_tagging\_sheet --tags data/tagged/tags\_qwen2.5\_7b\_tagging\_v1.jsonl |
| 13 | python -m diagnostics.59\_make\_tagging\_sheet --pass2 50 |
| 14 | python -m diagnostics.60\_score\_tagging --tags \<tags file> (repeat --tags per model) |

Step 9 saves after every posting. If the session disconnects, run the same command again and it continues where it stopped.

### Details on the code

#### TF-IDF pipeline

The TF-IDF pipeline is 55_lexicon_seed_coverage_tfidf.py. You run it as python -m diagnostics.55_lexicon_seed_coverage_tfidf, and its docstring has the usage notes.

1. It reads the corpus (from script 52) and drops exact duplicates.
2. Postings that contain a seed term form the “flagged” set, and the rest form the “other” set.
3. It counts 1- to 3-grams with scikit-learn’s CountVectorizer (ngram_range=(1, 3), line 177). A second pass at line 181 adds the TF-IDF weights: sublinear tf, idf computed over the whole corpus.
4. It ranks each n-gram by how much more often it appears in flagged postings than in the others. The score is the z-score of the log odds ratio, using a +0.5 correction in every cell. The mean TF-IDF weight in the flagged postings is shown next to it.

Candidates are filtered to those that:
* appear in at least --min-flagged-df flagged postings;
* appear under at least --min-titles distinct titles, so one employer’s repeated advert can’t dominate;
* don’t start or end with a stop word, and don’t contain a seed term;
* aren’t a shorter n-gram sitting wholly inside a longer candidate with almost the same count.

Outputs

docs/lexicon_seed_coverage.md shows the count for each seed term and the counts by month.
data/lexicon/candidates_tfidf.csv is the review sheet you filled in, with the columns term, n, df_flagged, df_other, z, mean_tfidf, titles, example, keep, channel. The sheet contains posting snippets, so keep it out of version control.

#### Expand lexicon using sentence-embedding similarity 

1. Candidate phrases are considered all 1- to 4-word phrases that occur in at least --min-df postings (Apriori counting, corpus_io.frequent_ngrams. We don't allow phrases to cross a sentence, comma or bracket; no stop word at either end). If there are more than --max-candidates, the most frequent are kept.
2. Each seed term and each of its variants are encoded into a numerical vector (a list of numbers). Both the seed terms and candidates receive the same "query: " prefix, in line with symmetric similarity. This is defined in the E5 (Embeddings from Bidirectional Encoder Representations) model, an open-source family of text-embedding models developed by Microsoft Research designed to convert text into dense vector representations for semantic search and retrieval (in line with the project brief). Therefore, both texts are encoded using the same convention because we want to compare two phrases on equal terms. Finally, they are L2-normalised, so each vector is adjusted to have a length (Euclidean norm) of exactly 1.
3. For every seed term the --k nearest candidates by cosine similarity are retrieved (FAISS inner-product index).
(Reference: @misc{johnson2017billionscalesimilaritysearchgpus, title={Billion-scale similarity search with GPUs}, author={Jeff Johnson and Matthijs Douze and Hervé Jégou}, year={2017}, eprint={1702.08734}, archivePrefix={arXiv}, primaryClass={cs.CV}, url={https://arxiv.org/abs/1702.08734},})
4. A candidate is dropped if it is, contains, or is part of a seed term (i.e. we use the same overlap rule as script 55). The rest go to a review sheet, ordered by the best similarity, with the seed it was closest to and the number of different seeds that retrieved it.

It's important to note that nothing is added automatically. In practice, similarity is a reason to look at a phrase, but doesn't not constitute the reason for it to belong to a channel; for example, "customs clearance" will be close to "customs compliance" but doesn't belong to the lexicon.

#### LLM-based classifier to tag each flagged posting by channel and intensity (low / medium / high).

The prompts are built with the following structure:

1. A decision order with the questions asked in sequence.
2. The model must quote its evidence.
3. A fixed JSON output.
4. Temperature 0. At temperature 0 the model always picks its most likely next token, so rerunning the same posting will give the same answer. It is therefore important for reproducibility, and is the default choice for classification. 
5. The lexicon term is described as “a reason to look, never a reason to assign a channel”.

To build the prompt, we used references such as "Törnberg (2023), ChatGPT-4 outperforms experts and crowd workers in annotating political Twitter messages with zero-shot learning", which describes the approach of using an LLM as a classifier against human-labelled data, as well as OpenAI, Prompt engineering guide (https://developers.openai.com/api/docs/guides/prompt-engineering?api-mode=responses).