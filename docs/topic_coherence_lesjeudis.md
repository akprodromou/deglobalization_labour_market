# Topic coherence (C_NPMI) and topic diversity of the clusters: lesjeudis

Reference corpus: 18,625 titles with a title (boolean document co-occurrence, one title = one document). Top 10 words per cluster by class-based tf-idf; clusters with at least 20 titles; diversity over the top 25 words. NPMI is -1 when two words never occur together and +1 when they always do.

| input | clusters | noise (postings with a title) | median C_NPMI | mean C_NPMI weighted by postings | topic diversity |
|---|---|---|---|---|---|
| A | 144 | 30.9% | -0.385 | -0.339 | 0.602 |
| Dv2ls08 | 121 | 13.0% | -0.534 | -0.442 | 0.597 |
| Dv3ls08 | 109 | 37.9% | -0.387 | -0.313 | 0.636 |

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

### Dv2ls08: the 10 clusters with the lowest C_NPMI

| cluster | titles | C_NPMI | top words |
|---|---|---|---|
| 72 | 77 | -0.934 | buyer acheteur itps gemizing sdm sourcing datacenter accounts methods purchase |
| 73 | 151 | -0.933 | tester aggp core fonctionnel opérationnel net nuxeo prodige visual debeug |
| 27 | 94 | -0.888 | htb éléctronique quality qualité hta remote electronic documents tier principal |
| 61 | 60 | -0.883 | servicenow fico risk concepteur datscientist aps mgmt postman cucumber mérignaccdii |
| 37 | 52 | -0.863 | incident salesforce release technique directory active merchandise itm insulaires inspecteur |
| 57 | 97 | -0.854 | technologies quantalys nouvelles palma wealth lawyer publishing campaign artificial react |
| 60 | 79 | -0.840 | designer pricing akur altium électronique creative médical ground equity product |
| 17 | 60 | -0.823 | yocto embedded servicenow engeniur kvm electricity cpq ssi cable itsm |
| 65 | 54 | -0.814 | counsel buyer legal lawyer slot quality continuity contracts resilience installation |
| 58 | 66 | -0.810 | growth startup human wlan api edition cdi lan coordination team |

### Dv3ls08: the 10 clusters with the lowest C_NPMI

| cluster | titles | C_NPMI | top words |
|---|---|---|---|
| 4 | 72 | -0.756 | coiffeur polyvalent server serveur diver plongeur breakfast masseur kinesitherapeute confirmé |
| 101 | 58 | -0.726 | consultant edi councils vent oracle cegid hcm relation immobilier talend |
| 44 | 117 | -0.718 | manager asset business sas park btob quant problem school career |
| 14 | 49 | -0.706 | pmo budget moa fms généraliste import committee budgétaire generalist integrated |
| 12 | 89 | -0.688 | buyer acheteur supplier group seo sea approvisionneur publicité procurement pii |
| 13 | 75 | -0.677 | devops devsecops aws segment kubernes typescipt énergies industrial finops secops |
| 25 | 133 | -0.628 | technician computer operating writer operations cto specialist technical maintenance electrician |
| 6 | 113 | -0.596 | industrie industry nuclear nucléaire aix provence thermohydraulic aeronautical pau embedded |
| 60 | 73 | -0.592 | cloud virtualisation experimente engineer platform success supervision provider openstack shaper |
| 27 | 49 | -0.585 | helpdesk technicien help vitrolles desk teleconseiller techniciencne automatism agv joué |
