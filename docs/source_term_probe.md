# Source term probe

Counts from the API keyword filter (one-row requests, `count` only) in one window per source. Hits per 10,000 postings in brackets. See the header of `diagnostics/61_source_term_probe.py` for what the filter can and cannot see; use this to rank sources, not to state prevalences.

## 1. Windows and totals

| Source | Window | Postings |
|---|---|---:|
| eures | 2025-09-01 to 2025-09-30 | 937 |

## 2. Language words (share of the window's postings containing the word)

| Source | en: the | de: und | fr: les | nl: het | sv: och | el: και |
|---|---|---|---|---|---|---|
| eures | 0% | 0% | 0% | 0% | 0% | 0% |

A rough indicator: a word can also occur in postings of another language (names, loan words), and a stemmed index can lower the count.

## 3. Index check (exact word against its stem)

| Source | manager / manag | engineer / engin | reading |
|---|---|---|---|
| eures | 0 / 63 | 0 / 30 | stem returns more: index looks STEMMED, unstemmed counts are lower bounds |

## 4. Terms

`form`: word = one keyword; all words = every word of a multi-word term with `and`, anywhere in the posting (the filter does not match phrases: an upper bound that says little). Cells: hits (per 10,000).

| Term | Lang | Channel | Form | eures |
|---|---|---|---|---|
| reshoring | any | reshoring | word | - |
| nearshoring | any | reshoring | word | - |
| onshoring | any | reshoring | word | - |
| friend-shoring | any | reshoring | word | - |
| friendshoring | any | reshoring | word | - |
| de-risking | any | reshoring | word | - |
| decoupling | en | reshoring | word | - |
| supply chain resilience | en | reshoring | all words | - |
| supply chain security | en | reshoring | all words | - |
| strategic autonomy | en | reshoring | all words | - |
| industrial policy | en | reshoring | all words | - |
| sovereignty | en | reshoring | word | - |
| geopolitical | en | context | word | - |
| tariffs | en | trade compliance | word | - |
| export controls | en | trade compliance | all words | - |
| export control | en | trade compliance | all words | - |
| dual-use | any | trade compliance | word | - |
| sanctions | any | trade compliance | word | - |
| embargo | any | trade compliance | word | - |
| customs | en | trade compliance | word | - |
| CBAM | any | trade compliance | word | - |
| EUDR | any | trade compliance | word | - |
| anti-dumping | en | trade compliance | word | - |
| rules of origin | en | trade compliance | all words | - |
| critical raw materials | en | critical materials | all words | - |
| rare earths | en | critical materials | all words | - |
| lithium | any | critical materials | word | - |
| semiconductor | en | critical materials | word | - |
| semiconductors | en | critical materials | word | - |
| chips act | en | critical materials | all words | - |
| defence | en | defense | word | - |
| defense | en | defense | word | - |
| armed forces | en | defense | all words | - |
| ammunition | en | defense | word | - |
| munitions | any | defense | word | - |
| energy security | en | energy security | all words | - |
| security of supply | en | energy security | all words | - |
| free trade agreement | en | diversification | all words | - |
| Rückverlagerung | de | reshoring | word | - |
| Lieferkettengesetz | de | trade compliance | word | - |
| Lieferkettensicherheit | de | reshoring | word | - |
| Lieferkette | de | context | word | - |
| Lieferketten | de | context | word | - |
| Exportkontrolle | de | trade compliance | word | - |
| Exportkontrollen | de | trade compliance | word | - |
| Ausfuhrkontrolle | de | trade compliance | word | - |
| Außenwirtschaft | de | trade compliance | word | - |
| Zoll | de | trade compliance | word | - |
| Zollabwicklung | de | trade compliance | word | - |
| Zollrecht | de | trade compliance | word | - |
| Zölle | de | trade compliance | word | - |
| Sanktionen | de | trade compliance | word | - |
| Rüstung | de | defense | word | - |
| Rüstungsindustrie | de | defense | word | - |
| Verteidigung | de | defense | word | - |
| Verteidigungsindustrie | de | defense | word | - |
| Munition | de | defense | word | - |
| Halbleiter | de | critical materials | word | - |
| seltene Erden | de | critical materials | all words | - |
| kritische Rohstoffe | de | critical materials | all words | - |
| Energiesicherheit | de | energy security | word | - |
| Versorgungssicherheit | de | energy security | word | - |
| Handelsabkommen | de | diversification | word | - |
| Industriepolitik | de | reshoring | word | - |
| relocalisation | fr | reshoring | word | - |
| réindustrialisation | fr | reshoring | word | - |
| souveraineté | fr | reshoring | word | - |
| souveraineté numérique | fr | reshoring | all words | - |
| autonomie stratégique | fr | reshoring | all words | - |
| douane | fr | trade compliance | word | - |
| douanes | fr | trade compliance | word | - |
| douanier | fr | trade compliance | word | - |
| droits de douane | fr | trade compliance | all words | - |
| contrôle des exportations | fr | trade compliance | all words | - |
| double usage | fr | trade compliance | all words | - |
| devoir de vigilance | fr | trade compliance | all words | - |
| défense | fr | defense | word | - |
| armement | fr | defense | word | - |
| semi-conducteurs | fr | critical materials | word | - |
| terres rares | fr | critical materials | all words | - |
| matières premières critiques | fr | critical materials | all words | - |
| exportcontrole | nl | trade compliance | word | - |
| douaneafhandeling | nl | trade compliance | word | - |
| sancties | nl | trade compliance | word | - |
| invoerrechten | nl | trade compliance | word | - |
| defensie | nl | defense | word | - |
| halfgeleiders | nl | critical materials | word | - |
| zeldzame aardmetalen | nl | critical materials | all words | - |
| toeleveringsketen | nl | context | word | - |
| leveringszekerheid | nl | energy security | word | - |
| energiezekerheid | nl | energy security | word | - |
| strategische autonomie | nl | reshoring | all words | - |
| exportkontroll | sv | trade compliance | word | - |
| tull | sv | trade compliance | word | - |
| tullhantering | sv | trade compliance | word | - |
| sanktioner | sv | trade compliance | word | - |
| försvarsindustri | sv | defense | word | - |
| totalförsvar | sv | defense | word | - |
| halvledare | sv | critical materials | word | - |
| sällsynta jordartsmetaller | sv | critical materials | all words | - |
| försörjningstrygghet | sv | energy security | word | - |

## 5. Per source: terms with hits and the most frequent terms

| Source | terms with at least 1 hit | with at least 10 hits | highest rates (hits per 10,000) |
|---|---:|---:|---|
| eures | 0 | 0 |  |

Generic words (for example `customs`, `Zoll`, `Lieferkette`, `defence`) dominate the rates; read the table by term, not by the sum. Counts of terms that are also ordinary words say little about deglobalization.

