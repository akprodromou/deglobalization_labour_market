# Boards compared: composition and concentration

Equal-size comparison uses subsamples of 12,243 postings drawn by weight, 200 repetitions. HHI on the whole board depends on the board's size and should not be compared across boards; use the equal-size columns.

## skills

| board | postings with the field | labels | HHI whole board | effective number whole | top-10 share whole | HHI equal size (median) | 95% range | effective number equal size | top-10 share equal size |
|---|---|---|---|---|---|---|---|---|---|
| jobbland | 97.9% | 6539 | 0.0052 | 192.6 | 17.7% | 0.0052 | 0.0051 to 0.0053 | 192.4 | 17.7% |
| lesjeudis | 99.1% | 4023 | 0.0032 | 309.3 | 11.2% | 0.0032 | 0.0032 to 0.0033 | 308.6 | 11.2% |
| jobsde | 89.7% | 3635 | 0.0034 | 296.4 | 12.6% | 0.0034 | 0.0033 to 0.0035 | 294.3 | 12.7% |

## sectors

| board | postings with the field | labels | HHI whole board | effective number whole | top-10 share whole | HHI equal size (median) | 95% range | effective number equal size | top-10 share equal size |
|---|---|---|---|---|---|---|---|---|---|
| jobbland | 35.3% | 621 | 0.0161 | 62.2 | 29.4% | 0.0161 | 0.0155 to 0.0167 | 62.1 | 29.3% |
| lesjeudis | 95.7% | 555 | 0.0221 | 45.3 | 38.0% | 0.0221 | 0.0216 to 0.0226 | 45.3 | 38.0% |
| jobsde | 83.1% | 593 | 0.0110 | 90.7 | 24.6% | 0.0110 | 0.0108 to 0.0113 | 90.6 | 24.6% |

## cluster

| board | postings with the field | labels | HHI whole board | effective number whole | top-10 share whole | HHI equal size (median) | 95% range | effective number equal size | top-10 share equal size |
|---|---|---|---|---|---|---|---|---|---|
| jobbland | 65.3% | 357 | 0.0052 | 192.8 | 13.5% | 0.0053 | 0.0051 to 0.0055 | 188.4 | 13.6% |
| lesjeudis | 68.5% | 144 | 0.0102 | 97.6 | 20.4% | 0.0104 | 0.0101 to 0.0107 | 96.3 | 20.7% |
| jobsde | 72.6% | 71 | 0.0322 | 31.0 | 45.3% | 0.0323 | 0.0310 to 0.0337 | 31.0 | 45.3% |

## region

| board | postings with the field | labels | HHI whole board | effective number whole | top-10 share whole | HHI equal size (median) | 95% range | effective number equal size | top-10 share equal size |
|---|---|---|---|---|---|---|---|---|---|
| jobbland | 81.2% | 8 | 0.1699 | 5.9 | 100.0% | 0.1699 | 0.1667 to 0.1731 | 5.9 | 100.0% |
| lesjeudis | 99.8% | 22 | 0.2396 | 4.2 | 92.2% | 0.2397 | 0.2317 to 0.2459 | 4.2 | 92.2% |
| jobsde | 98.8% | 38 | 0.0452 | 22.1 | 53.6% | 0.0452 | 0.0440 to 0.0464 | 22.1 | 53.7% |

## employer

| board | postings with the field | labels | HHI whole board | effective number whole | top-10 share whole | HHI equal size (median) | 95% range | effective number equal size | top-10 share equal size |
|---|---|---|---|---|---|---|---|---|---|
| jobbland | 0.0% | 0 | | | | | | | |
| lesjeudis | 0.0% | 1 | field not recorded | | | | | | |
| jobsde | 0.1% | 16 | 0.1017 | 9.8 | 79.4% | 0.1537 | 0.0999 to 0.2727 | 6.5 | 100.0% |

## Regions: HHI corrected for the number of regions

