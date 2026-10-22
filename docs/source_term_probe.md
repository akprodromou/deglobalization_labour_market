# Source term probe

Counts from the API keyword filter (one-row requests, `count` only) in one window per source. Hits per 10,000 postings in brackets. See the header of `diagnostics/61_source_term_probe.py` for what the filter can and cannot see; use this to rank sources, not to state prevalences.

## 1. Windows and totals

| Source | Window | Postings |
|---|---|---:|
| eures-escox | 2026-01-12 to 2026-01-18 | 22,499 |

## 2. Language words (share of the window's postings containing the word)

| Source | en: the | de: und | fr: les | nl: het | sv: och | el: και |
|---|---|---|---|---|---|---|
| eures-escox | 0% | 1% | 5% | 0% | 0% | 0% |

A rough indicator: a word can also occur in postings of another language (names, loan words), and a stemmed index can lower the count.

## 3. Index check (exact word against its stem)

| Source | manager / manag | engineer / engin | reading |
|---|---|---|---|
| eures-escox | 0 / 12,021 | 0 / 2,868 | stem returns more: index looks STEMMED, unstemmed counts are lower bounds |

## 4. Terms

`form`: word = one keyword; all words = every word of a multi-word term with `and`, anywhere in the posting (the filter does not match phrases: an upper bound that says little). Cells: hits (per 10,000).

