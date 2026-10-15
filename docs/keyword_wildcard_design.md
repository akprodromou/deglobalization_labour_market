# Keyword wildcard design test

Per form: count of the API's `keywords` filter (one keyword) and the word forms found in the title and description of the first 100 returned postings (top 6 with number of postings). 'plain' is the control: a count above 0 shows the word occurs in that month.

## jobbland.se, 2024-06, word `software`

| form | count | seconds | word forms in the first 100 postings | note |
|---|---:|---:|---|---|
| `software` (plain) | 269 | 18 | software 216 |  |
| `software*` | - | 105 | - | HTTP 504: <html>
<head><title>504 Gateway Time-out</title></head>
<body>
<center><h1>504 Gateway Time-out</ |
| `softwar*` | 25 | 7 | software 60 |  |
| `softwa*` | 0 | 0 | - |  |
| `soft*` | 43 | 4 | soft 101, software 3 |  |
| `softwares` | 1 | 2 | softwares 1 |  |
| `softwares*` | 1 | 0 | softwares 1 |  |
| `*oftware` | 0 | 0 | - |  |

## kariera.gr, 2026-03, word `hotel`

| form | count | seconds | word forms in the first 100 postings | note |
|---|---:|---:|---|---|
| `hotel` (plain) | 1,748 | 6 | hotel 255, hotels 102, hotelbrain 4, hotelscertification 1, hotelsexposure 1, hotelsafety 1 |  |
| `hotel*` | 1,748 | 3 | hotel 255, hotels 102, hotelbrain 4, hotelscertification 1, hotelsexposure 1, hotelsafety 1 |  |
| `hote*` | 0 | 0 | - |  |
| `hot*` | 64 | 5 | hot 91, hotel 83, hotels 46, hotelbrain 3 |  |
| `hotels` | 0 | 0 | - |  |
| `hotels*` | 0 | 0 | - |  |
| `*otel` | 0 | 0 | - |  |

## kariera.gr, 2026-03, word `nurse`

| form | count | seconds | word forms in the first 100 postings | note |
|---|---:|---:|---|---|
| `nurse` (plain) | 0 | 0 | - |  |
| `nurse*` | 0 | 0 | - |  |
| `nurs*` | 58 | 2 | nursing 77, nurse 35, nurses 21 |  |
| `nur*` | 0 | 0 | - |  |
| `nurses` | 0 | 1 | - |  |
| `nurses*` | 0 | 0 | - |  |
| `*urse` | 0 | 0 | - |  |

## kariera.gr, 2026-03, word `engineer`

| form | count | seconds | word forms in the first 100 postings | note |
|---|---:|---:|---|---|
| `engineer` (plain) | 0 | 0 | - |  |
| `engineer*` | 0 | 0 | - |  |
| `enginee*` | 0 | 0 | - |  |
| `engine*` | 0 | 0 | - |  |
| `engi*` | 0 | 0 | - |  |
| `engineers` | 0 | 1 | - |  |
| `engineers*` | 0 | 0 | - |  |
| `*ngineer` | 0 | 0 | - |  |

Reading: compare, within one case, the plain word with its starred forms (see the three patterns in the header of `diagnostics/44`). A starred form that returns more than the plain word together with longer word forms (plural, -ing, -ment) shows a wildcard for following characters; a starred form that returns less than the plain word shows that the asterisk needs a following character; identical counts show that the asterisk is ignored. A case in which even the plain word is 0 says nothing about the rule.