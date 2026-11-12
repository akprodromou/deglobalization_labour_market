# Sampling check: lesjeudis

Indicator: any Month 3 flag. 18,625 postings after 1,329 exact duplicates, 286 sampled days, 1000 draws. Intervals are 95%; widths are in share units (0.01 = 1 percentage point).

## Employer concentration inside a day

Cluster key: organization. Postings without a key: 100.0%. Each of those counts as its own cluster.

| measure | 10th pct of days | median day | 90th pct of days |
|---|---|---|---|
| top employer's share of the day's page | 1.0% | 1.3% | 5.7% |
| effective number of employers per page | 17.5 | 74.5 | 98.0 |

## Interval widths per quarter

A = postings redrawn inside each day; B = employers redrawn inside each day; C = whole ISO weeks redrawn.

| quarter | days | weeks | postings | share | width A | width B | width C | B/A | C/A |
|---|---|---|---|---|---|---|---|---|---|
| 2024-Q3 | 49 | 9 | 3566 | 0.149 | 0.0286 | 0.0296 | 0.0729 | 1.03 | 2.55 |
| 2024-Q4 | 92 | 14 | 5691 | 0.094 | 0.0154 | 0.0144 | 0.0400 | 0.94 | 2.60 |
| 2025-Q1 | 49 | 10 | 2985 | 0.095 | 0.0225 | 0.0229 | 0.0623 | 1.02 | 2.78 |
| 2025-Q2 | 44 | 11 | 3213 | 0.161 | 0.0331 | 0.0310 | 0.0714 | 0.94 | 2.16 |
| 2025-Q3 | 52 | 13 | 3170 | 0.160 | 0.0281 | 0.0289 | 0.0752 | 1.03 | 2.67 |

Reading: B/A above 1 means the within-day interval is too narrow because of employer clumping (design effect = (B/A) squared). C/A above B/A means day-to-day variation adds to it. Quarters with few weeks give noisy C.

## Weeks furthest from their quarter's share

Weeks with at least 20 sampled postings. Full series in data/tagged/weekly_share_lesjeudis.csv.

| week | quarter | days | postings | flagged | weekly share | quarter share | weighted postings |
|---|---|---|---|---|---|---|---|
| 2025-W28 | 2025-Q3 | 1 | 74 | 25 | 0.338 | 0.160 | 74 |
| 2025-W19 | 2025-Q2 | 1 | 59 | 20 | 0.339 | 0.161 | 360 |
| 2025-W38 | 2025-Q3 | 5 | 104 | 1 | 0.006 | 0.160 | 224 |
| 2025-W26 | 2025-Q2 | 2 | 96 | 16 | 0.315 | 0.161 | 198 |
| 2024-W33 | 2024-Q3 | 5 | 106 | 16 | 0.294 | 0.149 | 508 |
| 2025-W40 | 2025-Q3 | 2 | 97 | 2 | 0.021 | 0.160 | 141 |
| 2024-W32 | 2024-Q3 | 1 | 98 | 28 | 0.286 | 0.149 | 731 |
| 2025-W39 | 2025-Q3 | 4 | 200 | 9 | 0.045 | 0.160 | 736 |
| 2024-W34 | 2024-Q3 | 7 | 575 | 132 | 0.243 | 0.149 | 1,194 |
| 2025-W04 | 2025-Q1 | 7 | 549 | 99 | 0.183 | 0.095 | 923 |
