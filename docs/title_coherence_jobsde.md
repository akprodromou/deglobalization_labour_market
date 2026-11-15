# Title coherence of the clusters: jobsde

12,243 postings. Coherence = length of the mean of the centred, unit title embeddings of a cluster (1 = identical titles, 0 = unrelated); lift = coherence minus that of random sets of the same size; top-token share = share of the cluster's titles holding its most frequent title word. The weak cutoff is the 10th percentile of the lift of the clusters of A (0.424), the same bar for every input. Input A is built from the title embedding alone, so it has an advantage on coherence by construction; read the top-token share next to it.

| input | clusters | noise | lift Q1 / median / Q3 | lift, median per posting | top-token share, median | clusters below the weak cutoff | postings in them (of clustered) |
|---|---|---|---|---|---|---|---|
| A | 71 | 27.6% | 0.455 / 0.507 / 0.578 | 0.478 | 60% | 7 (10%) | 500 (6%) |
| Dv2 | 106 | 24.5% | 0.205 / 0.299 / 0.421 | 0.331 | 27% | 80 (75%) | 7,057 (76%) |

Postings clustered in every input: 7,220 (59.0% of all).

## Weakest 12 clusters of A

| cluster | size | lift | top token (share) | top ESCO skill (share) | sample titles |
|---|---|---|---|---|---|
| 64 | 67 | 0.389 | fitter (28%) | develop pension schemes develop pension  (15%) | Construction mechanic /welder / Company fitter [ ] / Construction mechanic / steel construction fi / Traffic safety fitter / Carpenter /) |
| 47 | 50 | 0.391 | head (62%) | assertiveness self-assured confidence as (14%) | Head of department: In Central technical serv / Head of Customer Service / Team management in the support center (GN) / Team leader network usage management / Head of Technical Customer Support |
| 15 | 94 | 0.392 | kitchen (21%) | coordinate catering coordinating caterin (13%) | Küchenchef / Housekeeper / Employee housekeeping (floor) / Spülhilfe - ID: 10256 / Training as a cook |
| 48 | 62 | 0.394 | quality (61%) | provide user documentation Develop and o (15%) | Quality representative in healthcare / Head of Research and Development / Head of Strategy Development Bomag Group / Commissioner for management systems / Team leader project management online |
| 19 | 119 | 0.405 | production (63%) | meet commitments meet commitment show co (11%) | Workshop Manager / Production employee / Skilled worker assembly Audi Ingolstadt / Employee for print preparation / Production employee |
| 37 | 62 | 0.406 | personalreferent (34%) | manage human resources manage hr direct  (26%) | Personalreferent / Recruiter / Talent Acquisi / Personalmanagement-Spezialist in Teilzeit (20 / Werde Freelance Recruiter bei kariera.group!  / Fachreferent/-in Recherche und wissenschaftli / Junior-Referent/-in |
| 32 | 46 | 0.408 | koch (37%) | food hygiene rules food hygiene laws rul (11%) | Koch À-la-carte-Küche (Teilzeit/ 25h) / Küchenmeisterin/ Küchenmeister / Jungkoch / Koch / Chef de partie / Koch / Beikoch / Jungkoch / Küchenhilfe am Standort Rissen |
| 27 | 876 | 0.424 | für (26%) | manage maintenance operations manage ope (15%) | Kfz.-Mechatroniker / Gartenbauhelfer/in / Stanzmaschinenfachkraft / -einrichter für ind / Bauleiter [ ] für den Gleisbau / E/E-Systems-Designer für intelligente Fahrzeu |
| 55 | 65 | 0.426 | software (37%) | Agile development The agile development  (12%) | SPS-Programmierer / SPS Entwickler / Software developer for web and cloud technolo / Software developer Focus on Java / (Senior) DevOps Engineer |
| 54 | 87 | 0.432 | commercial (70%) | accounting bookkeeping The documentation (16%) | Clerk Air Freight Export Gateway / Commercial employee in customer service / ord / Commercial employee facility management / Commercial employee / Processing for tree management and procuremen |
| 58 | 455 | 0.435 | clerk (58%) | accounting bookkeeping The documentation (26%) | Accounting Specialist IFRS / HGB / Budget Planning and Controlling Consultant /d / Financial/payroll age / Purchasing clerk / 1 clerk in the public order office |
| 56 | 202 | 0.436 | administrator (21%) | administer ICT system operate system adm (9%) | IT system administrator Focus on infrastructu / Training as an IT specialist for system integ / Senior IT-Systemadministrator* / Data Governance Spezialist / IT-Administrator |

## Weakest 12 clusters of Dv2

| cluster | size | lift | top token (share) | top ESCO skill (share) | sample titles |
|---|---|---|---|---|---|
| 21 | 45 | 0.096 | specialist (11%) | improve business processes manage proces (100%) | Business Partner Controlling / Systemadministrator / CNC production mechanic / HR specialist - payroll accounting / SAP Inhouse Consultant* |
| 24 | 137 | 0.140 | sales (19%) | sales activities sales activity sales ex (100%) | Uhrmacher / Watchmaker / Warehouse logistics specialist / Mitarbeiter Verkauf Frischfisch / Service employee |
| 49 | 43 | 0.144 | manager (19%) | mechanical engineering maintain mechanis (100%) | Production Manager / Steuerungstechniker/-in für Automatisierungsl / Solution Architect Teamcenter / Betriebsstellenleiter / Verfahrensentwickler |
| 13 | 53 | 0.144 | customer (26%) | satisfy customers ensure satisfied custo (100%) | Head of a health service / Mitarbeiter IT-Serviceprozesse / Customer advisor for Netflix in Greece - Incl / Customer service specialist* for the Munich T / Warehouse assistant Night Star Express |
| 33 | 48 | 0.148 | for (29%) | relate empathetically empathise with oth (100%) | Call center agent in receivables management / Kaufmann für Versicherungen für unsere laufen / Health and nursing staff for night duty / Sozialpädagoge / Pädagoge für Coachingprojekt / Pflegefachkraft / ATA Anästhesie - Wunschdien |
| 20 | 70 | 0.152 | customer (21%) | contact customers contacting customers g (100%) | Sachbearbeiter Aftermarket Industriekaufmann/ / Data Integration Manager / Data Analyst / Specialist warehouse clerk - spare parts busi / Customer Service Employee / Customer service / customer advisor career ch |
| 16 | 55 | 0.153 | für (20%) | numerology study of mystical relation be (60%) | Kaufm. Netzservice / Specialist service for the environmental serv / KAUFMÄNNISCHEN ANGESTELLTE IN DER FONDSADMINI / Bauprojektleiter Technische Gebäudeausrüstung / Employee*in Finance |
| 17 | 112 | 0.154 | clerk (19%) | issue sales invoices issue a sales invoi (100%) | Bauleiter/Projektleiter im Hochbau gesucht -  / Billing clerk / Eventmanager / Sachbearbeiter Im-/Export / Accounts payable accountant |
| 36 | 59 | 0.155 | for (17%) | support employability of people with dis (100%) | Sozialarbeit / Sozialpädagogik für den Sozial / Erzieher / Heilpädagoge / Koch large kitchen - inclusion operation / Leitung der Hauswirtschaft - gerne auch als K / Leitung der Abteilung Forschung und Transfer |
| 59 | 57 | 0.169 | manager (16%) | adhere to OHSAS 18001 adhere to OHSAS 18 (86%) | Security specialist / Expert for occupational safety, hazardous sub / Bauleiter [ ] für den Gleisbau / Mitarbeiter*in unseres Bauverwaltungs- und Li / Team Leader Technik / Schwerpunkt Werkstatt |
| 12 | 80 | 0.171 | security (11%) | cyber security IT security information s (34%) | Ausbildung zum Fachinformatiker für Systemint / IT-Admin / LKW-Mechatroniker / Absolvent:in Informatik / Cyber Security / Head of security |
| 15 | 117 | 0.171 | management (20%) | facilities management in the organisatio (100%) | Hausmeister (m,w,d) / Deputy nursing management / Standortmanager*in / Pflegehelfer / Merchant office management as a clerk for ins |

Reading notes

- A cluster far below the cutoff has titles that have little in common: it is held together by something else (a skill, company text, a template).
- A high top-skill share next to a weak lift is the single-skill pattern seen in D v1; a high top-token share next to a good lift is an ordinary occupation cluster.
- The lift compares clusters of different input spaces on the same scale (the title embedding); it does not say that one input finds more emerging occupations.
