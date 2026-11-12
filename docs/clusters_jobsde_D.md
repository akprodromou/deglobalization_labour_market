# Clusters: jobsde, input D

12,243 postings; 80 clusters; noise 29.5%; relative validity 0.199; min_cluster_size 40.

- Stability seed 1 vs seed 2: ARI 0.913 on the 64.2% of postings clustered in both; 72 clusters.
- Stability seed 1 vs seed 3: ARI 0.944 on the 66.3% of postings clustered in both; 77 clusters.
- k-means with k=80 on the same UMAP space: AMI 0.913, ARI 0.671 against HDBSCAN (non-noise postings).

## Named emerging occupations (regex on the cleaned title; found or not, never forced)

| occupation | titles matched | in a cluster | top clusters (matches / cluster size) |
|---|---|---|---|
| trade compliance officer | 0 | 0 | - |
| export control specialist | 1 | 0 | - |
| supply chain resilience analyst | 0 | 0 | - |
| semiconductor process engineer | 2 | 2 | C79 (2/210) |
| battery cell technician | 0 | 0 | - |
| critical materials specialist | 0 | 0 | - |
| reshoring program manager | 0 | 0 | - |

## Largest 60 clusters plus every cluster hit by a named occupation

### C29: 960 postings (7.84%)
- Titles: Elektriker Service-Center | Holzmechaniker | Bauingenieur als Lead Engineer CSA | Kfz.-Mechatroniker | Trained or semi-trained: WKS insulator in the area of ​​heating / plumbing at Sc | Kfz-Mechatroniker
- ESCO skills: manage maintenance operations manage ope (14%); develop pension schemes develop pension  (11%); mechatronics mechatronic engineering mec (8%); assume responsibility demonstrate a cons (6%); meet commitments meet commitment show co (5%); civil engineering civil engineering appl (4%)
- Lightcast terms: Planning Software (8); Lithography (2); Production Planning (2); Materials Management (1); Supply Chain (1)

### C52: 499 postings (4.08%)
- Titles: Financial and/or payroll accountant | Employee in financial accounting | Clerk applications | Personnel services clerk | Clerk | Office management clerk
- ESCO skills: accounting bookkeeping The documentation (24%); financial statements statements on finan (17%); develop pension schemes develop pension  (8%); issue sales invoices issue a sales invoi (8%); use microsoft office have proficiency in (7%); assume responsibility demonstrate a cons (7%)
- Lightcast terms: Materials Management (3); Supply Chain (1); Supply Chain Management (1)

### C45: 298 postings (2.43%)
- Titles: Warehouse logistics specialist on day shift | Warehouse clerk / warehouse logistics specialist | Warehouse logistics | Warehouse clerk auxiliary materials warehouse | Warehouse logistics specialist | Warehouse employee in picking
- ESCO skills: receive goods secure goods accept goods  (11%); develop pension schemes develop pension  (11%); manage transport of goods from warehouse (9%); unload supplies remove delivered product (8%); meet commitments meet commitment show co (7%); assume responsibility demonstrate a cons (7%)
- Lightcast terms: Supply Chain (7); Supply Chain Management (2); Delivery Performance (2); Materials Management (2); Production Planning (1)

### C77: 294 postings (2.40%)
- Titles: Construction manager maintenance | Surveyor / planner pipeline construction | Project manager TGA / HKLS / GLT in industrial planning | Construction manager maintenance Augsburg | Calculator for civil engineering | Project Manager Electrical Engineering
- ESCO skills: civil engineering civil engineering appl (16%); manage maintenance operations manage ope (15%); develop pension schemes develop pension  (15%); perform project management perform manag (12%); assume responsibility demonstrate a cons (11%); CAD software CADD software computer assi (10%)
- Lightcast terms: Supply Chain (3); Supply Chain Management (2); Lithography (1); Materials Management (1); Demand Planning (1)

### C78: 262 postings (2.14%)
- Titles: Electronics technician in system integration | Electrical engineer | Electronics technician / electrician | Electrician as DGUV V3 inspector | Electrician / electronics technician maintenance | Electrician
- ESCO skills: manage maintenance operations manage ope (38%); mechatronics mechatronic engineering mec (21%); develop pension schemes develop pension  (16%); work with e-services available to citize (12%); meet commitments meet commitment show co (10%); automation technology technology for con (9%)
- Lightcast terms: Material Flow Management (1); Supply Chain (1)

