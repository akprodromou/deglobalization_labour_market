# Tagging evaluation

Sample: postings drawn in strata by one model's predicted channel, equal numbers per stratum, weighted back to the population of lexicon-flagged postings (script 59). Intervals are 95% bootstrap intervals resampling inside each stratum. No acceptance threshold is applied: models are compared on the same sample.

## tags_qwen2.5_7b_tagging_v6

Annotated 472 of 472 sheet rows; `unclear`: 0.0% of the weighted flagged sample (left out); invalid model answers in the sample: 4.

| Channel | Precision | 95% interval | Recall | 95% interval | F1 | 95% interval |
|---|---:|---|---:|---|---:|---|
| reshoring (n=18) | 0.36 | 0.19 to 0.54 | 0.80 | 0.59 to 0.97 | 0.50 | 0.30 to 0.67 |
| defense (n=56) | 0.77 | 0.66 to 0.88 | 0.99 | 0.97 to 1.00 | 0.87 | 0.79 to 0.93 |
| critical materials (n=20) | 0.83 | 0.67 to 0.96 | 0.81 | 0.56 to 1.00 | 0.82 | 0.65 to 0.97 |
| energy security (n=74) | 0.89 | 0.79 to 0.97 | 0.76 | 0.65 to 0.88 | 0.82 | 0.73 to 0.90 |
| trade compliance (n=15) | 0.22 | 0.11 to 0.35 | 0.95 | 0.84 to 1.00 | 0.36 | 0.20 to 0.51 |
| diversification (n=1) | n/a | n/a | 0.00 | 0.00 to 0.00 | 0.00 | 0.00 to 0.00 |
| **any channel vs none** | 0.75 | 0.67 to 0.83 | 0.94 | 0.91 to 0.97 | 0.84 | 0.78 to 0.89 |

Macro-F1 over the channels present in the annotation: **0.56** (0.51 to 0.72).

Lexicon precision (flagged postings that are about a channel at all): 0.62 (0.55 to 0.69).

Intensity, where model and annotator agree on the channel: exact agreement 0.57 (0.45 to 0.68); quadratic-weighted kappa 0.55 (0.37 to 0.71).

| Annotator \ model (unweighted counts) | low | medium | high |
|---|---:|---:|---:|
| low | 29 | 6 | 12 |
| medium | 5 | 10 | 45 |
| high | 0 | 6 | 45 |

Lexicon misses: 0.02 of postings WITHOUT a lexicon term were judged relevant by the annotator (0.00 to 0.04).

## tags_claude-haiku-4-5-20251001_tagging_v6

Annotated 472 of 472 sheet rows; `unclear`: 0.0% of the weighted flagged sample (left out); invalid model answers in the sample: 0.

| Channel | Precision | 95% interval | Recall | 95% interval | F1 | 95% interval |
|---|---:|---|---:|---|---:|---|
| reshoring (n=18) | 0.68 | 0.47 to 0.88 | 1.00 | 1.00 to 1.00 | 0.81 | 0.64 to 0.93 |
| defense (n=56) | 0.85 | 0.75 to 0.94 | 1.00 | 0.99 to 1.00 | 0.92 | 0.86 to 0.97 |
| critical materials (n=20) | 1.00 | 1.00 to 1.00 | 0.81 | 0.56 to 1.00 | 0.90 | 0.72 to 1.00 |
| energy security (n=74) | 0.91 | 0.81 to 0.98 | 0.78 | 0.66 to 0.90 | 0.84 | 0.75 to 0.92 |
| trade compliance (n=15) | 0.28 | 0.13 to 0.47 | 0.93 | 0.77 to 1.00 | 0.43 | 0.24 to 0.63 |
| diversification (n=1) | n/a | n/a | 0.00 | 0.00 to 0.00 | 0.00 | 0.00 to 0.00 |
| **any channel vs none** | 0.83 | 0.76 to 0.90 | 0.95 | 0.91 to 0.98 | 0.89 | 0.84 to 0.93 |

Macro-F1 over the channels present in the annotation: **0.65** (0.60 to 0.83).

Lexicon precision (flagged postings that are about a channel at all): 0.62 (0.55 to 0.69).

Intensity, where model and annotator agree on the channel: exact agreement 0.59 (0.48 to 0.70); quadratic-weighted kappa 0.64 (0.50 to 0.75).

| Annotator \ model (unweighted counts) | low | medium | high |
|---|---:|---:|---:|
| low | 24 | 22 | 2 |
| medium | 9 | 35 | 16 |
| high | 1 | 29 | 26 |

Lexicon misses: 0.02 of postings WITHOUT a lexicon term were judged relevant by the annotator (0.00 to 0.04).

## Comparison

| Model | Macro-F1 | F1 any channel vs none |
|---|---:|---:|
| tags_qwen2.5_7b_tagging_v6 | 0.56 | 0.84 |
| tags_claude-haiku-4-5-20251001_tagging_v6 (best macro-F1) | 0.65 | 0.89 |
