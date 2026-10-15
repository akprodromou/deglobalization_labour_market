# Keyword index experiment: jobbland.se, 2024-06

Sample: 100 postings (page 1 of 2,879). For each keyword the server was asked which of these ids match. Per rule: TP = returned and rule says match, FP = returned but rule says no, FN = rule says match but not returned. The best rule is the one with the highest F1.

## A title word

| keyword | returned | best rule | TP / FP / FN (best) | title | desc | stem | substring | ws | note |
|---|---:|---|---|---|---|---|---|---|---|
| `wanted` | 48 | title|desc (F1 1.00) | 48/0/0 | 47/1/0 | 6/42/0 | 0/48/0 | 48/0/0 | 48/0/0 |  |
| `recording` | 45 | desc (F1 1.00) | 45/0/0 | 19/26/0 | 45/0/0 | 0/45/0 | 45/0/0 | 44/1/0 |  |
| `commercial` | 26 | ws (F1 1.00) | 26/0/0 | 14/12/0 | 23/3/1 | 0/26/0 | 26/0/3 | 26/0/0 |  |
| `looking` | 95 | title|desc (F1 1.00) | 95/0/0 | 14/81/0 | 93/2/0 | 0/95/0 | 95/0/0 | 95/0/0 |  |
| `film` | 27 | title|desc (F1 1.00) | 27/0/0 | 13/14/0 | 23/4/0 | 27/0/14 | 27/0/14 | 27/0/0 |  |
| `years` | 31 | title|desc (F1 1.00) | 31/0/0 | 11/20/0 | 27/4/0 | 0/31/0 | 31/0/2 | 31/0/0 |  |
| `woman` | 16 | desc (F1 1.00) | 16/0/0 | 11/5/0 | 16/0/0 | 16/0/0 | 16/0/0 | 16/0/0 |  |
| `extras` | 17 | ws (F1 1.00) | 17/0/0 | 9/8/1 | 17/0/31 | 0/17/0 | 17/0/44 | 17/0/0 |  |

## B early in description

| keyword | returned | best rule | TP / FP / FN (best) | title | desc | stem | substring | ws | note |
|---|---:|---|---|---|---|---|---|---|---|
| `hello` | 38 | desc (F1 1.00) | 38/0/0 | 0/38/0 | 38/0/0 | 38/0/0 | 38/0/0 | 38/0/0 |  |
| `role` | 36 | desc (F1 1.00) | 36/0/0 | 0/36/0 | 36/0/0 | 36/0/5 | 36/0/5 | 35/1/0 |  |
| `where` | 33 | desc (F1 1.00) | 33/0/0 | 0/33/0 | 33/0/0 | 33/0/0 | 33/0/2 | 33/0/0 |  |
| `place` | 28 | desc (F1 1.00) | 28/0/0 | 0/28/0 | 28/0/0 | 28/0/0 | 28/0/2 | 28/0/0 |  |
| `date` | 25 | ws (F1 1.00) | 25/0/0 | 0/25/0 | 25/0/1 | 25/0/5 | 25/0/10 | 25/0/0 |  |
| `taken` | 20 | desc (F1 1.00) | 20/0/0 | 0/20/0 | 20/0/0 | 20/0/0 | 20/0/0 | 20/0/0 |  |
| `picture` | 17 | desc (F1 1.00) | 17/0/0 | 0/17/0 | 17/0/0 | 0/17/0 | 17/0/7 | 17/0/0 |  |
| `available` | 17 | desc (F1 1.00) | 17/0/0 | 0/17/0 | 17/0/0 | 0/17/0 | 17/0/0 | 17/0/0 |  |

## C late in description

| keyword | returned | best rule | TP / FP / FN (best) | title | desc | stem | substring | ws | note |
|---|---:|---|---|---|---|---|---|---|---|
| `good` | 17 | desc (F1 1.00) | 17/0/0 | 0/17/0 | 17/0/0 | 17/0/0 | 17/0/0 | 17/0/0 |  |
| `other` | 16 | desc (F1 1.00) | 16/0/0 | 0/16/0 | 16/0/0 | 16/0/0 | 16/0/7 | 16/0/0 |  |
| `also` | 13 | desc (F1 1.00) | 13/0/0 | 0/13/0 | 13/0/0 | 13/0/0 | 13/0/0 | 13/0/0 |  |
| `position` | 13 | desc (F1 1.00) | 13/0/0 | 0/13/0 | 13/0/0 | 0/13/0 | 13/0/0 | 13/0/0 |  |
| `which` | 12 | desc (F1 1.00) | 12/0/0 | 0/12/0 | 12/0/0 | 12/0/0 | 12/0/0 | 12/0/0 |  |
| `employee` | 11 | desc (F1 1.00) | 11/0/0 | 0/11/0 | 11/0/0 | 0/11/0 | 11/0/0 | 11/0/0 |  |
| `only` | 11 | desc (F1 1.00) | 11/0/0 | 0/11/0 | 11/0/0 | 0/11/0 | 11/0/0 | 11/0/0 |  |
| `here` | 11 | desc (F1 1.00) | 11/0/0 | 0/11/0 | 11/0/0 | 11/0/0 | 11/0/37 | 11/0/0 |  |

