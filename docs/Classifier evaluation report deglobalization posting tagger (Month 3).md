# Classifier evaluation report: deglobalization posting tagger (Month 3)

Nov 1, 2026 · @anton

## What was evaluated and the result

The tagger is reliable for one channel, defense (F1 0.88 on 300 human-labelled postings), indicative for energy security (F1 0.62) and not measurable for the other four channels, which are reported as counts.

- **Tagger:** Qwen 2.5 7B run locally through Ollama, temperature 0, prompt v9, plus one rule that keeps a critical-materials tag only when the posting contains a term tied to the EU lists of critical raw materials.
- **Input:** the 154-term English lexicon flags a posting; only flagged postings are tagged. Postings without a lexicon term count as none.
- **Corpus:** English-language slice of jobbland.se, January 2024 to September 2026, 53,959 postings after removal of exact duplicates. The tagger and the lexicon were built and evaluated on this board only.
- **Output per posting:** one of six channels (reshoring, defense, critical materials, energy security, trade compliance, diversification) or none, and an intensity (low, medium, high), with a short quote as evidence.
- **Reference labels:** made by the author, by hand, from the annotation guide (`tagging_annotation_guide.md`).

## How the reference labels were made

Three samples were labelled by hand. All are drawn from postings the lexicon flagged, in strata, so rare channels are over-sampled, and every posting carries a weight that maps the sample back to the flagged population.

| Sample | Postings | How drawn | Guide and lexicon at labelling |
| --- | --: | --- | --- |
| Round 1 | 472 | 322 flagged postings in strata of the channel Qwen predicted, plus 150 postings without a lexicon term to measure lexicon misses | guide v6, lexicon v1 |
| Round 2 | 300 | equal numbers per stratum of the channel Claude Haiku (prompt v7) predicted | current guide; all 300 labelled by the author |
| Critical-materials sample | 98 | stratified by whether the posting contains a term tied to the EU lists, plus 40 others | current guide, EU definition |

The critical-materials sample has a different design from the other two and is not pooled with them; its figures are counts. Five of its rows are also among the round-2 labels and are counted once.

**What the annotator saw.** The sheets showed the first 1,800 characters of the description, while the tagger reads 3,000 characters plus passages around matched terms further in. For 158 of the 300 round-2 postings, at least one matched term lies only after character 1,800 (script 74). The author re-read those 158 with the full text and relabelled where the text changed the judgement. Round 2 is therefore scored twice, as first labelled and after the full-text check; the second is the reference. Round 1 was not rechecked.

**Scoring (script 60).**

- Precision, recall and F1 per channel, one channel against the rest, using the sample weights; 95% intervals from 2,000 bootstrap draws that resample inside each stratum.
- "Any channel vs none": does the posting relate to deglobalization at all.
- Lexicon precision: the weighted share of flagged postings that the author labelled as about a channel.
- Intensity: among postings where model and author agree on the channel, exact agreement and quadratic-weighted kappa.
- Postings the author marked unclear are left out (1.2% of the weighted round-2 sample). An invalid model answer counts as a wrong prediction.
- No pass or fail threshold is applied; the numbers are reported with intervals.

## Results

Defense has precision 0.88 and recall 0.87 on round 2 after the full-text check; energy security reaches F1 0.62 with a wide interval; reshoring is almost never found and the other channels have too few postings to score.

**Round 2: 300 postings, final tags (v9 with the rule, lexicon of 154 terms).** Counts n are annotator postings in the channel. Intervals are 95%.

| Channel | n | Precision | Recall | F1 (interval) | F1 as first labelled |
| --- | --: | --: | --: | --- | --: |
| Defense | 136 | 0.88 | 0.87 | **0.88** (0.84 to 0.92) | 0.82 |
| Energy security | 43 | 0.75 | 0.52 | **0.62** (0.43 to 0.80) | 0.66 |
| Reshoring | 11 | 1.00 | 0.01 | 0.03 (0.00 to 0.10) | 0.03 |
| Diversification | 2 | not estimable | 0.00 | 0.00 | 0.00 |
| Critical materials | 1 | not estimable | 0.00 | 0.00 | 0.00 |
| Trade compliance | 0 |  |  |  |  |
| Any channel vs none |  | 0.89 | 0.82 | **0.85** (0.81 to 0.89) | 0.81 |

Lexicon precision is 0.71 (0.66 to 0.77): 71% of flagged postings are about a channel at all; it was 0.61 before the full-text check. Intensity, where model and author agree on the channel: exact agreement 0.52, quadratic-weighted kappa 0.31 (0.18 to 0.44). The macro-F1 of 0.30 is an artifact of channels with one to eleven postings and is not reported as a result.

