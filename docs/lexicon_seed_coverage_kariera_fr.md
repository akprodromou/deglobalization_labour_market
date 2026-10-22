# Seed coverage and TF-IDF expansion

Corpus: corpus_kariera.fr_2024-08_2025-03.jsonl. 10,707 distinct postings after dropping 1,492 exact duplicates; day-weighted population 79,772. Text searched: title plus the first 6,000 characters of the description.

Postings containing at least one seed term: **454** (4.2% of the sample; 3.2% weighted).

## Seed terms

| Term | Channel | Postings | Weighted estimate | Months with a hit | Flag |
|---|---|---:|---:|---:|---|
| battery materials | critical materials | 0 | 0 | 0 | sparse |
| critical metals | critical materials | 0 | 0 | 0 | sparse |
| critical raw materials | critical materials | 0 | 0 | 0 | sparse |
| lithium | critical materials | 0 | 0 | 0 | sparse |
| rare earths | critical materials | 0 | 0 | 0 | sparse |
| raw materials security | critical materials | 0 | 0 | 0 | sparse |
| strategic raw materials | critical materials | 0 | 0 | 0 | sparse |
| ammunition production | defense | 1 | 2 | 1 | sparse |
| armament | defense | 82 | 495 | 5 |  |
| defence industrial base | defense | 7 | 36 | 4 |  |
| defence procurement | defense | 0 | 0 | 0 | sparse |
| defence supply chain | defense | 0 | 0 | 0 | sparse |
| defense | defense | 391 | 2,248 | 8 |  |
| military equipment | defense | 5 | 14 | 2 |  |
| de-risking | diversification | 0 | 0 | 0 | sparse |
| dumping | diversification | 0 | 0 | 0 | sparse |
| free trade agreement | diversification | 0 | 0 | 0 | sparse |
| market diversification | diversification | 0 | 0 | 0 | sparse |
| trade diversification | diversification | 0 | 0 | 0 | sparse |
| critical infrastructure protection | energy security | 2 | 9 | 2 | sparse |
| energy security | energy security | 1 | 1 | 1 | sparse |
| gas supply diversification | energy security | 0 | 0 | 0 | sparse |
| grid resilience | energy security | 0 | 0 | 0 | sparse |
| security of supply | energy security | 0 | 0 | 0 | sparse |
| China plus one | reshoring | 0 | 0 | 0 | sparse |
| de-risking | reshoring | 0 | 0 | 0 | sparse |
| deglobalization | reshoring | 0 | 0 | 0 | sparse |
| dual sourcing | reshoring | 0 | 0 | 0 | sparse |
| friend-shoring | reshoring | 0 | 0 | 0 | sparse |
| made in Europe | reshoring | 0 | 0 | 0 | sparse |
| nearshoring | reshoring | 0 | 0 | 0 | sparse |
| onshoring | reshoring | 0 | 0 | 0 | sparse |
| reshoring | reshoring | 0 | 0 | 0 | sparse |
| semiconductor sovereignty | reshoring | 0 | 0 | 0 | sparse |
| strategic autonomy | reshoring | 0 | 0 | 0 | sparse |
| supply chain diversification | reshoring | 0 | 0 | 0 | sparse |
| supply chain resilience | reshoring | 0 | 0 | 0 | sparse |
| supply chain security | reshoring | 0 | 0 | 0 | sparse |
| CBAM | trade compliance | 0 | 0 | 0 | sparse |
| ESG sourcing | trade compliance | 0 | 0 | 0 | sparse |
| anti-dumping | trade compliance | 0 | 0 | 0 | sparse |
| customs compliance | trade compliance | 20 | 91 | 5 |  |
| deforestation regulation | trade compliance | 0 | 0 | 0 | sparse |
| dual-use goods | trade compliance | 0 | 0 | 0 | sparse |
| export controls | trade compliance | 1 | 4 | 1 | sparse |
| global value chains | trade compliance | 0 | 0 | 0 | sparse |
| rules of origin | trade compliance | 0 | 0 | 0 | sparse |
| sanctions compliance | trade compliance | 0 | 0 | 0 | sparse |
| supply chain due diligence | trade compliance | 0 | 0 | 0 | sparse |
| telemigration | trade compliance | 0 | 0 | 0 | sparse |
| trade compliance | trade compliance | 2 | 14 | 2 | sparse |

46 of the seed terms occur in fewer than 5 postings (marked `sparse`). They stay in the lexicon, but they cannot anchor an expansion.

## Flagged share by month

| Month | Postings | Flagged | Weighted share flagged |
|---|---:|---:|---:|
| 2024-08 | 1,249 | 184 | 14.58% |
| 2024-09 | 1,902 | 177 | 7.16% |
| 2024-10 | 2,545 | 34 | 0.91% |
| 2024-11 | 1,985 | 22 | 1.09% |
| 2024-12 | 1,421 | 21 | 1.38% |
| 2025-01 | 972 | 13 | 1.38% |
| 2025-02 | 414 | 2 | 0.53% |
| 2025-03 | 219 | 1 | 0.19% |

## TF-IDF expansion

Flagged postings 454, other postings 10,253. 1,000 candidate n-grams written to `data/lexicon/candidates_tfidf_kariera_fr.csv` (found in at least 3 flagged postings under at least 2 distinct titles; ranked by z-score). Top 25:

| Term | Flagged | Other | z | Mean TF-IDF | Titles |
|---|---:|---:|---:|---:|---:|
| expected skills | 240 | 254 | 33.39 | 2.154 | 216 |
| ministry | 193 | 97 | 31.24 | 3.02 | 167 |
| armed forces | 185 | 106 | 30.68 | 2.617 | 158 |
| wordsthe | 150 | 166 | 26.85 | 1.493 | 136 |
| section | 114 | 101 | 23.91 | 1.844 | 108 |
| head | 137 | 364 | 21.39 | 1.756 | 135 |
| joint | 86 | 52 | 20.9 | 1.136 | 76 |
| team work | 103 | 224 | 19.73 | 1.018 | 91 |
| administration | 117 | 325 | 19.52 | 1.371 | 104 |
| organizations | 93 | 184 | 19.22 | 1.079 | 82 |
| civil | 92 | 179 | 19.19 | 1.147 | 87 |
| organization and methods | 73 | 67 | 19.1 | 0.857 | 67 |
| division | 88 | 161 | 19.04 | 1.397 | 82 |
| office software | 73 | 79 | 18.85 | 0.844 | 70 |
| ensures | 113 | 333 | 18.81 | 1.27 | 110 |
| use of office | 69 | 66 | 18.52 | 0.824 | 66 |
| army | 73 | 103 | 18.23 | 1.021 | 67 |
| armies | 64 | 51 | 17.99 | 0.903 | 58 |
| directorate | 69 | 92 | 17.88 | 0.955 | 67 |
| organization | 263 | 1975 | 17.84 | 1.952 | 239 |
| general | 168 | 885 | 17.71 | 1.696 | 152 |
| secretariat | 61 | 39 | 17.59 | 0.827 | 55 |
| expression | 68 | 108 | 17.25 | 0.858 | 64 |
| civilian | 59 | 60 | 17.05 | 0.925 | 53 |
| policy | 114 | 440 | 16.99 | 1.136 | 96 |

Read the list as candidates, not as findings. In a corpus dominated by a few employers, an n-gram can be frequent in flagged postings because of who posts them (boilerplate of one defence employer, say) and not because of the concept. The `titles` column and the example snippet are there to help you tell the difference.
