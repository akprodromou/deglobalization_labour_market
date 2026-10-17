# Completeness by country and by sector (postings, working sample)

Source file: `data/raw/postings_sample.jsonl`. Postings in the file: 6,723; used: 5,000 (the four alias sources jobbguru.se, jobbland.se, jobmedic.co.uk, lesjeudis.com are left out so duplicate postings are not counted twice). A field is filled when it is not null, not empty, not the literal 'empty' and not an empty list. `*` marks a row with fewer than 30 postings. The sample has about the same size per source, so read the shares within a row, not the counts.

## 1. By country (`location_code`)

| Country | Postings | `title` | `description` | `organization` | `location` | `location_code` | `nuts1` | `occupations` | `skills` | `sectors` | `experience_level` | `type` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| DE | 989 | 88% | 88% | 41% | 100% | 100% | 40% | 99% | 96% | 79% | 5% | 89% |
| FR | 952 | 99% | 99% | 0% | 100% | 100% | 0% | 97% | 96% | 88% | 50% | 99% |
| SE | 788 | 100% | 100% | 0% | 100% | 100% | 0% | 56% | 55% | 51% | 100% | 100% |
| UK | 489 | 96% | 96% | 0% | 100% | 100% | 0% | 94% | 82% | 86% | 99% | 98% |
| EL | 468 | 100% | 100% | 0% | 100% | 100% | 0% | 90% | 91% | 83% | 91% | 100% |
| BG | 268 | 99% | 98% | 99% | 100% | 100% | 99% | 1% | 32% | 0% | 0% | 100% |
| AT | 265 | 2% | 2% | 2% | 98% | 100% | 2% | 100% | 100% | 2% | 24% | 37% |
| CZ | 227 | 99% | 93% | 99% | 84% | 100% | 89% | 100% | 68% | 52% | 0% | 99% |
| CH | 22 | 100%* | 100%* | 100%* | 100%* | 100%* | 0%* | 95%* | 50%* | 0%* | 0%* | 100%* |
| IT | 16 | 0%* | 0%* | 0%* | 100%* | 100%* | 0%* | 100%* | 100%* | 0%* | 44%* | 44%* |
| NL | 12 | 25%* | 25%* | 25%* | 92%* | 100%* | 17%* | 100%* | 100%* | 17%* | 33%* | 50%* |
| BE | 10 | 10%* | 10%* | 10%* | 100%* | 100%* | 10%* | 100%* | 100%* | 0%* | 60%* | 40%* |
| ES | 8 | 0%* | 0%* | 0%* | 100%* | 100%* | 0%* | 100%* | 100%* | 0%* | 75%* | 50%* |
| CY | 5 | 100%* | 100%* | 100%* | 100%* | 100%* | 100%* | 100%* | 60%* | 100%* | 0%* | 100%* |
| LU | 4 | 100%* | 75%* | 100%* | 100%* | 100%* | 100%* | 100%* | 25%* | 0%* | 0%* | 100%* |
| IE | 4 | 0%* | 0%* | 0%* | 100%* | 100%* | 0%* | 100%* | 100%* | 0%* | 75%* | 50%* |
| PL | 2 | 0%* | 0%* | 0%* | 100%* | 100%* | 0%* | 100%* | 100%* | 0%* | 0%* | 0%* |
| HU | 1 | 0%* | 0%* | 0%* | 100%* | 100%* | 0%* | 100%* | 100%* | 0%* | 100%* | 0%* |
| FI | 1 | 0%* | 0%* | 0%* | 100%* | 100%* | 0%* | 100%* | 100%* | 0%* | 100%* | 0%* |
| (no code) | 469 | 100% | 100% | 0% | 100% | 0% | 0% | 95% | 96% | 90% | 100% | 100% |
| **All** | 5000 | 91% | 90% | 19% | 99% | 91% | 18% | 85% | 83% | 68% | 56% | 94% |

## 2. By sector (a posting with several sectors counts in each)

The 25 most frequent sector labels; labels are at mixed NACE levels (Section 13.3), so rows can overlap.

