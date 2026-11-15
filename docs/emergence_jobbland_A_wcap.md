# Cluster series: jobbland, input A

**Weights transformed (cap, cut at percentile 95).** Read the shares and their intervals as a sensitivity check of the inverse-probability weights. The transformed weights are rescaled to the same board total as the inverse-probability weights, so counts and the threshold are in comparable units overall; but the per-day totals change, so read counts as approximate and compare shares and verdicts.

53,959 postings after 3,578 duplicates; 357 clusters plus noise; 0 postings without a label. Noise holds 34.3% of the postings.

Threshold: 100 weighted postings a quarter (adjusted to all calendar days of the quarter) and, as a share version, 0.10% of the quarter. Eligible = crosses the threshold in a quarter with at least 20 sampled days and its largest template group holds under 30% of its postings and at most 50% of its postings lack a title. Eligible clusters: 335 of 357.

## Coverage per quarter

| quarter | sampled days | calendar days | weighted postings (sampled days) | usable |
|---|---|---|---|---|
| 2024-Q1 | 84 | 91 | 750 | yes |
| 2024-Q2 | 90 | 91 | 5,556 | yes |
| 2024-Q3 | 92 | 92 | 16,739 | yes |
| 2024-Q4 | 92 | 92 | 145,114 | yes |
| 2025-Q1 | 84 | 90 | 89,216 | yes |
| 2025-Q2 | 81 | 91 | 10,757 | yes |
| 2025-Q3 | 90 | 92 | 7,726 | yes |
| 2025-Q4 | 92 | 92 | 31,228 | yes |
| 2026-Q1 | 90 | 90 | 166,027 | yes |
| 2026-Q2 | 91 | 91 | 146,626 | yes |
| 2026-Q3 | 64 | 64 | 73,425 | yes |

## Occupation Emergence Rate

| quarter | at or above threshold | newly crossing | at or above share threshold | newly crossing (share) | clearly above (interval C) | clearly new (below the line in every earlier quarter) | returning after a dip | clearly below now, clearly above earlier |
|---|---|---|---|---|---|---|---|---|
| 2024-Q1 | 0 | 0 | 155 | 0 | 0 | 0 | 0 | 0 |
| 2024-Q2 | 0 | 0 | 173 | 75 | 0 | 0 | 0 | 0 |
| 2024-Q3 | 14 | 14 | 234 | 49 | 3 | 3 | 0 | 0 |
| 2024-Q4 | 233 | 220 | 172 | 30 | 107 | 75 | 0 | 0 |
| 2025-Q1 | 149 | 21 | 154 | 8 | 48 | 2 | 0 | 4 |
| 2025-Q2 | 13 | 0 | 153 | 8 | 1 | 0 | 0 | 85 |
| 2025-Q3 | 1 | 0 | 182 | 10 | 1 | 0 | 0 | 97 |
| 2025-Q4 | 61 | 10 | 198 | 9 | 11 | 0 | 8 | 54 |
| 2026-Q1 | 274 | 66 | 204 | 6 | 142 | 5 | 45 | 22 |
| 2026-Q2 | 277 | 16 | 219 | 4 | 132 | 0 | 0 | 27 |
| 2026-Q3 | 161 | 1 | 218 | 2 | 56 | 0 | 0 | 34 |

Clearly above = the lower end of interval C is at or above the threshold. Clearly new = clearly above now and the upper end of interval C was below the threshold in every earlier usable quarter (with --new-rule previous: in the previous quarter only). Returning after a dip = clearly above now, wholly below in the previous quarter, but above the line in an earlier one: not an emerging occupation. The count version moves with the weighted population of the board (see the coverage table); the share version does not.

**Joint dip in 2025-Q2.** 85 of the 110 clusters that were clearly above the line earlier are wholly below it in 2025-Q2 (81 of 91 days sampled; clusters 21, 26, 27, 28, 29, 30, 47, 48, 52, 57, 66, 68, 70, 71, 74). When many clusters drop in the same quarter, suspect the quarter (thin or unusual sampling, one source missing) before reading the drops as declines, and do not read the returns the quarter after as emergence.

**Joint dip in 2025-Q3.** 97 of the 110 clusters that were clearly above the line earlier are wholly below it in 2025-Q3 (90 of 92 days sampled; clusters 21, 26, 27, 28, 29, 30, 34, 47, 48, 52, 66, 68, 70, 71, 74). When many clusters drop in the same quarter, suspect the quarter (thin or unusual sampling, one source missing) before reading the drops as declines, and do not read the returns the quarter after as emergence.

**Joint dip in 2025-Q4.** 54 of the 110 clusters that were clearly above the line earlier are wholly below it in 2025-Q4 (92 of 92 days sampled; clusters 21, 26, 28, 48, 52, 66, 68, 70, 74, 83, 90, 99, 125, 131, 132). When many clusters drop in the same quarter, suspect the quarter (thin or unusual sampling, one source missing) before reading the drops as declines, and do not read the returns the quarter after as emergence.

The first usable quarter (2024-Q1) cannot show new crossings; clusters already above the line then count as present at the start.

## Eligible clusters (largest peak first)

