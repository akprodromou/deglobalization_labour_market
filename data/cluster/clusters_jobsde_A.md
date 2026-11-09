# Clusters: jobsde, input A

12,243 postings; 79 clusters; noise 32.2%; relative validity 0.198; min_cluster_size 40.

- Stability seed 1 vs seed 2: ARI 0.799 on the 62.9% of postings clustered in both; 70 clusters.
- Stability seed 1 vs seed 3: ARI 0.916 on the 63.1% of postings clustered in both; 73 clusters.
- k-means with k=79 on the same UMAP space: AMI 0.914, ARI 0.742 against HDBSCAN (non-noise postings).

## Named emerging occupations (regex on the cleaned title; found or not, never forced)

| occupation | titles matched | in a cluster | top clusters (matches / cluster size) |
|---|---|---|---|
| trade compliance officer | 0 | 0 | - |
| export control specialist | 1 | 1 | C29 (1/585) |
| supply chain resilience analyst | 0 | 0 | - |
| semiconductor process engineer | 2 | 1 | C78 (1/210) |
| battery cell technician | 0 | 0 | - |
| critical materials specialist | 0 | 0 | - |
| reshoring program manager | 0 | 0 | - |

## Largest 60 clusters plus every cluster hit by a named occupation

### C29: 585 postings (4.78%) [named: export control specialist]
- Titles: Spezialist Accounting IFRS / HGB | IT-Sachbearbeitung | Kaufmännische(r) Mitarbeiter(in) / Sachbearbeiter | Assistent/in für den Kaufmännischen Leiter | Verwaltungskraft für die Bewohnerverwaltung | Kaufmännischer Mitarbeiter - Büromanagement/Empfang
- ESCO skills: accounting bookkeeping The documentation (18%); financial statements statements on finan (13%); use microsoft office have proficiency in (11%); issue sales invoices issue a sales invoi (9%); assume responsibility demonstrate a cons (8%); develop pension schemes develop pension  (7%)
- Lightcast terms: Supply Chain (3); Supply Chain Management (2); Production Planning (1); Demand Forecasting (1)

### C62: 316 postings (2.58%)
- Titles: Clerk applications | Office management clerk | Application review clerk | Clerk maintenance department | Clerk / Clerk | Clerk for planning and consulting of the hospital and medical technology facilit
- ESCO skills: accounting bookkeeping The documentation (15%); financial statements statements on finan (9%); develop pension schemes develop pension  (8%); use microsoft office have proficiency in (7%); meet commitments meet commitment show co (7%); assume responsibility demonstrate a cons (7%)
- Lightcast terms: Supply Chain (1); Supply Chain Management (1); Materials Management (1)

### C76: 251 postings (2.05%)
- Titles: Engineer as a pipeline planner in plant construction | Construction manager maintenance | Surveyor / planner pipeline construction | Construction manager maintenance Augsburg region | Calculator for civil engineering | Project Manager Electrical Engineering
- ESCO skills: develop pension schemes develop pension  (16%); civil engineering civil engineering appl (16%); manage maintenance operations manage ope (13%); perform project management perform manag (12%); assume responsibility demonstrate a cons (11%); CAD software CADD software computer assi (10%)
- Lightcast terms: Supply Chain (2); Materials Management (1); Supply Chain Management (1); Demand Planning (1)

### C48: 248 postings (2.03%)
- Titles: Warehouse logistics specialist on day shift | Warehouse clerk / warehouse logistics specialist | Warehouse logistics | Packaging employee | Warehouse clerk auxiliary materials warehouse | Warehouse employee in the Bruchsal parcel center
- ESCO skills: receive goods secure goods accept goods  (14%); manage transport of goods from warehouse (12%); unload supplies remove delivered product (11%); meet commitments meet commitment show co (8%); develop pension schemes develop pension  (8%); check shipments carry out consignment in (7%)
- Lightcast terms: Supply Chain (3); Materials Management (2); Production Planning (1); Demand Management (1)

### C77: 234 postings (1.91%)
- Titles: Electronics technician in system integration | Electronics technician / electrician | Electrician as DGUV V3 inspector | Electrician / electronics technician maintenance | Electrician | Electronics technician (mf/d) / specialist in electrical engineering
- ESCO skills: manage maintenance operations manage ope (35%); mechatronics mechatronic engineering mec (20%); develop pension schemes develop pension  (16%); work with e-services available to citize (11%); meet commitments meet commitment show co (9%); provide user documentation Develop and o (9%)
- Lightcast terms: Material Flow Management (1); Supply Chain (1)