**Round 1: 472 postings, same tags.** Labelled under guide v6; the figures are not directly comparable with round 2.

| Channel | n | Precision | Recall | F1 (interval) |
| --- | --: | --: | --: | --- |
| Defense | 56 | 0.79 | 0.93 | **0.85** (0.76 to 0.92) |
| Energy security | 74 | 0.85 | 0.47 | 0.61 (0.48 to 0.73) |
| Reshoring | 18 | 0.79 | 0.39 | 0.52 (0.24 to 0.74) |
| Critical materials | 20 | 1.00 | 0.10 | 0.18 (0.00 to 0.42) |
| Trade compliance | 15 | 0.27 | 0.95 | 0.42 (0.24 to 0.60) |
| Diversification | 1 | not estimable | 0.00 | 0.00 |
| Any channel vs none |  | 0.77 | 0.79 | 0.78 (0.71 to 0.84) |

Macro-F1 0.43 (0.36 to 0.58). Lexicon precision 0.62. Lexicon misses: 2% of postings without a lexicon term were judged relevant by the author (0.00 to 0.04). Intensity: exact agreement 0.59, kappa 0.61. Three model answers are invalid and scored as wrong.

**Critical-materials sample (98 postings, EU definition).** Among the 11 postings tagged critical materials in the stratum with EU-anchored terms, 6 were correct (precision 6/11) and 6 of the author's 10 were found (recall 6/10). Two critical-materials postings outside that stratum were missed; both mention batteries. The channel holds 11 tagged postings in the whole corpus (about 100 in the population), so it is reported as counts.

**Qwen against Claude Haiku 4.5 (round 1, prompts v6 and v7).** Haiku scored higher: macro-F1 0.65 on v6 and 0.66 on v7, against 0.56 for Qwen on v6; F1 for any channel vs none 0.89 and 0.88, against 0.84. Qwen was kept for the full run because it runs locally at no cost; Haiku on prompt v9 has not been run.

## Where the tagger goes wrong

Most errors come from words that the lexicon matches in postings about something else; each channel fails in its own way.

- **Defense.** Stable across all samples (F1 0.85 to 0.88). The bare term "defense" is the main source of false flags: of the labelled postings in the first 155 round-2 rows flagged by "defense" alone, 15 of 26 were none. A small part is academic: the defense of a doctoral thesis in postdoc and physician ads (27 postings in the corpus, now removed from the flagged set by a written rule). Saab and similar ads are flagged by company boilerplate such as "defense and security company", not by the employer's name; the tagger judges by duties, so support roles come out low.
- **Energy security.** In the first 155 labelled rows the tagger gave this channel to 29 postings; 17 were right. Nine of the 12 wrong ones were grid-operator roles (Vattenfall Eldistribution, Skanska) matched by "secure electricity", "safe electricity" and similar phrases; the others were nuclear decommissioning at Ringhals, "produced in Sweden" in an asset-manager ad, and an electrician matched on "batteries". The four electricity terms were removed. Misses are nuclear in medical, radiation-measurement and marketing roles, and a solar and battery seller. On round 1 recall is 0.47, probably because that sample was labelled under guide v6, which counts more roles; this was not checked.
- **Reshoring.** Precision 1.00 but recall 0.01 on round 2: the tagger almost never assigns it, probably because the definition (firms moving production back from abroad, in space, aerospace, semiconductors and electronic components, and battery production) is narrow and a posting rarely shows the move. Recall is 0.39 on round 1.
- **Trade compliance.** On round 1 precision is 0.27 with recall 0.95 (n = 15): routine customs and freight work is tagged as compliance. Round 2 has no postings the author labelled trade compliance, so its precision there is 0.
- **Critical materials.** The EU definition removes iron-ore and general mining postings that the first definition counted. After the rule, 11 postings in the corpus carry the tag.
- **Intensity.** The tagger rates intensity lower than the author: of 110 round-2 postings the author rated high, it rated 33 low and 11 medium. Quadratic-weighted kappa is 0.31 on round 2 and 0.61 on round 1.
- **Short view.** Showing the author only 1,800 characters lowered defense precision from 0.88 to 0.76 and lexicon precision from 0.71 to 0.61, because late matched terms were invisible to the labeller. Labels made from a short view understate the tagger.

## Limits and what the results support

The results support using defense as a measured channel and energy security as an indicator; they do not support claims about the other channels or about other boards.

