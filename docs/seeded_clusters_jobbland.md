# Seeded clustering with the named occupations: jobbland

53,959 postings. Centre = mean title embedding of the postings whose cleaned title matches the occupation; a posting joins when its cosine similarity to the centre is at least the threshold; the matching postings always belong.

## Seeds

| occupation | titles matching | used as a centre |
|---|---|---|
| C350 | 193 | yes |
| C291 | 108 | yes |
| C263 | 81 | yes |
| C266 | 82 | yes |
| C283 | 262 | yes |

## The seed titles

- C350: System Engineer (10); Systems engineer (6); Security Engineer (5); Systems Engineer (5); Network Engineer (4); System Study Engineer (3); Senior Network Engineer (3); System engineer (3); System Safety Engineer (3); Control system engineer (3); Control Systems Engineer (3); Cyber Security Engineer (2); Development Engineer - Functional Safety (2); Network Security Engineer (2); System Security Engineer (2)
- C291: Quality Engineer (17); Quality engineer (8); Quality Assurance Specialist (4); Advanced Quality Engineer (2); Quality Control Engineer (2); Quality Specialist (2); Quality -Eskjör - Industry (2); Quality technician (2); Quality-conscious operators (2); Production Quality Engineer Specialist (1); Quality & Continuous Improvement Specialists (1); Quality and Test specialist (1); Controlor de Calitate (1); Quality Engineer for Production (1); QA Specialist - Microbiological Quality Assurance (1)
- C263: Compliance Officer (3); Compliance Manager (2); Compliance Officer for Group Technology (2); Safety Assurance Manager (2); IT Manager (2); System manager (2); IT manager (2); Trade Compliance Officer & Project Support (1); Security Protection Manager (1); Group Compliance Risk Manager - Webhelp (1); Team Manager - Compliance & Tech (1); IT-Manager to Avinode Group (1); IT Risk manager (1); System Manager HR (1); IT RISK AND COMPLIANCE MANAGER (1)
- C266: Process Engineer (8); Experienced process engineer (6); Process engineer (5); Material Engineer (2); Engineer for the process industry towards data and digitalisation (2); Materials Engineer (2); Process Equipment Installation Engineer (1); Process engineer in wastewater treatment (1); Process engineer within wastewater treatment (1); Process engineer - Plasma (1); Internship CAD engineer in process industry - Rejlers (1); Senior Material Engineer (1); Process Development Scientist/Sr. Scientist (1); Process engineer with experience in MIBI & FUP (1); Process Engineer - Annealing & Galvanising (1)
- C283: Commercial manager - Fastighets AB Balder (2); Project manager IT for our Stockholm office (2); Country IT Manager - Sweden & Oversight Countries (2); Project manager - Fastighets AB Balder (2); Technical Manager at 1621.Flygbaskompaniet to F 16 (2); Project manager Västerås, Mälardalen (2); contractors - the Swedish Traffic Agency (2); Deputy Technical Project Manager for a long consulting assignment in Skåne - Devotion (1); lawyer for the office in Lund - Advokatbyrån Gulliksson (1); Requirements and systems engineer with a heart for Sweden's security (1); corporate lawyer for Pincho's head office in Gothenburg - Pinchos (1); Work as Frontliner for the Swedish Society for Nature Conservation (1); Trainee program Umeå VT - Secure digitization (1); Design manager unit POP program Mälarbanan (1); Project manager - road and construction projects - Södermanland (1)

## Calibration: how similar is similar?
multilingual-e5 gives high cosine similarity to almost any pair of short texts, so an absolute threshold such as 0.85 means little. Background = the similarity of ALL postings of the board to the centre. Seed leave-one-out = each seed posting against the centre made from the others.

