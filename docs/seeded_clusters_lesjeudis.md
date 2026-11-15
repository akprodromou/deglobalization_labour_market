# Seeded clustering with the named occupations: lesjeudis

18,625 postings. Centre = mean title embedding of the postings whose cleaned title matches the occupation; a posting joins when its cosine similarity to the centre is at least the threshold; the matching postings always belong.

## Seeds

| occupation | titles matching | used as a centre |
|---|---|---|
| C33 | 73 | yes |
| C68 | 141 | yes |
| C137 | 230 | yes |
| C130 | 199 | yes |
| C139 | 201 | yes |

## The seed titles

- C33: IVVQ engineer (8); IVVQ Engineer (5); Ingénieur IVVQ (4); Responsable IVVQ (2); IVV Engineer (2); IVVQ engineer - Defense (2); IVVQ Radar engineer (2); Functional IVV engineer (2); IVVQ Cloud Engineer (1); IVVQ Technician (1); IVV system engineer (1); IVVQ Manager CybAir (1); IVVQ Radar Engineer (1); IVV Digital Radar Engineer (1); Software IVQ Manager (SwIVQM) (1)
- C68: Embedded Software Engineer (6); Embedded software engineer (3); Aeronautical Embedded Software Engineer - Industry (2); Embedded development engineer Matlab Simulink (2); Experienced embedded software development engineer (2); Embedded Systems Engineer (2); CDI embedded engineer CDI (2); Embedded software test engineer - Defense (2); On -board development engineer - aeronautics (2); Embedded electronic systems engineer (2); Embedded software development engineer - aeronautics (2); Embedded software engineer - Debeug Android & Android System - Automobile Domain (2); Embedded software development engineer - Autonomous vehicle (2); F.H on -board software development engineer (2); Embedded Tester (2)
- C137: Ingénieur Système (7); Ingénieur Systèmes (6); Ingénieur Qualité éléctronique (5); Ingénieur Intégration Systèmes (5); Ingénieur conception mécanique et méthodes industrielles (4); Naval engineer - Design/Mechanical design (4); Développeur Python - Nucléaire (3); Ingénieur Méthodes Electronique (3); Ingénieur Calcul en simulation numérique à Bouguenais (44) (3); Ingénieur Naval - Calcul de Structure (3); Ingénieur naval - Concepteur / Dessinateur projeteur (3); Naval engineer - Electric Studies Office (3); Naval engineer - Designer / Projector designer (3); Naval engineer - Structure calculation (3); FOLDER-WELDER (SE) TIG or MIG-MAG (2)
- C130: Electronics Engineer (4); Electronic Methods Engineer (4); General Installation Designer (3); Mechanical development engineer (3); Electronic quality engineer (3); Mechanical design engineer and industrial methods (3); Mechanical engineer (3); General Installations Designer (2); Electronic Hardware Engineer (2); Project quality engineer - Industry (2); Mechanical Design/Design Engineer (2); Electronic Quality Engineer (2); Power electronics engineer (2); Hardware Electronics Project Manager Engineer (2); Electrical Design Office Engineer (2)
- C139: Cybersecurity engineer (8); Network and Security Engineer (5); Security and Network Engineer (3); Cybersecurity Auditor (3); Cybersecurity Engineer (3); Network and security engineer (3); Network and Security Engineers (2); Technical Auditor - Cybersecurity (2); HSM Expert - Cybersecurity (2); Network security engineer - Cybersecurity (2); Cyber Technical Engineer Junior (2); Industrial Cybersecurity Engineer (2); Engineer / Cybersecurity Expert - Splunk / Cortex XSOAR / Windows and Linux (2); Cybersecurity/IS Audit Specialist (2); Security Engineer (2)

## Calibration: how similar is similar?
multilingual-e5 gives high cosine similarity to almost any pair of short texts, so an absolute threshold such as 0.85 means little. Background = the similarity of ALL postings of the board to the centre. Seed leave-one-out = each seed posting against the centre made from the others.

| occupation | background median | background 95th pct | background 99th pct | seed leave-one-out lowest | median | highest |
|---|---|---|---|---|---|---|
| C33 | 0.862 | 0.893 | 0.905 | 0.869 | 0.952 | 0.987 |
| C68 | 0.879 | 0.915 | 0.933 | 0.866 | 0.946 | 0.983 |
| C137 | 0.889 | 0.932 | 0.949 | 0.868 | 0.940 | 0.965 |
| C130 | 0.890 | 0.930 | 0.942 | 0.857 | 0.932 | 0.963 |
| C139 | 0.881 | 0.923 | 0.944 | 0.860 | 0.947 | 0.983 |