A country with 38 regions has a low HHI even if one region dominates, so the HHI is rescaled to (HHI - 1/R) / (1 - 1/R), 0 = postings spread evenly over the R regions, 1 = all in one.

| board | regions seen | HHI | normalised HHI |
|---|---|---|---|
| jobbland | 8 | 0.1699 | 0.051 |
| lesjeudis | 22 | 0.2396 | 0.203 |
| jobsde | 38 | 0.0452 | 0.019 |

## Composition similarity between boards (Jensen-Shannon, 1 = identical)

| board A | board B | dimension | shared labels | similarity | weight covered by shared labels (smaller side) |
|---|---|---|---|---|---|
| jobbland | lesjeudis | skills | 3586 | 0.697 | 89.7% |
| jobbland | lesjeudis | sectors | 538 | 0.847 | 98.9% |
| jobbland | jobsde | skills | 3279 | 0.781 | 86.7% |
| jobbland | jobsde | sectors | 577 | 0.888 | 99.9% |
| lesjeudis | jobsde | skills | 2416 | 0.628 | 89.8% |
| lesjeudis | jobsde | sectors | 521 | 0.800 | 98.0% |

## HHI by quarter (quarters with at least 300 taken postings)

| board | quarter | taken | skills HHI | postings with skills | skills per posting | most common skill | its share of postings with skills | cluster HHI |
|---|---|---|---|---|---|---|---|---|
| jobbland | 2024-Q1 | 701 | 0.0047 | 97.9% | 7.0 | http://data.europa.eu/esco/skill/7ee51257-8947-4b69-9bdf-322baf0a6398 | 23.7% | 0.0135 |
| jobbland | 2024-Q2 | 2417 | 0.0046 | 93.8% | 6.0 | http://data.europa.eu/esco/skill/7ee51257-8947-4b69-9bdf-322baf0a6398 | 21.7% | 0.0074 |
| jobbland | 2024-Q3 | 5369 | 0.0044 | 94.1% | 6.0 | http://data.europa.eu/esco/skill/7ee51257-8947-4b69-9bdf-322baf0a6398 | 20.8% | 0.0057 |
| jobbland | 2024-Q4 | 8172 | 0.0052 | 95.5% | 6.5 | http://data.europa.eu/esco/skill/7ee51257-8947-4b69-9bdf-322baf0a6398 | 23.3% | 0.0091 |
| jobbland | 2025-Q1 | 5515 | 0.0050 | 95.2% | 6.2 | http://data.europa.eu/esco/skill/7ee51257-8947-4b69-9bdf-322baf0a6398 | 22.4% | 0.0111 |
| jobbland | 2025-Q2 | 2010 | 0.0049 | 99.9% | 6.2 | http://data.europa.eu/esco/skill/7ee51257-8947-4b69-9bdf-322baf0a6398 | 16.6% | 0.0100 |
| jobbland | 2025-Q3 | 2900 | 0.0046 | 99.9% | 6.3 | http://data.europa.eu/esco/skill/7ee51257-8947-4b69-9bdf-322baf0a6398 | 19.3% | 0.0081 |
| jobbland | 2025-Q4 | 5405 | 0.0053 | 100.0% | 6.6 | http://data.europa.eu/esco/skill/7ee51257-8947-4b69-9bdf-322baf0a6398 | 23.1% | 0.0076 |
| jobbland | 2026-Q1 | 7944 | 0.0057 | 99.6% | 6.1 | http://data.europa.eu/esco/skill/7ee51257-8947-4b69-9bdf-322baf0a6398 | 21.4% | 0.0071 |
| jobbland | 2026-Q2 | 7744 | 0.0054 | 100.0% | 6.5 | http://data.europa.eu/esco/skill/7ee51257-8947-4b69-9bdf-322baf0a6398 | 20.9% | 0.0069 |
| jobbland | 2026-Q3 | 5782 | 0.0053 | 97.4% | 6.6 | http://data.europa.eu/esco/skill/7ee51257-8947-4b69-9bdf-322baf0a6398 | 22.5% | 0.0064 |
| lesjeudis | 2024-Q3 | 3566 | 0.0039 | 98.8% | 8.3 | http://data.europa.eu/esco/skill/d4789070-2ff7-4bbb-94ca-8bb1739826a9 | 16.7% | 0.0131 |
| lesjeudis | 2024-Q4 | 5691 | 0.0031 | 98.6% | 8.3 | http://data.europa.eu/esco/skill/f3c5fae0-c0e3-4410-bc09-62bd82d4cecc | 12.2% | 0.0121 |
| lesjeudis | 2025-Q1 | 2985 | 0.0032 | 98.5% | 8.3 | http://data.europa.eu/esco/skill/2fb8480e-de3c-462b-b169-e8bbb344da68 | 12.8% | 0.0156 |
| lesjeudis | 2025-Q2 | 3213 | 0.0041 | 100.0% | 8.6 | http://data.europa.eu/esco/skill/f3c5fae0-c0e3-4410-bc09-62bd82d4cecc | 16.1% | 0.0120 |
| lesjeudis | 2025-Q3 | 3170 | 0.0035 | 100.0% | 8.7 | http://data.europa.eu/esco/skill/8088750d-8388-4170-a76f-48354c469c44 | 12.7% | 0.0142 |
| jobsde | 2024-Q3 | 3253 | 0.0039 | 93.4% | 4.5 | http://data.europa.eu/esco/skill/a472a200-d895-40ca-95e7-5c5495e3dd7c | 10.9% | 0.0366 |
| jobsde | 2024-Q4 | 5519 | 0.0033 | 88.5% | 4.2 | http://data.europa.eu/esco/skill/113b4428-0a31-4199-8496-070af7854b91 | 7.5% | 0.0331 |
| jobsde | 2025-Q1 | 3122 | 0.0048 | 86.8% | 4.4 | http://data.europa.eu/esco/skill/a472a200-d895-40ca-95e7-5c5495e3dd7c | 11.3% | 0.0611 |
| jobsde | 2025-Q2 | 349 | 0.0070 | 100.0% | 4.8 | http://data.europa.eu/esco/skill/a472a200-d895-40ca-95e7-5c5495e3dd7c | 18.2% | 0.2090 |