| Sector | Postings | `title` | `description` | `organization` | `location` | `location_code` | `nuts1` | `occupations` | `skills` | `experience_level` | `type` |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Business and other management consultancy activities | 942 | 100% | 100% | 1% | 100% | 87% | 1% | 100% | 96% | 70% | 100% |
| Activities of head offices | 706 | 100% | 100% | 1% | 100% | 76% | 1% | 100% | 99% | 79% | 100% |
| Engineering activities and related technical consultancy | 494 | 100% | 100% | 4% | 100% | 76% | 4% | 100% | 98% | 63% | 100% |
| Hospital activities | 490 | 100% | 100% | 7% | 100% | 93% | 7% | 100% | 85% | 77% | 100% |
| Computer consultancy and computer facilities management acti | 386 | 100% | 100% | 1% | 100% | 75% | 1% | 100% | 99% | 85% | 100% |
| Research and experimental development on natural sciences an | 345 | 100% | 100% | 1% | 100% | 77% | 1% | 100% | 87% | 86% | 100% |
| Employment activities | 343 | 100% | 100% | 0% | 100% | 99% | 0% | 100% | 92% | 73% | 100% |
| Residential nursing care activities | 337 | 100% | 100% | 7% | 100% | 99% | 7% | 100% | 77% | 88% | 100% |
| Technical testing and analysis | 328 | 100% | 100% | 1% | 100% | 75% | 1% | 100% | 97% | 64% | 100% |
| Nursing and midwifery activities | 323 | 100% | 100% | 6% | 100% | 98% | 6% | 100% | 79% | 89% | 100% |
| Computer programming activities | 320 | 100% | 100% | 2% | 100% | 73% | 2% | 100% | 98% | 86% | 100% |
| Research and experimental development on social sciences and | 287 | 100% | 100% | 0% | 100% | 69% | 0% | 100% | 100% | 82% | 100% |
| MANUFACTURING | 255 | 100% | 100% | 17% | 100% | 88% | 16% | 100% | 95% | 49% | 100% |
| Diagnostic imaging services and medical laboratory activitie | 209 | 100% | 100% | 9% | 100% | 95% | 9% | 100% | 77% | 83% | 100% |
| Manufacture of leather and related products of other materia | 181 | 100% | 100% | 0% | 100% | 71% | 0% | 100% | 97% | 88% | 100% |
| Manufacture of electrical equipment | 173 | 100% | 100% | 8% | 100% | 73% | 8% | 100% | 95% | 52% | 100% |
| Computing infrastructure, data processing, hosting and relat | 172 | 100% | 100% | 1% | 100% | 81% | 1% | 100% | 100% | 87% | 100% |
| Investigation and private security activities | 147 | 100% | 100% | 1% | 100% | 92% | 1% | 100% | 98% | 88% | 100% |
| Manufacture of electronic components | 146 | 100% | 100% | 3% | 100% | 78% | 3% | 100% | 95% | 42% | 100% |
| General public administration activities | 137 | 100% | 100% | 1% | 100% | 72% | 1% | 100% | 99% | 77% | 100% |
| Accommodation | 127 | 100% | 100% | 0% | 100% | 74% | 0% | 100% | 100% | 84% | 100% |
| Manufacture of machinery and equipment n.e.c. | 124 | 100% | 100% | 16% | 100% | 77% | 16% | 100% | 99% | 47% | 100% |
| Security activities n.e.c. | 118 | 100% | 100% | 0% | 100% | 93% | 0% | 100% | 98% | 96% | 100% |
| Other information technology and computer service activities | 116 | 100% | 100% | 2% | 100% | 83% | 2% | 100% | 100% | 92% | 100% |
| Patient transportation by ambulance | 116 | 100% | 100% | 15% | 100% | 97% | 15% | 100% | 91% | 10% | 100% |
| (no sector) | 1617 | 71% | 71% | 28% | 99% | 97% | 26% | 53% | 63% | 45% | 80% |

## 3. Which sources make up each country

| Country | Postings | Sources (postings) |
|---|---|---|
| DE | 989 | jobs.de 468, eures-escox 213, eures 190, OJA 118 |
| FR | 952 | kariera.fr 468, lesjeudis 468, OJA 14, eures 2 |
| SE | 788 | jobbland 468, jobbguru 319, OJA 1 |
| UK | 489 | jobmedic 468, OJA 21 |
| EL | 468 | kariera.gr 468 |
| BG | 268 | eures 183, eures-escox 83, OJA 2 |
| AT | 265 | OJA 260, eures-escox 4, eures 1 |
| CZ | 227 | eures-escox 150, eures 75, OJA 2 |
| CH | 22 | eures 11, eures-escox 11 |
| IT | 16 | OJA 16 |
| NL | 12 | OJA 9, eures-escox 2, eures 1 |
| BE | 10 | OJA 9, eures-escox 1 |
| ES | 8 | OJA 8 |
| CY | 5 | eures-escox 3, eures 2 |
| LU | 4 | eures 3, eures-escox 1 |
| IE | 4 | OJA 4 |
| PL | 2 | OJA 2 |
| HU | 1 | OJA 1 |
| FI | 1 | OJA 1 |
| (no code) | 469 | jobscentral 468, brightminds 1 |

## 4. How to read it

- Country is almost a function of source, so a country row mostly repeats the completeness of its sources (table 3).
- The sector rows describe only postings that carry a sector; the row '(no sector)' shows what the others lack. Sector completeness is itself very uneven by source (Section 13.3).
- Rows marked `*` are too small to compare.

