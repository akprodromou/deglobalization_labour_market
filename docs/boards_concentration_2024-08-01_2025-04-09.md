# Boards compared: composition and concentration

Equal-size comparison uses subsamples of 12,243 postings drawn by weight, 200 repetitions. HHI on the whole board depends on the board's size and should not be compared across boards; use the equal-size columns.

## skills

| board | postings with the field | labels | HHI whole board | effective number whole | top-10 share whole | HHI equal size (median) | 95% range | effective number equal size | top-10 share equal size |
|---|---|---|---|---|---|---|---|---|---|
| jobbland | 95.3% | 5034 | 0.0050 | 199.8 | 17.0% | 0.0050 | 0.0049 to 0.0051 | 199.2 | 17.1% |
| lesjeudis | 98.7% | 3559 | 0.0032 | 310.6 | 11.4% | 0.0032 | 0.0032 to 0.0033 | 309.2 | 11.4% |
| jobsde | 89.7% | 3635 | 0.0034 | 296.4 | 12.6% | 0.0034 | 0.0033 to 0.0035 | 294.3 | 12.7% |

## sectors

| board | postings with the field | labels | HHI whole board | effective number whole | top-10 share whole | HHI equal size (median) | 95% range | effective number equal size | top-10 share equal size |
|---|---|---|---|---|---|---|---|---|---|
| jobbland | 90.2% | 607 | 0.0162 | 61.7 | 29.4% | 0.0162 | 0.0158 to 0.0167 | 61.6 | 29.4% |
| lesjeudis | 95.4% | 530 | 0.0222 | 45.1 | 37.8% | 0.0222 | 0.0217 to 0.0227 | 45.0 | 37.8% |
| jobsde | 83.1% | 593 | 0.0110 | 90.7 | 24.6% | 0.0110 | 0.0108 to 0.0113 | 90.6 | 24.6% |

## cluster

| board | postings with the field | labels | HHI whole board | effective number whole | top-10 share whole | HHI equal size (median) | 95% range | effective number equal size | top-10 share equal size |
|---|---|---|---|---|---|---|---|---|---|
| jobbland | 63.4% | 356 | 0.0088 | 113.2 | 21.8% | 0.0089 | 0.0085 to 0.0094 | 111.8 | 21.8% |
| lesjeudis | 68.1% | 144 | 0.0105 | 95.5 | 20.6% | 0.0106 | 0.0103 to 0.0109 | 94.5 | 20.8% |
| jobsde | 72.6% | 71 | 0.0322 | 31.0 | 45.3% | 0.0323 | 0.0310 to 0.0337 | 31.0 | 45.3% |

## region

| board | postings with the field | labels | HHI whole board | effective number whole | top-10 share whole | HHI equal size (median) | 95% range | effective number equal size | top-10 share equal size |
|---|---|---|---|---|---|---|---|---|---|
| jobbland | 92.7% | 8 | 0.1701 | 5.9 | 100.0% | 0.1700 | 0.1671 to 0.1731 | 5.9 | 100.0% |
| lesjeudis | 99.7% | 22 | 0.2353 | 4.2 | 92.2% | 0.2350 | 0.2277 to 0.2418 | 4.3 | 92.2% |
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
| jobbland | 8 | 0.1701 | 0.052 |
| lesjeudis | 22 | 0.2353 | 0.199 |
| jobsde | 38 | 0.0452 | 0.019 |

## Composition similarity between boards (Jensen-Shannon, 1 = identical)

| board A | board B | dimension | shared labels | similarity | weight covered by shared labels (smaller side) |
|---|---|---|---|---|---|
| jobbland | lesjeudis | skills | 2860 | 0.709 | 88.0% |
| jobbland | lesjeudis | sectors | 511 | 0.846 | 98.6% |
| jobbland | jobsde | skills | 2921 | 0.792 | 86.6% |
| jobbland | jobsde | sectors | 567 | 0.888 | 99.7% |
| lesjeudis | jobsde | skills | 2222 | 0.638 | 86.9% |
| lesjeudis | jobsde | sectors | 500 | 0.798 | 97.6% |

## HHI by quarter (quarters with at least 300 taken postings)

