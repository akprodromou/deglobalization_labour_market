# Keyword index experiment: kariera.gr, 2026-03

Sample: 100 postings (page 1 of 6,953). For each keyword the server was asked which of these ids match. Per rule: TP = returned and rule says match, FP = returned but rule says no, FN = rule says match but not returned. The best rule is the one with the highest F1.

## A title word

| keyword | returned | best rule | TP / FP / FN (best) | title | desc | stem | substring | ws | note |
|---|---:|---|---|---|---|---|---|---|---|
| `engineer` | 0 | stem (F1 1.00) | 0/0/0 | 0/0/22 | 0/0/25 | 0/0/0 | 0/0/43 | 0/0/26 |  |
| `senior` | 16 | ws (F1 0.97) | 15/1/0 | 11/5/3 | 15/1/3 | 15/1/0 | 16/0/3 | 15/1/0 |  |
| `store` | 33 | substring (F1 1.00) | 33/0/0 | 10/23/0 | 18/15/0 | 33/0/0 | 33/0/0 | 24/9/0 |  |
| `manager` | 0 | stem (F1 1.00) | 0/0/0 | 0/0/10 | 0/0/11 | 0/0/0 | 0/0/20 | 0/0/17 |  |
| `consultant` | 0 | desc<=200 (F1 1.00) | 0/0/0 | 0/0/9 | 0/0/6 | 0/0/0 | 0/0/15 | 0/0/11 |  |
| `lead` | 32 | stem (F1 1.00) | 32/0/0 | 8/24/0 | 17/15/0 | 32/0/0 | 32/0/7 | 17/15/0 |  |
| `analyst` | 12 | substring (F1 1.00) | 12/0/0 | 7/5/0 | 8/4/0 | 12/0/0 | 12/0/0 | 9/3/0 |  |
| `business` | 0 | stem (F1 1.00) | 0/0/0 | 0/0/7 | 0/0/62 | 0/0/0 | 0/0/62 | 0/0/62 |  |

## B early in description

| keyword | returned | best rule | TP / FP / FN (best) | title | desc | stem | substring | ws | note |
|---|---:|---|---|---|---|---|---|---|---|
| `future` | 0 | title (F1 1.00) | 0/0/0 | 0/0/0 | 0/0/59 | 0/0/0 | 0/0/59 | 0/0/59 |  |
| `over` | 0 | title (F1 1.00) | 0/0/0 | 0/0/0 | 0/0/58 | 0/0/58 | 0/0/71 | 0/0/58 |  |
| `across` | 54 | desc (F1 1.00) | 54/0/0 | 0/54/0 | 54/0/0 | 54/0/0 | 54/0/0 | 54/0/0 |  |
| `people` | 0 | title (F1 1.00) | 0/0/0 | 0/0/0 | 0/0/44 | 0/0/0 | 0/0/44 | 0/0/41 |  |
| `private` | 0 | title (F1 1.00) | 0/0/0 | 0/0/0 | 0/0/42 | 0/0/0 | 0/0/46 | 0/0/42 |  |
| `building` | 0 | title (F1 1.00) | 0/0/0 | 0/0/0 | 0/0/42 | 0/0/0 | 0/0/45 | 0/0/42 |  |
| `dedicated` | 0 | title (F1 1.00) | 0/0/0 | 0/0/0 | 0/0/40 | 0/0/0 | 0/0/40 | 0/0/40 |  |
| `drive` | 43 | stem (F1 1.00) | 43/0/0 | 0/43/0 | 40/3/0 | 43/0/0 | 41/2/9 | 40/3/0 |  |

## C late in description

