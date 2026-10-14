# Pilot exposure groups: keyword counts in the sampled postings

Pilot lists, titles (cut to 90 characters) and first sector labels only. Cells: matches / sampled postings (share), then the implied number of postings in the whole month (share x month total). Not results: the purpose is to see whether each group is large enough to analyse. Check the matched titles at the end for false positives.

## jobbland.se

| month | sampled | ev_industry | vehicle_retail_service | energy_fuels | transport_shipping | tourism | manufacturing | control_health_edu |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2026-01 | 600 | 6/600 (1.0%) ≈ 485 | 24/600 (4.0%) ≈ 1,940 | 31/600 (5.2%) ≈ 2,506 | 48/600 (8.0%) ≈ 3,881 | 21/600 (3.5%) ≈ 1,698 | 54/600 (9.0%) ≈ 4,366 | 105/600 (17.5%) ≈ 8,489 |
| 2026-02 | 600 | 11/600 (1.8%) ≈ 1,017 | 19/600 (3.2%) ≈ 1,756 | 27/600 (4.5%) ≈ 2,496 | 55/600 (9.2%) ≈ 5,084 | 23/600 (3.8%) ≈ 2,126 | 51/600 (8.5%) ≈ 4,714 | 97/600 (16.2%) ≈ 8,966 |
| 2026-03 | 600 | 9/600 (1.5%) ≈ 936 | 23/600 (3.8%) ≈ 2,392 | 33/600 (5.5%) ≈ 3,432 | 50/600 (8.3%) ≈ 5,199 | 23/600 (3.8%) ≈ 2,392 | 43/600 (7.2%) ≈ 4,471 | 111/600 (18.5%) ≈ 11,543 |
| 2026-04 | 600 | 6/600 (1.0%) ≈ 477 | 19/600 (3.2%) ≈ 1,511 | 20/600 (3.3%) ≈ 1,591 | 46/600 (7.7%) ≈ 3,659 | 25/600 (4.2%) ≈ 1,988 | 53/600 (8.8%) ≈ 4,215 | 132/600 (22.0%) ≈ 10,499 |
| 2026-05 | 600 | 14/600 (2.3%) ≈ 1,255 | 22/600 (3.7%) ≈ 1,972 | 35/600 (5.8%) ≈ 3,138 | 49/600 (8.2%) ≈ 4,393 | 22/600 (3.7%) ≈ 1,972 | 67/600 (11.2%) ≈ 6,007 | 149/600 (24.8%) ≈ 13,359 |

## kariera.gr

| month | sampled | ev_industry | vehicle_retail_service | energy_fuels | transport_shipping | tourism | manufacturing | control_health_edu |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2026-01 | 600 | 2/600 (0.3%) ≈ 24 | 20/600 (3.3%) ≈ 237 | 35/600 (5.8%) ≈ 415 | 34/600 (5.7%) ≈ 403 | 160/600 (26.7%) ≈ 1,897 | 69/600 (11.5%) ≈ 818 | 12/600 (2.0%) ≈ 142 |
| 2026-02 | 600 | 0/600 (0.0%) ≈ 0 | 17/600 (2.8%) ≈ 185 | 23/600 (3.8%) ≈ 251 | 40/600 (6.7%) ≈ 436 | 229/600 (38.2%) ≈ 2,497 | 75/600 (12.5%) ≈ 818 | 4/600 (0.7%) ≈ 44 |
| 2026-03 | 600 | 8/600 (1.3%) ≈ 93 | 17/600 (2.8%) ≈ 197 | 26/600 (4.3%) ≈ 301 | 45/600 (7.5%) ≈ 521 | 162/600 (27.0%) ≈ 1,877 | 65/600 (10.8%) ≈ 753 | 2/600 (0.3%) ≈ 23 |
| 2026-04 | 600 | 5/600 (0.8%) ≈ 55 | 18/600 (3.0%) ≈ 200 | 36/600 (6.0%) ≈ 400 | 67/600 (11.2%) ≈ 744 | 134/600 (22.3%) ≈ 1,487 | 58/600 (9.7%) ≈ 644 | 4/600 (0.7%) ≈ 44 |

## Before and after each event (pooled months, Wilson 95% interval for the share)

