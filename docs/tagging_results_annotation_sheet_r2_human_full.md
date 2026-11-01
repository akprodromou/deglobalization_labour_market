# Tagging evaluation

Sample: postings drawn in strata by one model's predicted channel, equal numbers per stratum, weighted back to the population of lexicon-flagged postings (script 59). Intervals are 95% bootstrap intervals resampling inside each stratum. No acceptance threshold is applied: models are compared on the same sample.

## tags_qwen2.5_7b_tagging_v9r_lex154

Annotated 300 of 300 sheet rows; `unclear`: 1.2% of the weighted flagged sample (left out); invalid model answers in the sample: 0.

| Channel | Precision | 95% interval | Recall | 95% interval | F1 | 95% interval |
|---|---:|---|---:|---|---:|---|
| reshoring (n=11) | 1.00 | 1.00 to 1.00 | 0.01 | 0.00 to 0.05 | 0.03 | 0.00 to 0.10 |
| defense (n=136) | 0.88 | 0.82 to 0.93 | 0.87 | 0.81 to 0.93 | 0.88 | 0.84 to 0.92 |
| critical materials (n=1) | n/a | n/a | 0.00 | 0.00 to 0.00 | 0.00 | 0.00 to 0.00 |
| energy security (n=43) | 0.75 | 0.51 to 0.96 | 0.52 | 0.33 to 0.75 | 0.62 | 0.43 to 0.80 |
| trade compliance (n=0) | 0.00 | 0.00 to 0.00 | n/a | n/a | n/a | n/a |
| diversification (n=2) | n/a | n/a | 0.00 | 0.00 to 0.00 | 0.00 | 0.00 to 0.00 |
| **any channel vs none** | 0.89 | 0.84 to 0.94 | 0.82 | 0.76 to 0.88 | 0.85 | 0.81 to 0.89 |

Macro-F1 over the channels present in the annotation: **0.30** (0.27 to 0.49).

Lexicon precision (flagged postings that are about a channel at all): 0.71 (0.66 to 0.77).

Intensity, where model and annotator agree on the channel: exact agreement 0.52 (0.42 to 0.61); quadratic-weighted kappa 0.31 (0.18 to 0.44).

| Annotator \ model (unweighted counts) | low | medium | high |
|---|---:|---:|---:|
| low | 10 | 2 | 0 |
| medium | 17 | 5 | 3 |
| high | 33 | 11 | 66 |