Seed titles of C33 that are no more similar to the others than the background 99th percentile (outliers; the threshold ignores them): RIVQ (0.869); IVQ IVQ SDR Tactical platform (0.887); IVVQ Manager - Airlance control system - Defense & Security BU (0.900)

Seed titles of C68 that are no more similar to the others than the background 99th percentile (outliers; the threshold ignores them): Responsible for the Development Resources Pole F.H Digital Solutions (0.866); Referent IV on-board computers (SW/HW) (0.878); on -board software architect (0.878); Architect software real -time platform on board (0.883); Embaquated engineer Scade (0.890); Airbus UpNext - On-board Mission Software Developer -CI/CD & Modern Practices (0.892); F.H software section manager (0.893); Software Architect_On Board Signalling Product (0.900); and 37 more

Seed titles of C137 that are no more similar to the others than the background 99th percentile (outliers; the threshold ignores them): HVAC Supervisor - Luxury Cruise Ships (0.868); Electric Cableur-Coffrets Tablet (0.874); FOLDER-WELDER (SE) TIG or MIG-MAG (0.880); FOLDER-WELDER (SE) TIG or MIG-MAG (0.880); Technicien(ne) Etude des conditions de recyclabilité de composites thermoplastiques pultrudables pour application rails de chemin de fer innovants - CDD 12 mois - IMT Mines Alès (0.884); Internship - Scientific Application Development - Nuclear (0.885); Développement Python: indexation de données & flux d'orchestration pour analyse de données massives (0.886); Mise en oeuvre d'un framework de Federated Learning pour l'Actuariat basé sur des données autonome (0.895); and 154 more

Seed titles of C130 that are no more similar to the others than the background 99th percentile (outliers; the threshold ignores them): Engineer Backup Flight Spatial launchers (0.857); ETR of digital systems (0.864); Simulation Service Owner (0.880); Engineer simulations dismantling (0.883); Heavy vehicle mechanical trainer (0.884); Vice-Président Rail Simulation (0.884); Metal materials specialist and surface treatment (0.886); Aeronautical quality engineer leaves 145 (0.888); and 147 more

Seed titles of C139 that are no more similar to the others than the background 99th percentile (outliers; the threshold ignores them): OFFICER COUNTER CYBER ZONAL INTERFERENCE (0.860); Expert Cisco Ironport and messaging (0.874); Operational security networks (0.878); BP2I - Security Gouvernance Analyst (0.884); Cybersecurity Risk Analyst Gouvernance - CCDP (0.886); Cyber ​​tools application driver (0.887); Accessibility Auditor (0.890); Safety engineer Specialization detection and N3 analyst (0.890); and 83 more

## Members by threshold
The last column uses the occupation's own seed-relative threshold = the larger of (the lowest leave-one-out seed similarity, the background 99th percentile); it is the one used for the series.

| occupation | seed (regex) | sim >= 0.90 | sim >= 0.92 | sim >= 0.94 | sim >= 0.96 | seed-relative threshold | members at it |
|---|---|---|---|---|---|---|---|
| C33 | 73 | 83 | 78 | 74 | 73 | 0.918 | 81 |
| C68 | 141 | 728 | 290 | 172 | 142 | 0.933 | 186 |
| C137 | 230 | 3815 | 2054 | 583 | 237 | 0.949 | 344 |
| C130 | 199 | 3436 | 1433 | 402 | 199 | 0.942 | 388 |
| C139 | 201 | 1281 | 619 | 301 | 209 | 0.944 | 271 |

## Members beyond the regex matches, to read for false positives
(seed-relative threshold; the most similar first)

### C33: 8 postings beyond the 73 matching titles

- Ingénieur vérificateur logiciel IVVQ (1)
- Electronic IVV engineer - power electronics (1)
- IVVQ Engineer (Integration Validation Validation Qualification) / V&V (1)
- Responsable IVVQ - Système de Défense Anti-Aérienne (1)
- IVVQ engineer/Test Top Box Test and Validation (1)
- Engineering Delivery Manager & IVV Manager (1)
- Responsable IVVQ - BU Défense & Sécurité (1)
- Ingénieur IVV Displays Front End (1)

### C68: 45 postings beyond the 141 matching titles

- Software Development Engineer (10)
- Embedded C/C++ Developer (4)
- Embedded C++/QT Software Architect CDI (2)
- Embedded Linux Software Engineer (1)
- Embedded Systems Development Engineer C/C++ (1)
- Embedded C++ development engineer (1)
- Embedded development engineer - Linux environment CDI (1)
- Embedded development engineer - Linux environment (1)
- Embedded developer C ++ / QT (1)
- C/C++ Embedded Systems Design and Development Engineer (1)
- Developer C ++ embedded (1)
- Linux embedded systems engineer (1)

