# Classifier evaluation report: deglobalization posting tagger (Month 3)

Nov 1, 2026 · @anton

## What was evaluated and the result

The tagger is reliable for one channel on jobbland.se, defense (F1 0.88 on 300 human-labelled postings, prompt v9), indicative for energy security (F1 0.62) and not measurable for the other four channels, which are reported as counts. The final prompt v12 is not worse than v9 on 620 annotated postings, but on lesjeudis.com its defense tag is only about 54% precise.

- **Tagger:** Qwen 2.5 7B run locally through Ollama, temperature 0, the final prompt v12 plus three post-tagging rules for diversification (R1 to R3, below). The tables in the Results section were measured with prompt v9 and its rule for critical materials (a tag stays only when the posting contains a term tied to the EU lists of critical raw materials); v12 was compared with v9 on 620 annotated postings.
- **Input:** the English lexicon (v7, 188 terms; 154 terms when the round-1 and round-2 samples were scored) flags a posting; only flagged postings are tagged. Postings without a lexicon term count as none.
- **Corpus:** three boards, all with English text: jobbland.se (Swedish employers, January 2024 to September 2026, 53,959 postings after removal of exact duplicates), lesjeudis.com (French employers, August 2024 to September 2025, 18,625 postings) and jobs.de (German board, August 2024 to April 2025, comparison only). The tagger and the lexicon were built and evaluated mainly on jobbland.se; the other two boards are only partly checked (see below).
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

**Round 2: 300 postings, tags of the first full run (prompt v9 with the rule, lexicon of 154 terms).** Counts n are annotator postings in the channel. Intervals are 95%.

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

## Prompt v12, post-tagging rules and the French board

Prompt v12 (lexicon v7, 188 terms) redefines diversification (subtypes supply-side and sovereign-tech), counts employers that offer a European alternative to US cloud providers (Outscale, Scaleway, OVHcloud), and adds a named-project rule for energy security (HYBRIT; Stegra together with Boden). The 7B model did not follow three of its written rules, so three deterministic corrections are applied to the saved answers (script 82), with the model's own answer kept beside each corrected one:

- **R1, supply-side.** A supply-side diversification tag is kept only when the evidence or the text has explicit diversification wording (dual or multiple sourcing, alternative suppliers, reduced dependence, nearshoring). Ordinary purchasing becomes none.
- **R2, SecNumCloud and EUCS.** A posting that names SecNumCloud or EUCS and that the model tagged none or trade compliance becomes diversification (sovereign-tech). It is high when the sentence naming the standard holds a duty verb, so the work is keeping the company or a service in line with the standard, and the standard is one of at most two items; a company paragraph keeps the model's intensity; everything else, including requirement lists and "plus" wording, is low. The author set the high rule for compliance work; the list-size condition is the analyst's and was not tested separately.
- **R3, tool lists.** A provider named only inside a list of tools ("GCP, S3NS, AWS") becomes none.

**v12 against v9 on the 620 annotated postings of jobbland.se** (F1 per channel, one channel against the rest; round 1 and the labelled part of round 2; the sheets were labelled under earlier guides). No channel falls by more than 0.03.

| Channel | F1 v9 | F1 v12 |
| --- | --: | --: |
| Defense | 0.80 | 0.85 |
| Energy security | 0.71 | 0.69 |
| Reshoring | 0.47 | 0.51 |
| Critical materials | 0.69 | 0.74 |
| Trade compliance | 0.51 | 0.50 |

Exact channel agreement is 480 of 620 for v12 against 466 for v9, and invalid answers fall from 3 to 0. The seven ordinary purchasing postings that prompt v11 tagged diversification are none after R1. Diversification itself cannot be scored on these postings: the gold holds 2 diversification labels, and the one posting v12 still tags diversification ("alternative suppliers... nearshoring") is labelled reshoring.

**Diversification on 79 labelled postings (lesjeudis.com).** With the rules applied, precision is 20 of 21 (0.95), recall 20 of 24 (0.83), exact channel agreement 65 of 79, and intensity matches exactly on 15 of 20 (within one level on 17). These figures are optimistic: the author labelled the 79 postings after the definition was set, and the rules were designed on the same postings. Remaining errors are two Inria postings missed, two defence cloud-as-product postings tagged defense, and general cybersecurity roles tagged defense (5) or trade compliance (4).

**Final tags, lesjeudis.com.** 3,906 flagged postings were tagged: defense 2,365, none 1,245, energy security 100, reshoring 80, diversification 69, trade compliance 45, critical materials 1, one invalid answer. Postings that carry no lexicon term count as none.

