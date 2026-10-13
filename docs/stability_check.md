# Composition stability check around candidate events

Sampled postings (evenly spaced pages of each calendar month) compared before and after each event, within one source. A reading of "within normal drift" means the pre/post divergence is no larger than the month-to-month divergence on the same side and no larger than a random relabelling; it supports comparing shares across the event. "Shift beyond drift" means the mix of postings changed more than usual and the cause (collection or labour market) has to be examined before shares are interpreted.

## oil-gr: kariera.gr, Iran war / oil shock, 28 Feb 2026

Months before the event: 2026-01, 2026-02; after: 2026-03, 2026-04 (the month of the event date is counted on the side where most of it falls).

| month | sampled postings | side |
|---|---:|---|
| 2026-01 | 600 | before |
| 2026-02 | 600 | before |
| 2026-03 | 600 | after |
| 2026-04 | 600 | after |

Jensen-Shannon divergence (0 = identical, 1 = disjoint). `drift` = largest divergence between two adjacent months on the same side; `null 95%` = 95th percentile when pre/post labels are shuffled.

| variable | pre vs post | drift (adjacent months) | null 95% | reading |
|---|---:|---:|---:|---|
| occupation (first tag) | 0.000 | 0.000 | 0.000 | within normal drift |
| sector (first tag) | 0.000 | 0.000 | 0.000 | within normal drift |
| experience_level | 0.036 | 0.075 | 0.003 | within normal drift |
| type | 0.007 | 0.007 | 0.004 | within normal drift |
| location_code | 0.000 | 0.000 | 0.000 | within normal drift |
| has occupation tag | 0.000 | 0.000 | 0.000 | within normal drift |
| has sector tag | 0.000 | 0.000 | 0.000 | within normal drift |
| has skills | 0.000 | 0.000 | 0.000 | within normal drift |
| description length (bin) | 0.004 | 0.043 | 0.003 | within normal drift |

Largest share changes, occupation (first tag) (pre n=1200, post n=1200):

| label | pre share | post share | change (pp) |
|---|---:|---:|---:|
| (none) | 100.0% | 100.0% | +0.0 |

Largest share changes, sector (first tag) (pre n=1200, post n=1200):

| label | pre share | post share | change (pp) |
|---|---:|---:|---:|
| (none) | 100.0% | 100.0% | +0.0 |
