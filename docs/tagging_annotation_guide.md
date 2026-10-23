# Annotation guide: channel and intensity of lexicon-flagged postings

For `docs/tagging_annotation_guide.md`. Draft of 22 October 2026 (revised after the lexicon build), to be fixed before the first posting is annotated. It uses the same definitions as the prompt the model receives (`prompts/tagging_v2.txt`), so that the annotator and the model are asked the same question.

## What you are annotating

Each posting in `data/tagging/annotation_sheet.csv` contains at least one term of the deglobalization lexicon (shown in `terms_found`). You decide two things:

1. `channel`: which channel of deglobalization the work described in the posting relates to.
2. `intensity`: how much of the job is about that channel.

Use only the text on the sheet. Do not look up the employer, and do not use what you know about it. If you did look something up, write "employer known from outside" in `note`. The sheet shows no model prediction; do not open `annotation_key.jsonl` or any tags file before you have finished.

## Channels (exactly one per posting)

| Value | Meaning |
|---|---|
| `reshoring` | Moving production or sourcing closer to home or to allied countries; shorter, more resilient or less single-country-dependent supply chains (nearshoring, friend-shoring, supply chain resilience, China plus one, strategic autonomy, European or local production) |
| `defense` | Producing, procuring or supplying defence equipment, ammunition and military materiel; the defence industrial base |
| `critical materials` | Securing, sourcing, processing or recycling critical or strategic raw materials (critical raw materials, rare earths, battery metals) |
| `energy security` | Securing energy supply or reducing dependence on one supplier (security of supply, diversifying gas supply, protecting energy infrastructure) |
| `trade compliance` | The legal and administrative work needed to trade under new rules (export controls, dual-use goods, sanctions, CBAM, customs and origin rules, supply chain due diligence, responsible sourcing) |
| `diversification` | Opening or diversifying markets and trade relations (free trade agreements, new export markets). A context channel in the thesis |
| `none` | The posting contains a lexicon term, but the work is not about any channel |
| `unclear` | The text is too short or too ambiguous to decide. Leave `intensity` empty |

If a posting fits several channels, choose the one most central to the work.

## Intensity

| Value | Meaning |
|---|---|
| `high` | The channel is the main subject of the role (job title or core duties) |
| `medium` | One of several explicit duties or requirements |
| `low` | Mentioned in passing (company description, a list item, boilerplate) while the job is mainly about something else |
| empty | When the channel is `none` or `unclear` |

## Edge cases

| Case | Channel | Intensity |
|---|---|---|
| Customs specialist whose duties include export-control and sanctions screening | trade compliance | high |
| Sourcing manager, one duty is "build a resilient and diversified supplier base" | reshoring | medium |
| Software developer at a defence company; the company description mentions the defence industrial base | defense | low |
| "De-risking" used for a clinical trial or a financial position | none | empty |
| "Lithium" in a posting for a battery cell chemist, with nothing about supply or sourcing | none | empty |
| Posting mentions "security of supply" for a grid operator's planning role | energy security | high or medium by the duties |
| Boilerplate list of a company's values that includes "responsible sourcing" | trade compliance | low |
| A term appears but you cannot tell from the text what the job is | unclear | empty |
| Catering assistant or secretary at an armed forces body; the text describes the ministry's defence mission | defense | low |
| Procurement officer buying weapons or munitions for a defence body or company | defense | medium or high by the duties |
| Customs clearance clerk: customs declarations, shipping documents, freight forwarding, nothing about export controls or sanctions | trade compliance | low |
| The same clerk, with export-control or sanctions screening as a named duty | trade compliance | medium or high by the duties |
| Staffing firm posting for a client "in the aerospace and defence sector"; the role is a CNC machinist | defense | low |
| "Weapons" in a police or security-guard posting; "batteries" in a general battery role; "nuclear" in a boilermaker posting | none | empty |

When unsure between two intensities, choose the lower one. A sector or customer industry named in the company description is `low` at most. Working for a defence employer does not make the role `high`; judge by the duties.

The rule for `none` against `low`: if the term is used in the sense of the channel, even only in passing, the channel applies with intensity `low`. `none` is for a term used in another sense, or one that has nothing to do with the work.

## Procedure

1. Annotate in sittings of at most about 100 postings. Write the date of each sitting in the `note` column of the first row of the sitting.
2. At least three days after finishing, annotate the pass-2 sheet (`python -m diagnostics.59_make_tagging_sheet --pass2 50`) without looking at pass 1. Script 60 reports your own consistency (kappa).
3. Run script 60 on the tags file(s).

## Limits to state in the thesis

One annotator; the annotation sample is drawn from the same corpus the tags are for; the corpus is an English-language slice of Swedish postings dominated by public-sector and care roles; the lexicon, not the model, decides which postings are looked at, so a posting without a lexicon term is not tagged (the optional `--unflagged` sample estimates how many relevant postings that leaves out).
