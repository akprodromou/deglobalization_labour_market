# Tagging evaluation

Sample: postings drawn in strata by one model's predicted channel, equal numbers per stratum, weighted back to the population of lexicon-flagged postings (script 59). Intervals are 95% bootstrap intervals resampling inside each stratum. No acceptance threshold is applied: models are compared on the same sample.

## tags_claude-haiku-4-5-20251001_tagging_v8

Annotated 300 of 300 sheet rows; `unclear`: 1.7% of the weighted flagged sample (left out); invalid model answers in the sample: 0.

| Channel | Precision | 95% interval | Recall | 95% interval | F1 | 95% interval |
|---|---:|---|---:|---|---:|---|
| reshoring (n=8) | 0.37 | 0.00 to 0.87 | 0.17 | 0.00 to 0.74 | 0.23 | 0.00 to 0.61 |
| defense (n=107) | 0.82 | 0.75 to 0.90 | 0.91 | 0.85 to 0.96 | 0.86 | 0.81 to 0.91 |
| critical materials (n=0) | n/a | n/a | n/a | n/a | n/a | n/a |
| energy security (n=49) | 0.69 | 0.53 to 0.85 | 0.60 | 0.43 to 0.82 | 0.64 | 0.50 to 0.79 |
| trade compliance (n=1) | 0.28 | 0.00 to 1.00 | 1.00 | 1.00 to 1.00 | 0.44 | 0.40 to 1.00 |
| diversification (n=0) | n/a | n/a | n/a | n/a | n/a | n/a |
| **any channel vs none** | 0.82 | 0.75 to 0.88 | 0.86 | 0.80 to 0.91 | 0.84 | 0.79 to 0.88 |

Macro-F1 over the channels present in the annotation: **0.54** (0.48 to 0.72).

Lexicon precision (flagged postings that are about a channel at all): 0.59 (0.53 to 0.64).

Intensity, where model and annotator agree on the channel: exact agreement 0.38 (0.28 to 0.48); quadratic-weighted kappa 0.39 (0.26 to 0.51).

| Annotator \ model (unweighted counts) | low | medium | high |
|---|---:|---:|---:|
| low | 20 | 8 | 0 |
| medium | 18 | 23 | 1 |
| high | 6 | 48 | 14 |
