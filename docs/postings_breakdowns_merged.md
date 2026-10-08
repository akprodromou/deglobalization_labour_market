# Postings breakdowns (sample of 5,004 postings, alias sources merged)

Counts describe the sample, which was drawn at roughly equal size per source; they are not the true distribution. See `diagnostics/18_postings_breakdowns.py`.

Duplicate source pairs were merged (--merge-aliases):
- jobbguru.se: 319 dropped as already in `jobbguru`, 0 kept and relabelled
- jobbland.se: 468 dropped as already in `jobbland`, 0 kept and relabelled
- jobmedic.co.uk: 468 dropped as already in `jobmedic`, 0 kept and relabelled
- lesjeudis.com: 464 dropped as already in `lesjeudis`, 4 kept and relabelled

## 1. Sample by source and `upload_date` year

| Source | n | 2019 | 2023 | 2024 | 2025 | 2026 | no date |
|---|---|---|---|---|---|---|---|
| lesjeudis | 472 | 0 | 0 | 468 | 3 | 1 | 0 |
| jobbland | 468 | 0 | 5 | 463 | 0 | 0 | 0 |
| jobmedic | 468 | 0 | 0 | 468 | 0 | 0 | 0 |
| jobscentral | 468 | 0 | 0 | 468 | 0 | 0 | 0 |
| jobs.de | 468 | 0 | 0 | 465 | 3 | 0 | 0 |
| kariera.fr | 468 | 0 | 0 | 468 | 0 | 0 | 0 |
| kariera.gr | 468 | 0 | 0 | 453 | 13 | 2 | 0 |
| eures | 468 | 0 | 100 | 100 | 100 | 168 | 0 |
| eures-escox | 468 | 0 | 0 | 0 | 0 | 468 | 0 |
| OJA | 468 | 468 | 0 | 0 | 0 | 0 | 0 |
| jobbguru | 319 | 0 | 0 | 319 | 0 | 0 | 0 |
| brightminds | 1 | 0 | 0 | 1 | 0 | 0 | 0 |

## 2. Country (`location_code`)

`location_code` is populated for 4,535 of 5,004 postings (90.6%). Codes follow the Eurostat convention (EL for Greece, UK for the United Kingdom).

| Country code | Postings in sample | % of postings with a code |
|---|---|---|
| DE | 1091 | 24.1% |
| FR | 954 | 21.0% |
| SE | 788 | 17.4% |
| UK | 489 | 10.8% |
| EL | 468 | 10.3% |
| CZ | 273 | 6.0% |
| AT | 264 | 5.8% |
| BG | 90 | 2.0% |
| IT | 32 | 0.7% |
| PL | 26 | 0.6% |
| BE | 15 | 0.3% |
| CH | 12 | 0.3% |
| NL | 12 | 0.3% |
| ES | 8 | 0.2% |
| LU | 5 | 0.1% |
| IE | 4 | 0.1% |
| CY | 2 | 0.0% |
| HU | 1 | 0.0% |
| FI | 1 | 0.0% |

### Country completeness and spread by source

| Source | With code | % | Distinct codes |
|---|---|---|---|
| lesjeudis | 472/472 | 100.0% | 1 |
| jobbland | 468/468 | 100.0% | 1 |
| jobmedic | 468/468 | 100.0% | 1 |
| jobscentral | 0/468 | 0.0% | 0 |
| jobs.de | 468/468 | 100.0% | 1 |
| kariera.fr | 468/468 | 100.0% | 1 |
| kariera.gr | 468/468 | 100.0% | 1 |
| eures | 468/468 | 100.0% | 11 |
| eures-escox | 468/468 | 100.0% | 5 |
| OJA | 468/468 | 100.0% | 15 |
| jobbguru | 319/319 | 100.0% | 1 |
| brightminds | 0/1 | 0.0% | 0 |

## 3. Sector (`sectors`)

`sectors` is populated for 3,528 of 5,004 postings (70.5%). A posting can list several sectors; each is counted once per posting.

| Sector | Postings in sample | % of postings with sectors |
|---|---|---|
| Business and other management consultancy activities | 945 | 26.8% |
| Activities of head offices | 711 | 20.2% |
| Engineering activities and related technical consultancy | 509 | 14.4% |
| Hospital activities | 498 | 14.1% |
| Computer consultancy and computer facilities management activities | 389 | 11.0% |
| Residential nursing care activities | 349 | 9.9% |
| Research and experimental development on natural sciences and engineering | 347 | 9.8% |
| Employment activities | 343 | 9.7% |
| Technical testing and analysis | 339 | 9.6% |
| Nursing and midwifery activities | 333 | 9.4% |
| Computer programming activities | 325 | 9.2% |
| Research and experimental development on social sciences and humanities | 288 | 8.2% |
| MANUFACTURING | 266 | 7.5% |
| Diagnostic imaging services and medical laboratory activities | 218 | 6.2% |
| Manufacture of leather and related products of other materials | 182 | 5.2% |
| Manufacture of electrical equipment | 177 | 5.0% |
| Computing infrastructure, data processing, hosting and related activities | 173 | 4.9% |
| Investigation and private security activities | 148 | 4.2% |
| Manufacture of electronic components | 147 | 4.2% |
| General public administration activities | 138 | 3.9% |
| Manufacture of machinery and equipment n.e.c. | 133 | 3.8% |
| Accommodation | 127 | 3.6% |
| Patient transportation by ambulance | 126 | 3.6% |
| Other information technology and computer service activities | 118 | 3.3% |
| Security activities n.e.c. | 118 | 3.3% |

(514 further sectors not shown; 539 distinct in total.)

### Sector completeness by source

| Source | With sectors | % |
|---|---|---|
| lesjeudis | 440/472 | 93.2% |
| jobbland | 343/468 | 73.3% |
| jobmedic | 422/468 | 90.2% |
| jobscentral | 422/468 | 90.2% |
| jobs.de | 429/468 | 91.7% |
| kariera.fr | 397/468 | 84.8% |
| kariera.gr | 388/468 | 82.9% |
| eures | 283/468 | 60.5% |
| eures-escox | 343/468 | 73.3% |
| OJA | 0/468 | 0.0% |
| jobbguru | 60/319 | 18.8% |
| brightminds | 1/1 | 100.0% |