### C10: 229 postings (1.87%)
- Titles: Customer service representative in office/part-time | Clerk/assistant in the secretariat full-time | Salesperson full-time and part-time | Service employee retail full time / part time | First/second level support staff in the photovoltaics sector full-time | Human resources clerk full-time/part-time
- ESCO skills: keep an open mind take on new ideas and  (15%); intensive care medicine medical intensiv (10%); supervise nursing staff supervise the nu (10%); specialist nursing care specialist analy (9%); meet commitments meet commitment show co (9%); provide user documentation Develop and o (7%)

### C78: 210 postings (1.72%) [named: semiconductor process engineer]
- Titles: Electrical engineer / electrical engineer specializing in electrical engineering | Mechatronics engineer compressed air/refrigeration - Böhlen | Mechatronics engineer / industrial electrician | Maintenance coordinator electrical engineering / mechatronics | Electronics engineer / mechatronics engineer | Automotive mechatronics engineer in Blankenheim
- ESCO skills: mechatronics mechatronic engineering mec (41%); manage maintenance operations manage ope (24%); develop pension schemes develop pension  (10%); pneumatics pneumatics applications The a (9%); drive agricultural machines agricultural (9%); build business relationships devise busi (9%)
- Lightcast terms: Vertical Integration (2)

### C58: 202 postings (1.65%)
- Titles: IT-Application-Manager | IT-Management-Assistent*in | IT-Administrative*r Spezialist*in | Office IT Specialist | IT specialist specializing in system integration, salary group 9b TVöD | Head of Service/Assembly/Installation - Security Solutions
- ESCO skills: German ability to comprehend spoken and  (10%); provide user documentation Develop and o (9%); administer ICT system operate system adm (9%); develop pension schemes develop pension  (9%); manage maintenance operations manage ope (9%); operating systems The features, restrict (8%)
- Lightcast terms: SAP Ariba (1)

### C19: 201 postings (1.64%)
- Titles: Nursing specialist as a wound expert | Health and nursing staff / geriatric nurse / MFA for the rehabilitation clinic | Nursing specialist | Geriatric psychiatry nurse | Geriatric nurse geriatric medicine | Certified nursing specialist
- ESCO skills: specialist nursing care specialist analy (30%); innovation in nursing innovation in the  (19%); supervise nursing staff supervise the nu (15%); professional documentation in health car (14%); follow safety precautions in printing ad (11%); develop pension schemes develop pension  (11%)
- Lightcast terms: Supply Management (1)

### C13: 200 postings (1.63%)
- Titles: State-recognized educator or qualified social worker | Professional recognition year (social worker or educator ) | Educator in Weilerswist-Lommersum | Social educators educators in the ION | Pedagogical employee/social worker in young care | Social worker, educator Buchholz, Tostedt, Winsen
- ESCO skills: assume responsibility demonstrate a cons (9%); meet commitments meet commitment show co (8%); supervision of persons guidance of perso (8%); coach individuals in specialised nursing (8%); recreation activities activities for rec (8%); develop creative ideas developing creati (6%)

### C69: 190 postings (1.55%)
- Titles: Mechatroniker / Elektroniker /i) | Betriebselektriker / Elektroniker | Mechatroniker oder Elektroniker | Elektriker Techniker in Berlin-Mariendorf | Mechatroniker für Produktionstechnik | Elektriker oder Elektroinstallateur
- ESCO skills: manage maintenance operations manage ope (23%); mechatronics mechatronic engineering mec (21%); develop pension schemes develop pension  (13%); pneumatics pneumatics applications The a (8%); meet commitments meet commitment show co (6%); sell bicycles put bikes up for sale sell (5%)
- Lightcast terms: Materials Management (1)

### C23: 188 postings (1.54%)
- Titles: Verkäufer Werkzeuge und Eisenwaren - auch Quereinsteiger | Verkäufer/Kassierer Fleischabteilung | Fleischer / Metzger im Verkauf | Verkäufer/Kassierer Getränkemarkt | Verkäuferin Bedientheke | Verkäufer/Kassierer Backshop
- ESCO skills: deal with public communicate with the pu (14%); German ability to comprehend spoken and  (13%); manufacturing of confectionery confectio (13%); show initiative take the initiative give (13%); handle returns handling a return deal wi (13%); process incoming construction supplies r (12%)
- Lightcast terms: Materials Management (1)

### C39: 184 postings (1.50%)
- Titles: Sales manager | Sales Manager / Area Sales Manager for Switzerland | Senior Sales Manager | Social Media Manager | Senior Customer Success Manager SaaS / B2B | Sales Manager / Sales Manager
- ESCO skills: sales activities sales activity sales ex (21%); prospect new customers prospecting a new (17%); communication conversation interaction c (15%); make investment decisions decide on inve (10%); develop creative ideas developing creati (9%); respond to customers' inquiries deal wit (9%)
- Lightcast terms: Supply Chain (6); Supply Chain Management (2); Demand Planning (1); Electronics Manufacturing (1); Production Planning (1)