### C14: 247 postings (2.02%)
- Titles: Specialist in anesthesiology with a focus on intensive care medicine | Nursing specialist for intensive care and ventilation | Nursing specialist for intensive care and ventilation, GfB | Nurse surgical gynecology | Nursing specialist: woman or health and nursing assistant | Nursing specialist cardiology ward
- ESCO skills: specialist nursing care specialist analy (31%); supervise nursing staff supervise the nu (21%); intensive care medicine medical intensiv (17%); innovation in nursing innovation in the  (16%); professional documentation in health car (13%); provide user documentation Develop and o (11%)
- Lightcast terms: Supply Management (1)

### C79: 210 postings (1.72%) [named: semiconductor process engineer]
- Titles: Electrical engineer / electrical engineer specializing in electrical engineering | Mechatronics engineer / industrial electrician | Maintenance coordinator electrical engineering / mechatronics | Electronics engineer / mechatronics engineer | Automotive mechatronics engineer | Automotive, agricultural or construction machinery mechanic
- ESCO skills: mechatronics mechatronic engineering mec (39%); manage maintenance operations manage ope (24%); pneumatics pneumatics applications The a (10%); develop pension schemes develop pension  (10%); provide user documentation Develop and o (9%); drive agricultural machines agricultural (9%)
- Lightcast terms: Vertical Integration (2); Lithography (1)

### C70: 189 postings (1.54%)
- Titles: Buchhalter/in / Finanzbuchhalter/in Personalsachbearbeiter/in | Leiter(in) Buchhaltung/Rechnungswesen | Mitarbeiter Rechnungswesen / Finanzen | Abrechnungsheld für unsere Provisionsabteilung gesucht | Sachbearbeiter Finanzbuchhaltung / Lohnbuchhaltung | Mitarbeiter Praxisanmeldung & Abrechnungsmanagement
- ESCO skills: accounting bookkeeping The documentation (41%); financial statements statements on finan (31%); issue sales invoices issue a sales invoi (14%); use microsoft office have proficiency in (14%); follow up accounts receivables monitor a (12%); prepare financial statements draw up fin (10%)

### C50: 184 postings (1.50%)
- Titles: Logistikmitarbeiter | Fachlagerist | Logistik-Koordinator | Logistik-Analyst | Dispenser Logistik | Fachlagerist Lager
- ESCO skills: receive goods secure goods accept goods  (11%); unload supplies remove delivered product (9%); meet commitments meet commitment show co (8%); develop pension schemes develop pension  (8%); use microsoft office have proficiency in (7%); logistics logistic coordination transpor (6%)
- Lightcast terms: Supply Chain (5); Production Planning (2); Capacity Planning (1); Supply Chain Management (1); Supply Management (1)

### C28: 171 postings (1.40%)
- Titles: Chemikant / Produktionsfachkraft Chemie | Chemielaborant | Ausbildung Maschinen- und Anlagenführer | Maschinenführer | Maschinen- und Anlagenführer Abfüllung | Anlagen- und Maschinenführer
- ESCO skills: production processes production process  (11%); milling machines powdering machines mill (8%); develop pension schemes develop pension  (8%); manage maintenance operations manage ope (6%); assume responsibility demonstrate a cons (5%); quality standards The national and inter (5%)
- Lightcast terms: Production Planning (1)

### C12: 166 postings (1.36%)
- Titles: Truck driver/professional driver | Truck driver / professional driver | Professional driver / truck loading crane driver in local transport | Local transport driver and shunting driver | Truck driver / professional driver in local transport | Truck driver in local transport
- ESCO skills: meet commitments meet commitment show co (10%); develop pension schemes develop pension  (10%); logistics logistic coordination transpor (9%); assume responsibility demonstrate a cons (8%); German ability to comprehend spoken and  (5%); receive goods secure goods accept goods  (5%)
- Lightcast terms: Supply Chain (1)

### C60: 148 postings (1.21%)
- Titles: Office worker/assistant | GTB Administration Officer | Office assistant in the Regulatory Affairs department | Office Manager/in | Administrative specialist | Office manager
- ESCO skills: manage human resources manage hr direct  (17%); use microsoft office have proficiency in (13%); attend meetings turn up at gatherings ta (9%); develop pension schemes develop pension  (9%); human resource management human resource (8%); communication conversation interaction c (7%)
- Lightcast terms: Cold Chain (1); Capacity Planning (1)