| keyword | returned | best rule | TP / FP / FN (best) | title | desc | stem | substring | ws | note |
|---|---:|---|---|---|---|---|---|---|---|
| `other` | 8 | stem (F1 0.23) | 8/0/53 | 0/8/0 | 7/1/53 | 8/0/53 | 8/0/54 | 7/1/53 |  |
| `culture` | 0 | title (F1 1.00) | 0/0/0 | 0/0/0 | 0/0/60 | 0/0/0 | 0/0/62 | 0/0/60 |  |
| `degree` | 0 | title (F1 1.00) | 0/0/0 | 0/0/0 | 0/0/59 | 0/0/0 | 0/0/62 | 0/0/56 |  |
| `years` | 0 | title (F1 1.00) | 0/0/0 | 0/0/0 | 0/0/59 | 0/0/0 | 0/0/59 | 0/0/59 |  |
| `benefits` | 0 | title (F1 1.00) | 0/0/0 | 0/0/0 | 0/0/57 | 0/0/0 | 0/0/58 | 0/0/51 |  |
| `equal` | 57 | stem (F1 1.00) | 57/0/0 | 0/57/0 | 56/1/1 | 57/0/0 | 57/0/1 | 56/1/0 |  |
| `from` | 0 | title (F1 1.00) | 0/0/0 | 0/0/0 | 0/0/56 | 0/0/55 | 0/0/56 | 0/0/55 |  |
| `disability` | 0 | title (F1 1.00) | 0/0/0 | 0/0/0 | 0/0/56 | 0/0/0 | 0/0/56 | 0/0/49 |  |

## D variants

| keyword | returned | best rule | TP / FP / FN (best) | title | desc | stem | substring | ws | note |
|---|---:|---|---|---|---|---|---|---|---|
| `engineers` | 0 | title (F1 1.00) | 0/0/0 | 0/0/0 | 0/0/7 | 0/0/0 | 0/0/12 | 0/0/7 |  |
| `enginee` | 0 | title (F1 1.00) | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/43 | 0/0/0 |  |
| `enginee*` | 0 | stem (F1 1.00) | 0/0/0 | 0/0/22 | 0/0/43 | 0/0/0 | 0/0/43 | 0/0/43 |  |
| `engineer*` | 0 | stem (F1 1.00) | 0/0/0 | 0/0/22 | 0/0/43 | 0/0/0 | 0/0/43 | 0/0/43 |  |
| `engi*` | 0 | stem (F1 1.00) | 0/0/0 | 0/0/22 | 0/0/45 | 0/0/0 | 0/0/52 | 0/0/45 |  |
| `seniors` | 0 | (no match anywhere) | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 |  |
| `senio` | 0 | title (F1 1.00) | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/19 | 0/0/0 |  |
| `senio*` | 0 | stem (F1 1.00) | 0/0/0 | 0/0/14 | 0/0/18 | 0/0/0 | 0/0/19 | 0/0/16 |  |
| `senior*` | 16 | ws (F1 1.00) | 16/0/0 | 11/5/3 | 15/1/3 | 0/16/0 | 16/0/3 | 16/0/0 |  |
| `seni*` | 0 | stem (F1 1.00) | 0/0/0 | 0/0/14 | 0/0/18 | 0/0/0 | 0/0/19 | 0/0/16 |  |
| `stores` | 0 | stem (F1 1.00) | 0/0/0 | 0/0/1 | 0/0/31 | 0/0/0 | 0/0/31 | 0/0/31 |  |
| `stor` | 0 | title (F1 1.00) | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/47 | 0/0/0 |  |
| `stor*` | 0 | stem (F1 1.00) | 0/0/0 | 0/0/11 | 0/0/43 | 0/0/0 | 0/0/47 | 0/0/43 |  |
| `store*` | 33 | desc (F1 1.00) | 33/0/0 | 11/22/0 | 33/0/0 | 0/33/0 | 33/0/0 | 33/0/0 |  |

## E extra keywords

