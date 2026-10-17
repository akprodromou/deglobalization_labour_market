# Sector-month counts around the primary events (Month 3, step 1)

Rule: a sector is usable for an event in a source only if its estimated number of postings is at least **100** in every pre-window month and every post-window month (event month left out). A description counts as text from 200 characters. Estimates come from page samples (see the script's header for limits); `!` = below the minimum, `~` = the 95% interval straddles the minimum. Only the first sector tag of a posting is used, duplicates are not removed, so the counts are optimistic upper bounds. These are estimates for the whole source. The rule is applied to the postings that are actually downloaded and analysed, so the download size per month has to be chosen so that every sector reaches the minimum (for a sector with a share s of a month's postings, about 100/s postings must be downloaded).

## EU Steel and Metals Action Plan, 19 Mar 2025

### kariera.gr  (pre: 2024-12, 2025-01, 2025-02; event month: 2025-03; post: 2025-04, 2025-05, 2025-06)

| Month | Postings | Sampled | With sector tag | With text | Est. tagged | Est. with text |
|---|---:|---:|---:|---:|---:|---:|
| 2024-12 | 4,866 | 300 | 87% | 99% | 4,250 | 4,801 |
| 2025-01 | 7,065 | 300 | 84% | 99% | 5,958 | 7,018 |
| 2025-02 | 3,174 | 300 | 88% | 99% | 2,783 | 3,153 |
| 2025-03 | 2,884 | 300 | 90% | 100% | 2,596 | 2,884 |
| 2025-04 | 1,458 | 300 | 84% | 98% | 1,225 | 1,429 |
| 2025-05 | 4,219 | 300 | 89% | 99% | 3,755 | 4,191 |
| 2025-06 | 4,678 | 300 | 86% | 100% | 4,023 | 4,662 |

| Sector (first tag) | 2024-12 | 2025-01 | 2025-02 | 2025-03* | 2025-04 | 2025-05 | 2025-06 | Rule met? |
|---|---|---|---|---|---|---|---|---|
| Activities of call centres | 389 | 306 | 201 | 154~ | 68! | 309 | 296 | no (pooled pre 896, post 674) |
| Research and experimental development on social science | 373 | 283 | 201 | 163 | 44! | 338 | 203 | no (pooled pre 857, post 584) |
| Warehousing and storage | 195 | 330 | 106~ | 96! | 102~ | 295 | 374 | **yes** (pooled pre 630, post 772) |
| Business and other management consultancy activities | 178 | 236 | 138~ | 163 | 63! | 183 | 312 | no (pooled pre 551, post 558) |
| Activities of head offices | 227 | 306 | 95! | 125~ | 58! | 98! | 187 | no (pooled pre 628, post 344) |
| Restaurant activities | 211 | 259 | 116~ | 144~ | 15! | 155~ | 78! | no (pooled pre 586, post 247) |
| Hotels and similar accommodation | 178 | 212 | 138~ | 125~ | 15! | 169~ | 47! | no (pooled pre 528, post 230) |
| Accommodation | 130~ | 118~ | 95! | 96! | 19! | 183 | 172~ | no (pooled pre 343, post 374) |
| Vocational secondary education | 162~ | 47! | 190 | 279 | 15! | 14! | 16! | no (pooled pre 400, post 44) |
| Accounting, bookkeeping and auditing activities; tax co | 178 | 212 | 21! | 58! | 34! | 56! | 125~ | no (pooled pre 412, post 215) |
| Activities of advertising agencies | 81! | 141~ | 159~ | 67! | 10! | 70! | 109~ | no (pooled pre 381, post 189) |
| Computing infrastructure, data processing, hosting and  | 114~ | 141~ | 32! | 38! | 63! | 113~ | 0! | no (pooled pre 287, post 176) |

Sectors meeting the rule: **1** of the 12 most frequent labels (`*` marks the event month).

**Pre-specified groups** (all labels of the group added up, same rule):

| Group | 2024-12 | 2025-01 | 2025-02 | 2025-03* | 2025-04 | 2025-05 | 2025-06 | Rule met? |
|---|---|---|---|---|---|---|---|---|
| Exposed manufacturing (primary): all 'Manufactur... | 454 | 942 | 317 | 288 | 180 | 464 | 312 | **yes** (pooled pre 1,714, post 956) |
| Narrow metals (secondary, descriptive only) | 32! | 118~ | 21! | 10! | 29! | 14! | 0! | no (pooled pre 171, post 43) |

### lesjeudis.com  (pre: 2024-12, 2025-01, 2025-02; event month: 2025-03; post: 2025-04, 2025-05, 2025-06)

