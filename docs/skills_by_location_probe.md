# skills-by-location probe: kariera.gr, 2025-03

## A. Default limit

Parameters: `{"limit": 100, "source": "kariera.gr", "from_date": "2025-03-01", "to_date": "2025-03-31"}`

HTTP 200, 1 s.

Rows: **100**.
Fields of the first row: `['location_code', 'Var1', 'label', 'Freq']`.
Numeric fields: `['Freq']`.
Sorted by `Freq` descending: **yes** (first 396, last 32); sum of `Freq` over the rows: 8,623.
Distinct `location_code` values: 1 (EL).

First 10 rows as returned:

```json
[
 {
  "location_code": "EL",
  "Var1": "http://data.europa.eu/esco/skill/15d76317-c71a-4fa2-aadc-2ecc34e627b7",
  "label": "communication",
  "Freq": 396
 },
 {
  "location_code": "EL",
  "Var1": "http://data.europa.eu/esco/skill/199f7919-5114-41b6-b6a5-41e0e4896ec1",
  "label": "assume responsibility",
  "Freq": 369
 },
 {
  "location_code": "EL",
  "Var1": "http://data.europa.eu/esco/skill/082967d4-b94c-4305-aa13-35a6aa8c5c7c",
  "label": "cooperate with colleagues",
  "Freq": 305
 },
 {
  "location_code": "EL",
  "Var1": "http://data.europa.eu/esco/skill/f683ae1d-cb7c-4aa1-b9fe-205e1bd23535",
  "label": "use microsoft office",
  "Freq": 290
 },
 {
  "location_code": "EL",
  "Var1": "http://data.europa.eu/esco/skill/a8d24a95-47b3-4f88-92e7-06600bcd3612",
  "label": "manage personal professional development",
  "Freq": 279
 },
 {
  "location_code": "EL",
  "Var1": "http://data.europa.eu/esco/skill/0e21e183-e787-4f23-a240-93b416c088c2",
  "label": "maintain personal hygiene standards",
  "Freq": 270
 },
 {
  "location_code": "EL",
  "Var1": "http://data.europa.eu/esco/skill/6d3edede-8951-4621-a835-e04323300fa0",
  "label": "English",
  "Freq": 267
 },
 {
  "location_code": "EL",
  "Var1": "http://data.europa.eu/esco/skill/e37d64dc-0f05-4ee8-b065-bf76f70d8f5c",
  "label": "respect confidentiality obligations",
  "Freq": 261
 },
 {
  "location_code": "EL",
  "Var1": "http://data.europa.eu/esco/skill/ea4ebfa1-e17a-4416-ac54-955f33e6ade7",
  "label": "Greek",
  "Freq": 202
 },
 {
  "location_code": "EL",
  "Var1": "http://data.europa.eu/esco/skill/a15dab55-f1da-4f85-ae3e-2b5c5b5333ca",
  "label": "provide high quality customer service",
  "Freq": 199
 }
]
```

## B. limit=1000

Parameters: `{"limit": 1000, "source": "kariera.gr", "from_date": "2025-03-01", "to_date": "2025-03-31"}`

HTTP 200, 6 s.

Rows: **1,000**.
Fields of the first row: `['location_code', 'Var1', 'label', 'Freq']`.
Numeric fields: `['Freq']`.
Sorted by `Freq` descending: **yes** (first 396, last 2); sum of `Freq` over the rows: 15,717.
Distinct `location_code` values: 1 (EL).

First 10 rows as returned:

