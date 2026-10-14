# Composition stability check around candidate events

Sampled postings (evenly spaced pages of each calendar month) compared before and after each event, within one source. A reading of "within normal drift" means the pre/post divergence is no larger than the month-to-month divergence on the same side and no larger than a random relabelling; it supports comparing shares across the event. "Shift beyond drift" means the mix of postings changed more than usual and the cause (collection or labour market) has to be examined before shares are interpreted.

## ev-de: jobs.de, EU tariffs on Chinese EVs, 30 Oct 2024

Months before the event: 2024-08, 2024-09, 2024-10; after: 2024-11, 2024-12, 2025-01 (the month of the event date is counted on the side where most of it falls).

| month | sampled postings | side |
|---|---:|---|
| 2024-08 | 600 | before |
| 2024-09 | 600 | before |
| 2024-10 | 600 | before |
| 2024-11 | 600 | after |
| 2024-12 | 600 | after |
| 2025-01 | 600 | after |

Share of sampled postings with a non-empty tag, by month (a month-to-month change here is a change in the data, not in the labour market):

| month | occupations | sectors | skills |
|---|---:|---:|---:|
| 2024-08 | 96% | 84% | 90% |
| 2024-09 | 95% | 88% | 91% |
| 2024-10 | 92% | 82% | 88% |
| 2024-11 | 89% | 82% | 92% |
| 2024-12 | 86% | 78% | 87% |
| 2025-01 | 85% | 76% | 84% |

Jensen-Shannon divergence (0 = identical, 1 = disjoint). `drift` = largest divergence between two adjacent months on the same side; `null 95%` = 95th percentile when pre/post labels are shuffled.

| variable | pre vs post | drift (adjacent months) | null 95% | reading |
|---|---:|---:|---:|---|
| occupation (first tag) | 0.105 | 0.204 | 0.011 | within normal drift |
| sector (first tag) | 0.075 | 0.184 | 0.011 | within normal drift |
| experience_level | 0.028 | 0.039 | 0.003 | within normal drift |
| type | 0.015 | 0.012 | 0.002 | shift beyond drift |
| location_code | 0.000 | 0.000 | 0.000 | NO VARIATION: one value in every sampled posting, not testable |
| has occupation tag | 0.014 | 0.002 | 0.001 | shift beyond drift |
| has sector tag | 0.004 | 0.006 | 0.001 | within normal drift |
| has skills | 0.001 | 0.004 | 0.001 | within normal drift |
| description length (bin) | 0.016 | 0.121 | 0.002 | within normal drift |
| title words (top 300) | 0.424 | 0.205 | 0.018 | shift beyond drift |

Largest share changes, occupation (first tag) (pre n=1800, post n=1800):

| label | pre share | post share | change (pp) |
|---|---:|---:|---:|
| http://data.europa.eu/esco/occupation/7ed2e153-8da8-4c0d-b4c5-3402c623 | 11.6% | 1.3% | -10.3 |
| (none) | 5.4% | 13.6% | +8.2 |
| http://data.europa.eu/esco/occupation/068370e0-9c27-4814-87d0-44fbb314 | 4.3% | 0.4% | -3.9 |
| http://data.europa.eu/esco/isco/C231 | 3.1% | 0.0% | -3.1 |
| http://data.europa.eu/esco/occupation/a504e79e-f146-4773-a1cf-2b15b9d6 | 0.0% | 2.1% | +2.1 |
| http://data.europa.eu/esco/occupation/234be692-befb-41df-bdf0-e1b2f4ea | 0.3% | 1.4% | +1.1 |
| http://data.europa.eu/esco/occupation/ea6cd713-94ca-4292-9ba9-ca8a4ec3 | 0.9% | 0.0% | -0.9 |
| http://data.europa.eu/esco/occupation/2168e49d-e58a-43ec-a15e-8e173939 | 0.2% | 0.9% | +0.7 |

Largest share changes, sector (first tag) (pre n=1800, post n=1800):

| label | pre share | post share | change (pp) |
|---|---:|---:|---:|
| Postal activities under universal service obligation | 11.6% | 1.3% | -10.3 |
| (none) | 15.0% | 20.9% | +5.9 |
| Business and other management consultancy activities | 5.6% | 1.9% | -3.7 |
| Removal services | 0.0% | 2.1% | +2.1 |
| Amusement and recreation activities n.e.c. | 0.3% | 1.4% | +1.1 |
| Other social work activities without accommodation n.e.c. | 0.2% | 1.3% | +1.1 |
| Other education n.e.c. | 2.4% | 3.4% | +1.0 |
| Other monetary intermediation | 0.6% | 1.6% | +1.0 |
