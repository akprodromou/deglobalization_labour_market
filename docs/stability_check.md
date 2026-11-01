# Composition stability check around candidate events

Sampled postings (evenly spaced pages of each calendar month) compared before and after each event, within one source. A reading of "within normal drift" means the pre/post divergence is no larger than the month-to-month divergence on the same side and no larger than a random relabelling; it supports comparing shares across the event. "Shift beyond drift" means the mix of postings changed more than usual and the cause (collection or labour market) has to be examined before shares are interpreted.

## aiact-fr: lesjeudis.com, EU AI Act obligations for general-purpose AI models, 2 Aug 2025

Months before the event: 2025-05, 2025-06, 2025-07; after: 2025-08, 2025-09 (the month of the event date is counted on the side where most of it falls).

| month | sampled postings | side |
|---|---:|---|
| 2025-05 | 900 | before |
| 2025-06 | 900 | before |
| 2025-07 | 600 | before |
| 2025-08 | 600 | after |
| 2025-09 | 600 | after |

Share of sampled postings with a non-empty tag, by month (a month-to-month change here is a change in the data, not in the labour market):

| month | occupations | sectors | skills |
|---|---:|---:|---:|
| 2025-05 | 97% | 96% | 100% |
| 2025-06 | 98% | 96% | 100% |
| 2025-07 | 98% | 97% | 100% |
| 2025-08 | 98% | 97% | 100% |
| 2025-09 | 97% | 96% | 100% |

Jensen-Shannon divergence (0 = identical, 1 = disjoint). `drift` = largest divergence between two adjacent months on the same side; `null 95%` = 95th percentile when pre/post labels are shuffled.

| variable | pre vs post | drift (adjacent months) | null 95% | reading |
|---|---:|---:|---:|---|
| occupation (first tag) | 0.019 | 0.043 | 0.013 | within normal drift |
| sector (first tag) | 0.014 | 0.045 | 0.013 | within normal drift |
| experience_level | 0.006 | 0.027 | 0.002 | within normal drift |
| type | 0.018 | 0.010 | 0.002 | shift beyond drift |
| location_code | 0.000 | 0.000 | 0.000 | NO VARIATION: one value in every sampled posting, not testable |
| has occupation tag | 0.000 | 0.000 | 0.001 | within normal drift |
| has sector tag | 0.000 | 0.000 | 0.001 | within normal drift |
| has skills | 0.000 | 0.000 | 0.000 | NO VARIATION: one value in every sampled posting, not testable |
| description length (bin) | 0.002 | 0.007 | 0.002 | within normal drift |
| title words (top 300) | 0.031 | 0.061 | 0.021 | within normal drift |

Largest share changes, occupation (first tag) (pre n=2400, post n=1200):

| label | pre share | post share | change (pp) |
|---|---:|---:|---:|
| http://data.europa.eu/esco/occupation/2fb96c6c-8d0b-4ef0-b1ee-3e493305 | 2.9% | 1.8% | -1.1 |
| http://data.europa.eu/esco/occupation/05a06850-d465-481e-9d68-792d4ad1 | 0.4% | 1.4% | +1.0 |
| http://data.europa.eu/esco/occupation/068370e0-9c27-4814-87d0-44fbb314 | 7.4% | 6.6% | -0.8 |
| http://data.europa.eu/esco/occupation/00030d09-2b3a-4efd-87cc-c4ea39d2 | 4.3% | 3.5% | -0.8 |
| http://data.europa.eu/esco/occupation/0ba06640-e0ac-4911-9e43-289a8e41 | 1.4% | 0.6% | -0.8 |
| http://data.europa.eu/esco/occupation/1b422c31-f242-46b5-bbdc-aa63885e | 0.1% | 0.8% | +0.7 |
| http://data.europa.eu/esco/occupation/1619d7f3-7d95-407c-a20e-47745bfc | 0.7% | 1.3% | +0.7 |
| http://data.europa.eu/esco/occupation/1ad59946-d13e-441e-9b36-56e1df05 | 0.2% | 0.9% | +0.7 |

Largest share changes, sector (first tag) (pre n=2400, post n=1200):

| label | pre share | post share | change (pp) |
|---|---:|---:|---:|
| Business and other management consultancy activities | 9.8% | 8.5% | -1.3 |
| Other education n.e.c. | 1.8% | 0.8% | -1.0 |
| Accounting, bookkeeping and auditing activities; tax consultancy | 1.1% | 2.1% | +1.0 |
| Security and commodity contracts brokerage | 0.6% | 1.5% | +0.9 |
| Activities of head offices | 3.6% | 2.7% | -0.9 |
| Operation of arts facilities and sites | 4.4% | 3.5% | -0.9 |
| Computing infrastructure, data processing, hosting and related activit | 0.8% | 1.6% | +0.8 |
| Accommodation | 1.2% | 0.5% | -0.8 |
