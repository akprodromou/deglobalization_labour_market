# Tagging evaluation

Sample: postings drawn in strata by one model's predicted channel, equal numbers per stratum, weighted back to the population of lexicon-flagged postings (script 59). Intervals are 95% bootstrap intervals resampling inside each stratum. No acceptance threshold is applied: models are compared on the same sample.

## tags_qwen2.5_7b_tagging_v9r

Annotated 300 of 300 sheet rows; `unclear`: 1.7% of the weighted flagged sample (left out); invalid model answers in the sample: 0.

| Channel | Precision | 95% interval | Recall | 95% interval | F1 | 95% interval |
|---|---:|---|---:|---|---:|---|
| reshoring (n=8) | 0.68 | 0.00 to 1.00 | 0.02 | 0.00 to 0.10 | 0.03 | 0.00 to 0.18 |
| defense (n=107) | 0.76 | 0.68 to 0.83 | 0.92 | 0.86 to 0.97 | 0.83 | 0.77 to 0.88 |
| critical materials (n=0) | n/a | n/a | n/a | n/a | n/a | n/a |
| energy security (n=49) | 0.84 | 0.69 to 0.96 | 0.66 | 0.48 to 0.85 | 0.74 | 0.58 to 0.87 |
| trade compliance (n=1) | 0.00 | 0.00 to 0.00 | 0.00 | 0.00 to 0.00 | 0.00 | 0.00 to 0.00 |
| diversification (n=0) | n/a | n/a | n/a | n/a | n/a | n/a |
| **any channel vs none** | 0.78 | 0.71 to 0.85 | 0.87 | 0.81 to 0.93 | 0.82 | 0.77 to 0.87 |

Macro-F1 over the channels present in the annotation: **0.40** (0.36 to 0.57).

Lexicon precision (flagged postings that are about a channel at all): 0.59 (0.53 to 0.64).

Intensity, where model and annotator agree on the channel: exact agreement 0.61 (0.51 to 0.71); quadratic-weighted kappa 0.52 (0.32 to 0.69).

| Annotator \ model (unweighted counts) | low | medium | high |
|---|---:|---:|---:|
| low | 23 | 2 | 2 |
| medium | 15 | 8 | 18 |
| high | 10 | 4 | 54 |
