# Title coherence of the clusters: jobbland

53,959 postings. Coherence = length of the mean of the centred, unit title embeddings of a cluster (1 = identical titles, 0 = unrelated); lift = coherence minus that of random sets of the same size; top-token share = share of the cluster's titles holding its most frequent title word. The weak cutoff is the 10th percentile of the lift of the clusters of A (0.470), the same bar for every input. Input A is built from the title embedding alone, so it has an advantage on coherence by construction; read the top-token share next to it.

| input | clusters | noise | lift Q1 / median / Q3 | lift, median per posting | top-token share, median | clusters below the weak cutoff | postings in them (of clustered) |
|---|---|---|---|---|---|---|---|
| A | 357 | 34.3% | 0.508 / 0.563 / 0.636 | 0.549 | 82% | 36 (10%) | 4,524 (13%) |
| Dv2 | 265 | 19.3% | 0.202 / 0.293 / 0.430 | 0.257 | 35% | 212 (80%) | 38,849 (89%) |

Postings clustered in every input: 29,239 (54.2% of all).

## Weakest 12 clusters of A

| cluster | size | lift | top token (share) | top ESCO skill (share) | sample titles |
|---|---|---|---|---|---|
| 276 | 179 | 0.371 | the (43%) | recruit personnel personnel recruiting p (47%) | International case officer - The Public Prose / Acting deputy head of the Chamber of Financia / HR expert in the investigation of abusive dis / Work as Analyst, Ministry of Social Affairs - / Correctional Officer at the Hall Prison |
| 328 | 40 | 0.375 | consultant (38%) | innovation processes The techniques, mod (35%) | VA engineer / Graduated VA Advisor - Overwater and Wiring F / Experienced energy consultant production heat / Energy specialist - All offices / Electricity & control consultant in hydropowe |
| 221 | 41 | 0.383 | interim (66%) | follow up orders for customers follow up (37%) | Operations Manager (COO) / Interim CTO - Ingrid Capacity / Interim group manager for an insurance compan / Interim unit manager within care and housing / Operations controller for the HR Section |
| 302 | 302 | 0.386 | marketing (34%) | communication conversation interaction c (24%) | Influencer & Social media manager (temporary  / Summer Internship / Content Producer / Social Media Intern / Digital Producers Marknad |
| 288 | 109 | 0.397 | for (46%) | Swedish competent in Swedish ability to  (24%) | Excavator Mark & ​​Construction (Stockholm ar / Aviation technician for Europe's largest test / field technicians for Trollhättan and surroun / Electrician - Barona / Field Service Specialist for the Malm fields |
| 261 | 194 | 0.398 | administrator (22%) | recruit personnel personnel recruiting p (42%) | HR specialists for the South-West and North-E / HR Specialist - Learning & Development / Head of HR / HR and Administrative Assistant - Internation / Administrator/HR Assistant |
| 263 | 81 | 0.404 | manager (68%) | Swedish competent in Swedish ability to  (30%) | Risk and Information Protection Manager / System manager IT / Management system manager / Compliance Coordinator / System manager for IT care systems |
| 128 | 99 | 0.407 | receptionist (47%) | arrange bookings take bookings arranging (26%) | Night receptionist for hotel / Gym owner Täby Center (extra/if needed) / Service - Extra if needed - Lundsbrunn Resort / Extra cook if needed Malmö area / Receptionist for Central Stockholm - Andara P |
| 108 | 75 | 0.409 | treatment (51%) | meet commitments meet commitment show co (47%) | Treatment educator for dropout activities in  / Treatment assistant at youth home Gudhemsgård / Treatment Pedagogue/ Social Pedagogue / quality manager who wants to make a differenc / Treatment pedagogue - The Norwegian Instituti |
| 284 | 348 | 0.424 | customer (45%) | Swedish competent in Swedish ability to  (28%) | Finnish Customer Advisor / Join Our Finnish Content Moderator Team in Vi / Work with customer service in sunny Cyprus / Du möchtest in den Niederlanden arbeiten Wir  / Finnish-speaking marketing consultant |
| 94 | 130 | 0.428 | seasonal (62%) | cooperate with colleagues work together  (38%) | Snow removal in Halmstad and surroundings / Logistics employee - Bauhaus & Co KB / Work extra with snow shoveling this winter / Seasonal worker High Chaparral - Warehouse wo / Seasonal worker High Chaparral - Locomotive d |
| 59 | 60 | 0.428 | student (93%) | communication conversation interaction c (20%) | Student Assistant, Supply Chain Planning / Medical & Scientific Affairs Student Assistan / Customer Support Agent to Qlik ( /Student) / Student Assistant / Sales Support & Analyst (Student service) - L |

## Weakest 12 clusters of Dv2

| cluster | size | lift | top token (share) | top ESCO skill (share) | sample titles |
|---|---|---|---|---|---|
| 28 | 75 | 0.032 | for (13%) | work with e-services available to citize (93%) | Work environment guidance officer - Swedish W / Nurses for 1177 healthcare advice Uppsala / Store employee ICA Baronen / Technical Expert Active Directory - Vattenfal / Sports teacher grades 3-9 |
| 155 | 52 | 0.052 | for (21%) | adapt existing designs to changed circum (65%) | nurses for night service / nurses for night service / Warehouse Administrator / Dentist / Expert in shipping, environment and dangerous |
| 69 | 175 | 0.065 | for (16%) | give interviews to media do interviews p (100%) | Content Creator & business reporter with driv / Holiday temps / Post builder / Truckförare / Truck/test driver |
| 108 | 73 | 0.070 | for (12%) | assessment processes assessments process (100%) | General Specialist / Assistant service technicians / Geriatric Care Lönsboda / Summer Trainee, Data Platforms / Studentjobb som Vågadministratör / Administra |
| 19 | 53 | 0.070 | quality (19%) | perform quality audits Execute regular,  (100%) | Two preschool teachers / Kvalitetstekniker / Handläggare till Myndigheten för digital förv / Area Sales Manager - Power Quality Products / Edge benders - take the next step in your ind |
| 36 | 40 | 0.084 | engineer (12%) | mobility as a service MaaS sustainable m (100%) | Graduate and Junior Strategy Analysts / Backend developer for global cloud service / Trafikplanerare, strategisk samhällsplanering / Felsökare / Bicycle mechanic for a good team |
| 138 | 66 | 0.098 | manager (23%) | apply change management alter management (79%) | HR Business partner / Regional manager for Region South - Modern / Socialsekreterare till barn och ungdomsenhete / Business developer for transition to new soci / RAN Network Engineer - Telia |
| 207 | 151 | 0.099 | project (19%) | carry out project activities execute pro (100%) | App developer for Digital Identity Wallet - T / Local supply strategist / Purchaser / Business developer, Product introductions, Ch / editorial assistant - Egmont |
| 121 | 61 | 0.103 | for (30%) | process data handle data convert data da (80%) | Nurse / Nurse for Infection Department 3 / Support teacher for functional support / Medical secretary / Weight Trainer coach |
| 175 | 298 | 0.105 | manager (16%) | hardware components suppliers The suppli (97%) | Senior mechanical designer in special machine / Truck driver C and CE Örebro, Summer substitu / support IT technician, Onsite - Danda / Adas Validation Engineer / Driver / Car transporter |
| 104 | 456 | 0.110 | for (10%) | consult with business clients consulting (98%) | Senior Full Stack Developer / Validation Engineer-Validation Manager Life S / Technical Project Manager / Mechanical designer / Construction manager / contract coordinator w |
| 39 | 63 | 0.112 | developer (11%) | innovate in ICT Create and describe new  (100%) | Installatör Kamerabevakning / Rådgivende ingeniør, prosjektleder eller bygg / Systemadministratör Linux / Simulation-based Optimization of Existing Fac / Aviation technician, Skaraborg's air fleet |

Reading notes

- A cluster far below the cutoff has titles that have little in common: it is held together by something else (a skill, company text, a template).
- A high top-skill share next to a weak lift is the single-skill pattern seen in D v1; a high top-token share next to a good lift is an ordinary occupation cluster.
- The lift compares clusters of different input spaces on the same scale (the title embedding); it does not say that one input finds more emerging occupations.
