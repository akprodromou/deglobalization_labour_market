# Sampling check: jobbland_text

Indicator: any Month 3 flag. 53,959 postings after 3,578 exact duplicates, 950 sampled days, 1000 draws. Intervals are 95%; widths are in share units (0.01 = 1 percentage point).

## Employer concentration inside a day

Cluster key: text. Postings without a key: 0.0%. Each of those counts as its own cluster.

| measure | 10th pct of days | median day | 90th pct of days |
|---|---|---|---|
| top employer's share of the day's page | 2.1% | 5.9% | 33.3% |
| effective number of employers per page | 4.0 | 46.5 | 90.4 |

## Interval widths per quarter

A = postings redrawn inside each day; B = employers redrawn inside each day; C = whole ISO weeks redrawn.

| quarter | days | weeks | postings | share | width A | width B | width C | B/A | C/A |
|---|---|---|---|---|---|---|---|---|---|
| 2024-Q1 | 84 | 13 | 701 | 0.054 | 0.0295 | 0.0339 | 0.0416 | 1.15 | 1.41 |
| 2024-Q2 | 90 | 13 | 2417 | 0.038 | 0.0170 | 0.0181 | 0.0138 | 1.07 | 0.81 |
| 2024-Q3 | 92 | 14 | 5369 | 0.046 | 0.0151 | 0.0180 | 0.0177 | 1.19 | 1.18 |
| 2024-Q4 | 92 | 14 | 8172 | 0.042 | 0.0107 | 0.0106 | 0.0164 | 0.99 | 1.54 |
| 2025-Q1 | 84 | 14 | 5515 | 0.038 | 0.0124 | 0.0124 | 0.0119 | 1.00 | 0.96 |
| 2025-Q2 | 81 | 14 | 2010 | 0.046 | 0.0232 | 0.0309 | 0.0914 | 1.33 | 3.94 |
| 2025-Q3 | 90 | 14 | 2900 | 0.046 | 0.0246 | 0.0245 | 0.0202 | 0.99 | 0.82 |
| 2025-Q4 | 92 | 14 | 5405 | 0.077 | 0.0319 | 0.0339 | 0.0594 | 1.06 | 1.87 |
| 2026-Q1 | 90 | 14 | 7944 | 0.036 | 0.0131 | 0.0136 | 0.0136 | 1.04 | 1.04 |
| 2026-Q2 | 91 | 14 | 7744 | 0.034 | 0.0098 | 0.0094 | 0.0090 | 0.96 | 0.91 |
| 2026-Q3 | 64 | 10 | 5782 | 0.037 | 0.0125 | 0.0125 | 0.0154 | 1.00 | 1.23 |

Reading: B/A above 1 means the within-day interval is too narrow because of employer clumping (design effect = (B/A) squared). C/A above B/A means day-to-day variation adds to it. Quarters with few weeks give noisy C.

## Weeks furthest from their quarter's share

Weeks with at least 20 sampled postings. Full series in data/tagged/weekly_share_jobbland_text.csv.

| week | quarter | days | postings | flagged | weekly share | quarter share | weighted postings |
|---|---|---|---|---|---|---|---|
| 2025-W16 | 2025-Q2 | 7 | 358 | 56 | 0.179 | 0.046 | 826 |
| 2024-W12 | 2024-Q1 | 7 | 80 | 9 | 0.113 | 0.054 | 80 |
| 2025-W47 | 2025-Q4 | 7 | 380 | 8 | 0.021 | 0.077 | 925 |
| 2025-W39 | 2025-Q3 | 7 | 258 | 26 | 0.101 | 0.046 | 273 |
| 2024-W05 | 2024-Q1 | 7 | 60 | 0 | 0.000 | 0.054 | 61 |
| 2025-W48 | 2025-Q4 | 7 | 397 | 13 | 0.023 | 0.077 | 1,283 |
| 2025-W28 | 2025-Q3 | 7 | 40 | 4 | 0.098 | 0.046 | 41 |
| 2025-W15 | 2025-Q2 | 5 | 23 | 0 | 0.000 | 0.046 | 23 |
| 2025-W25 | 2025-Q2 | 7 | 33 | 0 | 0.000 | 0.046 | 34 |
| 2025-W27 | 2025-Q2 | 5 | 51 | 0 | 0.000 | 0.046 | 58 |
