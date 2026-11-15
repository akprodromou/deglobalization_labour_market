# Title coherence of the clusters: lesjeudis

18,625 postings. Coherence = length of the mean of the centred, unit title embeddings of a cluster (1 = identical titles, 0 = unrelated); lift = coherence minus that of random sets of the same size; top-token share = share of the cluster's titles holding its most frequent title word. The weak cutoff is the 10th percentile of the lift of the clusters of A (0.439), the same bar for every input. Input A is built from the title embedding alone, so it has an advantage on coherence by construction; read the top-token share next to it.

| input | clusters | noise | lift Q1 / median / Q3 | lift, median per posting | top-token share, median | clusters below the weak cutoff | postings in them (of clustered) |
|---|---|---|---|---|---|---|---|
| A | 144 | 30.9% | 0.486 / 0.543 / 0.595 | 0.535 | 87% | 15 (10%) | 1,370 (11%) |
| Dv2 | 142 | 20.6% | 0.200 / 0.261 / 0.402 | 0.258 | 43% | 119 (84%) | 13,169 (89%) |
| Dv3 | 102 | 30.6% | 0.478 / 0.540 / 0.597 | 0.518 | 88% | 14 (14%) | 1,763 (14%) |

Postings clustered in every input: 8,481 (45.5% of all).
Agreement of A and Dv2 on the 10,462 postings clustered in both: ARI 0.139 (1 = same partition; a value near 0.3 to 0.5 means the inputs group the postings quite differently).
Agreement of A and Dv3 on the 10,145 postings clustered in both: ARI 0.533 (1 = same partition; a value near 0.3 to 0.5 means the inputs group the postings quite differently).

## Weakest 12 clusters of A

| cluster | size | lift | top token (share) | top ESCO skill (share) | sample titles |
|---|---|---|---|---|---|
| 44 | 89 | 0.356 | contract (65%) | support employability of people with dis (15%) | BETC Fullsix - Confirmed Web Technical Consul / Management controller / Versatile technical agent for sports faciliti / Manufacturing Controller / A DATA SCIENTIST - - with a view to a permane |
| 22 | 114 | 0.358 | tech (35%) | innovation processes The techniques, mod (20%) | Coach Trainer - Tech Universe / Talent Acquisition Officer - Nantes (44) / Coach Trainer - Tech Universe / Publisher Sales Developer UK / Talent Acquisition Lead - /NB |
| 70 | 71 | 0.388 | data (51%) | facilities management in the organisatio (25%) | Construction project manager - Data Center / Technical director / Chef d'équipe technique pour notre Data Cente / IT Technical Director / System and Data Center Engineer |
| 109 | 50 | 0.390 | servicenow (60%) | support employability of people with dis (26%) | Analyste Fonctionnel / Consultant fonctionnel ServiceNow / Consultant technique Servicenow / Analyste Fonctionnel / Functional Analyst |
| 78 | 40 | 0.391 | consultant (52%) | support employability of people with dis (38%) | Ingénieur Développement SIRH / Chef de Projet SIRH / MOA project consultant - Insurance Insurance / Consultant(e) MOA / Business Analyst - Indust / Consultant Confirmé MOA - Cash Management - F |
| 130 | 199 | 0.395 | engineer (79%) | develop new products generate new produc (27%) | Simulation and performance algorithm engineer / Power electric engineer / Hardware engineer - Automobile team / Electronics Engineer / Electronic quality engineer |
| 137 | 230 | 0.420 | ingénieur (65%) | cyber security IT security information s (30%) | Naval engineer - Design/Mechanical design / Ingénieur Intégration Validation Logiciel / Ingénieur Qualité Fournisseurs / Maritime Engineer / Marine System Engineer / Ingénieur Intégration Logiciel AUTOSAR |
| 97 | 45 | 0.421 | engineer (76%) | gender studies the study of gender gende (31%) | Field Service Engineer Grid Automation / Application Engineer, Venue Acoustics / MES Thermal energy and nuclear installations / Technical functional applications engineer / Application engineer |
| 20 | 53 | 0.421 | engineer (57%) | support employability of people with dis (19%) | Production engineer / IT production engineer / Flow simulation pilot / Production engineer of calculation means / Technical Tester |
| 123 | 68 | 0.427 | consultant (91%) | consult with business clients consulting (24%) | Marine Advisor / Innovation designer consultant - Automotive s / Consultant Workday HCM / Strategy ATIOS Consultant / Consultant(e) Technology Advantage |
| 89 | 52 | 0.427 | assistant (88%) | show initiative take the initiative give (21%) | Assistante Administrative / Assistant AdministratIF - CDD / Sales and administrative assistant / Assistant (E) Administratif / Deputy CIO of the Unified Support Center |
| 7 | 89 | 0.430 | mainframe (58%) | DB2 DB2 database software DB2 Connect DB (45%) | Ingétrologie Mainframe Expert / Développeur(se) Cobol - Mainframe Confirmé(e) / AS400 Systems Administrator / Cobol/Mainframe - IBM Customer Consultant CON / Cobol Developer/Integrator |

