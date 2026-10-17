# Greece panel reliability: Greek profiles in the working sample

Source file: `data/raw/profiles_sample.jsonl`. Profiles: 7,222. Profiles have no country code, so a profile is Greek when its free-text `location` contains a Greek country or city name (accents ignored; Athens in a US state excluded). The list of matched strings is below so the rule can be checked by eye.

## 1. How many

- Greek profiles: **99** of 7,222 (1.37%).
- Matched by term: `greece` 99.

### Sources of the Greek profiles

| Source | Greek profiles | All profiles of the source | Share |
|---|---:|---:|---:|
| stack-philosophy | 9 | 250 | 3.6% |
| stack-law | 8 | 250 | 3.2% |
| STACK-Earth Science | 6 | 250 | 2.4% |
| STACK-Philosophy | 6 | 250 | 2.4% |
| stack-earthscience | 5 | 204 | 2.5% |
| STACK-Literature | 5 | 250 | 2.0% |
| stack-math | 5 | 250 | 2.0% |
| STACK-Physics | 5 | 250 | 2.0% |
| stack-politics | 5 | 250 | 2.0% |
| linkedin | 4 | 250 | 1.6% |
| STACK-Electrical Engineering | 4 | 250 | 1.6% |
| STACK-Mathematics | 4 | 250 | 1.6% |
| stack-physics | 4 | 250 | 1.6% |
| STACK-Sports | 4 | 250 | 1.6% |
| STACK-Biology | 3 | 250 | 1.2% |
| stack-chemistry | 3 | 250 | 1.2% |
| STACK-Stack Overflow | 3 | 250 | 1.2% |
| stack-electronics | 2 | 250 | 0.8% |
| stack-linguistics | 2 | 250 | 0.8% |
| stack-literature | 2 | 123 | 1.6% |
| STACK-Politics | 2 | 250 | 0.8% |
| stack-sports | 2 | 145 | 1.4% |
| stack-stackoverflow | 2 | 250 | 0.8% |
| stack-biology | 1 | 250 | 0.4% |
| STACK-Chemistry | 1 | 250 | 0.4% |
| stack-interpersonal | 1 | 250 | 0.4% |
| STACK-Linguistics | 1 | 250 | 0.4% |

### Matched location strings (top 40)

| Location text | Profiles |
|---|---:|
| Greece | 58 |
| Athens, Greece | 20 |
| Athens, Greece and London, UK | 8 |
| Thessaloniki, Greece | 3 |
| Patra, Greece | 2 |
| Eleusis, Ditiki Attiki, Greece | 1 |
| Agia Paraskevi, Greece | 1 |
| Keratea, Greece | 1 |
| Greece,Volos | 1 |
| Greece, Νέα Υόρκη, Ηνωμένες Πολιτείες | 1 |
| Heraklion, Greece | 1 |
| Greece and United Kingdom | 1 |
| Thessaloniki, Kentriki Makedonia Greece | 1 |

### Locations with Greek letters that the rule did not match

None: every location written in Greek letters was matched.

### Most frequent location strings in the whole sample (top 25)

| Location text | Profiles |
|---|---:|
| Germany | 1479 |
| France | 541 |
| Netherlands | 484 |
| Italy | 294 |
| Belgium | 286 |
| Sweden | 282 |
| Poland | 175 |
| Denmark | 163 |
| Spain | 151 |
| Czech Republic | 141 |
| Ireland | 136 |
| Berlin, Germany | 135 |
| Austria | 132 |
| Portugal | 116 |
| Finland | 113 |
| Romania | 93 |
| Paris, France | 84 |
| Bulgaria | 81 |
| Stockholm, Sweden | 76 |
| Hungary | 74 |
| Greece | 58 |
| Croatia | 53 |
| Dublin, Ireland | 43 |
| Slovakia | 43 |
| Slovenia | 42 |

## 2. Field completeness: Greek against the rest

Each cell shows share (filled/total; 95% Wilson interval). 'Same sources' are non-Greek profiles from the sources that hold Greek profiles, which removes the source effect (Revelio's `skills` completeness is 12.4%).

| Field | Greek | All non-Greek | Non-Greek, same sources |
|---|---|---|---|
| `skills` | 64.6% (64/99; 55%-73%) | 62.6% (4462/7123; 62%-64%) | 66.1% (4215/6373; 65%-67%) |
| `occupation_uris` | 0.0% (0/99; 0%-4%) | 3.3% (235/7123; 3%-4%) | 0.0% (0/6373; 0%-0%) |
| `sectors` | 0.0% (0/99; 0%-4%) | 3.3% (232/7123; 3%-4%) | 0.0% (3/6373; 0%-0%) |
| `content` | 100.0% (99/99; 96%-100%) | 95.8% (6827/7123; 95%-96%) | 98.4% (6273/6373; 98%-99%) |
| `description` | 0.0% (0/99; 0%-4%) | 0.2% (14/7123; 0%-0%) | 0.0% (0/6373; 0%-0%) |
| `startdate` | 0.0% (0/99; 0%-4%) | 1.5% (105/7123; 1%-2%) | 0.0% (0/6373; 0%-0%) |

## 3. Tier split that needs no lookup

| Group | Tier 1 (skills) | Tier 2 reachable (no skills, has occupation_uris) | Neither (Tier 3 or 4) |
|---|---:|---:|---:|
| Greek (n=99) | 64 (64.6%) | 0 (0.0%) | 35 (35.4%) |
| All non-Greek (n=7123) | 4462 (62.6%) | 204 (2.9%) | 2457 (34.5%) |
| Non-Greek, same sources (n=6373) | 4215 (66.1%) | 0 (0.0%) | 2158 (33.9%) |

## 4. How to read it

- With fewer than about 30 Greek profiles the intervals are too wide to call Greek profiles sparse or not; say that the sample cannot answer and, if the Greece panel needs profiles, pull Greek profiles on purpose.
- Compare Greek with the 'same sources' column, not with the whole sample.
- The sample is not representative of the population (Section 13.1 of the report), so these shares describe the sample.

