# Annotation guide: channel and intensity of lexicon-flagged postings

For `docs/tagging_annotation_guide.md`. Version of 23 October 2026 (v6: strategic-sector definitions, customs authority rule). It uses the same definitions as the prompt the model receives (`prompts/tagging_v6.txt`), so that the annotator and the model are asked the same question.

## What you are annotating

Each posting in `data/tagging/annotation_sheet.csv` contains at least one term of the deglobalization lexicon (shown in `terms_found`). You decide two things:

1. `channel`: which channel of deglobalization the work described in the posting relates to.
2. `intensity`: how central the channel is to the job.

Use only the text on the sheet. Do not look up the employer, and do not use what you know about it. If you did look something up, write "employer known from outside" in `note`. The sheet shows no model prediction; do not open `annotation_key.jsonl` or any tags file before you have finished.

## Principle

Deglobalization shows up in jobs as national and local capacity replacing sourcing abroad in strategically important sectors, as defence and security build-up, and as the legal work of trading under new rules. A posting belongs to a channel when its **duties are in one of the named sectors** (or are the named trade work), not only when it contains a keyword. Work in sectors that are not named (automotive, construction, retail, health care, finance, general IT) is `none`.

## Channels (exactly one per posting)

| Value | Meaning |
|---|---|
| `reshoring` | Producing or sourcing nationally or locally instead of abroad in strategically important manufacturing sectors: space (satellites, launch vehicles), aerospace, semiconductors and electronic components, batteries; and any explicit move to shorten, localise or secure supply chains (nearshoring, friend-shoring, China plus one, supply chain resilience, strategic autonomy, European or local production) |
| `defense` | Producing, procuring, maintaining or supplying defence equipment, ammunition and military materiel; the defence industrial base; armed forces bodies and defence agencies |
| `critical materials` | Mining, processing, refining or recycling metals and minerals; securing critical or strategic raw materials (critical raw materials, rare earths, battery metals) |
| `energy security` | Building, engineering, operating or maintaining national electricity generation capacity (nuclear, solar, wind, hydro, thermal), energy storage and the electricity grid; securing energy supply or reducing dependence on one supplier |
| `trade compliance` | The legal work needed to trade under new rules (export controls, dual-use goods, sanctions, CBAM, customs legislation and origin rules, supply chain due diligence, responsible sourcing). Routine freight and customs paperwork is not trade compliance |
| `diversification` | Opening or diversifying markets and trade relations (free trade agreements, new export markets). A context channel in the thesis |
| `none` | The posting contains a lexicon term, but the work is not about any channel |
| `unclear` | The text is too short or too ambiguous to decide. Leave `intensity` empty |

If a posting fits several channels, choose the one most central to the work.

## Intensity

| Value | Meaning |
|---|---|
| `high` | The duties are the channel's own work: designing, engineering, producing, operating or maintaining in the sector, managing that work, or doing the trade-compliance task itself |
| `medium` | The role supports that work (quality, testing, logistics for production, maintenance, lean or improvement work, planning, purchasing components for the sector's production, plant IT), or the channel is one of several explicit duties |
| `low` | A corporate or customer-facing function of such an employer (sales, marketing, HR, finance, administration, communication, customer service, catering, cleaning), or the channel appears only in the company description, a mission statement or a customer list while the duties are about something else |
| empty | When the channel is `none` or `unclear` |

When unsure between two intensities, choose the lower one.

## Edge cases

| Case | Channel | Intensity |
|---|---|---|
| Plant engineering manager for a nuclear (SMR) power plant | energy security | high |
| Distribution electrician maintaining the electricity grid | energy security | high |
| Service coordinator or salesperson for solar and battery installations | energy security | low |
| Business developer for a nuclear power unit | energy security | low or medium by the duties |
| Design engineer at a satellite and launch-vehicle manufacturer | reshoring | high |
| Lean deployment leader at an aerospace manufacturer's production sites | reshoring | medium |
| Stock and order administration at a semiconductor and component distributor | reshoring | low |
| CNC operator at a supplier whose customers include nuclear power (staffing firm text) | energy security | low |
| Maintenance electrician at a mine; the company description says it secures society's access to metals | critical materials | medium |
| Supervisor of diamond drilling at a mine | critical materials | high |
| Software developer at a defence company; the company description mentions the defence industrial base | defense | low |
| Catering assistant or secretary at an armed forces body | defense | low |
| Procurement officer buying weapons or munitions for a defence body | defense | medium or high by the duties |
| Customs specialist with export-control or sanctions screening, or responsibility for customs legislation | trade compliance | high or medium by the duties |
| Customs authority officer who controls import and export declarations, origin or sanctions, or applies trade legislation | trade compliance | high or medium by the duties |
| Customs authority officer in border enforcement, crime prevention, smuggling control or general administration | none | empty |
| Customs clerk, freight forwarder or driver handling shipping documents, nothing about export controls or sanctions | none | empty |
| Sourcing manager, one duty is "build a resilient and diversified supplier base" | reshoring | medium |
| General purchasing or category management (for example construction materials) | none | empty |
| Automotive test engineer; a consultancy lists "automotive, aerospace, energy" among its sectors | none | empty |
| Public-sector posting: "staff are placed based on the needs of the total defence" (employment boilerplate) | none | empty |
| "Arms" in "arms and legs"; "weapons" in a police or security-guard posting; "trade agreements" meaning sales contracts; "FTA" as fault tree analysis | none | empty |
| "De-risking" used for a clinical trial or a financial position | none | empty |
| A term appears but you cannot tell from the text what the job is | unclear | empty |

The rule for `none` against `low`: if the term is used in the sense of the channel, even only in passing, the channel applies with intensity `low`. `none` is for a term used in another sense, or one that has nothing to do with the work.

## Procedure

1. Annotate in sittings of at most about 100 postings. Write the date of each sitting in the `note` column of the first row of the sitting.
2. At least three days after finishing, annotate the pass-2 sheet (`python -m diagnostics.59_make_tagging_sheet --pass2 50`) without looking at pass 1. Script 60 reports your own consistency (kappa).
3. Run script 60 on the tags file(s).

## Limits to state in the thesis

One annotator; the annotation sample is drawn from the same corpus the tags are for; the corpus is an English-language slice of Swedish postings dominated by public-sector and care roles; the lexicon, not the model, decides which postings are looked at, so a posting in a named sector without a lexicon term is not tagged (the optional `--unflagged` sample estimates how many relevant postings that leaves out).
