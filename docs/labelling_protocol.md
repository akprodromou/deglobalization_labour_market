# Labelling protocol for the 2026 validation sample

Written 18 October 2026, before any posting was labelled. Thresholds and rules below are fixed now and are not changed after the first label is entered.

## Purpose

The Tracker supplies no sector tags for 2026 postings. The analyses of the Steel import regulation (applies 1 July 2026) and of AccelerateEU (22 April 2026) therefore rest on a text classifier that flags manufacturing and, descriptively, metals postings. Hand labels give the ground truth against which the classifier, and the keyword screen it is compared with, are scored.

## Material

- Source: `jobbland.se`, January to August 2026, day-stratified corpus of script 52, exact description duplicates removed (script 53).
- The corpus is almost all English: about 98% of postings are in English and about 2% in Swedish. It is therefore an English-language slice of Swedish postings, not the national labour market. Municipalities, regions, health care and schools dominate the titles. This limits what any result can say about Sweden and is stated in the thesis.
- Sample: 400 postings drawn by script 53 in three strata (metals words; manufacturing words only; neither), shown in random order with title and the first 1,200 characters of the description. The stratum, the screen result and any prediction are hidden.

## What is labelled

Two columns, each with `yes`, `no` or `unclear`:

1. `manufacturing`: the employer's main activity is manufacturing.
2. `metals`: the employer's main activity is making or processing metals.

Label the employer's activity, not the job title. An accountant, a driver or a recruiter hired by a manufacturer is `yes` if the text says the employer is a manufacturer.

## Rules for `manufacturing`

`yes` when the text shows that the employer, or the site the job is at, makes physical goods in a factory or workshop: food and drink, textiles and clothing, wood, paper, chemicals and pharmaceuticals, plastics and rubber, metals, machinery, electrical and electronic equipment, vehicles, ships and aircraft, furniture. Also `yes`: repair, maintenance and installation of industrial machinery, because the group defined for the Steel plan includes it.

`no` when the employer is in: construction and civil engineering, utilities (electricity, water, waste), mining and quarrying, retail and wholesale, transport and logistics, software and IT services, consulting, finance, education, public administration, health and social care, hotels and restaurants, media, and staffing or recruitment with no manufacturing site named.

`unclear` when the text does not say what the employer does and the job is generic (an assistant, a manager, a recruiter), or when a staffing agency posts for an unnamed client.

Edge cases:

| Case | Label |
|---|---|
| Production operator or assembler at a named manufacturer | manufacturing `yes` |
| Staffing agency recruiting "production operators" for an unnamed client | `unclear` (the job is production work but the employer's sector is not shown); label `yes` only if the text names a factory, plant or manufacturing site |
| R&D engineer at a manufacturer | `yes` |
| Software or IT role at a manufacturer | `yes` if the text says the employer is a manufacturer, otherwise `no` |
| Food retail, bakery shop, restaurant kitchen | `no` |
| Industrial bakery, brewery, food factory | `yes` |
| Construction trades (welder on a building site) | `no` |
| Shipyard, vehicle workshop that builds (not only repairs) | `yes` |
| Car repair and servicing | `no` |
| Mining and quarrying | `no` |

## Rules for `metals`

`yes` when the employer makes or processes metals: steel and iron works, foundries, rolling and forging, aluminium and copper production, machining of metal parts, fabricated metal products (including welding and sheet-metal workshops that produce parts or structures), manufacture of metal machinery. A job title with "welder" or "CNC" counts only if the text shows a metalworking employer.

`no` for manufacturers that use but do not work metal (car assembly is `manufacturing yes`, `metals no` unless the posting is for a metal part or a foundry), for construction and for metal trading.

`unclear` when metalworking is possible but the text does not say.

`metals` can be `yes` only when `manufacturing` is `yes`.

## Procedure

1. Run script 53, open `data/labelling/validation_sheet.csv` in a spreadsheet, and fill the two columns without looking at `validation_key.jsonl`. Save as CSV (UTF-8).
2. Label in several sittings of at most about 100 postings. Record the date of each sitting in the `note` column of the first row of the sitting.
3. At least three days after finishing, run `--pass2 50`, label that sheet without opening the first, and score both passes.
4. Run script 54. It reports precision, recall and prevalence with intervals, the share of `unclear` and the agreement between the two passes.
5. The classifier is scored on the same sheet with `--predictions`.

## Acceptance (fixed in advance)

- Manufacturing flag: accepted if precision >= 0.80 and recall >= 0.70 on the weighted sample. If a point estimate meets the threshold but the lower end of its 95% interval does not, the result is reported as borderline and the flag is used only with that caveat.
- Not accepted: the manufacturing share is estimated with the keyword screen as a fallback, or the 2026 events are reported without a sector comparison.
- Metals: descriptive only.
- Consistency: Cohen's kappa of the two passes at least 0.6 for both labels. Below that, the rules above are tightened, a note records the change, and the sample is labelled again.
- Unclear: if more than 20% of the weighted labelled postings are `unclear`, the thesis states that the text of these postings does not support a sector classification for a fifth of the source.

## Limits to state in the thesis

- One labeller (the author) and no second rater, unless the supervisor labels 50 postings, which would add an inter-rater check.
- The sample is drawn from the same corpus the classifier is applied to; it is not a test on an independent source.
- The corpus is an English-language slice; the weights bring the sample back to that slice, not to Sweden.
- Weights treat the population as distinct posting texts; exact copies removed before sampling are not counted.

## Data handling

`data/labelling/` holds employer text and is not tracked by git. Only the aggregate results (`docs/labelling_results.md`) are committed.