| keyword | returned | best rule | TP / FP / FN (best) | title | desc | stem | substring | ws | note |
|---|---:|---|---|---|---|---|---|---|---|
| `engin` | 43 | stem (F1 1.00) | 43/0/0 | 0/43/0 | 0/43/0 | 43/0/0 | 43/0/9 | 0/43/0 |  |
| `manag` | 63 | stem (F1 0.99) | 62/1/0 | 0/63/0 | 0/63/0 | 62/1/0 | 63/0/4 | 0/63/0 |  |
| `busi` | 62 | substring (F1 1.00) | 62/0/0 | 0/62/0 | 0/62/0 | 62/0/0 | 62/0/0 | 0/62/0 |  |
| `year` | 81 | substring (F1 1.00) | 81/0/0 | 0/81/0 | 38/43/0 | 81/0/0 | 81/0/0 | 38/43/0 |  |
| `benefit` | 57 | substring (F1 0.99) | 57/0/1 | 0/57/0 | 0/57/0 | 51/6/0 | 57/0/1 | 0/57/0 |  |
| `consult` | 23 | substring (F1 1.00) | 23/0/0 | 0/23/0 | 0/23/0 | 23/0/0 | 23/0/0 | 0/23/0 |  |
| `futur` | 59 | substring (F1 1.00) | 59/0/0 | 0/59/0 | 0/59/0 | 59/0/0 | 59/0/0 | 0/59/0 |  |
| `peopl` | 44 | substring (F1 1.00) | 44/0/0 | 0/44/0 | 0/44/0 | 41/3/0 | 44/0/0 | 0/44/0 |  |
| `build` | 46 | stem (F1 1.00) | 46/0/0 | 0/46/0 | 13/33/0 | 46/0/0 | 46/0/1 | 13/33/0 |  |
| `energi` | 20 | stem (F1 0.97) | 19/1/0 | 0/20/0 | 0/20/0 | 19/1/0 | 0/20/0 | 0/20/0 |  |
| `nurs` | 0 | (no match anywhere) | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 |  |
| `softwar` | 26 | substring (F1 1.00) | 26/0/0 | 0/26/0 | 0/26/0 | 26/0/0 | 26/0/0 | 0/26/0 |  |

## Which rule fits best

| rule | number of keywords where it fits best |
|---|---:|
| stem | 18 |
| title | 16 |
| substring | 9 |
| ws | 2 |
| desc | 2 |
| desc<=200 | 1 |

## Postings that contain the keyword (title or description) but were not returned

Up to 4 missed postings (and 2 returned ones for comparison) per keyword, 40 characters either side of the first occurrence.

### `engineer`: 26 missed

- MISSED (id 248): `network engineer (customer ict)`
- MISSED (id 2822356): `systems engineer`
- MISSED (id 5287075): `lead software engineer (spring, spring boot)`
- MISSED (id 5287076): `lead software engineer (spring, spring boot)`

### `senior`: 3 missed

- MISSED (id 5631766): `mid/senior it business analyst (agile)`
- MISSED (id 5631866): `mid/senior it business analyst (agile)`
- MISSED (id 5631888): `mid/senior it business analyst (agile)`
- returned (id 5294191): `ta pipelines under the guidance of more senior engineers, using programming languages `
- returned (id 5352791): `senior electrical design engineer`

### `manager`: 17 missed

- MISSED (id 2449): `ness objectives. work closely with your manager and key stakeholders to ensure that the`
- MISSED (id 5353541): `on reports to the mechanical department manager. the primary scope of this role is to m`
- MISSED (id 5353659): `deputy store manager - thiva`
- MISSED (id 5354403): `deputy store manager - alexandroupoli`

### `consultant`: 11 missed

- MISSED (id 5291141): `ver the role of a junior presales - bid consultant in netcompany?the successful candidate `
- MISSED (id 5303536): `sap mm consultant`
- MISSED (id 5354080): `presales bid consultant - eu sector`
- MISSED (id 5355260): `data & ai governance consultant`

### `business`: 62 missed

- MISSED (id 2449): `he evolution and optimization of retail business processes supported by sap retail, our `
- MISSED (id 5287075): ` methods (unlimited access to udemy for business, ad-hoc trainings)a personalized develo`
- MISSED (id 5287076): ` methods (unlimited access to udemy for business, ad-hoc trainings)a personalized develo`
- MISSED (id 5287082): `d reliable software solutions that meet business objectiveswrite clean, well-designed, a`

### `future`: 59 missed