| occupation | background median | background 95th pct | background 99th pct | seed leave-one-out lowest | median | highest |
|---|---|---|---|---|---|---|
| C350 | 0.856 | 0.907 | 0.937 | 0.872 | 0.943 | 0.976 |
| C291 | 0.852 | 0.895 | 0.917 | 0.879 | 0.953 | 0.986 |
| C263 | 0.867 | 0.910 | 0.927 | 0.867 | 0.930 | 0.961 |
| C266 | 0.855 | 0.899 | 0.926 | 0.857 | 0.943 | 0.979 |
| C283 | 0.866 | 0.896 | 0.911 | 0.857 | 0.917 | 0.952 |

Seed titles of C350 that are no more similar to the others than the background 99th percentile (outliers; the threshold ignores them): System engineer propulsion system Surface vessels (0.872); Functional Safety Consultant - Process and Product Compliance (0.881); EQUIPMENT REPORTER for the Air Base Security Company (0.881); Functional Safety Consultant (0.886); Senior Functional Safety Consultant (0.887); Il's engineer (0.888); NETWORK MANAGER (0.889); ILS ingenjör (0.892); and 68 more

Seed titles of C291 that are no more similar to the others than the background 99th percentile (outliers; the threshold ignores them): SAMD24LIN, Quality work (0.879); Qualification specialist - UPLC/HPLC (0.894); quality developers for our new quality initiative (0.901); Quality conscious operators are sought (0.901); Quality Assurance Associate, Xspray Pharma (0.902); Quality -Eskjör - Industry (0.904); Quality -Eskjör - Industry (0.904); Quality Auditor - Shift - 12 month FTC (0.904); and 9 more

Seed titles of C263 that are no more similar to the others than the background 99th percentile (outliers; the threshold ignores them): Head of Data & Technology to Public Property Invest - Ants (0.867); Device Manager Security Protection - SKB (0.884); Chief Information Security Officer (CISO) to Atlantic Container Line - Ants (0.887); Experienced Team Leader for technical consulting assignment (0.889); SECURITY MANAGER FOR PINGDAY (0.893); IT and marketing (0.896); iGaming Licensing & Compliance Specialist (0.897); Compliance Coordinator - 10 month maternity cover (0.898); and 30 more

Seed titles of C266 that are no more similar to the others than the background 99th percentile (outliers; the threshold ignores them): SHE Divisional Business Partner - Element Materials Technology (0.857); Graduate Engineer - Aerospace Graduate Programme 2026/2027 - Element Materials Technology (0.865); Material Innovation Internship (0.880); Material Technician to 124.The Led Rire (0.883); Experienced and driven quality engineers who want to take the next step in their career (0.891); Expertise in additive manufacturing (0.891); QMS ASPICE Process Expert (0.893); Internship CAD engineer in process industry - Rejlers (0.897); and 12 more

Seed titles of C283 that are no more similar to the others than the background 99th percentile (outliers; the threshold ignores them): detectives for the customs crime unit north - the customs office (0.857); Functional representative Materiel data within the Armed Forces' logistics (0.862); Platoon leader for 1614. Strilförsvarskompaniet, F16 (0.866); Quartermaster at 1614 Artillery Defense Company to F 16 - THE DEFENSES (0.866); The Customs Administration seeks customs inspector internal control (0.868); Minesoldiers for the amphibious company at the 5th amphibious battalion - THE DEFENSE FORCES (0.869); The Customs Administration seeks customs inspector internal control, mockery (0.876); Head of Collections - Museum of Furniture Studies (0.876); and 95 more

## Members by threshold
The last column uses the occupation's own seed-relative threshold = the larger of (the lowest leave-one-out seed similarity, the background 99th percentile); it is the one used for the series.

| occupation | seed (regex) | sim >= 0.90 | sim >= 0.92 | sim >= 0.94 | sim >= 0.96 | seed-relative threshold | members at it |
|---|---|---|---|---|---|---|---|
| C350 | 193 | 2710 | 1398 | 497 | 194 | 0.937 | 587 |
| C291 | 108 | 648 | 277 | 184 | 111 | 0.917 | 319 |
| C263 | 81 | 4030 | 1267 | 102 | 81 | 0.927 | 543 |
| C266 | 82 | 746 | 241 | 124 | 82 | 0.926 | 201 |
| C283 | 262 | 1777 | 357 | 262 | 262 | 0.911 | 636 |

