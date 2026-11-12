# Composition stability: jobbland input A

Days 2024-01-01 to 2026-09-02: 950 sampled days, 53,959 postings taken (duplicates removed: 3578). Distance = Jensen-Shannon (0 to 1); p from 1000 shuffles of whole days; excess = distance minus the mean shuffled distance.

## 0. Field fill and volume by quarter

| quarter | sampled days | postings taken | mean day total | sector field filled | labelled by script 92 |
|---|---|---|---|---|---|
| 2024-Q1 | 84 | 701 | 9 | 91% | 100% |
| 2024-Q2 | 90 | 2,417 | 60 | 87% | 100% |
| 2024-Q3 | 92 | 5,369 | 177 | 89% | 100% |
| 2024-Q4 | 92 | 8,172 | 1,579 | 88% | 100% |
| 2025-Q1 | 84 | 5,515 | 1,037 | 89% | 100% |
| 2025-Q2 | 81 | 2,010 | 129 | 82% | 100% |
| 2025-Q3 | 90 | 2,900 | 83 | 52% | 100% |
| 2025-Q4 | 92 | 5,405 | 367 | 0% | 100% |
| 2026-Q1 | 90 | 7,944 | 1,848 | 0% | 100% |
| 2026-Q2 | 91 | 7,744 | 1,622 | 0% | 100% |
| 2026-Q3 | 64 | 5,782 | 1,135 | 0% | 100% |

Postings without a title: 1,389 of 53,959 taken.

Share of postings without a title by month, before any exclusion (taken; weighted):

| month | postings taken | without title (taken) | without title (weighted) |
|---|---|---|---|
| 2024-01 | 185 | 0% | 0% |
| 2024-02 | 227 | 0% | 0% |
| 2024-03 | 289 | 0% | 0% |
| 2024-04 | 317 | 0% | 0% |
| 2024-05 | 993 | 0% | 0% |
| 2024-06 | 1,107 | 0% | 0% |
| 2024-07 | 1,405 | 0% | 0% |
| 2024-08 | 1,777 | 0% | 0% |
| 2024-09 | 2,187 | 0% | 0% |
| 2024-10 | 2,759 | 0% | 0% |
| 2024-11 | 2,828 | 0% | 0% |
| 2024-12 | 2,585 | 0% | 0% |
| 2025-01 | 2,847 | 0% | 0% |
| 2025-02 | 1,478 | 0% | 0% |
| 2025-03 | 1,190 | 0% | 0% |
| 2025-04 | 798 | 0% | 0% |
| 2025-05 | 1,088 | 0% | 0% |
| 2025-06 | 124 | 0% | 0% |
| 2025-07 | 361 | 0% | 0% |
| 2025-08 | 1,088 | 0% | 0% |
| 2025-09 | 1,451 | 0% | 0% |
| 2025-10 | 1,447 | 0% | 0% |
| 2025-11 | 1,590 | 0% | 0% |
| 2025-12 | 2,368 | 44% | 54% |
| 2026-01 | 2,764 | 13% | 10% |
| 2026-02 | 2,537 | 0% | 0% |
| 2026-03 | 2,643 | 0% | 0% |
| 2026-04 | 2,520 | 0% | 0% |
| 2026-05 | 2,679 | 0% | 0% |
| 2026-06 | 2,545 | 0% | 0% |
| 2026-07 | 2,794 | 0% | 0% |
| 2026-08 | 2,836 | 0% | 0% |
| 2026-09 | 152 | 0% | 0% |

## 1. Low-volume against high-volume days

Thirds by day total: low = 316 days (median total 8), high = 316 days (median total 2,239).

| composition | JS | shuffled mean | excess | p |
|---|---|---|---|---|
| cluster | 0.141 | 0.035 | 0.106 | 0.001 |
| channel | 0.002 | 0.001 | 0.001 | 0.011 |
| sector | 0.084 | 0.035 | 0.049 | 0.001 |

Same split inside each calendar quarter AND weekday (days ranked within the same quarter and weekday; thirds pooled). A trend in the mix, or a weekend/weekday difference, would not survive this.

| composition | JS | shuffled mean | excess | p |
|---|---|---|---|---|
| cluster | 0.016 | 0.011 | 0.005 | 0.008 |
| channel | 0.001 | 0.000 | 0.000 | 0.101 |
| sector | 0.041 | 0.014 | 0.028 | 0.001 |

## 2. Jumps in the day total (mean of the next 14 sampled days / mean of the previous 14: >= 3 or <= 1/3)