- MISSED (id 248): `th disabilities. join us in shaping the future of gaming and lottery solutions!`
- MISSED (id 2822356): `ion, bally's intralot aims to shape the future of regulated gaming and deliver sustain`
- MISSED (id 5287075): `y descriptionare you ready to shape the future technological landscape in europe? we a`
- MISSED (id 5287076): `y descriptionare you ready to shape the future technological landscape in europe? we a`

### `over`: 58 missed

- MISSED (id 2430): `il, wholesale and franchise stores, and over 13,000 employees. it is a member of the`
- MISSED (id 5287075): `ions that drive meaningful impact. with over 8,900 professionals across europe, we h`
- MISSED (id 5287076): `ions that drive meaningful impact. with over 8,900 professionals across europe, we h`
- MISSED (id 5287082): `ions that drive meaningful impact. with over 8,900 professionals across europe, we h`

### `people`: 44 missed

- MISSED (id 2449): ` vassilopoulos, we are more than 12,000 people sharing the same purpose: to give our b`
- MISSED (id 5294187): `orld by creating new value for clients, people, society and the planet, while building`
- MISSED (id 5294188): `orld by creating new value for clients, people, society and the planet, while building`
- MISSED (id 5294189): `orld by creating new value for clients, people, society and the planet, while building`

### `private`: 42 missed

- MISSED (id 248): `itional benefits. hybrid working model. private insurance for you and your family. mode`
- MISSED (id 2822356): `itional benefits. hybrid working model. private insurance for you and your family. mode`
- MISSED (id 5287075): `pe, we help eu institutions, public and private organisations thrive in a rapidly evolv`
- MISSED (id 5287076): `pe, we help eu institutions, public and private organisations thrive in a rapidly evolv`

### `building`: 42 missed

- MISSED (id 2822356): `petitiveness both locally and globally. building on bally's proven digital b2c operation`
- MISSED (id 5287075): `edicated to responsible digitalisation, building innovative, inclusive solutions that dr`
- MISSED (id 5287076): `edicated to responsible digitalisation, building innovative, inclusive solutions that dr`
- MISSED (id 5287082): `edicated to responsible digitalisation, building innovative, inclusive solutions that dr`

### `dedicated`: 40 missed

- MISSED (id 5287075): `chnological landscape in europe? we are dedicated to responsible digitalisation, building`
- MISSED (id 5287076): `chnological landscape in europe? we are dedicated to responsible digitalisation, building`
- MISSED (id 5287082): `chnological landscape in europe? we are dedicated to responsible digitalisation, building`
- MISSED (id 5287083): `chnological landscape in europe? we are dedicated to responsible digitalisation, building`

### `other`: 53 missed

- MISSED (id 248): `, medical condition, disability, or any other protected status. our premises in paian`
- MISSED (id 2449): `sts, developers, business analysts, and other it teams to support the successful deli`
- MISSED (id 2822356): `, medical condition, disability, or any other protected status. our premises in paian`
- MISSED (id 5287075): `, physical or mental disability, or any other factor protected by applicable laws and`
- returned (id 5294187): `milar. finetuning or distilling llms or other predictive or generative ai models will`
- returned (id 5294188): `ferences and team's needs, and we enjoy other initiatives such as summer short friday`

### `culture`: 60 missed

- MISSED (id 5287075): `s prohibited. as part of the netcompany culture, we respect human rights and focus on c`
- MISSED (id 5287076): `s prohibited. as part of the netcompany culture, we respect human rights and focus on c`
- MISSED (id 5287082): `s prohibited. as part of the netcompany culture, we respect human rights and focus on c`
- MISSED (id 5287083): `s prohibited. as part of the netcompany culture, we respect human rights and focus on c`

### `degree`: 59 missed

- MISSED (id 248): `hould include:• a university or college degree in network engineering, computer scienc`
- MISSED (id 2822356): `s.what sets you apart:have a university degree in computer science, computer engineeri`
- MISSED (id 5287075): `swhat would make you a fit for the role:degree in computer science, software engineeri`
- MISSED (id 5287076): `swhat would make you a fit for the role:degree in computer science, software engineeri`

