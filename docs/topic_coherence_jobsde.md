# Topic coherence (C_NPMI) and topic diversity of the clusters: jobsde

Reference corpus: 12,243 titles with a title (boolean document co-occurrence, one title = one document). Top 10 words per cluster by class-based tf-idf; clusters with at least 20 titles; diversity over the top 25 words. NPMI is -1 when two words never occur together and +1 when they always do.

| input | clusters | noise (postings with a title) | median C_NPMI | mean C_NPMI weighted by postings | topic diversity |
|---|---|---|---|---|---|
| A | 71 | 27.6% | -0.314 | -0.186 | 0.749 |
| Dv2ls08 | 92 | 24.5% | -0.416 | -0.348 | 0.682 |
| Dv3ls08 | 73 | 35.5% | -0.223 | -0.166 | 0.756 |

### A: the 10 clusters with the lowest C_NPMI

| cluster | titles | C_NPMI | top words |
|---|---|---|---|
| 34 | 69 | -0.929 | assistenz teamassistenz geschäftsführung serviceassistent diätassistent geschäftsleitung serviceassistenz teamassistent projektassistenz marketingassistenz |
| 30 | 115 | -0.861 | teamleitung filialleitung teamleiter abteilungsleiter filialleiter reinigung gebäudereinigung führungskraft filiale leiter |
| 38 | 42 | -0.844 | immobilienkaufmann immobilienkauffrau immobilienmakler kapitalanlagen immobilienverwalter frau immobilienkoordinator immobilienberater immobilienmanager finanzierung |
| 26 | 116 | -0.816 | reinigungskraft hausmeister haustechniker cleaner minijob teilzeit glasreiniger hauswirtschaftskraft gesellen reinigungskräfte |
| 22 | 48 | -0.808 | serviceberater kundenberater automobilverkäufer automobil verkaufsberater vertriebsaktivitäten neu marke premium textile |
| 29 | 71 | -0.662 | stellvertretende leitung pflegedienstleitung fachbereichsleitung stellvertretender stationsleitung abteilung amtsleitung kindertagesstätte unseren |
| 37 | 62 | -0.653 | personalreferent referent woche fundraising stunden recruiter std generalist unterstützerkommunikation sekretariat |
| 35 | 113 | -0.645 | pflegefachkraft pflegefachfrau pflegefachkräfte pflege pflegefachmann intensivpflege anästhesie pflegehelfer pflegekraft interdisziplinäre |
| 51 | 41 | -0.628 | resources partner human talent generalist business recruiting recruiter speaker acquisition |
| 52 | 188 | -0.582 | sachbearbeiter sachbearbeitung personalsachbearbeiter sachbearbeiterin verwaltungsfachangestellte aufgabenbereich einkauf verwaltungsfachangestellter verwaltung zivil |

### Dv2ls08: the 10 clusters with the lowest C_NPMI

| cluster | titles | C_NPMI | top words |
|---|---|---|---|
| 75 | 45 | -1.000 | hausmeister gesellen hauswart zimmerergeselle hausverwalter landwirt handwerker montierer hauswirtschafterin stadtkämmerer |
| 36 | 42 | -0.932 | kindheitspädagoge stack contract xxl packaging referent development dhbw prefabrication müller |
| 21 | 90 | -0.887 | stationary erzieher bzw payment einrichtungsleitung representative gebäudereinigung shk employees grünberg |
| 35 | 42 | -0.880 | safety arbeitssicherheit telecontrol wind turbines sun occupational testing shutdowns bathing |
| 14 | 83 | -0.859 | retraining div environmental train ergotherapeut ergotherapeutin security speaker social drk |
| 18 | 175 | -0.840 | educator pedagogical heilbronn pädagogische dual specialist speech stiftsberg krankenversicherung fahrzeugmontage |
| 15 | 67 | -0.823 | merchant fleischereifachverkäuferin developer seller training administrator psychologe generalist counter welder |
| 19 | 47 | -0.780 | software anwendersupport entwickler digitale corporate partner business organization cooperations publishers |
| 41 | 47 | -0.776 | salesperson filialleiter employment changers also filialleitung products verkauf marketing gardener |
| 11 | 150 | -0.756 | schulbegleiter dualer optoelectronics campus master planung elektrotechnik development montage technische |

### Dv3ls08: the 10 clusters with the lowest C_NPMI

| cluster | titles | C_NPMI | top words |
|---|---|---|---|
| 42 | 81 | -0.898 | assistenz teamassistenz geschäftsführung serviceassistent projektassistenz diätassistent geschäftsleitung assistent serviceassistenz teamassistent |
| 39 | 54 | -0.887 | maler lackierer schreiner maurer handwerker schlosser drucker beschichter estrichleger monteur |
| 24 | 47 | -0.826 | immobilienkaufmann immobilienkauffrau immobilienmakler kapitalanlagen immobilienverwalter immobilien property technischer frau immobilienkoordinator |
| 51 | 65 | -0.723 | filialleitung leitung filialleiter sport abteilungsleiter stellvertretende hübner fachbereichsleitung sachgebietsleitung abteilung |
| 16 | 45 | -0.691 | verkäufer teilzeit seller kassierer voll großkunden teppiche vollzeit non full |
| 22 | 70 | -0.671 | student working recruiter work recruiting generalist partner resources business human |
| 35 | 84 | -0.627 | reinigungskraft hausmeister cleaner minijob mini hauswirtschaftskraft reinigungskräfte housekeeping teilzeit schule |
| 58 | 152 | -0.568 | pflegefachkraft pflegedienstleitung pflegefachfrau examinierte gesundheits pflege pflegefachkräfte pflegefachmann altenpfleger krankenpfleger |
| 10 | 44 | -0.548 | security staff kitchen koch gate military properties helper event district |
| 17 | 79 | -0.532 | chef cook kitchen house housekeeper helper housekeeping baker butcher cleaning |