## Members beyond the regex matches, to read for false positives
(seed-relative threshold; the most similar first)

### C350: 394 postings beyond the 193 matching titles

- Data Engineer (66)
- Software Engineer (40)
- Automation engineer (26)
- DevOps Engineer (24)
- Mechanical Engineer (21)
- Senior Software Engineer (18)
- Test Engineer (14)
- Automation Engineer (13)
- Electronics engineer (11)
- Electrical Engineer (8)
- Electronics Engineer (7)
- System Design Engineer (5)

### C291: 211 postings beyond the 108 matching titles

- Inspection technician (19)
- Maintenance technician (11)
- Supplier Quality Engineer (10)
- Maintenance Technician (9)
- Quality Manager (7)
- Quality Engineer - Electrical (6)
- Quality manager (4)
- Measurement technician (4)
- QA Engineer (3)
- Quality Coordinator (3)
- Engineering Quality Manager (2)
- Software Quality Assurance Engineer (2)

### C263: 462 postings beyond the 81 matching titles

- Account Manager (70)
- Project manager (58)
- Project Manager (44)
- Sales Manager (27)
- Operations manager (21)
- Operations Manager (14)
- Site Manager (12)
- Group Manager (12)
- Service manager (11)
- Accounting manager (10)
- Team Manager (10)
- Service Manager (9)

### C266: 119 postings beyond the 82 matching titles

- Production Engineer (12)
- Production engineer (6)
- Senior Process Engineer (4)
- Product Lifecycle Engineer (4)
- Process Operator (4)
- Plumbing engineer (4)
- Mechanic/Mechanical engineer (3)
- Automation engineer for leading company (3)
- Manufacturing Engineer (2)
- Process technician (2)
- Automation engineer in production (2)
- Plumbing Engineer (2)

### C283: 374 postings beyond the 262 matching titles

- regional manager for our Swedish sales team (3)
- Manager Civil Administration to Vattenfall - Sustainable Power for generations (3)
- Field technician for Liebherr in the Stockholm area (2)
- Customer service employee for our Swedish team in Larnaca, Cyprus (2)
- Customer advisor with a focus on appointment booking for Swedish Real Estate Agency (2)
- Business salesperson for Sweden's largest supplier in IT and Telecom (2)
- Seller in FoodTech - Swedish speaking (2)
- Engineers for one of Sweden's best employers (2)
- Installation electrician for Sweden's leading solar company - Svea Solar (2)
- Junior Customer Service Agent [Swedish speaking] (2)
- Swedish-speaking customer service agent (2)
- Swedish Business Development Consultant (2)

## Monthly weighted share of the board (seed-relative threshold)

