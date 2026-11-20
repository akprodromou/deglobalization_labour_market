# Laplacian Score filter: lesjeudis

An item is kept when its Laplacian Score (He, Cai and Niyogi 2005) is below 1.0. Graph: 5 nearest neighbours by title embedding (cosine), heat-kernel constant t = 0.1175 (mean squared distance over the edges between different titles). A low score means that the postings carrying the item are neighbours on the graph.

### esco: 990 items scored, 983 kept (score below 1.0), 7 dropped

Score: minimum 0.255, median 0.882, maximum 1.002.

| score below | items kept | share of items | postings with at least one kept item |
|---|---|---|---|
| 0.5 | 13 | 1% | 7.6% |
| 0.6 | 35 | 4% | 14.1% |
| 0.7 | 80 | 8% | 43.4% |
| 0.8 | 194 | 20% | 77.4% |
| 0.9 | 602 | 61% | 97.7% |
| 1.0 | 983 | 99% | 98.6% |

| item | postings | Laplacian Score | decision |
|---|---|---|---|
| innovation processes The techniques, mod | 2,412 | 0.834 | kept |
| support employability of people with dis | 2,357 | 0.836 | kept |
| cyber security IT security information s | 2,239 | 0.702 | kept |
| authoring software authoring software Th | 1,746 | 0.786 | kept |
| DevOps The DevOps development approach i | 1,621 | 0.604 | kept |
| coordinate security oversee security man | 1,475 | 0.866 | kept |
| perform project management perform manag | 1,464 | 0.828 | kept |
| Agile development The agile development  | 1,423 | 0.828 | kept |
| develop new products generate new produc | 1,407 | 0.746 | kept |
| mobility as a service MaaS sustainable m | 1,303 | 0.801 | kept |
| Python (computer programming) Python 3K  | 1,285 | 0.777 | kept |
| patient autonomy patient's independence  | 1,210 | 0.884 | kept |
| communicate with customers talk with cus | 1,208 | 0.831 | kept |
| communication conversation interaction c | 1,205 | 0.815 | kept |
| digitization digital enablement The proc | 1,195 | 0.788 | kept |
| recruit personnel personnel recruiting p | 1,146 | 0.812 | kept |
| Java (computer programming) Java The tec | 1,117 | 0.672 | kept |
| gender studies the study of gender gende | 1,110 | 0.810 | kept |
| cloud technologies cloud computing cloud | 1,055 | 0.715 | kept |
| feed concrete mixer supply concrete mixe | 1,038 | 0.301 | kept |
| consult with business clients consulting | 965 | 0.854 | kept |
| solution deployment The technologies and | 949 | 0.836 | kept |
| digital systems digital information syst | 926 | 0.568 | kept |
| Jenkins (tools for software configuratio | 923 | 0.730 | kept |
| quantum mechanics the study of quantum m | 914 | 0.670 | kept |
| defense system defensive system defense  | 914 | 0.668 | kept |
| provide user documentation Develop and o | 899 | 0.882 | kept |
| manage maintenance operations manage ope | 850 | 0.894 | kept |
| continuous improvement philosophies cont | 823 | 0.882 | kept |
| SAP Data Services The computer program S | 772 | 0.729 | kept |
| Ansible The tool Ansible is a software p | 740 | 0.715 | kept |
| aerodynamics aeronautics The scientific  | 726 | 0.782 | kept |
| SQL Informix 4GL/SQL SEQUEL Subquery The | 719 | 0.810 | kept |
| communicate with stakeholders inform sta | 713 | 0.859 | kept |
| meet deadlines achieve deadlines complet | 711 | 0.825 | kept |
| demonstrate curiosity display curiosity  | 696 | 0.842 | kept |
| monitor developments in field of experti | 660 | 0.827 | kept |
| laboratory equipment laboratory gear lab | 610 | 0.863 | kept |
| technical terminology technical lingo te | 609 | 0.916 | kept |
| solve technical problems Identify techni | 593 | 0.874 | kept |

### lightcast: 6 items scored, 6 kept (score below 1.0), 0 dropped

Score: minimum 0.464, median 0.762, maximum 0.952.

| score below | items kept | share of items | postings with at least one kept item |
|---|---|---|---|
| 0.5 | 1 | 17% | 0.1% |
| 0.6 | 1 | 17% | 0.1% |
| 0.7 | 2 | 33% | 0.3% |
| 0.8 | 4 | 67% | 4.8% |
| 0.9 | 4 | 67% | 4.8% |
| 1.0 | 6 | 100% | 4.8% |

| item | postings | Laplacian Score | decision |
|---|---|---|---|
| Supply Chain | 887 | 0.773 | kept |
| Supply Chain Management | 35 | 0.612 | kept |
| Supply Chain Planning | 16 | 0.464 | kept |
| Production Planning | 15 | 0.933 | kept |
| Demand Planning | 11 | 0.952 | kept |
| SAP Ariba | 10 | 0.752 | kept |
