# Tagged postings dataset: data dictionary

File: `tagged_postings_v12.csv`, written by `85_export_tagged_dataset_v12.py` (UTF-8 with BOM, one row per posting that the lexicon flagged).

## What a row is
A job posting that contains at least one term of the lexicon (v7, 188 terms) and was tagged by Qwen 2.5 7B with prompt v12, after the post-tagging rules R0 to R3 (script 82). Postings without a lexicon term are not in the file; they count as `none` when shares are computed. Three boards:

| Board | Corpus | Language of text |
|---|---|---|
| jobbland.se | January 2024 to September 2026, 53,959 postings after removal of exact duplicates | English slice of a Swedish board |
| lesjeudis.com | August 2024 to September 2025, 18,625 postings | English text, French employers |
| jobs.de | August 2024 to April 2025 | tagged for comparison only; no electric-vehicle analysis (see the evaluation report) |

## Contents of `tagged_postings_v12.csv` (generated 8 November 2026)
7,705 rows: jobbland.se 3,356, lesjeudis.com 3,899, jobs.de 450. The lesjeudis.com tag files hold 3,906 tags; 7 of them belong to postings that the merged corpus drops as exact duplicates across its two files, so they are not in the CSV (the channel counts differ from the tagging run by 4 defense and 3 none). 72 tags were changed by a rule: 43 by script 82 (jobbland.se 20, jobs.de 1, lesjeudis.com 22), 25 by script 71 and 4 by the author's manual labels. One lesjeudis.com row has an invalid model answer. The column `organization` is empty in every row because the corpus files do not carry it; the employer is usually named at the end of the title. 118 rows, all from jobbland.se, have no title.

## Columns

| Column | Meaning |
|---|---|
| `board` | jobbland.se, lesjeudis.com or jobs.de |
| `posting_id` | Posting id in the corpus files (the id of the Tracker record) |
| `source_id` | Id on the original board, where the corpus has it |
| `upload_date` | Publication date (the day of the corpus file entry if the posting has no date) |
| `title`, `organization`, `location`, `location_code`, `experience_level`, `type` | Metadata from the corpus; empty where the board does not give it. The description text is not exported |
| `matched_terms` | Lexicon terms found in the posting, separated by "; ". A term is a reason to look, never a reason for a channel |
| `channel` | Final channel: reshoring, defense, critical materials, energy security, trade compliance, diversification, none, or `invalid` (the model's answer could not be read; counts as none) |
| `subtype` | Only for diversification: `supply-side` (reducing dependence on a supplier or country) or `sovereign-tech` (European sovereign cloud and AI sector); empty otherwise |
| `intensity` | high, medium or low by how close the role's own duties are to the channel; empty or none for none. Exploratory (kappa 0.31 on round 2) |
| `evidence` | Quote of at most 25 words from the posting that the model gave |
| `weight` | The posting's day total divided by the postings taken that day. Weights of one board add up to its population of postings |
| `prompt` | Prompt version that produced the model answer |
| `post_rule` | Rule(s) that changed the model's answer, empty if none: `R0 ...`, `R1 supply-side without diversification wording`, `R2 ...`, `R3 ...` (script 82) `no_eu_anchored_term` (script 71) and `manual_review` (script 87, the author's labels on 4 jobbland.se postings) |
| `channel_model`, `intensity_model`, `subtype_model` | The model's own answer before the rules |
| `tag_ok` | False if the model's answer could not be parsed |

## How to use it
- **Shares.** The share of a channel in a period is the sum of `weight` of the rows with that channel divided by the sum of weights of ALL postings of the board in the period, including postings without a lexicon term. The file alone does not give the denominator; scripts 64 and 84 read the corpus for it. Use them rather than recomputing.
- **Switching a rule off.** Use `channel_model`, `intensity_model` and `subtype_model` instead of the final columns.
- **Medium or high only.** Intensity is reported in two readings (any intensity, and medium or high); the evaluation report uses medium or high where low-intensity tags are known to be unreliable.

## Known limits (read before using a channel)
- **Defense** is the only channel with a usable measurement on jobbland.se (F1 0.85 to 0.88 across samples). On lesjeudis.com the tag is about 54% precise (interval 0.41 to 0.67): 0.70 for high intensity, 0.42 for medium, 0.21 for low. Read defense there for high and medium intensity only; do not use the low-intensity tag. No defense precision sample exists for jobbland.se under v12 or for jobs.de.
- **Energy security** is an indicator (F1 about 0.62 to 0.69).
- **Reshoring** follows the fixed-sector rule (space, aerospace, semiconductors and electronic components, battery production). It measures exposure of postings to those sectors, not the moving of production back.
- **Trade compliance** is an ambiguous measure: routine customs work is created by globalization and by deglobalization alike. Report it as counts, with no event inference.
- **Critical materials** uses the EU definition (Regulation 2024/1252) in the prompt, and the EU-term rule of script 71 is applied after R0 to R3 (export from the `*.r71.post.jsonl` files, and for jobbland.se from `tags_v12_jobbland.final.post.jsonl`, which adds the 4 manual labels); the channel holds few postings (35 raw tags on jobbland.se, 1 on lesjeudis.com, 2 on jobs.de).
- **Diversification** is small and concentrated. On lesjeudis.com its 69 postings are all sovereign-tech and two employers (Scaleway, Outscale) account for about half; the same company paragraph recurs across postings, so they are not independent events. On jobbland.se 6 postings remain after rule R1, and on jobs.de none. The counts depend on three coding decisions of the author: employer-level coding of European cloud providers, SecNumCloud and EUCS mentions in a role, and the supply-side wording rule. A firm watchlist, where used, is an upper-bound sensitivity indicator only.
- **Labels.** One annotator made all reference labels. The v12 diversification check (79 postings) is optimistic because the rules were designed on the same postings.
- **Collection.** The weighted population of jobbland.se jumps from about 10,000 postings in September 2024 to about 48,000 in October 2024; the weights correct the sampling but not a change in what the board listed, so early 2024 months are not directly comparable. jobbland.se December 2025 shows a defense spike (6.8% of postings, against 2 to 3% in other months). In the postings read it appears to come largely from Swedish Armed Forces, Saab and Combitech recruitment and from a batch of ads without titles, together with some false positives; it is not read as an event effect.