| cluster | taken | peak quarter | peak adjusted | peak share | first crossing | flagged | top channel | top template | HHI norm | unplaced | change vs event (95% interval) | top titles |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 99 | 461 | 2024-Q4 | 4,028 | 2.78% | 2024-Q4 | 3% | energy security 62% | 5% | 0.09 | 9% | +0.09% (-0.03% to +0.20%) | Innesäljare | Säljare - Fast månadslön - Ingen erfarenhet krävs! | Företagssäljare |
| 124 | 382 | 2026-Q1 | 3,256 | 1.96% | 2024-Q4 | 0% |  0% | 4% | 0.04 | 23% | -1.46% (-1.92% to -0.87%) | Temporary workers are wanted for work before, during and after the summer! | Summer job LS |
| 166 | 389 | 2026-Q2 | 3,192 | 2.18% | 2024-Q4 | 0% | defense 100% | 7% | 0.03 | 11% | +0.83% (+0.11% to +1.47%) | Teacher grades 4-6 | Teacher go 1-3 | Mathematics teacher grades 7-9 |
| 197 | 703 | 2026-Q1 | 2,828 | 1.70% | 2024-Q3 | 0% |  0% | 4% | 0.03 | 23% | -0.23% (-0.87% to +0.32%) |  | Specialist nurse - Experience of intensive care | Operations nurse |
| 192 | 239 | 2024-Q4 | 2,492 | 1.72% | 2024-Q4 | 0% |  0% | 3% | 0.03 | 5% | -0.00% (-0.17% to +0.17%) | Lärare åk 4-6 | Speciallärare alternativt grundskollärare ma/sv/eng åk 1-6 | Vikarier för  |
| 180 | 236 | 2024-Q4 | 2,484 | 1.71% | 2024-Q4 | 1% | defense 100% | 6% | 0.03 | 4% | +0.03% (-0.03% to +0.09%) | Sjuksköterska till GAVA Inflammation med intresse för dagvård | Allmänsjuksköterskor med e |
| 48 | 200 | 2024-Q4 | 2,280 | 1.57% | 2024-Q4 | 0% |  0% | 2% | 0.05 | 3% | +0.03% (+0.00% to +0.08%) | Personlig assistent | Engagerad personlig assistent till en man med ALS i Hässelby | Perso |
| 159 | 356 | 2026-Q2 | 1,947 | 1.33% | 2024-Q3 | 1% | reshoring 100% | 2% | 0.08 | 11% | +0.17% (-0.21% to +0.59%) | CE driver | CE Driver | CE Drivers |
| 118 | 343 | 2026-Q2 | 1,941 | 1.32% | 2024-Q4 | 0% |  0% | 11% | 0.06 | 21% | +0.13% (-0.32% to +0.65%) |  | Social secretary | Social secretary financial assistance |
| 123 | 287 | 2026-Q1 | 1,921 | 1.16% | 2025-Q1 | 1% | defense 80% | 3% | 0.01 | 20% | -0.55% (-0.96% to -0.13%) | Summer job Shop assistant | Do you want a summer job as a lockkeeper at Göta canal in 2026 |
| 115 | 347 | 2026-Q1 | 1,832 | 1.10% | 2024-Q4 | 0% |  0% | 6% | 0.06 | 19% | -0.23% (-0.66% to +0.15%) |  | Support assistant | Assistance officer |
| 183 | 158 | 2024-Q4 | 1,723 | 1.19% | 2024-Q4 | 4% | defense 70% | 3% | 0.05 | 5% | -0.00% (-0.05% to +0.03%) | Projektledare | Projektledare via AFRY Partner Network | Koordinator till NKT-projekt i Ka |
| 137 | 358 | 2026-Q1 | 1,701 | 1.02% | 2024-Q3 | 0% |  0% | 3% | 0.04 | 18% | +0.28% (-0.17% to +0.76%) | Personal Assistants Wanted For Man in Hässelby Strand | Personal Assistant Wanted in Höllv |
| 117 | 208 | 2026-Q2 | 1,652 | 1.13% | 2024-Q4 | 0% |  0% | 5% | 0.04 | 14% | +0.23% (-0.23% to +0.58%) |  | Teacher in leisure centers | Teacher in leisure homes |
| 136 | 390 | 2026-Q1 | 1,619 | 0.98% | 2024-Q3 | 0% |  0% | 4% | 0.03 | 12% | +0.17% (-0.25% to +0.60%) | Personal assistant to a sporty girl in Solna! | Personal assistant to a woman in Järfälla  |
| 204 | 182 | 2024-Q4 | 1,591 | 1.10% | 2024-Q4 | 15% | defense 78% | 3% | 0.05 | 7% | +0.02% (-0.09% to +0.11%) | Automationsingenjör | Systemingenjör | Provcellsingenjör/ Test Bed Engineer |
| 184 | 141 | 2024-Q4 | 1,566 | 1.08% | 2024-Q4 | 6% | defense 83% | 2% | 0.02 | 2% | -0.05% (-0.10% to +0.00%) | Miljöhandläggare | Enhetschef | Biträdande avdelningschef för verksamhetsstöd |
| 283 | 262 | 2026-Q1 | 1,564 | 0.94% | 2026-Q1 | 28% | defense 82% | 4% | 0.05 | 20% | -0.27% (-0.58% to +0.03%) | Commercial manager - Fastighets AB Balder | Project manager IT for our Stockholm office |  |
| 268 | 341 | 2026-Q1 | 1,488 | 0.90% | 2024-Q4 | 7% | defense 98% | 2% | 0.08 | 23% | -0.09% (-0.49% to +0.30%) |  | Marketing coordinator | Security coordinator |
| 132 | 247 | 2025-Q1 | 1,429 | 1.49% | 2024-Q4 | 0% |  0% | 1% | 0.06 | 8% | -0.04% (-0.11% to +0.04%) | Restaurangbiträde | Köksbiträde | Restaurangmedarbetare |
| 190 | 152 | 2025-Q1 | 1,408 | 1.47% | 2024-Q4 | 0% |  0% | 5% | 0.01 | 5% | +0.00% (+0.00% to +0.00%) | Timvikarier till man i Tvärålund | Undersköterskor, psykiatri, till Region Skåne inför som |
| 88 | 377 | 2026-Q1 | 1,327 | 0.80% | 2024-Q4 | 1% | energy security 100% | 1% | 0.10 | 20% | -0.07% (-0.30% to +0.20%) |  | Home cleaners | Home cleaner |
| 185 | 117 | 2025-Q1 | 1,206 | 1.26% | 2024-Q4 | 0% |  0% | 5% | 0.05 | 1% | -0.02% (-0.05% to +0.00%) | Socialsekreterare | Socialsekreterare för konsultuppdrag inom Barn och unga i Stockholms l |
| 34 | 435 | 2026-Q2 | 1,164 | 0.79% | 2024-Q3 | 0% |  0% | 7% | 0.05 | 17% | +0.04% (-0.25% to +0.34%) | Dental hygienist |  | Dental nurse |
| 154 | 199 | 2026-Q1 | 1,113 | 0.67% | 2024-Q4 | 0% |  0% | 4% | 0.04 | 22% | -0.25% (-0.46% to -0.05%) | Physiotherapist/Physical therapist |  | Agila is looking for occupational therapists |
| 321 | 339 | 2026-Q1 | 1,107 | 0.67% | 2024-Q3 | 3% | defense 62% | 1% | 0.06 | 24% | -0.04% (-0.34% to +0.21%) |  | Maintenance mechanic | Maintenance technician |
| 261 | 194 | 2026-Q1 | 1,086 | 0.65% | 2024-Q4 | 6% | defense 98% | 4% | 0.07 | 27% | -0.37% (-0.60% to -0.12%) |  | Business administrator | HR administrator |
| 178 | 99 | 2024-Q4 | 1,048 | 0.72% | 2024-Q4 | 0% |  0% | 3% | 0.04 | 7% | +0.00% (+0.00% to +0.00%) | Undersköterskor för timanställning till Villa Tjädern i Haninge | Sjuksköterska DAG tid ti |
| 156 | 145 | 2026-Q2 | 1,035 | 0.71% | 2024-Q4 | 0% |  0% | 13% | 0.04 | 16% | +0.35% (+0.11% to +0.63%) | Student/support assistants for primary school | Special teacher for adapted elementary sch |
| 174 | 123 | 2024-Q4 | 1,029 | 0.71% | 2024-Q4 | 1% | trade compliance 100% | 2% | 0.10 | 8% | +0.02% (+0.00% to +0.05%) | Kundtjänstmedarbetare | Strategisk rådgivare | Kommunikatör |
| 150 | 120 | 2026-Q2 | 1,023 | 0.70% | 2024-Q4 | 0% |  0% | 6% | 0.07 | 16% | +0.39% (+0.14% to +0.63%) | Preschool teacher to Sjupundsgatan 33 | Part-time workers for preschools in Flens municipa |
| 167 | 127 | 2026-Q1 | 1,000 | 0.60% | 2024-Q4 | 0% |  0% | 3% | 0.03 | 13% | -0.20% (-0.65% to +0.21%) |  | High school mathematics teacher | Teacher in technology and mathematics |
| 74 | 72 | 2024-Q4 | 990 | 0.68% | 2024-Q4 | 0% |  0% | 10% | 0.10 | 3% | +0.01% (-0.04% to +0.06%) | Forskningsassistent | Doktorand i maskininlärning | Doktorandplatser inom cancerepidemiolo |
| 208 | 115 | 2024-Q4 | 952 | 0.66% | 2024-Q4 | 3% | defense 53% | 2% | 0.05 | 8% | +0.07% (-0.01% to +0.17%) | Servicetekniker | Montör | Handlingskraftig och social montör med ledaregenskap! |
| 211 | 81 | 2024-Q4 | 945 | 0.65% | 2024-Q4 | 0% |  0% | 4% | 0.06 | 6% | +0.01% (-0.04% to +0.07%) | Redovisningskonsult | Redovisningsekonom | Ekonomichef |
| 209 | 90 | 2025-Q1 | 939 | 0.98% | 2024-Q4 | 0% | defense 100% | 2% | 0.06 | 4% | +0.02% (+0.00% to +0.07%) | Fordonstekniker | Skadetekniker Sandströms Center AB | Personbilstekniker |
| 303 | 180 | 2026-Q1 | 874 | 0.53% | 2024-Q3 | 4% | defense 59% | 2% | 0.05 | 14% | -0.28% (-0.58% to -0.02%) | Tire fitter | Plumbing fitter |  |
| 203 | 105 | 2024-Q4 | 865 | 0.60% | 2024-Q4 | 4% | defense 100% | 4% | 0.05 | 8% | +0.03% (-0.06% to +0.13%) | Senior Systemutvecklare | Systemutvecklare | AI/ML-utvecklare till Softhouse |
| 276 | 179 | 2026-Q1 | 815 | 0.49% | 2024-Q4 | 6% | trade compliance 52% | 12% | 0.09 | 22% | +0.05% (-0.28% to +0.40%) |  | Security officer | Investigator |
| 351 | 331 | 2026-Q1 | 802 | 0.48% | 2024-Q4 | 10% | defense 89% | 2% | 0.27 | 30% | +0.06% (-0.16% to +0.33%) |  | IT consultant | Solution Consultant |

