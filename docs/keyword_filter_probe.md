# Keyword filter probe: kariera.gr, 2026-03

| probe | keywords | logic | count | seconds | first 100: keyword in title | in description | in description only | note |
|---|---|---|---:|---:|---:|---:|---:|---|
| no keyword (month total) | - | - | 6,953 | 25 | - | - | - |  |
| energy | ['energy'] | - | 0 | 0 | - | - | - |  |
| nurse | ['nurse'] | - | 0 | 1 | - | - | - |  |
| driver | ['driver'] | - | 525 | 4 | 18 | 96 | 82 |  |
| hotel | ['hotel'] | - | 1,748 | 1 | 8 | 99 | 92 |  |
| energy, logic=or with nurse | ['energy', 'nurse'] | or | 0 | 0 | - | - | - |  |
| energy, logic=and with nurse | ['energy', 'nurse'] | and | 0 | 0 | - | - | - |  |
| energy, logic=OR with nurse | ['energy', 'nurse'] | OR | - | 0 | - | - | - | HTTP 422: {"detail": [{"type": "enum", "loc": ["form", "keywords_logic"], "msg": "Input should be 'and' or 'or'", "ctx": {"expecte |
| ENERGY (upper case) | ['ENERGY'] | - | 0 | 0 | - | - | - |  |
| energ (stem) | ['energ'] | - | 12 | 0 | 0 | 12 | 12 |  |

Reading: a count that falls when `and` is used and rises when `or` is used means the logic parameter works as named; a large 'in description only' column means the filter searches the description; identical counts for 'energy', 'ENERGY' and the other cases show case-insensitivity or its absence; 'energ' matching more than 'energy' shows stem matching.