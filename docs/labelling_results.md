# Validation of the labels and of the predictor

Predictor scored: keyword screen of script 53 (baseline). Sample: 400 postings drawn in three strata (1 metals words, 2 manufacturing words only, 3 neither); weights bring the sample back to the population of distinct 2026 postings in the source. Intervals are 95% bootstrap intervals resampling inside each stratum (2000 draws). Thresholds for accepting the manufacturing flag, fixed before labelling: precision >= 0.80 and recall >= 0.70.

## Label: manufacturing

Labelled yes 123, no 271, unclear 6, not yet labelled 0. Weighted share of unclear among labelled: 1.9%.

| Quantity | Estimate | 95% interval |
|---|---:|---:|
| Prevalence among decidable postings | 12.2% | 9.3% to 15.6% |
| Precision | 0.49 | 0.41 to 0.56 |
| Recall | 0.83 | 0.67 to 0.99 |
| F1 | 0.61 | 0.53 to 0.69 |

Yes / no labels per stratum: stratum 1: 57 yes, 42 no; stratum 2: 62 yes, 85 no; stratum 3: 4 yes, 144 no.

Decision for the manufacturing flag: **Not accepted** (precision 0.49 against 0.80, recall 0.83 against 0.70).

## Label: metals

Labelled yes 38, no 348, unclear 14, not yet labelled 0. Weighted share of unclear among labelled: 1.6%.

| Quantity | Estimate | 95% interval |
|---|---:|---:|
| Prevalence among decidable postings | 1.9% | 1.3% to 2.6% |
| Precision | 0.41 | 0.30 to 0.53 |
| Recall | 0.78 | 0.58 to 1.00 |
| F1 | 0.54 | 0.42 to 0.66 |

Yes / no labels per stratum: stratum 1: 35 yes, 56 no; stratum 2: 3 yes, 143 no; stratum 3: 0 yes, 149 no.

The metals label is descriptive only: the group is too small to pass the volume rule (docs/sector_month_counts_steel.md), so no acceptance rule applies.

