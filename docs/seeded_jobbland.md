# Seeded clustering with the named occupations: jobbland

53,959 postings. Centre = mean title embedding of the postings whose cleaned title matches the occupation; a posting joins when its cosine similarity to the centre is at least the threshold; the matching postings always belong.

## Seeds

| occupation | titles matching | used as a centre |
|---|---|---|
| trade compliance officer | 5 | yes |
| export control specialist | 8 | yes |
| supply chain resilience analyst | 1 | no (fewer than 5) |
| semiconductor process engineer | 0 | no (fewer than 5) |
| battery cell technician | 6 | yes |
| critical materials specialist | 0 | no (fewer than 5) |
| reshoring program manager | 0 | no (fewer than 5) |

## The seed titles

- trade compliance officer: Trade Compliance Officer & Project Support (1); Trade Compliance Representative (1); Global Trade Compliance Leader (1); Trade Compliance Officer (1); Global Trade Compliance - Project Manager - epiroc (1)
- export control specialist: Export Control Analyst (2); Export Control Manager (2); TULL24STO, Export Control, 10Yhp, v18-19, VT25 (1); Consultant within export control and regulatory requirements (1); Customs and Export Control Specialist (1); Authority officer responsible for export control to nuclear ver (1)
- battery cell technician: Machine Vision Engineer - Battery Cell Process & Equipment Engineering (1); Automation Engineer - Battery Cell Process & Equipment Engineering (1); Manager Engineering - Battery Cell Process & Equipment Engineering (1); Battery mechanic/Technician (1); Battery Manufacturing Operator Technician (1); Batteribyggnationstekniker - Pilot Plant Battery Assembly (1)

## Calibration: how similar is similar?
multilingual-e5 gives high cosine similarity to almost any pair of short texts, so an absolute threshold such as 0.85 means little. Background = the similarity of ALL postings of the board to the centre. Seed leave-one-out = each seed posting against the centre made from the others.

| occupation | background median | background 95th pct | background 99th pct | seed leave-one-out lowest | median | highest |
|---|---|---|---|---|---|---|
| trade compliance officer | 0.825 | 0.860 | 0.872 | 0.911 | 0.954 | 0.965 |
| export control specialist | 0.832 | 0.868 | 0.881 | 0.860 | 0.959 | 0.970 |
| battery cell technician | 0.830 | 0.875 | 0.892 | 0.907 | 0.947 | 0.959 |

Seed titles of export control specialist that are no more similar to the others than the background 99th percentile (outliers; the threshold ignores them): TULL24STO, Export Control, 10Yhp, v18-19, VT25 (0.860)

## Members by threshold
The last column uses the occupation's own seed-relative threshold = the larger of (the lowest leave-one-out seed similarity, the background 99th percentile); it is the one used for the series.

| occupation | seed (regex) | sim >= 0.90 | sim >= 0.92 | sim >= 0.94 | sim >= 0.96 | seed-relative threshold | members at it |
|---|---|---|---|---|---|---|---|
| trade compliance officer | 5 | 34 | 16 | 5 | 5 | 0.911 | 26 |
| export control specialist | 8 | 60 | 13 | 10 | 8 | 0.881 | 517 |
| battery cell technician | 6 | 147 | 11 | 7 | 6 | 0.907 | 45 |

## Members beyond the regex matches, to read for false positives
(seed-relative threshold; the most similar first)

### trade compliance officer: 21 postings beyond the 5 matching titles

- Compliance Officer (3)
- Trade Marketing Representative (3)
- Compliance Manager (2)
- Compliance Officer for Group Technology (2)
- Compliance Coordinator (1)
- International Trade Licence Officer (1)
- Legal & Compliance manager (1)
- Compliance Engineer (1)
- Compliance Quality Engineer (1)
- Customs & Trade Specialist (1)
- IT Compliance Officer (1)
- Security & Compliance Lead (1)

### export control specialist: 509 postings beyond the 8 matching titles

- Account Manager (65)
- Sales Manager (27)
- Business Controller (18)
- Sales Representative (11)
- Financial Controller (9)
- Category Manager (9)
- Senior Business Controller (8)
- Quality Manager (7)
- Accounting Economist (7)
- Group Business Controller (5)
- Operations Controller (4)
- Project Controller (4)

### battery cell technician: 39 postings beyond the 6 matching titles