15 jumps compared (14 sampled days before against 14 after, the strongest change in each stretch); 17 stretches with no jump (ratio within 1/1.5 to 1.5, no overlap) kept as placebo.

| first day after the jump | ratio | mean day total before -> after | cluster: JS (excess, p) | channel: JS (excess, p) | sector: JS (excess, p) |
|---|---|---|---|---|---|
| 2024-05-03 | 8.0 | 8 -> 62 | 0.403 (+0.055, p=0.076) | 0.015 (-0.003, p=0.549) | 0.380 (+0.004, p=0.455) |
| 2024-09-30 | 3.3 | 342 -> 1,139 | 0.111 (+0.005, p=0.275) | 0.003 (+0.002, p=0.083) | 0.111 (+0.007, p=0.163) |
| 2024-12-23 | 0.3 | 2,118 -> 539 | 0.105 (+0.032, p=0.001) | 0.008 (+0.006, p=0.001) | 0.121 (+0.020, p=0.014) |
| 2025-01-06 | 3.3 | 539 -> 1,802 | 0.089 (+0.009, p=0.139) | 0.003 (+0.001, p=0.228) | 0.111 (+0.006, p=0.223) |
| 2025-02-15 | 0.0 | 1,635 -> 10 | 0.420 (+0.066, p=0.025) | 0.004 (-0.006, p=0.870) | 0.334 (+0.034, p=0.153) |
| 2025-03-05 | 26.0 | 10 -> 251 | 0.350 (-0.021, p=0.729) | 0.006 (-0.003, p=0.637) | 0.283 (-0.005, p=0.561) |
| 2025-04-06 | 0.1 | 563 -> 62 | 0.208 (-0.034, p=0.931) | 0.054 (+0.022, p=0.032) | 0.192 (-0.007, p=0.642) |
| 2025-04-29 | 6.6 | 62 -> 409 | 0.267 (+0.014, p=0.265) | 0.051 (+0.020, p=0.031) | 0.222 (+0.002, p=0.439) |
| 2025-05-17 | 0.0 | 306 -> 10 | 0.424 (+0.048, p=0.112) | 0.014 (+0.003, p=0.280) | 0.321 (-0.018, p=0.678) |
| 2025-07-16 | 3.1 | 8 -> 25 | 0.426 (+0.061, p=0.055) | 0.023 (+0.009, p=0.170) | 0.653 (+0.334, p=0.001) |
| 2025-08-07 | 6.3 | 24 -> 154 | 0.290 (-0.003, p=0.557) | 0.008 (+0.001, p=0.371) | 0.209 (-0.018, p=0.734) |
| 2025-09-17 | 0.2 | 212 -> 37 | 0.235 (+0.033, p=0.029) | 0.016 (+0.011, p=0.013) | 0.415 (+0.290, p=0.001) |
| 2025-12-09 | 7.0 | 233 -> 1,622 | 0.301 (+0.181, p=0.001) | 0.004 (+0.001, p=0.248) | 0.001 (+0.001, p=0.404) |
| 2025-12-23 | 0.3 | 1,622 -> 508 | 0.132 (+0.036, p=0.001) | 0.004 (+0.001, p=0.188) | 0.000 (-0.000, p=1.001) |
| 2026-01-06 | 3.4 | 508 -> 1,744 | 0.151 (+0.043, p=0.001) | 0.003 (+0.000, p=0.330) | 0.000 (-0.000, p=1.001) |

## 3. Placebo: stretches without a jump

| composition | stretches | median JS | 95th percentile JS | median excess | share with p < 0.05 |
|---|---|---|---|---|---|
| cluster | 17 | 0.107 | 0.281 | +0.001 | 6% |
| channel | 17 | 0.003 | 0.011 | -0.000 | 0% |
| sector | 17 | 0.005 | 0.358 | +0.000 | 12% |

## Reading notes

- A jump whose JS and excess clearly exceed the placebo 95th percentile, with p near 0, is evidence that the mix moved with the volume. Jumps inside the placebo range are consistent with volume only.
- Real day-to-day variation (weekday effects, seasonality, events) is inside the placebo, so a stable-mechanism board will not show 5% rejections exactly; compare the jumps with the placebo, not with 0.05.
- Page clumping: the shuffle moves whole days, so it already includes the clumping within a page.
- The cluster dimension depends on script 92 (clusters are fitted on all postings); the channel and sector dimensions do not.
- Passing the test does not show that Skillab's ingestion is random; failing it shows that it was not stable.