## D variants

| keyword | returned | best rule | TP / FP / FN (best) | title | desc | stem | substring | ws | note |
|---|---:|---|---|---|---|---|---|---|---|
| `wanteds` | 0 | (no match anywhere) | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 |  |
| `wante` | 0 | title (F1 1.00) | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/50 | 0/0/0 |  |
| `wante*` | 0 | stem (F1 1.00) | 0/0/0 | 0/0/49 | 0/0/6 | 0/0/0 | 0/0/50 | 0/0/50 |  |
| `wanted*` | 48 | title|desc (F1 1.00) | 48/0/0 | 47/1/0 | 6/42/0 | 0/48/0 | 48/0/0 | 48/0/0 |  |
| `want*` | 22 | desc (F1 0.86) | 22/0/7 | 7/15/42 | 22/0/7 | 0/22/0 | 22/0/43 | 22/0/43 |  |
| `recordings` | 0 | (no match anywhere) | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 |  |
| `recordin` | 0 | title (F1 1.00) | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/45 | 0/0/0 |  |
| `recordin*` | 0 | stem (F1 1.00) | 0/0/0 | 0/0/19 | 0/0/45 | 0/0/0 | 0/0/45 | 0/0/44 |  |
| `recording*` | 45 | desc (F1 1.00) | 45/0/0 | 19/26/0 | 45/0/0 | 0/45/0 | 45/0/0 | 44/1/0 |  |
| `reco*` | 0 | stem (F1 1.00) | 0/0/0 | 0/0/19 | 0/0/46 | 0/0/0 | 0/0/46 | 0/0/45 |  |
| `commercials` | 7 | title|desc (F1 1.00) | 7/0/0 | 5/2/0 | 2/5/0 | 0/7/0 | 7/0/0 | 7/0/0 |  |
| `commercia` | 0 | title (F1 1.00) | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/29 | 0/0/0 |  |
| `commercia*` | 0 | stem (F1 1.00) | 0/0/0 | 0/0/19 | 0/0/25 | 0/0/0 | 0/0/29 | 0/0/29 |  |
| `commercial*` | 26 | title|desc (F1 0.95) | 26/0/3 | 18/8/1 | 23/3/2 | 0/26/0 | 26/0/3 | 26/0/3 |  |
| `comm*` | 0 | stem (F1 1.00) | 0/0/0 | 0/0/20 | 0/0/42 | 0/0/0 | 0/0/47 | 0/0/46 |  |

## E extra keywords

| keyword | returned | best rule | TP / FP / FN (best) | title | desc | stem | substring | ws | note |
|---|---:|---|---|---|---|---|---|---|---|
| `commerci` | 0 | title (F1 1.00) | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/28 | 0/0/29 | 0/0/0 |  |
| `record` | 2 | desc (F1 1.00) | 2/0/0 | 0/2/0 | 2/0/0 | 2/0/43 | 2/0/44 | 2/0/0 |  |

## Which rule fits best

| rule | number of keywords where it fits best |
|---|---:|
| desc | 20 |
| title|desc | 7 |
| stem | 5 |
| title | 4 |
| ws | 3 |

## Postings that contain the keyword (title or description) but were not returned

Up to 4 missed postings (and 2 returned ones for comparison) per keyword, 40 characters either side of the first occurrence.

### `commercial`: 1 missed

- MISSED (id 1623611): ` the background of que for 1 scene in a commercial.there will be breakfast and lovely snac`
- returned (id 1623533): ` women 20-50 years old are wanted for a commercial for a chocolate brand!`
- returned (id 1623538): `participating in a commercial, filming in stockholm`

### `extras`: 31 missed