```json
[
 {
  "location_code": "EL",
  "Var1": "http://data.europa.eu/esco/skill/15d76317-c71a-4fa2-aadc-2ecc34e627b7",
  "label": "communication",
  "Freq": 396
 },
 {
  "location_code": "EL",
  "Var1": "http://data.europa.eu/esco/skill/199f7919-5114-41b6-b6a5-41e0e4896ec1",
  "label": "assume responsibility",
  "Freq": 369
 },
 {
  "location_code": "EL",
  "Var1": "http://data.europa.eu/esco/skill/082967d4-b94c-4305-aa13-35a6aa8c5c7c",
  "label": "cooperate with colleagues",
  "Freq": 305
 },
 {
  "location_code": "EL",
  "Var1": "http://data.europa.eu/esco/skill/f683ae1d-cb7c-4aa1-b9fe-205e1bd23535",
  "label": "use microsoft office",
  "Freq": 290
 },
 {
  "location_code": "EL",
  "Var1": "http://data.europa.eu/esco/skill/a8d24a95-47b3-4f88-92e7-06600bcd3612",
  "label": "manage personal professional development",
  "Freq": 279
 },
 {
  "location_code": "EL",
  "Var1": "http://data.europa.eu/esco/skill/0e21e183-e787-4f23-a240-93b416c088c2",
  "label": "maintain personal hygiene standards",
  "Freq": 270
 },
 {
  "location_code": "EL",
  "Var1": "http://data.europa.eu/esco/skill/6d3edede-8951-4621-a835-e04323300fa0",
  "label": "English",
  "Freq": 267
 },
 {
  "location_code": "EL",
  "Var1": "http://data.europa.eu/esco/skill/e37d64dc-0f05-4ee8-b065-bf76f70d8f5c",
  "label": "respect confidentiality obligations",
  "Freq": 261
 },
 {
  "location_code": "EL",
  "Var1": "http://data.europa.eu/esco/skill/ea4ebfa1-e17a-4416-ac54-955f33e6ade7",
  "label": "Greek",
  "Freq": 202
 },
 {
  "location_code": "EL",
  "Var1": "http://data.europa.eu/esco/skill/a15dab55-f1da-4f85-ae3e-2b5c5b5333ca",
  "label": "provide high quality customer service",
  "Freq": 199
 }
]
```

## C. One country (GR)

Parameters: `{"limit": 100, "source": "kariera.gr", "location_code": "GR", "from_date": "2025-03-01", "to_date": "2025-03-31"}`

HTTP 200, 0 s.

Rows: **0**.

First 10 rows as returned:

```json
[]
```

## D. The next month (2025-04)

Parameters: `{"limit": 100, "source": "kariera.gr", "from_date": "2025-04-01", "to_date": "2025-04-30"}`

HTTP 200, 1 s.

Rows: **100**.
Fields of the first row: `['location_code', 'Var1', 'label', 'Freq']`.
Numeric fields: `['Freq']`.
Sorted by `Freq` descending: **yes** (first 198, last 16); sum of `Freq` over the rows: 3,996.
Distinct `location_code` values: 1 (EL).

First 10 rows as returned:

```json
[
 {
  "location_code": "EL",
  "Var1": "http://data.europa.eu/esco/skill/15d76317-c71a-4fa2-aadc-2ecc34e627b7",
  "label": "communication",
  "Freq": 198
 },
 {
  "location_code": "EL",
  "Var1": "http://data.europa.eu/esco/skill/082967d4-b94c-4305-aa13-35a6aa8c5c7c",
  "label": "cooperate with colleagues",
  "Freq": 155
 },
 {
  "location_code": "EL",
  "Var1": "http://data.europa.eu/esco/skill/199f7919-5114-41b6-b6a5-41e0e4896ec1",
  "label": "assume responsibility",
  "Freq": 151
 },
 {
  "location_code": "EL",
  "Var1": "http://data.europa.eu/esco/skill/6d3edede-8951-4621-a835-e04323300fa0",
  "label": "English",
  "Freq": 148
 },
 {
  "location_code": "EL",
  "Var1": "http://data.europa.eu/esco/skill/f683ae1d-cb7c-4aa1-b9fe-205e1bd23535",
  "label": "use microsoft office",
  "Freq": 130
 },
 {
  "location_code": "EL",
  "Var1": "http://data.europa.eu/esco/skill/ea4ebfa1-e17a-4416-ac54-955f33e6ade7",
  "label": "Greek",
  "Freq": 125
 },
 {
  "location_code": "EL",
  "Var1": "http://data.europa.eu/esco/skill/a8d24a95-47b3-4f88-92e7-06600bcd3612",
  "label": "manage personal professional development",
  "Freq": 123
 },
 {
  "location_code": "EL",
  "Var1": "http://data.europa.eu/esco/skill/0e21e183-e787-4f23-a240-93b416c088c2",
  "label": "maintain personal hygiene standards",
  "Freq": 120
 },
 {
  "location_code": "EL",
  "Var1": "http://data.europa.eu/esco/skill/e37d64dc-0f05-4ee8-b065-bf76f70d8f5c",
  "label": "respect confidentiality obligations",
  "Freq": 110
 },
 {
  "location_code": "EL",
  "Var1": "http://data.europa.eu/esco/skill/a15dab55-f1da-4f85-ae3e-2b5c5b5333ca",
  "label": "provide high quality customer service",
  "Freq": 95
 }
]
```

Reading: compare the row counts of A and B (a cap or not), check whether the numeric field counts postings or skill mentions by comparing it with a known monthly total for the source (Report Section 9.3), and whether C and D differ from A. A month without tags should return an empty list.