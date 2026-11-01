# Tagging evaluation

Sample: postings drawn in strata by one model's predicted channel, equal numbers per stratum, weighted back to the population of lexicon-flagged postings (script 59). Intervals are 95% bootstrap intervals resampling inside each stratum. No acceptance threshold is applied: models are compared on the same sample.

## tags_qwen2.5_7b_tagging_v9r_lex154

Annotated 142 of 300 sheet rows; `unclear`: 1.2% of the weighted flagged sample (left out); invalid model answers in the sample: 0.

| Channel | Precision | 95% interval | Recall | 95% interval | F1 | 95% interval |
|---|---:|---|---:|---|---:|---|
| reshoring (n=7) | 1.00 | 1.00 to 1.00 | 0.01 | 0.00 to 0.10 | 0.03 | 0.00 to 0.17 |
| defense (n=39) | 0.83 | 0.70 to 0.94 | 0.85 | 0.72 to 0.96 | 0.84 | 0.74 to 0.92 |
| critical materials (n=1) | n/a | n/a | 0.00 | 0.00 to 0.00 | 0.00 | 0.00 to 0.00 |
| energy security (n=27) | 0.77 | 0.48 to 1.00 | 0.59 | 0.35 to 0.86 | 0.67 | 0.45 to 0.87 |
| trade compliance (n=0) | n/a | n/a | n/a | n/a | n/a | n/a |
| diversification (n=2) | n/a | n/a | 0.00 | 0.00 to 0.00 | 0.00 | 0.00 to 0.00 |
| **any channel vs none** | 0.84 | 0.74 to 0.94 | 0.74 | 0.62 to 0.85 | 0.79 | 0.70 to 0.86 |

Macro-F1 over the channels present in the annotation: **0.31** (0.26 to 0.52).

Lexicon precision (flagged postings that are about a channel at all): 0.60 (0.51 to 0.68).

Intensity, where model and annotator agree on the channel: exact agreement 0.45 (0.27 to 0.61); quadratic-weighted kappa 0.28 (0.12 to 0.48).

| Annotator \ model (unweighted counts) | low | medium | high |
|---|---:|---:|---:|
| low | 4 | 0 | 0 |
| medium | 8 | 0 | 0 |
| high | 13 | 6 | 22 |
