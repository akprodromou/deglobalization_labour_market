# Tagging evaluation

Sample: postings drawn in strata by one model's predicted channel, equal numbers per stratum, weighted back to the population of lexicon-flagged postings (script 59). Intervals are 95% bootstrap intervals resampling inside each stratum. No acceptance threshold is applied: models are compared on the same sample.

## tags_qwen2.5_7b_tagging_v9r_lex154

Annotated 300 of 300 sheet rows; `unclear`: 4.1% of the weighted flagged sample (left out); invalid model answers in the sample: 0.

| Channel | Precision | 95% interval | Recall | 95% interval | F1 | 95% interval |
|---|---:|---|---:|---|---:|---|
| reshoring (n=10) | 1.00 | 1.00 to 1.00 | 0.01 | 0.00 to 0.06 | 0.03 | 0.00 to 0.12 |
| defense (n=111) | 0.76 | 0.68 to 0.84 | 0.88 | 0.82 to 0.94 | 0.82 | 0.76 to 0.87 |
| critical materials (n=1) | n/a | n/a | 0.00 | 0.00 to 0.00 | 0.00 | 0.00 to 0.00 |
| energy security (n=39) | 0.75 | 0.52 to 0.97 | 0.58 | 0.39 to 0.82 | 0.66 | 0.47 to 0.83 |
| trade compliance (n=1) | 0.00 | 0.00 to 0.00 | 0.00 | 0.00 to 0.00 | 0.00 | 0.00 to 0.00 |
| diversification (n=2) | n/a | n/a | 0.00 | 0.00 to 0.00 | 0.00 | 0.00 to 0.00 |
| **any channel vs none** | 0.78 | 0.71 to 0.86 | 0.83 | 0.77 to 0.89 | 0.81 | 0.75 to 0.86 |

Macro-F1 over the channels present in the annotation: **0.25** (0.23 to 0.41).

Lexicon precision (flagged postings that are about a channel at all): 0.61 (0.55 to 0.68).

Intensity, where model and annotator agree on the channel: exact agreement 0.55 (0.44 to 0.65); quadratic-weighted kappa 0.36 (0.22 to 0.51).

| Annotator \ model (unweighted counts) | low | medium | high |
|---|---:|---:|---:|
| low | 10 | 1 | 0 |
| medium | 13 | 5 | 1 |
| high | 27 | 11 | 59 |