## Weakest 12 clusters of Dv2

| cluster | size | lift | top token (share) | top ESCO skill (share) | sample titles |
|---|---|---|---|---|---|
| 32 | 46 | 0.109 | engineer (24%) | gender studies the study of gender gende (39%) | Assistant/Associate Professor in Neuro-Symbol / IT Business Analyst Banking CIB, Paris / Cobol/Mainframe - IBM Customer Consultant CON / Data Analyste Power BI - junior(e) ou expérim / Technical Recruiter |
| 102 | 156 | 0.114 | data (34%) | SQL Informix 4GL/SQL SEQUEL Subquery The (100%) | Data Scientist - Innovation / Digital / Proje / Senior developer / Life & Health Pricing Actuary/Data scientist / Data ops confirmed / Lead Developer Java/Guidewire |
| 92 | 105 | 0.115 | data (32%) | business intelligence The tools used to  (100%) | ERP functional analyst / Researcher - Business Intelligence (French an / Business Developer - Data et IA / Architecte IT / DATA ENGINEER - Domaine DATA DECISIONNEL BI |
| 34 | 136 | 0.129 | developer (15%) | mobility disability mobility delay mobil (99%) | Project Manager / Technicien en électricité, automatismes et in / Consultant / Consultante Junior Data & IA / Google Appsheet Developer / Développeur Front-End React/Next.js Senior |
| 99 | 42 | 0.130 | data (48%) | data analytics data anlysis The science  (100%) | Senior PMO / Data Security, Risk & Compliance Manager / DATA ANALYST / Data Analyst (Power BI, SQL, Oracle) / Senior IT Auditor |
| 70 | 141 | 0.133 | manager (27%) | quantum mechanics the study of quantum m (100%) | Global Chapter Lead Architecture IS/IT / System engineer Validation / Versatile pyrotechnic operator / Technical project manager in the spatial fiel / Experienced research scientist-Photonic techn |
| 91 | 60 | 0.134 | engineer (32%) | Jenkins (tools for software configuratio (100%) | Développeur Python senior / Data Engineer - Banque / Backend Engineer / Production Engineer / Depreciation Fulltack Python / Django |
| 96 | 69 | 0.135 | data (39%) | data models The techniques and existing  (100%) | Administrateur Systèmes et Réseaux / Software Engineer, Integrations - TypeScript  / Data Analyst Power BI / Data Engineer MSBI Montpellier / IT system architect |
| 95 | 40 | 0.139 | engineer (52%) | debug software Repair computer code by a (88%) | Ingénieur/re Support Logiciel de Niveau 3 / Confirmed FULLSTACK Developer / Confirmed Kotlin Developer / FOTA validation engineer - Automotive / Digital Workflow Engineer /NB) |
| 76 | 60 | 0.142 | engineer (27%) | operate on-board computer systems utilis (33%) | Innovative systems validation engineer - Auto / Support technician / Confirmed C++ Development Engineer / Tech Lead RUN / Multipurpose IT technician and ELEC wiring |
| 60 | 123 | 0.146 | manager (20%) | develop digital content develop digital  (98%) | Quality Manager/IT Asset Manager / Chef de projet PLM / VMware Virtualization Engineer / IT Recruiter & Business Partner / Ingénieur Infrastructure SharePoint |
| 107 | 80 | 0.151 | data (52%) | data warehouse The data storage system t (96%) | Data scientist / Group Data Management Officer / Data Steward / Senior Analytics Engineer Senior - Data Platf / Data Analyst / CDI - Product Data Analyst (Paris) |

## Weakest 12 clusters of Dv3

| cluster | size | lift | top token (share) | top ESCO skill (share) | sample titles |
|---|---|---|---|---|---|
| 34 | 97 | 0.325 | coordinator (26%) | support employability of people with dis (20%) | Coordinateur / Team Leader support informatique / IT coordinator / activity manager / Team Leader Support IT / IGC/PKI coordinator |
| 81 | 99 | 0.350 | ingénieur (39%) | quantum mechanics the study of quantum m (91%) | Event Thales - The RDV of Talents - A Limours / Responsable ingénierie de spécialité / Responsable fonctionnel et technique projet S / Responsable d'Offres - Solutions de Guerre El / Ingénieur Systèmes |
| 61 | 248 | 0.362 | engineer (47%) | Python (computer programming) Python 3K  (21%) | Physically-informed machine learning for mode / INTESCIA GROUP - Lead Machine Learning Engine / Compilation engineer position for machine lea / PhD Position Verifying Memory Safety of Linux / Digital simulation engineer |
| 69 | 305 | 0.374 | responsable (49%) | support employability of people with dis (12%) | Contrôleur de gestion / Chargé de Prospection / Responsable Veille Produits et Etudes Clients / Responsable Digital Scientifique Oncologie et / Responsable IT |
| 54 | 109 | 0.381 | industry (41%) | computer simulation computer-based simul (100%) | Engineer internship - Thermohydraulics Design / Développeur(se) C++ / Python environnement sc / Développeur Python - Nucléaire / Développeur(se) informatique géospatialisée s / Sector project manager - Energy - Aix en Prov |
| 17 | 60 | 0.401 | application (77%) | gender studies the study of gender gende (20%) | Application tester / Application Engineer / Field Application Specialist Research / MRI Application Engineer / Spontaneous Application - Propulsion |
| 6 | 68 | 0.418 | dba (50%) | PostgreSQL Postgres The computer program (53%) | Postgres & SQL Server Database Administrator / Expert Base de Données (DBA) - L3 / Confirmed PostgreSQL DBA - HF / Administrateur Bases de données / DBA |
| 8 | 90 | 0.421 | mainframe (54%) | DB2 DB2 database software DB2 Connect DB (53%) | Mainframe Project Manager 14 Caen / Analyste Développeur COBOL / Cobol Developer / Développeur(se) MicroStrategy / Mainframe software engineer |
| 74 | 58 | 0.423 | manager (90%) | cyber security IT security information s (100%) | Engineering Delivery Manager / Project Manage / Export project manager - Naval communications / Engineering Delivery Manager / Systems Engineering Activities Manager / Manager of France/Export Customer Support Pro |
| 97 | 69 | 0.423 | consultant (94%) | communicate with customers talk with cus (20%) | Consultant INFOLOG / Consultant / Consultant(e) Talend / Consultant IT M&A / Consultant ITSM |
| 47 | 42 | 0.424 | audit (36%) | develop audit plan Define all organisati (57%) | Auditeur IT Interne Expérimenté / Auditeur interne IT secteur Asset Management  / IT auditor / Consultant junior SI Audit IT / Accessibility Auditor |
| 40 | 307 | 0.436 | java (51%) | feed concrete mixer supply concrete mixe (90%) | Alternation - Communication and event in char / Development Engineer Internship - fiber conte / Développeur(se) Java - Services Financiers / Architecte - JAVA - Energy & Utilities / Developer (Euse) - Java Fullstack - Energie & |

Reading notes

- A cluster far below the cutoff has titles that have little in common: it is held together by something else (a skill, company text, a template).
- A high top-skill share next to a weak lift is the single-skill pattern seen in D v1; a high top-token share next to a good lift is an ordinary occupation cluster.
- The lift compares clusters of different input spaces on the same scale (the title embedding); it does not say that one input finds more emerging occupations.
