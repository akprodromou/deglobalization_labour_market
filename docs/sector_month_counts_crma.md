# Sector-month counts around the primary events (Month 3, step 1)

Rule: a sector is usable for an event in a source only if its estimated number of postings is at least **100** in every pre-window month and every post-window month (event month left out). A description counts as text from 200 characters. Estimates come from page samples (see the script's header for limits); `!` = below the minimum, `~` = the 95% interval straddles the minimum. Only the first sector tag of a posting is used, duplicates are not removed, so the counts are optimistic upper bounds. These are estimates for the whole source. The rule is applied to the postings that are actually downloaded and analysed, so the download size per month has to be chosen so that every sector reaches the minimum (for a sector with a share s of a month's postings, about 100/s postings must be downloaded).

## EU Critical Raw Materials Act, 23 May 2024

### jobbland.se  (pre: 2024-01, 2024-02, 2024-03, 2024-04; event month: 2024-05; post: 2024-06, 2024-07, 2024-08)

| Month | Postings | Sampled | With sector tag | With text | Est. tagged | Est. with text |
|---|---:|---:|---:|---:|---:|---:|
| 2024-01 | 191 | 191 | 88% | 100% | 169 | 191 |
| 2024-02 | 246 | 200 | 92% | 100% | 225 | 245 |
| 2024-03 | 292 | 200 | 96% | 100% | 280 | 292 |
| 2024-04 | 410 | 300 | 73% | 100% | 299 | 410 |
| 2024-05 | 2,116 | 300 | 87% | 99% | 1,848 | 2,102 |
| 2024-06 | 2,879 | 300 | 84% | 100% | 2,418 | 2,879 |
| 2024-07 | 2,060 | 300 | 85% | 100% | 1,758 | 2,053 |
| 2024-08 | 4,184 | 300 | 85% | 99% | 3,556 | 4,156 |

| Sector (first tag) | 2024-01 | 2024-02 | 2024-03 | 2024-04 | 2024-05* | 2024-06 | 2024-07 | 2024-08 | Rule met? |
|---|---|---|---|---|---|---|---|---|---|
| Business and other management consultancy activities | 49! | 28! | 79! | 53! | 339 | 374 | 378 | 683 | no (pooled pre 209, post 1,435) |
| Computer programming activities | 9! | 16! | 19! | 14! | 169 | 96! | 96! | 139~ | no (pooled pre 58, post 332) |
| Activities of head offices | 12! | 18! | 15! | 12! | 106~ | 77! | 62! | 98! | no (pooled pre 57, post 236) |
| Research and experimental development on social science | 7! | 1! | 3! | 7! | 56! | 106~ | 27! | 112~ | no (pooled pre 18, post 245) |
| Activities of advertising agencies | 2! | 2! | 4! | 4! | 14! | 173 | 55! | 42! | no (pooled pre 13, post 270) |
| Engineering activities and related technical consultanc | 3! | 2! | 4! | 5! | 14! | 10! | 34! | 167~ | no (pooled pre 15, post 211) |
| Hospital activities | 2! | 4! | 3! | 7! | 0! | 67! | 27! | 112~ | no (pooled pre 15, post 206) |
| MANUFACTURING | 3! | 10! | 3! | 11! | 35! | 106~ | 7! | 42! | no (pooled pre 27, post 154) |
| Restaurant activities | 0! | 1! | 3! | 0! | 21! | 86! | 41! | 56! | no (pooled pre 4, post 183) |
| Warehousing and storage | 1! | 6! | 6! | 3! | 49! | 38! | 21! | 84! | no (pooled pre 16, post 143) |
| Manufacture of electronic components and boards | 1! | 5! | 4! | 3! | 35! | 38! | 34! | 84! | no (pooled pre 13, post 156) |
| Warehousing, storage and support activities for transpo | 1! | 7! | 3! | 1! | 106~ | 29! | 48! | 0! | no (pooled pre 13, post 77) |

Sectors meeting the rule: **0** of the 12 most frequent labels (`*` marks the event month).