### `years`: 59 missed

- MISSED (id 248): `lated technology field.• a minimum of 2 years of experience in network engineering.• `
- MISSED (id 2449): ` ecc6 platformwho we are looking for 3+ years of relevant it experience, experience i`
- MISSED (id 2822356): `ring, or a related technology field.2-3 years of hands-on experience in systems engin`
- MISSED (id 5294187): `ultiple awards received over the last 3 years (top employer, great place to work and `

### `benefits`: 57 missed

- MISSED (id 248): `sation package combined with additional benefits. hybrid working model. private insuranc`
- MISSED (id 2822356): `athens stock exchange, bally's intralot benefits from access to international capital ma`
- MISSED (id 5287075): `first stepsa competitive compensation & benefits packagehealth and life insurance progra`
- MISSED (id 5287076): `first stepsa competitive compensation & benefits packagehealth and life insurance progra`

### `equal`: 1 missed

- MISSED (id 5353776): `l advancement both locally and globally.equal opportunity employer: we celebrate dive`
- returned (id 248): ` possibility, and always guard the game.equal opportunity employer: we celebrate dive`
- returned (id 2822356): `sional growth both locally and globally.equal opportunity employer: we celebrate dive`

### `from`: 56 missed

- MISSED (id 248): `rtunity employer. we welcome applicants from all backgrounds and do not discriminate`
- MISSED (id 2449): ` lives. with a presence across greece - from stores and offices to distribution cent`
- MISSED (id 2822356): `ock exchange, bally's intralot benefits from access to international capital markets`
- MISSED (id 5287076): `ce, you'll have the flexibility to work from our three modern, sustainable, and stat`

### `disability`: 56 missed

- MISSED (id 248): `age, marital status, medical condition, disability, or any other protected status. our pre`
- MISSED (id 2449): `r, sexual orientation, national origin, disability, or any other characteristic protected `
- MISSED (id 2822356): `age, marital status, medical condition, disability, or any other protected status. our pre`
- MISSED (id 5287075): `l or ethnic origin, religion or belief, disability, age, sexual orientation or marital sta`

### `engineers`: 7 missed

- MISSED (id 5287075): `ide leadership and guidance to software engineers, serving as a mentor and role model in `
- MISSED (id 5287076): `ide leadership and guidance to software engineers, serving as a mentor and role model in `
- MISSED (id 5287083): `ide leadership and guidance to software engineers, serving as a mentor and role model in `
- MISSED (id 5294191): `lines under the guidance of more senior engineers, using programming languages such as py`

### `enginee*`: 43 missed

- MISSED (id 248): `network engineer (customer ict)`
- MISSED (id 2822356): `systems engineer`
- MISSED (id 5287075): `lead software engineer (spring, spring boot)`
- MISSED (id 5287076): `lead software engineer (spring, spring boot)`

### `engineer*`: 43 missed

- MISSED (id 248): `network engineer (customer ict)`
- MISSED (id 2822356): `systems engineer`
- MISSED (id 5287075): `lead software engineer (spring, spring boot)`
- MISSED (id 5287076): `lead software engineer (spring, spring boot)`

### `engi*`: 45 missed

- MISSED (id 248): `network engineer (customer ict)`
- MISSED (id 2822356): `systems engineer`
- MISSED (id 5287075): `lead software engineer (spring, spring boot)`
- MISSED (id 5287076): `lead software engineer (spring, spring boot)`

### `senio*`: 19 missed

- MISSED (id 5294191): `ta pipelines under the guidance of more senior engineers, using programming languages`
- MISSED (id 5352791): `senior electrical design engineer`
- MISSED (id 5352803): `senior project development analyst`
- MISSED (id 5353538): `senior cloud architecture engineer (ict )`

### `senior*`: 3 missed

- MISSED (id 5631766): `mid/senior it business analyst (agile)`
- MISSED (id 5631866): `mid/senior it business analyst (agile)`
- MISSED (id 5631888): `mid/senior it business analyst (agile)`
- returned (id 5294191): `ta pipelines under the guidance of more senior engineers, using programming languages `
- returned (id 5352791): `senior electrical design engineer`