| month | C350 | C291 | C263 | C266 | C283 |
|---|---|---|---|---|---|
| 2024-01 | 3.26% (6) | 1.57% (3) | 1.57% (3) | 1.05% (2) | 1.05% (2) |
| 2024-02 | 2.85% (7) | 0.88% (2) | 0.81% (2) | 0.00% (0) | 1.69% (4) |
| 2024-03 | 2.76% (8) | 1.03% (3) | 1.72% (5) | 0.34% (1) | 0.69% (2) |
| 2024-04 | 2.72% (8) | 1.21% (3) | 2.12% (6) | 0.30% (1) | 1.03% (4) |
| 2024-05 | 1.86% (22) | 2.49% (14) | 1.35% (16) | 0.90% (16) | 1.17% (14) |
| 2024-06 | 2.82% (25) | 0.97% (11) | 1.14% (17) | 0.75% (10) | 0.70% (7) |
| 2024-07 | 1.88% (29) | 0.91% (11) | 1.78% (20) | 0.48% (7) | 0.40% (8) |
| 2024-08 | 1.49% (25) | 1.56% (21) | 1.40% (26) | 0.31% (7) | 0.45% (9) |
| 2024-09 | 1.91% (44) | 0.86% (17) | 1.16% (27) | 0.54% (14) | 0.66% (17) |
| 2024-10 | 0.79% (20) | 1.05% (31) | 0.97% (24) | 0.37% (11) | 0.73% (18) |
| 2024-11 | 1.13% (26) | 0.33% (9) | 0.73% (23) | 0.20% (6) | 0.37% (10) |
| 2024-12 | 0.99% (20) | 0.52% (11) | 0.47% (9) | 0.11% (4) | 0.09% (2) |
| 2025-01 | 0.64% (20) | 0.38% (10) | 0.53% (19) | 0.06% (4) | 0.05% (3) |
| 2025-02 | 0.85% (16) | 0.39% (6) | 1.12% (14) | 0.68% (9) | 0.48% (9) |
| 2025-03 | 0.26% (5) | 0.32% (5) | 1.11% (11) | 0.27% (5) | 0.38% (3) |
| 2025-04 | 1.06% (11) | 0.49% (1) | 1.39% (10) | 0.07% (1) | 0.68% (5) |
| 2025-05 | 1.87% (13) | 0.49% (9) | 0.94% (15) | 0.20% (4) | 0.95% (14) |
| 2025-06 | 0.00% (0) | 0.76% (1) | 3.91% (5) | 0.76% (1) | 0.76% (1) |
| 2025-07 | 0.44% (2) | 0.00% (0) | 0.79% (3) | 0.36% (1) | 1.45% (5) |
| 2025-08 | 1.26% (15) | 0.87% (8) | 1.36% (11) | 1.34% (8) | 0.93% (16) |
| 2025-09 | 1.29% (24) | 0.45% (8) | 1.02% (12) | 0.08% (2) | 1.87% (24) |
| 2025-10 | 2.21% (31) | 0.70% (10) | 1.17% (17) | 0.75% (10) | 1.70% (24) |
| 2025-11 | 1.36% (34) | 0.46% (8) | 0.98% (18) | 0.17% (4) | 4.00% (17) |
| 2025-12 | 1.28% (32) | 0.91% (18) | 2.87% (49) | 1.12% (18) | 0.35% (9) |
| 2026-01 | 0.61% (15) | 0.50% (16) | 0.91% (27) | 0.31% (10) | 1.75% (41) |
| 2026-02 | 0.69% (24) | 0.19% (5) | 0.64% (18) | 0.35% (7) | 2.71% (63) |
| 2026-03 | 0.81% (25) | 0.42% (14) | 0.80% (19) | 0.13% (4) | 1.76% (50) |
| 2026-04 | 0.18% (10) | 0.31% (6) | 0.54% (17) | 0.20% (6) | 2.41% (56) |
| 2026-05 | 0.92% (19) | 0.46% (13) | 0.80% (20) | 0.38% (8) | 1.72% (39) |
| 2026-06 | 0.78% (20) | 0.73% (17) | 0.68% (18) | 0.16% (8) | 1.37% (39) |
| 2026-07 | 0.64% (19) | 0.65% (11) | 1.39% (38) | 0.19% (6) | 1.82% (50) |
| 2026-08 | 0.34% (11) | 0.74% (17) | 1.01% (24) | 0.23% (6) | 2.02% (63) |
| 2026-09 | 0.80% (1) | 0.00% (0) | 0.00% (0) | 0.00% (0) | 5.34% (8) |

Shares in percent of all weighted postings of the month; the number in brackets is the postings taken. Months with few sampled days (see the coverage table of script 93) are unreliable.

## Where the members fall in the HDBSCAN clustering (input A)

| occupation | members | in noise | largest HDBSCAN clusters (members) |
|---|---|---|---|
| C350 | 587 | 85 | C350 (193), C60 (67), C47 (49), C109 (40) |
| C291 | 319 | 78 | C291 (108), C257 (58), C96 (21), C321 (20) |
| C263 | 543 | 79 | C263 (81), C250 (71), C78 (58), C112 (44) |
| C266 | 201 | 77 | C266 (82), C109 (9), C232 (5), C253 (5) |
| C283 | 636 | 200 | C283 (262), C284 (35), C288 (21), C295 (18) |

