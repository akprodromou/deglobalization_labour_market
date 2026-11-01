# Tagging evaluation

Sample: postings drawn in strata by one model's predicted channel, equal numbers per stratum, weighted back to the population of lexicon-flagged postings (script 59). Intervals are 95% bootstrap intervals resampling inside each stratum. No acceptance threshold is applied: models are compared on the same sample.

## tags_qwen2.5_7b_tagging_v9r

Annotated 472 of 472 sheet rows; `unclear`: 0.0% of the weighted flagged sample (left out); invalid model answers in the sample: 3.

| Channel | Precision | 95% interval | Recall | 95% interval | F1 | 95% interval |
|---|---:|---|---:|---|---:|---|
| reshoring (n=18) | 0.79 | 0.47 to 1.00 | 0.39 | 0.15 to 0.66 | 0.52 | 0.24 to 0.74 |
| defense (n=56) | 0.79 | 0.67 to 0.89 | 0.93 | 0.85 to 0.99 | 0.85 | 0.76 to 0.92 |
| critical materials (n=20) | 1.00 | 1.00 to 1.00 | 0.10 | 0.00 to 0.26 | 0.18 | 0.00 to 0.42 |
| energy security (n=74) | 0.87 | 0.73 to 0.98 | 0.55 | 0.43 to 0.69 | 0.68 | 0.56 to 0.78 |
| trade compliance (n=15) | 0.27 | 0.14 to 0.44 | 0.95 | 0.84 to 1.00 | 0.42 | 0.24 to 0.60 |
| diversification (n=1) | n/a | n/a | 0.00 | 0.00 to 0.00 | 0.00 | 0.00 to 0.00 |
| **any channel vs none** | 0.78 | 0.68 to 0.86 | 0.81 | 0.75 to 0.87 | 0.79 | 0.72 to 0.85 |

Macro-F1 over the channels present in the annotation: **0.44** (0.38 to 0.59).

Lexicon precision (flagged postings that are about a channel at all): 0.62 (0.55 to 0.69).

Intensity, where model and annotator agree on the channel: exact agreement 0.59 (0.45 to 0.72); quadratic-weighted kappa 0.60 (0.42 to 0.73).

| Annotator \ model (unweighted counts) | low | medium | high |
|---|---:|---:|---:|
| low | 16 | 5 | 10 |
| medium | 6 | 8 | 27 |
| high | 3 | 3 | 41 |

Lexicon misses: 0.02 of postings WITHOUT a lexicon term were judged relevant by the annotator (0.00 to 0.04).
