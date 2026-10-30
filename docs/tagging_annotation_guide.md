# Annotation guide: channel and intensity of lexicon-flagged postings

For `docs/tagging_annotation_guide.md`. Version of 30 October 2026 (v9: `critical materials` follows the EU lists of strategic and critical raw materials, Regulation (EU) 2024/1252; iron ore, steel, cement and chemicals are not on them; the 20 round-1 postings labelled `critical materials` under v8 need to be judged again). Earlier version, 28 October 2026 (v8: reshoring means firms moving production back from abroad, so only space, aerospace, semiconductors and electronic components and battery production count; wind and solar equipment manufacturing is energy security). Earlier version, 27 October 2026 (v7: written after reading the round-1 disagreements; it tightens reshoring, trade compliance, `none` against `low`, and `high` against `medium`). Round 1 was annotated under the v6 guide and is used to develop the prompt; round 2 (a fresh sample, `data/tagging_r2/`) is annotated under this guide and is the test. It uses the same definitions as the prompt the model receives (`prompts/tagging_v8.txt`), so that the annotator and the model are asked the same question.

## What you are annotating

Each posting in the annotation sheet (round 2: `data/tagging_r2/annotation_sheet.csv`) contains at least one term of the deglobalization lexicon (shown in `terms_found`). You decide two things:

1. `channel`: which channel of deglobalization the work described in the posting relates to.
2. `intensity`: how central the channel is to the job.

Use only the text on the sheet. Do not look up the employer, and do not use what you know about it. If you did look something up, write "employer known from outside" in `note`. The sheet shows no model prediction; do not open `annotation_key.jsonl` or any tags file before you have finished.

## Principle

Deglobalization shows up in jobs as national and local capacity replacing sourcing abroad in strategically important sectors, as defence and security build-up, and as the legal work of trading under new rules. A posting belongs to a channel when its **duties are in one of the named sectors** (or are the named trade work), not only when it contains a keyword. Work in sectors that are not named (automotive, construction, retail, health care, finance, general IT) is `none`.

## Channels (exactly one per posting)

| Value | Meaning |
|---|---|
| `reshoring` | Firms moving manufacturing or supply chain operations back home from abroad. A posting cannot show the earlier offshoring, so the sectors are fixed in advance: the duties are developing, manufacturing or scaling up production in space (satellites, launch vehicles), aerospace, semiconductors and electronic components, or battery production (cells, packs, battery factories); or an explicit move to shorten, localise or secure supply chains (nearshoring, friend-shoring, China plus one, supply chain resilience, strategic autonomy, European or local production). Using, installing, repairing, testing or stocking batteries, chips or electronics in another kind of job is `none` |
| `defense` | Producing, procuring, maintaining or supplying defence equipment, ammunition and military materiel; the defence industrial base; armed forces bodies and defence agencies |
| `critical materials` | Mining, processing, refining or recycling of the raw materials on the EU lists of strategic and critical raw materials (Regulation (EU) 2024/1252), or securing their supply. Strategic: bauxite/alumina/aluminium, bismuth, boron (metallurgy grade), cobalt, copper, gallium, germanium, lithium (battery grade), magnesium metal, manganese (battery grade), natural graphite (battery grade), nickel (battery grade), platinum group metals, rare earth elements for permanent magnets, silicon metal, titanium metal, tungsten; the critical list adds, for example, antimony, niobium, tantalum, vanadium, fluorspar and phosphate rock. Not on the lists: iron ore, steel, cement, chemicals, gold, silver, zinc, lead. The posting counts only if its text names a listed material (or critical or strategic raw materials in general); a posting that names only iron ore, steel, metals or minerals in general is `none` |
| `energy security` | Building, engineering, operating or maintaining national electricity generation capacity (nuclear, solar, wind, hydro, thermal), energy storage and the electricity grid, including manufacturing of wind and solar equipment (never reshoring); securing energy supply or reducing dependence on one supplier |
| `trade compliance` | The legal work needed to trade under new rules (export controls, dual-use goods, sanctions, CBAM, customs legislation and origin rules, supply chain due diligence, responsible sourcing). The role is responsible for compliance with these rules. Not trade compliance (`none`): routine freight and customs paperwork inside order handling, purchasing, logistics, customer support or distribution; "exports" or "export markets" in a company description; a skill listed as "a plus" |
| `diversification` | Opening or diversifying markets and trade relations (free trade agreements, new export markets). A context channel in the thesis |
| `none` | The posting contains a lexicon term, but the work is not about any channel |
| `unclear` | The text is too short or too ambiguous to decide. Leave `intensity` empty |

