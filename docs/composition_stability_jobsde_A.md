# Composition stability: jobsde input A

Days 2024-08-11 to 2025-04-09: 221 sampled days, 12,243 postings taken (duplicates removed: 2041). Distance = Jensen-Shannon (0 to 1); p from 1000 shuffles of whole days; excess = distance minus the mean shuffled distance.

## 0. Field fill and volume by quarter

| quarter | sampled days | postings taken | mean day total | sector field filled | labelled by script 92 |
|---|---|---|---|---|---|
| 2024-Q3 | 47 | 3,253 | 193 | 87% | 100% |
| 2024-Q4 | 91 | 5,519 | 204 | 80% | 100% |
| 2025-Q1 | 76 | 3,122 | 78 | 80% | 100% |
| 2025-Q2 | 7 | 349 | 85 | 93% | 100% |

## 1. Low-volume against high-volume days

Thirds by day total: low = 73 days (median total 35), high = 73 days (median total 234).

| composition | JS | shuffled mean | excess | p |
|---|---|---|---|---|
| cluster | 0.048 | 0.041 | 0.007 | 0.157 |
| channel | 0.000 | 0.001 | -0.001 | 0.794 |
| sector | 0.085 | 0.080 | 0.005 | 0.197 |

Same split inside each calendar quarter (days ranked within the quarter; thirds pooled across quarters). A trend in the mix would not survive this.

| composition | JS | shuffled mean | excess | p |
|---|---|---|---|---|
| cluster | 0.033 | 0.038 | -0.005 | 0.826 |
| channel | 0.001 | 0.001 | -0.000 | 0.439 |
| sector | 0.075 | 0.069 | 0.006 | 0.120 |

## 2. Jumps in the day total (mean of the next 14 sampled days / mean of the previous 14: >= 3 or <= 1/3)

2 jumps compared (14 sampled days before against 14 after, the strongest change in each stretch); 4 stretches with no jump (ratio within 1/1.5 to 1.5, no overlap) kept as placebo.

| first day after the jump | ratio | mean day total before -> after | cluster: JS (excess, p) | channel: JS (excess, p) | sector: JS (excess, p) |
|---|---|---|---|---|---|
| 2024-12-25 | 0.3 | 170 -> 46 | 0.071 (+0.016, p=0.091) | 0.001 (-0.001, p=0.846) | 0.248 (+0.021, p=0.133) |
| 2025-02-05 | 3.0 | 44 -> 131 | 0.144 (+0.036, p=0.076) | 0.001 (-0.000, p=0.362) | 0.195 (-0.008, p=0.643) |

## 3. Placebo: stretches without a jump

| composition | stretches | median JS | 95th percentile JS | median excess | share with p < 0.05 |
|---|---|---|---|---|---|
| cluster | 4 | 0.053 | 0.088 | +0.007 | 25% |
| channel | 4 | 0.002 | 0.005 | -0.001 | 0% |
| sector | 4 | 0.161 | 0.172 | +0.005 | 0% |

## Reading notes

- A jump whose JS and excess clearly exceed the placebo 95th percentile, with p near 0, is evidence that the mix moved with the volume. Jumps inside the placebo range are consistent with volume only.
- Real day-to-day variation (weekday effects, seasonality, events) is inside the placebo, so a stable-mechanism board will not show 5% rejections exactly; compare the jumps with the placebo, not with 0.05.
- Page clumping: the shuffle moves whole days, so it already includes the clumping within a page.
- The cluster dimension depends on script 92 (clusters are fitted on all postings); the channel and sector dimensions do not.
- Passing the test does not show that Skillab's ingestion is random; failing it shows that it was not stable.