### C35: 180 postings (1.47%)
- Titles: Logistikmitarbeiter | Fachlagerist | Logistik-Koordinator | Logistik-Analyst | Fachlagerist Lager | Lagermitarbeiter
- ESCO skills: receive goods secure goods accept goods  (11%); unload supplies remove delivered product (8%); meet commitments meet commitment show co (7%); logistics logistic coordination transpor (7%); develop pension schemes develop pension  (7%); use microsoft office have proficiency in (7%)
- Lightcast terms: Supply Chain (5); Production Planning (2); Capacity Planning (1); Supply Chain Management (1); Supply Management (1)

### C65: 137 postings (1.12%)
- Titles: Sales representative | Sales representative IT projects for legal software solutions | Consultant corporate strategy | Sales representative in the field of laboratory medicine | Consultant in building materials sales | Sales specialist for building products
- ESCO skills: sales activities sales activity sales ex (14%); communication conversation interaction c (10%); meet commitments meet commitment show co (10%); operate cash register run a cash point o (10%); sell products selling products sell a pr (9%); develop pension schemes develop pension  (9%)
- Lightcast terms: Cold Chain (1); Cold Store (1); Demand Management (1)

### C73: 132 postings (1.08%)
- Titles: CNC specialist | Machining mechanic - milling technology | Tool mechanic | Cutting mechanic with and without shift | Mechanic hose line inspection | CNC machining mechanic turning or milling machines
- ESCO skills: manage maintenance operations manage ope (31%); develop pension schemes develop pension  (23%); milling machines powdering machines mill (14%); tend CNC milling machine monitor CNC mil (11%); work with e-services available to citize (11%); assume responsibility demonstrate a cons (11%)
- Lightcast terms: Production Planning (4)

### C47: 130 postings (1.06%)
- Titles: Truck driver - shunter | Truck driver / professional driver | Professional driver / truck loading crane driver in local transport | Local transport driver and shunting driver in Potsdam | Professional driver / truck driver early or late shift! | Truck driver in local transport
- ESCO skills: logistics logistic coordination transpor (11%); develop pension schemes develop pension  (9%); meet commitments meet commitment show co (8%); assume responsibility demonstrate a cons (8%); maintain personal hygiene standards main (6%); maintain relationship with customers sus (5%)

### C49: 126 postings (1.03%)
- Titles: Assistant to the management | Administration employees for our shipping area | Assistant to the house manager | Employee in human resources administration | GTB Administration Officer | Office assistant in the Regulatory Affairs department
- ESCO skills: manage human resources manage hr direct  (17%); use microsoft office have proficiency in (12%); attend meetings turn up at gatherings ta (10%); communication conversation interaction c (9%); human resource management human resource (9%); cooperate with colleagues work together  (7%)
- Lightcast terms: Cold Chain (1)

### C20: 121 postings (0.99%)
- Titles: Versicherungskaufmann / Versicherungsmakler gesucht | Finanzberater / Versicherungskaufmann | Kaufmann für Versicherungen für unsere laufenden Neukundenzugänge Region Stuttga | Bankkaufmann gesucht für die Region Ellwangen und Umgebung | Duales Studium Bachelor of Laws plus Ausbildung zum Kaufmann für Büromanagement | Kauffrau/-mann für Versicherungen und Finanzen
- ESCO skills: sales activities sales activity sales ex (21%); prospect new customers prospecting a new (19%); banking activities banking activity The  (18%); advise on investment provide investment  (10%); accounting bookkeeping The documentation (7%); teach further education teaches further  (7%)

### C52: 119 postings (0.97%)
- Titles: Palliative Care Fachkraft | Pflegefachkraft für die vollstationäre Pflege | Pflegefachkräfte | Pflegefachkraft Kardiologie | Pflegekräfte | Pflegefachkraft
- ESCO skills: specialist nursing care specialist analy (15%); professional documentation in health car (9%); assume responsibility demonstrate a cons (9%); geriatrics preventative methods in healt (9%); teach further education teaches further  (8%); supervise nursing staff supervise the nu (7%)

### C60: 118 postings (0.96%)
- Titles: Salesperson part-time - also career changers | E-scooter mechanic also career changer | Customer service / customer advisor career changers welcome! | Salesperson beverage market - also career changers | Employee customer service / career changer | Call center agent / career changer in customer service
- ESCO skills: develop pension schemes develop pension  (13%); deal with public communicate with the pu (11%); bake goods bake a good bake bake product (10%); receive goods secure goods accept goods  (9%); meet commitments meet commitment show co (8%); sell products selling products sell a pr (8%)