**Defense precision on lesjeudis.com.** In a blind sample of 58 postings (20 high, 19 medium and 19 low intensity, drawn from the 2,365 defense tags and labelled by the author; two unclear postings left out) the weighted precision is 0.54 (95% interval 0.41 to 0.67): 0.70 for high intensity, 0.42 for medium and 0.21 for low. Weighted by stratum, about 54% of the defense tags are defense, 24% none, 15% reshoring and 7% energy security. The tag is mostly wrong on engineering and IT-consulting roles at employers whose company paragraph names several sectors ("experts in critical systems for the Defense, Industry, Space, Cybersecurity and AI sectors"), and on aerospace and space roles, which the author labels reshoring under the fixed-sector rule. Counts of defense postings on this board are therefore overstated by about half. They should be read for high and medium intensity only (weighted precision about 0.63), and the low-intensity defense tag should not be used. Among the 26 postings the author also labelled defense, intensity agrees exactly in 14 and within one level in 22. The sample was drawn after the rules were set but is also the only labelled defense check on this board, so no held-out sample exists.

**Diversification on lesjeudis.com is a small and concentrated set.** The 69 postings are all sovereign-tech. Scaleway accounts for 18 (11 distinct texts), Outscale 15 (10 distinct texts), postings that mention SecNumCloud or EUCS in a requirement for 19 (15 distinct texts; 17 low, 2 high) and other sovereign-cloud wording for 17. The same company paragraph is repeated across postings (for example, one Scaleway sentence appears eight times), so the 69 do not count as independent events, and two employers account for about half of them. The count depends on the employer-level rule, which is the author's coding decision; without it the channel would be close to empty.

**Reshoring on lesjeudis.com** (80 postings) is mostly software and engineering at aerospace and semiconductor employers. It follows the fixed-sector definition, so it measures exposure of postings to those sectors, not duties of moving production back.

**Events on lesjeudis.com.** The board holds August 2024 to September 2025 with thin months (210 postings in March 2025, 306 in April). The 90 days after the InvestAI announcement (11 February 2025) contain postings on 14 days only (967 postings), and the change in diversification is -0.15 points (interval -0.42 to +0.18): no effect can be detected. Monthly defense shares swing from 5.9% to 18.5% with the mix of employers, so a before-and-after change in defense on this board (+4.9 points around InvestAI) reflects the board and is not read as an effect.

## Final tags on jobbland.se and jobs.de (prompt v12)

On jobbland.se no channel changes detectably around either event, and jobs.de is too short to test any event; the tags of both boards carry the same limits as those of lesjeudis.com.

**jobbland.se.** All 3,356 flagged postings were re-tagged with prompt v12, with no invalid answer. Rule R1 changed 20 diversification tags to none (19 with the subtype supply-side and one with no subtype); all 20 were ordinary purchasing work (supplier-base management, strategic sourcing, SAP Ariba integration, human-rights due diligence). The EU-term rule for critical materials (script 71) then changed 27 of the model's 35 critical-materials tags to none: the matched terms were "mining and mineral" (15), "precious metals" (7), "batteries" (4), "northvolt" (4), "battery manufacturing" (3) and "energy storage" (1). The rule sends a removed tag to none, so the author read the four removed postings that carried a Northvolt or battery-manufacturing term; all four are battery-factory roles at Northvolt (automation, quality, R&D technician, process operator) and were labelled reshoring, high, which overrides the rule for those four (marked manual\_review in the data). Final tags: none 1,302, defense 1,254, energy security 571, trade compliance 137, reshoring 79, critical materials 8, diversification 5. The flags come from lexicon v7: Stegra (151 postings) and Northvolt (48) are among the most frequent terms, while IRIS², HYBRIT and the European cloud providers flag no posting on this board.

**Events on jobbland.se** (change in the weighted share of all postings, any intensity, percentage points, 95% interval). The 90 days before and after CRMA (23 May 2024) rest on 1,447 and 3,785 sampled postings, but those postings stand for only 2,146 and 8,105 in the population, because the board's population jumps from about 10,000 postings in September 2024 to about 48,000 in October 2024: the early months are not directly comparable with the later ones.

