# Weighted channel shares

Tags: `tags_qwen2.5_7b_tagging_v9r.jsonl`. Share = weighted share of all postings (flagged or not) with the channel as tag. 95% intervals from 1000 bootstrap draws inside each day. Unflagged and invalid-answer postings count as none (10 invalid answers). Values in per cent.

## Events: Any intensity

| Event | Channel | Before | After | Change (points) | 95% interval of the change |
|---|---|---:|---:|---:|---|
| CRMA | reshoring | 0.57 | 0.45 | -0.12 | -0.61 to +0.33 |
| CRMA | defense | 1.94 | 1.53 | -0.41 | -1.34 to +0.51 |
| CRMA | critical materials | 0.13 | 0.03 | -0.10 | -0.29 to +0.06 |
| CRMA | energy security | 1.15 | 1.47 | +0.33 | -0.64 to +1.16 |
| CRMA | trade compliance | 0.19 | 0.03 | -0.16 | -0.35 to +0.00 |
| CRMA | diversification | 0.00 | 0.00 | +0.00 | +0.00 to +0.00 |
| AccelerateEU | reshoring | 0.01 | 0.06 | +0.04 | -0.02 to +0.11 |
| AccelerateEU | defense | 2.35 | 2.75 | +0.40 | -0.21 to +0.98 |
| AccelerateEU | critical materials | 0.03 | 0.00 | -0.03 | -0.09 to +0.00 |
| AccelerateEU | energy security | 0.58 | 0.61 | +0.03 | -0.25 to +0.29 |
| AccelerateEU | trade compliance | 0.21 | 0.18 | -0.03 | -0.18 to +0.13 |
| AccelerateEU | diversification | 0.00 | 0.00 | +0.00 | +0.00 to +0.00 |

## Events: Medium or high intensity only

| Event | Channel | Before | After | Change (points) | 95% interval of the change |
|---|---|---:|---:|---:|---|
| CRMA | reshoring | 0.57 | 0.34 | -0.22 | -0.70 to +0.19 |
| CRMA | defense | 0.65 | 0.70 | +0.05 | -0.58 to +0.61 |
| CRMA | critical materials | 0.13 | 0.03 | -0.10 | -0.29 to +0.06 |
| CRMA | energy security | 0.85 | 0.87 | +0.02 | -0.90 to +0.78 |
| CRMA | trade compliance | 0.14 | 0.03 | -0.12 | -0.29 to +0.03 |
| CRMA | diversification | 0.00 | 0.00 | +0.00 | +0.00 to +0.00 |
| AccelerateEU | reshoring | 0.01 | 0.06 | +0.04 | -0.02 to +0.11 |
| AccelerateEU | defense | 1.26 | 1.49 | +0.23 | -0.20 to +0.66 |
| AccelerateEU | critical materials | 0.03 | 0.00 | -0.03 | -0.09 to +0.00 |
| AccelerateEU | energy security | 0.36 | 0.34 | -0.02 | -0.22 to +0.18 |
| AccelerateEU | trade compliance | 0.11 | 0.15 | +0.04 | -0.10 to +0.17 |
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
| 2024-01 | 185 | 0.60 | 0.52 | 0.00 | 1.05 | 1.05 | 0.00 |
| 2024-02 | 227 | 0.88 | 0.41 | 0.00 | 0.41 | 0.41 | 0.00 |
| 2024-03 | 289 | 0.00 | 3.10 | 0.00 | 2.07 | 0.34 | 0.00 |
| 2024-04 | 317 | 1.56 | 1.17 | 0.00 | 0.25 | 0.52 | 0.00 |
| 2024-05 | 993 | 0.93 | 1.47 | 0.13 | 1.21 | 0.05 | 0.00 |
| 2024-06 | 1,107 | 0.36 | 1.41 | 0.00 | 1.37 | 0.00 | 0.00 |
| 2024-07 | 1,405 | 0.26 | 1.88 | 0.00 | 2.06 | 0.00 | 0.00 |
| 2024-08 | 1,777 | 0.53 | 1.87 | 0.15 | 0.92 | 0.18 | 0.00 |
| 2024-09 | 2,187 | 0.12 | 2.69 | 0.03 | 1.53 | 0.01 | 0.00 |
| 2024-10 | 2,759 | 0.05 | 2.42 | 0.01 | 1.05 | 0.31 | 0.00 |
| 2024-11 | 2,828 | 0.05 | 2.35 | 0.00 | 0.92 | 0.22 | 0.00 |
| 2024-12 | 2,585 | 0.07 | 3.41 | 0.00 | 1.21 | 0.21 | 0.00 |
| 2025-01 | 2,847 | 0.05 | 2.32 | 0.04 | 0.81 | 0.37 | 0.00 |
| 2025-02 | 1,478 | 0.10 | 2.47 | 0.00 | 1.37 | 0.29 | 0.00 |
| 2025-03 | 1,190 | 0.18 | 1.68 | 0.00 | 0.57 | 0.38 | 0.00 |
| 2025-04 | 798 | 0.00 | 3.27 | 0.00 | 0.61 | 0.62 | 0.00 |
| 2025-05 | 1,088 | 0.07 | 2.40 | 0.00 | 0.62 | 0.10 | 0.00 |
| 2025-06 | 124 | 0.00 | 1.39 | 0.00 | 0.76 | 0.00 | 0.00 |
| 2025-07 | 361 | 0.00 | 1.35 | 0.00 | 1.85 | 0.22 | 0.00 |
| 2025-08 | 1,088 | 0.00 | 3.28 | 0.00 | 1.22 | 0.18 | 0.00 |
| 2025-09 | 1,451 | 0.03 | 3.07 | 0.00 | 0.92 | 0.56 | 0.00 |
| 2025-10 | 1,447 | 0.13 | 2.82 | 0.00 | 0.29 | 0.13 | 0.00 |
| 2025-11 | 1,590 | 0.00 | 2.13 | 0.13 | 0.25 | 0.28 | 0.00 |
| 2025-12 | 2,368 | 0.22 | 6.67 | 0.00 | 1.27 | 0.10 | 0.00 |
| 2026-01 | 2,764 | 0.05 | 2.60 | 0.00 | 0.44 | 0.11 | 0.00 |
| 2026-02 | 2,537 | 0.00 | 2.64 | 0.06 | 0.59 | 0.06 | 0.00 |
| 2026-03 | 2,643 | 0.00 | 2.23 | 0.04 | 0.23 | 0.29 | 0.00 |
| 2026-04 | 2,520 | 0.00 | 2.14 | 0.00 | 1.02 | 0.34 | 0.00 |
| 2026-05 | 2,679 | 0.00 | 2.16 | 0.00 | 0.70 | 0.26 | 0.00 |
| 2026-06 | 2,545 | 0.10 | 3.01 | 0.00 | 0.59 | 0.17 | 0.00 |
| 2026-07 | 2,794 | 0.18 | 2.75 | 0.00 | 0.38 | 0.15 | 0.00 |
| 2026-08 | 2,836 | 0.12 | 2.69 | 0.00 | 0.91 | 0.23 | 0.00 |
| 2026-09 | 152 | 0.00 | 0.45 | 0.00 | 1.25 | 1.59 | 0.00 |

Intervals for every month are in the CSV.