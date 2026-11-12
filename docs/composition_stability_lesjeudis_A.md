# Composition stability: lesjeudis input A

Days 2024-08-11 to 2025-09-30: 286 sampled days, 18,625 postings taken (duplicates removed: 1329). Distance = Jensen-Shannon (0 to 1); p from 1000 shuffles of whole days; excess = distance minus the mean shuffled distance.

## 0. Field fill and volume by quarter

| quarter | sampled days | postings taken | mean day total | sector field filled | labelled by script 92 |
|---|---|---|---|---|---|
| 2024-Q3 | 49 | 3,566 | 251 | 95% | 100% |
| 2024-Q4 | 92 | 5,691 | 135 | 95% | 100% |
| 2025-Q1 | 49 | 2,985 | 126 | 94% | 100% |
| 2025-Q2 | 44 | 3,213 | 155 | 97% | 100% |
| 2025-Q3 | 52 | 3,170 | 144 | 97% | 100% |

## 1. Low-volume against high-volume days

Thirds by day total: low = 95 days (median total 60), high = 95 days (median total 235).

| composition | JS | shuffled mean | excess | p |
|---|---|---|---|---|
| cluster | 0.027 | 0.015 | 0.012 | 0.001 |
| channel | 0.001 | 0.001 | -0.000 | 0.354 |
| sector | 0.031 | 0.027 | 0.005 | 0.019 |

Same split inside each calendar quarter (days ranked within the quarter; thirds pooled across quarters). A trend in the mix would not survive this.

| composition | JS | shuffled mean | excess | p |
|---|---|---|---|---|
| cluster | 0.020 | 0.015 | 0.004 | 0.038 |
| channel | 0.001 | 0.001 | 0.000 | 0.298 |
| sector | 0.031 | 0.027 | 0.004 | 0.031 |

## 2. Jumps in the day total (mean of the next 14 sampled days / mean of the previous 14: >= 3 or <= 1/3)

0 jumps compared (14 sampled days before against 14 after, the strongest change in each stretch); 8 stretches with no jump (ratio within 1/1.5 to 1.5, no overlap) kept as placebo.

| first day after the jump | ratio | mean day total before -> after | cluster: JS (excess, p) | channel: JS (excess, p) | sector: JS (excess, p) |
|---|---|---|---|---|---|

## 3. Placebo: stretches without a jump

| composition | stretches | median JS | 95th percentile JS | median excess | share with p < 0.05 |
|---|---|---|---|---|---|
| cluster | 8 | 0.087 | 0.112 | +0.004 | 0% |
| channel | 8 | 0.004 | 0.022 | +0.001 | 12% |
| sector | 8 | 0.093 | 0.114 | +0.003 | 0% |

## Reading notes

- A jump whose JS and excess clearly exceed the placebo 95th percentile, with p near 0, is evidence that the mix moved with the volume. Jumps inside the placebo range are consistent with volume only.
- Real day-to-day variation (weekday effects, seasonality, events) is inside the placebo, so a stable-mechanism board will not show 5% rejections exactly; compare the jumps with the placebo, not with 0.05.
- Page clumping: the shuffle moves whole days, so it already includes the clumping within a page.
- The cluster dimension depends on script 92 (clusters are fitted on all postings); the channel and sector dimensions do not.
- Passing the test does not show that Skillab's ingestion is random; failing it shows that it was not stable.