## Field coverage by month (share of weighted postings with the field filled)

| board | month | taken | skills | sectors | occupations |
|---|---|---|---|---|---|
| jobbland | 2024-01 | 185 | 97.0% | 90.1% | 92.9% |
| jobbland | 2024-02 | 227 | 97.0% | 87.4% | 89.8% |
| jobbland | 2024-03 | 289 | 99.3% | 93.1% | 94.8% |
| jobbland | 2024-04 | 317 | 96.9% | 84.3% | 89.1% |
| jobbland | 2024-05 | 993 | 93.8% | 89.3% | 93.3% |
| jobbland | 2024-06 | 1107 | 93.3% | 86.4% | 91.8% |
| jobbland | 2024-07 | 1405 | 95.5% | 89.0% | 94.4% |
| jobbland | 2024-08 | 1777 | 94.5% | 88.1% | 94.1% |
| jobbland | 2024-09 | 2187 | 93.6% | 90.5% | 94.8% |
| jobbland | 2024-10 | 2759 | 95.2% | 90.4% | 94.6% |
| jobbland | 2024-11 | 2828 | 94.6% | 87.9% | 93.9% |
| jobbland | 2024-12 | 2585 | 96.9% | 91.3% | 95.7% |
| jobbland | 2025-01 | 2847 | 94.8% | 90.6% | 94.4% |
| jobbland | 2025-02 | 1478 | 94.0% | 91.1% | 93.7% |
| jobbland | 2025-03 | 1190 | 99.6% | 91.1% | 94.6% |
| jobbland | 2025-04 | 798 | 99.9% | 92.1% | 95.3% |
| jobbland | 2025-05 | 1088 | 100.0% | 90.3% | 92.7% |
| jobbland | 2025-06 | 124 | 100.0% | 0.0% | 0.0% |
| jobbland | 2025-07 | 361 | 100.0% | 65.7% | 67.4% |
| jobbland | 2025-08 | 1088 | 99.9% | 79.1% | 81.6% |
| jobbland | 2025-09 | 1451 | 100.0% | 68.8% | 71.1% |
| jobbland | 2025-10 | 1447 | 100.0% | 0.2% | 0.2% |
| jobbland | 2025-11 | 1590 | 99.9% | 0.3% | 0.3% |
| jobbland | 2025-12 | 2368 | 100.0% | 0.0% | 0.0% |
| jobbland | 2026-01 | 2764 | 99.5% | 0.0% | 0.0% |
| jobbland | 2026-02 | 2537 | 100.0% | 0.8% | 0.8% |
| jobbland | 2026-03 | 2643 | 99.4% | 0.0% | 0.0% |
| jobbland | 2026-04 | 2520 | 100.0% | 0.0% | 0.0% |
| jobbland | 2026-05 | 2679 | 100.0% | 0.0% | 0.0% |
| jobbland | 2026-06 | 2545 | 100.0% | 0.0% | 0.0% |
| jobbland | 2026-07 | 2794 | 99.4% | 0.0% | 0.0% |
| jobbland | 2026-08 | 2836 | 95.9% | 0.0% | 0.0% |
| jobbland | 2026-09 | 152 | 100.0% | 0.0% | 0.0% |
| lesjeudis | 2024-08 | 1348 | 99.3% | 96.8% | 98.0% |
| lesjeudis | 2024-09 | 2218 | 98.5% | 94.2% | 96.3% |
| lesjeudis | 2024-10 | 1975 | 99.0% | 95.8% | 97.8% |
| lesjeudis | 2024-11 | 1981 | 97.7% | 95.4% | 96.9% |
| lesjeudis | 2024-12 | 1735 | 99.0% | 95.7% | 97.2% |
| lesjeudis | 2025-01 | 1792 | 98.0% | 94.0% | 96.8% |
| lesjeudis | 2025-02 | 983 | 99.2% | 96.0% | 96.9% |
| lesjeudis | 2025-03 | 210 | 100.0% | 94.2% | 96.9% |
| lesjeudis | 2025-04 | 306 | 100.0% | 97.2% | 98.1% |
| lesjeudis | 2025-05 | 1249 | 100.0% | 96.2% | 97.6% |
| lesjeudis | 2025-06 | 1658 | 100.0% | 97.0% | 98.4% |
| lesjeudis | 2025-07 | 604 | 100.0% | 96.3% | 97.6% |
| lesjeudis | 2025-08 | 1544 | 100.0% | 97.0% | 97.7% |
| lesjeudis | 2025-09 | 1022 | 100.0% | 95.9% | 97.4% |
| jobsde | 2024-08 | 1145 | 93.2% | 87.5% | 95.5% |
| jobsde | 2024-09 | 2108 | 93.5% | 87.4% | 95.6% |
| jobsde | 2024-10 | 1863 | 87.7% | 82.5% | 90.9% |
| jobsde | 2024-11 | 1975 | 88.5% | 79.1% | 87.6% |
| jobsde | 2024-12 | 1681 | 89.9% | 81.6% | 88.8% |
| jobsde | 2025-01 | 979 | 82.7% | 79.6% | 86.0% |
| jobsde | 2025-02 | 1308 | 80.7% | 76.6% | 84.2% |
| jobsde | 2025-03 | 835 | 100.0% | 90.7% | 97.4% |
| jobsde | 2025-04 | 349 | 100.0% | 92.8% | 97.2% |
