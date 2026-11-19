# Topic coherence (C_NPMI) and topic diversity of the clusters: lesjeudis

Reference corpus: 18,625 titles with a title (boolean document co-occurrence, one title = one document). Top 10 words per cluster by class-based tf-idf; clusters with at least 20 titles; diversity over the top 25 words. NPMI is -1 when two words never occur together and +1 when they always do.

| input | clusters | noise (postings with a title) | median C_NPMI | mean C_NPMI weighted by postings | topic diversity |
|---|---|---|---|---|---|
| A | 144 | 30.9% | -0.389 | -0.342 | 0.600 |
| Dv2 | 142 | 20.6% | -0.485 | -0.447 | 0.567 |
| Dv3 | 102 | 30.6% | -0.376 | -0.273 | 0.625 |

### A: the 10 clusters with the lowest C_NPMI

| cluster | titles | C_NPMI | top words |
|---|---|---|---|
| 13 | 82 | -0.918 | coiffeur server serveur supplier diver livreur chauffeur approvisionneur breakfast ajusteur |
| 19 | 44 | -0.750 | coordinator coordinateur stock logistician logistics agent qhse cordinator igc stewardship |
| 5 | 42 | -0.742 | workstation intune workstations work modern television macos chrome intuune flexra |
| 58 | 62 | -0.682 | devops engot devsecops segment experienced observability confirmed monitoring engines kubernes |
| 17 | 117 | -0.661 | scientist data llm applied computer science had datscientist standardization statistician |
| 135 | 65 | -0.653 | gestionnaire contrôleur gestion parc risques equipe maitrise humaines formateur consulting |
| 143 | 74 | -0.642 | testeur automaticien automatisation test fonctionnel automatician essayeur metteur triconnex sncc |
| 14 | 73 | -0.641 | buyer acheteur group purchase pii buyers experth bpo purchasing market |
| 103 | 40 | -0.639 | directory active expert alert progiciel openshift filenet netapp nsx certificate |
| 123 | 68 | -0.633 | consultant quant relation advantage associate strategy generalist consulting hcm workday |

### Dv2: the 10 clusters with the lowest C_NPMI

| cluster | titles | C_NPMI | top words |
|---|---|---|---|
| 87 | 41 | -1.000 | safe golang prévoaynce usinage opensearch developeur dry embarqué embedded prototyping |
| 94 | 78 | -0.890 | react informatica visual net back autosar cegid windchill automatisme ios |
| 51 | 72 | -0.857 | incident change release salesforce pre merchandise itm insulaires youth literacy |
| 91 | 60 | -0.822 | holidays vendarian vue postgresql kotlin core monétique end experienced convergence |
| 109 | 58 | -0.797 | hairdresser coiffeur versatile serveur adjuster manicurist makeup masseur kinesitherapeute déjeuner |
| 10 | 191 | -0.786 | helpdesk installation driver automated technicien laval technician conducteur sirh human |
| 25 | 48 | -0.785 | auditor sec pcaob cybersecurity hsm espagnol ingéme citrix bases cybersécurité |
| 34 | 136 | -0.772 | agile webmaster luxe testeur master aws web nodejs html css |
| 62 | 62 | -0.770 | proximité local technicien technician informatique sas bilingual hotliner environmental operating |
| 70 | 141 | -0.765 | discipline student cifre optical quantum program system fusion displays pyrotechnic |

### Dv3: the 10 clusters with the lowest C_NPMI

| cluster | titles | C_NPMI | top words |
|---|---|---|---|
| 30 | 69 | -0.918 | coiffeur server serveur livreur plongeur diver chauffeur approvisionneur breakfast ajusteur |
| 31 | 58 | -0.780 | pmo fraude budget mco agile monétique moa fms généraliste budgétaire |
| 11 | 75 | -0.713 | devops devsecops aws segment énergies icare devopsdevsecops kubernes typescipt secops |
| 55 | 54 | -0.691 | expert active directory alert progiciel referent ambassador filenet ssi zabbix |
| 97 | 69 | -0.644 | consultant edi relation client seo vsi chain csv infolog moa |
| 46 | 40 | -0.640 | affaires commercial business alternating ingénieur trilingue dmu engineered allemand patent |
| 9 | 40 | -0.629 | workstation workplace workstations intune modern television macos cio chrome intuune |
| 20 | 69 | -0.604 | buyer acheteur group achats pii buyers bpo experth market industriels |
| 54 | 109 | -0.593 | industry industrie nuclear nucléaire thermohydraulic provence aeronautical aix embedded scientific |
| 34 | 97 | -0.589 | coordinator coordinateur deputy director logistics leader head team agent section |