- **One board.** Lexicon, prompt and labels all come from jobbland.se (Swedish employers, English text). The lesjeudis.com and jobs.de boards, also in English, were used only to test three events; no posting from them was tagged or labelled, so the accuracy there is unknown.
- **Small counts.** Reshoring, critical materials, trade compliance and diversification have 0 to 11 labelled postings in round 2, so their scores are not estimable or are driven by a few postings. Energy security has 43 postings and an interval of 0.43 to 0.80.
- **Two guides.** Round 1 was labelled under guide v6 and lexicon v1, round 2 under the current guide. The two rounds are not pooled, and channel scores differ between them (energy security recall 0.47 against 0.52 is close, but reshoring recall 0.39 against 0.01 is not).
- **Tuning on the evaluation sample.** The removal of four energy-security terms was decided on rows that were then scored. The 300-row score includes those rows.
- **Labeller.** One annotator made all reference labels. Agreement between two passes of the same annotator (round 1 pass 2) has not been measured.
- **Employer boilerplate and the diversification channel.** The channel codes what the role does, not what the employer's text says. A posting whose only link to sovereignty is a company paragraph (for example "innovative sovereign solutions" on a pentester or SOC analyst advertisement; the sentence appears on 151 lesjeudis.com postings) is none, in line with the rule for defense employers. A sovereign-cloud or sovereign-AI provider is the exception: there the employer's product is the sovereignty service, so developers and engineers at the provider are diversification, with intensity set by how close the duties are to that service. Pure cybersecurity work is none. This is a coding decision of the author; coding at employer level would raise the channel's counts.
- **Diversification is not yet validated.** Prompt v10 and v11 redefined the channel (reducing dependence on a supplier, country or technology provider, including sovereign cloud and AI). On the 472 round-1 postings v11 gives macro-F1 0.52 against 0.53 for v9, but it tagged 7 ordinary purchasing postings as diversification (none correct); prompt v12 tightens the purchasing rule and is reserved for the final run. The 85 diversification tags on lesjeudis.com under v11 (all but one low intensity) were not yet checked against labels; a 79-posting sample is being labelled.
- **Intensity** is exploratory: kappa 0.31 on round 2.
- **Short view** (see above): round 1 was not rechecked against the full text.
- **Not tested:** Claude Haiku on prompt v9, other open models, and any posting not flagged by the lexicon (apart from the 2% miss rate measured in round 1).

## Deviations from the brief

The brief asks for an evaluation on 300 annotated postings with precision, recall and F1; the report gives these, with the following differences.

| Brief | What was done | Why |
| --- | --- | --- |
| Lexicon of 300 to 500 terms | 154 terms | Only terms the author approved entered; unapproved candidates stay in the proposals files |
| Tagging with Mistral or Qwen, or the Claude API | Qwen 2.5 7B in production; Claude Haiku 4.5 as a benchmark on prompts v6 and v7 | Local and free; Haiku scored higher and is future work on the final prompt |
| One annotated set of 300 | Round 1 (472), round 2 (300), a critical-materials sample (98) | The samples were drawn at different stages as definitions changed; they are scored separately, not pooled |
| Multilingual corpus (Greek and English tools) | English-language jobbland.se only; Swedish terms dropped | The pipeline was validated on one board in English |
| Sector classifier | Not built | Rejected by the author; the ESCO skill extractor is used only as a diagnostic |
| Event analysis for each channel | Defense and, with caution, energy security; other channels as counts | Too few validated postings |

Three board events were examined: the EU tariffs on Chinese electric vehicles (jobs.de, dropped as an analysis because the board's mix changed), the EU InvestAI initiative and the AI Act obligations (lesjeudis.com, tested with keyword groups; no detectable effect). Two further events, the Section 232 tariffs of June 2025 and the EU-US trade deal of July 2025, could not be tested because no board has data for them.

**Why no electric-vehicle reshoring lexicon for jobs.de.** Two reasons. First, collection on jobs.de looks inconsistent: the mix of postings varies considerably from month to month, and the 2.5 months before the EU tariffs on Chinese electric vehicles (30 October 2024) hold only 93 postings, so a before-and-after comparison would mostly measure changes in what was collected. The supervisor agreed to drop the analysis. Second, a probe of electric-vehicle seed terms on the jobs.de corpus (12,243 postings) found 420 postings with an electric-vehicle term, but in the postings read these were employer perks and fleet text (delivery vehicles that are fully electric, charging options for staff cars), not production work. Terms that would identify battery or vehicle production were almost absent: "battery production" twice, "powertrain" once, and no posting with "gigafactory", "battery cell", "cell production" or any reshoring term. jobs.de is therefore tagged with the existing lexicon like the other boards, and no event analysis is reported for it.