- MISSED (id 1623534): `on invoice location: stockholmcategory: extras/actorspublished: 28/6 invoice: sek 5,00`
- MISSED (id 1623535): `self tape! location: stockholmcategory: extras/actorspublished: 28/6 invoice: sek 2,50`
- MISSED (id 1623536): `self tape! location: stockholmcategory: extras/actorspublished: 28/6 invoice: sek 2,00`
- MISSED (id 1623538): ` to apply! location: stockholmcategory: extras/actorspublished: 28/6 invoice: sek 5,00`
- returned (id 1623537): `looking for extras aged 25-55 for a recording on august 19`
- returned (id 1623549): `he spirit of the 1950s! !warm greetings extras department art&bob location: stockholmc`

### `date`: 1 missed

- MISSED (id 1623603): `oductions, background in theater/acting.date of recording: 4/7recording in the stock`
- returned (id 1623535): `ted in front of the camera is required. date: august 19, 2024 times: about half a da`
- returned (id 1623536): `le lines that have an element of humor. date: august 19, 2024 times: about half a da`

### `wante*`: 50 missed

- MISSED (id 1623533): `tistics - fit women 20-50 years old are wanted for a commercial for a chocolate brand`
- MISSED (id 1623534): `children with size 104 wanted for campaign film!`
- MISSED (id 1623541): `mom wanted for nice fire film (probono)`
- MISSED (id 1623543): `1x female actor wanted for a simple production for a retail c`

### `want*`: 43 missed

- MISSED (id 1623533): `tistics - fit women 20-50 years old are wanted for a commercial for a chocolate bran`
- MISSED (id 1623534): `children with size 104 wanted for campaign film!`
- MISSED (id 1623541): `mom wanted for nice fire film (probono)`
- MISSED (id 1623543): `1x female actor wanted for a simple production for a retail `
- returned (id 1623564): `male extra wanted for commercial for food company`
- returned (id 1623573): `families wanted for a commercial for gröna lund in st`

### `recordin*`: 45 missed

- MISSED (id 1623533): `colate brand! salary sek 999 as salary. recording july 4th. sincerely, cara location: st`
- MISSED (id 1623535): `ed 20-25 to play an office worker for a recording on august 19`
- MISSED (id 1623536): ` woman aged 30-40 to play manager for a recording on august 19`
- MISSED (id 1623537): `looking for extras aged 25-55 for a recording on august 19`

### `reco*`: 46 missed

- MISSED (id 1623533): `colate brand! salary sek 999 as salary. recording july 4th. sincerely, cara location`
- MISSED (id 1623535): `ed 20-25 to play an office worker for a recording on august 19`
- MISSED (id 1623536): ` woman aged 30-40 to play manager for a recording on august 19`
- MISSED (id 1623537): `looking for extras aged 25-55 for a recording on august 19`

### `commercia*`: 29 missed

- MISSED (id 1623533): ` women 20-50 years old are wanted for a commercial for a chocolate brand!`
- MISSED (id 1623538): `participating in a commercial, filming in stockholm`
- MISSED (id 1623539): `cocker spaniel for filming commercials for beauty companies`
- MISSED (id 1623548): `children for a commercial for a well-known coffee brand.`

### `commercial*`: 3 missed

- MISSED (id 1623593): `female participation in commercials in financial services`
- MISSED (id 1623611): ` the background of que for 1 scene in a commercial.there will be breakfast and lovely snac`
- MISSED (id 1623612): `s is especially common when testing for commercials. therefore, we will work especially wi`
- returned (id 1623533): ` women 20-50 years old are wanted for a commercial for a chocolate brand!`
- returned (id 1623538): `participating in a commercial, filming in stockholm`

### `comm*`: 46 missed

- MISSED (id 1623533): ` women 20-50 years old are wanted for a commercial for a chocolate brand!`
- MISSED (id 1623538): `participating in a commercial, filming in stockholm`
- MISSED (id 1623539): `cocker spaniel for filming commercials for beauty companies`
- MISSED (id 1623548): `children for a commercial for a well-known coffee brand.`


## Returned by the server although the whitespace rule (`ws`) says no

The server splits words in a way that differs from `ws` for these postings. Text around the first occurrence of the word:

### `recording`: 1 posting(s)

- id 1623593: `. you who send video have an advantage=)recording date: august 8 (we want to fill the rol`

### `role`: 1 posting(s)

- id 1623609: `vailable and discussed depending on the role's effort .are you interested? then send`


Reading: columns title, desc, desc<=500 and substring give TP/FP/FN against that rule. A keyword whose returned postings are all TP for `title` and with few FN means the filter searches the title (exact words). FN under `desc` with TP under `desc<=500` means only the start of the description is indexed. FP under every rule means the server matches text we do not hold (translation, extracted keywords). Starred keywords are compared as prefixes; if their FN stay high under every rule, the asterisk is not a prefix wildcard.