### C37: 130 postings (1.06%)
- Titles: SALONLEITUNG LÜNEBURG | Filialleitung / Studioleitung | Marktleitung | Marktleiter / Filialleiter | Abteilungsleitung Blutspende | Führungskraft in der Filiale
- ESCO skills: assume responsibility demonstrate a cons (13%); communication conversation interaction c (12%); sales activities sales activity sales ex (12%); lead others exert a goal-oriented leader (11%); motivate employees encourage employees m (10%); sell products selling products sell a pr (10%)
- Lightcast terms: Capacity Planning (1); Materials Management (1); Supply Chain (1); Supply Chain Management (1)

### C69: 127 postings (1.04%)
- Titles: Verwaltungskraft für die Bewohnerverwaltung | Sachbearbeiter:in für Zivil- und Katastrophenschutz | Sachbearbeiter*in im Bereich Einbürgerung, Staatsangehörigkeiten | Sachbearbeiter/in für die Strassenverkehrsbehörde | Zwei Sachbearbeiter / Sachbearbeiterinnen Stellenbewertung | Sachbearbeiter/ Sachbearbeiterin Gremienbetreuung/ Beschluss- und Vorlagenmanage
- ESCO skills: assume responsibility demonstrate a cons (14%); office administration office control off (7%); meet commitments meet commitment show co (6%); assertiveness self-assured confidence as (6%); application process applications process (6%); coordinate security oversee security man (6%)

### C75: 124 postings (1.01%)
- Titles: Service technician for frigates | technology employee | Maintenance technician Maintenance (PAT) | Technical employee configuration | Technical employee | Trainer for technical training
- ESCO skills: manage maintenance operations manage ope (24%); mechatronics mechatronic engineering mec (17%); develop pension schemes develop pension  (13%); communicate with customers talk with cus (7%); consumer electronics home electronics el (6%); meet commitments meet commitment show co (6%)
- Lightcast terms: Materials Management (1)

### C66: 124 postings (1.01%)
- Titles: Salesperson / career changer bakery | Salesperson/bakery salesperson/career changer bakery | Salesman / cheese / employee bakery | Salesperson delicatessen | Baker in our organic bakery | Salesperson/customer advisor fresh food and service counter
- ESCO skills: maintain personal hygiene standards main (13%); sell products selling products sell a pr (10%); operate cash register run a cash point o (9%); sales activities sales activity sales ex (8%); assume responsibility demonstrate a cons (6%); coordinate catering coordinating caterin (6%)
- Lightcast terms: Cold Chain (1); Cold Store (1); Demand Management (1)

### C46: 122 postings (1.00%)
- Titles: Systemadministrator Senior/Linux | IT-Infrastrukturmanager/in | Systemexperte MES iTAC | IT-Management-Spezialist*in | IT-Support-Koordinator*in | IT-Support-Spezialist*in
- ESCO skills: German ability to comprehend spoken and  (11%); operating systems The features, restrict (11%); administer ICT system operate system adm (11%); provide user documentation Develop and o (11%); manage maintenance operations manage ope (10%); develop pension schemes develop pension  (10%)

### C25: 119 postings (0.97%)
- Titles: Deputy ward manager for our urological ward | Deputy ward manager for ophthalmology | Deputy ward manager oncology/palliative | Deputy branch manager | Deputy Nursing service manager | Deputy laboratory manager
- ESCO skills: assume responsibility demonstrate a cons (13%); sales activities sales activity sales ex (8%); sell products selling products sell a pr (8%); motivate others inspire others stimulate (8%); facilities management in the organisatio (8%); assertiveness self-assured confidence as (8%)

### C57: 117 postings (0.96%)
- Titles: Pflegefachkraft gesucht | Pflegefachkraft Geriatrie Privita | Pflegefachkraft für die vollstationäre Pflege | Pflegefachkräfte | Pflegefachkraft Kardiologie | Pflegefachkraft für Fachbereich Demenz
- ESCO skills: specialist nursing care specialist analy (14%); assume responsibility demonstrate a cons (11%); geriatrics preventative methods in healt (9%); teach further education teaches further  (9%); professional documentation in health car (9%); supervise nursing staff supervise the nu (9%)

### C34: 115 postings (0.94%)
- Titles: Seller Non Food | Verkäuferin Bedientheke | Verkäufer/Kassierer Backshop | Verkäufer Frischfisch | Verkäuferin / Verkäufer für Bäckerei in Berlin Köpenick | Verkäufer/in
- ESCO skills: show initiative take the initiative give (16%); process incoming construction supplies r (15%); deal with public communicate with the pu (15%); maintain personal hygiene standards main (14%); develop pension schemes develop pension  (14%); German ability to comprehend spoken and  (14%)
- Lightcast terms: Materials Management (1)