### `seni*`: 19 missed

- MISSED (id 5294191): `ta pipelines under the guidance of more senior engineers, using programming language`
- MISSED (id 5352791): `senior electrical design engineer`
- MISSED (id 5352803): `senior project development analyst`
- MISSED (id 5353538): `senior cloud architecture engineer (ict )`

### `stores`: 31 missed

- MISSED (id 2430): `butcher saleswomen for our stores in volos`
- MISSED (id 2449): `s. with a presence across greece - from stores and offices to distribution centers and`
- MISSED (id 5303536): `evements in numbers3,000+ people | 100+ stores | 2 logistics centers - 77.000 sqm | 2 `
- MISSED (id 5352913): ` the food trade area with more than 500 stores, retail, wholesale and franchise stores`

### `stor*`: 43 missed

- MISSED (id 2430): `butcher saleswomen for our stores in volos`
- MISSED (id 2449): `s. with a presence across greece - from stores and offices to distribution centers a`
- MISSED (id 5294188): `infrastructure components like servers, storage systems, and networking. understandi`
- MISSED (id 5294189): `also created new challenges in how they store, engineer, and extract value from it. `


## Returned by the server although the whitespace rule (`ws`) says no

The server splits words in a way that differs from `ws` for these postings. Text around the first occurrence of the word:

### `senior`: 1 posting(s)

- id 5356231: `data engineer (senior-lead)`

### `store`: 9 posting(s)

- id 2430: ``
- id 2449: ``
- id 5303536: ``
- id 5354952: ``

### `lead`: 15 posting(s)

- id 248: ``
- id 2822356: ``
- id 5294187: ``
- id 5294188: ``

### `analyst`: 3 posting(s)

- id 2449: ``
- id 5294189: ``
- id 5356231: ``

### `drive`: 3 posting(s)

- id 2449: ``
- id 5355811: ``
- id 5355890: ``

### `other`: 1 posting(s)

- id 5353776: ``

### `equal`: 1 posting(s)

- id 2449: ``

### `engin`: 43 posting(s)

- id 248: ``
- id 2822356: ``
- id 5287075: ``
- id 5287076: ``

### `manag`: 63 posting(s)

- id 248: ``
- id 2449: ``
- id 2822356: ``
- id 5287075: ``

### `busi`: 62 posting(s)

- id 2449: ``
- id 5287075: ``
- id 5287076: ``
- id 5287082: ``

### `year`: 43 posting(s)

- id 248: ``
- id 2449: ``
- id 2822356: ``
- id 5308127: ``

### `benefit`: 57 posting(s)

- id 248: ``
- id 2822356: ``
- id 5287075: ``
- id 5287076: ``

### `consult`: 23 posting(s)

- id 5291141: ``
- id 5294187: ``
- id 5294188: ``
- id 5294189: ``

### `futur`: 59 posting(s)

- id 248: ``
- id 2822356: ``
- id 5287075: ``
- id 5287076: ``

### `peopl`: 44 posting(s)

- id 2449: ``
- id 5294187: ``
- id 5294188: ``
- id 5294189: ``

### `build`: 33 posting(s)

- id 2822356: ``
- id 5287075: ``
- id 5287076: ``
- id 5287082: ``

### `energi`: 20 posting(s)

- id 5352746: ``
- id 5352764: ``
- id 5352766: ``
- id 5352791: ``

### `softwar`: 26 posting(s)

- id 2822356: ``
- id 5287075: ``
- id 5287076: ``
- id 5287082: ``


Reading: columns title, desc, desc<=500 and substring give TP/FP/FN against that rule. A keyword whose returned postings are all TP for `title` and with few FN means the filter searches the title (exact words). FN under `desc` with TP under `desc<=500` means only the start of the description is indexed. FP under every rule means the server matches text we do not hold (translation, extracted keywords). Starred keywords are compared as prefixes; if their FN stay high under every rule, the asterisk is not a prefix wildcard.