| Channel | CRMA, 23 May 2024 | AccelerateEU, 22 April 2026 |
| --- | --- | --- |
| Defense | -0.64 (-1.69 to +0.42) | +0.52 (-0.07 to +1.08) |
| Energy security | +0.13 (-0.92 to +1.15) | -0.42 (-1.01 to +0.08) |
| Reshoring | +0.11 (-0.46 to +0.65) | +0.01 (-0.07 to +0.09) |
| Critical materials | -0.10 (-0.28 to +0.06) | -0.01 (-0.07 to +0.05) |
| Trade compliance | -0.16 (-0.38 to +0.01) | -0.03 (-0.17 to +0.12) |
| Diversification | +0.04 (0.00 to +0.11) | 0.00 (0.00 to 0.00) |

Every interval includes zero except diversification around CRMA, where the lower end sits at zero and the channel holds five postings on the whole board and the change is 0.04 points. Trade compliance is reported as counts, with no inference (see Limits). Defense runs at 2 to 3% of postings in most months. December 2025 stands out at 6.8% (interval 5.2 to 8.7). Of its 118 defense-tagged postings in the sample, 61 have no title and mostly sit in runs of consecutive ids, which looks like one batch of ads that arrived without a title. The ones read are mostly Swedish Armed Forces, Saab and Combitech recruitment, together with several that look like false positives (a welder, an assembler, a production technician). The spike is not read as an event effect.

Defense precision was not measured on this board under v12. On round 2 the v9 tag had precision 0.88, and v12 scores 0.85 against 0.80 for v9 on the 620 annotated postings. On lesjeudis.com the same tag is 54% precise, and the bare term "defense" is among the matched terms of 1,103 of the 1,254 jobbland defense tags, so the counts are probably overstated here too, by an amount that is not known.

**jobs.de.** 450 flagged postings were tagged with v12 (none 310, energy security 103, trade compliance 20, defense 13, reshoring 4; R1 removed its one supply-side diversification tag and script 71 its two critical-materials tags, which rested on "precious metals" and "aerospace"). The flags come mostly from generic terms (solar power 77, "wholesale and foreign" 65, nuclear 42, hydrogen 38, wind power 36, customs clearance 20). Only energy security registers, at 0.4 to 1.6% of postings a month with overlapping intervals; trade compliance is at most 0.33% (December 2024) and defense at most 0.16%. The corpus ends in April 2025, so no event is tested on it. jobs.de therefore works as a comparison board, with no labelled posting and an unknown precision.

**Two side indicators (not channels).** The sovereignty-wording indicator and the firm watchlist count postings by wording or by named firm, not by tag, and are upper bounds. Sovereignty wording is near zero on jobbland.se (at most 0.05% a month) and jobs.de (2 postings, one federal advertisement). On lesjeudis.com it is 0.8% to 3.1% a month, mostly recruiting-page boilerplate repeated by a few employers, and the 90 days after InvestAI show 0.84% (0.33 to 1.46) against 1.18% (0.92 to 1.48) before. The firm watchlist names 10 postings on jobbland.se (all tagged none), 2 on jobs.de (none) and 87 on lesjeudis.com (none 53, defense 29, reshoring 4, energy security 1); the contexts are mostly employer descriptions or lists of customers and competitors. The lesjeudis.com share after InvestAI (1.59%, 0.46 to 2.90) is above the share before (0.24%), but it rests on few postings and is reported as a count with no event inferred.

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

