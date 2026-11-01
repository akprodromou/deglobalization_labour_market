# Seed coverage and TF-IDF expansion

Corpus: corpus_lesjeudis.com_2025-05_2025-09.jsonl. 6,110 distinct postings after dropping 407 exact duplicates; day-weighted population 13,685. Text searched: title plus the first 6,000 characters of the description.

Postings containing at least one seed term: **97** (1.6% of the sample; 1.6% weighted).

## Seed terms

| Term | Channel | Postings | Weighted estimate | Months with a hit | Flag |
|---|---|---:|---:|---:|---|
| AI compute | diversification | 2 | 2 | 2 | sparse |
| AI gigafactory | diversification | 4 | 6 | 3 | sparse |
| AI infrastructure | diversification | 9 | 16 | 2 |  |
| EuroHPC | diversification | 0 | 0 | 0 | sparse |
| European AI | diversification | 0 | 0 | 0 | sparse |
| alternative suppliers | diversification | 0 | 0 | 0 | sparse |
| dependence on non-European providers | diversification | 0 | 0 | 0 | sparse |
| digital sovereignty | diversification | 12 | 43 | 3 |  |
| dual sourcing | diversification | 0 | 0 | 0 | sparse |
| reduce dependence | diversification | 0 | 0 | 0 | sparse |
| single supplier | diversification | 8 | 18 | 5 |  |
| sovereign AI | diversification | 14 | 40 | 4 |  |
| sovereign cloud | diversification | 36 | 82 | 5 |  |
| supercomputing | diversification | 27 | 59 | 5 |  |
| supplier diversification | diversification | 0 | 0 | 0 | sparse |

9 of the seed terms occur in fewer than 5 postings (marked `sparse`). They stay in the lexicon, but they cannot anchor an expansion.

## Flagged share by month

| Month | Postings | Flagged | Weighted share flagged |
|---|---:|---:|---:|
| 2025-05 | 1,256 | 13 | 0.93% |
| 2025-06 | 1,673 | 22 | 1.28% |
| 2025-07 | 608 | 10 | 1.62% |
| 2025-08 | 1,549 | 32 | 2.02% |
| 2025-09 | 1,024 | 20 | 2.17% |

## TF-IDF expansion

Flagged postings 97, other postings 6,013. 1,000 candidate n-grams written to `data/lexicon/candidates_tfidf_lesjeudis_b.csv` (found in at least 3 flagged postings under at least 2 distinct titles; ranked by z-score). Top 25:

| Term | Flagged | Other | z | Mean TF-IDF | Titles |
|---|---:|---:|---:|---:|---:|
| technical excellence | 19 | 42 | 11.99 | 1.095 | 19 |
| iaas | 19 | 50 | 11.66 | 1.234 | 19 |
| round | 17 | 33 | 11.59 | 1.014 | 17 |
| paas | 18 | 55 | 11.05 | 1.105 | 18 |
| renewable energy | 14 | 13 | 11.03 | 0.922 | 14 |
| terraces | 15 | 30 | 10.9 | 0.953 | 15 |
| days of remote | 13 | 14 | 10.64 | 0.856 | 13 |
| private and public | 13 | 15 | 10.63 | 0.851 | 13 |
| committed to supporting | 13 | 10 | 10.6 | 0.876 | 13 |
| work per week | 13 | 19 | 10.51 | 0.834 | 13 |
| serverless | 14 | 29 | 10.5 | 0.941 | 14 |
| designing secure | 14 | 6 | 10.48 | 0.963 | 14 |
| collaborative and international | 13 | 8 | 10.47 | 0.888 | 13 |
| spirit of sharing | 13 | 8 | 10.47 | 0.888 | 13 |
| dining | 13 | 8 | 10.47 | 0.888 | 13 |
| offices are located | 13 | 7 | 10.36 | 0.894 | 13 |
| facilities | 18 | 74 | 10.31 | 0.999 | 18 |
| rich and diverse | 14 | 5 | 10.23 | 0.97 | 14 |
| located in paris | 13 | 26 | 10.19 | 0.808 | 13 |
| aimed at supporting | 15 | 4 | 10.1 | 1.04 | 15 |
| spoken | 20 | 108 | 10.0 | 1.071 | 20 |
| catalog of products | 13 | 5 | 9.97 | 0.908 | 13 |
| cnrs | 11 | 11 | 9.84 | 0.868 | 11 |
| containerization | 21 | 131 | 9.75 | 1.149 | 21 |
| chef | 17 | 78 | 9.75 | 0.977 | 17 |

Read the list as candidates, not as findings. In a corpus dominated by a few employers, an n-gram can be frequent in flagged postings because of who posts them (boilerplate of one defence employer, say) and not because of the concept. The `titles` column and the example snippet are there to help you tell the difference.
