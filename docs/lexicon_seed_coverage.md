# Seed coverage and TF-IDF expansion

Corpus: corpus_jobbland.se_2026-01_2026-08.jsonl. 21,398 distinct postings after dropping 1,240 exact duplicates; day-weighted population 386,043. Text searched: title plus the first 6,000 characters of the description.

Postings containing at least one seed term: **181** (0.8% of the sample; 0.9% weighted).

## Seed terms

| Term | Channel | Postings | Weighted estimate | Months with a hit | Flag |
|---|---|---:|---:|---:|---|
| battery materials | critical materials | 0 | 0 | 0 | sparse |
| critical metals | critical materials | 1 | 24 | 1 | sparse |
| critical raw materials | critical materials | 1 | 33 | 1 | sparse |
| lithium | critical materials | 9 | 175 | 6 |  |
| rare earths | critical materials | 2 | 58 | 2 | sparse |
| raw materials security | critical materials | 1 | 28 | 1 | sparse |
| strategic raw materials | critical materials | 0 | 0 | 0 | sparse |
| ammunition production | defense | 5 | 129 | 4 |  |
| defence industrial base | defense | 110 | 2,128 | 8 |  |
| defence procurement | defense | 0 | 0 | 0 | sparse |
| defence supply chain | defense | 0 | 0 | 0 | sparse |
| military equipment | defense | 8 | 137 | 4 |  |
| free trade agreement | diversification | 5 | 87 | 3 |  |
| market diversification | diversification | 0 | 0 | 0 | sparse |
| trade diversification | diversification | 0 | 0 | 0 | sparse |
| critical infrastructure protection | energy security | 0 | 0 | 0 | sparse |
| energy security | energy security | 0 | 0 | 0 | sparse |
| gas supply diversification | energy security | 0 | 0 | 0 | sparse |
| grid resilience | energy security | 0 | 0 | 0 | sparse |
| security of supply | energy security | 9 | 158 | 5 |  |
| China plus one | reshoring | 0 | 0 | 0 | sparse |
| de-risking | reshoring | 1 | 2 | 1 | sparse |
| deglobalization | reshoring | 0 | 0 | 0 | sparse |
| dual sourcing | reshoring | 0 | 0 | 0 | sparse |
| friend-shoring | reshoring | 0 | 0 | 0 | sparse |
| made in Europe | reshoring | 0 | 0 | 0 | sparse |
| nearshoring | reshoring | 1 | 21 | 1 | sparse |
| onshoring | reshoring | 0 | 0 | 0 | sparse |
| reshoring | reshoring | 0 | 0 | 0 | sparse |
| semiconductor sovereignty | reshoring | 0 | 0 | 0 | sparse |
| strategic autonomy | reshoring | 0 | 0 | 0 | sparse |
| supply chain diversification | reshoring | 0 | 0 | 0 | sparse |
| supply chain resilience | reshoring | 1 | 20 | 1 | sparse |
| supply chain security | reshoring | 2 | 19 | 2 | sparse |
| CBAM | trade compliance | 0 | 0 | 0 | sparse |
| ESG sourcing | trade compliance | 0 | 0 | 0 | sparse |
| anti-dumping | trade compliance | 1 | 22 | 1 | sparse |
| customs compliance | trade compliance | 5 | 68 | 4 |  |
| deforestation regulation | trade compliance | 1 | 3 | 1 | sparse |
| dual-use goods | trade compliance | 0 | 0 | 0 | sparse |
| export controls | trade compliance | 28 | 484 | 8 |  |
| global value chains | trade compliance | 0 | 0 | 0 | sparse |
| rules of origin | trade compliance | 1 | 22 | 1 | sparse |
| sanctions compliance | trade compliance | 0 | 0 | 0 | sparse |
| supply chain due diligence | trade compliance | 1 | 3 | 1 | sparse |
| telemigration | trade compliance | 0 | 0 | 0 | sparse |
| trade compliance | trade compliance | 5 | 103 | 4 |  |

38 of the seed terms occur in fewer than 5 postings (marked `sparse`). They stay in the lexicon, but they cannot anchor an expansion.

## Flagged share by month

| Month | Postings | Flagged | Weighted share flagged |
|---|---:|---:|---:|
| 2026-01 | 2,788 | 18 | 0.49% |
| 2026-02 | 2,555 | 20 | 0.75% |
| 2026-03 | 2,651 | 19 | 0.74% |
| 2026-04 | 2,533 | 17 | 0.67% |
| 2026-05 | 2,684 | 26 | 1.09% |
| 2026-06 | 2,550 | 25 | 0.97% |
| 2026-07 | 2,798 | 27 | 1.53% |
| 2026-08 | 2,839 | 29 | 0.96% |

## TF-IDF expansion

Flagged postings 181, other postings 21,217. 1,000 candidate n-grams written to `data/lexicon/candidates_tfidf.csv` (found in at least 3 flagged postings under at least 2 distinct titles; ranked by z-score). Top 25:

| Term | Flagged | Other | z | Mean TF-IDF | Titles |
|---|---:|---:|---:|---:|---:|
| citizenship | 62 | 1156 | 13.87 | 1.383 | 61 |
| technology | 126 | 4242 | 13.65 | 3.128 | 119 |
| defense secrecy | 17 | 38 | 13.62 | 0.652 | 17 |
| armed forces | 25 | 162 | 13.4 | 1.425 | 25 |
| verification | 33 | 339 | 13.22 | 1.318 | 31 |
| engineering | 75 | 1853 | 13.14 | 2.143 | 72 |
| complex | 91 | 2639 | 13.11 | 2.167 | 88 |
| certain citizenship | 17 | 52 | 13.1 | 0.631 | 17 |
| requirements management | 16 | 46 | 12.85 | 0.682 | 15 |
| technically advanced | 22 | 137 | 12.76 | 0.811 | 21 |
| advanced | 64 | 1493 | 12.6 | 1.733 | 63 |
| saab | 20 | 117 | 12.4 | 1.218 | 20 |
| swedish and english | 86 | 2701 | 12.18 | 1.49 | 81 |
| systems | 112 | 4253 | 12.15 | 3.176 | 108 |
| fmv | 13 | 27 | 12.08 | 1.274 | 13 |
| technical | 106 | 3966 | 11.98 | 3.251 | 100 |
| engineering education | 18 | 114 | 11.57 | 0.605 | 17 |
| swedish citizenship | 36 | 577 | 11.55 | 0.905 | 35 |
| technically | 38 | 658 | 11.44 | 1.129 | 36 |
| english | 120 | 5199 | 11.41 | 1.692 | 114 |
| aviation | 17 | 118 | 10.98 | 0.772 | 17 |
| defense materiel | 10 | 10 | 10.87 | 0.438 | 10 |
| create innovation | 16 | 111 | 10.68 | 0.541 | 11 |
| karlskoga | 13 | 63 | 10.61 | 0.668 | 12 |
| complex technical | 18 | 158 | 10.51 | 0.621 | 17 |

Read the list as candidates, not as findings. In a corpus dominated by a few employers, an n-gram can be frequent in flagged postings because of who posts them (boilerplate of one defence employer, say) and not because of the concept. The `titles` column and the example snippet are there to help you tell the difference.