### C59: 112 postings (0.91%)
- Titles: Complaint processing employee | Employee customer service | Service worker | Service employee retail | Canteen service worker | SERVICE EMPLOYEE
- ESCO skills: meet commitments meet commitment show co (10%); respond to customers' inquiries deal wit (9%); sales activities sales activity sales ex (9%); write German writing German correspond i (6%); hygiene in a health care setting hygiene (6%); communicate by telephone communicate thr (6%)
- Lightcast terms: Supply Chain (1)

### C1: 112 postings (0.91%)
- Titles: Postman for parcels and letters | Postman for letters and parcels | Postman for parcels and letters in Bad | Postman for parcels | Postman for letters and parcels in Wattenscheid | Postman for parcels and letters in Mühlenbeck
- ESCO skills: sell bicycles put bikes up for sale sell (97%); deliver correspondence deliver the corre (22%); handle delivered packages distribute del (10%)

### C44: 111 postings (0.91%)
- Titles: Sales professional / consultant / financial advisor / insurance agent Dortmund | Versicherungskaufmann / Versicherungsmakler gesucht | Finanzberater / Versicherungskaufmann | Kaufmann für Versicherungen für unsere laufenden Neukundenzugänge Region Stuttga | Bankkaufmann gesucht für die Region Ellwangen und Umgebung | Kauffrau/-mann für Versicherungen und Finanzen
- ESCO skills: sales activities sales activity sales ex (22%); banking activities banking activity The  (21%); prospect new customers prospecting a new (21%); advise on investment provide investment  (11%); assume responsibility demonstrate a cons (8%); accounting bookkeeping The documentation (8%)

### C33: 105 postings (0.86%)
- Titles: Production employee in the food industry | Production employee aviation | Employee for production | Team member production | Production employee at the Landsberg plant | Production employee
- ESCO skills: meet commitments meet commitment show co (11%); control production direct production con (11%); production processes production process  (10%); assume responsibility demonstrate a cons (10%); optimise production maximise production  (8%); adhere to OHSAS 18001 adhere to OHSAS 18 (7%)
- Lightcast terms: Production Planning (10); Capacity Planning (3); Electronics Manufacturing (1); Planning Software (1); Supply Chain (1)

### C5: 103 postings (0.84%)
- Titles: Postman for parcels and letters - temporary help/retrieval | postman on call | Postman for parcels and letters - temporary help / on-call worker | Postman - temporary help / on-call | Postman for parcels and letters - temporary help/on-call | Postman - temporary assistant / caller
- ESCO skills: deliver correspondence deliver the corre (36%); sell bicycles put bikes up for sale sell (27%); handle delivered packages distribute del (19%); German ability to comprehend spoken and  (1%); assume responsibility demonstrate a cons (1%); develop creative ideas developing creati (1%)

### C16: 99 postings (0.81%)
- Titles: Professional recognition year (social worker or educator ) | Trainees as youth and home educators in Niefern | Social educators educators in the ION | Pedagogical employee/social worker in young care | Trainees as youth and home educators SGA school starter | Social educator Social pedagogy course (Bachelor / Master)
- ESCO skills: meet commitments meet commitment show co (11%); recreation activities activities for rec (10%); assume responsibility demonstrate a cons (9%); relate empathetically empathise with oth (8%); supervision of persons guidance of perso (7%); assess the development of youth promote  (7%)

### C26: 93 postings (0.76%)
- Titles: Machine and plant operator | Plant operator | Machine operator / plant operator | Machine and plant operator project production | Plant operator at the firing table kiln | Training to become a machine and plant operator
- ESCO skills: production processes production process  (17%); packaging functions packaging operations (6%); meet commitments meet commitment show co (6%); manage maintenance operations manage ope (6%); German ability to comprehend spoken and  (6%); tend packaging machines mind packaging m (5%)
- Lightcast terms: Shipping Systems (1)

### C55: 92 postings (0.75%)
- Titles: Erzieher / Heilerziehungspfleger / Sozialpädagogen | Erzieher / Heilpädagoge | Fachkräfte Erzieher/Innen für den Gruppendienst im Elementarbereich | Heilerziehungspfleger/in | Heilerziehungspfleger / Erzieher | Erzieher / Heilerziehungspfleger
- ESCO skills: coach individuals in specialised nursing (10%); recreation activities activities for rec (10%); supervision of persons guidance of perso (9%); provide user documentation Develop and o (8%); meet commitments meet commitment show co (7%); support employability of people with dis (5%)