### C50: 117 postings (0.96%)
- Titles: Complaint processing employee | Employee customer service | Unsolicited application | Canteen service worker | SERVICE EMPLOYEE | Employee for our media customer center
- ESCO skills: meet commitments meet commitment show co (9%); sales activities sales activity sales ex (9%); communication conversation interaction c (6%); draft procurement technical specificatio (6%); advise customers on new equipment inform (6%); recruit personnel personnel recruiting p (5%)
- Lightcast terms: Demand Planning (1); Supply Chain (1)

### C67: 117 postings (0.96%)
- Titles: Kfz.-Mechatroniker | Kfz-Mechatroniker | Kfz-Mechaniker | KFZ-Mechatroniker / Mechaniker / Helfer | LKW-Mechatroniker | Fahrzeugpfleger in Münster
- ESCO skills: manage maintenance operations manage ope (14%); cooperate with colleagues work together  (7%); mechatronics mechatronic engineering mec (7%); assume responsibility demonstrate a cons (6%); assemble mechatronic units mechatronic u (5%); agricultural equipment agricultural appa (5%)

### C24: 114 postings (0.93%)
- Titles: Glasreiniger | Hygienefachkraft | Hauswart | Busreiniger | Housekeeping / Raumpfleger | Mitarbeiter mit hauswirtschaftlicher Erfahrung
- ESCO skills: facilities management in the organisatio (15%); clean building floors cleaning building  (11%); human-computer interaction HCI The study (9%); maintain personal hygiene standards main (9%); develop pension schemes develop pension  (9%); manage maintenance operations manage ope (9%)
- Lightcast terms: Cold Store (1); Production Planning (1); Demand Management (1)

### C63: 112 postings (0.91%)
- Titles: Employee in financial accounting | Employee as a junior employee in accounting | Financial accountant for the housing industry | Employee Financial Accounting Accounts Payable | Financial accountant | Financial or accounting accountant
- ESCO skills: accounting bookkeeping The documentation (50%); financial statements statements on finan (36%); accounting techniques accounting perform (14%); develop pension schemes develop pension  (13%); issue sales invoices issue a sales invoi (12%); follow up accounts receivables monitor a (12%)
- Lightcast terms: Materials Management (1)

### C22: 109 postings (0.89%)
- Titles: Production employee in the food industry | Laundry assistant / production employee | Production employee aviation | Employee for production | Team member production | Production employee at the Landsberg plant
- ESCO skills: meet commitments meet commitment show co (13%); control production direct production con (11%); production processes production process  (9%); assume responsibility demonstrate a cons (8%); recruit personnel personnel recruiting p (7%); optimise production maximise production  (7%)
- Lightcast terms: Production Planning (10); Capacity Planning (3); Electronics Manufacturing (1); Planning Software (1); Supply Chain (1)

### C46: 108 postings (0.88%)
- Titles: Deputy ward manager for our urological ward | Deputy ward manager for ophthalmology | Deputy ward manager oncology/palliative | Deputy branch manager | Deputy Nursing service manager | Deputy laboratory manager
- ESCO skills: assume responsibility demonstrate a cons (14%); sell products selling products sell a pr (9%); motivate others inspire others stimulate (9%); facilities management in the organisatio (9%); motivate employees encourage employees m (8%); sales activities sales activity sales ex (8%)

### C38: 103 postings (0.84%)
- Titles: SALONLEITUNG LÜNEBURG | Filialleitung / Studioleitung | Marktleitung | Marktleiter / Filialleiter | Fachbereichsleitung | Abteilungsleiter in Nordhorn oder Meppen
- ESCO skills: sales activities sales activity sales ex (16%); motivate employees encourage employees m (15%); communication conversation interaction c (14%); assertiveness self-assured confidence as (14%); assume responsibility demonstrate a cons (14%); sell products selling products sell a pr (13%)
- Lightcast terms: Capacity Planning (1); Production Planning (1); Materials Management (1); Supply Chain (1); Supply Chain Management (1)

### C7: 101 postings (0.82%)
- Titles: Parcel delivery person | Full-time parcel delivery person | Parcel delivery person (Weidendamm) | Parcel delivery person from parcel center | Parcel delivery person , HH-Allermöhe | Parcel delivery person in Brühl
- ESCO skills: sell bicycles put bikes up for sale sell (80%); handle delivered packages distribute del (15%); deliver correspondence deliver the corre (13%); German ability to comprehend spoken and  (6%); communication conversation interaction c (3%); work with a dance team work with dance t (2%)

