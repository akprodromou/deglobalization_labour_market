# Sector-month counts around the primary events (Month 3, step 1)

Rule: a sector is usable for an event in a source only if its estimated number of postings is at least **100** in every pre-window month and every post-window month (event month left out). A description counts as text from 200 characters. Estimates come from page samples (see the script's header for limits); `!` = below the minimum, `~` = the 95% interval straddles the minimum. Only the first sector tag of a posting is used, duplicates are not removed, so the counts are optimistic upper bounds. These are estimates for the whole source. The rule is applied to the postings that are actually downloaded and analysed, so the download size per month has to be chosen so that every sector reaches the minimum (for a sector with a share s of a month's postings, about 100/s postings must be downloaded).

## EU steel import regulation, Parliament vote, 19 May 2026

### jobbland.se  (pre: 2026-01, 2026-02, 2026-03, 2026-04; event month: 2026-05; post: 2026-06, 2026-07, 2026-08)

| Month | Postings | Sampled | With sector tag | With text | Est. tagged | Est. with text |
|---|---:|---:|---:|---:|---:|---:|
| 2026-01 | 48,511 | 1500 | 0% | 100% | 0 | 48,479 |
| 2026-02 | 55,457 | 1500 | 0% | 100% | 0 | 55,457 |
| 2026-03 | 62,392 | 1500 | 0% | 100% | 0 | 62,392 |
| 2026-04 | 47,721 | 1500 | 0% | 100% | 0 | 47,657 |
| 2026-05 | 53,794 | 1500 | 0% | 100% | 0 | 53,794 |
| 2026-06 | 46,127 | 1500 | 0% | 100% | 0 | 46,127 |
| 2026-07 | 31,166 | 1500 | 0% | 100% | 0 | 31,124 |
| 2026-08 | 40,875 | 1500 | 0% | 100% | 0 | 40,848 |

**No sector tags in any sampled month of this window.** Sector must come from the text classifier; the usable ceiling is the 'Est. with text' column above.