| Month | Postings | Sampled | With sector tag | With text | Est. tagged | Est. with text |
|---|---:|---:|---:|---:|---:|---:|
| 2024-12 | 3,511 | 300 | 97% | 100% | 3,394 | 3,511 |
| 2025-01 | 4,191 | 300 | 91% | 100% | 3,814 | 4,191 |
| 2025-02 | 1,548 | 300 | 96% | 100% | 1,491 | 1,548 |
| 2025-03 | 450 | 300 | 97% | 100% | 435 | 450 |
| 2025-04 | 581 | 300 | 97% | 100% | 566 | 581 |
| 2025-05 | 2,336 | 300 | 95% | 100% | 2,227 | 2,336 |
| 2025-06 | 3,887 | 300 | 95% | 100% | 3,706 | 3,887 |

| Sector (first tag) | 2024-12 | 2025-01 | 2025-02 | 2025-03* | 2025-04 | 2025-05 | 2025-06 | Rule met? |
|---|---|---|---|---|---|---|---|---|
| Business and other management consultancy activities | 456 | 740 | 279 | 57! | 29! | 273 | 479 | no (pooled pre 1,475, post 781) |
| Computer programming activities | 199 | 405 | 119~ | 54! | 76! | 179 | 505 | no (pooled pre 723, post 760) |
| Security activities n.e.c. | 351 | 279 | 186 | 36! | 77! | 343 | 246 | no (pooled pre 816, post 666) |
| Operation of arts facilities and sites | 105~ | 168~ | 36! | 18! | 35! | 132~ | 285 | no (pooled pre 309, post 452) |
| General public administration activities | 94! | 210 | 72! | 10! | 10! | 164 | 168~ | no (pooled pre 375, post 342) |
| Activities of head offices | 140~ | 140~ | 41! | 28! | 17! | 101~ | 143~ | no (pooled pre 321, post 261) |
| Computer consultancy and computer facilities management | 47! | 70! | 41! | 20! | 27! | 47! | 117~ | no (pooled pre 158, post 190) |
| Other monetary intermediation | 70! | 28! | 15! | 3! | 15! | 55! | 117~ | no (pooled pre 114, post 187) |
| Activities of religious organisations | 129~ | 14! | 31! | 12! | 10! | 47! | 39! | no (pooled pre 174, post 95) |
| Manufacture of footwear | 59! | 84! | 26! | 4! | 2! | 55! | 52! | no (pooled pre 168, post 108) |
| MANUFACTURING | 117~ | 70! | 5! | 4! | 2! | 23! | 39! | no (pooled pre 192, post 64) |
| Other education n.e.c. | 94! | 14! | 21! | 8! | 4! | 31! | 65! | no (pooled pre 128, post 100) |

Sectors meeting the rule: **0** of the 12 most frequent labels (`*` marks the event month).

**Pre-specified groups** (all labels of the group added up, same rule):

| Group | 2024-12 | 2025-01 | 2025-02 | 2025-03* | 2025-04 | 2025-05 | 2025-06 | Rule met? |
|---|---|---|---|---|---|---|---|---|
| Exposed manufacturing (primary): all 'Manufactur... | 550 | 433 | 170 | 28! | 45! | 195 | 376 | no (pooled pre 1,153, post 615) |
| Narrow metals (secondary, descriptive only) | 59! | 0! | 5! | 3! | 4! | 39! | 39! | no (pooled pre 64, post 82) |

### jobbland.se  (pre: 2024-12, 2025-01, 2025-02; event month: 2025-03; post: 2025-04, 2025-05, 2025-06)

| Month | Postings | Sampled | With sector tag | With text | Est. tagged | Est. with text |
|---|---:|---:|---:|---:|---:|---:|
| 2024-12 | 47,151 | 300 | 80% | 100% | 37,564 | 47,151 |
| 2025-01 | 53,139 | 300 | 91% | 100% | 48,356 | 52,962 |
| 2025-02 | 23,017 | 300 | 89% | 100% | 20,562 | 23,017 |
| 2025-03 | 10,959 | 300 | 89% | 100% | 9,754 | 10,959 |
| 2025-04 | 4,139 | 300 | 93% | 100% | 3,835 | 4,139 |
| 2025-05 | 6,210 | 300 | 91% | 100% | 5,630 | 6,210 |
| 2025-06 | 132 | 132 | 0% | 100% | 0 | 132 |

