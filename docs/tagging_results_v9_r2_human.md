# Tagging evaluation

Sample: postings drawn in strata by one model's predicted channel, equal numbers per stratum, weighted back to the population of lexicon-flagged postings (script 59). Intervals are 95% bootstrap intervals resampling inside each stratum. No acceptance threshold is applied: models are compared on the same sample.

## tags_qwen2.5_7b_tagging_v9r

Annotated 59 of 300 sheet rows; `unclear`: 1.7% of the weighted flagged sample (left out); invalid model answers in the sample: 0.

| Channel | Precision | 95% interval | Recall | 95% interval | F1 | 95% interval |
|---|---:|---|---:|---|---:|---|
| reshoring (n=3) | 1.00 | 1.00 to 1.00 | 0.07 | 0.00 to 1.00 | 0.13 | 0.00 to 1.00 |
| defense (n=20) | 0.76 | 0.58 to 0.92 | 0.90 | 0.76 to 1.00 | 0.82 | 0.69 to 0.93 |
| critical materials (n=0) | n/a | n/a | n/a | n/a | n/a | n/a |
| energy security (n=9) | 0.98 | 0.90 to 1.00 | 0.61 | 0.29 to 1.00 | 0.75 | 0.44 to 1.00 |
| trade compliance (n=0) | n/a | n/a | n/a | n/a | n/a | n/a |
| diversification (n=0) | n/a | n/a | n/a | n/a | n/a | n/a |
| **any channel vs none** | 0.77 | 0.61 to 0.93 | 0.84 | 0.70 to 0.97 | 0.80 | 0.69 to 0.91 |

Macro-F1 over the channels present in the annotation: **0.57** (0.45 to 0.82).

Lexicon precision (flagged postings that are about a channel at all): 0.66 (0.52 to 0.79).

Intensity, where model and annotator agree on the channel: exact agreement 0.59 (0.40 to 0.81); quadratic-weighted kappa 0.12 (-0.00 to 0.39).

| Annotator \ model (unweighted counts) | low | medium | high |
|---|---:|---:|---:|
| low | 0 | 0 | 0 |
| medium | 1 | 2 | 0 |
| high | 7 | 2 | 15 |
