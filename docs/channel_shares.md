# Weighted channel shares

Tags: `tags_qwen2.5_7b_tagging_v8.jsonl`. Share = weighted share of all postings (flagged or not) with the channel as tag. 95% intervals from 1000 bootstrap draws inside each day. Unflagged and invalid-answer postings count as none (9 invalid answers). Values in per cent.

## Events: Any intensity

| Event | Channel | Before | After | Change (points) | 95% interval of the change |
|---|---|---:|---:|---:|---|
| CRMA | reshoring | 0.45 | 0.24 | -0.21 | -0.61 to +0.17 |
| CRMA | defense | 1.94 | 1.59 | -0.35 | -1.37 to +0.59 |
| CRMA | critical materials | 0.17 | 0.04 | -0.13 | -0.33 to +0.05 |
| CRMA | energy security | 0.74 | 0.45 | -0.29 | -0.99 to +0.23 |
| CRMA | trade compliance | 0.19 | 0.04 | -0.15 | -0.38 to +0.02 |
| CRMA | diversification | 0.00 | 0.00 | +0.00 | +0.00 to +0.00 |
| AccelerateEU | reshoring | 0.06 | 0.08 | +0.01 | -0.08 to +0.12 |
| AccelerateEU | defense | 2.34 | 2.66 | +0.32 | -0.26 to +0.86 |
| AccelerateEU | critical materials | 0.08 | 0.00 | -0.08 | -0.15 to -0.02 |
| AccelerateEU | energy security | 0.44 | 0.47 | +0.04 | -0.21 to +0.29 |
| AccelerateEU | trade compliance | 0.21 | 0.18 | -0.03 | -0.19 to +0.13 |
| AccelerateEU | diversification | 0.00 | 0.00 | +0.00 | +0.00 to +0.00 |

## Events: Medium or high intensity only

| Event | Channel | Before | After | Change (points) | 95% interval of the change |
|---|---|---:|---:|---:|---|
| CRMA | reshoring | 0.45 | 0.21 | -0.24 | -0.63 to +0.14 |
| CRMA | defense | 0.74 | 0.71 | -0.03 | -0.70 to +0.52 |
| CRMA | critical materials | 0.13 | 0.04 | -0.08 | -0.28 to +0.07 |
| CRMA | energy security | 0.43 | 0.14 | -0.29 | -0.85 to +0.11 |
| CRMA | trade compliance | 0.19 | 0.03 | -0.16 | -0.38 to +0.00 |
| CRMA | diversification | 0.00 | 0.00 | +0.00 | +0.00 to +0.00 |
| AccelerateEU | reshoring | 0.05 | 0.08 | +0.03 | -0.06 to +0.13 |
| AccelerateEU | defense | 1.25 | 1.46 | +0.22 | -0.18 to +0.64 |
| AccelerateEU | critical materials | 0.08 | 0.00 | -0.08 | -0.15 to -0.02 |
| AccelerateEU | energy security | 0.29 | 0.34 | +0.05 | -0.14 to +0.24 |
| AccelerateEU | trade compliance | 0.14 | 0.16 | +0.03 | -0.12 to +0.17 |
| AccelerateEU | diversification | 0.00 | 0.00 | +0.00 | +0.00 to +0.00 |

## Postings behind each window

| Window | Days | Postings taken | Weighted postings (population) |
|---|---:|---:|---:|
| CRMA before | 86 | 1,447 | 2,146 |
| CRMA after | 90 | 3,785 | 8,105 |
| AccelerateEU before | 90 | 7,843 | 165,853 |
| AccelerateEU after | 90 | 7,779 | 138,270 |

Days with postings in a window can be fewer than the window length (the corpus ends in September 2026). A window with a few hundred postings gives wide intervals: read the interval, not the point change.

## Monthly shares, any intensity