## Clearly new clusters (interval C wholly above the threshold now, wholly below it in every earlier usable period)

Candidates for emerging occupations. Read the share in the next periods too: a real new occupation stays above the line.

| cluster | taken | first clearly new | flagged | top template | without title | eligible | top titles |
|---|---|---|---|---|---|---|---|
| 197 | 703 | 2024-Q3; stays clearly above in 9 of 9 periods from then on | 0% | 4% | 1% | eligible |  | Specialist nurse - Experience of intensive care | Operations nurse |
| 136 | 390 | 2024-Q3; stays clearly above in 5 of 9 periods from then on | 0% | 4% | 0% | eligible | Personal assistant to a sporty girl in Solna! | Personal assistant to a woman in Järfälla  |
| 284 | 348 | 2024-Q3; stays clearly above in 6 of 9 periods from then on | 0% | 1% | 0% | eligible | Danish-speaking customer service employee | Flogas is looking for regional manager for our |
| 99 | 461 | 2024-Q4; stays clearly above in 2 of 8 periods from then on | 3% | 5% | 0% | eligible | Innesäljare | Säljare - Fast månadslön - Ingen erfarenhet krävs! | Företagssäljare |
| 166 | 389 | 2024-Q4; stays clearly above in 4 of 8 periods from then on | 0% | 7% | 0% | eligible | Teacher grades 4-6 | Teacher go 1-3 | Mathematics teacher grades 7-9 |
| 192 | 239 | 2024-Q4; stays clearly above in 3 of 8 periods from then on | 0% | 3% | 0% | eligible | Lärare åk 4-6 | Speciallärare alternativt grundskollärare ma/sv/eng åk 1-6 | Vikarier för  |
| 48 | 200 | 2024-Q4; stays clearly above in 2 of 8 periods from then on | 0% | 2% | 0% | eligible | Personlig assistent | Engagerad personlig assistent till en man med ALS i Hässelby | Perso |
| 118 | 343 | 2024-Q4; stays clearly above in 5 of 8 periods from then on | 0% | 11% | 6% | eligible |  | Social secretary | Social secretary financial assistance |
| 115 | 347 | 2024-Q4; stays clearly above in 4 of 8 periods from then on | 0% | 6% | 5% | eligible |  | Support assistant | Assistance officer |
| 204 | 182 | 2024-Q4; stays clearly above in 2 of 8 periods from then on | 15% | 3% | 0% | eligible | Automationsingenjör | Systemingenjör | Provcellsingenjör/ Test Bed Engineer |
| 184 | 141 | 2024-Q4; stays clearly above in 2 of 8 periods from then on | 6% | 2% | 0% | eligible | Miljöhandläggare | Enhetschef | Biträdande avdelningschef för verksamhetsstöd |
| 268 | 341 | 2024-Q4; stays clearly above in 5 of 8 periods from then on | 7% | 2% | 10% | eligible |  | Marketing coordinator | Security coordinator |
| 132 | 247 | 2024-Q4; stays clearly above in 3 of 8 periods from then on | 0% | 1% | 0% | eligible | Restaurangbiträde | Köksbiträde | Restaurangmedarbetare |
| 190 | 152 | 2024-Q4; stays clearly above in 2 of 8 periods from then on | 0% | 5% | 0% | eligible | Timvikarier till man i Tvärålund | Undersköterskor, psykiatri, till Region Skåne inför som |
| 57 | 264 | 2024-Q4; stays clearly above in 5 of 8 periods from then on | 0% | 31% | 4% | not eligible |  | Babysitter Nanny Bromma 1-2 times a year - 2007 Nannynu AB | Babysitter |
| 185 | 117 | 2024-Q4; stays clearly above in 2 of 8 periods from then on | 0% | 5% | 0% | eligible | Socialsekreterare | Socialsekreterare för konsultuppdrag inom Barn och unga i Stockholms l |
| 261 | 194 | 2024-Q4; stays clearly above in 4 of 8 periods from then on | 6% | 4% | 5% | eligible |  | Business administrator | HR administrator |
| 178 | 99 | 2024-Q4; stays clearly above in 2 of 8 periods from then on | 0% | 3% | 0% | eligible | Undersköterskor för timanställning till Villa Tjädern i Haninge | Sjuksköterska DAG tid ti |
| 174 | 123 | 2024-Q4; stays clearly above in 2 of 8 periods from then on | 1% | 2% | 0% | eligible | Kundtjänstmedarbetare | Strategisk rådgivare | Kommunikatör |
| 150 | 120 | 2024-Q4; stays clearly above in 3 of 8 periods from then on | 0% | 6% | 0% | eligible | Preschool teacher to Sjupundsgatan 33 | Part-time workers for preschools in Flens municipa |
| 74 | 72 | 2024-Q4; stays clearly above in 1 of 8 periods from then on | 0% | 10% | 0% | eligible | Forskningsassistent | Doktorand i maskininlärning | Doktorandplatser inom cancerepidemiolo |
| 208 | 115 | 2024-Q4; stays clearly above in 3 of 8 periods from then on | 3% | 2% | 0% | eligible | Servicetekniker | Montör | Handlingskraftig och social montör med ledaregenskap! |
| 211 | 81 | 2024-Q4; stays clearly above in 2 of 8 periods from then on | 0% | 4% | 0% | eligible | Redovisningskonsult | Redovisningsekonom | Ekonomichef |
| 209 | 90 | 2024-Q4; stays clearly above in 2 of 8 periods from then on | 0% | 2% | 0% | eligible | Fordonstekniker | Skadetekniker Sandströms Center AB | Personbilstekniker |
| 203 | 105 | 2024-Q4; stays clearly above in 2 of 8 periods from then on | 4% | 4% | 0% | eligible | Senior Systemutvecklare | Systemutvecklare | AI/ML-utvecklare till Softhouse |
| 276 | 179 | 2024-Q4; stays clearly above in 4 of 8 periods from then on | 6% | 12% | 7% | eligible |  | Security officer | Investigator |
| 212 | 71 | 2024-Q4; stays clearly above in 2 of 8 periods from then on | 3% | 3% | 0% | eligible | Administratör | Ekonomiassistent | Ekonomiansvarig för anställning hos kund |
| 131 | 123 | 2024-Q4; stays clearly above in 2 of 8 periods from then on | 2% | 5% | 0% | eligible | Städare - Deltid | Städare | Vaktmästare |
| 133 | 67 | 2024-Q4; stays clearly above in 2 of 8 periods from then on | 3% | 6% | 0% | eligible | Lagermedarbetare - Deltid | Lagermedarbetare | Lagermedarbetare - extra vid behov |
| 71 | 127 | 2024-Q4; stays clearly above in 4 of 8 periods from then on | 8% | 7% | 2% | eligible |  | Doctoral student in AI and future teacher education - Royal Institute of Technology | D |
| 228 | 133 | 2024-Q4; stays clearly above in 5 of 8 periods from then on | 2% | 2% | 9% | eligible | Administrator |  | Order administrator |
| 191 | 45 | 2024-Q4; stays clearly above in 1 of 8 periods from then on | 0% | 4% | 0% | eligible | Förskollärare | Vi söker en förskollärare/rektor till två förskolor i Saltsjö-Boo och Älta |
| 189 | 49 | 2024-Q4; stays clearly above in 2 of 8 periods from then on | 0% | 6% | 0% | eligible | Rekondtekniker - Sommarjobb 2025 | Sommarjobb: Produktionstekniker till Reningsverket Pree |
| 175 | 68 | 2024-Q4; stays clearly above in 2 of 8 periods from then on | 0% | 3% | 0% | eligible | Trädgårdsarbetare | Fastighetsskötare | Markarbetare till NYAB! |
| 210 | 60 | 2024-Q4; stays clearly above in 2 of 8 periods from then on | 0% | 5% | 0% | eligible | Vi söker erfaren lackerare till kund i tenhult! | Manuellsvetsare och robotsvetsare till K |
| 216 | 135 | 2024-Q4; stays clearly above in 4 of 8 periods from then on | 0% | 9% | 0% | eligible | Nurses for home care Norra Fäladen | Nurses for the Gamla Lasarettsgatan home service | Nu |
| 350 | 193 | 2024-Q4; stays clearly above in 3 of 8 periods from then on | 41% | 2% | 4% | eligible |  | System Engineer | Security Engineer |
| 90 | 98 | 2024-Q4; stays clearly above in 2 of 8 periods from then on | 0% | 2% | 0% | eligible | Taxiförare | CE-chaufför sökes! | DHL Freight söker: CE Chaufför |
| 134 | 59 | 2024-Q4; stays clearly above in 1 of 8 periods from then on | 0% | 14% | 0% | eligible | Servitör/servitris | Servitris | Extraarbetare sökes till livsmedelsproduktion i Kävlinge! |
| 102 | 85 | 2024-Q4; stays clearly above in 2 of 8 periods from then on | 2% | 4% | 7% | eligible |  | Soccer Scout | Job coach |
| 170 | 51 | 2024-Q4; stays clearly above in 1 of 8 periods from then on | 0% | 12% | 0% | eligible | Arbetsterapeut | Fysioterapeut/Sjukgymnast | Arbetsterapeut till Villa Täby Park |
| 177 | 42 | 2024-Q4; stays clearly above in 1 of 8 periods from then on | 0% | 5% | 0% | eligible | Distriktssköterska | Distriktsläkare, Primärvårdsområde Väst, Vindelns Hälsocentral | Dist |
| 125 | 55 | 2024-Q4; stays clearly above in 1 of 8 periods from then on | 0% | 11% | 0% | eligible | Butiksmedarbetare, extra- och sommarjobb | Inventeringsuppdrag i butik | Inventeringsuppdr |
| 179 | 53 | 2024-Q4; stays clearly above in 1 of 8 periods from then on | 0% | 6% | 0% | eligible | Capio Ögonklinik söker specialistläkare till vår öppenvårdsmottagning | Specialistläkare i |
| 199 | 44 | 2024-Q4; stays clearly above in 2 of 8 periods from then on | 4% | 5% | 0% | eligible | Maskinoperatör | Maskinoperatör -Ettiketto Arlöv | CNC-operatör |
| 326 | 135 | 2024-Q4; stays clearly above in 3 of 8 periods from then on | 3% | 1% | 2% | eligible | First Line Support | IT Support Technician | Support technician |
| 70 | 113 | 2024-Q4; stays clearly above in 3 of 8 periods from then on | 5% | 6% | 1% | eligible | Postdoctoral fellow in Distributed machine learning and optimization | Postdoc position |  |
| 105 | 133 | 2024-Q4; stays clearly above in 4 of 8 periods from then on | 1% | 3% | 5% | eligible | Receptionist |  | Receptionist at Gullmarsstrand Hotel |
| 52 | 121 | 2024-Q4; stays clearly above in 4 of 8 periods from then on | 5% | 2% | 4% | eligible | Production manager | Production Manager |  |
| 338 | 154 | 2024-Q4; stays clearly above in 3 of 8 periods from then on | 0% | 1% | 5% | eligible |  | Financial assistant | Financial Assistant |
| 265 | 121 | 2024-Q4; stays clearly above in 4 of 8 periods from then on | 4% | 2% | 1% | eligible | Area Sales Manager Scandinavia | Counsel, Business & Legal Affairs - Nordics - Netflix | B |
| 267 | 137 | 2024-Q4; stays clearly above in 4 of 8 periods from then on | 0% | 8% | 7% | eligible |  | Service advisor | Service Advisor |
| 269 | 114 | 2024-Q4; stays clearly above in 4 of 8 periods from then on | 3% | 4% | 4% | eligible | Environmental and health protection inspector |  | Environmental consultant |
| 301 | 145 | 2024-Q4; stays clearly above in 5 of 8 periods from then on | 12% | 2% | 5% | eligible |  | Contract Manager | Product Marketing Manager |
| 29 | 126 | 2024-Q4; stays clearly above in 5 of 8 periods from then on | 3% | 2% | 2% | eligible | Service technician | Service Technician | Service technician Stockholm |
| 121 | 95 | 2024-Q4; stays clearly above in 3 of 8 periods from then on | 0% | 8% | 0% | eligible | Home cleaner - Hemfrid Gothenburg | Window cleaners 2026 - Hemfrid Stockholm | Cleaners fo |
| 26 | 85 | 2024-Q4; stays clearly above in 2 of 8 periods from then on | 2% | 2% | 2% | eligible | HR Business Partner | People Operations Partner | People Business Partner |
| 236 | 56 | 2024-Q4; stays clearly above in 2 of 8 periods from then on | 0% | 7% | 0% | eligible | Sales manager Delicatessen - Stora Coop Sundby park - Coop | Salesperson - Stora Coop Hägg |
| 278 | 85 | 2024-Q4; stays clearly above in 1 of 8 periods from then on | 0% | 5% | 1% | eligible | Senior UX/UI Designer | UX-Designer | Senior UX/UI designer |
| 66 | 82 | 2024-Q4; stays clearly above in 2 of 8 periods from then on | 0% | 5% | 6% | eligible |  | Laboratory assistant | Biomedicinsk analytiker |
| 255 | 87 | 2024-Q4; stays clearly above in 2 of 8 periods from then on | 2% | 2% | 0% | eligible | Account manager | Account Manager B2B | Sales Executive Account Manager |
| 273 | 105 | 2024-Q4; stays clearly above in 4 of 8 periods from then on | 9% | 2% | 5% | eligible |  | Sourcing Manager | Purchasing manager |
| 83 | 76 | 2024-Q4; stays clearly above in 2 of 8 periods from then on | 0% | 12% | 1% | eligible | Pizzabagare | Pizza Bagare | Servispersonal till Pinchos X |
| 330 | 88 | 2024-Q4; stays clearly above in 1 of 8 periods from then on | 0% | 2% | 6% | eligible | Business Controller |  | Group Business Controller |
| 241 | 144 | 2024-Q4; stays clearly above in 2 of 8 periods from then on | 0% | 44% | 1% | not eligible | Brand Merchandiser | Shop assistant 70%, temp, Stadium Outlet Borås | Visual Merchandiser  |
| 285 | 120 | 2024-Q4; stays clearly above in 2 of 8 periods from then on | 15% | 6% | 1% | eligible | Embedded Software Developer | Embedded developer | Embedded Developer |
| 21 | 42 | 2024-Q4; stays clearly above in 1 of 8 periods from then on | 0% | 19% | 0% | eligible | Leader Jungle Gym - Spread the joy of movement for children 2-6 years old in Kungsbacka HT |
| 345 | 130 | 2024-Q4; stays clearly above in 1 of 8 periods from then on | 0% | 4% | 1% | eligible | Financial consultant within Dynamics 365 for Operations at Columbus | Solution Architect A |
| 223 | 59 | 2024-Q4; stays clearly above in 2 of 8 periods from then on | 8% | 5% | 5% | eligible | Operator | Organist |  |
| 304 | 122 | 2024-Q4; stays clearly above in 2 of 8 periods from then on | 13% | 9% | 1% | eligible | Senior Project Manager | Senior project manager | Scrum Master |
| 344 | 124 | 2024-Q4; stays clearly above in 1 of 8 periods from then on | 23% | 3% | 2% | eligible | Enterprise Architect | SAP Solution Architect | Cloud Architect |
| 256 | 78 | 2024-Q4; stays clearly above in 2 of 8 periods from then on | 3% | 4% | 10% | eligible |  | Legal Counsel | Jurist |
| 253 | 76 | 2024-Q4; stays clearly above in 1 of 8 periods from then on | 20% | 4% | 0% | eligible | Mechanical Engineer | Mechanical engineer | FEM- & Hållf engineer |
| 227 | 63 | 2024-Q4; stays clearly above in 1 of 8 periods from then on | 1% | 3% | 2% | eligible | Application Engineer | Application specialist | Application Manager |
| 28 | 46 | 2024-Q4; stays clearly above in 1 of 8 periods from then on | 4% | 4% | 7% | eligible | Controller |  | Arrival Controller at Grid Automation Products |
| 47 | 82 | 2024-Q4; stays clearly above in 1 of 8 periods from then on | 12% | 2% | 0% | eligible | Software Engineer | Software Engineer till SJ AB | Program engineer for Vattenfall Eldistr |
| 336 | 67 | 2024-Q4; stays clearly above in 1 of 8 periods from then on | 0% | 3% | 1% | eligible | Financial Controller | Group Financial Controller | Senior Financial Controller |
| 248 | 60 | 2024-Q4; stays clearly above in 1 of 8 periods from then on | 4% | 15% | 3% | eligible | Group Manager | Group manager |  |
| 123 | 287 | 2025-Q1; stays clearly above in 4 of 7 periods from then on | 1% | 3% | 0% | eligible | Summer job Shop assistant | Do you want a summer job as a lockkeeper at Göta canal in 2026 |
| 240 | 104 | 2025-Q1; stays clearly above in 2 of 7 periods from then on | 0% | 26% | 0% | eligible | Store employees (summer jobs), Willys Home Ulricehamn C | Store assistant (summer job), Wi |
| 10 | 44 | 2026-Q1; stays clearly above in 1 of 3 periods from then on | 0% | 50% | 2% | not eligible | Almia is looking for a nurse for Örnsköldsvik | Almia is looking for a nurse for Kalmar |  |
| 277 | 53 | 2026-Q1; stays clearly above in 2 of 3 periods from then on | 0% | 47% | 0% | not eligible | Head (probation inspector) for the probation service in northern Norrland | Head (Prison S |
| 282 | 55 | 2026-Q1; stays clearly above in 2 of 3 periods from then on | 0% | 25% | 0% | eligible | Department Manager Workplace Development and Service to Uppsala Municipality | For those w |
| 205 | 112 | 2026-Q1; stays clearly above in 2 of 3 periods from then on | 0% | 13% | 4% | eligible |  | Shop assistant, fish & delicatessen, City Gross Hyllie | Shop assistant, cashier/front  |
| 234 | 50 | 2026-Q1; stays clearly above in 1 of 3 periods from then on | 8% | 4% | 2% | eligible | Service Manager | Service manager | Service Delivery Manager |

## Returning after a dip (not counted as new)

Clearly above the line now and wholly below it in the previous quarter, but clearly above it in an earlier quarter, or with an interval that reaches the line there: a gap in the series, not a new occupation.

| cluster | taken | returns | flagged | top template | without title | eligible | top titles |
|---|---|---|---|---|---|---|---|
| 124 | 382 | returns 2025-Q4; interval C reaches the line in 2024-Q4, 2025-Q1, 2025-Q2 | 0% | 4% | 0% | eligible | Temporary workers are wanted for work before, during and after the summer! | Summer job LS |
| 123 | 287 | returns 2025-Q4; clearly above earlier in 2025-Q1; interval C reaches the line in 2025-Q2 | 1% | 3% | 0% | eligible | Summer job Shop assistant | Do you want a summer job as a lockkeeper at Göta canal in 2026 |
| 88 | 377 | returns 2025-Q4; clearly above earlier in 2024-Q4; interval C reaches the line in 2024-Q2, 2024-Q3, 2025-Q1, 2025-Q2 | 1% | 1% | 5% | eligible |  | Home cleaners | Home cleaner |
| 34 | 435 | returns 2025-Q4; clearly above earlier in 2024-Q4, 2025-Q1; interval C reaches the line in 2024-Q3, 2025-Q2 | 0% | 7% | 2% | eligible | Dental hygienist |  | Dental nurse |
| 351 | 331 | returns 2025-Q4; clearly above earlier in 2024-Q4, 2025-Q1; interval C reaches the line in 2024-Q3, 2025-Q2 | 10% | 2% | 4% | eligible |  | IT consultant | Solution Consultant |
| 296 | 226 | returns 2025-Q4; clearly above earlier in 2024-Q4, 2025-Q1; interval C reaches the line in 2024-Q3 | 6% | 2% | 4% | eligible | Business Analyst |  | Data Analyst |
| 14 | 60 | returns 2025-Q4; interval C reaches the line in 2024-Q4 | 0% | 5% | 52% | not eligible |  | Personal Assistant | Personal Assistant Gothenburg |
| 29 | 126 | returns 2025-Q4; clearly above earlier in 2024-Q4; interval C reaches the line in 2025-Q1 | 3% | 2% | 2% | eligible | Service technician | Service Technician | Service technician Stockholm |
| 156 | 145 | returns 2026-Q1; interval C reaches the line in 2024-Q4, 2025-Q1 | 0% | 13% | 0% | eligible | Student/support assistants for primary school | Special teacher for adapted elementary sch |
| 150 | 120 | returns 2026-Q1; clearly above earlier in 2024-Q4; interval C reaches the line in 2025-Q1 | 0% | 6% | 0% | eligible | Preschool teacher to Sjupundsgatan 33 | Part-time workers for preschools in Flens municipa |
| 303 | 180 | returns 2026-Q1; clearly above earlier in 2024-Q4; interval C reaches the line in 2024-Q3 | 4% | 2% | 2% | eligible | Tire fitter | Plumbing fitter |  |
| 196 | 148 | returns 2026-Q1; interval C reaches the line in 2024-Q4, 2025-Q1 | 0% | 5% | 0% | eligible | Psychologist, legitimate, child and adolescent psychiatry, Lycksele | Psychologist, legiti |
| 334 | 140 | returns 2026-Q1; interval C reaches the line in 2024-Q4, 2025-Q1 | 1% | 4% | 3% | eligible | Concrete worker | Construction workers |  |
| 129 | 72 | returns 2026-Q1; interval C reaches the line in 2025-Q1 | 0% | 10% | 0% | eligible | ARE YOU LOOKING FOR A NICE SUMMER JOB? THEN APPLY AS A PERSONAL ASSISTANT WITH US | Summer |
| 13 | 83 | returns 2026-Q1; interval C reaches the line in 2024-Q4, 2025-Q1 | 0% | 22% | 1% | eligible | Tire changer | Tire shifters | Tire changer - SIMPLEX |
| 240 | 104 | returns 2026-Q1; clearly above earlier in 2025-Q1 | 0% | 26% | 0% | eligible | Store employees (summer jobs), Willys Home Ulricehamn C | Store assistant (summer job), Wi |
| 70 | 113 | returns 2026-Q1; clearly above earlier in 2024-Q4; interval C reaches the line in 2025-Q1 | 5% | 6% | 1% | eligible | Postdoctoral fellow in Distributed machine learning and optimization | Postdoc position |  |
| 39 | 82 | returns 2026-Q1; interval C reaches the line in 2024-Q4 | 0% | 9% | 0% | eligible | Shop assistant | Shop assistant with a visual focus | Shop assistant 50% |
| 52 | 121 | returns 2026-Q1; clearly above earlier in 2024-Q4; interval C reaches the line in 2025-Q1 | 5% | 2% | 4% | eligible | Production manager | Production Manager |  |
| 340 | 115 | returns 2026-Q1; interval C reaches the line in 2024-Q4, 2025-Q1 | 0% | 2% | 0% | eligible | Carpenters are sought | Self-propelled carpenter wanted | Carpenter / Construction worker  |
| 67 | 80 | returns 2026-Q1; interval C reaches the line in 2024-Q4, 2025-Q1, 2025-Q2 | 0% | 11% | 1% | eligible | Research assistant | Researcher in Electromagnetic Theory | Assistant researcher in dement |
| 176 | 71 | returns 2026-Q1; interval C reaches the line in 2024-Q3 | 7% | 3% | 1% | eligible | Vehicle assembler | Assembly Technician | Öhlins is looking for assemblers for Upplands Vä |
| 108 | 75 | returns 2026-Q1; interval C reaches the line in 2024-Q4, 2025-Q1 | 0% | 33% | 3% | not eligible | Treatment assistant who wants to contribute to vital change |  | Social pedagogue |
| 352 | 170 | returns 2026-Q1; clearly above earlier in 2024-Q4; interval C reaches the line in 2024-Q3, 2025-Q1, 2025-Q2 | 17% | 3% | 1% | eligible | Mechanical designer | Senior Mechanical Engineer | Electrical Design Engineer |
| 149 | 67 | returns 2026-Q1; interval C reaches the line in 2024-Q4 | 0% | 7% | 1% | eligible | Substitutes for preschool | Hourly substitutes for Östervångsskolan, Lund - Special Educat |
| 163 | 65 | returns 2026-Q1; interval C reaches the line in 2024-Q4, 2025-Q1 | 1% | 6% | 2% | eligible | Teacher, Swedish, Swedish as Second Language | Teacher, Swedish, Swedish as Second Languag |
| 288 | 109 | returns 2026-Q1; interval C reaches the line in 2024-Q4 | 3% | 5% | 0% | eligible | Installation electrician for Sweden's leading solar company - Svea Solar Sweden | Metso is |
| 58 | 78 | returns 2026-Q1; interval C reaches the line in 2024-Q4, 2025-Q1 | 0% | 1% | 5% | eligible | Property manager |  | Property Manager |
| 17 | 144 | returns 2026-Q1; interval C reaches the line in 2024-Q4, 2025-Q1 | 2% | 6% | 0% | eligible | Seller | Seller Stockholm | Seller to Fibio |
| 26 | 85 | returns 2026-Q1; clearly above earlier in 2024-Q4; interval C reaches the line in 2025-Q1 | 2% | 2% | 2% | eligible | HR Business Partner | People Operations Partner | People Business Partner |
| 139 | 55 | returns 2026-Q1; interval C reaches the line in 2024-Q3, 2024-Q4 | 0% | 5% | 0% | eligible | Warehouse worker - Extra job | Extra job in warehouse in Alingsås | Warehouse workers want |
| 116 | 51 | returns 2026-Q1; interval C reaches the line in 2024-Q4 | 0% | 4% | 0% | eligible | Active and fun extra job as a personal assistant! | Extra work as a personal assistant in  |
| 7 | 60 | returns 2026-Q1; interval C reaches the line in 2024-Q4, 2025-Q1 | 0% | 5% | 0% | eligible | Personal assistant | Personal assistant wanted in Gällivare | Personal assistant Lund |
| 242 | 61 | returns 2026-Q1; interval C reaches the line in 2024-Q4 | 0% | 7% | 0% | eligible | We are looking for shop assistants for our store in Kalmar - 5 hours a week - Hunkemöller  |
| 22 | 60 | returns 2026-Q1; interval C reaches the line in 2024-Q4, 2025-Q1 | 7% | 7% | 2% | eligible | Electrician | Electrician for Revent International | Electrician for Halmstad |
| 236 | 56 | returns 2026-Q1; clearly above earlier in 2024-Q4; interval C reaches the line in 2025-Q1 | 0% | 7% | 0% | eligible | Sales manager Delicatessen - Stora Coop Sundby park - Coop | Salesperson - Stora Coop Hägg |
| 158 | 52 | returns 2026-Q1; interval C reaches the line in 2024-Q4, 2025-Q1 | 0% | 4% | 6% | eligible |  | Sports teacher | Swimming teacher |
| 104 | 46 | returns 2026-Q1; interval C reaches the line in 2025-Q1 | 1% | 4% | 0% | eligible | Summer job | Summer job camp leader | Summer job 2026 |
| 31 | 51 | returns 2026-Q1; interval C reaches the line in 2024-Q4, 2025-Q1 | 0% | 6% | 0% | eligible | Nurses for Råsvägen in Tranås | Nurses for hourly employment, Hudiksvall | Nurse eyes |
| 273 | 105 | returns 2026-Q1; clearly above earlier in 2024-Q4; interval C reaches the line in 2025-Q1 | 9% | 2% | 5% | eligible |  | Sourcing Manager | Purchasing manager |
| 95 | 50 | returns 2026-Q1; interval C reaches the line in 2024-Q4 | 0% | 4% | 0% | eligible | School nurse | School nurse who wants to develop the school with us | Do you want to work  |
| 64 | 52 | returns 2026-Q1; interval C reaches the line in 2024-Q4 | 0% | 10% | 4% | eligible | Researcher | Scientist | Formulation Scientist |
| 264 | 97 | returns 2026-Q1; interval C reaches the line in 2024-Q4, 2025-Q1 | 1% | 5% | 1% | eligible | Meeting booker | Meeting Booker - Vasastan | Customer booker for media companies |
| 223 | 59 | returns 2026-Q1; clearly above earlier in 2024-Q4; interval C reaches the line in 2025-Q1 | 8% | 5% | 5% | eligible | Operator | Organist |  |
| 81 | 49 | returns 2026-Q1; interval C reaches the line in 2024-Q4 | 0% | 12% | 0% | eligible | District nurse | District nurse for ASiH Täby | Almia is looking for a district nurse for  |
| 314 | 87 | returns 2026-Q1; interval C reaches the line in 2024-Q4, 2025-Q1 | 8% | 2% | 3% | eligible | Machine Learning Engineer | AI Engineer | Software developer with an interest in AI |
| 75 | 50 | returns 2026-Q1; interval C reaches the line in 2024-Q4, 2025-Q1 | 0% | 16% | 4% | eligible | Nurse for pediatric X -ray | X -ray nurse | X-ray nurse |
| 325 | 74 | returns 2026-Q1; interval C reaches the line in 2024-Q4, 2025-Q1 | 12% | 4% | 3% | eligible | IT technician | Network technicians wanted for Tele2 | Network technicians |
| 86 | 57 | returns 2026-Q1; interval C reaches the line in 2025-Q1 | 0% | 4% | 0% | eligible | Dental hygienist to the unit for jaw surgery, Sunderby hospital | Nurse to the Orthopedic  |
| 130 | 83 | returns 2026-Q1; interval C reaches the line in 2024-Q4 | 0% | 4% | 1% | eligible | Serving staff | Staff wanted | Serving staff wanted |
| 54 | 44 | returns 2026-Q1; interval C reaches the line in 2025-Q1 | 0% | 7% | 0% | eligible | Store manager | Store manager for Willys Umeå Avion | Store manager for the Candy Factory  |
| 214 | 48 | returns 2026-Q1; interval C reaches the line in 2024-Q4, 2025-Q3 | 0% | 21% | 0% | eligible | Almia is looking for a nurse for Östersund municipality | Nurse Malmö Health Center | Ambu |
| 207 | 60 | returns 2026-Q1; interval C reaches the line in 2024-Q4, 2025-Q1 | 0% | 20% | 13% | eligible |  | Store Manager | Department Store Manager Motonet Umeå |

## Largest rise in share, first usable period (2024-Q1) to last (2026-Q3)

Both ends are weighted shares of the whole board with interval C. Clear = the lower end at the last period is above the upper end at the first.

| cluster | taken | share first (interval C) | share last (interval C) | clear | flagged | top template | without title | eligible | top titles |
|---|---|---|---|---|---|---|---|---|---|
| 137 | 358 | 0.28% (0.00% to 0.67%) | 1.72% (1.32% to 2.07%) | yes | 0% | 3% | 0% | eligible | Personal Assistants Wanted For Man in Hässelby Strand | Personal Assistant Wante |
| 136 | 390 | 0.00% (0.00% to 0.00%) | 1.19% (0.92% to 1.52%) | yes | 0% | 4% | 0% | eligible | Personal assistant to a sporty girl in Solna! | Personal assistant to a woman in |
| 197 | 703 | 0.32% (0.00% to 1.06%) | 1.49% (1.06% to 1.99%) | yes | 0% | 4% | 1% | eligible |  | Specialist nurse - Experience of intensive care | Operations nurse |
| 115 | 347 | 0.43% (0.00% to 1.14%) | 1.48% (1.17% to 1.78%) | yes | 0% | 6% | 5% | eligible |  | Support assistant | Assistance officer |
| 118 | 343 | 0.14% (0.00% to 0.44%) | 1.15% (0.68% to 1.64%) | yes | 0% | 11% | 6% | eligible |  | Social secretary | Social secretary financial assistance |
| 166 | 389 | 0.14% (0.00% to 0.42%) | 0.94% (0.63% to 1.20%) | yes | 0% | 7% | 0% | eligible | Teacher grades 4-6 | Teacher go 1-3 | Mathematics teacher grades 7-9 |
| 283 | 262 | 0.28% (0.00% to 0.62%) | 1.04% (0.72% to 1.59%) | yes | 28% | 4% | 0% | eligible | Commercial manager - Fastighets AB Balder | Project manager IT for our Stockholm |
| 88 | 377 | 0.14% (0.00% to 0.42%) | 0.82% (0.46% to 1.21%) | yes | 1% | 1% | 5% | eligible |  | Home cleaners | Home cleaner |
| 156 | 145 | 0.00% (0.00% to 0.00%) | 0.61% (0.42% to 0.79%) | yes | 0% | 13% | 0% | eligible | Student/support assistants for primary school | Special teacher for adapted elem |
| 172 | 277 | 0.14% (0.00% to 0.45%) | 0.67% (0.49% to 0.92%) | yes | 1% | 1% | 1% | eligible |  | Baker/Confectioner | Chef is sought |
| 57 | 264 | 0.28% (0.00% to 0.65%) | 0.81% (0.53% to 1.18%) | no | 0% | 31% | 4% | not eligible |  | Babysitter Nanny Bromma 1-2 times a year - 2007 Nannynu AB | Babysitter |
| 121 | 95 | 0.00% (0.00% to 0.00%) | 0.53% (0.31% to 0.74%) | yes | 0% | 8% | 0% | eligible | Home cleaner - Hemfrid Gothenburg | Window cleaners 2026 - Hemfrid Stockholm | C |
| 117 | 208 | 0.00% (0.00% to 0.00%) | 0.51% (0.33% to 0.77%) | yes | 0% | 5% | 5% | eligible |  | Teacher in leisure centers | Teacher in leisure homes |
| 119 | 119 | 0.00% (0.00% to 0.00%) | 0.50% (0.18% to 0.81%) | yes | 3% | 12% | 6% | eligible |  | Unit manager for elderly care | Unit managers for special housing |
| 154 | 199 | 0.00% (0.00% to 0.00%) | 0.50% (0.32% to 0.68%) | yes | 0% | 4% | 3% | eligible | Physiotherapist/Physical therapist |  | Agila is looking for occupational therap |

## Clusters with the largest flagged share (at least 10 flagged postings taken, not template-dominated)

| cluster | taken | flagged taken | flagged share (weighted) | top channel | peak share | first crossing | top template | HHI norm | unplaced | change vs event (95% interval) | top titles |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 350 | 193 | 61 | 41% | defense 94% | 0.36% | 2024-Q4 | 2% | 0.15 | 26% | -0.01% (-0.20% to +0.20%) |  | System Engineer | Security Engineer |
| 266 | 82 | 27 | 36% | defense 43% | 0.11% | 2025-Q1 | 5% | 0.10 | 35% | -0.06% (-0.19% to +0.03%) | Process Engineer |  | Material Engineer |
| 283 | 262 | 81 | 28% | defense 82% | 0.94% | 2026-Q1 | 4% | 0.05 | 20% | -0.27% (-0.58% to +0.03%) | Commercial manager - Fastighets AB Balder | Project manager IT for our Stockholm office |  |
| 61 | 42 | 14 | 28% | defense 93% | 0.10% | 2026-Q1 | 7% | 0.10 | 32% | +0.02% (-0.05% to +0.09%) | Technical Project Manager | Technical Project Manager in Construction & Product Developmen |
| 37 | 45 | 13 | 24% | defense 76% | 0.09% | 2026-Q1 | 4% | 0.13 | 36% | +0.03% (-0.07% to +0.15%) | Operational buyer | Operational Buyer | Operational buyer to Saab! |
| 356 | 60 | 19 | 23% | defense 76% | 0.09% | 2026-Q2 | 3% | 0.18 | 26% | +0.08% (-0.01% to +0.18%) | Electronics engineer | Electronics Engineer | E-mobility Engineer - Knightec |
| 262 | 60 | 13 | 23% | energy security 100% | 0.23% | 2025-Q1 | 13% | 0.11 | 32% | -0.15% (-0.37% to +0.04%) | Manager Civil Administration to Vattenfall - Sustainable Power for generations | Technical |
| 344 | 124 | 14 | 23% | defense 53% | 0.19% | 2024-Q4 | 3% | 0.22 | 21% | -0.00% (-0.09% to +0.09%) | Enterprise Architect | SAP Solution Architect | Cloud Architect |
| 138 | 41 | 10 | 21% | energy security 51% | 0.12% | 2026-Q1 | 10% | 0.18 | 28% | -0.07% (-0.19% to +0.04%) | Calculator facility | Calculation engineer strength theory FEM for nuclear power to TÜV NO |
| 253 | 76 | 20 | 20% | defense 68% | 0.18% | 2024-Q4 | 4% | 0.10 | 13% | -0.06% (-0.19% to +0.04%) | Mechanical Engineer | Mechanical engineer | FEM- & Hållf engineer |
| 355 | 58 | 10 | 17% | defense 61% | 0.09% | 2024-Q4 | 3% | 0.52 | 26% | +0.05% (-0.02% to +0.12%) | System Design Engineer | R&D Senior Engineer | Senior Electrical Engineer |
| 352 | 170 | 22 | 17% | defense 92% | 0.29% | 2024-Q4 | 3% | 0.02 | 15% | -0.06% (-0.21% to +0.09%) | Mechanical designer | Senior Mechanical Engineer | Electrical Design Engineer |
| 232 | 70 | 16 | 17% | defense 82% | 0.19% | 2024-Q4 | 4% | 0.10 | 26% | -0.06% (-0.24% to +0.08%) | Production technician | Production techniques |  |
| 342 | 109 | 22 | 16% | energy security 68% | 0.23% | 2024-Q4 | 6% | 0.03 | 22% | -0.04% (-0.23% to +0.11%) | Project manager Elkraft | Hello Project Manager Electricity! | Project manager within Ener |
| 204 | 182 | 30 | 15% | defense 78% | 1.10% | 2024-Q4 | 3% | 0.05 | 7% | +0.02% (-0.09% to +0.11%) | Automationsingenjör | Systemingenjör | Provcellsingenjör/ Test Bed Engineer |
| 285 | 120 | 18 | 15% | defense 100% | 0.21% | 2024-Q4 | 6% | 0.17 | 35% | +0.04% (-0.07% to +0.13%) | Embedded Software Developer | Embedded developer | Embedded Developer |
| 294 | 223 | 33 | 15% | energy security 60% | 0.47% | 2024-Q3 | 2% | 0.06 | 19% | -0.02% (-0.23% to +0.19%) | Service electrician |  | Installation electrician |
| 291 | 108 | 15 | 14% | defense 66% | 0.24% | 2024-Q4 | 2% | 0.06 | 27% | +0.20% (+0.10% to +0.33%) | Quality Engineer |  | Quality engineer |
| 109 | 125 | 18 | 13% | defense 53% | 0.16% | 2024-Q4 | 6% | 0.08 | 23% | +0.02% (-0.11% to +0.16%) | Automation engineer | Automation Engineer | Automation engineer with experience in PLC pro |
| 301 | 145 | 13 | 12% | defense 70% | 0.29% | 2024-Q4 | 2% | 0.15 | 21% | +0.24% (+0.09% to +0.42%) |  | Contract Manager | Product Marketing Manager |
| 202 | 180 | 18 | 12% | defense 91% | 0.41% | 2024-Q4 | 1% | 0.04 | 23% | +0.02% (-0.19% to +0.23%) | Production planner |  | Project Planner |
| 343 | 232 | 24 | 11% | defense 83% | 0.48% | 2024-Q4 | 1% | 0.13 | 22% | -0.10% (-0.31% to +0.13%) |  | Construction manager | Experienced project managers |
| 114 | 123 | 13 | 10% | defense 73% | 0.25% | 2024-Q4 | 2% | 0.03 | 17% | +0.13% (-0.04% to +0.33%) | Head of department |  | LSS manager |
| 42 | 98 | 12 | 10% | defense 100% | 0.26% | 2024-Q4 | 9% | 0.09 | 41% | -0.05% (-0.16% to +0.06%) |  | PRISMA Security is looking for Security Guards | Lifeguard |
| 351 | 331 | 25 | 10% | defense 89% | 0.48% | 2024-Q4 | 2% | 0.27 | 30% | +0.06% (-0.16% to +0.33%) |  | IT consultant | Solution Consultant |

## Crossing the threshold but not eligible (one template or mostly title-less)

| cluster | taken | peak adjusted | top template | without title | unplaced | top titles |
|---|---|---|---|---|---|---|
| 57 | 264 | 1,407 | 31% | 4% | 25% |  | Babysitter Nanny Bromma 1-2 times a year - 2007 Nannynu AB | Babysitter |
| 10 | 44 | 576 | 50% | 2% | 41% | Almia is looking for a nurse for Örnsköldsvik | Almia is looking for a nurse for Kalmar |  |
| 277 | 53 | 435 | 47% | 0% | 24% | Head (probation inspector) for the probation service in northern Norrland | Head (Prison S |
| 108 | 75 | 431 | 33% | 3% | 14% | Treatment assistant who wants to contribute to vital change |  | Social pedagogue |
| 14 | 60 | 431 | 5% | 52% | 64% |  | Personal Assistant | Personal Assistant Gothenburg |
| 241 | 144 | 312 | 44% | 1% | 19% | Brand Merchandiser | Shop assistant 70%, temp, Stadium Outlet Borås | Visual Merchandiser  |
| 77 | 67 | 238 | 43% | 0% | 26% | Ica Kvantum Liljeholmen is looking for shop assistants for the Colonial department | Specs |
| 85 | 54 | 196 | 33% | 7% | 26% | Licensed Optician for Synoptics |  | Licensed Optician |
| 243 | 60 | 184 | 32% | 0% | 16% | Store employee, cashier/checkout, Willys Södertälje Vasa | Store employees, cash/checkout, |
| 147 | 55 | 173 | 58% | 0% | 20% | DHL Freight is looking for: Site Manager DHL Jönköping | DHL Freight is looking for: Drive |
| 53 | 79 | 165 | 46% | 0% | 20% | Car mechanic | Car mechanic wanted! | Car mechanic wanted immediately for Kalmar |
| 106 | 50 | 144 | 30% | 6% | 20% | Leg. Nurse | Leg. Nurse - Autumn 2026 | Leg. nurse |
| 239 | 44 | 132 | 39% | 0% | 13% | Store employee, team fresh, Willys Malmö Emporia | Store employee, team fresh, Willys Habo |

## Reading notes

- Report interval C (weeks redrawn) when judging a change; A is optimistic when postings of a day are clumped.
- Adjusted counts assume unsampled days resemble sampled ones; quarters with few sampled days are not used for crossings.
- HHI uses placed postings only; read it with the unplaced share and the number of placed postings (data/cluster/hhi_*.csv).
- Baseline windows are the --window-days days before and from the event (default 90), the same length on both sides; check the coverage of each window before reading a difference.
