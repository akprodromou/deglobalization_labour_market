# Seed coverage and TF-IDF expansion

Corpus: corpus_lesjeudis.com_2024-08_2025-04.jsonl. 12,548 distinct postings after dropping 889 exact duplicates; day-weighted population 31,510. Text searched: title plus the first 6,000 characters of the description.

Postings containing at least one seed term: **141** (1.1% of the sample; 1.1% weighted).

## Seed terms

| Term | Channel | Postings | Weighted estimate | Months with a hit | Flag |
|---|---|---:|---:|---:|---|
| AI compute | diversification | 0 | 0 | 0 | sparse |
| AI gigafactory | diversification | 13 | 32 | 4 |  |
| AI infrastructure | diversification | 7 | 12 | 5 |  |
| EuroHPC | diversification | 1 | 2 | 1 | sparse |
| European AI | diversification | 0 | 0 | 0 | sparse |
| alternative suppliers | diversification | 1 | 3 | 1 | sparse |
| dependence on non-European providers | diversification | 0 | 0 | 0 | sparse |
| digital sovereignty | diversification | 16 | 53 | 7 |  |
| dual sourcing | diversification | 1 | 1 | 1 | sparse |
| reduce dependence | diversification | 0 | 0 | 0 | sparse |
| single supplier | diversification | 6 | 24 | 2 |  |
| sovereign AI | diversification | 0 | 0 | 0 | sparse |
| sovereign cloud | diversification | 31 | 80 | 7 |  |
| supercomputing | diversification | 69 | 151 | 9 |  |
| supplier diversification | diversification | 0 | 0 | 0 | sparse |

9 of the seed terms occur in fewer than 5 postings (marked `sparse`). They stay in the lexicon, but they cannot anchor an expansion.

## Flagged share by month

| Month | Postings | Flagged | Weighted share flagged |
|---|---:|---:|---:|
| 2024-08 | 1,348 | 23 | 1.17% |
| 2024-09 | 2,218 | 22 | 1.01% |
| 2024-10 | 1,975 | 22 | 1.19% |
| 2024-11 | 1,981 | 14 | 0.75% |
| 2024-12 | 1,735 | 27 | 1.31% |
| 2025-01 | 1,792 | 17 | 0.91% |
| 2025-02 | 983 | 9 | 0.81% |
| 2025-03 | 210 | 5 | 2.44% |
| 2025-04 | 306 | 2 | 0.66% |

## TF-IDF expansion

Flagged postings 141, other postings 12,407. 1,000 candidate n-grams written to `data/lexicon/candidates_tfidf_lesjeudis_a.csv` (found in at least 3 flagged postings under at least 2 distinct titles; ranked by z-score). Top 25:

| Term | Flagged | Other | z | Mean TF-IDF | Titles |
|---|---:|---:|---:|---:|---:|
| eviden | 28 | 87 | 15.15 | 2.868 | 26 |
| advanced computing | 26 | 81 | 14.63 | 1.118 | 24 |
| continuum | 27 | 95 | 14.55 | 1.077 | 25 |
| entire digital continuum | 21 | 72 | 13.02 | 0.878 | 20 |
| precisely this audacity | 21 | 75 | 12.92 | 0.873 | 20 |
| possibilities into reality | 20 | 68 | 12.75 | 0.844 | 19 |
| salary range | 17 | 35 | 12.73 | 0.812 | 15 |
| talents to grow | 20 | 75 | 12.5 | 0.833 | 19 |
| tech and society | 20 | 75 | 12.5 | 0.833 | 19 |
| digital and world | 15 | 13 | 12.34 | 0.752 | 14 |
| inclusion to life | 19 | 68 | 12.33 | 0.803 | 18 |
| employees are fully | 19 | 69 | 12.29 | 0.802 | 18 |
| develop solutions | 17 | 48 | 12.21 | 0.784 | 16 |
| bringing this culture | 18 | 61 | 12.15 | 0.773 | 17 |
| involved in bringing | 18 | 61 | 12.15 | 0.773 | 17 |
| transform possibilities | 19 | 75 | 12.08 | 0.793 | 18 |
| atos group | 15 | 29 | 12.08 | 0.705 | 14 |
| pioneers | 22 | 115 | 12.08 | 0.86 | 21 |
| support all diversity | 18 | 64 | 12.04 | 0.768 | 17 |
| strategic subjects | 14 | 16 | 11.99 | 0.695 | 13 |
| technical audit | 14 | 16 | 11.99 | 0.695 | 13 |
| hr policy | 23 | 135 | 11.95 | 0.876 | 21 |
| hsm | 14 | 20 | 11.93 | 0.683 | 13 |
| programs that support | 18 | 67 | 11.92 | 0.764 | 17 |
| clients and shape | 18 | 69 | 11.85 | 0.761 | 17 |

Read the list as candidates, not as findings. In a corpus dominated by a few employers, an n-gram can be frequent in flagged postings because of who posts them (boilerplate of one defence employer, say) and not because of the concept. The `titles` column and the example snippet are there to help you tell the difference.