### C137: 114 postings beyond the 230 matching titles

- Ingénieur système informatique (5)
- Ingénieur Sécurité Informatique (3)
- Ingénieur Systèmes et Réseaux (3)
- Ingénieur Système Windows (3)
- Ingénieur Système Linux (3)
- Ingénieur SysOps (3)
- Technicien Systèmes et Réseaux (3)
- Ingénieur Systèmes Embarqués (2)
- Ingénieur Systèmes et Cloud (2)
- Ingénieur systèmes et datacenter (2)
- Ingénieur QA/ QA engineer (2)
- Ingénieur Cybersécurité Industrielle (2)

### C130: 189 postings beyond the 199 matching titles

- Data Engineer (96)
- Software Engineer (31)
- Systems Engineer (13)
- System Engineer (11)
- Artificial Intelligence Engineer (8)
- System engineer (5)
- AI Engineer (5)
- Systems engineer (3)
- IT System Engineer (2)
- Test Engineer (2)
- IT Systems Engineer (1)
- Data Engineering System Engineer (1)

### C139: 70 postings beyond the 201 matching titles

- Cloud Security Engineer (3)
- Cybersecurity architect (3)
- Cybersecurity engineer - Defense and Security (2)
- Software Engineer, Security (2)
- DevOps Engineer - Cybersecurity (2)
- Cyber Security Pre-Sales Engineer (2)
- Cybersecurity Consultant (2)
- Consultant in cybersecurity (2)
- Network security engineer - Infrastructure (2)
- Cybersecurity Architect (2)
- Cybersecurity Manager (2)
- Cyber Security Architect (2)

## Monthly weighted share of the board (seed-relative threshold)

| month | C33 | C68 | C137 | C130 | C139 |
|---|---|---|---|---|---|
| 2024-08 | 0.34% (4) | 1.52% (27) | 0.33% (1) | 3.03% (49) | 2.84% (34) |
| 2024-09 | 0.22% (6) | 1.18% (25) | 0.35% (7) | 2.96% (58) | 1.83% (48) |
| 2024-10 | 0.23% (6) | 1.90% (20) | 0.22% (4) | 2.60% (61) | 1.28% (33) |
| 2024-11 | 0.40% (8) | 0.29% (7) | 3.50% (86) | 1.26% (21) | 0.75% (24) |
| 2024-12 | 0.27% (6) | 0.18% (5) | 4.70% (95) | 1.09% (22) | 0.38% (5) |
| 2025-01 | 0.08% (3) | 0.12% (2) | 3.57% (82) | 1.75% (21) | 0.62% (9) |
| 2025-02 | 0.17% (2) | 0.59% (6) | 3.32% (41) | 0.97% (10) | 0.73% (8) |
| 2025-03 | 0.32% (1) | 0.47% (1) | 0.00% (0) | 1.90% (4) | 0.95% (2) |
| 2025-04 | 0.52% (2) | 1.17% (4) | 0.95% (5) | 2.57% (9) | 2.17% (8) |
| 2025-05 | 0.94% (10) | 1.37% (17) | 1.76% (4) | 1.15% (17) | 1.86% (23) |
| 2025-06 | 0.49% (10) | 1.49% (23) | 0.24% (6) | 2.38% (43) | 1.48% (28) |
| 2025-07 | 0.38% (3) | 2.67% (15) | 0.32% (1) | 2.21% (14) | 1.34% (10) |
| 2025-08 | 0.72% (15) | 1.61% (26) | 0.20% (5) | 2.40% (43) | 1.16% (23) |
| 2025-09 | 0.41% (5) | 0.98% (8) | 1.06% (7) | 1.48% (16) | 1.48% (16) |

Shares in percent of all weighted postings of the month; the number in brackets is the postings taken. Months with few sampled days (see the coverage table of script 93) are unreliable.

## Where the members fall in the HDBSCAN clustering (input A)

| occupation | members | in noise | largest HDBSCAN clusters (members) |
|---|---|---|---|
| C33 | 81 | 5 | C33 (73), C140 (1), C84 (1), C130 (1) |
| C68 | 186 | 14 | C68 (141), C69 (19), C63 (6), C59 (1) |
| C137 | 344 | 42 | C137 (230), C131 (25), C126 (11), C143 (8) |
| C130 | 388 | 5 | C130 (199), C28 (50), C27 (48), C127 (37) |
| C139 | 271 | 28 | C139 (201), C56 (10), C114 (7), C128 (6) |