| case | group | pre: matches/n (share, interval) | post: matches/n (share, interval) |
|---|---|---|---|
| oil-gr (kariera.gr) | ev_industry | 2/1200 (0.2%, 0.0-0.6%) | 13/1200 (1.1%, 0.6-1.8%) |
| oil-gr (kariera.gr) | vehicle_retail_service | 37/1200 (3.1%, 2.2-4.2%) | 35/1200 (2.9%, 2.1-4.0%) |
| oil-gr (kariera.gr) | energy_fuels | 58/1200 (4.8%, 3.8-6.2%) | 62/1200 (5.2%, 4.1-6.6%) |
| oil-gr (kariera.gr) | transport_shipping | 74/1200 (6.2%, 4.9-7.7%) | 112/1200 (9.3%, 7.8-11.1%) |
| oil-gr (kariera.gr) | tourism | 389/1200 (32.4%, 29.8-35.1%) | 296/1200 (24.7%, 22.3-27.2%) |
| oil-gr (kariera.gr) | manufacturing | 144/1200 (12.0%, 10.3-14.0%) | 123/1200 (10.2%, 8.7-12.1%) |
| oil-gr (kariera.gr) | control_health_edu | 16/1200 (1.3%, 0.8-2.2%) | 6/1200 (0.5%, 0.2-1.1%) |
| oil-se (jobbland.se) | ev_industry | 17/1200 (1.4%, 0.9-2.3%) | 29/1800 (1.6%, 1.1-2.3%) |
| oil-se (jobbland.se) | vehicle_retail_service | 43/1200 (3.6%, 2.7-4.8%) | 64/1800 (3.6%, 2.8-4.5%) |
| oil-se (jobbland.se) | energy_fuels | 58/1200 (4.8%, 3.8-6.2%) | 88/1800 (4.9%, 4.0-6.0%) |
| oil-se (jobbland.se) | transport_shipping | 103/1200 (8.6%, 7.1-10.3%) | 145/1800 (8.1%, 6.9-9.4%) |
| oil-se (jobbland.se) | tourism | 44/1200 (3.7%, 2.7-4.9%) | 70/1800 (3.9%, 3.1-4.9%) |
| oil-se (jobbland.se) | manufacturing | 105/1200 (8.8%, 7.3-10.5%) | 163/1800 (9.1%, 7.8-10.5%) |
| oil-se (jobbland.se) | control_health_edu | 202/1200 (16.8%, 14.8-19.1%) | 392/1800 (21.8%, 19.9-23.7%) |

## Matched titles (first few per group, to spot false positives)

### jobbland.se

- **ev_industry**: Verification and Validation Engineer IRC286823 - GlobalLogic; dSpace HIL engineer - AD/ADAS in passenger cars - Alten Sverige AB; Service Technician/Mechanic for Service Workshop in Gothenburg! - The Automotive Academy; Electrician for 1KOMMA5° in Kalmar - 1KOMMA5 & deg; Sweden; Design engineer with engine experience - Sigma; Senior Exterior Designer - Blue Eye AB; Senior Product Manager - Avaron AB; Driver / Warehouse worker - Gävle - Pilkington Automotive Sweden AB
- **vehicle_retail_service**: Vehicle electrician for WC trailer in Härryda - Ikett Personalpartner AB; Workshop technician for Eslöv municipality - Eslöv municipality; Damage technician - Norrköping - Kraftsam Rekrytering & Bemanning AB; Vehicle attendant Bus Växjö - Connect Bus Sverige AB; We need you, rehab assistant for temporary work! - Ronneby municipality; Shop assistant café summer job - Biltema Sweden AB; Verification and Validation Engineer IRC286823 - GlobalLogic; Account Manager ID Scandinavian countries- EMEA - Graco, Inc.
- **energy_fuels**: Thermion is looking for a Project Manager for West Sweden - Thermion AB; Finsktalande Lekledare till sommarsässonen - Tallink Silja AB; System Administrator - SAP Basis - Centio Consulting Group AB; Warehouse worker for Apotek Hjärtat's E-pharmacy in Norrköping - Apotek Hjärtat AB; Extra job as shop assistant in Stockholm - Social attitude AB; Mountain technician - AFRY AB; Blomsterlandet Skövde - Next U AB; Blomsterlandet Norrköping Risängen - Next U AB
- **transport_shipping**: Workshop technician for Eslöv municipality - Eslöv municipality; Damage technician - Norrköping - Kraftsam Rekrytering & Bemanning AB; Vehicle attendant Bus Växjö - Connect Bus Sverige AB; We are looking for an experienced traverse driver! - TopWork Sweden AB; Substitute preschool teacher Möckelns preschool - Älmhult municipality; Quality coordinator - Swedish Maritime Administration; Project manager Road - Centio Consulting Group AB; Fun holiday temporary job as an occupational therapist in Älmhult municipality! - Älmhult
- **tourism**: Bartender & Servis till Pool Club & Kellys 50% - ESS Hotel Group AB; Worth entering a hotel environment - Tempest Security Sverige AB; CE Driver; Need for HAVI in Malmö - Driver service Jobbförmedling Sverige AB; Store assistant (summer job), Snabbgross Visby - Axfood Snabbgross AB; Restaurant assistant at Solgården, Sollefteå - VÄSTERNORRLAND REGION; NOVI Resort Visby is looking for Supervisor for Housekeeping - NO VI RESORT AB; Masseur/Massage therapist - Åkerblads i Tällberg AB; Machine Learning Engineer, Personalisation - Wolt Development Sverige AB
- **manufacturing**: Risk engineer in machine safety! - Framtiden i Sverige AB; Innovative designer wanted - create the solutions of the future! - GV Stars Bemanning AB; IT architect within the Production Center in Sundsvall - Försäkringskassan; Printer Offset - PAWR AB; We are looking for an experienced traverse driver! - TopWork Sweden AB; Department manager for Muskövarvet - Dala Industrisupport AB; International coordinator - Total Defense Research Institute, Foi; Warehouse worker for Apotek Hjärtat's E-pharmacy in Norrköping - Apotek Hjärtat AB
- **control_health_edu**: Psychiatric nurse/nurse mobile team, psychiatry Skövde - VÄSTRA GÖTALANDSREGIONEN; Nurse, temp - REGION UPPSALA; Nurse, Tegs elderly center - Umeå municipality; Pediatric nurse for Ofelia Vård - Ofelia Vård AB; X-ray nurse for Ofelia Vård - Ofelia Vård AB; Dental shoes! - People Personnel in Stockholm AB; Licensed Physician Specialist in General Medicine to To Care Solna Hlm - Prima Vård Sverig; Lärare i svenska/svenska som andraspråk till gymnasiumet, substitutes - ÖRNSKÖLDSVIKS KOMM