### C54: 100 postings (0.82%)
- Titles: Customer advisor services/service | Customer advisor ADAC credit card | Telephone customer advisor inbound | Customer advisor customer service | Customer advisor for building materials | Customer advisor service and sales outbound
- ESCO skills: German ability to comprehend spoken and  (13%); satisfy customers ensure satisfied custo (13%); provide high quality customer service pu (11%); identify customer's needs identifying a  (10%); meet commitments meet commitment show co (8%); carry out active selling make active sel (7%)

### C33: 100 postings (0.82%)
- Titles: Chemikant / Produktionsfachkraft Chemie | Chemielaborant | Extrusionsanlagen-Operator | Ausbildung Maschinen- und Anlagenführer | Maschinenführer | Maschinen- und Anlagenführer Abfüllung
- ESCO skills: production processes production process  (13%); assume responsibility demonstrate a cons (6%); develop pension schemes develop pension  (6%); manage maintenance operations manage ope (6%); quality standards The national and inter (5%); packaging functions packaging operations (5%)
- Lightcast terms: Production Planning (1)

### C64: 93 postings (0.76%)
- Titles: Sales representative in the B2B field service | Technical sales in the field | Sales representative field service | Sales engineer TECHNICAL FIELD SERVICE | Pharmaceutical representative in the field | Field sales representative electrical
- ESCO skills: maintain relationship with customers sus (28%); prospect new customers prospecting a new (17%); sales activities sales activity sales ex (15%); show entrepreneurial spirit identify opp (15%); market analysis analysis of the market m (14%); meet commitments meet commitment show co (14%)
- Lightcast terms: Planning Software (1)

### C16: 90 postings (0.74%)
- Titles: Kitchen helper | Housekeeping helper or housekeeper | Housekeeper trainees at Haus Karlsruher Weg | Cook - permanent | Chef food production | Head chef
- ESCO skills: coordinate catering coordinating caterin (13%); respect the diversity of cultural values (12%); workplace sanitation workplace hygiene w (10%); recreation activities activities for rec (10%); respect data protection principles follo (9%); supervise housekeeping operations overse (8%)

### C71: 88 postings (0.72%)
- Titles: Machine and plant operator | Plant operator | Machine operator / plant operator full-time | Machine and plant operator project production | Plant operators also career changers | Machine and plant operator for lamination
- ESCO skills: production processes production process  (16%); meet commitments meet commitment show co (7%); manage maintenance operations manage ope (7%); German ability to comprehend spoken and  (7%); tend packaging machines mind packaging m (6%); packaging functions packaging operations (6%)
- Lightcast terms: Shipping Systems (1)

### C5: 85 postings (0.69%)
- Titles: Postman for parcels and letters | Postman for parcels | Postman for parcels and letters in Beckum | Postman for parcels and letters in Kamen | Postman for parcels and letters - Nierstein | Postman for parcels and letters , Neugraben
- ESCO skills: sell bicycles put bikes up for sale sell (100%); deliver correspondence deliver the corre (34%); handle delivered packages distribute del (7%); negotiate employment agreements negotiat (1%)

### C57: 85 postings (0.69%)
- Titles: Trained or semi-trained: WKS insulator in the area of ​​heating / plumbing at Sc | Anlagenmechaniker / Installateur für die Sanitär-, Heizungs- und Lüftungstechnik | Anlagenmechaniker SHK | Anlagenmechaniker für Sanitär-, Heizungs- und Klimatechnik | Servicemonteure für Lüftungs- und Klima-Technik / SHK für die Abteilung RLT | SHK-Anlagenmechaniker oder vergleichbare Ausbildung als Haustechniker Heizung, K
- ESCO skills: design ventilation network planning of v (14%); manage maintenance operations manage ope (11%); mechatronics mechatronic engineering mec (11%); sell bicycles put bikes up for sale sell (11%); district heating and cooling heat networ (9%); perform inspection analysis report on in (8%)

### C3: 81 postings (0.66%)
- Titles: weitere pädagogische Fachkraft für die Tageseinrichtung für Kinder Ravensburger  | weitere pädagogische Fachkraft für die Tageseinrichtung für Kinder Dr.-Herbert-C | Weitere pädagogische Fachkraft für die Tageseinrichtung für Kinder Jägerhalde 11 | Kinderpfleger*in für die Tageseinrichtung für Kinder Don-Carlos-Straße 20 in Stu | Sozialpädagogische Assistenz für die Tageseinrichtung für Kinder Holdermannstr.  | Weitere pädagogische Fachkraft für die Tageseinrichtung für Kinder Felix-Dahn-St
- ESCO skills: cooperate with colleagues work together  (99%); recruit personnel personnel recruiting p (99%); manage personal professional development (95%); coordinate communication within a team f (93%); develop pension schemes develop pension  (48%); supervision of persons guidance of perso (41%)

