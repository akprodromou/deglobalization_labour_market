# Postings per location code, by source

Endpoint `GET /descriptive-analytics/jobs/locations`, limit 300. Source list: from GET /jobs/sources. No date filter: counts cover all months of a source.

## All sources

First 5 rows as returned:

```json
[
 {
  "Var1": "DE",
  "Freq": 1362950
 },
 {
  "Var1": "FR",
  "Freq": 1064855
 },
 {
  "Var1": "SE",
  "Freq": 893400
 },
 {
  "Var1": "NL",
  "Freq": 469833
 },
 {
  "Var1": "UK",
  "Freq": 376926
 }
]
```

Distinct codes: 32; total: 5,519,045.

| code | postings | share |
|---|---:|---:|
| DE | 1,362,950 | 24.7% |
| FR | 1,064,855 | 19.3% |
| SE | 893,400 | 16.2% |
| NL | 469,833 | 8.5% |
| UK | 376,926 | 6.8% |
| BE | 336,967 | 6.1% |
| AT | 268,201 | 4.9% |
| IT | 146,039 | 2.6% |
| PL | 102,572 | 1.9% |
| EL | 91,670 | 1.7% |
| ES | 75,377 | 1.4% |
| CZ | 52,494 | 1.0% |
| CH | 34,758 | 0.6% |
| SK | 29,386 | 0.5% |
| FI | 27,616 | 0.5% |

## By source

| source | postings with a code | distinct codes | largest codes (share) |
|---|---:|---:|---|
| OJA | 2,371,346 | 30 | DE 27%, FR 20%, UK 16%, AT 9%, NL 6%, IT 6% |
| brightminds | 0 | 0 | (empty) |
| eures | 560,175 | 31 | DE 53%, FR 12%, NL 8%, BE 6%, AT 3%, CZ 3% |
| eures-escox | 1,539,252 | 31 | DE 26%, FR 24%, NL 18%, BE 16%, SE 4%, AT 3% |
| jobbguru | 319 | 1 | SE 100% |
| jobbguru.se | 319 | 1 | SE 100% |
| jobbland | 68,095 | 1 | SE 100% |
| jobbland.se | 694,838 | 1 | SE 100% |
| jobmedic | 1,010 | 1 | UK 100% |
| jobmedic.co.uk | 1,448 | 1 | UK 100% |
| jobs.de | 34,230 | 1 | DE 100% |
| jobscentral | 0 | 0 | (empty) |
| kariera.fr | 86,468 | 1 | FR 100% |
| kariera.gr | 87,766 | 1 | EL 100% |
| lesjeudis | 18,404 | 1 | FR 100% |
| lesjeudis.com | 55,375 | 1 | FR 100% |

Reading: compare the code spellings with those used in earlier filters (for example `EL` against `GR`), and the totals with the source totals of Report Section 9.6; a source whose total is far below its posting count has many postings without a location code.