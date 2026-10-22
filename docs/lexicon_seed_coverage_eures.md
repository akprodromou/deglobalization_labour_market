# Seed coverage and TF-IDF expansion

Corpus: corpus_eures_2025-12_2026-02.jsonl. 7,231 distinct postings after dropping 654 exact duplicates; day-weighted population 381,769. Text searched: title plus the first 6,000 characters of the description.

Postings containing at least one seed term: **38** (0.5% of the sample; 0.3% weighted).

## Seed terms

| Term | Channel | Postings | Weighted estimate | Months with a hit | Flag |
|---|---|---:|---:|---:|---|
| battery materials | critical materials | 0 | 0 | 0 | sparse |
| critical metals | critical materials | 0 | 0 | 0 | sparse |
| critical raw materials | critical materials | 0 | 0 | 0 | sparse |
| lithium | critical materials | 2 | 12 | 1 | sparse |
| rare earths | critical materials | 0 | 0 | 0 | sparse |
| raw materials security | critical materials | 0 | 0 | 0 | sparse |
| strategic raw materials | critical materials | 0 | 0 | 0 | sparse |
| ammunition production | defense | 0 | 0 | 0 | sparse |
| armament | defense | 1 | 59 | 1 | sparse |
| defence industrial base | defense | 1 | 7 | 1 | sparse |
| defence procurement | defense | 0 | 0 | 0 | sparse |
| defence supply chain | defense | 0 | 0 | 0 | sparse |
| defense | defense | 19 | 242 | 2 |  |
| military equipment | defense | 0 | 0 | 0 | sparse |
| de-risking | diversification | 0 | 0 | 0 | sparse |
| dumping | diversification | 2 | 79 | 2 | sparse |
| free trade agreement | diversification | 2 | 50 | 2 | sparse |
| market diversification | diversification | 0 | 0 | 0 | sparse |
| trade diversification | diversification | 0 | 0 | 0 | sparse |
| critical infrastructure protection | energy security | 3 | 37 | 1 | sparse |
| energy security | energy security | 0 | 0 | 0 | sparse |
| gas supply diversification | energy security | 0 | 0 | 0 | sparse |
| grid resilience | energy security | 0 | 0 | 0 | sparse |
| security of supply | energy security | 2 | 48 | 2 | sparse |
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
| customs compliance | trade compliance | 6 | 350 | 3 |  |
| deforestation regulation | trade compliance | 0 | 0 | 0 | sparse |
| dual-use goods | trade compliance | 0 | 0 | 0 | sparse |
| export controls | trade compliance | 1 | 158 | 1 | sparse |
| global value chains | trade compliance | 0 | 0 | 0 | sparse |
| rules of origin | trade compliance | 0 | 0 | 0 | sparse |
| sanctions compliance | trade compliance | 0 | 0 | 0 | sparse |
| supply chain due diligence | trade compliance | 0 | 0 | 0 | sparse |
| telemigration | trade compliance | 0 | 0 | 0 | sparse |
| trade compliance | trade compliance | 0 | 0 | 0 | sparse |

49 of the seed terms occur in fewer than 5 postings (marked `sparse`). They stay in the lexicon, but they cannot anchor an expansion.

## Flagged share by month

| Month | Postings | Flagged | Weighted share flagged |
|---|---:|---:|---:|
| 2025-12 | 2,193 | 23 | 1.20% |
| 2026-01 | 2,750 | 8 | 0.35% |
| 2026-02 | 2,288 | 7 | 0.16% |

**Warning: only 38 flagged postings.** The expansion below rests on too little text to say much. Options: widen the seed list, add the 2024 sources (other countries, other boards) to the corpus, or lower --min-flagged-df.

## TF-IDF expansion

Flagged postings 38, other postings 7,193. 384 candidate n-grams written to `data/lexicon/candidates_tfidf_eures.csv` (found in at least 3 flagged postings under at least 2 distinct titles; ranked by z-score). Top 25:

| Term | Flagged | Other | z | Mean TF-IDF | Titles |
|---|---:|---:|---:|---:|---:|
| training offers | 14 | 28 | 13.14 | 2.257 | 14 |
| wedding | 13 | 15 | 13.04 | 2.23 | 13 |
| time possible | 13 | 20 | 12.97 | 2.176 | 13 |
| incl | 13 | 20 | 12.97 | 2.176 | 13 |
| innovations | 13 | 22 | 12.91 | 2.156 | 13 |
| fitness studio | 13 | 27 | 12.73 | 2.112 | 13 |
| successful team | 13 | 28 | 12.69 | 2.103 | 13 |
| health promotion | 13 | 30 | 12.61 | 2.088 | 13 |
| working time account | 14 | 44 | 12.52 | 2.14 | 14 |
| owned | 13 | 33 | 12.49 | 2.065 | 13 |
| vehicle technology | 13 | 34 | 12.45 | 2.277 | 13 |
| flensburg | 13 | 6 | 12.33 | 2.357 | 13 |
| innovation | 14 | 58 | 12.01 | 2.062 | 13 |
| canteen | 14 | 67 | 11.71 | 2.019 | 13 |
| language courses | 13 | 4 | 11.63 | 2.393 | 13 |
| stretched | 13 | 4 | 11.63 | 2.393 | 13 |
| tradition | 13 | 61 | 11.43 | 1.905 | 13 |
| offered | 14 | 79 | 11.34 | 1.968 | 14 |
| bicycle leasing | 13 | 69 | 11.17 | 1.87 | 13 |
| company events | 13 | 70 | 11.14 | 1.866 | 13 |
| special vacation days | 9 | 8 | 11.06 | 1.657 | 9 |
| moving | 13 | 89 | 10.59 | 1.797 | 13 |
| world | 19 | 222 | 10.52 | 2.359 | 19 |
| family additional information | 13 | 2 | 10.23 | 2.434 | 13 |
| sap | 12 | 91 | 10.03 | 2.819 | 12 |

Read the list as candidates, not as findings. In a corpus dominated by a few employers, an n-gram can be frequent in flagged postings because of who posts them (boilerplate of one defence employer, say) and not because of the concept. The `titles` column and the example snippet are there to help you tell the difference.