### C6: 80 postings (0.65%)
- Titles: Postman for parcels and letters - temporary help/retrieval | Postman for parcels and letters - temporary help / on-call worker | Temporary assistant / on-call worker as a postman for parcels and letters in Aug | Temporary assistant / on-call worker as a postman for parcels and letters in Mem | Temporary assistant / on-call worker as a parcel delivery person in Neusäß | Temporary assistant / on-call worker as a postman for parcels and letters in Don
- ESCO skills: deliver correspondence deliver the corre (45%); handle delivered packages distribute del (21%); sell bicycles put bikes up for sale sell (14%); German ability to comprehend spoken and  (1%)

### C44: 79 postings (0.65%)
- Titles: Physiotherapeut / Ergotherapeut / Logopäde | Physiotherapist full time / part time / mini job Bad Waldsee | Logopäde | Ergotherapeuten | Ergotherapeut* Ergotherapeutin Neuruppin | Ergotherapeutin / Ergotherapeutin
- ESCO skills: physiotherapy specialism in physiotherap (28%); develop pension schemes develop pension  (14%); attend meetings turn up at gatherings ta (11%); occupational science study of everyday a (11%); meet commitments meet commitment show co (11%); neurology medical conditions of the nerv (10%)

### C42: 78 postings (0.64%)
- Titles: Training / Occupational Therapist / Occupational Therapist | Occupational therapist | Physiotherapist / physiotherapist for our independent practice | Occupational therapist/in | Movement therapist | Rehabilitationsspezialist
- ESCO skills: physiotherapy specialism in physiotherap (28%); treat speech disorders provide speech th (15%); develop pension schemes develop pension  (10%); occupational science study of everyday a (10%); rehabilitation methods to regain patient (9%); geriatrics preventative methods in healt (8%)
- Lightcast terms: Supply Chain (1)

### C68: 78 postings (0.64%)
- Titles: Bauingenieur als Lead Engineer CSA | (Innen-)Architekt Neue Arbeitswelten | Bauingenieur / Architekt / Bauleiter / Projektleiter Hochbau | Bauingenieurin/Bauingenieur, Vertiefung Verkehrstechnik, für Planung und Bau | Mitarbeiter Konstruktion und Arbeitsplanung | Mitarbeiter [ ] für den Ingenieur- und Brückenbau
- ESCO skills: develop pension schemes develop pension  (19%); civil engineering civil engineering appl (17%); provide user documentation Develop and o (13%); German ability to comprehend spoken and  (10%); assertiveness self-assured confidence as (10%); manage maintenance operations manage ope (8%)
- Lightcast terms: Planning Software (1)

### C2: 76 postings (0.62%)
- Titles: Postman for parcels and letters | Postman for parcels and letters in Brilon | Postman for parcels | Postman for letters and parcels | Postman for parcels and letters in Eutin | Postman for letters and parcels in Roth
- ESCO skills: sell bicycles put bikes up for sale sell (99%); deliver correspondence deliver the corre (28%); handle delivered packages distribute del (7%)

### C56: 76 postings (0.62%)
- Titles: Erzieher / Heilerziehungspfleger / Sozialpädagogen | Erzieher / Heilpädagoge | Heilerziehungspfleger/in | Heilerziehungspfleger / Erzieher | Heilerziehungspfleger / Erzieher als Teamleitung | Erzieher / Heilerziehungspfleger
- ESCO skills: coach individuals in specialised nursing (11%); recreation activities activities for rec (9%); supervision of persons guidance of perso (9%); meet commitments meet commitment show co (8%); support employability of people with dis (7%); pedagogy methods of teaching paedagogy s (7%)

### C43: 75 postings (0.61%)
- Titles: Medizinische Fachangestellte/r | Arbeitsmediziner oder Arzt in Weiterbildung | Medizinische Fachangestellte ZNA | Medizinische Fachangestellte | Ausbildung medizinischer Fachangestellter | Medizinischer Fachangestellter Medizinisches Versorgungszentrum
- ESCO skills: urology diagnosis and treatment of urina (5%); cardiology disorders of the heart diseas (5%); meet commitments meet commitment show co (5%); assume responsibility demonstrate a cons (5%); collect biological samples from patients (5%); neurology medical conditions of the nerv (5%)

