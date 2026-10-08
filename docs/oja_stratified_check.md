# OJA time-stratified sample: composition across windows

Random result pages (100 postings each) from single-month windows of source `OJA`. Pages are clusters of consecutive results, so differences of a few percentage points are within sampling noise; large shifts are not. Script: `diagnostics/21_oja_time_stratified_sample.py`.

## 1. Sample

| Window | Postings in window | Pages sampled | Postings in sample |
|---|---|---|---|
| 2019-06 | 14,739 | 5/5 | 500 |
| 2023-06 | ? | 0/0 | 0 |
| 2023-12 | 5,391 | 5/5 | 500 |
| 2024-01 | 276,271 | 5/5 | 500 |
| 2024-02 | 236,890 | 5/5 | 500 |
| 2024-12 | 48,950 | 2/5 | 200 |
| 2025-03 | ? | 0/0 | 0 |

## 2. Field completeness and duplicates

| Window | skills | occupations | organization | description | mean desc. chars | repeated description prefix | repeated title/org/place/date | top-10 org share |
|---|---|---|---|---|---|---|---|---|
| 2019-06 | 100.0% | 100.0% | 0.0% | 0.0% | 0 | 0/0 | 0/0 | n/a |
| 2023-12 | 100.0% | 100.0% | 0.0% | 0.0% | 0 | 0/0 | 0/0 | n/a |
| 2024-01 | 100.0% | 100.0% | 0.0% | 0.0% | 0 | 0/0 | 0/0 | n/a |
| 2024-02 | 100.0% | 100.0% | 0.0% | 0.0% | 0 | 0/0 | 0/0 | n/a |
| 2024-12 | 100.0% | 100.0% | 0.0% | 0.0% | 0 | 0/0 | 0/0 | n/a |

## 3. Country mix (`location_code`)

| Window | with code | DE | FR | AT | UK | IT | NL | BE | SE | ES | DK | other |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2019-06 | 100.0% | 37.6% | 1.8% | 40.4% | 4.6% | 9.2% | 0.6% | 1.2% | 0.4% | 0.4% | 0.0% | 3.8% |
| 2023-12 | 100.0% | 28.0% | 2.8% | 1.0% | 13.2% | 19.6% | 12.8% | 7.4% | 7.8% | 3.6% | 0.6% | 3.2% |
| 2024-01 | 60.0% | 32.3% | 66.7% | 0.0% | 0.3% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.7% |
| 2024-02 | 60.0% | 22.7% | 63.0% | 0.0% | 10.7% | 0.0% | 0.3% | 0.7% | 0.0% | 1.7% | 0.0% | 1.0% |
| 2024-12 | 100.0% | 2.0% | 11.0% | 5.5% | 48.0% | 15.5% | 1.0% | 0.5% | 0.5% | 5.0% | 4.5% | 6.5% |

## 4. ISCO major-group mix

| Window | with ISCO | ISCO 1 | ISCO 2 | ISCO 3 | ISCO 4 | ISCO 8 |
|---|---|---|---|---|---|---|
| 2019-06 | 100.0% | 0.0% | 20.0% | 80.0% | 0.0% | 0.0% |
| 2023-12 | 100.0% | 0.0% | 20.0% | 40.0% | 0.0% | 40.0% |
| 2024-01 | 100.0% | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% |
| 2024-02 | 100.0% | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% |
| 2024-12 | 100.0% | 23.0% | 76.0% | 0.5% | 0.5% | 0.0% |

## 5. Distance between consecutive windows

Total variation distance (0 = identical mix, 1 = disjoint) between the window and the previous one in the table.

| From → to | country | ISCO group |
|---|---|---|
| 2019-06 → 2023-12 | 0.52 | 0.40 |
| 2023-12 → 2024-01 | 0.69 | 0.80 |
| 2024-01 → 2024-02 | 0.14 | 0.00 |
| 2024-02 → 2024-12 | 0.73 | 0.24 |

Read the Dec 2023 → Jan 2024 row against the others. A distance much larger there than between, say, 2023-06 and 2023-12 or 2024-01 and 2024-02 points to a change of composition (new feed or source mix) at the break; similar distances point to the same mix at a different volume.

## 6. Shared description prefixes between windows

Share of the row window's postings whose description prefix also appears in the column window's sample. High values across months mean the same adverts are listed repeatedly.

| Window ↓ in → | 2019-06 | 2023-12 | 2024-01 | 2024-02 | 2024-12 |
|---|---|---|---|---|---|
| 2019-06 | - | - | - | - | - |
| 2023-12 | - | - | - | - | - |
| 2024-01 | - | - | - | - | - |
| 2024-02 | - | - | - | - | - |
| 2024-12 | - | - | - | - | - |

Sample sizes are a few hundred per window, so an overlap can only be seen if a large share of the population repeats; zero overlap does not rule out smaller-scale duplication.
