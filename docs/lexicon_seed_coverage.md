# Seed coverage and TF-IDF expansion

Corpus: corpus_jobbland.se_2026-01_2026-08.jsonl. 21,398 distinct postings after dropping 1,240 exact duplicates; day-weighted population 386,043. Text searched: title plus the first 6,000 characters of the description.

Postings containing at least one seed term: **258** (1.2% of the sample; 1.2% weighted).

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
| de-risking | diversification | 1 | 2 | 1 | sparse |
| dumping | diversification | 1 | 22 | 1 | sparse |
| free trade agreement | diversification | 5 | 87 | 3 |  |
| market diversification | diversification | 0 | 0 | 0 | sparse |
| trade diversification | diversification | 0 | 0 | 0 | sparse |
| critical infrastructure protection | energy security | 84 | 1,270 | 8 |  |
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

39 of the seed terms occur in fewer than 5 postings (marked `sparse`). They stay in the lexicon, but they cannot anchor an expansion.

## Flagged share by month

| Month | Postings | Flagged | Weighted share flagged |
|---|---:|---:|---:|
| 2026-01 | 2,788 | 28 | 0.72% |
| 2026-02 | 2,555 | 28 | 0.98% |
| 2026-03 | 2,651 | 31 | 1.27% |
| 2026-04 | 2,533 | 29 | 0.96% |
| 2026-05 | 2,684 | 30 | 1.25% |
| 2026-06 | 2,550 | 31 | 1.25% |
| 2026-07 | 2,798 | 40 | 1.93% |
| 2026-08 | 2,839 | 41 | 1.35% |

## TF-IDF expansion

Flagged postings 258, other postings 21,140. 1,000 candidate n-grams written to `data/lexicon/candidates_tfidf.csv` (found in at least 3 flagged postings under at least 2 distinct titles; ranked by z-score). Top 25:

| Term | Flagged | Other | z | Mean TF-IDF | Titles |
|---|---:|---:|---:|---:|---:|
| technology | 174 | 4194 | 15.87 | 2.924 | 165 |
| technical | 150 | 3922 | 14.2 | 3.029 | 143 |
| complex | 118 | 2612 | 14.14 | 1.97 | 113 |
| systems | 152 | 4213 | 13.73 | 2.862 | 146 |
| armed forces | 29 | 158 | 13.42 | 1.12 | 29 |
| secrecy | 22 | 68 | 13.42 | 0.568 | 22 |
| advanced | 81 | 1476 | 13.27 | 1.513 | 80 |
| engineering | 91 | 1837 | 13.21 | 1.812 | 88 |
| english | 166 | 5153 | 13.16 | 1.633 | 158 |
| attaching your cv | 33 | 234 | 13.15 | 0.688 | 32 |
| swedish and english | 112 | 2675 | 13.13 | 1.36 | 105 |
| fmv | 17 | 23 | 12.96 | 1.25 | 17 |
| citizenship | 69 | 1149 | 12.91 | 1.075 | 67 |
| classified | 39 | 384 | 12.61 | 0.931 | 35 |
| rights regardless | 20 | 69 | 12.56 | 0.502 | 19 |
| defense secrecy | 17 | 38 | 12.46 | 0.458 | 17 |
| opportunities and rights | 20 | 74 | 12.38 | 0.497 | 19 |
| requirements management | 17 | 45 | 12.18 | 0.505 | 16 |
| materiel | 16 | 34 | 12.18 | 0.82 | 16 |
| verification | 35 | 337 | 12.08 | 0.999 | 33 |
| convinced that diversity | 21 | 96 | 12.06 | 0.505 | 20 |
| projects | 120 | 3398 | 12.01 | 2.023 | 113 |
| certain citizenship | 17 | 52 | 11.89 | 0.443 | 17 |
| diversity contributes | 19 | 80 | 11.74 | 0.469 | 18 |
| apply quickly | 19 | 84 | 11.6 | 0.466 | 17 |

Read the list as candidates, not as findings. In a corpus dominated by a few employers, an n-gram can be frequent in flagged postings because of who posts them (boilerplate of one defence employer, say) and not because of the concept. The `titles` column and the example snippet are there to help you tell the difference.