### C30: 73 postings (0.60%)
- Titles: Berufskraftfahrer | Schwertransportfahrer für den nationalen & internationalen Fernverkehr gesucht! | Kraftfahrer / Berufskraftfahrer im Fernverkehr | Berufskraftfahrer im Nahverkehr - hohe Spesen | LKW Fahrer im Nahverkehr in Neu Wulmstorf | Taxifahrer
- ESCO skills: logistics logistic coordination transpor (15%); assume responsibility demonstrate a cons (11%); develop pension schemes develop pension  (10%); maintain personal hygiene standards main (10%); warehousing regulations warehouse regula (10%); sustainable building materials sustainab (10%)
- Lightcast terms: Supply Chain (1)

### C26: 71 postings (0.58%)
- Titles: Teamassistenz | Serviceassistenz | Assistent | Teamassistent/in | Teamassistent | Sterilisationsassistenten
- ESCO skills: German ability to comprehend spoken and  (14%); meet commitments meet commitment show co (11%); communicate with customers talk with cus (11%); issue sales invoices issue a sales invoi (11%); use presentation software produce electr (11%); office software office soft-ware office  (10%)

### C74: 67 postings (0.55%)
- Titles: Service technician for frigates | Maintenance technician Maintenance (PAT) | Tiler for maintenance | Technical employee | Trainer for technical training | Technical quality inspector
- ESCO skills: manage maintenance operations manage ope (25%); mechatronics mechatronic engineering mec (15%); develop pension schemes develop pension  (10%); calibrate electronic instruments Correct (9%); consumer electronics home electronics el (7%); meet commitments meet commitment show co (7%)
- Lightcast terms: Materials Management (1)

### C14: 67 postings (0.55%)
- Titles: Pedagogical specialist | Specialists/pedagogical staff in group service | Pedagogical specialist for a new fully supervised facility | Pedagogical specialist / educator | Pedagogical specialist as group leader | Pedagogical specialist / nursing specialist
- ESCO skills: cooperate with colleagues work together  (16%); coach individuals in specialised nursing (12%); develop pension schemes develop pension  (12%); meet commitments meet commitment show co (10%); supervision of persons guidance of perso (9%); develop creative ideas developing creati (7%)

### C8: 67 postings (0.55%)
- Titles: Start your adventure: German-speaking job offers in Greece! - Career career chan | German customer advisor , start your career at Mercedes-Benz in Greece | Jobs in Greece! Including moving support! | Customer advisor for NETFLIX in Greece - Including moving package | Your adventure in Greece: 6 months of sun, culture and career | German-speaking customer advisor in Crete (including relocation & apartment)
- ESCO skills: German ability to comprehend spoken and  (28%); innovate in ICT Create and describe new  (18%); maintain relationship with customers sus (18%); communicate with customers talk with cus (13%); promote healthy lifestyle encourage heal (12%); table tennis ping-pong The theory, techn (10%)

### C61: 65 postings (0.53%)
- Titles: Internal Sales Employee | Employee in internal sales | Employee in internal sales insurance | Head of Internal Sales | Internal sales representative (gn) | Internal sales representative electrical engineering
- ESCO skills: communicate with customers talk with cus (15%); sales activities sales activity sales ex (12%); maintain relationship with customers sus (12%); prospect new customers prospecting a new (11%); use microsoft office have proficiency in (8%); recruit personnel personnel recruiting p (6%)
- Lightcast terms: Materials Management (1); Supply Chain (1)

### C41: 65 postings (0.53%)
- Titles: Kita-Assistenzleitung | Leitung - besondere Wohnformen | stellvertretende Niederlassungsleitung | Stellvertretende Pflegedienstleitung | Stellvertretende Abteilungsleitung für die Metallverarbeitung | Stellvertretende Leitung für die Metallverarbeitung
- ESCO skills: assertiveness self-assured confidence as (14%); facilities management in the organisatio (12%); manage troop deployment supervise troop  (12%); meet commitments meet commitment show co (9%); recruit employees hire new personnel man (9%); manage a team managing a team supervise  (8%)
- Lightcast terms: Materials Management (2)

### C12: 63 postings (0.51%)
- Titles: Nursing staff | Health and nursing staff transfusion medicine | Employees for the care of people with disabilities | Health and nursing staff - endoscopy | Exam. Nurses for our department of anesthesia and intensive care medicine | Documentation care force
- ESCO skills: supervise nursing staff supervise the nu (40%); assume responsibility demonstrate a cons (29%); provide user documentation Develop and o (24%); develop pension schemes develop pension  (22%); geriatrics preventative methods in healt (19%); application process applications process (17%)

