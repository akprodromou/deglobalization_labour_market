# Tagging evaluation

Sample: postings drawn in strata by one model's predicted channel, equal numbers per stratum, weighted back to the population of lexicon-flagged postings (script 59). Intervals are 95% bootstrap intervals resampling inside each stratum. No acceptance threshold is applied: models are compared on the same sample.

## tags_qwen2.5_7b_tagging_v9r

Annotated 155 of 300 sheet rows; `unclear`: 2.4% of the weighted flagged sample (left out); invalid model answers in the sample: 0.

| Channel | Precision | 95% interval | Recall | 95% interval | F1 | 95% interval |
|---|---:|---|---:|---|---:|---|
| reshoring (n=6) | 1.00 | 1.00 to 1.00 | 0.04 | 0.00 to 0.23 | 0.07 | 0.00 to 0.37 |
| defense (n=55) | 0.75 | 0.63 to 0.86 | 0.89 | 0.81 to 0.97 | 0.81 | 0.73 to 0.89 |
| critical materials (n=1) | n/a | n/a | 0.00 | 0.00 to 0.00 | 0.00 | 0.00 to 0.00 |
| energy security (n=21) | 0.47 | 0.26 to 0.73 | 0.59 | 0.33 to 0.99 | 0.52 | 0.32 to 0.75 |
| trade compliance (n=1) | n/a | n/a | 0.00 | 0.00 to 0.00 | 0.00 | 0.00 to 0.00 |
| diversification (n=1) | n/a | n/a | 0.00 | 0.00 to 0.00 | 0.00 | 0.00 to 0.00 |
| **any channel vs none** | 0.73 | 0.63 to 0.83 | 0.83 | 0.74 to 0.92 | 0.78 | 0.70 to 0.85 |

Macro-F1 over the channels present in the annotation: **0.23** (0.21 to 0.45).

Lexicon precision (flagged postings that are about a channel at all): 0.62 (0.53 to 0.70).

Intensity, where model and annotator agree on the channel: exact agreement 0.60 (0.46 to 0.74); quadratic-weighted kappa 0.35 (0.16 to 0.55).

| Annotator \ model (unweighted counts) | low | medium | high |
|---|---:|---:|---:|
| low | 6 | 0 | 0 |
| medium | 4 | 2 | 0 |
| high | 17 | 4 | 34 |