### kariera.gr

- **ev_industry**: IT Application Support Engineer; INSURANCE OFFICER; Commercial Department Clerk; Spare Parts Specialist - Spare Parts Specialist | Karenta; Receptionist / Front Office; Logistics / Workshop Support Guide; Administrative Executive of the Commercial Department; Workshop Manager
- **vehicle_retail_service**: DRIVER (B' or C' or E' category); Parts Dealer; Drivers, Escorts and Remittance Counters - Arta; Sales Executive; Reservations Manager; Car Rental Laundry Manager; Driver – Vehicle Fleet Support; Car Delivery Clerk
- **energy_fuels**: Loopi crew member; OFFICE EMPLOYEES – Fixed breakfast Hours & Bonus  📍Kallithea | ⏱ 09:00–17:00 |💰 Bonus over; CUSTOMER SERVICE OFFICER; Energy consultants -Protergia (8 hours/6 hours in the morning); Customer Service - Inclusive Position, Immediate Hiring; Customer Service for Energy Provider (Hybrid Work Model) Start 01/19; Management of Existing Clientele (6h with wages 8h - Immediate Hiring); Incoming Communications Management (Fixed Afternoon Hours) - Start 19/01 Peania
- **transport_shipping**: DRIVER (B' or C' or E' category); Sales Consultant - Neo Heraklion; Sales Consultant - Patras; Back Office / Office support; Accounting Clerk - Assistant Accountant; Parts Dealer; Procurement Back Office; FORKLIFT OPERATOR (CLARKE)
- **tourism**: TUI Hotel or Service Support Rep | Kefalonia; Newly established cocktail bar restaurant; Bartender; First Cook; First Waiter; Second Waiter; TUI Airport Rep | Local Residents - Chania Crete; TUI Hotel Rep | German or English Speaking | Kos
- **manufacturing**: RESPONSIBLE FOR THE PRODUCTION OF SPACE FRAGRANCES; Accounting Clerk - Assistant Accountant; Production Workers; Mobile Service Technician; Assistant Clerk Operator - Storekeeper; Technical Director / Production Manager; MEDICAL VISITORS; Production Supervisor
- **control_health_edu**: Nurse / Nurse HEI / TEI; TEACHER (IONIAN ISLANDS); MEDICAL VISITORS; PHARMACY SALESMEN; Teacher / Child Care - KOS; Nurse - Piraeus; APPLICATION SPECIALIST (MEDICAL EQUIPMENT OPERATOR); Nurse - Thessaloniki