### C51: 62 postings (0.51%)
- Titles: Commercial employee | Commercial processing for property management | Commercial employee as assistant to the facility management | Commercial employee in property management | Commercial employee in the construction and real estate sector | Commercial employee facility management
- ESCO skills: accounting bookkeeping The documentation (16%); issue sales invoices issue a sales invoi (10%); facilities management in the organisatio (6%); German ability to comprehend spoken and  (6%); assume responsibility demonstrate a cons (5%); develop pension schemes develop pension  (5%)
- Lightcast terms: Materials Management (1)

### C11: 62 postings (0.51%)
- Titles: Salesperson part-time | Salesperson part-time for our store in Munich | Salesperson as a temporary worker | Seller part -time | Cashier part-time | Service worker part-time
- ESCO skills: trends in fashion directions in fashion  (63%); satisfy customers ensure satisfied custo (45%); keep an open mind take on new ideas and  (42%); apply development process to footwear de (40%); think innovatively apply innovative thin (40%); keep inventory of goods in production th (23%)

### C59: 61 postings (0.50%)
- Titles: Software developer | Application developer Quadient | SPS-Programmierer / Application Engineer | Software developer ILE RPG | Software Engineer (.NET Core) | Experienced software developer
- ESCO skills: Agile development The agile development  (13%); solution deployment The technologies and (11%); TypeScript The techniques and principles (11%); Java (computer programming) Java The tec (11%); develop pension schemes develop pension  (10%); C# C Sharp The techniques and principles (8%)

### C66: 59 postings (0.48%)
- Titles: Quality controller | Quality inspector / quality planner | Manager for integrated management systems - process optimization | Head of integrated management systems - quality management | Quality representative in healthcare | Head of integrated management systems
- ESCO skills: provide user documentation Develop and o (15%); implement a management system employ a m (12%); support implementation of quality manage (12%); inspect quality of products oversee prod (8%); manage quality oversee quality apply qua (8%); assertiveness self-assured confidence as (8%)
- Lightcast terms: Supply Chain (1)

### C53: 58 postings (0.47%)
- Titles: Studied social insurance with a focus on accident insurance | Training to become a social insurance clerk | Training as a bank clerk | Training as an industrial clerk | Training to become a merchant in the retail technology world | Training to become a merchant in e-commerce
- ESCO skills: accounting bookkeeping The documentation (26%); sales activities sales activity sales ex (17%); German ability to comprehend spoken and  (14%); logistics logistic coordination transpor (14%); consumer electronics home electronics el (10%); communicate with customers talk with cus (10%)
- Lightcast terms: Materials Management (2)

### C32: 58 postings (0.47%)
- Titles: Vertriebsmitarbeiter im Außendienst Großraum Neuruppin | Außendienstmitarbeiter im Direktvertrieb Zwickau, Aue | Sicherheitstechniker im Außendienst | Ökotrophologe als Ernährungsberater im Außendienst Süddeutschland | Außendienstmitarbeiter (Schwaben) Nutzfahrzeugreifen | Katalogverteiler im Außendienst
- ESCO skills: maintain relationship with customers sus (21%); prospect new customers prospecting a new (17%); develop pension schemes develop pension  (16%); attend trade fairs attending trade fairs (10%); manage personal professional development (10%); sales activities sales activity sales ex (10%)

### C4: 56 postings (0.46%)
- Titles: Postman for parcels and letters in Pansdorf | Postman for parcels and letters in Plön | Postman for parcels and letters in Ahrensbök | Postman for parcels and letters in Lübeck Kücknitz | Postman for parcels and letters in Berlin-Lankwitz | Postman for letters and parcels in Berlin-Köpenick
- ESCO skills: sell bicycles put bikes up for sale sell (91%); handle delivered packages distribute del (16%); deliver correspondence deliver the corre (16%); collect mail collecting mail pick up mai (4%); process booking process accommodation bo (2%); provide training in sustainable tourism  (2%)

### C55: 53 postings (0.43%)
- Titles: Sozialpädagoge:in / Sozialarbeiter:in mit staatlicher Anerkennung (Diplom/Bachel | Sozialpädagoge - für die Einrichtung Rue 66 | Sozialpädagoge - für die Einrichtung Kriwo Wandsbek | Sozialarbeiterin / Sozialarbeiter oder Sozialpädagogin / Sozialpädagoge im Sozia | Sozialpädagogin | Sozialpädagoge / Sozialarbeiter Kinder- und Jugendnotdienst
- ESCO skills: recreation activities activities for rec (13%); supervision of persons guidance of perso (11%); assertiveness self-assured confidence as (8%); develop creative ideas developing creati (6%); gender studies the study of gender gende (6%); public relations PR public image The pra (6%)

