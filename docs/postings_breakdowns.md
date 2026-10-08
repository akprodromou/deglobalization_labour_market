# Postings breakdowns (sample of 6,723 postings)

Counts describe the sample, which was drawn at roughly equal size per source; they are not the true distribution. See `diagnostics/18_postings_breakdowns.py`.

## 1. Sample by source and `upload_date` year

| Source | n | 2019 | 2023 | 2024 | 2025 | 2026 | no date |
|---|---|---|---|---|---|---|---|
| jobbland | 468 | 0 | 5 | 463 | 0 | 0 | 0 |
| jobmedic | 468 | 0 | 0 | 468 | 0 | 0 | 0 |
| jobmedic.co.uk | 468 | 0 | 0 | 468 | 0 | 0 | 0 |
| jobscentral | 468 | 0 | 0 | 468 | 0 | 0 | 0 |
| jobs.de | 468 | 0 | 0 | 465 | 3 | 0 | 0 |
| kariera.fr | 468 | 0 | 0 | 468 | 0 | 0 | 0 |
| kariera.gr | 468 | 0 | 0 | 453 | 13 | 2 | 0 |
| lesjeudis | 468 | 0 | 0 | 468 | 0 | 0 | 0 |
| lesjeudis.com | 468 | 0 | 0 | 462 | 3 | 3 | 0 |
| jobbland.se | 468 | 0 | 5 | 463 | 0 | 0 | 0 |
| eures | 468 | 0 | 100 | 100 | 100 | 168 | 0 |
| eures-escox | 468 | 0 | 0 | 0 | 0 | 468 | 0 |
| OJA | 468 | 468 | 0 | 0 | 0 | 0 | 0 |
| jobbguru | 319 | 0 | 0 | 319 | 0 | 0 | 0 |
| jobbguru.se | 319 | 0 | 0 | 319 | 0 | 0 | 0 |
| brightminds | 1 | 0 | 0 | 1 | 0 | 0 | 0 |

## 2. Country (`location_code`)

`location_code` is populated for 6,254 of 6,723 postings (93.0%). Codes follow the Eurostat convention (EL for Greece, UK for the United Kingdom).

| Country code | Postings in sample | % of postings with a code |
|---|---|---|
| SE | 1575 | 25.2% |
| FR | 1418 | 22.7% |
| DE | 1091 | 17.4% |
| UK | 957 | 15.3% |
| EL | 468 | 7.5% |
| CZ | 273 | 4.4% |
| AT | 264 | 4.2% |
| BG | 90 | 1.4% |
| IT | 32 | 0.5% |
| PL | 26 | 0.4% |
| BE | 15 | 0.2% |
| CH | 12 | 0.2% |
| NL | 12 | 0.2% |
| ES | 8 | 0.1% |
| LU | 5 | 0.1% |
| IE | 4 | 0.1% |
| CY | 2 | 0.0% |
| HU | 1 | 0.0% |
| FI | 1 | 0.0% |

### Country completeness and spread by source

| Source | With code | % | Distinct codes |
|---|---|---|---|
| jobbland | 468/468 | 100.0% | 1 |
| jobmedic | 468/468 | 100.0% | 1 |
| jobmedic.co.uk | 468/468 | 100.0% | 1 |
| jobscentral | 0/468 | 0.0% | 0 |
| jobs.de | 468/468 | 100.0% | 1 |
| kariera.fr | 468/468 | 100.0% | 1 |
| kariera.gr | 468/468 | 100.0% | 1 |
| lesjeudis | 468/468 | 100.0% | 1 |
| lesjeudis.com | 468/468 | 100.0% | 1 |
| jobbland.se | 468/468 | 100.0% | 1 |
| eures | 468/468 | 100.0% | 11 |
| eures-escox | 468/468 | 100.0% | 5 |
| OJA | 468/468 | 100.0% | 15 |
| jobbguru | 319/319 | 100.0% | 1 |
| jobbguru.se | 319/319 | 100.0% | 1 |
| brightminds | 0/1 | 0.0% | 0 |

## 3. Sector (`sectors`)

`sectors` is populated for 4,785 of 6,723 postings (71.2%). A posting can list several sectors; each is counted once per posting.

| Sector | Postings in sample | % of postings with sectors |
|---|---|---|
| Business and other management consultancy activities | 1414 | 29.6% |
| Activities of head offices | 1002 | 20.9% |
| Hospital activities | 833 | 17.4% |
| Engineering activities and related technical consultancy | 653 | 13.6% |
| Residential nursing care activities | 641 | 13.4% |
| Nursing and midwifery activities | 615 | 12.9% |
| Computer consultancy and computer facilities management activities | 602 | 12.6% |
| Employment activities | 579 | 12.1% |
| Research and experimental development on natural sciences and engineering | 541 | 11.3% |
| Computer programming activities | 499 | 10.4% |
| Technical testing and analysis | 431 | 9.0% |
| Diagnostic imaging services and medical laboratory activities | 382 | 8.0% |
| Research and experimental development on social sciences and humanities | 347 | 7.3% |
| MANUFACTURING | 336 | 7.0% |
| Computing infrastructure, data processing, hosting and related activities | 280 | 5.9% |
| Manufacture of leather and related products of other materials | 266 | 5.6% |
| Investigation and private security activities | 251 | 5.2% |
| Security activities n.e.c. | 222 | 4.6% |
| Manufacture of electrical equipment | 211 | 4.4% |
| Other information technology and computer service activities | 202 | 4.2% |
| General public administration activities | 193 | 4.0% |
| Accommodation | 181 | 3.8% |
| Public relations and communication activities | 175 | 3.7% |
| Manufacture of electronic components | 171 | 3.6% |
| Computing infrastructure, data processing, hosting and other information service activities | 159 | 3.3% |

(514 further sectors not shown; 539 distinct in total.)

### Sector completeness by source

| Source | With sectors | % |
|---|---|---|
| jobbland | 343/468 | 73.3% |
| jobmedic | 422/468 | 90.2% |
| jobmedic.co.uk | 422/468 | 90.2% |
| jobscentral | 422/468 | 90.2% |
| jobs.de | 429/468 | 91.7% |
| kariera.fr | 397/468 | 84.8% |
| kariera.gr | 388/468 | 82.9% |
| lesjeudis | 436/468 | 93.2% |
| lesjeudis.com | 436/468 | 93.2% |
| jobbland.se | 343/468 | 73.3% |
| eures | 283/468 | 60.5% |
| eures-escox | 343/468 | 73.3% |
| OJA | 0/468 | 0.0% |
| jobbguru | 60/319 | 18.8% |
| jobbguru.se | 60/319 | 18.8% |
| brightminds | 1/1 | 100.0% |