| board | quarter | taken | skills HHI | postings with skills | skills per posting | most common skill | its share of postings with skills | cluster HHI |
|---|---|---|---|---|---|---|---|---|
| jobbland | 2024-Q3 | 3964 | 0.0044 | 93.9% | 6.0 | http://data.europa.eu/esco/skill/7ee51257-8947-4b69-9bdf-322baf0a6398 | 20.9% | 0.0059 |
| jobbland | 2024-Q4 | 8172 | 0.0052 | 95.5% | 6.5 | http://data.europa.eu/esco/skill/7ee51257-8947-4b69-9bdf-322baf0a6398 | 23.3% | 0.0091 |
| jobbland | 2025-Q1 | 5515 | 0.0050 | 95.2% | 6.2 | http://data.europa.eu/esco/skill/7ee51257-8947-4b69-9bdf-322baf0a6398 | 22.4% | 0.0111 |
| lesjeudis | 2024-Q3 | 3566 | 0.0039 | 98.8% | 8.3 | http://data.europa.eu/esco/skill/d4789070-2ff7-4bbb-94ca-8bb1739826a9 | 16.7% | 0.0131 |
| lesjeudis | 2024-Q4 | 5691 | 0.0031 | 98.6% | 8.3 | http://data.europa.eu/esco/skill/f3c5fae0-c0e3-4410-bc09-62bd82d4cecc | 12.2% | 0.0121 |
| lesjeudis | 2025-Q1 | 2985 | 0.0032 | 98.5% | 8.3 | http://data.europa.eu/esco/skill/2fb8480e-de3c-462b-b169-e8bbb344da68 | 12.8% | 0.0156 |
| lesjeudis | 2025-Q2 | 306 | 0.0042 | 100.0% | 8.5 | http://data.europa.eu/esco/skill/de4bd326-332c-4e03-9d61-1b810d4a3e8e | 18.1% | 0.0215 |
| jobsde | 2024-Q3 | 3253 | 0.0039 | 93.4% | 4.5 | http://data.europa.eu/esco/skill/a472a200-d895-40ca-95e7-5c5495e3dd7c | 10.9% | 0.0366 |
| jobsde | 2024-Q4 | 5519 | 0.0033 | 88.5% | 4.2 | http://data.europa.eu/esco/skill/113b4428-0a31-4199-8496-070af7854b91 | 7.5% | 0.0331 |
| jobsde | 2025-Q1 | 3122 | 0.0048 | 86.8% | 4.4 | http://data.europa.eu/esco/skill/a472a200-d895-40ca-95e7-5c5495e3dd7c | 11.3% | 0.0611 |
| jobsde | 2025-Q2 | 349 | 0.0070 | 100.0% | 4.8 | http://data.europa.eu/esco/skill/a472a200-d895-40ca-95e7-5c5495e3dd7c | 18.2% | 0.2090 |

## Field coverage by month (share of weighted postings with the field filled)

| board | month | taken | skills | sectors | occupations |
|---|---|---|---|---|---|
| jobbland | 2024-08 | 1777 | 94.5% | 88.1% | 94.1% |
| jobbland | 2024-09 | 2187 | 93.6% | 90.5% | 94.8% |
| jobbland | 2024-10 | 2759 | 95.2% | 90.4% | 94.6% |
| jobbland | 2024-11 | 2828 | 94.6% | 87.9% | 93.9% |
| jobbland | 2024-12 | 2585 | 96.9% | 91.3% | 95.7% |
| jobbland | 2025-01 | 2847 | 94.8% | 90.6% | 94.4% |
| jobbland | 2025-02 | 1478 | 94.0% | 91.1% | 93.7% |
| jobbland | 2025-03 | 1190 | 99.6% | 91.1% | 94.6% |
| jobbland | 2025-04 | 287 | 100.0% | 91.3% | 94.1% |
| lesjeudis | 2024-08 | 1348 | 99.3% | 96.8% | 98.0% |
| lesjeudis | 2024-09 | 2218 | 98.5% | 94.2% | 96.3% |
| lesjeudis | 2024-10 | 1975 | 99.0% | 95.8% | 97.8% |
| lesjeudis | 2024-11 | 1981 | 97.7% | 95.4% | 96.9% |
| lesjeudis | 2024-12 | 1735 | 99.0% | 95.7% | 97.2% |
| lesjeudis | 2025-01 | 1792 | 98.0% | 94.0% | 96.8% |
| lesjeudis | 2025-02 | 983 | 99.2% | 96.0% | 96.9% |
| lesjeudis | 2025-03 | 210 | 100.0% | 94.2% | 96.9% |
| lesjeudis | 2025-04 | 306 | 100.0% | 97.2% | 98.1% |
| jobsde | 2024-08 | 1145 | 93.2% | 87.5% | 95.5% |
| jobsde | 2024-09 | 2108 | 93.5% | 87.4% | 95.6% |
| jobsde | 2024-10 | 1863 | 87.7% | 82.5% | 90.9% |
| jobsde | 2024-11 | 1975 | 88.5% | 79.1% | 87.6% |
| jobsde | 2024-12 | 1681 | 89.9% | 81.6% | 88.8% |
| jobsde | 2025-01 | 979 | 82.7% | 79.6% | 86.0% |
| jobsde | 2025-02 | 1308 | 80.7% | 76.6% | 84.2% |
| jobsde | 2025-03 | 835 | 100.0% | 90.7% | 97.4% |
| jobsde | 2025-04 | 349 | 100.0% | 92.8% | 97.2% |