| Sector (first tag) | 2024-12 | 2025-01 | 2025-02 | 2025-03* | 2025-04 | 2025-05 | 2025-06 | Rule met? |
|---|---|---|---|---|---|---|---|---|
| Business and other management consultancy activities | 12,416 | 16,650 | 6,215 | 3,397 | 1,159 | 1,677 | 0! | no (pooled pre 35,281, post 2,836) |
| Physiotherapy activities | 1,100 | 2,303 | 767 | 475 | 110~ | 145~ | 0! | no (pooled pre 4,170, post 255) |
| Activities of head offices | 1,729 | 886 | 537 | 73! | 110~ | 124~ | 0! | no (pooled pre 3,152, post 235) |
| Activities of call centres | 943 | 1,063 | 537 | 146~ | 14! | 62! | 0! | no (pooled pre 2,543, post 76) |
| Warehousing and storage | 786 | 531 | 537 | 219 | 69! | 166~ | 0! | no (pooled pre 1,854, post 235) |
| Publishing of journals and periodicals | 314~ | 1,240 | 307 | 256 | 28! | 41! | 0! | no (pooled pre 1,861, post 69) |
| Activities of advertising agencies | 314~ | 1,063 | 460 | 110~ | 55! | 41! | 0! | no (pooled pre 1,837, post 97) |
| Research and experimental development on social science | 0! | 1,240 | 460 | 73! | 110~ | 83! | 0! | no (pooled pre 1,700, post 193) |
| Technical testing and analysis | 472 | 1,063 | 153~ | 110~ | 55! | 41! | 0! | no (pooled pre 1,688, post 97) |
| Computer programming activities | 629 | 709 | 384 | 37! | 83! | 21! | 0! | no (pooled pre 1,721, post 103) |
| Restaurant activities | 157~ | 1,063 | 307 | 110~ | 41! | 83! | 0! | no (pooled pre 1,527, post 124) |
| Regulation of health care, education, cultural services | 314~ | 531 | 460 | 183~ | 55! | 124~ | 0! | no (pooled pre 1,306, post 179) |

Sectors meeting the rule: **0** of the 12 most frequent labels (`*` marks the event month).

**Pre-specified groups** (all labels of the group added up, same rule):

| Group | 2024-12 | 2025-01 | 2025-02 | 2025-03* | 2025-04 | 2025-05 | 2025-06 | Rule met? |
|---|---|---|---|---|---|---|---|---|
| Exposed manufacturing (primary): all 'Manufactur... | 3,772 | 4,074 | 1,381 | 584 | 428 | 435 | 0! | no (pooled pre 9,227, post 862) |
| Narrow metals (secondary, descriptive only) | 472 | 531 | 153~ | 37! | 110~ | 62! | 0! | no (pooled pre 1,156, post 172) |

### jobs.de  (pre: 2024-12, 2025-01, 2025-02; event month: 2025-03; post: 2025-04)

| Month | Postings | Sampled | With sector tag | With text | Est. tagged | Est. with text |
|---|---:|---:|---:|---:|---:|---:|
| 2024-12 | 4,029 | 300 | 81% | 100% | 3,250 | 4,029 |
| 2025-01 | 1,690 | 300 | 61% | 94% | 1,037 | 1,594 |
| 2025-02 | 2,572 | 300 | 86% | 99% | 2,212 | 2,555 |
| 2025-03 | 1,691 | 300 | 90% | 100% | 1,522 | 1,691 |
| 2025-04 | 597 | 300 | 91% | 100% | 543 | 597 |

| Sector (first tag) | 2024-12 | 2025-01 | 2025-02 | 2025-03* | 2025-04 | Rule met? |
|---|---|---|---|---|---|---|
| Business and other management consultancy activities | 94! | 39! | 171 | 28! | 16! | no (pooled pre 305, post 16) |
| Hospital activities | 67! | 6! | 9! | 180 | 70! | no (pooled pre 81, post 70) |
| CONSTRUCTION | 0! | 11! | 274 | 0! | 0! | no (pooled pre 286, post 0) |
| Technical testing and analysis | 81! | 39! | 69! | 79! | 10! | no (pooled pre 189, post 10) |
| Activities of head offices | 161~ | 28! | 34! | 11! | 8! | no (pooled pre 224, post 8) |
| Other education n.e.c. | 94! | 68! | 34! | 28! | 10! | no (pooled pre 196, post 10) |
| Accounting, bookkeeping and auditing activities; tax co | 54! | 23! | 94! | 34! | 10! | no (pooled pre 171, post 10) |
| Physiotherapy activities | 81! | 11! | 34! | 51! | 10! | no (pooled pre 126, post 10) |
| Manufacture of leather and related products of other ma | 107~ | 0! | 43! | 17! | 4! | no (pooled pre 150, post 4) |
| Educational support activities n.e.c. | 94! | 28! | 34! | 6! | 8! | no (pooled pre 156, post 8) |
| Other monetary intermediation | 81! | 17! | 51! | 17! | 4! | no (pooled pre 149, post 4) |
| Activities of religious organisations | 0! | 0! | 0! | 141~ | 2! | no (pooled pre 0, post 2) |

Sectors meeting the rule: **0** of the 12 most frequent labels (`*` marks the event month).

**Pre-specified groups** (all labels of the group added up, same rule):

| Group | 2024-12 | 2025-01 | 2025-02 | 2025-03* | 2025-04 | Rule met? |
|---|---|---|---|---|---|---|
| Exposed manufacturing (primary): all 'Manufactur... | 551 | 118~ | 352 | 180 | 64! | no (pooled pre 1,020, post 64) |
| Narrow metals (secondary, descriptive only) | 94! | 23! | 43! | 17! | 4! | no (pooled pre 159, post 4) |