- **One board.** Lexicon, prompt and labels all come from jobbland.se (Swedish employers, English text). lesjeudis.com (French employers, English text) was tagged in full with the final prompt; 79 diversification postings and 58 defense postings were labelled there (see the French-board section), and its defense tag is only about 54% precise. jobs.de (450 flagged postings) was tagged with the final prompt as a comparison corpus; no posting from it was labelled, so the accuracy there is unknown.
- **Small counts.** Reshoring, critical materials, trade compliance and diversification have 0 to 11 labelled postings in round 2, so their scores are not estimable or are driven by a few postings. Energy security has 43 postings and an interval of 0.43 to 0.80.
- **Two guides.** Round 1 was labelled under guide v6 and lexicon v1, round 2 under the current guide. The two rounds are not pooled, and channel scores differ between them (energy security recall 0.47 against 0.52 is close, but reshoring recall 0.39 against 0.01 is not).
- **Tuning on the evaluation sample.** The removal of four energy-security terms was decided on rows that were then scored. The 300-row score includes those rows.
- **Labeller.** One annotator made all reference labels. Agreement between two passes of the same annotator (round 1 pass 2) has not been measured.
- **Employer boilerplate and the diversification channel.** The channel codes what the role does, not what the employer's text says. A posting whose only link to sovereignty is a company paragraph (for example "innovative sovereign solutions" on a pentester or SOC analyst advertisement; the sentence appears on 151 lesjeudis.com postings) is none, in line with the rule for defense employers. A sovereign-cloud or sovereign-AI provider is the exception: there the employer's product is the sovereignty service, so developers and engineers at the provider are diversification, with intensity set by how close the duties are to that service. Pure cybersecurity work is none. This is a coding decision of the author; coding at employer level would raise the channel's counts.
- **Diversification has only a small check.** Prompt v12 redefines the channel (reducing dependence on a supplier, country or technology provider, including sovereign cloud and AI). It was checked on 79 labelled lesjeudis.com postings (precision 0.95 and recall 0.83 with the post-tagging rules, optimistic because the rules were designed on the same postings) and on 620 jobbland postings (no ordinary purchasing posting is tagged after rule R1, but the gold holds only 2 diversification labels). The channel's counts rest on three decisions of the author: employer-level coding of European cloud providers, SecNumCloud and EUCS mentions in a role, and the supply-side wording rule. No held-out sample exists.
- **Trade compliance is an ambiguous measure of deglobalization.** Routine customs work cuts both ways. Deglobalization adds obstacles, which creates compliance work, while globalization adds shipments, which creates customs work. So a rise in customs postings after an event is ambiguous, and no ad will announce which cause it has. The channel is therefore kept as an exposure measure for trade-administration work, not as a clean deglobalization signal. Postings that name the new rules themselves (tariffs, sanctions, export controls, dual-use goods, CBAM, rules of origin) are a narrower subset; whether ads state them is being checked with a term probe on the full corpora.
- **Intensity** is exploratory: kappa 0.31 on round 2.
- **Short view** (see above): round 1 was not rechecked against the full text.
- **Not tested:** Claude Haiku on prompt v12, other open models, and any posting not flagged by the lexicon (apart from the 2% miss rate measured in round 1).

## Deviations from the brief

The brief asks for an evaluation on 300 annotated postings with precision, recall and F1; the report gives these, with the following differences.

| Brief | What was done | Why |
| --- | --- | --- |
| Lexicon of 300 to 500 terms | 188 terms (lexicon v7; 154 when the round-1 and round-2 samples were scored) | Only terms the author approved entered; unapproved candidates stay in the proposals files |
| Tagging with Mistral or Qwen, or the Claude API | Qwen 2.5 7B in production; Claude Haiku 4.5 as a benchmark on prompts v6 and v7 | Local and free; Haiku scored higher and is future work on the final prompt |
| One annotated set of 300 | Round 1 (472), round 2 (300), a critical-materials sample (98) | The samples were drawn at different stages as definitions changed; they are scored separately, not pooled |
| Multilingual corpus (Greek and English tools) | English text from three boards (jobbland.se, lesjeudis.com, jobs.de); Swedish terms dropped | The pipeline was validated mainly on jobbland.se in English; lesjeudis.com is partly checked and jobs.de not at all |
| Sector classifier | Not built | Rejected by the author; the ESCO skill extractor is used only as a diagnostic |
| Event analysis for each channel | Defense and, with caution, energy security; other channels as counts | Too few validated postings |

Three board events were examined: the EU tariffs on Chinese electric vehicles (jobs.de, dropped as an analysis because the board's mix changed), the EU InvestAI initiative and the AI Act obligations (lesjeudis.com, tested with keyword groups; no detectable effect). Two further events, the Section 232 tariffs of June 2025 and the EU-US trade deal of July 2025, could not be tested: the only board that covers them, jobbland.se, holds 124 sampled postings in June 2025 and 361 in July 2025.

**Why no electric-vehicle reshoring lexicon for jobs.de.** Two reasons. First, collection on jobs.de looks inconsistent: the mix of postings varies considerably from month to month, and the 2.5 months before the EU tariffs on Chinese electric vehicles (30 October 2024) hold only 93 postings, so a before-and-after comparison would mostly measure changes in what was collected. The supervisor agreed to drop the analysis. Second, a probe of electric-vehicle seed terms on the jobs.de corpus (12,243 postings) found 420 postings with an electric-vehicle term, but in the postings read these were employer perks and fleet text (delivery vehicles that are fully electric, charging options for staff cars), not production work. Terms that would identify battery or vehicle production were almost absent: "battery production" twice, "powertrain" once, and no posting with "gigafactory", "battery cell", "cell production" or any reshoring term. jobs.de is therefore tagged with the existing lexicon like the other boards, and no event analysis is reported for it.
