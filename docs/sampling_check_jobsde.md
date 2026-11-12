# Sampling check: jobsde

Indicator: any Month 3 flag. 12,243 postings after 2,041 exact duplicates, 221 sampled days, 1000 draws. Intervals are 95%; widths are in share units (0.01 = 1 percentage point).

## Employer concentration inside a day

Cluster key: organization. Postings without a key: 99.8%. Each of those counts as its own cluster.

| measure | 10th pct of days | median day | 90th pct of days |
|---|---|---|---|
| top employer's share of the day's page | 1.1% | 1.9% | 6.7% |
| effective number of employers per page | 16.0 | 53.0 | 95.0 |

## Interval widths per quarter

A = postings redrawn inside each day; B = employers redrawn inside each day; C = whole ISO weeks redrawn.

| quarter | days | weeks | postings | share | width A | width B | width C | B/A | C/A |
|---|---|---|---|---|---|---|---|---|---|
| 2024-Q3 | 47 | 9 | 3253 | 0.014 | 0.0149 | 0.0162 | 0.0103 | 1.09 | 0.69 |
| 2024-Q4 | 91 | 14 | 5519 | 0.009 | 0.0055 | 0.0054 | 0.0065 | 0.98 | 1.19 |
| 2025-Q1 | 76 | 12 | 3122 | 0.007 | 0.0062 | 0.0059 | 0.0055 | 0.95 | 0.89 |

Reading: B/A above 1 means the within-day interval is too narrow because of employer clumping (design effect = (B/A) squared). C/A above B/A means day-to-day variation adds to it. Quarters with few weeks give noisy C.