If a posting fits several channels, choose the one most central to the work.

## Intensity

| Value | Meaning |
|---|---|
| `high` | Most of the duties are the channel's own work: designing, engineering, producing, operating or maintaining in the sector, managing that work, or doing the trade-compliance task itself. The job title and the first duties named are about that work |
| `medium` | The role supports that work (quality, testing, logistics for production, lean or improvement work, planning, purchasing components for the sector's production, plant IT, project or programme support, research or analysis on the sector, a role in a unit of the sector's employer that is not itself production, engineering or operation), or the channel is one of several explicit duties. Doing the core work as one task among many is `medium` |
| `low` | A corporate or customer-facing function of such an employer (sales, marketing, HR, finance, administration, communication, customer service, catering, cleaning), or the channel appears only in the company description, a mission statement or a customer list while the duties are about something else |
| empty | When the channel is `none` or `unclear` |

When unsure between two intensities, choose the lower one. Do not choose `high` merely because the employer is a defence, energy or aerospace company: ask whether this person's own duties are the core work.

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
| Maintenance electrician at a copper, nickel or lithium mine; the text names the metal | critical materials | medium |
| Supervisor or mechanic at an iron ore mine or a steelworks; iron ore and steel are not on the EU lists | none | empty |
| Mechanic at a mining company; the text says only "metals" or "minerals" | none | empty |
| Process engineer on a rare earth, lithium or graphite refining or recycling project | critical materials | high |
| Mine or smelter administrator (finance, HR) where the text names a listed material | critical materials | low |
| Software developer at a defence company; the company description mentions the defence industrial base | defense | low |
| Catering assistant or secretary at an armed forces body | defense | low |
| Procurement officer buying weapons or munitions for a defence body | defense | medium or high by the duties |
| Customs specialist with export-control or sanctions screening, or responsibility for customs legislation | trade compliance | high or medium by the duties |
| Customs authority officer who controls import and export declarations, origin or sanctions, or applies trade legislation | trade compliance | high or medium by the duties |
| Customs authority officer in border enforcement, crime prevention, smuggling control or general administration | none | empty |
| Customs clerk, freight forwarder or driver handling shipping documents, nothing about export controls or sanctions | none | empty |
| Buyer, order handler or customer support whose duties include import or export documents | none | empty |
| Logistics role that lists "trade compliance" only as a plus | none | empty |
| Technician or electrician installing or replacing batteries; electronics engineer in telecoms, vehicles or instruments | none | empty |
| Production engineer in a battery or semiconductor manufacturer | reshoring | high |
| Technician or production worker in a solar panel or wind turbine factory | energy security | by the duties |
| Battery cell or battery pack production worker | reshoring | by the duties |
| Technician installing or maintaining grid-scale storage or a solar plant | energy security | by the duties |
| Sourcing manager, one duty is "build a resilient and diversified supplier base" | reshoring | medium |
| General purchasing or category management (for example construction materials) | none | empty |
| Automotive test engineer; a consultancy lists "automotive, aerospace, energy" among its sectors | none | empty |
| Public-sector posting: "staff are placed based on the needs of the total defence" (employment boilerplate) | none | empty |
| "Arms" in "arms and legs"; "weapons" in a police or security-guard posting; "trade agreements" meaning sales contracts; "FTA" as fault tree analysis | none | empty |
| "De-risking" used for a clinical trial or a financial position | none | empty |
| A term appears but you cannot tell from the text what the job is | unclear | empty |

The rule for `none` against `low` (v7): `low` is for a corporate or customer-facing role at an employer that really works in the channel's sector, or for a channel that is the employer's own sector described in the text. `none` is for a term used in another sense, for a sector word that only appears in passing in a job in an unnamed sector (a technician replacing batteries, a buyer who handles customs documents, an engineer at a consultancy listing many sectors), and for a skill listed as "a plus".

## Procedure

1. Annotate in sittings of at most about 100 postings. Write the date of each sitting in the `note` column of the first row of the sitting.
2. At least three days after finishing, annotate the pass-2 sheet (`python -m diagnostics.59_make_tagging_sheet --pass2 50`) without looking at pass 1. Script 60 reports your own consistency (kappa).
3. Run script 60 on the tags file(s).

## Limits to state in the thesis

One annotator; the annotation sample is drawn from the same corpus the tags are for; the corpus is an English-language slice of Swedish postings dominated by public-sector and care roles; the lexicon, not the model, decides which postings are looked at, so a posting in a named sector without a lexicon term is not tagged (the optional `--unflagged` sample estimates how many relevant postings that leaves out).