| Term | Lang | Channel | Form | eures-escox |
|---|---|---|---|---|
| reshoring | any | reshoring | word | 0 (0.0) |
| nearshoring | any | reshoring | word | 0 (0.0) |
| onshoring | any | reshoring | word | 0 (0.0) |
| friend-shoring | any | reshoring | word | 0 (0.0) |
| friendshoring | any | reshoring | word | 0 (0.0) |
| de-risking | any | reshoring | word | 0 (0.0) |
| decoupling | en | reshoring | word | 0 (0.0) |
| supply chain resilience | en | reshoring | all words | 0 (0.0) |
| supply chain security | en | reshoring | all words | 0 (0.0) |
| strategic autonomy | en | reshoring | all words | 0 (0.0) |
| industrial policy | en | reshoring | all words | 0 (0.0) |
| sovereignty | en | reshoring | word | 0 (0.0) |
| geopolitical | en | context | word | 0 (0.0) |
| tariffs | en | trade compliance | word | 0 (0.0) |
| export controls | en | trade compliance | all words | 0 (0.0) |
| export control | en | trade compliance | all words | 36 (16.0) |
| dual-use | any | trade compliance | word | 0 (0.0) |
| sanctions | any | trade compliance | word | 0 (0.0) |
| embargo | any | trade compliance | word | 2 (0.9) |
| customs | en | trade compliance | word | 0 (0.0) |
| CBAM | any | trade compliance | word | 2 (0.9) |
| EUDR | any | trade compliance | word | 2 (0.9) |
| anti-dumping | en | trade compliance | word | 0 (0.0) |
| rules of origin | en | trade compliance | all words | 0 (0.0) |
| critical raw materials | en | critical materials | all words | 0 (0.0) |
| rare earths | en | critical materials | all words | 0 (0.0) |
| lithium | any | critical materials | word | 1 (0.4) |
| semiconductor | en | critical materials | word | 18 (8.0) |
| semiconductors | en | critical materials | word | 0 (0.0) |
| chips act | en | critical materials | all words | 0 (0.0) |
| defence | en | defense | word | 0 (0.0) |
| defense | en | defense | word | 0 (0.0) |
| armed forces | en | defense | all words | 0 (0.0) |
| ammunition | en | defense | word | 0 (0.0) |
| munitions | any | defense | word | 0 (0.0) |
| energy security | en | energy security | all words | 0 (0.0) |
| security of supply | en | energy security | all words | 0 (0.0) |
| free trade agreement | en | diversification | all words | 33 (14.7) |
| Rückverlagerung | de | reshoring | word | 0 (0.0) |
| Lieferkettengesetz | de | trade compliance | word | 0 (0.0) |
| Lieferkettensicherheit | de | reshoring | word | 0 (0.0) |
| Lieferkette | de | context | word | 0 (0.0) |
| Lieferketten | de | context | word | 0 (0.0) |
| Exportkontrolle | de | trade compliance | word | 0 (0.0) |
| Exportkontrollen | de | trade compliance | word | 0 (0.0) |
| Ausfuhrkontrolle | de | trade compliance | word | 0 (0.0) |
| Außenwirtschaft | de | trade compliance | word | 0 (0.0) |
| Zoll | de | trade compliance | word | 0 (0.0) |
| Zollabwicklung | de | trade compliance | word | 0 (0.0) |
| Zollrecht | de | trade compliance | word | 0 (0.0) |
| Zölle | de | trade compliance | word | 0 (0.0) |
| Sanktionen | de | trade compliance | word | 0 (0.0) |
| Rüstung | de | defense | word | 0 (0.0) |
| Rüstungsindustrie | de | defense | word | 0 (0.0) |
| Verteidigung | de | defense | word | 0 (0.0) |
| Verteidigungsindustrie | de | defense | word | 0 (0.0) |
| Munition | de | defense | word | 0 (0.0) |
| Halbleiter | de | critical materials | word | 0 (0.0) |
| seltene Erden | de | critical materials | all words | 0 (0.0) |
| kritische Rohstoffe | de | critical materials | all words | 0 (0.0) |
| Energiesicherheit | de | energy security | word | 0 (0.0) |
| Versorgungssicherheit | de | energy security | word | 1 (0.4) |
| Handelsabkommen | de | diversification | word | 0 (0.0) |
| Industriepolitik | de | reshoring | word | 0 (0.0) |
| relocalisation | fr | reshoring | word | 0 (0.0) |
| réindustrialisation | fr | reshoring | word | 0 (0.0) |
| souveraineté | fr | reshoring | word | 0 (0.0) |
| souveraineté numérique | fr | reshoring | all words | 0 (0.0) |
| autonomie stratégique | fr | reshoring | all words | 0 (0.0) |
| douane | fr | trade compliance | word | 0 (0.0) |
| douanes | fr | trade compliance | word | 0 (0.0) |
| douanier | fr | trade compliance | word | 0 (0.0) |
| droits de douane | fr | trade compliance | all words | 0 (0.0) |
| contrôle des exportations | fr | trade compliance | all words | 0 (0.0) |
| double usage | fr | trade compliance | all words | 0 (0.0) |
| devoir de vigilance | fr | trade compliance | all words | 0 (0.0) |
| défense | fr | defense | word | 0 (0.0) |
| armement | fr | defense | word | 0 (0.0) |
| semi-conducteurs | fr | critical materials | word | 0 (0.0) |
| terres rares | fr | critical materials | all words | 0 (0.0) |
| matières premières critiques | fr | critical materials | all words | 0 (0.0) |
| exportcontrole | nl | trade compliance | word | 0 (0.0) |
| douaneafhandeling | nl | trade compliance | word | 0 (0.0) |
| sancties | nl | trade compliance | word | 0 (0.0) |
| invoerrechten | nl | trade compliance | word | 0 (0.0) |
| defensie | nl | defense | word | 0 (0.0) |
| halfgeleiders | nl | critical materials | word | 0 (0.0) |
| zeldzame aardmetalen | nl | critical materials | all words | 0 (0.0) |
| toeleveringsketen | nl | context | word | 0 (0.0) |
| leveringszekerheid | nl | energy security | word | 0 (0.0) |
| energiezekerheid | nl | energy security | word | 0 (0.0) |
| strategische autonomie | nl | reshoring | all words | 0 (0.0) |
| exportkontroll | sv | trade compliance | word | 0 (0.0) |
| tull | sv | trade compliance | word | 8 (3.6) |
| tullhantering | sv | trade compliance | word | 0 (0.0) |
| sanktioner | sv | trade compliance | word | 0 (0.0) |
| försvarsindustri | sv | defense | word | 0 (0.0) |
| totalförsvar | sv | defense | word | 0 (0.0) |
| halvledare | sv | critical materials | word | 0 (0.0) |
| sällsynta jordartsmetaller | sv | critical materials | all words | 0 (0.0) |
| försörjningstrygghet | sv | energy security | word | 0 (0.0) |

## 5. Per source: terms with hits and the most frequent terms

| Source | terms with at least 1 hit | with at least 10 hits | highest rates (hits per 10,000) |
|---|---:|---:|---|
| eures-escox | 7 | 1 | semiconductor 8.0, tull 3.6, embargo 0.9, EUDR 0.9, CBAM 0.9, lithium 0.4, Versorgungssicherheit 0.4 |

Generic words (for example `customs`, `Zoll`, `Lieferkette`, `defence`) dominate the rates; read the table by term, not by the sum. Counts of terms that are also ordinary words say little about deglobalization.