| Month | Taken | reshoring | defense | critical materials | energy security | trade compliance | diversification |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2024-01 | 185 | 0.60 | 0.52 | 0.00 | 0.00 | 1.05 | 0.00 |
| 2024-02 | 227 | 0.47 | 0.41 | 0.00 | 1.22 | 0.41 | 0.00 |
| 2024-03 | 289 | 0.00 | 3.45 | 0.34 | 1.03 | 0.34 | 0.00 |
| 2024-04 | 317 | 1.56 | 0.91 | 0.00 | 0.25 | 0.52 | 0.00 |
| 2024-05 | 993 | 0.26 | 1.47 | 0.13 | 0.47 | 0.05 | 0.00 |
| 2024-06 | 1,107 | 0.25 | 1.59 | 0.00 | 0.50 | 0.00 | 0.00 |
| 2024-07 | 1,405 | 0.15 | 1.88 | 0.06 | 0.74 | 0.00 | 0.00 |
| 2024-08 | 1,777 | 0.45 | 1.87 | 0.15 | 0.17 | 0.21 | 0.00 |
| 2024-09 | 2,187 | 0.12 | 2.52 | 0.03 | 1.00 | 0.01 | 0.00 |
| 2024-10 | 2,759 | 0.09 | 2.41 | 0.15 | 0.57 | 0.31 | 0.00 |
| 2024-11 | 2,828 | 0.00 | 2.31 | 0.09 | 0.23 | 0.26 | 0.00 |
| 2024-12 | 2,585 | 0.00 | 3.40 | 0.10 | 0.51 | 0.28 | 0.00 |
| 2025-01 | 2,847 | 0.10 | 2.37 | 0.15 | 0.73 | 0.33 | 0.00 |
| 2025-02 | 1,478 | 0.00 | 2.38 | 0.17 | 0.40 | 0.29 | 0.00 |
| 2025-03 | 1,190 | 0.00 | 1.71 | 0.18 | 0.74 | 0.20 | 0.18 |
| 2025-04 | 798 | 0.00 | 3.20 | 0.00 | 0.00 | 0.62 | 0.00 |
| 2025-05 | 1,088 | 0.07 | 2.53 | 0.00 | 0.47 | 0.16 | 0.00 |
| 2025-06 | 124 | 0.00 | 1.39 | 0.00 | 0.76 | 0.00 | 0.00 |
| 2025-07 | 361 | 0.00 | 1.35 | 0.00 | 0.94 | 0.00 | 0.00 |
| 2025-08 | 1,088 | 0.00 | 3.28 | 0.00 | 0.77 | 0.19 | 0.00 |
| 2025-09 | 1,451 | 0.03 | 3.51 | 0.00 | 0.62 | 0.45 | 0.00 |
| 2025-10 | 1,447 | 0.20 | 2.82 | 0.00 | 0.07 | 0.13 | 0.00 |
| 2025-11 | 1,590 | 0.00 | 2.10 | 0.13 | 0.19 | 0.28 | 0.00 |
| 2025-12 | 2,368 | 0.22 | 6.43 | 0.01 | 0.65 | 0.19 | 0.00 |
| 2026-01 | 2,764 | 0.09 | 2.53 | 0.40 | 0.41 | 0.16 | 0.00 |
| 2026-02 | 2,537 | 0.10 | 2.58 | 0.06 | 0.33 | 0.06 | 0.00 |
| 2026-03 | 2,643 | 0.00 | 2.24 | 0.08 | 0.26 | 0.29 | 0.00 |
| 2026-04 | 2,520 | 0.11 | 2.11 | 0.02 | 0.81 | 0.29 | 0.00 |
| 2026-05 | 2,679 | 0.00 | 2.06 | 0.00 | 0.56 | 0.26 | 0.00 |
| 2026-06 | 2,545 | 0.10 | 2.96 | 0.00 | 0.51 | 0.16 | 0.00 |
| 2026-07 | 2,794 | 0.19 | 2.68 | 0.00 | 0.22 | 0.15 | 0.00 |
| 2026-08 | 2,836 | 0.12 | 2.55 | 0.11 | 0.65 | 0.27 | 0.00 |
| 2026-09 | 152 | 0.00 | 0.45 | 0.00 | 2.04 | 0.80 | 0.00 |

Intervals for every month are in the CSV.