### C24: 91 postings (0.74%)
- Titles: Career changer for retraining as a train driver in the Munich S-Bahn November 1 | Customer service / customer advisor career changers welcome | Nursing assistant / career changer | Train driver / locomotive driver career changer | Employee customer service / career changer | Call center agent / career changer in customer service
- ESCO skills: deal with public communicate with the pu (14%); develop pension schemes develop pension  (13%); receive goods secure goods accept goods  (12%); bake goods bake a good bake bake product (11%); sell products selling products sell a pr (11%); meet commitments meet commitment show co (9%)

### C27: 91 postings (0.74%)
- Titles: Glasreiniger | Hygienefachkraft | Cleaner / mini job [Villingen-Schw | Cleaner / mini job [Queidersbach | Busreiniger | Housekeeping / Raumpfleger
- ESCO skills: facilities management in the organisatio (14%); maintain personal hygiene standards main (10%); clean building floors cleaning building  (10%); manage maintenance operations manage ope (9%); human-computer interaction HCI The study (8%); develop pension schemes develop pension  (7%)
- Lightcast terms: Cold Store (1)

### C62: 89 postings (0.73%)
- Titles: CNC specialist | Machining mechanic - milling technology | Tool mechanic | Cutting mechanic with and without shift | CNC machining mechanic turning or milling machines | Mechanic
- ESCO skills: manage maintenance operations manage ope (24%); milling machines powdering machines mill (20%); tend CNC milling machine monitor CNC mil (16%); develop pension schemes develop pension  (16%); assume responsibility demonstrate a cons (16%); injection moulding machine parts compone (13%)
- Lightcast terms: Production Planning (4)

### C31: 87 postings (0.71%)
- Titles: Sales manager | Senior Sales Manager | Sales Manager / Sales Manager | Regional Sales Manager | Sales-Manager | Global Sales Trainer
- ESCO skills: sales activities sales activity sales ex (24%); prospect new customers prospecting a new (20%); communicate with customers talk with cus (15%); assume responsibility demonstrate a cons (11%); show entrepreneurial spirit identify opp (10%); maintain relationship with customers sus (9%)
- Lightcast terms: Supply Chain (2); Supply Chain Management (2)

### C0: 87 postings (0.71%)
- Titles: Postman for parcels and letters | Postman for letters and parcels
- ESCO skills: sell bicycles put bikes up for sale sell (99%); deliver correspondence deliver the corre (38%); handle delivered packages distribute del (8%); negotiate employment agreements negotiat (1%)

### C41: 82 postings (0.67%)
- Titles: Movement/sports/dance therapist | Physiotherapist / physiotherapist for our independent practice | Movement therapist | Rehabilitationsspezialist | Physiotherapist / physiotherapist as practice manager | Physiotherapist
- ESCO skills: physiotherapy specialism in physiotherap (33%); treat speech disorders provide speech th (15%); occupational science study of everyday a (12%); assume responsibility demonstrate a cons (9%); develop creative ideas developing creati (9%); develop pension schemes develop pension  (9%)
- Lightcast terms: Supply Chain (1)

### C32: 81 postings (0.66%)
- Titles: Social Media Manager | Senior Social Media Manager (gn) | (Junior) Business Development Manager | Social Media Manager B2B | Junior Marketing Specialist | Junior Marketing Assistant
- ESCO skills: communication conversation interaction c (26%); market analysis analysis of the market m (16%); develop creative ideas developing creati (16%); sales activities sales activity sales ex (11%); use presentation software produce electr (10%); work with different target groups work w (9%)
- Lightcast terms: Supply Chain (1)

### C21: 81 postings (0.66%)
- Titles: Kitchen helper | Housekeeping helper or housekeeper | Domestic employee in the living area | Cook - permanent | Chef food production | Head chef
- ESCO skills: coordinate catering coordinating caterin (15%); respect the diversity of cultural values (14%); workplace sanitation workplace hygiene w (11%); recreation activities activities for rec (11%); respect data protection principles follo (10%); supervise housekeeping operations overse (9%)

### C58: 75 postings (0.61%)
- Titles: Medizinische Fachangestellte/r | Arbeitsmediziner oder Arzt in Weiterbildung | Medizinische Fachangestellte ZNA | Medizinische Fachangestellte | Medizinische*r Fachangestellte*r Hämatologie / Onkologie / Infektionskrankheiten | Medizinischer Fachangestellter Medizinisches Versorgungszentrum
- ESCO skills: cardiology disorders of the heart diseas (5%); meet commitments meet commitment show co (5%); assume responsibility demonstrate a cons (5%); collect biological samples from patients (5%); neurology medical conditions of the nerv (5%); innovation in nursing innovation in the  (5%)

### C51: 74 postings (0.60%)
- Titles: Teamassistenz | Serviceassistenz | Assistent | Teamassistent/in | Teamassistent | Sterilisationsassistenten
- ESCO skills: attend meetings turn up at gatherings ta (14%); German ability to comprehend spoken and  (14%); meet commitments meet commitment show co (11%); use presentation software produce electr (11%); communication conversation interaction c (9%); communicate with customers talk with cus (9%)

### C53: 74 postings (0.60%)
- Titles: Commercial employee | Commercial processing for property management | Commercial employee in property management | Housing benefit processing | Commercial employee in the construction and real estate sector | Commercial specialist as technical team assistant
- ESCO skills: accounting bookkeeping The documentation (16%); issue sales invoices issue a sales invoi (11%); facilities management in the organisatio (5%); develop pension schemes develop pension  (5%); office administration office control off (5%); German ability to comprehend spoken and  (5%)
- Lightcast terms: Materials Management (1)

### C9: 74 postings (0.60%)
- Titles: specialist in the field of stage design and work pedagogy | Pedagogical specialist | Pedagogical specialist for a new fully supervised facility | ped. Specialist | ped. Specialist or supplementary worker in Oberpleis | Pedagogical specialist / educator
- ESCO skills: cooperate with colleagues work together  (20%); meet commitments meet commitment show co (14%); supervision of persons guidance of perso (11%); coach individuals in specialised nursing (11%); develop pension schemes develop pension  (11%); demonstrate willingness to learn display (8%)

### C48: 72 postings (0.59%)
- Titles: Berufskraftfahrer | Schwertransportfahrer für den nationalen & internationalen Fernverkehr gesucht | Kraftfahrer / Berufskraftfahrer im Fernverkehr | Berufskraftfahrer im Nahverkehr - hohe Spesen | LKW Fahrer im Nahverkehr | LKW Fahrer/ Berufskraftfahrer mit FS-Klasse C/CE
- ESCO skills: logistics logistic coordination transpor (17%); maintain personal hygiene standards main (12%); sustainable building materials sustainab (12%); develop pension schemes develop pension  (11%); assume responsibility demonstrate a cons (11%); warehousing regulations warehouse regula (11%)
- Lightcast terms: Supply Chain (1)

### C68: 71 postings (0.58%)
- Titles: Internal Sales Employee | Employee in internal sales | Sales representative internal service - building technology | Employee in internal sales insurance | Head of Internal Sales | Internal sales representative (gn)
- ESCO skills: communicate with customers talk with cus (15%); maintain relationship with customers sus (13%); sales activities sales activity sales ex (11%); use microsoft office have proficiency in (8%); show initiative take the initiative give (8%); negotiate compromises resolve conflict n (8%)
- Lightcast terms: Materials Management (1); Supply Chain (1)

### C67: 70 postings (0.57%)
- Titles: Customer advisor services/service | Customer advisor ADAC credit card | Service advisor in the car dealership | Telephone customer advisor inbound | Customer advisor customer service | Customer advisor service and sales outbound
- ESCO skills: provide high quality customer service pu (16%); satisfy customers ensure satisfied custo (14%); assume responsibility demonstrate a cons (13%); identify customer's needs identifying a  (10%); hotel operations hotel management hotel  (7%); develop pension schemes develop pension  (7%)

### C56: 69 postings (0.56%)
- Titles: Physiotherapeut / Ergotherapeut / Logopäde | Physiotherapist / physiotherapist 20-28€/h | Physiotherapist / mini job Bad Waldsee | Physiotherapeut*in | Ergotherapeuten | Ergotherapeut* Ergotherapeutin
- ESCO skills: physiotherapy specialism in physiotherap (29%); develop pension schemes develop pension  (14%); neurology medical conditions of the nerv (12%); treat speech disorders provide speech th (12%); attend meetings turn up at gatherings ta (12%); meet commitments meet commitment show co (12%)

### C8: 68 postings (0.56%)
- Titles: Digital Trust and Safety Analyst with knowledge of German | Digital Trust and Safety Analyst with German | Digital Trust and Safety Analyst with Arabic | Start your adventure: German-speaking job offers in Greece - Career career chang | German customer advisor, start your career at Mercedes-Benz in Greece | Jobs in Greece Including moving support
- ESCO skills: German ability to comprehend spoken and  (28%); innovate in ICT Create and describe new  (18%); maintain relationship with customers sus (18%); communicate with customers talk with cus (13%); promote healthy lifestyle encourage heal (12%); table tennis ping-pong The theory, techn (10%)

### C65: 68 postings (0.56%)
- Titles: Assistent/in für den Kaufmännischen Leiter | Kaufm. Mitarbeiter:in als Auftragsmanager | Kaufmännischer Mitarbeiter / Spezialist Einkauf | Kaufmännischer Angestellter Service Support/Control | Kaufmännischer Mitarbeiter / Sachbearbeiter mit Polnischkenntnissen | Kaufmännische Fachkraft
- ESCO skills: use microsoft office have proficiency in (18%); communicate with customers talk with cus (16%); write German writing German correspond i (9%); issue sales invoices issue a sales invoi (9%); meet commitments meet commitment show co (9%); office software office soft-ware office  (7%)
- Lightcast terms: Supply Chain (2); Supply Chain Management (2); Production Planning (1); Demand Forecasting (1)

### C10: 67 postings (0.55%)
- Titles: Nursing staff | Health and nursing staff transfusion medicine | Nurse infusion center | Employee in care and nursing | Green area nurse | Nursing person
- ESCO skills: supervise nursing staff supervise the nu (55%); provide user documentation Develop and o (40%); assume responsibility demonstrate a cons (27%); develop pension schemes develop pension  (21%); communicate by telephone communicate thr (16%); application process applications process (16%)

### C49: 67 postings (0.55%)
- Titles: Fleischer/in - Metzgergeselle/in | Cook/Chef de partie/Demichef de partie abroad | Koch / Beikoch | Koch / Beikoch / Jungkoch | Koch in the Gastronomie im CenterParcs Bispinger | Chef de partie Restaurant in Stiftsberg
- ESCO skills: develop pension schemes develop pension  (7%); maintain personal hygiene standards main (7%); food hygiene rules food hygiene laws rul (7%); assume responsibility demonstrate a cons (7%); prepared meals previously prepared meals (6%); coordinate catering coordinating caterin (6%)

### C71: 65 postings (0.53%)
- Titles: Consultant corporate strategy | Sales consultant for cars, vans | Sales consultant | Sales consultant for automotive spare parts (mobile working) | Salesperson / Consultant | Sales Consultant for Automation Technology
- ESCO skills: maintain relationship with customers sus (32%); meet commitments meet commitment show co (25%); show initiative take the initiative give (18%); sales activities sales activity sales ex (15%); show entrepreneurial spirit identify opp (15%); communication conversation interaction c (12%)

### C54: 65 postings (0.53%)
- Titles: Sozialpädagoge:in / Sozialarbeiter:in mit staatlicher Anerkennung (Diplom/Bachel | Sozialpädagoge - für die Einrichtung Kriwo Wandsbek | Sozialarbeiterin / Sozialarbeiter oder Sozialpädagogin / Sozialpädagoge im Sozia | Sozialpädagoge / Sozialarbeiter Kinder- und Jugendnotdienst | Sozialarbeiter im Allgemeinen Sozialdienst (ASD) | Mitarbeiter Soziale Beratung mit Option auf Weiterentwicklung zum Projektkoordin
- ESCO skills: recreation activities activities for rec (12%); supervision of persons guidance of perso (11%); develop creative ideas developing creati (6%); cooperate with colleagues work together  (6%); assume responsibility demonstrate a cons (6%); assertiveness self-assured confidence as (6%)

### C74: 64 postings (0.52%)
- Titles: Employee central quality management | Quality controller | Quality inspector / quality planner | Manager for integrated management systems - process optimization | Head of integrated management systems - quality management | Quality representative in healthcare
- ESCO skills: provide user documentation Develop and o (14%); implement a management system employ a m (9%); support implementation of quality manage (9%); assertiveness self-assured confidence as (9%); communicate with customers talk with cus (8%); internal auditing internal investigation (8%)
- Lightcast terms: Supply Chain (1)

### C30: 63 postings (0.51%)
- Titles: Sales representative in the B2B field service | Sales representative field service | Field service representative technical sales in Lower Saxony | Pharmaceutical representative in the field | Field sales representative electrical | Field sales representative
- ESCO skills: prospect new customers prospecting a new (22%); sales activities sales activity sales ex (17%); maintain relationship with customers sus (14%); market analysis analysis of the market m (14%); develop pension schemes develop pension  (14%); manage sales teams managing sales teams  (13%)
- Lightcast terms: Planning Software (1)

### C42: 63 postings (0.51%)
- Titles: Software developer | Application developer Quadient | Software developer ILE RPG | Software Engineer (.NET Core) | Experienced software developer | SPS Entwickler
- ESCO skills: Agile development The agile development  (13%); solution deployment The technologies and (11%); TypeScript The techniques and principles (11%); Java (computer programming) Java The tec (11%); develop pension schemes develop pension  (10%); C# C Sharp The techniques and principles (8%)

### C7: 62 postings (0.51%)
- Titles: Postman / delivery person for parcels and letters | Parcel delivery driver / driver career changer | Postman / delivery person for parcels | Postman / delivery person for parcels and letters in India | Parcel deliverer / courier / driver | Postman / parcel delivery person
- ESCO skills: sell bicycles put bikes up for sale sell (76%); deliver correspondence deliver the corre (24%); handle delivered packages distribute del (18%); German ability to comprehend spoken and  (5%); childbirth birth of a child confinement  (5%); collect mail collecting mail pick up mai (3%)

### C39: 62 postings (0.51%)
- Titles: Versicherungsfachmann Außendienst | Vertriebsmitarbeiter im Außendienst Großraum | Außendienstmitarbeiter im Direktvertrieb Zwickau, Aue | Sicherheitstechniker im Außendienst | Handelsvertreter für Nutzfahrzeuge im Außendienst | Ökotrophologe als Ernährungsberater im Außendienst Süddeutschland
- ESCO skills: maintain relationship with customers sus (19%); prospect new customers prospecting a new (18%); develop pension schemes develop pension  (15%); attend trade fairs attending trade fairs (10%); manage personal professional development (10%); set sales goals settle sales goals estab (10%)

### C20: 61 postings (0.50%)
- Titles: Plant operator from 16€/h | Schlosser ab 17€/h in Tagschicht | Industrial mechanic with flexible working hours (17€/h) | Glazier on day shift (depending on qualifications €13.80/h - €17/h) | Employees for building technology in day shifts from 16€/h | Forklift driver in 3 shifts (€14.15/h)
- ESCO skills: recruit personnel personnel recruiting p (79%); mechatronics mechatronic engineering mec (11%); communication conversation interaction c (7%); precision mechanics discipline of precis (5%); manage maintenance operations manage ope (5%); manage a good diction use a good diction (5%)
- Lightcast terms: Photolithography (1); Plasma Etching (1)

### C19: 59 postings (0.48%)
- Titles: MFA Order Entry/Customer Care | Medical Assistant / Medical Assistant Clinic for Radiology and Nuclear Medicine | Medical Assistant / MFA | MFA / Medical Assistant | MFA in blood donation | Operational technical assistance (OTA)
- ESCO skills: innovation in nursing innovation in the  (14%); meet commitments meet commitment show co (8%); dermatology dermatology principles medin (8%); specialist nursing care specialist analy (8%); recreation activities activities for rec (8%); cardiology disorders of the heart diseas (8%)

### C4: 59 postings (0.48%)
- Titles: Salesperson | Salesperson retail | Sales person | Saleswoman | Salesperson, retail merchant | Salesperson fashion
- ESCO skills: demonstrate motivation for sales demonst (29%); trends in fashion directions in fashion  (27%); keep inventory of goods in production th (27%); sell products selling products sell a pr (10%); personal development self-reflection tec (10%); meet commitments meet commitment show co (8%)

### C76: 58 postings (0.47%)
- Titles: Welder | Pipe fitter or fitter | Welder in pipeline construction | Welder MAG process | Bricklayer/drywaller | TIG/MAG welder - metal industry
- ESCO skills: develop pension schemes develop pension  (17%); manage maintenance operations manage ope (10%); technical drawings mechanical drawings s (10%); perform metal active gas welding impleme (9%); meet commitments meet commitment show co (7%); build machines fabricate equipment assem (7%)
- Lightcast terms: Vertical Integration (1)

### C36: 57 postings (0.47%)
- Titles: Mediaberater | Serviceberater in Nürnberg | Serviceberater | BAV Berater | Serviceberater Automobil | Automobil-Serviceberater
- ESCO skills: sales activities sales activity sales ex (14%); show initiative take the initiative give (12%); meet commitments meet commitment show co (11%); respond to customers' inquiries deal wit (11%); deal with public communicate with the pu (9%); develop pension schemes develop pension  (9%)
- Lightcast terms: Capacity Planning (1)