- Electronics Engineer (7)
- Manufacturing Engineer (2)
- Battery Management System Engineer (1)
- System Design Engineer, Battery Systems (1)
- EMC Engineer for Battery Management Systems (1)
- Junior Battery Lab Engineer within the Automotive Industry (1)
- Quality Control Engineer - Cell Production (1)
- Test cell engineer/ Test Bed Engineer (1)
- Production engineer/ Production technician (1)
- Production technician / Process engineer for manufacturing industry (1)
- Technical Salesperson - Solar Cells and Batteries (1)
- Department Project Manager - Structural Battery Hardware (1)

## Monthly weighted share of the board (seed-relative threshold)

| month | trade compliance officer | export control specialist | battery cell technician |
|---|---|---|---|
| 2024-01 | 0.52% (1) | 4.25% (8) | 0.52% (1) |
| 2024-02 | 0.00% (0) | 2.10% (5) | 0.00% (0) |
| 2024-03 | 0.34% (1) | 1.03% (3) | 0.00% (0) |
| 2024-04 | 0.00% (0) | 1.02% (4) | 0.00% (0) |
| 2024-05 | 0.00% (0) | 1.39% (15) | 0.09% (2) |
| 2024-06 | 0.00% (0) | 0.91% (10) | 0.10% (2) |
| 2024-07 | 0.00% (0) | 1.55% (15) | 0.27% (3) |
| 2024-08 | 0.07% (2) | 1.48% (26) | 0.15% (3) |
| 2024-09 | 0.14% (1) | 0.95% (24) | 0.08% (3) |
| 2024-10 | 0.00% (0) | 1.18% (31) | 0.05% (2) |
| 2024-11 | 0.01% (1) | 0.98% (26) | 0.14% (3) |
| 2024-12 | 0.17% (3) | 0.75% (21) | 0.13% (2) |
| 2025-01 | 0.12% (5) | 0.40% (12) | 0.00% (0) |
| 2025-02 | 0.10% (1) | 0.63% (10) | 0.29% (3) |
| 2025-03 | 0.18% (1) | 0.86% (11) | 0.09% (2) |
| 2025-04 | 0.07% (1) | 1.10% (5) | 0.08% (1) |
| 2025-05 | 0.00% (0) | 0.90% (11) | 0.07% (1) |
| 2025-06 | 0.00% (0) | 1.52% (2) | 0.00% (0) |
| 2025-07 | 0.00% (0) | 0.36% (1) | 0.26% (1) |
| 2025-08 | 0.12% (2) | 1.39% (10) | 0.13% (2) |
| 2025-09 | 0.00% (0) | 0.46% (11) | 0.00% (0) |
| 2025-10 | 0.00% (0) | 1.26% (18) | 0.07% (1) |
| 2025-11 | 0.00% (0) | 1.66% (26) | 0.06% (2) |
| 2025-12 | 0.01% (1) | 2.04% (44) | 0.00% (0) |
| 2026-01 | 0.05% (1) | 0.93% (30) | 0.06% (2) |
| 2026-02 | 0.00% (0) | 0.56% (16) | 0.09% (2) |
| 2026-03 | 0.04% (1) | 1.36% (27) | 0.00% (1) |
| 2026-04 | 0.06% (1) | 0.42% (15) | 0.05% (1) |
| 2026-05 | 0.00% (0) | 0.53% (14) | 0.05% (1) |
| 2026-06 | 0.04% (1) | 0.67% (17) | 0.00% (1) |
| 2026-07 | 0.03% (1) | 0.99% (25) | 0.01% (1) |
| 2026-08 | 0.04% (1) | 0.87% (23) | 0.09% (2) |
| 2026-09 | 0.00% (0) | 0.80% (1) | 0.00% (0) |

Shares in percent of all weighted postings of the month; the number in brackets is the postings taken. Months with few sampled days (see the coverage table of script 93) are unreliable.

## Where the members fall in the HDBSCAN clustering (input A)

| occupation | members | in noise | largest HDBSCAN clusters (members) |
|---|---|---|---|
| trade compliance officer | 26 | 10 | C263 (15), C291 (1) |
| export control specialist | 517 | 159 | C250 (65), C330 (60), C257 (28), C249 (27) |
| battery cell technician | 45 | 22 | C356 (9), C232 (3), C266 (3), C321 (2) |

